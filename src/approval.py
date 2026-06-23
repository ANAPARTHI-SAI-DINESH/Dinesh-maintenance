"""Human-in-the-loop approval gate.

Rule: anything that touches the outside world (submitting a PO) is an APPROVAL
step, not an AI step. The agent DRAFTS the PO; a human approves before it's
'submitted'. This gate is plain deterministic code — no LLM involved.
"""
import json

from src import db


def request_approval(po: dict, input_fn=input) -> bool:
    """Show the drafted PO and ask a human to approve it. Returns True if approved.

    input_fn is injectable so tests (and the web UI) can supply the decision
    instead of reading from the keyboard.
    """
    print("\n--- PURCHASE ORDER (needs human approval) ---")
    print(f"  Part : {po.get('part_name')} ({po.get('part_number')})")
    print(f"  Qty  : {po.get('quantity')} @ ${po.get('unit_cost')} = ${po.get('total_cost')}")
    print(f"  From : {po.get('supplier')}")
    answer = input_fn("Approve and submit this PO? [y/N] ").strip().lower()
    approved = answer in ("y", "yes")
    db.save_purchase_order(json.dumps(po), "SUBMITTED" if approved else "REJECTED")
    print("  -> SUBMITTED" if approved else "  -> REJECTED")
    return approved
