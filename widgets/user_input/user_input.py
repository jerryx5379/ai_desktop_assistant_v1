from PySide6.QtWidgets import (
    QHBoxLayout,QPushButton,QTextBrowser
)
from PySide6.QtGui import QTextCursor, QFontMetrics
from PySide6.QtCore import QThread, QTimer, Qt, Signal

import markdown
from pygments.formatters.html import HtmlFormatter

from threads import OllamaWorker
from widgets.chat_box import ChatBubble
from .input_text_box import InputTextBox

class UserInput(QHBoxLayout):
    send_message_signal = Signal()

    def __init__(self):
        super().__init__()
        
        self.send_button = QPushButton("Send") 

        self.input_text = InputTextBox(send_button=self.send_button)

        self.addWidget(self.input_text) 
        self.addWidget(self.send_button) 

        self.send_button.clicked.connect(self.send_message_signal.emit)
        self.input_text.send_message_signal.connect(self.send_message_signal.emit)

    
        

        
        

        


        

        
    
