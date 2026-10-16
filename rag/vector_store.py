"""
ChromaDB vector database for RAG.
"""
import os
from typing import List, Dict
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

CHROMA_DIR = "data/chroma"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def get_embeddings():
    """Returns an embedding model."""
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )


def build_vector_store(chunks: List[Dict], collection_name: str = "filings") -> Chroma:
    """Creates a vector database from chunks."""
    os.makedirs(CHROMA_DIR, exist_ok=True)

    texts = [c["text"] for c in chunks]
    metadatas = [c["metadata"] for c in chunks]

    print(f"[RAG] Creating a vector database: {len(texts)} chunks...")

    vector_store = Chroma.from_texts(
        texts=texts,
        metadatas=metadatas,
        embedding=get_embeddings(),
        collection_name=collection_name,
        persist_directory=CHROMA_DIR,
    )
    print(f"[RAG] Database saved to: {CHROMA_DIR}")
    return vector_store


def load_vector_store(collection_name: str = "filings") -> Chroma:
    """Loads an existing database."""
    return Chroma(
        collection_name=collection_name,
        embedding_function=get_embeddings(),
        persist_directory=CHROMA_DIR,
    )


def search_with_mmr(vector_store: Chroma, query: str, ticker: str, k: int = 6) -> list:
    """MMR search: k diverse fragments."""
    return vector_store.max_marginal_relevance_search(
        query=query,
        k=k,
        fetch_k=20,
        filter={"ticker": ticker},
    )