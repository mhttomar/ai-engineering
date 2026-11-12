from pathlib import Path
from langchain_core.vectorstores import InMemoryVectorStore
from common.documents import load_documents, split_documents
from common.llm import get_embeddings
"""
from_documents embeds every chunk and stores the vectors. as_retriever() wraps the store in the standard interface that chains and agents use. We use an in-memory store for now. Module 3 swaps in real vector databases.

Checkpoint: does each question pull chunks from the file you’d expect? If one doesn’t, that’s a retrieval failure. Note which one.
"""
KB = Path(__file__).parent / "sample_data" / "knowledge_base"
chunks = split_documents(load_documents(KB))
store = InMemoryVectorStore.from_documents(chunks, get_embeddings())

for q in ["What does RAG stand for?",
          "Which database adds vector search to PostgreSQL?",
          "What is a node in LangGraph?"]:
    print("\nQ:", q)
    for doc, score in store.similarity_search_with_score(q, k=2):
        print(f"  {score:.3f} | {Path(doc.metadata['source']).name} | "
              f"{doc.page_content[:80]!r}")

retriever = store.as_retriever(search_kwargs={"k": 3})