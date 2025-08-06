from sentence_transformers import SentenceTransformer

class EmbeddingModel:
    model = SentenceTransformer('msmarco-MiniLM-L6-cos-v5')

    vector_length = model.encode("test", convert_to_numpy=True).shape[-1]






