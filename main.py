"""
This is the entry point to the application.
This file creates the application and starts the event loop
It also sets application level details like system name of this app, application style
"""

# TODO: add load model and unload model on program start and end
# TODO: add save chat on program close
# TODO: add a icon with pyinstaller when making the exe     pyinstaller --onefile --windowed --icon="assets/icons/app_icon.ico" main.py


# This version TODO: add the the rag search button
# first maybe change it so there is a "tool"... ehh idk
# add a file button in the inputarea, 
# on button click, open another window that has folders of files that can be rag searched through. 
# have text parsers for:  pdf and docx

# Plan:
# first create a script that can take in files, create vector embeddings, then rag search that


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


    