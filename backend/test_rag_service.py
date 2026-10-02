from app.services.rag_service import RAGService


def main():
    service = RAGService()

    question = "What certifications does Upanita have?"

    result = service.answer_question(
        question,
        document_id="test-document",
        top_k=3,
    )

    print("\nQuestion:")
    print(question)

    print("\nAnswer:")
    print(result["answer"])

    print("\nSources:")

    for source in result["sources"]:
        print(
            f"- Page {source['page']} | "
            f"{source['chunk_id']} | "
            f"Distance: {source['distance']:.4f}"
        )


if __name__ == "__main__":
    main()