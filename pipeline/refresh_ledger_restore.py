"""Restore a verified ledger snapshot from a versioned manifest. QA only."""
import argparse
import hashlib
import json
import os
import re
import sqlite3
import tempfile
from pathlib import Path
from deployment.download_r2_source import download_r2_object

def validate_entry(entry, environment):
    if environment != "qa":
        raise ValueError("only QA restore enabled")
    sha=entry["sha256"]
    if not re.fullmatch(r"[0-9a-f]{64}",sha):
        raise ValueError("invalid hash")
    run=entry["run_id"]
    if type(run) is not int or run<=0:
        raise ValueError("invalid run")
    expected=f"sp_645/maintenance/ledger/{environment}/run_{run}/{sha}.sqlite"
    if entry["object_key"]!=expected:
        raise ValueError("invalid object namespace")
    for k in ("operations","events"):
        if type(entry[k]) is not int or entry[k]<0:
            raise ValueError("invalid count")

def verify(path, entry):
    with path.open("rb") as f:
        if hashlib.file_digest(f,"sha256").hexdigest()!=entry["sha256"]:
            raise ValueError("checksum mismatch")
    with sqlite3.connect(path.resolve().as_uri()+"?mode=ro",uri=True) as db:
        if db.execute("PRAGMA integrity_check").fetchall()!=[("ok",)]:
            raise ValueError("integrity failure")
        if db.execute("PRAGMA foreign_key_check").fetchall():
            raise ValueError("foreign key failure")
        for table in ("operations","events"):
            if db.execute(f"SELECT count(*) FROM {table}").fetchone()[0]!=entry[table]:
                raise ValueError("count mismatch")
        if db.execute("SELECT count(*) FROM operations WHERE status<>'planned'").fetchone()[0]:
            raise ValueError("unexpected non-simulated state")

def restore(manifest, output, fetch):
    if manifest["schema_version"]!=1 or manifest["environment"]!="qa" or manifest["publication_authorized"] is not False:
        raise ValueError("invalid QA manifest")
    if type(manifest["generation"]) is not int or manifest["generation"]<1:
        raise ValueError("invalid generation")
    candidates=[manifest]
    if manifest.get("predecessor"):
        p=manifest["predecessor"]
        if p["run_id"]>=manifest["run_id"] or p["operations"]>manifest["operations"] or p["events"]>manifest["events"]:
            raise ValueError("invalid predecessor")
        candidates.append(p)
    for entry in candidates:
        validate_entry(entry,"qa")
    if output.exists():
        raise FileExistsError(output)
    output.parent.mkdir(parents=True,exist_ok=True)
    failures=[]
    for i,entry in enumerate(candidates):
        with tempfile.TemporaryDirectory(dir=output.parent) as tmp:
            path=Path(tmp)/"candidate.sqlite"
            try:
                fetch(entry["object_key"],path)
                verify(path,entry)
            except Exception as exc:
                failures.append({"run_id":entry["run_id"],"error_type":type(exc).__name__})
                continue
            os.replace(path,output)
            return {"environment":"qa","selected_run":entry["run_id"],"sha256":entry["sha256"],"operations":entry["operations"],"events":entry["events"],"fallback":bool(i),"failures":failures,"dispatch_authorized":False,"promotion_authorized":False}
    raise RuntimeError(f"no valid snapshot: {failures}")

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--manifest",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--report",type=Path,required=True)
    a=p.parse_args()
    def fetch(key,path):
        download_r2_object(account_id=os.environ["CLOUDFLARE_ACCOUNT_ID"],api_token=os.environ["CLOUDFLARE_API_TOKEN"],bucket=os.environ["CLOUDFLARE_R2_BUCKET"],object_key=key,output=path)
    result=restore(json.loads(a.manifest.read_text()),a.output,fetch)
    a.report.parent.mkdir(parents=True,exist_ok=True)
    a.report.write_text(json.dumps(result,indent=2)+"\n")
    print("LEDGER_RESTORE_QA",json.dumps(result))
if __name__=="__main__":main()
