"""The agent's tools — plain Python functions wrapped with @tool.

@tool turns a function into something the LangGraph agent can CALL. The docstring
tells the model *when* to call it; the type hints become the input schema. These
now read from SQLite (src/db.py) and the manual index (src/rag.py).
"""
import itertools
import json
from typing import List

from langchain_core.tools import tool

from src import db
from src.models import PurchaseOrder, WorkOrder
from src.rag import search_manual_raw

_wo_ids = itertools.count(1001)  # WO-1001, WO-1002, ...


@tool
def look_up_fault(fault_code: str) -> str:
    """Look up what a machine fault code means. Call this FIRST for any fault.
    Returns description, likely cause, the part it needs, and the skill required.
    Args: fault_code, e.g. 'E-214'."""
    f = db.get_fault(fault_code)
    return json.dumps(f) if f else f"Unknown fault code '{fault_code}'."


@tool
def get_fault_history(machine_id: str) -> str:
    """Get how this machine's PAST faults were resolved — useful for recurring
    issues. Args: machine_id, e.g. 'CNC-7'."""
    rows = db.get_history(machine_id)
    return json.dumps(rows) if rows else f"No history on record for {machine_id}."


@tool
def search_manual(query: str) -> str:
    """Search the equipment manual for the official repair procedure and specs.
    Call this to base the repair steps on the manual instead of guessing.
    Args: query, e.g. 'spindle bearing over-temperature procedure'."""
    docs = search_manual_raw(query, k=2)
    return "\n\n---\n\n".join(docs) if docs else "Nothing relevant in the manual."


@tool
def check_inventory(part_number: str) -> str:
    """Check whether a spare part is in stock, before scheduling a repair.
    Args: part_number, e.g. 'BRG-6207'."""
    p = db.get_part(part_number)
    if not p:
        return f"Part '{part_number}' is not in the catalog."
    return json.dumps({**p, "in_stock": p["qty"] > 0})


@tool
def draft_purchase_order(part_number: str, quantity: int) -> str:
    """Draft a purchase order for a part. Call ONLY when the part is out of stock.
    The PO is a DRAFT — never submitted automatically; a human approves it.
    Args: part_number, quantity."""
    p = db.get_part(part_number)
    if not p:
        return f"Cannot draft PO: '{part_number}' not in catalog."
    po = PurchaseOrder(
        part_number=p["part_number"],
        part_name=p["name"],
        quantity=quantity,
        unit_cost=p["unit_cost"],
        total_cost=round(p["unit_cost"] * quantity, 2),
        supplier=p["supplier"],
    )
    return po.model_dump_json()


@tool
def find_technician(skill: str) -> str:
    """Find an available technician with a skill ('spindle', 'hydraulics',
    'electrical', 'mechanical') and their next free slot. Args: skill."""
    t = db.find_technician_by_skill(skill)
    return json.dumps(t) if t else f"No technician available with skill '{skill}'."


@tool
def create_work_order(
    machine_id: str,
    fault_code: str,
    diagnosis: str,
    part_needed: str,
    part_in_stock: bool,
    assigned_technician: str,
    scheduled_time: str,
    repair_procedure: List[str],
) -> str:
    """Create the final work order. Call LAST, after diagnosing, searching the
    manual, checking the part, and finding a technician. repair_procedure is a
    list of step strings (base them on the manual)."""
    wo = WorkOrder(
        work_order_id=f"WO-{next(_wo_ids)}",
        machine_id=machine_id.upper(),
        fault_code=fault_code.upper(),
        diagnosis=diagnosis,
        part_needed=part_needed,
        part_in_stock=part_in_stock,
        assigned_technician=assigned_technician,
        scheduled_time=scheduled_time,
        repair_procedure=repair_procedure,
    )
    db.save_work_order(wo.work_order_id, wo.model_dump_json())
    return wo.model_dump_json(indent=2)


ALL_TOOLS = [
    look_up_fault,
    get_fault_history,
    search_manual,
    check_inventory,
    draft_purchase_order,
    find_technician,
    create_work_order,
]
