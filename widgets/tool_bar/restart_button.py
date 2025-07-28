from PySide6.QtWidgets import (
    QHBoxLayout,QPushButton,QTextBrowser,QVBoxLayout, QWidget
)
from PySide6.QtGui import QTextCursor, QFontMetrics, QIcon
from PySide6.QtCore import QThread, QTimer, Qt, Signal, QSize

import markdown
from pygments.formatters.html import HtmlFormatter

from threads import OllamaWorker
from widgets.chat_box import ChatBubble


class RestartButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.setIcon(QIcon("assets/icons/restart.svg"))
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
        self.setToolTip("Clear chat")


        