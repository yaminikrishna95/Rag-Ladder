from pathlib import Path

import chromadb

from load import load_pdf
from chunk import chunk_pages

HERE = Path(__file__).parent
DB_PATH = HERE / "chroma_db"
COLLECTION = "rag_paper"


def build_index(chunk_size=1000, overlap=200):
    pages = load_pdf(HERE / "rag_paper.pdf")
    chunks = chunk_pages(pages, chunk_size, overlap)

    client = chromadb.PersistentClient(path=str(DB_PATH))

    # Start fresh on every run, so re-running never hits duplicate IDs
    # or leaves stale chunks behind. It's fine if the collection doesn't exist yet.
    try:
        client.delete_collection(COLLECTION)
    except Exception:
        pass

    collection = client.create_collection(COLLECTION)

    # Three parallel lists, all in the same order
    collection.add(
        ids=[c["id"] for c in chunks],
        documents=[c["text"] for c in chunks],
        metadatas=[{"page": c["page"]} for c in chunks],
    )
    return collection


if __name__ == "__main__":
    collection = build_index()
    print(f"Indexed {collection.count()} chunks")

    for question in ["what is retrieval-augmented generation", "best pizza in Chicago"]:
        results = collection.query(query_texts=[question], n_results=3)
        print(f"\nQ: {question}")
        for id_, meta, dist, doc in zip(
            results["ids"][0],
            results["metadatas"][0],
            results["distances"][0],
            results["documents"][0],
        ):
            print(f"  {id_} (page {meta['page']}) distance={dist:.3f} | {doc[:80]}...")