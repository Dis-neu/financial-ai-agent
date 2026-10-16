"""
Downloading and parsing 10-K filings via edgartools.
"""
import os
from edgar import Company, set_identity
from config import SEC_EMAIL, DATA_DIR


class EdgarClient:
    """A client for interacting with SEC EDGAR via edgar tools."""

    def __init__(self):
        os.makedirs(DATA_DIR, exist_ok=True)
        # The SEC requires identification — edgartools uses it for requests
        set_identity(SEC_EMAIL)

    def get_sections(self, ticker: str, year: int = None) -> dict:
        """
        Extracts high-quality sections from a 10-K.
        ALWAYS returns a dictionary (maybe empty, but never None).
        """
        try:
            company = Company(ticker)
            filings = company.get_filings(form="10-K")

            if not filings:
                print(f"[EDGAR] 10-K for {ticker} not found.")
                return {}

            # Take the latest report (or a specific year, if one is indicated)
            if year is None:
                filing = filings.latest()
            else:
                year_filings = filings.filter(filing_date=f"{year}-01-01:{year}-12-31")
                filing = year_filings.latest() if year_filings else filings.latest()

            tenk = filing.obj()
            print(f"[EDGAR] Отчёт: {filing.form} от {filing.filing_date}")

            # Let’s try extracting the sections one by one, each within its own try block
            sections = {}

            for key, accessor in {
                "item_1": lambda t: t.business,
                "item_1a": lambda t: t.risk_factors,
                "item_7": lambda t: t["Item 7"],
                "item_8": lambda t: t["Item 8"],
            }.items():
                try:
                    value = accessor(tenk)
                    if value:
                        sections[key] = str(value)
                except Exception as inner_e:
                    print(f"[EDGAR] Section {key} unavailable: {inner_e}")

            if not sections:
                print(f"[EDGAR] Failed to extract any sections.")
                return {}

            print(f"[EDGAR] Sections found: {list(sections.keys())}")
            return sections

        except Exception as e:
            print(f"[EDGAR] Error extracting sections: {e}")
            return {}  # ← we guarantee the return of an empty dictionary
