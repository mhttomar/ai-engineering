# Retrieval-Augmented Generation (RAG)

RAG stands for Retrieval-Augmented Generation. A large language model answers a question
using documents retrieved at query time, instead of relying only on its training memory.

## Why RAG exists
LLMs have a training cutoff and do not know private data such as company wikis. When they
lack facts they may hallucinate. RAG reduces this by putting relevant text in the prompt
and asking the model to answer only from that text.

## The pipeline
Indexing (once): load documents, split into chunks, embed each chunk, store in a vector database.
Querying (each question): embed the question, retrieve the top-k similar chunks, build a prompt
with those chunks as context, and let the LLM answer, ideally citing sources.

## Common failure modes
Chunks that are too large dilute meaning; too small lose context. Poor retrieval means the
right chunk never reaches the model. Without a "answer only from context" instruction, the
model may answer from memory.