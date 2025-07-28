from PySide6.QtWidgets import (
    QHBoxLayout,QPushButton,QTextBrowser,QVBoxLayout, QWidget, QSizePolicy, QFrame
)
from PySide6.QtGui import QTextCursor, QFontMetrics, QIcon
from PySide6.QtCore import QThread, QTimer, Qt, Signal, QSize

import markdown
from pygments.formatters.html import HtmlFormatter

from threads import OllamaWorker
from widgets.chat_box import ChatBubble
from .restart_button import RestartButton
from .history_button import HistoryButton

class Toolbar(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color:gray;")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(5, 5, 5, 5) 
        self.main_layout.setSpacing(10)

        self.history_button = HistoryButton()
        self.restart_button = RestartButton()

        self.main_layout.addWidget(self.history_button)
        self.main_layout.addWidget(self.restart_button)
        self.main_layout.addStretch()




