from PySide6.QtCore import Signal,QObject

class ToolBarController(QObject):
    early_cancel = Signal()

    def __init__(self, chat_box, tool_bar):
        super().__init__()
        self.CONVERSATION_MODE_FLAG = False

        self.chat_box = chat_box
        self.scroll_layout = self.chat_box.get_scroll_layout()
        self.scroll_content = self.chat_box.get_scroll_content()

        self.tool_bar = tool_bar
        self.conversation_button = self.tool_bar.get_conversation_button()

    def clear_chat(self): # logic for restart_button.py
        self.early_cancel.emit()
        self.chat_box.clear_context()
        self.chat_box.clear_messages()
        self.scroll_content.setMinimumHeight(0)

    def toggle_conversation_mode(self):
        if self.CONVERSATION_MODE_FLAG:
            self.CONVERSATION_MODE_FLAG = False
            self.chat_box.toggle_conversation_mode(enabled = False)
            self.conversation_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: white;
            }
            QPushButton:hover {
                background-color: #a4a6a5;  
            }
            """)  
        else:
            self.CONVERSATION_MODE_FLAG = True
            self.chat_box.toggle_conversation_mode(enabled = True)
            self.conversation_button.setStyleSheet("""
            QPushButton {
                background-color: green;
                border: none;
                color: white;
            }
            """)  
            


# have future logic for storing and retrieving old chats




















