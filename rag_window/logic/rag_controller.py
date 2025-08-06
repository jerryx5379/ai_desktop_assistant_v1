from PySide6.QtWidgets import (
    QTextBrowser, QApplication, QFrame, QSizePolicy, QLabel, QHBoxLayout, QPushButton
)

from PySide6.QtCore import QObject,QSize, Signal,QThread
from PySide6.QtGui import QIcon
from rag_window.threads import RagWorker

from pathlib import Path


class RagController(QObject):
    update_stacked_widget = Signal()

    def __init__(self, new_file_screen):
        super().__init__()

        self.new_file_screen = new_file_screen
        self.new_screen_layout = self.new_file_screen.get_new_screen_layout()

        self.embedding_thread_running = False
        self.skip = False

    def added_new_file(self, pdf_paths:list):
        if self.embedding_thread_running:
            return

        self.embedding_thread_running = True

        self.thread = QThread()
        self.thread.setObjectName("creating_embeddings_thread")
        self.worker = RagWorker()
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(lambda: print("embeddings Thread started"))
        self.thread.started.connect(lambda: setattr(self,'skip',True))        
        self.thread.started.connect(lambda: self.worker.pdf_to_vector_embeddings(pdf_paths))

        self.worker.emit_file_name.connect(self.add_file_bubble)

        self.worker.finished_embeddings.connect(lambda: print("embeddings Thread Finished"))
        self.worker.finished_embeddings.connect(self.aggregate_embeddings_and_create_indexes)
        self.worker.finished_embeddings.connect(self.thread.quit)
        self.worker.finished_embeddings.connect(self.worker.deleteLater)
        self.worker.finished_embeddings.connect(self.thread.deleteLater)
        

        self.thread.start()
        self.thread.setPriority(QThread.LowPriority) # trying to fix freezing window


    def remove_bubble_and_embeddings(self, bubble_name):
        #print(f"This function is called with {bubble_name}")

        if self.embedding_thread_running:
            return

        for i in range(self.new_screen_layout.count()):
            item = self.new_screen_layout.itemAt(i)
            widget = item.widget()

            if widget and widget.objectName() == bubble_name:
                target_widget = widget
                break

        self.new_screen_layout.removeWidget(target_widget)
        target_widget.setParent(None)
        target_widget.deleteLater()

        target_path = Path("user_data/embeddings") / (bubble_name + ".npy")
        target_path.unlink()

        target_path = Path("user_data/file_text_chunks") / (bubble_name + ".npy")
        target_path.unlink()

        self.aggregate_embeddings_and_create_indexes()
        self.update_stacked_widget.emit()

    def load_previous_files(self):
        folder = Path("user_data/embeddings")
        npy_files = folder.glob("*.npy")

        file_names = [file.stem for file in npy_files]


        for file_name in file_names:
            self.add_file_bubble(file_name=file_name)


    ### Helper Functions ###
    def is_already_created(self, file_name):
        for i in range(self.new_screen_layout.count()):
            item = self.new_screen_layout.itemAt(i)
            widget = item.widget()
            if widget is not None:
                object_name = widget.objectName()

                if object_name == file_name:
                    return True
            
        return False

    def file_bubble(self, file_name):
        bubble = QFrame()
        bubble.setObjectName(file_name)
        bubble.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        layout = QHBoxLayout(bubble)

        label = QLabel(file_name)
        
        trash_button = QPushButton()
        trash_button.setIcon(QIcon("assets/icons/trash.svg"))
        trash_button.setIconSize(QSize(24,24))
        trash_button.setStyleSheet("""
        QPushButton {
            background-color: transparent;
            border: none;
            color: white;
        }
        QPushButton:disabled {
            background-color: transparent;
            color: #aaaaaa;
        }

        QPushButton:hover {
            background-color: #a4a6a5;
        }
        """) 

        layout.addWidget(label)
        layout.addStretch()
        layout.addWidget(trash_button)

        trash_button.clicked.connect(lambda checked, bubble_name=file_name: self.remove_bubble_and_embeddings(bubble_name))

        return bubble

    def aggregate_embeddings_and_create_indexes(self):

        if self.skip:
            pass
        elif self.embedding_thread_running:
            return

        self.skip = False
        self.embedding_thread_running = True

        self.aggregation_thread = QThread()
        self.aggregation_thread.setObjectName("aggregate_embeddings_and_indexes_thread")
        self.aggregation_worker = RagWorker()
        self.aggregation_worker.moveToThread(self.aggregation_thread)

        self.aggregation_thread.started.connect(lambda: print("aggregation Thread started"))
        self.aggregation_thread.started.connect(self.aggregation_worker.aggregate_embeddings_and_create_indexes)

        self.aggregation_worker.finished_aggregating.connect(self.aggregation_thread_end)

        self.aggregation_thread.start()

    
    def add_file_bubble(self, file_name):
        if self.is_already_created(file_name=file_name):
            return

        new_bubble = self.file_bubble(file_name=file_name)
        self.new_screen_layout.insertWidget(self.new_screen_layout.count() - 1, new_bubble)

        self.update_stacked_widget.emit()

    def aggregation_thread_end(self):
        print("aggregation Thread finished")

        self.aggregation_thread.quit()
        self.aggregation_thread.wait()  
        
        self.aggregation_worker.deleteLater()
        self.aggregation_thread.deleteLater()

        self.embedding_thread_running = False






