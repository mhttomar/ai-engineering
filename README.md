# AI Engineering Portfolio

Hands-on learning of **LangChain, LangGraph and LangFlow**: building AI applications with
**RAG, vector databases and agents**. Everything runs **locally and free** using
[Ollama](https://ollama.com). No paid API keys.

## Roadmap

| # | Module | Status |
|---|---|---|
| 01 | [LangChain core](module-01-langchain-core/): models, prompts, chains, structured output | In progress |
| 02 | RAG: loaders, chunking, embeddings, retrieval | Planned |
| 03 | Vector databases: Chroma, FAISS, pgvector, Qdrant | Planned |
| 04 | Agents and tools | Planned |
| 05 | LangGraph: stateful workflows, memory, human-in-the-loop | Planned |
| 06 | LangFlow: visual prototyping and export | Planned |
| 07 | Capstone: document Q&A agent served via FastAPI | Planned |

## Project structure

```
ai-engineering-portfolio/
├── README.md
├── pyproject.toml          # installs the shared `common` package
├── .env.example            # model names, copy to .env
├── .gitignore
├── common/
│   ├── __init__.py
│   └── llm.py              # get_llm() and get_embeddings() used by every module
└── module-01-langchain-core/
    ├── README.md
    ├── 01_basic_call.py
    ├── 02_prompt_chain.py
    ├── 03_structured_output.py
    ├── 04_streaming_and_batching.py
    ├── 05_exercise_job_parser.py
    └── sample_data/job_descriptions.txt
```

## Setup

```bash
# 1. Install Ollama, then pull models
ollama pull llama3.1:8b          # or llama3.2:3b on low-RAM machines
ollama pull nomic-embed-text     # embeddings (used from Module 2)

# 2. Python environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e .

# 3. Optional config
cp .env.example .env             # Windows: copy .env.example .env
```

## Tech

Python, LangChain, LangGraph, LangFlow, Ollama, Chroma/FAISS/Qdrant, FastAPI.
