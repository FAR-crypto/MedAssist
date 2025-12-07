"""
embeddings_service.py

Lightweight embeddings helper with safe fallbacks so imports succeed
in environments without `chromadb` or `openai` installed. Exposes:
- retrieve_similar_cases(text, k=3) -> list of dicts
- upsert_case(case_id, text) -> bool

This module is defensive: when optional libs are missing it returns
empty results or no-ops so the demo continues to work.
"""
from typing import List, Dict, Optional
import warnings

CHROMA_AVAILABLE = False
OPENAI_AVAILABLE = False

try:
    import chromadb  # type: ignore
    from chromadb.config import Settings  # type: ignore
    CHROMA_AVAILABLE = True
except Exception:
    warnings.warn("chromadb not available; embeddings will be no-op")

try:
    import openai  # type: ignore
    OPENAI_AVAILABLE = True
except Exception:
    warnings.warn("openai package not available; embeddings will be no-op")

# Simple in-memory fallback index
_IN_MEMORY_INDEX: Dict[str, str] = {}

def retrieve_similar_cases(text: str, k: int = 3) -> List[Dict[str, str]]:
    """Return up to `k` similar cases. If chromadb is not available,
    perform a naive substring match against an in-memory index.
    """
    if CHROMA_AVAILABLE:
        try:
            client = chromadb.Client(Settings())
            # use a simple collections-based approach if available
            col = client.get_or_create_collection("cases")
            # chromadb query requires embeddings; safe fallback to empty
            results = col.query(query_texts=[text], n_results=k)
            hits = []
            for ids, metadatas in zip(results.get("ids", []), results.get("metadatas", [])):
                pass
            # We return an empty list for now as complex chroma wiring
            return []
        except Exception:
            return []

    # Fallback: naive substring scoring
    text_l = (text or "").lower()
    scored = []
    for cid, doc in _IN_MEMORY_INDEX.items():
        score = 0
        dl = doc.lower()
        if text_l and text_l in dl:
            score = 10
        else:
            # count shared words
            words = set(text_l.split())
            common = sum(1 for w in words if w and w in dl)
            score = common
        if score > 0:
            scored.append((score, cid, doc))
    scored.sort(reverse=True)
    results = []
    for score, cid, doc in scored[:k]:
        results.append({"case_id": cid, "text": doc, "score": score})
    return results

def upsert_case(case_id: str, text: str) -> bool:
    """Store the case text in the fallback index. If chromadb is available,
    a best-effort upsert would be performed (not implemented here).
    """
    if CHROMA_AVAILABLE:
        try:
            client = chromadb.Client(Settings())
            col = client.get_or_create_collection("cases")
            # production code would compute embeddings and upsert here
            # keep as a no-op to avoid hard dependency
            return True
        except Exception:
            pass

    # fallback: store in-memory
    try:
        _IN_MEMORY_INDEX[case_id] = text or ""
        return True
    except Exception:
        return False

__all__ = ["retrieve_similar_cases", "upsert_case"]
"""Optional embeddings + vector DB (Chroma) service.

Provides upsert_case(text) and retrieve_similar_cases(text, k).
Falls back to no-op if chromadb or OpenAI embeddings unavailable.
"""
import os
from typing import List

_HAS_CHROMA = False
_HAS_OPENAI = False
try:
    import chromadb  # type: ignore
    from chromadb.config import Settings  # type: ignore
    _HAS_CHROMA = True
except Exception:
    _HAS_CHROMA = False

try:
    import openai  # type: ignore
    _HAS_OPENAI = True
except Exception:
    _HAS_OPENAI = False

COLLECTION_NAME = os.environ.get("CHROMA_COLLECTION", "cases")
_client = None
_collection = None

if _HAS_CHROMA:
    try:
        _client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory="./chroma_db"))
        # create or get collection
        try:
            _collection = _client.get_collection(COLLECTION_NAME)
        except Exception:
            _collection = _client.create_collection(COLLECTION_NAME)
    except Exception:
        _HAS_CHROMA = False


def _embed_text_openai(text: str):
    if not _HAS_OPENAI:
        return None
    try:
        resp = openai.Embedding.create(model=os.environ.get("OPENAI_EMBEDDING", "text-embedding-3-small"), input=text)
        return resp["data"][0]["embedding"]
    except Exception:
        return None


def upsert_case(case_id: str, text: str) -> bool:
    """Store case text in vector DB. Returns True if stored."""
    if not _HAS_CHROMA:
        return False
    emb = _embed_text_openai(text)
    if emb is None:
        return False
    try:
        _collection.upsert(ids=[case_id], documents=[text], embeddings=[emb])
        _client.persist()
        return True
    except Exception:
        return False


def retrieve_similar_cases(text: str, k: int = 3) -> List[str]:
    """Return list of similar case texts (strings)."""
    if not _HAS_CHROMA:
        return []
    emb = _embed_text_openai(text)
    if emb is None:
        return []
    try:
        results = _collection.query(embeddings=[emb], n_results=k)
        docs = results.get("documents")
        if docs and len(docs) > 0:
            return docs[0]
    except Exception:
        return []
    return []
