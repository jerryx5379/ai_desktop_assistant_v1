from PySide6.QtWidgets import (
    QHBoxLayout, QSizePolicy, QFrame
)
from PySide6.QtCore import Signal

from .restart_button import RestartButton
from .history_button import HistoryButton
from .conversation_button import ConversationButton
from .speaker_button import SpeakerButton

class Toolbar(QFrame):
    clear_chat = Signal()
    toggle_conversation_mode = Signal()
    toggle_speaker_mode = Signal()

    def __init__(self):
        super().__init__()
        self.setObjectName("chatWindowToolBar")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(5, 5, 5, 5) 
        self.main_layout.setSpacing(10)

        self.history_button = HistoryButton()
        self.restart_button = RestartButton()
        self.conversation_button = ConversationButton()
        self.speaker_button = SpeakerButton()


        # self.main_layout.addWidget(self.history_button) # Maybe implement later
        self.main_layout.addWidget(self.restart_button)
        self.main_layout.addStretch()
        self.main_layout.addWidget(self.conversation_button)
        self.main_layout.addWidget(self.speaker_button)

        self.restart_button.clear_chat.connect(self.clear_chat.emit)
        self.conversation_button.clicked.connect(self.toggle_conversation_mode.emit)
        self.speaker_button.clicked.connect(self.toggle_speaker_mode.emit)

    def get_conversation_button(self):
        return self.conversation_button

    def get_speaker_button(self):
        return self.speaker_button


