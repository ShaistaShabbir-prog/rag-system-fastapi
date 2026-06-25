"""
Issue #2: ChromaDB persistent vector store — replaces in-memory FAISS.
"""
import os, logging
log = logging.getLogger(__name__)
CHROMA_PATH = os.getenv("CHROMA_PATH", "./chroma_db")
COLLECTION  = os.getenv("CHROMA_COLLECTION", "documents")

def get_collection():
    try:
        import chromadb
        client = chromadb.PersistentClient(path=CHROMA_PATH)
        return client.get_or_create_collection(
            name=COLLECTION,
            metadata={"hnsw:space": "cosine"}
        )
    except ImportError:
        raise ImportError("pip install chromadb")

def add_documents(texts: list[str], metadatas: list[dict] | None = None,
                  ids: list[str] | None = None) -> int:
    col = get_collection()
    import hashlib
    ids = ids or [hashlib.md5(t.encode()).hexdigest() for t in texts]
    col.add(documents=texts, metadatas=metadatas or [{} for _ in texts], ids=ids)
    log.info("Added %d documents to ChromaDB", len(texts))
    return len(texts)

def query(text: str, n: int = 4, where: dict | None = None) -> list[dict]:
    col = get_collection()
    results = col.query(query_texts=[text], n_results=n, where=where)
    docs = results["documents"][0]
    metas = results["metadatas"][0]
    dists = results["distances"][0]
    return [{"text": d, "metadata": m, "distance": s}
            for d, m, s in zip(docs, metas, dists)]

def collection_stats() -> dict:
    col = get_collection()
    return {"collection": COLLECTION, "count": col.count(), "path": CHROMA_PATH}
