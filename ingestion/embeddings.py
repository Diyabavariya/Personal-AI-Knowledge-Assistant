from sentence_transformers import SentenceTransformer

class EmbeddingGenerator:
    """
    Generates vector embeddings for text chunks.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        # Load a pre-trained embedding model
        self.model = SentenceTransformer(model_name)

    def embed_texts(self, texts):
        """
        Converts a list of text chunks into embeddings.

        Args:
            texts (List[str]): List of text chunks

        Returns:
            List[List[float]]: List of embedding vectors
        """
        embeddings = self.model.encode(texts)
        return embeddings
