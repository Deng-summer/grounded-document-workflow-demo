"""Minimal in-memory API for the public portfolio demo."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from workflow import Passage, llm_draft, retrieve, split_document

app = FastAPI(title="Grounded Document Workflow Demo")
passages: list[Passage] = []


class DocumentInput(BaseModel):
    source: str = Field(min_length=1, max_length=80)
    text: str = Field(min_length=1, max_length=50_000)


class QuestionInput(BaseModel):
    question: str = Field(min_length=1, max_length=1000)


@app.post("/documents")
def add_document(document: DocumentInput):
    if any(p.source == document.source for p in passages):
        raise HTTPException(status_code=409, detail="Use a unique source name")
    added = split_document(document.source, document.text)
    passages.extend(added)
    return {"source": document.source, "passages": len(added)}


@app.post("/draft")
def draft(input: QuestionInput):
    evidence = retrieve(input.question, passages)
    try:
        result = llm_draft(input.question, evidence)
    except (ValueError, KeyError, OSError) as error:
        raise HTTPException(status_code=502, detail=f"Drafting failed: {type(error).__name__}") from error
    return {**result, "evidence": [{"citation": p.citation, "text": p.text} for p in evidence]}
