# Module 01: LangChain Core

Foundations: models, prompts, output parsers, structured output, and the `|` pipe (LCEL).

## What each script teaches

| Script | Concept |
|---|---|
| `01_basic_call.py` | A chat model is a Runnable; `.invoke()` returns an `AIMessage` |
| `02_prompt_chain.py` | `prompt \| model \| parser` pipelines |
| `03_structured_output.py` | `with_structured_output()` returns validated Pydantic objects |
| `04_streaming_and_batching.py` | `.stream()` and `.batch()` on any chain |
| `05_exercise_job_parser.py` | Mini project: job postings to typed JSON |

## Run (from the repo root)

```bash
python module-01-langchain-core/01_basic_call.py
python module-01-langchain-core/05_exercise_job_parser.py
```

## Key takeaways

- Every component implements `invoke`, `stream` and `batch`.
- `a | b` feeds a's output into b, so chains are composable.
- Structured output is what makes later agent and RAG steps reliable.
- Local small models are weaker at structured output; keep schemas simple and `temperature=0`.

## Sample output

_Paste the output of `05_exercise_job_parser.py` here once you've run it._
