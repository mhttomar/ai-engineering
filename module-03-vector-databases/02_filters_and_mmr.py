from langchain_chroma import Chroma
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

store = Chroma(collection_name="knowledge_base", embedding_function=emb,
               persist_directory=str(ROOT / "chroma_db"))

q = "How do I search for similar items?"

print("--- plain search ---")
for d in store.similarity_search(q, k=3):
    print(d.metadata["filename"], "|", repr(d.page_content[:60]))

print("--- filtered to one file ---")
for d in store.similarity_search(q, k=3, filter={"filename": "langchain_and_agents.md"}):
    print(d.metadata["filename"], "|", repr(d.page_content[:60]))

print("--- MMR (diverse results) ---")
for d in store.max_marginal_relevance_search(q, k=3, fetch_k=8):
    print(d.metadata["filename"], "|", repr(d.page_content[:60]))