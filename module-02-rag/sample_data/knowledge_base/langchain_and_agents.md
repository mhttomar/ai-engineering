# LangChain, LangGraph and LangFlow

LangChain provides building blocks for LLM apps: models, prompts, parsers, loaders, splitters,
embeddings, vector stores, retrievers and tools. Components are Runnables joined with the pipe
operator (LCEL), and all support invoke, stream and batch.

A retriever takes a query and returns relevant Documents. A vector store becomes a retriever
with as_retriever(), and k controls how many results come back.

An agent is an LLM that decides which tools to call, and in what order, to reach a goal.

LangGraph models an app as a graph of nodes and edges with shared state. It supports loops,
branching, memory persistence and human-in-the-loop approval.

LangFlow is a visual drag-and-drop builder for LangChain-style flows, useful for prototyping
and for exporting flows as an API.