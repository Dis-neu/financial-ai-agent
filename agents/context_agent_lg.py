"""
A RAG agent wrapper for integration into LangGraph.
"""
from typing import TypedDict
from rag.vector_store import load_vector_store
from rag.context_agent import context_agent as rag_query
from agents.state import CreditState


class ContextState(TypedDict):
    ticker: str
    anomaly_question: str
    context_summary: str


# Load the database once during import
_vector_store = None


def _get_store():
    global _vector_store
    if _vector_store is None:
        _vector_store = load_vector_store()
    return _vector_store


def context_agent_lg(state: ContextState) -> dict:
    """RAG agent in LangGraph format."""
    question = state.get("anomaly_question", "")
    if not question:
        return {"context_summary": "(no context requested)"}

    store = _get_store()
    answer = rag_query(store, question, state["ticker"])
    return {"context_summary": answer}