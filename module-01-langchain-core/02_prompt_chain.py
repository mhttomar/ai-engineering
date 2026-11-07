"""Step 2: prompt template | model | output parser.

Concept: the `|` operator pipes one Runnable into the next (LCEL).
Run:  python module-01-langchain-core/02_prompt_chain.py
"""
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from common.llm import get_llm

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a concise tutor for {audience}."),
        ("human", "Explain {topic} in 3 bullet points."),
    ]
)

"""
{audience} and {topic} are template variables filled from the dict you pass.
| pipes each step’s output into the next: template to model to parser.
StrOutputParser turns the AIMessage into a plain string.
"""

chain = prompt | get_llm() | StrOutputParser()

print(chain.invoke({"audience": "10 year old", "topic": "embeddings"}))
