from PySide6.QtWidgets import (
    QTextBrowser, QApplication, QFrame, QSizePolicy, QVBoxLayout, QLabel, QScrollArea, QWidget
)

from PySide6.QtGui import QIcon, QDragEnterEvent, QDropEvent
from PySide6.QtCore import Qt, QUrl, Signal


class NewFileScreen(QFrame):
    added_new_file = Signal(list)

    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setAcceptDrops(True)


        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.main_layout.addWidget(self.scroll_area)

        self.scroll_content = QWidget()
        self.scroll_content.setObjectName("newFileScreenScrollContent")
        self.scroll_area.setWidget(self.scroll_content)

        self.new_screen_layout = QVBoxLayout(self.scroll_content)
        self.new_screen_layout.setContentsMargins(10, 10, 10, 10)
        self.new_screen_layout.setSpacing(7)
        self.new_screen_layout.addStretch()

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        file_paths = [url.toLocalFile() for url in urls if url.isLocalFile()]
        pdf_files = [f for f in file_paths if f.lower().endswith('.pdf')]

        if pdf_files:
            self.added_new_file.emit(pdf_files)
        event.acceptProposedAction()


    ### Helper Functions ###
    def get_new_screen_layout(self):
        return self.new_screen_layout
















