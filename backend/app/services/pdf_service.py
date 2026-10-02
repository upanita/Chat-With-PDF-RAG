import re

import pymupdf


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


def create_chunks(text, page_number, document_id):
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
                    "chunk_id": (
                        f"{document_id}-page-"
                        f"{page_number}-chunk-{chunk_number}"
                    ),
                    "document_id": document_id,
                    "page": page_number,
                    "text": " ".join(current_sentences),
                }
            )

            overlap_sentences = []
            overlap_length = 0

            for previous_sentence in reversed(current_sentences):
                if (
                    overlap_length + len(previous_sentence)
                    > CHUNK_OVERLAP
                ):
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
                "chunk_id": (
                    f"{document_id}-page-"
                    f"{page_number}-chunk-{chunk_number}"
                ),
                "document_id": document_id,
                "page": page_number,
                "text": " ".join(current_sentences),
            }
        )

    return chunks


def extract_pdf_chunks(pdf_path, document_id):
    document = pymupdf.open(pdf_path)

    all_chunks = []

    for page_number, page in enumerate(
        document,
        start=1,
    ):
        text = page.get_text()

        page_chunks = create_chunks(
            text,
            page_number,
            document_id,
        )

        all_chunks.extend(page_chunks)

    document.close()

    return all_chunks