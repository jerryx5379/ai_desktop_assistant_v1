from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTextBrowser
)
from PySide6.QtCore import Qt, QEvent, QTimer


import pathlib
import json

from .chat_box import ChatBox
from .user_input import UserInput
from widgets.chat_box import ChatBubble


from PySide6.QtWidgets import (
    QHBoxLayout,QPushButton,QTextBrowser
)
from PySide6.QtGui import QTextCursor, QFontMetrics
from PySide6.QtCore import QThread, QTimer, Qt

import markdown
from pygments.formatters.html import HtmlFormatter

from threads import OllamaWorker
from widgets.chat_box import chat_bubble

from logic import ChatController

class MainChatWindow(QWidget):  
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Assistant")
        self.setMinimumSize(150,250) 
        #self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        
        self.main_layout = QVBoxLayout(self)

        self.chat_box = ChatBox()
        self.user_input = UserInput() 

        self.main_layout.addWidget(self.chat_box)
        self.main_layout.addLayout(self.user_input)

        self.chat_controller = ChatController(chat_box=self.chat_box, user_input=self.user_input)

        self.user_input.send_message_signal.connect(self.chat_controller.send_message)

        self.config_path = pathlib.Path.home() / ".Ollama_project_config.json"

    ### Event Overrides ###
    def showEvent(self, event): 
        super().showEvent(event)
        self.open_in_prev_location()
        

    def closeEvent(self, event):  
        self.save_window_location()
        event.accept()  

    def changeEvent(self, event: QEvent):
        super().changeEvent(event)
        if event.type() == QEvent.Type.WindowStateChange:
            old_state = event.oldState()
            if self.isMinimized():
                self.save_window_location()

            elif old_state & Qt.WindowState.WindowMinimized:
                self.open_in_prev_location()


    ### Helper Functions ###
    def open_in_prev_location(self):
        if self.config_path.exists():
            with open(self.config_path, "r") as f:
                settings = json.load(f)
                self.move(*settings["pos"])
                self.resize(*settings["size"])

    def save_window_location(self):
        settings = {
            "pos": [self.pos().x(), self.pos().y()],
            "size": [self.size().width(), self.size().height()]
        }
        with open(self.config_path, "w") as f:
            json.dump(settings, f)
    
    

    




