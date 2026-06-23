"""Synthetic-but-realistic plant data, held in memory.

In a real system this lives in a database (loaded into SQLite by src/db.py). For the
agent core, in-memory dicts keep everything runnable with zero setup.
"""

MACHINES = {
    "CNC-7": {"name": "Haas VF-2 CNC Mill", "line": "Machining Cell A"},
    "PUMP-3": {"name": "Grundfos Hydraulic Power Unit", "line": "Press Line 1"},
    "CONV-2": {"name": "Dorner 2200 Conveyor", "line": "Packaging"},
}

# Fault code -> what it means, the usual cause, the part it needs, and the skill.
FAULT_CODES = {
    "E-214": {
        "description": "Spindle bearing over-temperature",
        "likely_cause": "Worn spindle bearing or insufficient lubrication",
        "recommended_part": "BRG-6207",
        "skill_needed": "spindle",
    },
    "E-091": {
        "description": "Hydraulic pressure below threshold",
        "likely_cause": "Failing pump seal or internal leak",
        "recommended_part": "SEAL-HP12",
        "skill_needed": "hydraulics",
    },
    "E-330": {
        "description": "Conveyor drive motor overload trip",
        "likely_cause": "Jammed belt or degraded drive motor",
        "recommended_part": "MTR-CV3",
        "skill_needed": "electrical",
    },
}

# Parts on the shelf. qty 0 == out of stock -> the agent must draft a PO.
INVENTORY = {
    "BRG-6207": {"name": "Spindle Bearing 6207", "qty": 0, "supplier": "SKF Industrial", "unit_cost": 48.50},
    "SEAL-HP12": {"name": "Hydraulic Seal HP-12", "qty": 5, "supplier": "Parker Hannifin", "unit_cost": 12.75},
    "MTR-CV3": {"name": "Conveyor Drive Motor 3kW", "qty": 1, "supplier": "Baldor", "unit_cost": 640.00},
}

# Past faults and how they were resolved — the agent can learn from history.
FAULT_HISTORY = [
    {"machine_id": "CNC-7", "fault_code": "E-214", "date": "2026-03-12",
     "resolution": "Replaced spindle bearing BRG-6207, re-lubricated. 45 min downtime."},
    {"machine_id": "CNC-7", "fault_code": "E-214", "date": "2025-11-02",
     "resolution": "Bearing replacement. Recurring fault - review lubrication schedule."},
    {"machine_id": "CONV-2", "fault_code": "E-330", "date": "2026-01-20",
     "resolution": "Cleared belt jam; motor was fine. No part replaced."},
]

# Technicians, their skills, and the next time they're free.
TECHNICIANS = {
    "T-01": {"name": "Maria Gomez", "skills": ["mechanical", "spindle", "bearings"], "next_slot": "2026-06-19 14:00"},
    "T-02": {"name": "Dan Whitfield", "skills": ["hydraulics", "electrical"], "next_slot": "2026-06-19 16:30"},
}
