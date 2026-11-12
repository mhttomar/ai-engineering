from pathlib import Path
from langchain_core.vectorstores import InMemoryVectorStore
from common.documents import load_documents, split_documents
from common.llm import get_embeddings
"""
This runs a small evaluation. For each chunk size it checks whether the top-1 retrieved chunk comes from the expected file (hit@1). Evaluating retrieval with numbers is what separates a portfolio project from a tutorial copy.

Checkpoint: which size wins? With only 7 questions and 3 short docs the results will be close, so add 5 more questions or a few of your own documents to make the comparison meaningful.
"""
KB = Path(__file__).parent / "sample_data" / "knowledge_base"

TEST_SET = [  # (question, file that should contain the answer)
    ("What does RAG stand for?", "rag_overview.md"),
    ("What are the steps in the indexing phase?", "rag_overview.md"),
    ("What is cosine similarity?", "vector_databases.md"),
    ("Which tool is a fast similarity library from Meta?", "vector_databases.md"),
    ("What is HNSW?", "vector_databases.md"),
    ("What can LangGraph do that a simple chain cannot?", "langchain_and_agents.md"),
    ("What is LangFlow used for?", "langchain_and_agents.md"),
]

docs = load_documents(KB)
emb = get_embeddings()

print(f"{'size':>6} {'overlap':>8} {'chunks':>7} {'hit@1':>6}")
for size, overlap in [(200, 30), (500, 80), (1000, 150)]:
    chunks = split_documents(docs, size, overlap)
    store = InMemoryVectorStore.from_documents(chunks, emb)
    hits = sum(
        Path(store.similarity_search(q, k=1)[0].metadata["source"]).name == f
        for q, f in TEST_SET
    )
    print(f"{size:>6} {overlap:>8} {len(chunks):>7} {hits}/{len(TEST_SET)}")