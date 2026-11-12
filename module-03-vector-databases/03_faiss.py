from langchain_community.vectorstores import FAISS
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

INDEX_DIR = ROOT / "faiss_index"

if INDEX_DIR.exists():
    store = FAISS.load_local(str(INDEX_DIR), emb, allow_dangerous_deserialization=True)
    print("loaded from disk")
else:
    store = FAISS.from_documents(chunks, emb)
    store.save_local(str(INDEX_DIR))
    print("built and saved")

for doc, score in store.similarity_search_with_score("What is RAG?", k=2):
    print(f"{score:.3f} | {doc.metadata['filename']} | {repr(doc.page_content[:60])}")