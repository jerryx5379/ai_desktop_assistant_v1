from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QScrollArea
)
from PySide6.QtCore import Qt

# this is the area where the user and assistant messages show up
class ChatBox(QScrollArea):
    MAX_CONTEXT_MESSAGES = 2
    SYS_INSTRUC = "You are a personal AI assistant. Keep your responses concise to the prompt"
    MODEL = "gemma3n:e2b"
    
    def __init__(self):
        super().__init__()
        self.setWidgetResizable(True)  # Automatically resize the QWidget inside the scrollarea to the scrollarea viewport size
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.scroll_content = QWidget() # This is the "div" that is inside scroll_area
        self.scroll_layout = QVBoxLayout(self.scroll_content) # This is the vertical layoutbox inside that "div"
        self.scroll_layout.setAlignment(Qt.AlignTop)

        self.setWidget(self.scroll_content)

        self.messages = [{"role":"system", "content": ChatBox.SYS_INSTRUC}]

    def update_chat_context(self, role:str, message:str): 
        self.messages.append({"role":role,"content":message})
        if len(self.messages) > self.MAX_CONTEXT_MESSAGES+1:
            self.messages.pop(1)

    def clear_messages(self):
        self.messages = [{"role":"system", "content": ChatBox.SYS_INSTRUC}]

    def get_data(self):
        model = ChatBox.MODEL
        data = {
            "model": model,
            "messages": self.messages
        }
        return data
    










