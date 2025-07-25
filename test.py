from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QTextEdit, QSizePolicy
)
from PySide6.QtCore import Qt
import sys


class UserInputWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("""
            QTextEdit {
                border: 1px solid #ccc;
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
            }

            QPushButton {
                padding: 6px 12px;
                border-radius: 6px;
                background-color: #f0f0f0;
            }

            QPushButton:hover {
                background-color: #e0e0e0;
            }

            QPushButton#sendButton {
                background-color: #10a37f;
                color: white;
            }

            QPushButton#sendButton:hover {
                background-color: #0e8f6e;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(8)
        main_layout.setContentsMargins(8, 8, 8, 8)

        # Input box
        self.input_textbox = QTextEdit()
        self.input_textbox.setPlaceholderText("Send a message...")
        self.input_textbox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.input_textbox.setFixedHeight(80)
        main_layout.addWidget(self.input_textbox)

        # Bottom layout with buttons
        button_layout = QHBoxLayout()

        # Left buttons
        self.button1 = QPushButton("Button 1")
        self.button2 = QPushButton("Button 2")
        self.button3 = QPushButton("Button 3")
        button_layout.addWidget(self.button1)
        button_layout.addWidget(self.button2)
        button_layout.addWidget(self.button3)

        button_layout.addStretch()  # Push right button to the far right

        # Right send button
        self.send_button = QPushButton("Send")
        self.send_button.setObjectName("sendButton")
        button_layout.addWidget(self.send_button)

        main_layout.addLayout(button_layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chat Input Example")
        self.setCentralWidget(UserInputWidget())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(600, 200)
    window.show()
    sys.exit(app.exec())
