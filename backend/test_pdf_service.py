from app.services.pdf_service import extract_pdf_chunks


PDF_PATH = "sample_data/UPANITA MAHALA 2025 RESUME-2026.pdf"


def main():
    chunks = extract_pdf_chunks(
        PDF_PATH,
        "test-document",
    )

    print(f"Total chunks: {len(chunks)}")
    print(f"First chunk page: {chunks[0]['page']}")
    print(f"First chunk ID: {chunks[0]['chunk_id']}")


if __name__ == "__main__":
    main()