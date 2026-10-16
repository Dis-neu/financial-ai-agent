"""Anomaly detector: decides whether to query 10-K for explanations."""
from typing import TypedDict


class AnomalyState(TypedDict):
    financial_summary: str
    risk_summary: str
    benchmark_summary: str
    needs_context: bool
    anomaly_question: str


def anomaly_detector(state: AnomalyState) -> dict:
    benchmark = state.get("benchmark_summary", "").lower()

    questions = []

    if "debt" in benchmark or "d/e" in benchmark or "above normal" in benchmark:
        questions.append(
            "Does the company mention share repurchase programs, buybacks, "
            "or debt issuance as reasons for changes in stockholders' equity?"
        )

    if "margin" in benchmark or "below normal" in benchmark:
        questions.append(
            "What are the main product segments and their respective profit margins? "
            "Are there any one-time items affecting profitability?"
        )

    if not questions:
        questions.append(
            "What are the main financial risks and changes in capital structure?"
        )

    return {
        "needs_context": True,
        "anomaly_question": " | ".join(questions),
    }