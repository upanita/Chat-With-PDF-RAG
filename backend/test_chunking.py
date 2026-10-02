import re

import pymupdf


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

            # Keep the last few sentences for overlap
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


def main():
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

    print(f"Total chunks: {len(all_chunks)}")

    for chunk in all_chunks:
        print("\n" + "=" * 70)
        print(f"Chunk ID: {chunk['chunk_id']}")
        print(f"Page: {chunk['page']}")
        print(f"Characters: {len(chunk['text'])}")
        print("=" * 70)
        print(chunk["text"])


if __name__ == "__main__":
    main()