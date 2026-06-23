"""SQLite persistence layer.

Moves the in-memory seed data into a real SQLite database file. Tools query this
instead of Python dicts. SQLite is built into Python — no server, just a file.
The DB path is configurable via the MAINTENANCE_DB env var (tests use a temp file).
"""
import json
import os
import sqlite3
from typing import Optional

from data.seed import FAULT_CODES, FAULT_HISTORY, INVENTORY, TECHNICIANS

_DEFAULT = os.path.join(os.path.dirname(os.path.dirname(__file__)), "maintenance.db")
DB_PATH = os.getenv("MAINTENANCE_DB", _DEFAULT)


def _conn() -> sqlite3.Connection:
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row  # rows behave like dicts
    return c


def init_db() -> None:
    """Create tables and seed them from data/seed.py. Safe to call repeatedly."""
    c = _conn()
    try:
        c.executescript(
            """
            CREATE TABLE IF NOT EXISTS faults
                (code TEXT PRIMARY KEY, description TEXT, likely_cause TEXT,
                 recommended_part TEXT, skill_needed TEXT);
            CREATE TABLE IF NOT EXISTS inventory
                (part_number TEXT PRIMARY KEY, name TEXT, qty INTEGER,
                 supplier TEXT, unit_cost REAL);
            CREATE TABLE IF NOT EXISTS history
                (id INTEGER PRIMARY KEY AUTOINCREMENT, machine_id TEXT,
                 fault_code TEXT, date TEXT, resolution TEXT);
            CREATE TABLE IF NOT EXISTS technicians
                (id TEXT PRIMARY KEY, name TEXT, skills TEXT, next_slot TEXT);
            CREATE TABLE IF NOT EXISTS work_orders
                (work_order_id TEXT PRIMARY KEY, payload TEXT);
            CREATE TABLE IF NOT EXISTS purchase_orders
                (id INTEGER PRIMARY KEY AUTOINCREMENT, payload TEXT, status TEXT);
            """
        )
        if not c.execute("SELECT 1 FROM faults LIMIT 1").fetchone():
            for code, f in FAULT_CODES.items():
                c.execute("INSERT INTO faults VALUES (?,?,?,?,?)",
                          (code, f["description"], f["likely_cause"],
                           f["recommended_part"], f["skill_needed"]))
            for pn, p in INVENTORY.items():
                c.execute("INSERT INTO inventory VALUES (?,?,?,?,?)",
                          (pn, p["name"], p["qty"], p["supplier"], p["unit_cost"]))
            for h in FAULT_HISTORY:
                c.execute("INSERT INTO history (machine_id,fault_code,date,resolution) "
                          "VALUES (?,?,?,?)",
                          (h["machine_id"], h["fault_code"], h["date"], h["resolution"]))
            for tid, t in TECHNICIANS.items():
                c.execute("INSERT INTO technicians VALUES (?,?,?,?)",
                          (tid, t["name"], json.dumps(t["skills"]), t["next_slot"]))
        c.commit()
    finally:
        c.close()


def get_fault(code: str) -> Optional[dict]:
    c = _conn()
    try:
        r = c.execute("SELECT * FROM faults WHERE code=?", (code.upper(),)).fetchone()
        return dict(r) if r else None
    finally:
        c.close()


def get_history(machine_id: str) -> list:
    c = _conn()
    try:
        rs = c.execute("SELECT machine_id,fault_code,date,resolution FROM history "
                       "WHERE machine_id=?", (machine_id.upper(),)).fetchall()
        return [dict(r) for r in rs]
    finally:
        c.close()


def get_part(part_number: str) -> Optional[dict]:
    c = _conn()
    try:
        r = c.execute("SELECT * FROM inventory WHERE part_number=?",
                      (part_number.upper(),)).fetchone()
        return dict(r) if r else None
    finally:
        c.close()


def find_technician_by_skill(skill: str) -> Optional[dict]:
    c = _conn()
    try:
        for r in c.execute("SELECT * FROM technicians").fetchall():
            skills = json.loads(r["skills"])
            if skill.lower() in [s.lower() for s in skills]:
                d = dict(r)
                d["skills"] = skills
                return d
        return None
    finally:
        c.close()


def save_work_order(work_order_id: str, payload: str) -> None:
    c = _conn()
    try:
        c.execute("INSERT OR REPLACE INTO work_orders VALUES (?,?)",
                  (work_order_id, payload))
        c.commit()
    finally:
        c.close()


def save_purchase_order(payload: str, status: str) -> int:
    c = _conn()
    try:
        cur = c.execute("INSERT INTO purchase_orders (payload,status) VALUES (?,?)",
                        (payload, status))
        c.commit()
        return cur.lastrowid
    finally:
        c.close()
