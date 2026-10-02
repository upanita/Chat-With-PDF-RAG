from fastembed import TextEmbedding


def main():
    model = TextEmbedding()

    documents = [
        "Python is a programming language.",
        "React is a JavaScript library for building user interfaces.",
        "RAG combines document retrieval with a language model.",
    ]

    embeddings = list(model.embed(documents))

    print(f"Number of embeddings: {len(embeddings)}")
    print(f"Embedding dimensions: {len(embeddings[0])}")


if __name__ == "__main__":
    main()