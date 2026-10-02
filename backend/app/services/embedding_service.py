from fastembed import TextEmbedding


EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"


class EmbeddingService:
    def __init__(self):
        self.model = TextEmbedding(
            model_name=EMBEDDING_MODEL
        )

    def embed_documents(self, documents):
        return list(
            self.model.passage_embed(documents)
        )

    def embed_query(self, query):
        return list(
            self.model.query_embed([query])
        )[0]