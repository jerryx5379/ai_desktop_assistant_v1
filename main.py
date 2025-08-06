"""
This is the entry point to the application.
This file creates the application and starts the event loop
It also sets application level details like system name of this app, application style
"""


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


    
