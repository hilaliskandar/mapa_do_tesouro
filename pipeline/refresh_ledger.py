"""Persistent SQLite ledger for source refresh actions; no external dispatch."""
import argparse
import datetime as dt
import json
import sqlite3
from pathlib import Path

SCHEMA="""
CREATE TABLE IF NOT EXISTS operations(
    operation_key TEXT PRIMARY KEY,
    source TEXT NOT NULL,
    scheduled_date TEXT NOT NULL,
    action TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'planned',
    attempts INTEGER NOT NULL DEFAULT 0,
    next_retry_at TEXT,
    lease_until TEXT,
    worker TEXT,
    updated_at TEXT NOT NULL,
    evidence_key TEXT,
    source_version TEXT,
    error TEXT,
    UNIQUE(source,scheduled_date,action)
);
CREATE TABLE IF NOT EXISTS events(
    event_id INTEGER PRIMARY KEY,
    operation_key TEXT NOT NULL REFERENCES operations(operation_key),
    occurred_at TEXT NOT NULL,
    state TEXT NOT NULL,
    details TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_due ON operations(status,next_retry_at,scheduled_date);
CREATE INDEX IF NOT EXISTS idx_source ON operations(source,status,lease_until);
"""
def connect(path):
    db=sqlite3.connect(path,timeout=30,isolation_level=None)
    db.row_factory=sqlite3.Row
    db.execute("PRAGMA foreign_keys=ON")
    db.executescript(SCHEMA)
    return db

def stamp(now):
    if now.tzinfo is None:raise ValueError("timezone required")
    return now.astimezone(dt.timezone.utc).isoformat(timespec="seconds")

def event(db,key,now,state,details=None):
    db.execute("INSERT INTO events(operation_key,occurred_at,state,details) VALUES(?,?,?,?)",(key,stamp(now),state,json.dumps(details or {},sort_keys=True)))

def seed(db,tasks,now):
    added=0
    db.execute("BEGIN IMMEDIATE")
    try:
        for task in tasks:
            day=dt.date.fromisoformat(task["date"]).isoformat()
            for action in task["actions"]:
                key=f"{day}:{task['source']}:{action}"
                cur=db.execute("INSERT OR IGNORE INTO operations(operation_key,source,scheduled_date,action,updated_at) VALUES(?,?,?,?,?)",(key,task["source"],day,action,stamp(now)))
                if cur.rowcount:
                    event(db,key,now,"planned");added+=1
        db.commit()
    except BaseException:db.rollback();raise
    return added

def claim(db,key,worker,now,local_date,lease_minutes=60):
    if not worker or lease_minutes<=0:raise ValueError("invalid lease")
    at=stamp(now)
    db.execute("BEGIN IMMEDIATE")
    try:
        row=db.execute("SELECT * FROM operations WHERE operation_key=?",(key,)).fetchone()
        if not row or row["scheduled_date"]>local_date.isoformat() or row["status"] not in ("planned","retry","running"):
            db.rollback();return False
        if row["status"]=="retry" and row["next_retry_at"]>at:
            db.rollback();return False
        if row["status"]=="running" and row["lease_until"]>at:
            db.rollback();return False
        busy=db.execute("SELECT 1 FROM operations WHERE source=? AND operation_key<>? AND status='running' AND lease_until>?",(row["source"],key,at)).fetchone()
        if busy:
            db.rollback();return False
        db.execute("UPDATE operations SET status='running',worker=?,lease_until=?,attempts=attempts+1,updated_at=?,next_retry_at=NULL WHERE operation_key=?",(worker,stamp(now+dt.timedelta(minutes=lease_minutes)),at,key))
        event(db,key,now,"running",{"worker":worker});db.commit();return True
    except BaseException:db.rollback();raise

def finish(db,key,worker,now,status,evidence_key=None,source_version=None,error=None,max_attempts=3):
    if status not in ("unchanged","persisted","quarantined","failed"):raise ValueError("invalid terminal status")
    if status in ("unchanged","persisted") and not evidence_key:raise ValueError("evidence required")
    at=stamp(now)
    db.execute("BEGIN IMMEDIATE")
    try:
        row=db.execute("SELECT * FROM operations WHERE operation_key=?",(key,)).fetchone()
        if not row or row["status"]!="running" or row["worker"]!=worker or row["lease_until"]<=at:raise ValueError("not current lease owner")
        retry_at=None
        if status=="failed" and row["attempts"]<max_attempts:
            status="retry";retry_at=stamp(now+dt.timedelta(hours=2**row["attempts"]))
        db.execute("UPDATE operations SET status=?,next_retry_at=?,lease_until=NULL,worker=NULL,updated_at=?,evidence_key=?,source_version=?,error=? WHERE operation_key=?",(status,retry_at,at,evidence_key,source_version,error,key))
        event(db,key,now,status,{"evidence_key":evidence_key,"error":error});db.commit()
        return status
    except BaseException:db.rollback();raise

def summary(db):
    return {"operations":db.execute("SELECT count(*) FROM operations").fetchone()[0],"states":{r[0]:r[1] for r in db.execute("SELECT status,count(*) FROM operations GROUP BY status")},"events":db.execute("SELECT count(*) FROM events").fetchone()[0],"dispatch_count":0}

def main():
    p=argparse.ArgumentParser();p.add_argument("--plan",type=Path,required=True);p.add_argument("--ledger",type=Path,required=True);p.add_argument("--summary",type=Path,required=True);a=p.parse_args()
    payload=json.loads(a.plan.read_text())
    if payload["mode"]!="dry_run" or any(t["dispatch"] for t in payload["tasks"]):raise ValueError("only dry-run plans accepted")
    a.ledger.parent.mkdir(parents=True,exist_ok=True);db=connect(a.ledger)
    added=seed(db,payload["tasks"],dt.datetime.now(dt.timezone.utc))
    result={**summary(db),"new_operations":added,"mode":"dry_run"}
    a.summary.parent.mkdir(parents=True,exist_ok=True);a.summary.write_text(json.dumps(result,indent=2)+"\n")
    print("REFRESH_LEDGER_SUMMARY",json.dumps(result));db.close()
if __name__=="__main__":main()
