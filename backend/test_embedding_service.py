from app.services.embedding_service import EmbeddingService


def main():
    service = EmbeddingService()

    documents = [
        "React is a JavaScript library.",
        "Java Spring Boot is used for backend development.",
    ]

    embeddings = service.embed_documents(documents)

    print(f"Number of embeddings: {len(embeddings)}")
    print(f"Embedding dimensions: {len(embeddings[0])}")

    query_embedding = service.embed_query(
        "What is used for backend development?"
    )

    print(
        f"Query embedding dimensions: "
        f"{len(query_embedding)}"
    )


if __name__ == "__main__":
    main()