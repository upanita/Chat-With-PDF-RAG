import re

import pymupdf
import chromadb
from fastembed import TextEmbedding


PDF_PATH = "sample_data/UPANITA MAHALA 2025 RESUME-2026.pdf"

CHUNK_SIZE = 1200
CHUNK_OVERLAP = 200


def split_into_sentences(text):
    text = " ".join(text.split())

    sentences = re.split(
        r"(?<=[.!?])\s+",
        text,
    )

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]


def create_chunks(text, page_number):
    sentences = split_into_sentences(text)

    chunks = []
    current_sentences = []
    current_length = 0
    chunk_number = 1

    for sentence in sentences:
        sentence_length = len(sentence)

        if (
            current_sentences
            and current_length + sentence_length > CHUNK_SIZE
        ):
            chunk_text = " ".join(current_sentences)

            chunks.append(
                {
                    "chunk_id": f"page-{page_number}-chunk-{chunk_number}",
                    "page": page_number,
                    "text": chunk_text,
                }
            )

            # Keep the last few sentences as overlap
            overlap_sentences = []
            overlap_length = 0

            for previous_sentence in reversed(current_sentences):
                if overlap_length + len(previous_sentence) > CHUNK_OVERLAP:
                    break

                overlap_sentences.insert(
                    0,
                    previous_sentence,
                )

                overlap_length += len(previous_sentence)

            current_sentences = overlap_sentences

            current_length = sum(
                len(sentence)
                for sentence in current_sentences
            )

            chunk_number += 1

        current_sentences.append(sentence)
        current_length += sentence_length

    # Add final chunk
    if current_sentences:
        chunks.append(
            {
                "chunk_id": f"page-{page_number}-chunk-{chunk_number}",
                "page": page_number,
                "text": " ".join(current_sentences),
            }
        )

    return chunks


def extract_pdf_chunks():
    document = pymupdf.open(PDF_PATH)

    all_chunks = []

    for page_number, page in enumerate(document, start=1):
        text = page.get_text()

        page_chunks = create_chunks(
            text,
            page_number,
        )

        all_chunks.extend(page_chunks)

    document.close()

    return all_chunks


def main():
    print("Loading PDF...")

    chunks = extract_pdf_chunks()

    print(f"Total chunks: {len(chunks)}")

    print("\nLoading embedding model...")

    embedding_model = TextEmbedding(
        model_name="BAAI/bge-small-en-v1.5"
    )

    print("Creating embeddings...")

    documents = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = list(
        embedding_model.passage_embed(documents)
    )

    print("Connecting to Chroma...")

    client = chromadb.PersistentClient(
        path="./chroma_data"
    )

    collection = client.get_or_create_collection(
        name="resume_documents",
        metadata={
            "hnsw:space": "cosine"
        },
    )

    ids = [
        chunk["chunk_id"]
        for chunk in chunks
    ]

    metadatas = [
        {
            "page": chunk["page"],
            "chunk_id": chunk["chunk_id"],
        }
        for chunk in chunks
    ]

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    print(
        f"Stored {len(chunks)} chunks in Chroma."
    )

    # -----------------------------
    # Ask a question
    # -----------------------------

    question = input(
        "\nEnter your question: "
    )

    print("\nSearching for relevant chunks...")

    query_embedding = list(
        embedding_model.query_embed(
            [question]
        )
    )[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3,
    )

    print("\nTop matching chunks:")

    for i, (
        document,
        metadata,
        distance,
    ) in enumerate(
        zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        ),
        start=1,
    ):
        print("\n" + "=" * 70)
        print(f"RESULT {i}")
        print("=" * 70)

        print(
            f"Distance: {distance:.4f}"
        )

        print(
            f"Page: {metadata['page']}"
        )

        print(
            f"Chunk ID: {metadata['chunk_id']}"
        )

        print("\n" + document)


if __name__ == "__main__":
    main()