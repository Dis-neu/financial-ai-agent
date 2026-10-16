"""Synthesis agent: issues the final credit verdict."""
from agents.state import CreditState
from agents.llm import llm, extract_text


def synthesis_agent(state: CreditState) -> dict:
    prompt = f"""You are the head of the credit committee.

Financial analysis: {state['financial_summary']}
Risk analysis: {state['risk_summary']}
Peer group comparison: {state['benchmark_summary']}
10-K context: {state.get('context_summary', '(none)')}

Based on these four reports, issue a verdict for {state['ticker']}:
- INVEST (low risk)
- HOLD (medium risk)
- AVOID (high risk)

CRITERIA (apply strictly):
- INVEST: D/E within ±30% of peer group median AND margin ≥ median
- HOLD:   D/E deviation 30-100% OR margin 10-30% below median
- AVOID:  D/E deviation > 100% AND margin > 30% below median
         OR signs of default / YoY revenue decline

If the 10-K context explains an anomaly as a structural feature
(e.g., buyback program, one-time items), treat it as NOT a credit risk indicator.

Response format:
VERDICT: [X]
Reason: [which criteria triggered]
Risks: [what could change the verdict]
"""
    response = llm.invoke(prompt)
    return {"verdict": extract_text(response)}