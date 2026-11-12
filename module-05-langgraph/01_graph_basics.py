import operator
from typing import Annotated, TypedDict

from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    text: str
    log: list[str]   # reducer: APPEND instead of overwrite


def shout(state: State):
    return {"text": state["text"].upper(), "log": ["shout"]}


def exclaim(state: State):
    return {"text": state["text"] + "!", "log": ["exclaim"]}


graph = StateGraph(State)
graph.add_node("shout", shout)
graph.add_node("exclaim", exclaim)
graph.add_edge(START, "shout")
graph.add_edge("shout", "exclaim")
graph.add_edge("exclaim", END)

app = graph.compile()
print(app.invoke({"text": "Come here", "log": []}))