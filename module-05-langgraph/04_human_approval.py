from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command

from agent_graph import build_graph, print_trace

graph = build_graph(checkpointer=InMemorySaver())
config = {"configurable": {"thread_id": "email-1"}}

graph.invoke(
    {"messages": [("user", "Send an email to bob@example.com with subject 'Meeting' "
                           "saying the meeting is at 5pm.")]},
    config,
)

state = graph.get_state(config)
if state.next:                                   # the graph is paused
    print("PAUSED before:", state.next)
    print("Pending:", state.tasks[0].interrupts[0].value)
    answer = input("Approve? (yes/no): ")
    graph.invoke(Command(resume=answer), config)  # resume with the human's answer
else:
    print("No approval was requested.")

print()
print_trace(graph.get_state(config).values["messages"])