from PySide6.QtWidgets import (
    QPushButton
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Signal, QSize
from logic import MicButtonController

class MicButton(QPushButton):
    send_message_signal = Signal() # when the mic button is on, can automatically send messages to the chat
    update_input_box = Signal(str)

    def __init__(self):
        super().__init__()
        self.setIcon(QIcon("assets/icons/mic.svg"))
        self.setIconSize(QSize(24,24))
        self.setStyleSheet("""
        QPushButton {
            background-color: transparent;
            border: none;
        }
        QPushButton:hover {
            background-color: #a4a6a5;  
        }
        """)   

        self.clicked.connect(self.on_button_click)

        self.mic_controller = MicButtonController(self)
        self.mic_controller.send_message_signal.connect(self.send_message_signal.emit)
        self.mic_controller.update_input_box_signal.connect(self.update_user_text_box)

    def on_button_click(self):
        is_running = self.mic_controller.worker_thread and self.mic_controller.worker_thread.isRunning()
        
        if is_running:
            self.mic_controller.disable_mic_input()
        else:
            self.mic_controller.load_model_and_stream_audio()

    def update_user_text_box(self,text):
        self.update_input_box.emit(text)

