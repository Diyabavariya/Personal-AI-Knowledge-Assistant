import numpy as np
import ast

def to_numeric_vector(vec):
    """
    Ensures the vector is a NumPy float array.
    Handles strings, lists, and numpy arrays safely.
    """
    if isinstance(vec, str):
        vec = ast.literal_eval(vec)

    vec = np.array(vec, dtype=np.float32)
    return vec

def cosine_similarity(vec1, vec2):
    v1 = to_numeric_vector(vec1)
    v2 = to_numeric_vector(vec2)

    if v1.shape != v2.shape:
        raise ValueError("Embedding dimension mismatch")

    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return float(np.dot(v1, v2) / (norm1 * norm2))

class VectorStore:
    def __init__(self, embeddings, texts):
        self.embeddings = embeddings
        self.texts = texts

    def search(self, query_embedding, top_k=4):
        scores = []

        for emb, text in zip(self.embeddings, self.texts):
            score = cosine_similarity(query_embedding, emb)
            scores.append((score, text))

        scores.sort(reverse=True, key=lambda x: x[0])
        return [text for _, text in scores[:top_k]]
