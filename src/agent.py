"""Builds the maintenance agent with LangGraph.

create_react_agent wires the classic agent loop for us:
  1. Send the conversation + the tool list to Claude.
  2. If Claude asks to call a tool, run it and feed the result back.
  3. Repeat until Claude stops calling tools and gives a final answer.

It replaces a hand-written agent loop (~30 lines) with a single call.
"""
from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent

from src.config import MODEL
from src.tools import ALL_TOOLS

SYSTEM_PROMPT = """You are a maintenance resolution agent for a manufacturing plant.

When given a machine fault, resolve it end to end using your tools — do not guess:
1. look_up_fault to understand the fault and the part it needs.
2. get_fault_history to learn how this machine's past faults were fixed.
3. search_manual for the official repair procedure and specs.
4. check_inventory for the recommended part.
5. If the part is OUT OF STOCK, draft_purchase_order (a DRAFT only — a human approves it).
6. find_technician with the skill the fault needs.
7. create_work_order LAST, with a clear step-by-step repair_procedure based on the manual.

Finish with a short plain-English summary: the work order you created, the part
situation (in stock vs PO drafted), and who is assigned.
"""


def build_agent():
    """Construct and return the runnable agent graph."""
    # ChatAnthropic is LangChain's wrapper around the Claude API. We don't set
    # temperature: claude-opus-4-8 rejects it, and the default is fine for haiku.
    llm = ChatAnthropic(model=MODEL, max_tokens=4096)
    return create_react_agent(llm, ALL_TOOLS, prompt=SYSTEM_PROMPT)
