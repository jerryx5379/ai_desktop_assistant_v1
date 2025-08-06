from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

import sys

from util import update_qss_theme


def create_app():
    app = QApplication(sys.argv)
    app.setApplicationName("Desktop Assistant")
    app.setStyle("Fusion")      
    app.setWindowIcon(QIcon("assets/icons/app.png"))
    update_qss_theme()

    return app
