"""Step 1: call a local model directly.

Concept: a chat model is a Runnable. `.invoke()` takes input and returns a message.
Run:  python module-01-langchain-core/01_basic_call.py
"""
from common.llm import get_llm

llm = get_llm()

response = llm.invoke("Explain Retrieval-Augmented Generation (RAG) in one sentence.")

print(type(response).__name__)  # AIMessage
print(response.content)         # the text
print(response.response_metadata.get("eval_count"), "tokens generated")
