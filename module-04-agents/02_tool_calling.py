from common.llm import get_llm
from my_tools import TOOLS

llm = get_llm().bind_tools(TOOLS)

for q in ["What is 17 * 23 + 4?", "What does RAG stand for?", "Say hello"]:
    resp = llm.invoke(q)
    print("\nQ:", q)
    print("text:      ", repr(resp.content))
    print("tool_calls:", resp.tool_calls)