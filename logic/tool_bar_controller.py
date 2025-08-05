from PySide6.QtCore import Signal,QObject

class ToolBarController(QObject):
    early_cancel = Signal()

    def __init__(self, chat_box):
        super().__init__()

        self.chat_box = chat_box
        self.scroll_layout = self.chat_box.get_scroll_layout()
        self.scroll_content = self.chat_box.get_scroll_content()

    def clear_chat(self): # logic for restart_button.py
        self.early_cancel.emit()
        self.chat_box.clear_context()
        self.chat_box.clear_messages()
        self.scroll_content.setMinimumHeight(0)




# have future logic for storing and retrieving old chats




















