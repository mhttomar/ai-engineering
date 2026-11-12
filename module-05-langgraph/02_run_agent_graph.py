from agent_graph import build_graph, print_trace

graph = build_graph()

print(graph.get_graph().draw_mermaid())   # paste the output into https://mermaid.live

for q in [
    "Say hello in one sentence.",
    "What is 365 * 24?",
    "In the docs, what is cosine similarity?",
]:
    print("\n===", q)
    print("USER :", q)

    messages = []
    for update in graph.stream({"messages": [("user", q)]}, stream_mode="updates"):
        for node, changes in update.items():
            print(f"[node ran: {node}]")
            if isinstance(changes, dict) and "messages" in changes:
                messages.extend(changes["messages"])

    print_trace(messages)
