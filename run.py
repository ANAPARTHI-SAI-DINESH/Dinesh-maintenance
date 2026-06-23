"""Run the maintenance agent from the command line.

Usage:
    python run.py
Then describe a fault, e.g.:  Machine CNC-7 threw fault E-214
"""
import json

from langchain_core.messages import HumanMessage

from src import approval, db, rag
from src.agent import build_agent
from src.config import MODEL, require_api_key


def _extract_draft_po(messages):
    """Find the most recent purchase order the agent drafted, if any."""
    for m in reversed(messages):
        if getattr(m, "name", None) == "draft_purchase_order":
            try:
                return json.loads(m.content)
            except (ValueError, TypeError):
                return None
    return None


def main() -> None:
    require_api_key()
    db.init_db()        # set up the database
    rag.build_index()   # index the manual for retrieval
    agent = build_agent()

    print(f"\nMaintenance agent ready (model: {MODEL}).")
    print("Describe a fault, e.g.: 'Machine CNC-7 threw fault E-214'\n")
    user_input = input("Fault > ").strip()
    if not user_input:
        user_input = "Machine CNC-7 threw fault code E-214."
        print(f"(no input - using demo fault: {user_input})")

    result = agent.invoke({"messages": [HumanMessage(content=user_input)]})

    print("\n=== Agent resolution ===\n")
    print(result["messages"][-1].content)

    # if the agent drafted a PO, a human approves before it's submitted.
    po = _extract_draft_po(result["messages"])
    if po:
        approval.request_approval(po)

    print(f"\n(The agent took {len(result['messages'])} messages/steps total.)")


if __name__ == "__main__":
    main()
