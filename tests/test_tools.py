import json

from src.tools import (
    check_inventory,
    create_work_order,
    draft_purchase_order,
    look_up_fault,
)


def test_look_up_fault():
    out = json.loads(look_up_fault.invoke({"fault_code": "E-214"}))
    assert "spindle" in out["description"].lower()


def test_check_inventory_out_of_stock():
    out = json.loads(check_inventory.invoke({"part_number": "BRG-6207"}))
    assert out["in_stock"] is False


def test_draft_purchase_order_math():
    po = json.loads(draft_purchase_order.invoke({"part_number": "BRG-6207", "quantity": 2}))
    assert po["total_cost"] == 97.0  # 48.50 * 2
    assert "DRAFT" in po["status"]


def test_create_work_order():
    out = json.loads(create_work_order.invoke({
        "machine_id": "CNC-7", "fault_code": "E-214", "diagnosis": "bearing worn",
        "part_needed": "BRG-6207", "part_in_stock": False,
        "assigned_technician": "Maria Gomez", "scheduled_time": "2026-06-19 14:00",
        "repair_procedure": ["lockout", "replace bearing"],
    }))
    assert out["work_order_id"].startswith("WO-")
    assert out["assigned_technician"] == "Maria Gomez"
