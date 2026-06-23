"""Retrieval over the equipment manual (RAG).

Pipeline: load the manual -> split into chunks -> embed each chunk into a vector
-> store in Chroma -> at query time, embed the question and return the most
similar chunks. The agent uses this to ground its repair steps in the manual.

Embeddings use Chroma's built-in local model, so there's no extra API key and
nothing leaves your machine — a good property for plant data.
"""
import os

import chromadb

_MANUAL = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "manual.md")
_DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".chroma")
_COLLECTION = "equipment_manual"


def _chunks(text: str, size: int = 600, overlap: int = 120) -> list:
    """Split text into ~size-character chunks, keeping paragraphs together."""
    paras = [p.strip() for p in text.split("\n\n") if p.strip()]
    out, buf = [], ""
    for p in paras:
        if buf and len(buf) + len(p) > size:
            out.append(buf.strip())
            buf = buf[-overlap:]  # carry a little overlap for context continuity
        buf += "\n\n" + p
    if buf.strip():
        out.append(buf.strip())
    return out


def build_index() -> int:
    """Chunk + embed the manual into Chroma. Returns the number of chunks stored."""
    client = chromadb.PersistentClient(path=_DB_DIR)
    try:
        client.delete_collection(_COLLECTION)  # rebuild fresh each time
    except Exception:
        pass
    col = client.create_collection(_COLLECTION)
    text = open(_MANUAL, encoding="utf-8").read()
    chunks = _chunks(text)
    col.add(documents=chunks, ids=[f"chunk-{i}" for i in range(len(chunks))])
    return len(chunks)


def search_manual_raw(query: str, k: int = 2) -> list:
    """Return the top-k most relevant manual chunks for a query."""
    client = chromadb.PersistentClient(path=_DB_DIR)
    col = client.get_or_create_collection(_COLLECTION)
    res = col.query(query_texts=[query], n_results=k)
    return res["documents"][0] if res.get("documents") else []
