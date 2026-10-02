import numpy as np
from fastembed import TextEmbedding


def cosine_similarity(a, b):
    return np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )


def main():
    embedding_model = TextEmbedding(
        model_name="BAAI/bge-small-en-v1.5"
    )

    documents = [
        "Retrieval Augmented Generation, or RAG, retrieves relevant documents and provides them to a language model before generating an answer.",
        "A RAG system first searches a vector database for information related to the user's question.",
        "Large language models can generate answers based on information provided in their context.",
        "React is a JavaScript library for building user interfaces.",
        "Python is a programming language commonly used for backend development.",
        "Chroma is a vector database that can store embeddings and perform similarity searches.",
    ]

    queries = [
        "How does retrieval augmented generation work?",
        "What is React used for?",
        "What is Chroma used for?",
    ]

    document_embeddings = list(
        embedding_model.passage_embed(documents)
    )

    for query in queries:
        query_embedding = list(
            embedding_model.query_embed([query])
        )[0]

        results = []

        for document, embedding in zip(
            documents,
            document_embeddings,
        ):
            similarity = cosine_similarity(
                query_embedding,
                embedding,
            )

            results.append(
                (similarity, document)
            )

        results.sort(
            key=lambda x: x[0],
            reverse=True,
        )

        print("\n" + "=" * 70)
        print(f"Query: {query}")
        print("=" * 70)

        for similarity, document in results[:3]:
            print(f"\nSimilarity: {similarity:.4f}")
            print(document)


if __name__ == "__main__":
    main()