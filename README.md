# Dinesh-maintenance

An AI agent that resolves manufacturing equipment faults end to end. An operator
reports a fault in plain English; the agent diagnoses it, looks up the machine's
history, finds the official repair procedure in the equipment manual, checks
whether the needed part is in stock, drafts a purchase order if it isn't, assigns
a technician, and produces a complete work order. Any purchase order is held for
**human approval** before it is submitted.

Built with **LangGraph + LangChain**, powered by **Anthropic Claude**, with
retrieval (RAG) over the equipment manual and **SQLite** for persistence.

## Architecture

See [**ARCHITECTURE.md**](ARCHITECTURE.md) for the system diagram, request flow,
component breakdown, and data model.

## Features

* Natural-language fault intake (CLI or Streamlit web UI)
* Agentic loop with 7 tools: fault lookup, fault history, manual search (RAG),
inventory check, purchase-order drafting, technician matching, work-order creation
* RAG over the equipment manual (Chroma vector store + local embeddings — no extra key)
* SQLite persistence (faults, inventory, history, technicians, work orders, POs)
* Pydantic-validated outputs
* Human-in-the-loop approval gate for purchase orders
* Test suite (pytest)

## Setup

```bash
git clone <this-repo-url>
cd nik-maintenance
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
cp .env.example .env               # then paste your Anthropic key into .env
pytest -q                          # confirm everything works (no key needed)
```

Get an Anthropic API key at https://console.anthropic.com. Each developer uses
their **own** key — `.env` is gitignored and never committed.

## Usage

```bash
python run.py                      # CLI: describe a fault when prompted
streamlit run app.py               # web UI: type a fault, approve/reject the PO with a button
```

Faults to try:

* `Machine CNC-7 threw fault E-214` — part out of stock → agent drafts a PO for approval
* `Machine PUMP-3 fault E-091` — part in stock → no PO needed

## Project layout

|Path|Responsibility|
|-|-|
|`run.py`|CLI entry point|
|`app.py`|Streamlit web UI|
|`src/agent.py`|LangGraph agent (the loop)|
|`src/tools.py`|the 7 agent tools|
|`src/rag.py`|manual indexing + retrieval (RAG)|
|`src/db.py`|SQLite persistence|
|`src/models.py`|Pydantic schemas|
|`src/approval.py`|human-approval gate|
|`src/config.py`|env / model configuration|
|`data/seed.py`|synthetic plant data|
|`data/manual.md`|equipment manual (RAG corpus)|
|`tests/`|pytest suite|

## Tech stack

Python · LangGraph · LangChain · Anthropic Claude · Chroma · SQLite · Pydantic ·
Streamlit · pytest

## Notes

Self-contained demo using synthetic data and a sample manual — not yet integrated
with a real CMMS/ERP, and without auth or multi-tenancy.

