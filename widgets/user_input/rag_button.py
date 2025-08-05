from PySide6.QtWidgets import (
    QPushButton
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize, Signal


class RagButton(QPushButton):
    open_rag_window_signal = Signal()

    def __init__(self):
        super().__init__()
        self.setIcon(QIcon("assets/icons/folder.svg"))
        self.setIconSize(QSize(24,24))
        self.setStyleSheet("""
        QPushButton {
            background-color: transparent;
            border: none;
            color: white;
        }
        QPushButton:disabled {
            background-color: transparent;
            color: #aaaaaa;
        }

        QPushButton:hover {
            background-color: #a4a6a5;
        }
        """)   

        self.clicked.connect(self.open_rag_window_signal.emit)
       