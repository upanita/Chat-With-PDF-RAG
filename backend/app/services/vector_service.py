import chromadb


CHROMA_PATH = "./chroma_data"
COLLECTION_NAME = "pdf_documents"


class VectorService:
    def __init__(self):
        self.client = chromadb.PersistentClient(
            path=CHROMA_PATH
        )

        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={
                "hnsw:space": "cosine"
            },
        )

    def add_documents(
        self,
        chunks,
        embeddings,
    ):
        ids = [
            chunk["chunk_id"]
            for chunk in chunks
        ]

        documents = [
            chunk["text"]
            for chunk in chunks
        ]

        metadatas = [
            {
                "document_id": chunk["document_id"],
                "page": chunk["page"],
                "chunk_id": chunk["chunk_id"],
            }
            for chunk in chunks
        ]

        self.collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    def search(
        self,
        query_embedding,
        document_id,
        top_k=3,
    ):
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where={
                "document_id": document_id
            },
        )

        documents = []

        for document, metadata, distance in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        ):
            documents.append(
                {
                    "text": document,
                    "document_id": metadata["document_id"],
                    "page": metadata["page"],
                    "chunk_id": metadata["chunk_id"],
                    "distance": distance,
                }
            )

        return documents