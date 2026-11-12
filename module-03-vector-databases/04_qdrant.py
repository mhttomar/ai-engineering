from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
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

COLLECTION = "knowledge_base"

client = QdrantClient(path=str(ROOT / "qdrant_db"))   # the ONLY client for this folder

is_new = not client.collection_exists(COLLECTION)
if is_new:
    dim = len(emb.embed_query("dimension probe"))      # vector size comes from the model
    client.create_collection(
        COLLECTION,
        vectors_config=VectorParams(size=dim, distance=Distance.COSINE),
    )

store = QdrantVectorStore(client=client, collection_name=COLLECTION, embedding=emb)

if is_new:
    store.add_documents(chunks)
    print(f"created collection with {len(chunks)} chunks")
else:
    print("opened existing collection")

for doc, score in store.similarity_search_with_score(
    "Which database adds vector search to PostgreSQL?", k=2
):
    print(f"{score:.3f} | {doc.metadata['filename']} | {doc.page_content[:60]!r}")