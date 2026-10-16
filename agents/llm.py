"""A shared LLM for all agents."""
import os
from dotenv import load_dotenv

load_dotenv()

from langchain_groq import ChatGroq


llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0)


def extract_text(response) -> str:
    """Extracts text from an LLM response."""
    content = response.content
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                parts.append(block.get("text", ""))
            elif isinstance(block, str):
                parts.append(block)
        return "\n".join(parts)
    return str(content)