"""Pydantic schemas — the *shape* of the data our tools produce.

Pydantic validates that data has the right fields and types. If our code (or the
model) tries to build a WorkOrder with a missing field or a wrong type, Pydantic
raises immediately instead of letting bad data flow downstream. That's your
"validate AI output against a schema" rule, enforced in code.
"""
from typing import List, Optional

from pydantic import BaseModel, Field


class PurchaseOrder(BaseModel):
    part_number: str
    part_name: str
    quantity: int
    unit_cost: float
    total_cost: float
    supplier: str
    # A PO is NEVER auto-submitted. It stays a draft until a human approves it.
    status: str = "DRAFT - awaiting human approval"


class WorkOrder(BaseModel):
    work_order_id: str
    machine_id: str
    fault_code: str
    diagnosis: str
    part_needed: Optional[str] = None
    part_in_stock: bool = False
    assigned_technician: Optional[str] = None
    scheduled_time: Optional[str] = None
    repair_procedure: List[str] = Field(default_factory=list)
    status: str = "OPEN"
