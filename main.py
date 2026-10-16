"""
Точка входа: запуск полного пайплайна кредитного анализа.

Пайплайн:
    START → financial ┐
          → risk      ├→ anomaly → context → synthesis → END
          → benchmark ┘
"""
"""
Точка входа: запуск полного пайплайна кредитного анализа.
"""
import sys
from langgraph.graph import StateGraph, START, END

from agents.state import CreditState
from agents.financial_agent import financial_agent
from agents.risk_agent import risk_agent
from agents.benchmark_agent import benchmark_agent
from agents.anomaly_detector import anomaly_detector
from agents.context_agent_lg import context_agent_lg
from agents.synthesis_agent import synthesis_agent


def get_ticker() -> str:
    """Получает тикер из CLI-аргумента или запрашивает интерактивно."""
    if len(sys.argv) > 1:
        return sys.argv[1].upper().strip()

    ticker = input("Enter ticker (e.g., AAPL, MSFT, TSLA): ").upper().strip()
    if not ticker:
        print("Error: ticker is required.")
        sys.exit(1)
    return ticker


def build_credit_graph():
    """Собирает полный граф кредитного анализа."""
    graph = StateGraph(CreditState)

    graph.add_node("financial", financial_agent)
    graph.add_node("risk", risk_agent)
    graph.add_node("benchmark", benchmark_agent)
    graph.add_node("anomaly", anomaly_detector)
    graph.add_node("context", context_agent_lg)
    graph.add_node("synthesis", synthesis_agent)

    graph.add_edge(START, "financial")
    graph.add_edge(START, "risk")
    graph.add_edge(START, "benchmark")

    graph.add_edge("financial", "anomaly")
    graph.add_edge("risk", "anomaly")
    graph.add_edge("benchmark", "anomaly")

    graph.add_edge("anomaly", "context")
    graph.add_edge("context", "synthesis")
    graph.add_edge("synthesis", END)

    return graph.compile()


def print_report(result: dict) -> None:
    print("=" * 60)
    print(f"CREDIT REPORT: {result['ticker']}")
    print("=" * 60)
    print(f"\n📊 Financial Analysis:\n{result['financial_summary']}")
    print(f"\n⚠️ Risk Analysis:\n{result['risk_summary']}")
    print(f"\n🔍 Peer Comparison:\n{result['benchmark_summary']}")

    if result.get("context_summary"):
        print(f"\n📚 Context from 10-K:\n{result['context_summary']}")

    print(f"\n🎯 VERDICT:\n{result['verdict']}")


if __name__ == "__main__":
    ticker = get_ticker()
    app = build_credit_graph()
    result = app.invoke({"ticker": ticker})
    print_report(result)