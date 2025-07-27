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
from .send_button import SendButton

class UserInput(QVBoxLayout):
    send_message_signal = Signal()

    def __init__(self):
        super().__init__()
        self.setObjectName("userInput")

        # Layout for the buttons (send_button, mic_button)
        self.buttons_layout = QHBoxLayout()

        self.buttons_layout.addStretch()
        self.mic_button = MicButton()
        self.send_button = SendButton()

        self.buttons_layout.addWidget(self.mic_button)
        self.buttons_layout.addWidget(self.send_button)
        
        # User input textbox
        self.input_text = InputTextBox(send_button=self.send_button)

        # Add usertextbox and buttons layout to main layout
        self.addWidget(self.input_text)
        self.addLayout(self.buttons_layout)

        # Conenct signals that send the message
        self.send_button.clicked.connect(self.send_message_signal.emit)
        self.input_text.send_message_signal.connect(self.send_message_signal.emit)
        self.mic_button.update_input_box.connect(self.update_user_text_box)
        self.mic_button.send_message_signal.connect(self.send_message_signal.emit)

    def get_send_button(self):
        return self.send_button
    
    def get_input_text_box(self):
        return self.input_text
    
    def update_user_text_box(self,text):
        self.input_text.setPlainText(text)

    
        

        
        

        


        

        
    
