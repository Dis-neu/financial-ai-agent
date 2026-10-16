"""
RAG agent: searches 10-K for anomaly explanations.
"""
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from rag.vector_store import search_with_mmr


llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0)


def context_agent(vector_store: Chroma, question: str, ticker: str) -> str:
    """Takes a question and returns an answer grounded in the 10-K text."""
    docs = search_with_mmr(vector_store, query=question, ticker=ticker, k=6)

    if not docs:
        return f"[CONTEXT] No relevant fragments found in 10-K for {ticker}."

    print(f"\n[CONTEXT] Found {len(docs)} fragments:")
    for i, doc in enumerate(docs, 1):
        section = doc.metadata.get("section", "?")
        preview = doc.page_content[:150].replace("\n", " ")
        print(f"  [{i}] {section}: {preview}...")

    context_parts = []
    for i, doc in enumerate(docs, 1):
        section = doc.metadata.get("section", "unknown")
        context_parts.append(f"[Fragment {i}, section {section}]:\n{doc.page_content}")

    context = "\n\n".join(context_parts)

    prompt = f"""You are an analyst working with 10-K filings.

Question: {question}

Fragments from the 10-K of {ticker}:
{context}

Answer the question USING ONLY the provided fragments.
If the text does not contain the answer, honestly say "The provided fragments do not contain the answer."
At the end, specify which section (item_1, item_1a, item_7, item_8) you used.

Response format:
ANSWER: [1-2 paragraphs]
SOURCE: [which sections were used]
"""

    response = llm.invoke(prompt)
    return response.content