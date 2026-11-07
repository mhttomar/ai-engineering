"""Step 4: streaming and batching come free with every Runnable.

Run:  python module-01-langchain-core/04_streaming_and_batching.py
"""
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from common.llm import get_llm

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a concise tutor for {audience}."),
        ("human", "Explain {topic} in 2 sentences."),
    ]
)
chain = prompt | get_llm() | StrOutputParser()

print("--- stream ---")
for chunk in chain.stream({"audience": "a PM", "topic": "RAG in AI"}):
    print(chunk, end="", flush=True)
print("\n")

print("--- batch ---")
topics = ["agents", "chunking", "vector databases"]
results = chain.batch([{"audience": "a PM", "topic": t} for t in topics])
for topic, text in zip(topics, results):
    print(f"[{topic}] {text}\n")
