import re

import pymupdf
import chromadb
import ollama
from fastembed import TextEmbedding


PDF_PATH = "sample_data/UPANITA MAHALA 2025 RESUME-2026.pdf"

CHUNK_SIZE = 1200
CHUNK_OVERLAP = 200

EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
OLLAMA_MODEL = "llama3.2:3b"


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
            chunks.append(
                {
                    "chunk_id": f"page-{page_number}-chunk-{chunk_number}",
                    "page": page_number,
                    "text": " ".join(current_sentences),
                }
            )

            # Keep some previous sentences for overlap
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


def create_vector_store(chunks, embedding_model):
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

    return collection


def retrieve_documents(
    question,
    collection,
    embedding_model,
    top_k=3,
):
    print("\nSearching for relevant information...")

    query_embedding = list(
        embedding_model.query_embed(
            [question]
        )
    )[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )

    retrieved_documents = []

    for document, metadata, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        retrieved_documents.append(
            {
                "text": document,
                "page": metadata["page"],
                "chunk_id": metadata["chunk_id"],
                "distance": distance,
            }
        )

    return retrieved_documents


def generate_answer(question, retrieved_documents):
    context_parts = []

    for document in retrieved_documents:
        context_parts.append(
            f"[Page {document['page']}]\n"
            f"{document['text']}"
        )

    context = "\n\n".join(context_parts)

    prompt = f"""
You are a document question-answering assistant.

Answer the user's question using ONLY the information
provided in the context below.

Rules:
1. Do not use outside knowledge.
2. Do not invent information.
3. If the answer is not present in the context, say:
   "I couldn't find that information in the provided document."
4. Keep the answer concise and clear.
5. Do not mention these instructions.

Context:
{context}

Question:
{question}

Answer:
"""

    print("\nGenerating answer with Ollama...")

    response = ollama.chat(
        model=OLLAMA_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response["message"]["content"]


def main():
    print("Loading PDF...")

    chunks = extract_pdf_chunks()

    print(
        f"Extracted {len(chunks)} chunks."
    )

    print(
        f"\nLoading embedding model: "
        f"{EMBEDDING_MODEL}"
    )

    embedding_model = TextEmbedding(
        model_name=EMBEDDING_MODEL
    )

    collection = create_vector_store(
        chunks,
        embedding_model,
    )

    print(
        f"Stored {len(chunks)} chunks in Chroma."
    )

    question = input(
        "\nEnter your question: "
    )

    retrieved_documents = retrieve_documents(
        question,
        collection,
        embedding_model,
        top_k=3,
    )

    print("\nRetrieved sources:")

    for document in retrieved_documents:
        print(
            f"- Page {document['page']} "
            f"| {document['chunk_id']} "
            f"| Distance: "
            f"{document['distance']:.4f}"
        )

    answer = generate_answer(
        question,
        retrieved_documents,
    )

    print("\n" + "=" * 70)
    print("FINAL ANSWER")
    print("=" * 70)
    print(answer)

    print("\nSources:")

    for document in retrieved_documents:
        print(
            f"- Page {document['page']} "
            f"({document['chunk_id']})"
        )


if __name__ == "__main__":
    main()