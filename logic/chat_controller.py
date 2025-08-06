from PySide6.QtWidgets import (
    QTextBrowser, QApplication
)
from PySide6.QtCore import QTimer,QThread, QObject, Slot
from PySide6.QtGui import QPalette,QTextCursor, QFontMetrics

import json
import markdown
from pygments.formatters.html import HtmlFormatter
import numpy as np
import faiss

from widgets.chat_box import ChatBubble
from threads import OllamaWorker
from core import CallableFunctions, EmbeddingModel


class ChatController(QObject):
    def __init__(self, chat_box, user_input):
        super().__init__()

        self.OPERATING_SYSTEM_INTERACTION_FLAG = False
        self.model = EmbeddingModel.model

        self.chat_box = chat_box
        self.user_input = user_input

        self.scroll_content = self.chat_box.get_scroll_content()
        self.scroll_layout = self.chat_box.get_scroll_layout()
        self.send_button = self.user_input.get_send_button()
        self.input_text_box = self.user_input.get_input_text_box()
        self.os_button = self.user_input.get_os_button()
        
        self.total_chat_bubbles_height = 0
        self.layout_spacing = self.chat_box.scroll_layout.spacing()
        self.total_scroll_content_height = 0

        sample_chat_bubble = ChatBubble(text="1",sender="user")
        QTimer.singleShot(0,lambda: self.get_indiv_line_height(sample_chat_bubble))

    @Slot()
    def send_message(self):
        if not self.send_button.isEnabled():
            self.input_text_box.clear()
            return

        text = self.input_text_box.toPlainText().strip() 
        if not text:
            return

        self.send_button.setEnabled(False) 

        # This adds the user's text message to the chat_box
        self.chat_bubble = ChatBubble(text=text, sender= "user")
        self.scroll_layout.insertWidget(self.scroll_layout.count(), self.chat_bubble)

        # Rag search step: before updating the chat context with the user prompt, add rag context if there is
        text = self.add_rag_context(text=text)

        self.chat_box.update_chat_context(role = "user", message = text)
        self.input_text_box.clear()

        sample_chat_bubble = ChatBubble(text="1",sender="user") # used to get unit height of a chat bubble
        QTimer.singleShot(0,lambda: self.add_preview_height(sample_chat_bubble))

        # This adds the llm's response to chatbox. while the response is being streamed on another thread, user cannot send another message
        self.chat_bubble = ChatBubble(text=text,sender = "assistant")
        self.scroll_layout.insertWidget(self.scroll_layout.count(), self.chat_bubble)

        if self.OPERATING_SYSTEM_INTERACTION_FLAG:
            self.thread = QThread()
            self.thread.setObjectName("Ollama_inference_tool_call_thread")
            url = "http://localhost:11434/api/generate"
            data = self.get_data_tool_call(text)
            self.worker = OllamaWorker(url=url, data=data)
            self.worker.moveToThread(self.thread)

            self.thread.started.connect(self.thinking_text)
            self.thread.started.connect(self.worker.generate_ollama)
            self.worker.early_cancel_signal.connect(self.early_cancel_func)
            self.worker.finished.connect(self.finished_generating_tool_call_response) # rest of the send_message logic is here

            self.thread.start()

        else:
            self.thread = False
            self.worker = False
            empty_result = '{"empty": 0}'
            self.finished_generating_tool_call_response(empty_result)


    def handle_output_chunk(self, chunk):
        try:
            # Append new chunk to chat_bubble, keeping existing text
            self.chat_bubble.moveCursor(QTextCursor.End)
            self.chat_bubble.insertPlainText(chunk)
            self.chat_bubble.ensureCursorVisible()

            if self.chat_bubble.height() + self.total_chat_bubbles_height + self.layout_spacing > self.total_scroll_content_height:
                self.total_scroll_content_height += 5*self.layout_spacing
                self.scroll_content.setMinimumHeight(self.total_scroll_content_height)
        except Exception as e:
            return
        

    def worker_finished(self, response):
        if hasattr(self, 'chat_bubble') and self.chat_bubble is not None:
            self.chat_box.update_chat_context(role = "assistant", message = response)

        try:
            # basic formatting: get the plain text, convert it to html then set html
            text_html = markdown.markdown(text=response,extensions=['fenced_code','tables','codehilite'])
            if self.is_dark_theme():
                style = HtmlFormatter(style='monokai').get_style_defs('.codehilite')
            else:
                style = HtmlFormatter(style='manni').get_style_defs('.codehilite')


            text_html = f"""
<style>
{style}
.codehilite {{
    font-family: {self.chat_bubble.code_block_font};
    background-color: transparent !important;

}}
</style>
{text_html}
"""
            self.chat_bubble.setHtml(text_html)

            if '<code' in text_html and '</code>' in text_html:
                self.chat_bubble.ignore_keypress_scrolling = False
                self.chat_bubble.ignore_wheel_event = False

            #adjust_height = self.chat_bubble.height() + 2*self.layout_spacing + self.total_chat_bubbles_height
            #self.chat_box.scroll_content.setMinimumHeight(adjust_height)
        except Exception as e:
            print("error finalizing response chat_bubble. likely cleared chat while it was working")
        
        self.send_button.setEnabled(True) 
        self.end_thread()

    def add_preview_height(self, sample_chat_bubble:QTextBrowser):
        self.add_to_chat_bubbles_total_height()

        unit_height_of_chat_bubble = sample_chat_bubble.height()
        viewport_height = self.chat_box.viewport().height()
        padding_height = viewport_height - unit_height_of_chat_bubble

        self.total_scroll_content_height = self.total_chat_bubbles_height + 0.94*padding_height

        self.scroll_content.setMinimumHeight(self.total_scroll_content_height)

        self.chat_box.verticalScrollBar().setValue( 
            self.chat_box.verticalScrollBar().maximum()
        )

    def get_data_tool_call(self,user_prompt):
        prompt_skeleton = """Determine if the following prompt requires any of these function calls:
change_system_theme_to_dark
change_system_theme_to_light
0 means no. 1 means yes. 
Prompt:"""

        prompt = prompt_skeleton + user_prompt

        data = {
            "model": "gemma3n:e2b",
            "prompt": prompt,
            "stream": False,
            "format": {
                "type": "object",
                "properties": {
                "change_to_dark_theme": {
                    "type": "integer"
                },
                "change_to_light_theme": {
                    "type": "integer"
                }
                },
                "required": [
                "change_to_dark_theme",
                "change_to_light_theme"
                ]
            }
        }

        return data

    def finished_generating_tool_call_response(self, result):
        """
        result looks like:
        '
        {
        "change_to_dark_theme": int,
        "change_to_light_theme": int
        }
        '

        """

        llm_result = json.loads(result)

        if self.thread and self.worker:
            self.end_thread()

        # if there is a tool call, then just do that, otherwise send request to llm as usual
        if 1 in llm_result.values():
            # start another thread to carry out the tool call

            self.thread = QThread()
            self.thread.setObjectName("thread_for_callable_functions")
            self.worker = CallableFunctions(llm_result)
            self.worker.moveToThread(self.thread)

            self.thread.started.connect(self.worker.call_functions)
            self.worker.error.connect(self.print_error)
            self.worker.finished.connect(self.tool_call_worker_finished)
            
            self.thread.start()
        else:

            self.thread = QThread()
            self.thread.setObjectName("Ollama_inference_thread")

            url = "http://localhost:11434/api/chat"
            data = self.chat_box.get_data_regular()
            self.worker = OllamaWorker(url=url, data=data)
            self.worker.moveToThread(self.thread)

            self.thread.started.connect(self.clear_chat_bubble)
            self.thread.started.connect(self.worker.stream_ollama)
            self.worker.text_chunk.connect(self.handle_output_chunk)
            self.worker.early_cancel_signal.connect(self.early_cancel_func)
            self.worker.finished.connect(self.worker_finished)

            self.thread.start()
            return

    def tool_call_worker_finished(self, text):
        try:
            text_html = "<i>" + text + "</i>"
            self.chat_bubble.setHtml(text_html)

            self.chat_box.update_chat_context(role = "assistant", message = text)
        except:
            pass

        self.send_button.setEnabled(True)

        self.end_thread()


    ### Helper Functions ###
    def add_to_chat_bubbles_total_height(self):
        layout = self.scroll_layout

        if layout.count() == 2: 
            height = layout.itemAt(0).widget().height()
            self.total_chat_bubbles_height += height 
            self.indexes_added = [0]
        else:
            last_index = self.indexes_added[-1]
            new_indexes = [last_index+1,last_index+2]
            for index in new_indexes:
                height = layout.itemAt(index).widget().height()
                self.total_chat_bubbles_height += height + self.layout_spacing
                self.indexes_added.append(index)

    def get_indiv_line_height(self, sample_chat_bubble:QTextBrowser):
        line_height = QFontMetrics(sample_chat_bubble.font()).lineSpacing()
        self.indiv_line_height = line_height

    def is_dark_theme(self):
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

    def end_thread(self):
        self.thread.quit()
        self.thread.wait()
        self.worker.deleteLater()
        self.thread.deleteLater()

    def thinking_text(self):
        text = "<i>Reading Message</i>"
        self.chat_bubble.setHtml(text)

    def print_error(self, error):
        print(error)

    def clear_chat_bubble(self):
        try:
            self.chat_bubble.setPlainText("")
        except:
            pass

    def set_early_cancel(self):
        self.worker.set_early_cancel()

        self.total_chat_bubbles_height = 0
        self.layout_spacing = self.chat_box.scroll_layout.spacing()
        self.total_scroll_content_height = 0

    @Slot()
    def early_cancel_func(self):
        self.send_button.setEnabled(True)
        self.end_thread()

        self.total_chat_bubbles_height = 0
        self.layout_spacing = self.chat_box.scroll_layout.spacing()
        self.total_scroll_content_height = 0

    def vector_search(self, text, top_k=5):
        try:
            answers = np.load("user_data/file_text_chunks/aggregated/text_chunks.npy", allow_pickle=True).tolist()
            index = faiss.read_index("user_data/embeddings/aggregated/index.faiss")
        except FileNotFoundError as e:
            return []

        query_embedding = self.model.encode([text], convert_to_numpy=True)
        faiss.normalize_L2(query_embedding)
        
        distances, indices = index.search(query_embedding, top_k)

        results = []
        print(f"\nQuestion: {text}")
        print(f"Top {top_k} potential answers:")

        for dist, idx in zip(distances[0], indices[0]):
            if idx == -1:
                continue
            
            print(f"  - (Score: {dist:.4f}) {answers[idx]}")
            if dist > 0.45:
                results.append(answers[idx])
        
        return results
        
    def add_rag_context(self, text) -> str:
        rag_context = self.vector_search(text=text)

        all_context = ""
        for context in rag_context:
            if len(all_context) > 800:
                break
            all_context += f"\n{context}"

        print(all_context)

        new_text = f"""Respond to the prompt using this information:
{all_context}

Prompt:
{text}  
"""
        if len(rag_context) == 0:
            new_text = text

        return new_text

        
    @Slot()
    def toggle_operating_system_interaction(self):
        if self.OPERATING_SYSTEM_INTERACTION_FLAG:
            self.OPERATING_SYSTEM_INTERACTION_FLAG = False

            self.os_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: white;
            }
            QPushButton:disabled {
                background-color: transparent;
            }

            QPushButton:hover {
                background-color: #a4a6a5;
            }
            """) 


        else:
            self.OPERATING_SYSTEM_INTERACTION_FLAG =  True
            self.os_button.setStyleSheet("""
            QPushButton {
                background-color: green;
                border: none;
            }
            QPushButton:disabled {
                background-color: transparent;
                color: #aaaaaa;
            }

            QPushButton:hover {
                background-color: #a4a6a5;
            }
            """) 


