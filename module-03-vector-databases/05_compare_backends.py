import time
from langchain_chroma import Chroma
from langchain_community.vectorstores import FAISS
from langchain_qdrant import QdrantVectorStore
#
from pathlib import Path
from common.documents import load_documents, split_documents
from common.llm import get_embeddings

ROOT = Path(__file__).parent.parent
KB = ROOT / "module-02-rag" / "sample_data" / "knowledge_base"

chunks = split_documents(load_documents(KB))
for c in chunks:  # friendlier metadata for filtering
    c.metadata["filename"] = Path(c.metadata["source"]).name
emb = get_embeddings()
#

TEST_SET = [
    ("What does RAG stand for?", "rag_overview.md"),
    ("What are the steps in the indexing phase?", "rag_overview.md"),
    ("What is cosine similarity?", "vector_databases.md"),
    ("Which tool is a fast similarity library from Meta?", "vector_databases.md"),
    ("What is HNSW?", "vector_databases.md"),
    ("What can LangGraph do that a simple chain cannot?", "langchain_and_agents.md"),
    ("What is LangFlow used for?", "langchain_and_agents.md"),
]

BACKENDS = {
    "chroma": lambda: Chroma.from_documents(chunks, emb, collection_name="bench"),
    "faiss":  lambda: FAISS.from_documents(chunks, emb),
    "qdrant": lambda: QdrantVectorStore.from_documents(
        chunks, emb, location=":memory:", collection_name="bench"),
}

qvecs = [emb.embed_query(q) for q, _ in TEST_SET]  # embed once: isolates the DB's speed

print(f"{'backend':8} {'build s':>8} {'query ms':>9} {'hit@1':>6}")
for name, make in BACKENDS.items():
    t0 = time.perf_counter()
    store = make()
    build = time.perf_counter() - t0

    t0 = time.perf_counter()
    hits = 0
    for (q, expected), v in zip(TEST_SET, qvecs):
        top = store.similarity_search_by_vector(v, k=1)[0]
        hits += top.metadata["filename"] == expected
    per_query = (time.perf_counter() - t0) / len(TEST_SET) * 1000

    print(f"{name:8} {build:8.2f} {per_query:9.2f} {hits}/{len(TEST_SET)}")