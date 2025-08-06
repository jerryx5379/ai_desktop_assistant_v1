from PySide6.QtWidgets import (
    QWidget, QVBoxLayout
)
from PySide6.QtCore import Qt, QEvent

import pathlib
import json

from .chat_box import ChatBox
from .user_input import UserInput
from .tool_bar import Toolbar

from logic import ChatController, ToolBarController, RagController

class MainChatWindow(QWidget):  
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Assistant")
        self.setMinimumSize(150,250) 
        self.setWindowOpacity(0.83)
        #self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        
        self.main_layout = QVBoxLayout(self)

        self.tool_bar = Toolbar()
        self.chat_box = ChatBox()
        self.user_input = UserInput() 

        self.main_layout.addWidget(self.tool_bar, 0)
        self.main_layout.addWidget(self.chat_box, 1)
        self.main_layout.addWidget(self.user_input, 0)


        self.tool_bar_controller = ToolBarController(chat_box=self.chat_box)
        self.tool_bar.clear_chat.connect(self.tool_bar_controller.clear_chat)
        
        self.chat_controller = ChatController(chat_box=self.chat_box, user_input=self.user_input)
        self.user_input.send_message_signal.connect(self.chat_controller.send_message)
        self.user_input.toggle_operating_system_interaction.connect(self.chat_controller.toggle_operating_system_interaction)
        self.tool_bar_controller.early_cancel.connect(self.chat_controller.set_early_cancel)

        self.rag_controller = RagController()
        self.user_input.open_rag_window_signal.connect(self.rag_controller.open_rag_window) 

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
    
    

    









