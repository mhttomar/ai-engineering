"""Exercise: turn free-text job descriptions into structured data.

Reads sample_data/job_descriptions.txt (postings separated by a line of '---'),
extracts a typed JobPosting from each, and saves results to output/jobs.json.
Run:  python module-01-langchain-core/05_exercise_job_parser.py
"""
import json
from pathlib import Path
from typing import Literal

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from common.llm import get_llm

HERE = Path(__file__).parent


class JobPosting(BaseModel):
    title: str = Field(description="Job title")
    seniority: Literal["intern", "junior", "mid", "senior", "lead"] = Field(
        description="Best guess of seniority level"
    )
    required_skills: list[str] = Field(description="Skills the posting requires")
    location: str = Field(description="City or 'Remote'; 'Unknown' if not stated")


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Extract data exactly as written in the text. "
            "Never add notes or explanations. "
            "Never add information that is not in the text. "
            "Include all technologies mentioned in the posting.",
        ),
        ("human", "{description}"),
    ]
)

chain = prompt | get_llm().with_structured_output(JobPosting)


def main() -> None:
    raw = (HERE / "sample_data" / "job_descriptions.txt").read_text()
    postings = [p.strip() for p in raw.split("---") if p.strip()]

    # batch() runs the chain over all inputs
    results = chain.batch([{"description": p} for p in postings])

    out_dir = HERE / "output"
    out_dir.mkdir(exist_ok=True)
    (out_dir / "jobs.json").write_text(
        json.dumps([r.model_dump() for r in results], indent=2)
    )

    for r in results:
        print(f"{r.title} | {r.seniority} | {r.location} | {', '.join(r.required_skills)}")
    print(f"\nSaved to {out_dir / 'jobs.json'}")


if __name__ == "__main__":
    main()
