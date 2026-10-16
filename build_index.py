"""
Build the ChromaDB vector store for a given ticker.
Downloads the latest 10-K from SEC EDGAR and indexes it.
"""
import sys
from data_loader.edgar_client import EdgarClient
from data_loader.section_parser import prepare_sections_for_rag, normalize_section
from rag.vector_store import build_vector_store


def main():
    if len(sys.argv) > 1:
        ticker = sys.argv[1].upper().strip()
    else:
        ticker = input("Enter ticker to index (e.g., AAPL): ").upper().strip()

    if not ticker:
        print("Error: ticker is required.")
        sys.exit(1)

    client = EdgarClient()
    sections = client.get_sections(ticker, year=None)

    if not sections:
        print(f"⚠️ No sections found for {ticker}.")
        sys.exit(1)

    clean_sections = {}
    for key, raw_value in sections.items():
        text = normalize_section(raw_value)
        if text:
            clean_sections[key] = text

    docs = prepare_sections_for_rag(clean_sections, ticker, "latest")
    print(f"\n✅ {len(docs)} chunks ready")

    build_vector_store(docs, collection_name="filings")
    print(f"\n✅ Index for {ticker} is ready. Run: python main.py {ticker}")


if __name__ == "__main__":
    main()
