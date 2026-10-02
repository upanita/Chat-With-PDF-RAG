from app.services.pdf_service import extract_pdf_chunks
from app.services.embedding_service import EmbeddingService
from app.services.vector_service import VectorService


PDF_PATH = "sample_data/UPANITA MAHALA 2025 RESUME-2026.pdf"


def main():
    print("Loading PDF...")

    document_id = "test-document"

    chunks = extract_pdf_chunks(
        PDF_PATH,
        document_id,
    )

    print(f"Chunks: {len(chunks)}")

    print("Loading embedding service...")

    embedding_service = EmbeddingService()

    documents = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = embedding_service.embed_documents(
        documents
    )

    print("Connecting to Chroma...")

    vector_service = VectorService()

    vector_service.add_documents(
        chunks,
        embeddings,
    )

    print("Documents stored successfully.")

    question = "What certifications does Upanita have?"

    print(f"\nQuestion: {question}")

    query_embedding = embedding_service.embed_query(
        question
    )

    results = vector_service.search(
        query_embedding,
        document_id=document_id,
        top_k=3,
    )

    print("\nRetrieved results:")

    for result in results:
        print(
            f"- Page {result['page']} | "
            f"{result['chunk_id']} | "
            f"Distance: {result['distance']:.4f}"
        )


if __name__ == "__main__":
    main()