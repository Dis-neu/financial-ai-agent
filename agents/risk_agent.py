"""Risk agent: evaluates market risk."""
import yfinance as yf

from agents.state import CreditState
from agents.llm import llm, extract_text


def risk_agent(state: CreditState) -> dict:
    ticker = state["ticker"]
    stock = yf.Ticker(ticker)
    hist = stock.history(period="90d")

    returns = hist["Close"].pct_change().dropna()
    volatility = returns.std() * (252 ** 0.5)

    prompt = f"""You are a risk analyst. Evaluate the risk of {ticker}
    based on the annualized volatility: {volatility:.2%}
    Provide a brief assessment (2-3 sentences): high/medium/low risk.
    Important: compare against typical volatility of large-cap stocks (25-40%
    is normal, not "high" risk)."""

    response = llm.invoke(prompt)
    return {"risk_summary": extract_text(response)}