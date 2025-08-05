from PySide6.QtCore import QThread,Signal,QObject

from rag_window import RagWindow

class RagController(QObject):
    
    def __init__(self):
        super().__init__()

        self.rag_window = RagWindow()

    def open_rag_window(self):
        self.rag_window.show()



















        