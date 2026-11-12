import hashlib
from langchain_postgres import PGVector
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

def chunk_id(c):
    key = f"{c.metadata['filename']}:{c.page_content}"
    return hashlib.sha1(key.encode()).hexdigest()

ids = [chunk_id(c) for c in chunks]

store = PGVector(
    embeddings=emb,
    collection_name="knowledge_base",
    connection="postgresql+psycopg://postgres:pass@localhost:5432/postgres",
    use_jsonb=True,
)

store.add_documents(chunks, ids=ids)
print(f"stored {len(ids)} chunks")

for doc, score in store.similarity_search_with_score("What is HNSW?", k=2):
    print(f"{score:.3f} | {doc.metadata['filename']} | {doc.page_content[:60]!r}")