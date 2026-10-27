# Grounded Document Workflow — Public Demo

An original, small portfolio demo of document chunking, lexical retrieval, evidence-linked drafting, and an optional LLM call. It uses invented sample content and contains no code, data, prompts, or configuration copied from a client or employer project.

This **is not** the private AI tender platform described in my [product case study](https://github.com/Deng-summer/ai-bidding-platform-case-study). That larger team project includes document parsing, knowledge retrieval, generation workflows, and review. This repository only demonstrates a few transferable implementation ideas in code. The original platform source remains private because it includes confidential project material; separately reviewed, non-confidential examples may be released later.

## What it shows

1. Add a text document through `POST /documents`.
2. Split it into numbered passages and retrieve relevant passages for a question.
3. Produce an evidence-linked offline preview. If an OpenAI-compatible endpoint is explicitly configured, request an LLM draft and reject citations that do not refer to retrieved passages.

```text
Text document → passages → lexical retrieval → evidence set → preview or opt-in LLM → citation validation
```

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload
```

Open `http://127.0.0.1:8000/docs` for the interactive API. By default, **no text is sent to an external model**.

Optional model use requires `LLM_BASE_URL`, `LLM_API_KEY`, and `LLM_MODEL`. Use only an endpoint you trust and only documents you are allowed to send there. The endpoint must support OpenAI-compatible `/chat/completions` and JSON output.

## Example

```bash
curl -X POST http://127.0.0.1:8000/documents -H 'Content-Type: application/json' -d '{"source":"service-policy","text":"Appointments can be rescheduled online.\n\nInvoices are payable within 30 days."}'
curl -X POST http://127.0.0.1:8000/draft -H 'Content-Type: application/json' -d '{"question":"When are invoices payable?"}'
```

Run checks with `python3 -m unittest -v`.

## Scope and limits

This is a focused demo, not a production SaaS: documents are kept in memory, retrieval is lexical only, and there is no authentication, tenant isolation, file parsing, background queue, or persistent storage. A production system would add those components, access checks before retrieval, audit trails, evaluation data, and human review for consequential outputs.

© 2026 Deng-summer. Portfolio demo.
