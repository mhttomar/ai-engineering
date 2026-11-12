from pydantic import BaseModel, Field

MAX_DISTANCE = 1.0   # placeholder: calibrate it (see below)

class SearchInput(BaseModel):
    query: str = Field(
        min_length=3,
        max_length=200,
        description="Short search query about the topic, at least 3 characters",
    )

@tool("search_docs", args_schema=SearchInput)
def search_docs(query: str) -> str:
    """Search the knowledge base for facts about RAG, vector databases, LangChain,
    LangGraph and LangFlow. Use ONLY when the user asks about those specific topics.
    Do NOT use for greetings, jokes, math, time, or general chat."""
    try:
        results = _store.similarity_search_with_score(query, k=3)
    except Exception as e:
        return f"Search failed: {e}. Try a different query."

    # keep only chunks that are close enough (Chroma distance: lower = closer)
    relevant = [d for d, score in results if score < MAX_DISTANCE]
    if not relevant:
        return "No relevant documents found."

    return "\n\n".join(
        f"[{d.metadata.get('filename', 'unknown')}] {d.page_content}" for d in relevant
    )