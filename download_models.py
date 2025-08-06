from sentence_transformers import SentenceTransformer
from TTS.api import TTS
from faster_whisper import WhisperModel

sentence_model = SentenceTransformer('msmarco-MiniLM-L6-cos-v5')
    
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")

model = WhisperModel("base", compute_type='int8')

print("Finished with all model downloads")

