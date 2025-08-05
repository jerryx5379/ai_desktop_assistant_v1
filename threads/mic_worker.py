from PySide6.QtCore import QObject, Signal, Slot
from faster_whisper import WhisperModel
import collections
import numpy as np
import pyaudio

class MicWorker(QObject):
    finished_loading = Signal()
    text_chunk = Signal(str)
    end_worker = Signal()
    error = Signal(str)

    def __init__(self):
        super().__init__()

        self.ACCEPT_AUDIO_INPUT = False
        self.model = None
        
    @Slot()
    def load_whisper_model(self):
        try:
            self.model = WhisperModel("base", compute_type='int8')
            self.finished_loading.emit()
        except Exception as e:
            self.error.emit(f"Failed to load Whisper model: {e}")
            self.end_worker.emit()
        

    @Slot()
    def enable_user_audio_to_text(self):
        self.ACCEPT_AUDIO_INPUT = True

        try:
            audio = pyaudio.PyAudio()
            py_stream = audio.open(rate=16000, format=pyaudio.paInt16, channels=1, input=True, frames_per_buffer=512)
            while self.ACCEPT_AUDIO_INPUT:
                audio_buffer = collections.deque(maxlen=int((16000 // 512) * 0.5))
                frames, long_term_noise_level, current_noise_level, ambient_noise_level, voice_activity_detected = [], 0.0, 0.0, 0.0, False
    
                while self.ACCEPT_AUDIO_INPUT:
                    data = py_stream.read(512)
                    amp, long_term_noise_level, current_noise_level = self.get_levels(data, long_term_noise_level, current_noise_level)
                    audio_buffer.append(data)

                    if voice_activity_detected:
                        frames.append(data)
                        if current_noise_level < ambient_noise_level + 100:
                            break  # voice actitivy ends

                    if not voice_activity_detected and current_noise_level > long_term_noise_level + 300:
                        voice_activity_detected = True
                        ambient_noise_level = long_term_noise_level
                        frames.extend(list(audio_buffer))

                if not self.ACCEPT_AUDIO_INPUT:
                    break

                if not frames:
                    continue

                audio_data = b''.join(frames)
                audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
                
                segments, _ = self.model.transcribe(audio_np, without_timestamps=True, language='en')
                user_text = " ".join(seg.text for seg in segments).strip()

                if user_text: 
                    self.text_chunk.emit(user_text)
                    print(f'>>> Transcribed: {user_text}')

        except Exception as e:
            self.error.emit(str(e))
        finally:
            # Ensure resources are always cleaned up
            if 'py_stream' in locals() and py_stream.is_active():
                py_stream.stop_stream()
                py_stream.close()
            if 'audio' in locals():
                audio.terminate()
            
            # Signal that the worker has finished its job
            self.end_worker.emit()
    @Slot()
    def disable_user_audio_to_text(self):
        self.ACCEPT_AUDIO_INPUT = False

    ### Helper Functions ###

    def get_levels(self, data, long_term_noise_level, current_noise_level):
        amp = np.abs(np.frombuffer(data, dtype=np.int16)).mean()
        long_term_noise_level = long_term_noise_level * 0.995 + amp * (1.0 - 0.995)
        current_noise_level = current_noise_level * 0.920 + amp * (1.0 - 0.920)
        return amp, long_term_noise_level, current_noise_level
    
