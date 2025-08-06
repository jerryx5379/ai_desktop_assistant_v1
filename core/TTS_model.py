from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from TTS.api import TTS


class TTSModel:
    tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")

