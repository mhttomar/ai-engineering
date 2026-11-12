import ast
import operator
from datetime import datetime
from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.tools import tool

from common.llm import get_embeddings

ROOT = Path(__file__).parent.parent

# ---------- calculator (safe: no eval) ----------
_OPS = {
    ast.Add: operator.add, ast.Sub: operator.sub,
    ast.Mult: operator.mul, ast.Div: operator.truediv,
    ast.Pow: operator.pow, ast.USub: operator.neg,
}

def _eval(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval(node.left), _eval(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval(node.operand))
    raise ValueError("unsupported expression")

@tool
def calculator(expression: str) -> str:
    """Evaluate a math expression such as '17 * 23 + 4'.
    Supports + - * / ** and parentheses. Use this for ANY arithmetic."""
    try:
        return str(_eval(ast.parse(expression, mode="eval").body))
    except Exception as e:
        return f"Error: {e}"

# ---------- clock ----------
@tool
def current_time() -> str:
    """Get the current local date and time."""
    return datetime.now().strftime("%A, %d %B %Y, %H:%M")

# ---------- your RAG index as a tool ----------
_store = Chroma(
    collection_name="knowledge_base",
    embedding_function=get_embeddings(),
    persist_directory=str(ROOT / "chroma_db"),
)

@tool
def search_docs(query: str) -> str:
    """Search the knowledge base about RAG, vector databases, LangChain, LangGraph
    and LangFlow. Use this for any question about those topics. Input is a short
    search query."""
    docs = _store.similarity_search(query, k=3)
    if not docs:
        return "No relevant documents found."
    return "\n\n".join(
        f"[{d.metadata.get('filename', 'unknown')}] {d.page_content}" for d in docs
    )

TOOLS = [calculator, current_time, search_docs]
TOOL_MAP = {t.name: t for t in TOOLS}