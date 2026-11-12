from pathlib import Path
from common.documents import load_documents

KB = Path(__file__).parent / "sample_data" / "knowledge_base"
docs = load_documents(KB)

print(f"Loaded {len(docs)} documents")
for d in docs:
    print(Path(d.metadata["source"]).name, len(d.page_content), "chars")
print(docs[0].metadata)