import sys
from pathlib import Path
from typing import Literal

from langchain_core.messages import SystemMessage, ToolMessage
from langchain_core.tools import tool
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode
from langgraph.types import Command, interrupt
from pydantic import BaseModel, Field

from common.llm import get_llm

# reuse the Module 04 tools
sys.path.insert(0, str(Path(__file__).parent.parent / "module-04-agents"))
from my_tools import TOOLS  # noqa: E402

SYSTEM = (
    "You are a helpful assistant. Only call a tool when the question needs "
    "arithmetic, the current time, sending an email, or facts about RAG, vector "
    "databases, LangChain, LangGraph or LangFlow. For greetings, jokes and general "
    "conversation, answer directly without calling any tool."
)


# ---------- a risky tool: needs human approval ----------
@tool
def send_email(to: str, subject: str, body: str) -> str:
    """Send an email. Use only when the user explicitly asks to send an email."""
    print(f"\n[FAKE EMAIL SENT] to={to} subject={subject!r}")
    return f"Email sent to {to}."


ALL_TOOLS = TOOLS + [send_email]
RISKY = {"send_email"}

llm = get_llm()
llm_with_tools = llm.bind_tools(ALL_TOOLS)


# ---------- router: does this message need tools at all? ----------
class Route(BaseModel):
    needs_tool: bool = Field(
        description="True ONLY if the question needs arithmetic, the current time, "
        "sending an email, or facts about RAG, vector databases, LangChain, "
        "LangGraph or LangFlow. False for greetings, jokes, general knowledge, chat."
    )

gate = llm.with_structured_output(Route)


def route_start(state: MessagesState) -> Literal["agent", "chat"]:
    try:
        return "agent" if gate.invoke(state["messages"][-1].content).needs_tool else "chat"
    except Exception:
        return "agent"          # if the gate fails, fall back to the capable path


# ---------- nodes ----------
def chat(state: MessagesState):
    reply = llm.invoke([SystemMessage(content=SYSTEM)] + state["messages"])
    return {"messages": [reply]}


def agent(state: MessagesState):
    reply = llm_with_tools.invoke([SystemMessage(content=SYSTEM)] + state["messages"])
    return {"messages": [reply]}


def after_agent(state: MessagesState):
    calls = state["messages"][-1].tool_calls
    if not calls:
        return END
    if any(c["name"] in RISKY for c in calls):
        return "approval"
    return "tools"


def approval(state: MessagesState) -> Command[Literal["tools", "agent"]]:
    calls = state["messages"][-1].tool_calls
    risky = [c for c in calls if c["name"] in RISKY]

    decision = interrupt({                       # <- graph PAUSES here
        "question": "Approve these actions? (yes/no)",
        "actions": [{"tool": c["name"], "args": c["args"]} for c in risky],
    })

    if str(decision).strip().lower() in ("y", "yes"):
        return Command(goto="tools")

    rejected = [
        ToolMessage(content="The user rejected this action. Do not retry it.",
                    tool_call_id=c["id"])
        for c in calls
    ]
    return Command(goto="agent", update={"messages": rejected})


# ---------- build ----------
def build_graph(checkpointer=None):
    g = StateGraph(MessagesState)
    g.add_node("chat", chat)
    g.add_node("agent", agent)
    g.add_node("tools", ToolNode(ALL_TOOLS))
    g.add_node("approval", approval)

    g.add_conditional_edges(START, route_start, ["agent", "chat"])
    g.add_edge("chat", END)
    g.add_conditional_edges("agent", after_agent, ["approval", "tools", END])
    g.add_edge("tools", "agent")      # after a tool runs, the agent looks at the result
    # "approval" has no outgoing edge: it routes itself with Command(goto=...)
    return g.compile(checkpointer=checkpointer)


def print_trace(messages):
    for m in messages:
        if m.type == "human":
            print("USER :", m.content)
        elif m.type == "ai" and m.tool_calls:
            print("AI   : calls", [(c["name"], c["args"]) for c in m.tool_calls])
        elif m.type == "ai":
            print("AI   :", m.content)
        elif m.type == "tool":
            print("TOOL :", str(m.content)[:100].replace("\n", " "))