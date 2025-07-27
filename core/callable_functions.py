from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTextBrowser, QApplication
)
from PySide6.QtCore import Qt, QEvent, QTimer
from PySide6.QtGui import QPalette


import pathlib
import json

from widgets.chat_box import ChatBubble



from PySide6.QtWidgets import (
    QHBoxLayout,QPushButton,QTextBrowser
)
from PySide6.QtGui import QTextCursor, QFontMetrics
from PySide6.QtCore import QThread, QTimer, Qt, Signal

import markdown
from pygments.formatters.html import HtmlFormatter

from threads import OllamaWorker
from widgets.chat_box import ChatBubble
from PySide6.QtCore import QObject, QThread, QTimer, Qt

import subprocess

class CallableFunctions(QObject):
    finished = Signal(str)
    error = Signal(str)

    def __init__(self, result):
        super().__init__()
        self.result = result

    def call_functions(self):
        try:
            for key, value in self.result.items():
                if value == 1:
                    match key:
                        case "change_to_dark_theme":
                            self.change_system_theme_to_dark()
                            self.finished.emit("Changed system to dark theme")

                        case "change_to_light_theme":
                            self.change_system_theme_to_light()
                            self.finished.emit("Changed system to light theme")

                        case _:
                            print("callable_functions.py: no matching key")

        except Exception as e:
            self.error.emit(str(e))



    def change_system_theme_to_dark(self):
        subprocess.run([
            "reg", "add",
            r"HKCU\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
            "/v", "AppsUseLightTheme",
            "/t", "REG_DWORD",
            "/d", "0",
            "/f"
        ])
        subprocess.run([
            "reg", "add",
            r"HKCU\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
            "/v", "SystemUsesLightTheme",
            "/t", "REG_DWORD",
            "/d", "0",
            "/f"
        ])

    def change_system_theme_to_light(self):
        subprocess.run([
            "reg", "add",
            r"HKCU\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
            "/v", "AppsUseLightTheme",
            "/t", "REG_DWORD",
            "/d", "1",
            "/f"
        ])
        subprocess.run([
            "reg", "add",
            r"HKCU\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
            "/v", "SystemUsesLightTheme",
            "/t", "REG_DWORD",
            "/d", "1",
            "/f"
        ])











