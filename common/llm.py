"""Shared model factory so every module uses the same local, free Ollama setup.

Change the model once here (or via the OLLAMA_MODEL env var) and all modules follow.
"""
import os

from dotenv import load_dotenv
from langchain_ollama import ChatOllama, OllamaEmbeddings

load_dotenv()

CHAT_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
EMBED_MODEL = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")
BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

def get_llm(temperature: float = 0.0, **kwargs) -> ChatOllama:
    """Return a chat model.
    temperature=0 makes output as repeatable as possible. 
    keep_alive keeps the model in memory between calls, which avoids the slow
    cold start you see on the first request.
    keep_alive="30m" keeps the model loaded, which avoids the slow first call you saw earlier
    """
    return ChatOllama(
        model=CHAT_MODEL,
        base_url=BASE_URL,
        temperature=temperature,
        keep_alive="30m",
        **kwargs,
    )


def get_embeddings() -> OllamaEmbeddings:
    """Return an embedding model (used from Module 2 onwards)."""
    return OllamaEmbeddings(model=EMBED_MODEL, base_url=BASE_URL)
