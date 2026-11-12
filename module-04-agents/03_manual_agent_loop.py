from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from common.llm import get_llm
from my_tools import TOOLS, TOOL_MAP

llm = get_llm().bind_tools(TOOLS)
MAX_STEPS = 6

def run_agent(question: str) -> str:
    messages = [
        SystemMessage(content="You are a helpful assistant. Use tools when they help. "
                              "Answer concisely, based on tool results."),
        HumanMessage(content=question),
    ]
    for step in range(MAX_STEPS):
        ai = llm.invoke(messages)
        messages.append(ai)

        if not ai.tool_calls:            # no tool requested -> final answer
            return ai.content

        for call in ai.tool_calls:       # run every requested tool
            print(f"  step {step + 1}: {call['name']}({call['args']})")
            tool = TOOL_MAP.get(call["name"])
            result = tool.invoke(call["args"]) if tool else f"Error: unknown tool {call['name']}"
            messages.append(ToolMessage(content=str(result), tool_call_id=call["id"]))

    return "Stopped: too many steps."

for q in [
    "What is 365 * 24?",
    "In the docs, what is cosine similarity?",
    "What day is it today, and what is 100 divided by 8?",
]:
    print("\nQ:", q)
    print("A:", run_agent(q))