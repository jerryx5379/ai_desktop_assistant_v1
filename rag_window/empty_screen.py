from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFrame, QSizePolicy
    )
from PySide6.QtCore import Qt, QUrl, Signal
from PySide6.QtGui import QIcon, QDragEnterEvent, QDropEvent
import sys

from util import FlowLayout


class EmptyScreen(QFrame):
    added_new_file = Signal(list)

    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setAcceptDrops(True)
        self.setStyleSheet("""
            QFrame {
                border: 4px dotted #aaa;
                border-radius: 15px;
                background-color: gray;
            }
            QLabel {
                font-size: 14px;
                border: none;
            }
        """)

        self.label = QLabel("Drag and drop PDF files for context")
        self.label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout(self)
        layout.addStretch()
        layout.addWidget(self.label)
        layout.addStretch()

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        file_paths = [url.toLocalFile() for url in urls if url.isLocalFile()]
        pdf_files = [f for f in file_paths if f.lower().endswith('.pdf')]

        if pdf_files:
            self.added_new_file.emit(pdf_files)
        event.acceptProposedAction()








