"""Benchmark agent: compares metrics against peer group."""
import json
import yfinance as yf

from agents.state import CreditState
from agents.llm import llm, extract_text


def benchmark_agent(state: CreditState) -> dict:
    ticker = state["ticker"]
""" Нужно поработать с peers_map, требует оптимизации"""
    peers_map = {
        "AAPL": ["MSFT", "GOOGL", "META", "AMZN"],
        "MSFT": ["AAPL", "GOOGL", "META", "AMZN"],
        "GOOGL": ["AAPL", "MSFT", "META", "AMZN"],
        "TSLA": ["F", "GM", "RIVN", "LCID"],
        "JPM": ["BAC", "WFC", "C", "GS"],
    }
    peers = peers_map.get(ticker, [])

    if not peers:
        return {"benchmark_summary": f"No peer group data available for {ticker}."}

    target_info = yf.Ticker(ticker).info
    target_metrics = {
        "debt_to_equity": target_info.get("debtToEquity"),
        "profit_margin": target_info.get("profitMargins"),
    }

    peer_metrics = []
    for peer in peers:
        info = yf.Ticker(peer).info
        peer_metrics.append({
            "ticker": peer,
            "debt_to_equity": info.get("debtToEquity"),
            "profit_margin": info.get("profitMargins"),
        })
"""заменить математические операции агента на математические операции в коде, и передавать агенту уже посчитаные значения"""
    
    prompt = f"""You are a comparative valuation analyst.
    Target company: {ticker}
    Target metrics: {json.dumps(target_metrics, indent=2)}
    Peer group metrics: {json.dumps(peer_metrics, indent=2)}

    Calculate the peer group median for each metric and determine
    how the target company compares to the median (in %).
    Provide a verdict: within normal range / above normal / below normal."""

    response = llm.invoke(prompt)
    return {"benchmark_summary": extract_text(response)}