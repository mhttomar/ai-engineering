import hashlib
from langchain_chroma import Chroma
from pathlib import Path
from common.documents import load_documents, split_documents
from common.llm import get_embeddings

ROOT = Path(__file__).parent.parent
KB = ROOT / "module-02-rag" / "sample_data" / "knowledge_base"

chunks = split_documents(load_documents(KB))
for c in chunks:  # friendlier metadata for filtering
    c.metadata["filename"] = Path(c.metadata["source"]).name
emb = get_embeddings()

def chunk_id(c):  # ID from CONTENT, so edited text gets a new ID
    key = f"{c.metadata['filename']}:{c.page_content}"
    return hashlib.sha1(key.encode()).hexdigest()

ids = [chunk_id(c) for c in chunks]

store = Chroma(
    collection_name="knowledge_base",
    embedding_function=emb,
    persist_directory=str(ROOT / "chroma_db"),
)

# 1) add only chunks that aren't stored yet (skips slow embedding)
existing = set(store.get()["ids"])
new = [(c, i) for c, i in zip(chunks, ids) if i not in existing]
if new:
    docs, new_ids = zip(*new)
    store.add_documents(list(docs), ids=list(new_ids))

# 2) delete chunks whose source text no longer exists
stale = existing - set(ids)
if stale:
    store.delete(ids=list(stale))

print(f"added {len(new)}, removed {len(stale)}, total {len(store.get()['ids'])}")