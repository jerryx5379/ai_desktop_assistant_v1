from PySide6.QtWidgets import (
    QPushButton
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize


class HistoryButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.setIcon(QIcon("assets/icons/history.svg"))
        self.setIconSize(QSize(24,24))
        self.setStyleSheet("""
        QPushButton {
            background-color: transparent;
            border: none;
            color: white;
        }
        QPushButton:hover {
            background-color: #a4a6a5;  
        }
        """)        
        self.setToolTip("Previous Chats")


        