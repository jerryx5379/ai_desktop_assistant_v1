from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPalette

def update_qss_theme():
    app = QApplication.instance()

    paths = ['style/app.qss']
    if is_dark_theme():
        paths.append('style/dark_theme.qss')
    else:
        paths.append('style/light_theme.qss')

    qss = ""
    for path in paths:
        with open(path, "r") as file:
            qss += file.read() + "\n"

    app.setStyleSheet(qss)


### Helper functions

def is_dark_theme():
    app = QApplication.instance()
    if not app:
        raise RuntimeError("QApplication must be initialized before checking theme.")
    
    palette = app.palette()
    window_color = palette.color(QPalette.Window)
    brightness = (
        window_color.red() * 0.299 +
        window_color.green() * 0.587 +
        window_color.blue() * 0.114
    )
    return brightness < 128

