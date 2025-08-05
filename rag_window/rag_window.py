from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QStackedWidget, QFrame
    )
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
import sys
from pathlib import Path

from .empty_screen import EmptyScreen
from .new_file_screen import NewFileScreen
from .logic import RagController


class RagWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add context to your chat")
        self.setWindowIcon(QIcon("assets/icons/app.png"))
        self.setMinimumSize(250,150) 

        self.main_layout = QVBoxLayout(self)

        self.stacked_screens = QStackedWidget()

        self.empty_screen = EmptyScreen()
        self.new_file_screen = NewFileScreen()

        self.stacked_screens.addWidget(self.empty_screen)       # Index 0 
        self.stacked_screens.addWidget(self.new_file_screen)    # Index 1

        self.main_layout.addWidget(self.stacked_screens)

        self.rag_controller = RagController(new_file_screen=self.new_file_screen)
        self.empty_screen.added_new_file.connect(self.rag_controller.added_new_file)
        self.empty_screen.added_new_file.connect(self.update_stacked_screens)
        self.new_file_screen.added_new_file.connect(self.rag_controller.added_new_file)

        self.rag_controller.load_previous_files() 
        self.update_stacked_screens()

        self.rag_controller.update_stacked_widget.connect(self.update_stacked_screens)

    def update_stacked_screens(self):
        layout = self.new_file_screen.get_new_screen_layout()

        empty = True
        for i in range(layout.count()):
            item = layout.itemAt(i)
            widget = item.widget()
            if isinstance(widget, QFrame):
                empty = False
        
        if empty:
            self.stacked_screens.setCurrentIndex(0)
        else:
            self.stacked_screens.setCurrentIndex(1)

    





