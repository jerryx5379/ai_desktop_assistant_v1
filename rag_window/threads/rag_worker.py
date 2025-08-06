from PySide6.QtWidgets import (
    QTextBrowser, QApplication
)
from PySide6.QtCore import QTimer,QThread, QObject, Signal, Slot
from PySide6.QtGui import QPalette,QTextCursor, QFontMetrics

import json
import markdown
from pygments.formatters.html import HtmlFormatter
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import re
import fitz
import os
from pathlib import Path


from core import EmbeddingModel




class RagWorker(QObject):
    finished_embeddings = Signal()
    emit_file_name = Signal(str)

    finished_aggregating = Signal()

    def __init__(self):
        super().__init__()

    @Slot()
    def pdf_to_vector_embeddings(self, pdf_paths):
        for pdf_path in pdf_paths:

            if not hasattr(self,'model'):
                self.model = EmbeddingModel.model

            text_chunks = self.parse_pdf_to_text_chunks(pdf_path=pdf_path)

            embeddings = self.model.encode(text_chunks,convert_to_numpy=True)
            faiss.normalize_L2(embeddings)

            file_name = os.path.basename(pdf_path)
            np.save(f'user_data/embeddings/{file_name}.npy', embeddings)
            np.save(f'user_data/file_text_chunks/{file_name}.npy', text_chunks)

            self.emit_file_name.emit(file_name)

        self.finished_embeddings.emit()

    @Slot()
    def aggregate_embeddings_and_create_indexes(self):
        folder = Path("user_data/embeddings")
        embedding_files = sorted(folder.glob("*.npy"))

        if not embedding_files:
            empty_npy = np.empty((0,EmbeddingModel.vector_length)) 
            np.save('user_data/embeddings/aggregated/embeddings.npy', empty_npy)

            dim = empty_npy.shape[1]
            index = faiss.IndexFlatIP(dim)
            index.add(empty_npy)
            faiss.write_index(index, "user_data/embeddings/aggregated/index.faiss")

            empty = np.array([])
            np.save('user_data/file_text_chunks/aggregated/text_chunks.npy', empty)


            self.finished_aggregating.emit()
            return

        arrays = [np.load(f) for f in embedding_files]
        stacked = np.vstack(arrays)  # Shape: (total_rows, embedding_dim)

        np.save('user_data/embeddings/aggregated/embeddings.npy', stacked)

        dim = stacked.shape[1]
        index = faiss.IndexFlatIP(dim)
        index.add(stacked)

        faiss.write_index(index, "user_data/embeddings/aggregated/index.faiss")

        # This part for the file_text_chunks
        folder = Path("user_data/file_text_chunks")
        text_chunk_files = sorted(folder.glob("*.npy"))

        arrays = [np.load(f) for f in text_chunk_files]
        combined = np.concatenate(arrays)

        np.save('user_data/file_text_chunks/aggregated/text_chunks.npy', combined)

        self.finished_aggregating.emit()




    ### Helper Functions ###

    def parse_pdf_to_text_chunks(self, pdf_path) -> list:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()

        text_chunks = re.split(r'\n\s*\n', text)
        return text_chunks



















