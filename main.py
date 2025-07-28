"""
This is the entry point to the application.
This file creates the application and starts the event loop
It also sets application level details like system name of this app, application style
"""

# TODO: add load model and unload model on program start and end
# TODO: add save chat on program close

# This version TODO: 
# Add a tool bar at the top of the chat:
# 1. clear chat -> clear chat and save chat
# 2. previous chats -> new window: previous chats 
# 3. on program/window close, save chat

# plan:
# first create the tool bar on top
# then add funcitonality


from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase, QFont

import sys

from widgets import MainChatWindow
from app import create_app

def main():
    app = create_app()

    window = MainChatWindow() 
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()


    