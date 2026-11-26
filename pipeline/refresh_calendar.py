"""Deterministic source-refresh planning; no network or dispatch."""
import argparse
import collections
import datetime as dt
import json
from pathlib import Path
from zoneinfo import ZoneInfo

CADENCES={"daily","weekly","monthly","monthly_after20","quarterly"}
def validate(catalog):
    ids=set()
    ZoneInfo(catalog["timezone"])
    for source in catalog["sources"]:
        sid=source["id"]
        if sid in ids:raise ValueError(f"duplicate source {sid}")
        ids.add(sid)
        seen=set()
        if not source["schedule"]:raise ValueError(f"empty schedule {sid}")
        for r in source["schedule"]:
            cadence=r["cadence"]; weekday=r["weekday"]; months=r["months"]
            if cadence not in CADENCES:raise ValueError(cadence)
            if cadence=="daily":
                if weekday is not None:raise ValueError("daily weekday must be null")
            elif type(weekday) is not int or not 0<=weekday<=6:raise ValueError("invalid weekday")
            if months is not None and (not months or len(set(months))!=len(months) or any(type(m) is not int or not 1<=m<=12 for m in months)):raise ValueError("invalid months")
            key=(cadence,weekday,tuple(months or []),r["action"])
            if key in seen:raise ValueError("duplicate rule")
            seen.add(key)
    return catalog

def matches(day,rule):
    months=rule["months"];cadence=rule["cadence"]
    if months and day.month not in months:return False
    if cadence=="daily":return True
    if day.weekday()!=rule["weekday"]:return False
    if cadence=="weekly":return True
    if cadence=="monthly":return day.day<=7
    if cadence=="quarterly":return day.month in (1,4,7,10) and day.day<=7
    if cadence=="monthly_after20":return 21<=day.day<=27
    raise ValueError(cadence)

def plan(catalog,start,end):
    if end<start:raise ValueError("end before start")
    validate(catalog)
    tasks=[]
    for i in range((end-start).days+1):
        day=start+dt.timedelta(days=i)
        for s in catalog["sources"]:
            actions=sorted({r["action"] for r in s["schedule"] if matches(day,r)})
            if not actions:continue
            tasks.append({"date":day.isoformat(),"source":s["id"],"actions":actions,"key":f"{day.isoformat()}:{s['id']}","enabled":s["enabled"],"dispatch":False})
    return tasks

def summarize(tasks):
    source=collections.Counter(t["source"] for t in tasks)
    actions=collections.Counter(f"{t['source']}:{a}" for t in tasks for a in t["actions"])
    days=collections.Counter(t["date"] for t in tasks)
    return {"source_days":len(tasks),"distinct_days":len(days),"action_count":sum(actions.values()),"by_source":dict(sorted(source.items())),"by_source_action":dict(sorted(actions.items())),"multiple_actions_same_source_day":sum(len(t["actions"])>1 for t in tasks),"max_sources_per_day":max(days.values(),default=0),"dispatch_count":0}

def main():
    p=argparse.ArgumentParser();p.add_argument("--catalog",type=Path,default=Path("data/catalogs/source_refresh_calendar.json"));p.add_argument("--start");p.add_argument("--end");p.add_argument("--output",type=Path,required=True);a=p.parse_args()
    c=validate(json.loads(a.catalog.read_text(encoding="utf-8")))
    today=dt.datetime.now(ZoneInfo(c["timezone"])).date()
    start=dt.date.fromisoformat(a.start) if a.start else today
    end=dt.date.fromisoformat(a.end) if a.end else start
    tasks=plan(c,start,end);summary=summarize(tasks)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps({"mode":"dry_run","catalog_version":c["version"],"start":start.isoformat(),"end":end.isoformat(),"summary":summary,"tasks":tasks},indent=2)+"\n")
    print("REFRESH_CALENDAR_SUMMARY",json.dumps(summary))
if __name__=="__main__":main()
