from PySide6.QtWidgets import (
    QHBoxLayout,QVBoxLayout,QFrame, QSizePolicy
)
from PySide6.QtCore import Signal

from .input_text_box import InputTextBox
from .mic_button import MicButton
from .send_button import SendButton
from .rag_button import RagButton


class UserInput(QFrame):
    send_message_signal = Signal()
    open_rag_window_signal = Signal()

    def __init__(self):
        super().__init__()
        self.setObjectName("userInput")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)    
        

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(5,5,5,5) 
        self.main_layout.setSpacing(0)

        # Layout for the buttons (send_button, mic_button)
        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.setSpacing(10)

        self.rag_button = RagButton()
        self.mic_button = MicButton()
        self.send_button = SendButton()

        self.buttons_layout.addWidget(self.rag_button)
        self.buttons_layout.addStretch()
        self.buttons_layout.addWidget(self.mic_button)
        self.buttons_layout.addWidget(self.send_button)
        
        # User input textbox
        self.input_text = InputTextBox(send_button=self.send_button)

        # Add usertextbox and buttons layout to main layout
        self.main_layout.addWidget(self.input_text)
        self.main_layout.addLayout(self.buttons_layout)

        # Conenct signals that send the message
        self.send_button.clicked.connect(self.send_message_signal.emit)
        self.rag_button.clicked.connect(self.open_rag_window_signal.emit)
        self.input_text.send_message_signal.connect(self.send_message_signal.emit)
        self.mic_button.update_input_box.connect(self.update_user_text_box)
        self.mic_button.send_message_signal.connect(self.send_message_signal.emit)

    def get_send_button(self):
        return self.send_button
    
    def get_input_text_box(self):
        return self.input_text
    
    def update_user_text_box(self,text):
        self.input_text.setPlainText(text)

    
        

        
        

        


        

        
    
