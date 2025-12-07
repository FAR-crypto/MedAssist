"""Optional clinical NER wrapper using scispacy/spacy.

Provides `extract_entities(text)` returning list of entity strings.
If scispacy/spacy are unavailable, falls back to simple symptom tokenization.
"""
from typing import List
import re

_HAS_SPACY = False
try:
    import spacy  # type: ignore
    # scispacy models are heavy; user must install separately (e.g., en_core_sci_sm)
    _HAS_SPACY = True
except Exception:
    _HAS_SPACY = False

_nlp = None
if _HAS_SPACY:
    try:
        # prefer sci model if present
        try:
            _nlp = spacy.load("en_core_sci_sm")
        except Exception:
            _nlp = spacy.load("en_core_web_sm")
    except Exception:
        _nlp = None
        _HAS_SPACY = False


def extract_entities(text: str) -> List[str]:
    """Return extracted entities or tokens approximating symptoms."""
    if not text:
        return []
    if _HAS_SPACY and _nlp:
        doc = _nlp(text)
        ents = [ent.text for ent in doc.ents]
        if ents:
            return ents
    # fallback: split on commas/newlines and take short tokens
    tokens = [t.strip() for t in re.split(r"[,\n;]+", text) if t.strip()]
    # filter out long tokens
    return [t for t in tokens if len(t) < 60][:20]
