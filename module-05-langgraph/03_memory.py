from langgraph.checkpoint.memory import InMemorySaver

from agent_graph import build_graph

graph = build_graph(checkpointer=InMemorySaver())

alice = {"configurable": {"thread_id": "alice"}}
bob = {"configurable": {"thread_id": "bob"}}

graph.invoke({"messages": [("user", "My name is Mohit and I am learning LangGraph.")]}, alice)

r = graph.invoke({"messages": [("user", "What is my name?")]}, alice)
print("alice thread:", r["messages"][-1].content)

r = graph.invoke({"messages": [("user", "What is my name?")]}, bob)
print("bob thread:  ", r["messages"][-1].content)

print("messages stored for alice:", len(graph.get_state(alice).values["messages"]))