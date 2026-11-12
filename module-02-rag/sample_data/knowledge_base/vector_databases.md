# Embeddings and Vector Databases

An embedding is a list of numbers representing the meaning of text. Similar meanings give
nearby vectors, even with no shared words. nomic-embed-text produces 768 dimensions.

Cosine similarity compares the angle between two vectors: near 1 is very similar, near 0
is unrelated.

A vector database stores embeddings with the source text and metadata and finds nearest
neighbours quickly. Large collections use approximate nearest neighbour indexes such as HNSW,
trading a little accuracy for large speed gains.

Chroma is a simple embedded database for prototypes. FAISS is a fast in-memory similarity
library from Meta. Qdrant is a production vector database with filtering. pgvector adds
vector search to PostgreSQL.