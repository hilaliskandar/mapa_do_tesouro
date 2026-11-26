import datetime as dt
import json
import unittest
from pathlib import Path
from pipeline.refresh_calendar import plan,summarize,validate

class CalendarTests(unittest.TestCase):
    def setUp(self):
        self.c=json.loads(Path("data/catalogs/source_refresh_calendar.json").read_text())
        self.tasks=plan(self.c,dt.date(2027,1,1),dt.date(2027,12,31))
        self.summary=summarize(self.tasks)
    def test_unique_and_safe(self):
        self.assertEqual(len(self.tasks),len({t["key"] for t in self.tasks}))
        self.assertTrue(all(not t["dispatch"] and not t["enabled"] for t in self.tasks))
        self.assertEqual(len(self.summary["by_source"]),18)
    def test_cadence(self):
        a=self.summary["by_source_action"]
        self.assertEqual(a["transferegov:metadata_probe"],365)
        for s in ("tcesp_receitas","tcesp_despesas"):
            self.assertEqual(a[s+":refresh"],12)
            self.assertEqual(a[s+":prior_year_probe"],4)
            dates=[dt.date.fromisoformat(t["date"]) for t in self.tasks if t["source"]==s and "refresh" in t["actions"]]
            self.assertTrue(all(d.weekday()==1 and 21<=d.day<=27 for d in dates))
        self.assertEqual(a["territorial_dimensions:probe"],4)
        self.assertEqual(a["finbra_dca:historical_probe"],4)
    def test_leap(self):
        x=plan(self.c,dt.date(2028,2,28),dt.date(2028,3,1))
        self.assertEqual(sum(t["source"]=="transferegov" for t in x),3)
    def test_invalid(self):
        self.c["sources"][0]["schedule"][0]["weekday"]=8
        with self.assertRaises(ValueError):validate(self.c)
    def test_reverse(self):
        with self.assertRaises(ValueError):plan(self.c,dt.date(2027,2,1),dt.date(2027,1,1))
if __name__=="__main__":unittest.main()
