from pathlib import Path
from common.documents import load_documents, split_documents
"""
Whole documents blur several topics into one vector. Small focused chunks retrieve better. chunk_overlap repeats a little text between neighbours so a sentence isn’t cut off from its context.

Checkpoint: look at where chunks start and end. Do they break at sensible places (paragraphs)? The splitter tries paragraph breaks first, then lines, then sentences.
"""
KB = Path(__file__).parent / "sample_data" / "knowledge_base"
chunks = split_documents(load_documents(KB), chunk_size=500, chunk_overlap=80)

print(f"{len(chunks)} chunks")
for c in chunks[:3]:
    print("---", Path(c.metadata["source"]).name, "start:", c.metadata["start_index"])
    print(c.page_content)