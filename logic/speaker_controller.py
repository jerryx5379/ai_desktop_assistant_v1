from PySide6.QtWidgets import (
    QTextBrowser, QApplication
)
from PySide6.QtCore import QTimer,QThread, QObject, Slot,Signal
from PySide6.QtGui import QPalette,QTextCursor, QFontMetrics

import json
import markdown
from pygments.formatters.html import HtmlFormatter
import numpy as np
import faiss
import re

from widgets.chat_box import ChatBubble
from threads import OllamaWorker, SpeakerWorker
from core import CallableFunctions, EmbeddingModel



class SpeakerController(QObject):
    
    # 2 signals coming in 
    # toggle speaker mode
    # text chunk

    def __init__(self, tool_bar):
        super().__init__()

        self.SPEAKER_MODE_ENABLED_FLAG = False

        self.tool_bar = tool_bar
        self.speaker_button = self.tool_bar.get_speaker_button()

        self.thread = None
        self.worker = None

        # Later implement that conversation mode is enabled with speaker mode

    def new_response(self, response):
        if not self.SPEAKER_MODE_ENABLED_FLAG:
            return
        
        response = response.strip()
        print(response)

        if self.worker is not None:
            print("hi")
            self.worker.enable_early_stop()
        
            self.thread1 = QThread()
            self.thread1.setObjectName("Speaker_thread1")
            self.worker1 = SpeakerWorker(text=response)
            self.worker1.moveToThread(self.thread1)

            self.thread1.started.connect(self.worker1.text_to_speech)

            self.worker1.finished.connect(self.end_thread)

            self.thread1.start()
        
        else:
            self.thread = QThread()
            self.thread.setObjectName("Speaker_thread")
            self.worker = SpeakerWorker(text=response)
            self.worker.moveToThread(self.thread)

            self.thread.started.connect(self.worker.text_to_speech)

            self.worker.finished.connect(self.end_thread)

            self.thread.start()
    

    @Slot()
    def toggle_speaker_mode(self):
        if self.SPEAKER_MODE_ENABLED_FLAG:
            self.SPEAKER_MODE_ENABLED_FLAG = False
            self.speaker_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: white;
            }
            QPushButton:disabled {
                background-color: transparent;
            }

            QPushButton:hover {
                background-color: #a4a6a5;
            }
            """) 
        else:
            self.SPEAKER_MODE_ENABLED_FLAG = True
            self.speaker_button.setStyleSheet("""
            QPushButton {
                background-color: green;
                border: none;
                color: white;
            }
            QPushButton:disabled {
                background-color: transparent;
            }

            QPushButton:hover {
                background-color: #a4a6a5;
            }
            """) 

    
    ### Helper Functions ###
    def end_thread(self):
        self.thread.quit()
        self.thread.wait()
        self.worker.deleteLater()
        self.thread.deleteLater()

        setattr(self,'worker',None)











        