from PySide6.QtCore import QObject, Signal, Slot

import requests
import json

class OllamaWorker(QObject):
    text_chunk = Signal(str) 
    finished  = Signal(str)
    early_cancel_signal = Signal()

    def __init__(self, url, data):
        super().__init__()

        self.url = url
        self.data = data
        self.EARLY_CANCEL = False
        
    @Slot()
    def stream_ollama(self):
        with requests.post(url=self.url, json=self.data, stream=True) as response:
            response.raise_for_status() 
            
            assis_response = ""
            for line in response.iter_lines():

                if self.EARLY_CANCEL:
                    self.early_cancel_signal.emit()
                    return

                if line:
                    chunk = json.loads(line.decode("utf-8"))\
                    
                    if chunk.get("done",False):
                        total_tokens = chunk.get("eval_count", 0)
                        total_time = chunk.get("eval_duration", 1) / (10**9)
                        prompt_time = chunk.get("prompt_eval_duration", 1) / (10**9)
                        #print(assis_response)
                        #print(f"\nTokens: {total_tokens}")
                        #print(f"Tk/s: {total_tokens/total_time}")
                        #print(f"Prompt_time: {prompt_time}")

                    new_text = chunk["message"]["content"]
                    
                    assis_response += new_text 
                    self.text_chunk.emit(new_text)
        
        self.finished.emit(assis_response)

    @Slot()
    def generate_ollama(self):
        response = requests.post(url=self.url, json=self.data)

        result = response.json()
        #print(result['response'])
        
        if self.EARLY_CANCEL:
            self.early_cancel_signal.emit()
        else:
            self.finished.emit(result['response'])

    @Slot()
    def set_early_cancel(self):
        self.EARLY_CANCEL = True


    