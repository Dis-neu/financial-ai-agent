
"""Financial agent: extracts metrics and evaluates creditworthiness."""
import json
import yfinance as yf

from agents.state import CreditState
from agents.llm import llm, extract_text


def financial_agent(state: CreditState) -> dict:
    ticker = state["ticker"]
    stock = yf.Ticker(ticker)
    info = stock.info

    metrics = {
        "revenue": info.get("totalRevenue"),
        "profit_margin": info.get("profitMargins"),
        "debt_to_equity": info.get("debtToEquity"),
        "current_ratio": info.get("currentRatio"),
    }

    prompt = f"""You are a financial analyst. Evaluate the creditworthiness of {ticker}
    based on these metrics: {json.dumps(metrics, indent=2)}
    Provide a brief summary (3-4 sentences) focusing on debt load and liquidity."""

    response = llm.invoke(prompt)
    return {"financial_summary": extract_text(response)}