import math
from common.llm import get_embeddings
"""
Checkpoint: the pizza sentence should score clearly lowest. This is semantic similarity: the model compares meaning, not keywords.
"""
emb = get_embeddings()

def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))

vec = emb.embed_query("What is retrieval-augmented generation?")
print(len(vec), "dimensions")

anchor = emb.embed_query("How do I store vectors for semantic search?")
for text in [
    "A vector database stores embeddings and finds nearest neighbours.",
    "Chroma and Qdrant are tools for similarity search.",
    "My favourite pizza topping is mushrooms.",
]:
    print(f"{cosine(anchor, emb.embed_query(text)):.3f}  {text}")