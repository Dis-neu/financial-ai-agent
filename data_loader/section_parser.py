"""
Parsing and preparing 10-K sections for RAG.
Splits long texts into chunks for a vector database.
"""
from typing import List, Dict


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """
        Splits text into chunks with overlap.
        Overlap is necessary to avoid losing context at the boundaries.
    """
    if not text:
        return []
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks
def normalize_section(value) -> str:
    """Converts a section to a string, regardless of the format."""
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        # Trying out various possible keys
        for key in ("text", "content", "body", "value"):
            if key in value and isinstance(value[key], str):
                return value[key]
        return ""
    if isinstance(value, list):
        return "\n".join(str(item) for item in value)
    return str(value) if value else ""

def prepare_sections_for_rag(sections, ticker: str, year: int):
    documents = []
    for section_name, raw_value in sections.items():
        text = normalize_section(raw_value)   # ← вот тут
        if not text:
            continue
        chunks = chunk_text(text)
        for i, chunk in enumerate(chunks):
            documents.append({
                "text": chunk,
                "metadata": {
                    "ticker": ticker,
                    "year": year,
                    "section": section_name,
                    "chunk_id": i,
                }
            })
    print(f"[PARSER] {ticker} {year}: {len(documents)} chunk from {len(sections)} section")
    return documents