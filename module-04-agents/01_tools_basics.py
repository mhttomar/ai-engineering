from my_tools import TOOLS, calculator, current_time, search_docs

for t in TOOLS:
    print(t.name, "|", t.description[:60], "|", t.args)

print(calculator.invoke({"expression": "17 * 23 + 4"}))
print(current_time.invoke({}))
print(search_docs.invoke({"query": "What is HNSW?"})[:200])
print(calculator.invoke({"expression": "__import__('os')"}))   # should be refused