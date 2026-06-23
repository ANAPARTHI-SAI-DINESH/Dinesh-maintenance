from src import db


def test_seed_and_query():
    fault = db.get_fault("E-214")
    assert fault and fault["recommended_part"] == "BRG-6207"

    part = db.get_part("BRG-6207")
    assert part["qty"] == 0  # deliberately out of stock -> triggers a PO

    tech = db.find_technician_by_skill("spindle")
    assert tech and tech["id"] == "T-01"

    history = db.get_history("CNC-7")
    assert len(history) >= 1
