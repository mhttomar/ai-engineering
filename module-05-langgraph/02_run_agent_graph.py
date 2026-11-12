from agent_graph import build_graph, print_trace

graph = build_graph()

print(graph.get_graph().draw_mermaid())   # paste the output into https://mermaid.live

for q in [
    "Say hello in one sentence.",
    "What is 365 * 24?",
    "In the docs, what is cosine similarity?",
]:
    print("\n=== ", q)
    result = graph.invoke({"messages": [("user", q)]})
    print_trace(result["messages"])