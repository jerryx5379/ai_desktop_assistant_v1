from PySide6.QtCore import QObject, Signal, Slot
from faster_whisper import WhisperModel
import collections
import numpy as np
import pyaudio
import pyaudio
import wave
import time
from core import TTSModel

class SpeakerWorker(QObject):
    finished = Signal()

    def __init__(self, text):
        super().__init__()

        self.tts = TTSModel.tts
        self.text = text
        self.temp_wav_path = "user_data/temp_wavs/temp.wav"
        
        self.EARLY_STOP_FLAG = False
     
    @Slot()
    def text_to_speech(self):
        self.tts.tts_to_file(text=self.text, file_path=self.temp_wav_path)
        self.play_audio()
        self.EARLY_STOP_FLAG = False
        self.finished.emit()

    def play_audio(self):
        wf = wave.open(self.temp_wav_path, 'rb')
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True)
        
        chunk_size = 1024
        data = wf.readframes(chunk_size)
        while data and not self.EARLY_STOP_FLAG:
            stream.write(data)
            data = wf.readframes(chunk_size)

        stream.stop_stream()
        stream.close()
        p.terminate()
        wf.close()


    ### Helper Functions ###
    @Slot()
    def enable_early_stop(self):
        self.EARLY_STOP_FLAG = True










