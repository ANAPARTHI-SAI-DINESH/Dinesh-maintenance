from src import approval

_PO = {"part_name": "Spindle Bearing", "part_number": "BRG-6207", "quantity": 2,
       "unit_cost": 48.5, "total_cost": 97.0, "supplier": "SKF"}


def test_approval_yes():
    assert approval.request_approval(_PO, input_fn=lambda _: "y") is True


def test_approval_no():
    assert approval.request_approval(_PO, input_fn=lambda _: "n") is False
