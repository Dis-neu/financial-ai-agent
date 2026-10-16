"""Shared state for all LangGraph agents."""
from typing import TypedDict


class CreditState(TypedDict):
    ticker: str
    financial_summary: str
    risk_summary: str
    benchmark_summary: str
    needs_context: bool
    anomaly_question: str
    context_summary: str
    verdict: str