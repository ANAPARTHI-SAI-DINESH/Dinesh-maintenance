# Dinesh-maintenance

> **An end-to-end AI agent that resolves manufacturing equipment faults automatically.**

An operator reports a machine fault in plain English. The agent diagnoses it, retrieves
the official repair procedure from the equipment manual, checks parts inventory, drafts a
purchase order if a part is missing, assigns the right technician, and produces a complete
work order — all in one agentic loop. Every purchase order is held for **human approval**
before it is submitted.

Built with **LangGraph + LangChain**, powered by **Anthropic Claude**, with **RAG** over
the equipment manual (Chroma vector store) and **SQLite** for full persistence.

---

## Table of Contents

- [Features](#features)
- [How It Works](#how-it-works)
- [Tech Stack](#tech-stack)
- [Project Layout](#project-layout)
- [Setup](#setup)
- [Usage](#usage)
- [Architecture](#architecture)
- [Design Principle](#design-principle)
- [Limitations](#limitations)
- [Author](#author)

---

## Features

- **Natural-language fault intake** — describe a fault in plain English via CLI or Streamlit web UI
- **Agentic reasoning loop** — LangGraph `create_react_agent` thinks, calls tools, observes results, and repeats until the work order is complete
- **7 specialized tools** — fault lookup, fault history, manual search (RAG), inventory check, purchase-order drafting, technician matching, work-order creation
- **RAG over the equipment manual** — Chroma vector store with local embeddings (no extra API key needed)
- **SQLite persistence** — faults, inventory, history, technicians, work orders, and purchase orders all stored durably
- **Pydantic-validated outputs** — structured `WorkOrder` and `PurchaseOrder` schemas
- **Human-in-the-loop approval gate** — purchase orders require explicit human approval before submission
- **Test suite** — pytest coverage across tools, DB, RAG, models, and approval logic

---

## How It Works

1. **Operator reports a fault** — e.g. `"Machine CNC-7 threw fault E-214"`
2. **Agent looks up the fault** — retrieves description, likely cause, and recommended part from the DB
3. **Agent searches the manual** — RAG retrieves the official repair procedure for that fault type
4. **Agent checks inventory** — if the required part is in stock, no PO is needed
5. **Agent drafts a PO** — if the part is out of stock, a purchase order is drafted and held for approval
6. **Agent assigns a technician** — matches skill requirements to available technicians
7. **Agent creates a work order** — a structured `WorkOrder` is persisted to SQLite
8. **Human approves/rejects the PO** — via CLI prompt or Streamlit button (no LLM involved in this step)

---

## Tech Stack

| Layer | Technology |
|---|---|
| AI Agent | LangGraph 0.6.11 · `create_react_agent` |
| LLM | Anthropic Claude (`claude-haiku-4-5` dev / `claude-opus-4-8` prod) |
| LLM Framework | LangChain 0.3.30 · langchain-anthropic 0.3.22 |
| RAG / Vector Store | Chroma 1.5.9 · local sentence embeddings |
| Persistence | SQLite (Python stdlib) |
| Data Validation | Pydantic 2.13.4 |
| Web UI | Streamlit 1.50.0 |
| Testing | pytest 8.4.2 |
| Language | Python 3.9+ |

---

## Project Layout

```
Dinesh-maintenance/
├── run.py                  # CLI entry point
├── app.py                  # Streamlit web UI
├── conftest.py             # pytest fixtures
├── requirements.txt
├── .env.example            # copy to .env and add your Anthropic key
│
├── src/
│   ├── agent.py            # LangGraph agent loop (think → tool → observe → repeat)
│   ├── tools.py            # the 7 @tool functions
│   ├── rag.py              # manual chunking, embedding, and retrieval (Chroma)
│   ├── db.py               # SQLite schema + all queries
│   ├── models.py           # Pydantic schemas (WorkOrder, PurchaseOrder)
│   ├── approval.py         # human-in-the-loop PO approval gate
│   └── config.py           # loads .env, selects Claude model
│
├── data/
│   ├── seed.py             # seeds the DB with synthetic plant data
│   └── manual.md           # equipment manual (the RAG corpus)
│
└── tests/
    ├── test_tools.py
    ├── test_db.py
    ├── test_rag.py
    ├── test_models.py
    └── test_approval.py
```

---

## Setup

### Prerequisites

- Python 3.9+
- An [Anthropic API key](https://console.anthropic.com)

### Installation

```bash
git clone https://github.com/ANAPARTHI-SAI-DINESH/Dinesh-maintenance.git
cd Dinesh-maintenance

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate        # macOS/Linux
.venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt

# Configure your API key
cp .env.example .env
# Open .env and paste your Anthropic API key

# Verify the setup (no API key needed for tests)
pytest -q
```

> Each developer uses their **own** Anthropic key. `.env` is gitignored and never committed.

---

## Usage

### CLI

```bash
python run.py
```

Describe a fault when prompted. The agent works through diagnosis, parts check, and work
order creation, then asks for PO approval if needed.

### Streamlit Web UI

```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser. Type a fault description and use the
**Approve / Reject** buttons for any purchase order.

### Example Faults to Try

| Fault description | Expected outcome |
|---|---|
| `Machine CNC-7 threw fault E-214` | Part out of stock → agent drafts a PO for approval |
| `Machine PUMP-3 fault E-091` | Part in stock → no PO needed, work order created directly |

---

## Architecture

For the full system diagram, request flow (sequence diagram), component breakdown, tool
list, and SQLite data model, see [**ARCHITECTURE.md**](ARCHITECTURE.md).

---

## Design Principle

> **AI for judgment. Code for everything else.**

| Done by **Claude** (language & reasoning) | Done by **deterministic code** |
|---|---|
| Diagnose the fault, decide which tools to call | DB lookups (faults, inventory, history) |
| Write the repair procedure from the manual | Purchase-order math (qty × unit cost) |
| Summarize the resolution for the operator | Human-approval gate (no LLM) |
| | Persisting work orders and POs to SQLite |

The LLM is kept out of money-touching and state-changing paths — the agent **drafts**,
deterministic code and a human **decide and commit**.

---

## Limitations

- Uses **synthetic data** and a sample equipment manual — not yet connected to a real CMMS/ERP system
- No authentication or multi-tenancy
- The approval gate runs inline in the CLI/UI rather than as a durable async queue

---

## Author

**Sai Dinesh Anaparthi** ([@ANAPARTHI-SAI-DINESH](https://github.com/ANAPARTHI-SAI-DINESH))
