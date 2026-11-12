# Module 02: RAG (Retrieval-Augmented Generation)

A question-answering pipeline that answers from my own documents, with sources, instead of
from the model's memory. Runs fully locally with Ollama.

```
Indexing (once):   files -> load -> split into chunks -> embed -> vector store
Querying (always): question -> embed -> retrieve top-k -> prompt + context -> LLM -> answer + sources
```

## Scripts

| Script | What it demonstrates |
|---|---|
| `01_load_documents.py` | `Document` = text + metadata; loading a folder of markdown |
| `02_chunking.py` | `RecursiveCharacterTextSplitter`, chunk size and overlap |
| `03_embeddings.py` | Text to vectors; cosine similarity between sentences |
| `04_retrieval.py` | In-memory vector store, `similarity_search_with_score`, retrievers |
| `05_rag_chain.py` | Full pipeline: grounded prompt, answer, cited sources |
| `06_experiment_chunk_sizes.py` | Retrieval hit@1 across chunk sizes |

Shared helpers live in `common/documents.py` (`load_documents`, `split_documents`).

## Run

```bash
ollama pull nomic-embed-text
python module-02-rag/05_rag_chain.py
```

## Results

**Before vs after RAG.** Asked "Explain RAG in one sentence" with no context, the model
(llama3.1:8b) described the Recombination Activating Gene, a biology term. With retrieval,
the same question returns: TODO paste your Step 5 answer for "What is RAG?"

**Grounding test.** For "What is the capital of France?" (not in the documents), the system
responded: TODO paste your answer. Expected behaviour is "I don't know based on the provided documents."

**Chunk-size experiment** (7 questions, 3 documents, hit@1):

| chunk_size | overlap | chunks | hit@1 |
|---|---|---|---|
| 200 | 30 | TODO | TODO |
| 500 | 80 | TODO | TODO |
| 1000 | 150 | TODO | TODO |

## Key takeaways

- RAG fixes missing knowledge and ambiguity by putting retrieved text into the prompt.
- The instruction "answer ONLY from the context" is what stops the model falling back on memory.
- Chunk size is a trade-off: large chunks dilute meaning, small chunks lose context.
- Returning source filenames and character offsets makes every answer checkable.
- With a tiny corpus the chunk-size results are noisy; a larger corpus is needed for a real comparison.

## Limitations

- The vector store is in-memory, so it is rebuilt on every run (fixed in Module 03).
- Only markdown files are loaded; PDFs and web pages are not yet supported.