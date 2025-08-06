from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import re

# Load a model fine-tuned for question-answer retrieval (dual-encoder style)
#model = SentenceTransformer('msmarco-MiniLM-L6-cos-v5')


import fitz

doc = fitz.open("Payment_info.pdf")
text = ""
for page in doc:
    text += page.get_text()
#print(repr(text))

answers = re.split(r'\n\s*\n', text)

print(answers)


"""
# 1. Embed the answers separately
answer_embeddings = model.encode(answers, convert_to_numpy=True)

# Normalize embeddings for cosine similarity search
faiss.normalize_L2(answer_embeddings)

# 2. Create a FAISS index for the answers
dim = answer_embeddings.shape[1]
index = faiss.IndexFlatIP(dim)  # Inner product = cosine similarity on normalized vectors
index.add(answer_embeddings)



"""









"""
answers = np.load("user_data/file_text_chunks/aggregated/text_chunks.npy", allow_pickle=True).tolist()
index = faiss.read_index("user_data/embeddings/aggregated/index.faiss")

# Search function
def search_question(query, top_k=3):
    query_embedding = model.encode([query], convert_to_numpy=True)
    faiss.normalize_L2(query_embedding)
    distances, indices = index.search(query_embedding, top_k)

    print(f"\nQuestion: {query}")
    print(f"Top {top_k} answers:")
    for dist, idx in zip(distances[0], indices[0]):
        print(f"  - ({dist:.4f}) {answers[idx]}")

# Demo interaction loop
if __name__ == "__main__":
    while True:
        q = input("\nEnter your question (or type 'exit'): ")
        if q.lower() == 'exit':
            break
        search_question(q)

"""











