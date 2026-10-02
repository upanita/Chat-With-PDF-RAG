import pymupdf


PDF_PATH = "sample_data/UPANITA MAHALA 2025 RESUME-2026.pdf"


def main():
    document = pymupdf.open(PDF_PATH)

    print(f"Number of pages: {len(document)}")

    for page_number, page in enumerate(document, start=1):
        text = page.get_text()

        print("\n" + "=" * 70)
        print(f"PAGE {page_number}")
        print("=" * 70)

        print(text[:2000])

    document.close()


if __name__ == "__main__":
    main()