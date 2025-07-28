import sys
from PySide6.QtWidgets import (
    QTextEdit
)

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QResizeEvent

class InputTextBox(QTextEdit):
    send_message_signal = Signal()

    def __init__(self, send_button):  
        super().__init__()
        self.setObjectName("inputTextBox")
        self.setFixedHeight(32) 
        self.setPlaceholderText("Ask anything...")
        self.setStyleSheet("QTextEdit { border: none;}")

        self.textChanged.connect(self.adjust_input_height) # increase input box size based on how much the user types up to 3 times the normal

        self.send_button = send_button

    def adjust_input_height(self): 
        doc = self.document()
        height = doc.size().height() + 10
        font_metrics = self.fontMetrics()
        line_height = font_metrics.lineSpacing()
        max_height = line_height * 3 + 10
        new_height = min(height, max_height)
        self.setFixedHeight(new_height)

    # When user in the inputtextbox, if they press enter/return, starts send_message. shift/ctrl + enter replaces its functionality
    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            if event.modifiers() in (Qt.ShiftModifier, Qt.ControlModifier):
                super().keyPressEvent(event) 
            else:
                if self.send_button.isEnabled():
                    self.send_message_signal.emit()
        else:
            super().keyPressEvent(event)

    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)
        self.adjust_input_height()




