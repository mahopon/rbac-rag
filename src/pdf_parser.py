import fitz


def parse_pdf(file_path: str) -> list[str]:
    doc = fitz.open(file_path)
    pages = []
    for page in doc:
        text = page.get_text()
        pages.append(text)
    doc.close()
    return pages


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python pdf_parser.py <pdf_path>")
        sys.exit(1)

    text_pages = parse_pdf(sys.argv[1])
    for i, page_text in enumerate(text_pages):
        print(f"--- Page {i + 1} ---")
        print(page_text)
