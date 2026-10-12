from pathlib import Path
from pypdf import PdfReader

HERE = Path(__file__).parent

def load_pdf(path):
    reader = PdfReader(path)
    pages = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        if text.strip():
            pages.append({"page": i + 1, "text": text})
    return pages

if __name__ == "__main__":
    pages = load_pdf(HERE / "rag_paper.pdf")   # change to your PDF's name
    print(f"Loaded {len(pages)} pages with text")
    print(f"--- Page {pages[0]['page']} preview ---")
    print(pages[0]["text"][:500])