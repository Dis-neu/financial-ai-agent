"""
Project configuration.
The SEC requires a valid email address to be specified in the User-Agent string; otherwise, it blocks the IP.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# SEC User-Agent (required!)
SEC_COMPANY_NAME = os.getenv("SEC_COMPANY_NAME", "Max Musterman")
SEC_EMAIL = os.getenv("SEC_EMAIL", "maxmusterman@gmail.com")

# Folder for downloaded reports
DATA_DIR = "data/filings"

# Peer group tickers (for benchmarking)
PEER_GROUPS = {
    "AAPL": ["MSFT", "GOOGL", "META", "AMZN"],
    "MSFT": ["AAPL", "GOOGL", "META", "AMZN"],
    "GOOGL": ["AAPL", "MSFT", "META", "AMZN"],
    "TSLA": ["F", "GM", "RIVN", "LCID"],
    "JPM": ["BAC", "WFC", "C", "GS"],
}