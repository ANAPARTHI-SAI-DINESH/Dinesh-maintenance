from src.models import PurchaseOrder, WorkOrder


def test_purchase_order_is_draft_by_default():
    po = PurchaseOrder(part_number="X", part_name="x", quantity=1,
                       unit_cost=1.0, total_cost=1.0, supplier="s")
    assert "DRAFT" in po.status


def test_work_order_minimal():
    wo = WorkOrder(work_order_id="WO-1", machine_id="CNC-7",
                   fault_code="E-214", diagnosis="d", part_in_stock=True)
    assert wo.status == "OPEN"
    assert wo.repair_procedure == []
