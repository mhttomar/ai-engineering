from common.llm import get_llm
from my_tools import TOOLS
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage

llm = get_llm().bind_tools(TOOLS)

TESTS = [  # (question, expected first tool or None)
    ("What is 12 * 12?", "calculator"),
    ("What is (45 + 15) / 4?", "calculator"),
    ("What does HNSW stand for in the docs?", "search_docs"),
    ("What is LangGraph used for?", "search_docs"),
    ("What time is it right now?", "current_time"),
    ("Say hello in one sentence.", None),
    ("Tell me a joke.", None),
]
SYSTEM = (
    "You are a helpful assistant. Only call a tool when the question needs "
    "arithmetic, the current time, or facts about RAG, vector databases, "
    "LangChain, LangGraph or LangFlow. For greetings, jokes and general "
    "conversation, answer directly without calling any tool."
)

correct = 0
for q, expected in TESTS:
    calls = llm.invoke([SystemMessage(content=SYSTEM), HumanMessage(content=q)]).tool_calls
    got = calls[0]["name"] if calls else None
    ok = got == expected
    correct += ok
    print(f"{'OK  ' if ok else 'FAIL'} | {q:45} | expected={expected} got={got}")

print(f"\nTool-selection accuracy: {correct}/{len(TESTS)}")