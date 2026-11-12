from langchain.agents import create_agent
from common.llm import get_llm
from my_tools import TOOLS

agent = create_agent(
    get_llm(),
    TOOLS,
    system_prompt="You are a helpful assistant. Use tools when they help. "
                  "For questions about RAG, vector databases or LangChain, always search the docs first.",
)

question = "According to the docs, which vector database adds search to PostgreSQL? Also, what is 2**10?"

result = agent.invoke(
    {"messages": [{"role": "user", "content": question}]},
    config={"recursion_limit": 12},
)

for m in result["messages"]:
    if m.type == "ai" and m.tool_calls:
        print("AI wants:", [(c["name"], c["args"]) for c in m.tool_calls])
    elif m.type == "tool":
        print("TOOL result:", m.content[:100].replace("\n", " "))
    elif m.type == "ai":
        print("FINAL:", m.content)