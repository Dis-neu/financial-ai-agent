# Financial AI Agent — Credit Analysis with RAG

A multi-agent system built on **LangGraph** for automated credit analysis of public companies, using **SEC 10-K filings** as the primary source of truth. The system combines quantitative metrics, peer comparison, and retrieval-augmented generation (RAG) to produce auditable credit verdicts.

---

## 🎯 What It Does

Given a stock ticker (e.g., `AAPL`), the system:

1. **Pulls financial metrics** from market data (revenue, margins, D/E, current ratio)
2. **Assesses market risk** via annualized volatility
3. **Compares against a peer group** — calculates medians and deviations
4. **Detects anomalies** — flags metrics that deviate significantly from peers
5. **Retrieves explanations** from the company's 10-K filing (RAG over SEC EDGAR)
6. **Issues a credit verdict** — `INVEST` / `HOLD` / `AVOID` — with explicit criteria and audit trail

Example output for AAPL:

```
VERDICT: HOLD
Reason: D/E deviation +118% from peer median (>100%),
        margin 21% below median (within 10-30% range → HOLD).
        10-K context confirms high D/E is driven by buyback program,
        not by credit deterioration.
Risks:  Rising interest rates, YoY revenue decline, margin compression.
```

---

## 🏗️ Architecture

```
                START
                  │
        ┌─────────┼─────────┐
        ▼         ▼         ▼
   financial    risk    benchmark      ← fan-out (parallel)
        │         │         │
        └─────────┼─────────┘
                  ▼
            anomaly_detector           ← decides if 10-K context is needed
                  │
                  ▼
            context_agent              ← RAG over SEC 10-K (ChromaDB)
                  │
                  ▼
             synthesis                 ← final verdict with criteria
                  │
                  ▼
                 END
```

**Six specialized agents**, each with a clear responsibility:

| Agent | Role |
|---|---|
| `financial_agent` | Extracts financial metrics and evaluates creditworthiness |
| `risk_agent` | Evaluates market risk via volatility |
| `benchmark_agent` | Compares metrics against peer group medians |
| `anomaly_detector` | Decides whether 10-K context is required |
| `context_agent` | RAG search over 10-K for explanations (MMR retrieval) |
| `synthesis_agent` | Issues the final verdict using strict criteria |

---

## 🛠️ Tech Stack

- **LangGraph** — multi-agent orchestration
- **Groq** (`openai/gpt-oss-120b`) — LLM reasoning
- **ChromaDB** — local vector store
- **sentence-transformers** (`all-MiniLM-L6-v2`) — embeddings
- **edgartools** — SEC EDGAR filing retrieval
- **yfinance** — market data
- **Python 3.12**

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/Dis-neu/financial-ai-agent.git
cd financial-ai-agent
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

Copy `.env.example` to `.env` and fill in:

```env
SEC_COMPANY_NAME=YourName
SEC_EMAIL=your_real_email@example.com
GROQ_API_KEY=your_groq_api_key
```

- **SEC_EMAIL** must be a real email — SEC requires it for API access.
- **GROQ_API_KEY** is free — get it at [console.groq.com](https://console.groq.com).

### 4. Build the vector store (one-time, ~3 min)

```bash
python build_index.py AAPL
```

This downloads the latest 10-K from SEC EDGAR and builds a ChromaDB index.

### 5. Run the analysis

```bash
python main.py AAPL
```

Or interactively:

```bash
python main.py
>>> Enter ticker (e.g., AAPL, MSFT, TSLA): TSLA
```

---

## 📁 Project Structure

```
.
├── agents/                  # LangGraph agents
│   ├── state.py             # Shared CreditState
│   ├── llm.py               # Groq LLM + text extraction
│   ├── financial_agent.py
│   ├── risk_agent.py
│   ├── benchmark_agent.py
│   ├── anomaly_detector.py
│   ├── context_agent_lg.py  # RAG wrapper for LangGraph
│   └── synthesis_agent.py
├── data_loader/             # SEC EDGAR integration
│   ├── edgar_client.py
│   └── section_parser.py
├── rag/                     # Retrieval-Augmented Generation
│   ├── vector_store.py      # ChromaDB + MMR search
│   └── context_agent.py     # RAG query logic
├── data/                    # 10-K filings + ChromaDB (gitignored)
├── exports/                 # Output reports (gitignored)
├── main.py                  # Entry point
├── config.py                # Settings
└── requirements.txt
```

---

## 🧠 Key Design Decisions

### Why peer comparison?

A raw metric (e.g., D/E = 78.4) is meaningless without context. The system calculates the **median** of a peer group and expresses deviations as percentages. This turns "high" into "117% above median."

### Why RAG over 10-K?

Market data gives numbers. 10-K filings explain **why** those numbers exist. For example, Apple's high D/E is driven by its share buyback program (which reduces equity), not by credit deterioration. RAG surfaces this context.

### Why MMR retrieval?

Maximum Marginal Relevance returns fragments that are both **relevant** and **diverse**. Without it, all top-4 fragments could come from the same section, losing cross-sectional context.

### Why anomaly_detector?

Not every analysis needs 10-K context. The anomaly detector only triggers RAG when a metric deviates significantly — this saves tokens and keeps latency low.

### Why strict verdict criteria?

LLMs tend to "drift" between categories without hard rules. The synthesis agent uses explicit numeric thresholds (±30%, 10-30%, >30%) to produce auditable verdicts.

---

## 📊 Example Output

See [`examples/aapl_report.md`](examples/aapl_report.md) for a full sample report.

---

## 🔒 Security

- **API keys** are stored in `.env` (gitignored)
- **10-K filings** and **vector stores** are local-only (gitignored)
- **No user data** leaves the machine except LLM queries to Groq

---

## 🛣️ Roadmap

- [x] Multi-agent credit analysis
- [x] RAG over SEC 10-K filings
- [x] Peer group benchmarking
- [x] Anomaly detection + context retrieval
- [ ] Multi-year financial trend analysis
- [ ] Human-in-the-loop verdict approval
- [ ] Model risk documentation (Model Card generation)
- [ ] Macro-event correlation agent

---

## 📚 Background

This project is part of a learning path toward **AI + Finance** specialization, focusing on **Risk / Model Validation**.

Key skills demonstrated:
- Multi-agent orchestration with LangGraph
- Retrieval-Augmented Generation (RAG) over financial documents
- Grounded LLM reasoning with source citations
- Auditable verdict generation with explicit criteria
- Production-grade Python project structure

---

## 📄 License

MIT

---

## 🤝 Contributing

This is a personal learning project, but issues and suggestions are welcome.
