from PySide6.QtWidgets import (
    QHBoxLayout,QPushButton,QTextBrowser,QVBoxLayout
)
from PySide6.QtGui import QTextCursor, QFontMetrics, QIcon
from PySide6.QtCore import QThread, QTimer, Qt, Signal, QSize

import markdown
from pygments.formatters.html import HtmlFormatter

from threads import OllamaWorker
from widgets.chat_box import ChatBubble
from .input_text_box import InputTextBox
from .mic_button import MicButton

class SendButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.setIcon(QIcon("assets/icons/send.svg"))
        self.setIconSize(QSize(24,24))
        self.setStyleSheet("""
QPushButton:enabled{
    background-color:gray;
}
""")