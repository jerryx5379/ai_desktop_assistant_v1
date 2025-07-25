import json
from PySide6.QtCore import QObject, Signal
import requests

from PySide6.QtCore import QObject, Signal

class OllamaWorker(QObject):
    text_chunk = Signal(str) 
    finished  = Signal(str)

    def __init__(self, url, data):
        super().__init__()

        self.url = url
        self.data = data
        
    def stream_ollama(self):
        with requests.post(url=self.url, json=self.data, stream=True) as response:
            response.raise_for_status() 
            
            assis_response = ""
            for line in response.iter_lines():
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


    