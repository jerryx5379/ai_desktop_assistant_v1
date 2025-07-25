"""
This is the entry point to the application.
This file creates the application and starts the event loop
It also sets application level details like system name of this app, application style
"""

# TODO: add load model and unload model on program start and end

# This version TODO: 
# 1. add voice to speech tech with openai whisper
# 2. add the text from voice to the gemma 3n model
# 3. have the model determine if the reqeust is to modify the system os
# 4. have a tool calling step


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


    