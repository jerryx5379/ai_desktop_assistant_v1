from sentence_transformers import SentenceTransformer
import faiss
import numpy as np


class EmbeddingModel:
    _model = SentenceTransformer('msmarco-MiniLM-L6-cos-v5')

    vector_length = _model.encode("test", convert_to_numpy=True).shape[-1]






