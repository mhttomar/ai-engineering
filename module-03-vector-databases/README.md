# Module 03: Vector Databases

The same chunks and embeddings from Module 02, stored in four different vector databases,
plus persistence, filtering and idempotent indexing.

## Scripts

| Script | What it demonstrates |
|---|---|
| `01_chroma_persist.py` | Persistent Chroma store with content-hash IDs; add new, delete stale |
| `02_filters_and_mmr.py` | Metadata filtering and MMR (diverse results) |
| `03_faiss.py` | FAISS index saved to and loaded from disk |
| `04_qdrant.py` | Qdrant in local mode with an explicit client and collection |
| `05_compare_backends.py` | Build time, query time and hit@1 across Chroma, FAISS and Qdrant |
| `06_pgvector_optional.py` | PostgreSQL + pgvector running in Docker |

## Idempotent indexing

Rerunning the indexer must not create duplicates. Each chunk gets an ID derived from its
filename and its text (SHA-1). On each run the script:

1. embeds and adds only chunks whose ID is not already stored (skips slow embedding calls),
2. deletes stored chunks whose ID no longer exists in the source files (removes stale text).

Results: first run added 12, second run added 0 and the store stayed at 12 chunks.

## Backend comparison

In-memory mode, 12 chunks, 7 test questions:

| Backend | Build (s) | Query (ms) | hit@1 |
|---|---|---|---|
| Chroma | TODO | TODO | TODO |
| FAISS | TODO | TODO | TODO |
| Qdrant | TODO | TODO | TODO |

With only 12 chunks the speed differences are noise. Build time is dominated by embedding
calls, which are identical across backends. A meaningful speed comparison needs thousands
of chunks.

| Backend | Best for | Watch out for |
|---|---|---|
| Chroma | Prototypes, simple local apps | Less suited to heavy production load |
| FAISS | Fast in-memory search, research | No built-in metadata filtering or server; pickle files must be trusted |
| Qdrant | Production, rich filtering, scale | Local mode allows one client per folder |
| pgvector | Already running PostgreSQL | You manage indexes and tuning |

Score direction differs: Chroma and FAISS return distances (lower is better); Qdrant returns
cosine similarity (higher is better).

## Problems hit and fixed

- **Qdrant "already accessed by another instance".** My first version tried
  `from_existing_collection`, which opened a client, failed on a fresh folder, and left the
  client open. The fallback then opened a second client on the same folder. Fix: create one
  `QdrantClient`, check `collection_exists`, create the collection if missing, and wrap the
  same client in the vector store.
- **pgvector insert failed with "cannot adapt type ellipsis".** I had left a placeholder
  (`ids=[...]`) in the code, so Python inserted the literal `Ellipsis` as the row ID. Fix:
  pass real content-hash IDs. pgvector upserts by ID, so reruns do not duplicate rows.

## Run

```bash
pip install langchain-chroma langchain-qdrant qdrant-client faiss-cpu
python module-03-vector-databases/01_chroma_persist.py
```