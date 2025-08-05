from PySide6.QtWidgets import (
    QHBoxLayout, QSizePolicy, QFrame
)
from PySide6.QtCore import Signal

from .restart_button import RestartButton
from .history_button import HistoryButton

class Toolbar(QFrame):
    clear_chat = Signal()

    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color:gray;")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(5, 5, 5, 5) 
        self.main_layout.setSpacing(10)

        self.history_button = HistoryButton()
        self.restart_button = RestartButton()

        # self.main_layout.addWidget(self.history_button) # Maybe implement later
        self.main_layout.addWidget(self.restart_button)
        self.main_layout.addStretch()

        self.restart_button.clear_chat.connect(self.clear_chat.emit)





