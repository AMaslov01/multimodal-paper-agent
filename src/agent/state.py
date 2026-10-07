"""TypedDict-state для langgraph."""

from __future__ import annotations

from typing import TypedDict

from src.index.retriever import Plan, RetrievedDoc

class AgentState(TypedDict, total=False):
    question: str
    article_readme: str
    plan: Plan
    docs: list[RetrievedDoc]
    draft_answer: str
    timings: dict
