# Module 04: Agents and Tools

An LLM that decides which tool to call. I built the agent loop by hand first, then used the
framework, then measured how reliably a small local model chooses tools.

## Scripts

| Script | What it demonstrates |
|---|---|
| `my_tools.py` | Three tools: safe calculator, clock, and the Module 03 vector index as `search_docs` |
| `01_tools_basics.py` | Tools are plain functions with name, description and argument schema |
| `02_tool_calling.py` | `bind_tools`: the model returns a tool request; my code runs it |
| `03_manual_agent_loop.py` | The agent loop written by hand, with a step limit |
| `04_create_agent.py` | The same behaviour using `create_agent`, and reading the message trace |
| `05_guardrails_and_eval.py` | Argument validation and a tool-selection test set |

## How an agent works

1. Call the model with the conversation so far.
2. If it requested tools, run them and append the results as tool messages.
3. Repeat until the model answers without requesting a tool, or the step limit is hit.

The model never runs tools itself. It only asks, which keeps execution under my control.

## Tool-selection evaluation

The test checks the model's first decision: which tool (if any) it requests.
Model: llama3.1:8b via Ollama, temperature 0.

| Setup | Needs-tool accuracy | No-tool accuracy |
|---|---|---|
| Baseline: bare question, broad tool description | 5/5 | 0/2 |

**Finding:** the model was over-eager and called `search_docs` even for greetings and jokes.
What fixed it: TODO state which change(s) you found mattered when you switched them off one by one.

## Guardrails

| Guardrail | What it protects against |
|---|---|
| Calculator uses `ast`, not `eval` | Arbitrary code execution from model output |
| Pydantic `args_schema` on search | Empty or malformed queries |
| Errors returned as text | Crashes; lets the agent retry |
| Step / recursion limit | Infinite tool loops |
| Distance cutoff in `search_docs` (calibrated to TODO value) | Irrelevant chunks polluting the answer |
| Precise tool descriptions, including when NOT to use the tool | Wrong or unnecessary tool calls |

## Key takeaways

- Tool descriptions are the interface: vague docstrings lead to wrong choices.
- Small local models over-call tools; instructions and narrow descriptions reduce it.
- A single blended accuracy hides this problem; measure needs-tool and no-tool cases separately.
- Agents fail quietly, so a small test set is cheaper than debugging in production.

## Limitations

- The test set is small (7 cases), so results may not generalise.
- Only the first tool decision is evaluated, not multi-step reasoning or final answer quality.

## Run

```bash
python module-04-agents/03_manual_agent_loop.py
python module-04-agents/05_guardrails_and_eval.py
```