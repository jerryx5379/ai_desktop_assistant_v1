from PySide6.QtCore import QThread,Signal,QObject

from threads import MicWorker

class MicButtonController(QObject):
    send_message_signal = Signal()
    update_input_box_signal = Signal(str)

    def __init__(self, mic_button):
        super().__init__()

        self.mic_button = mic_button
        self.worker_thread = None

    def load_model_and_stream_audio(self):
        self.worker_thread = QThread() 
        self.worker_thread.setObjectName("user_mic_thread")
        self.worker = MicWorker()
        self.worker.moveToThread(self.worker_thread)

        # Also make ui changes
        self.worker_thread.started.connect(self.is_loading_ui)
        self.worker.finished_loading.connect(self.is_on_ui)

        self.worker_thread.started.connect(self.worker.load_whisper_model)
        self.worker.finished_loading.connect(self.worker.enable_user_audio_to_text)
        self.worker.error.connect(self.print_error) 
        self.worker.end_worker.connect(self.end_thread)
        self.worker.text_chunk.connect(self.update_user_input_box_text_and_send)

        self.worker_thread.start()

    def disable_mic_input(self):
        self.worker.disable_user_audio_to_text()

    ### Helper Functions ###
    def is_off_ui(self):
        self.mic_button.setStyleSheet("""
        QPushButton {
            background-color: transparent;
            border: none;
        }
        QPushButton:hover {
            background-color: #a4a6a5;  
        }
        """)   

        self.mic_button.setEnabled(True)

    def is_loading_ui(self):
        self.mic_button.setStyleSheet("""
        QPushButton {
            background-color: yellow;
            border: none;
        }
        QPushButton:hover {
            background-color: #a4a6a5;  
        }
        """)         

        self.mic_button.setEnabled(False)

    def is_on_ui(self):
        self.mic_button.setStyleSheet("""
        QPushButton {
            background-color: green;
            border: none;
        }
        QPushButton:hover {
            background-color: #a4a6a5;  
        }
        """)         

        self.mic_button.setEnabled(True)

    def end_thread(self):
        self.is_off_ui()
        self.worker_thread.quit()
        self.worker_thread.wait()
        self.worker.deleteLater()
        self.worker_thread.deleteLater()

        self.worker_thread = None


    def print_error(self, error):
        print(error)
        self.end_thread()

    def update_user_input_box_text_and_send(self, text):
        self.update_input_box_signal.emit(text)
        self.send_message_signal.emit()
    












