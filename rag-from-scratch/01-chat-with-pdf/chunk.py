import re
import unicodedata
from pathlib import Path

from load import load_pdf

HERE = Path(__file__).parent


def clean_text(text):
    # Turn ligatures like "ﬁ" back into normal letters: "speciﬁc" -> "specific"
    text = unicodedata.normalize("NFKC", text)
    # Join words split across lines by a hyphen: "retrie-\nval" -> "retrieval"
    text = re.sub(r"-\s*\n\s*", "", text)
    # Collapse all whitespace (spaces, newlines, tabs) into single spaces
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def chunk_text(text, chunk_size=1000, overlap=200):
    if overlap >= chunk_size:
        raise ValueError("chunk_size must be greater than overlap")

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)

        # Pull end back to the last space so words aren't cut in half
        if end < text_length and text[end] != " ":
            space = text.rfind(" ", start, end)
            if space > start:
                end = space

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        if end == text_length:
            break

        # Next start comes from the end POSITION, and must move forward
        next_start = end - overlap
        start = next_start if next_start > start else end

    return chunks


def chunk_pages(pages, chunk_size=1000, overlap=200):
    all_chunks = []
    for page in pages:
        cleaned = clean_text(page["text"])
        for i, text in enumerate(chunk_text(cleaned, chunk_size, overlap)):
            all_chunks.append({
                "id": f"p{page['page']}-c{i}",
                "page": page["page"],
                "text": text,
            })
    return all_chunks


if __name__ == "__main__":
    pages = load_pdf(HERE / "rag_paper.pdf")
    chunks = chunk_pages(pages)

    lengths = [len(c["text"]) for c in chunks]
    print(f"{len(pages)} pages → {len(chunks)} chunks")
    print(f"avg {sum(lengths) // len(lengths)} chars, min {min(lengths)}, max {max(lengths)}")
    print(f"unique IDs: {len({c['id'] for c in chunks})} (should equal chunk count)")

    for c in chunks[:2]:
        print(f"\n--- {c['id']} (page {c['page']}) ---")
        print(c["text"][:300] + "...")