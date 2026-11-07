"""Step 3: force the model to return a typed Python object.

Concept: `with_structured_output(Schema)` turns the model into a typed function.
Agents and RAG pipelines rely on this for reliable data flow.
Tip: small local models can fail on complex schemas. Keep schemas simple.
Run:  python module-01-langchain-core/03_structured_output.py
"""
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from common.llm import get_llm


class Quiz(BaseModel):
    question: str
    options: list[str] = Field(description="Exactly 4 answer choices")
    answer: str = Field(description="The correct option, copied exactly")


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You write quiz questions for {audience}."),
        ("human", "Write one multiple-choice question about {topic}."),
    ]
)

quiz_chain = prompt | get_llm().with_structured_output(Quiz)

quiz = quiz_chain.invoke({"audience": "beginners", "topic": "vector databases"})
print(type(quiz).__name__)
print(quiz.question)
for i, option in enumerate(quiz.options, 1):
    print(f"  {i}. {option}")
print("Answer:", quiz.answer)
