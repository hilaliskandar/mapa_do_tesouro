import datetime as dt
import tempfile
import unittest
from pathlib import Path
from pipeline.refresh_ledger import connect,seed,claim,finish,summary

class LedgerTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path=Path(self.tmp.name)/"ledger.sqlite"
        self.db=connect(self.path)
        self.addCleanup(self.db.close)
        self.now=dt.datetime(2027,1,4,12,tzinfo=dt.timezone.utc)
        self.day=self.now.date()
        self.tasks=[{"date":self.day.isoformat(),"source":"a","actions":["probe","refresh"]},{"date":self.day.isoformat(),"source":"b","actions":["probe"]},{"date":"2027-01-05","source":"c","actions":["probe"]}]
        self.key="2027-01-04:a:probe"
        self.other="2027-01-04:a:refresh"
        self.assertEqual(seed(self.db,self.tasks,self.now),4)
    def test_idempotence_reopen(self):
        db=connect(self.path)
        try:
            self.assertEqual(seed(db,self.tasks,self.now),0)
            self.assertEqual(summary(db)["events"],4)
        finally:db.close()
    def test_concurrency_and_future(self):
        db=connect(self.path)
        try:
            self.assertTrue(claim(self.db,self.key,"worker1",self.now,self.day))
            self.assertFalse(claim(db,self.key,"worker2",self.now,self.day))
            self.assertFalse(claim(db,self.other,"worker2",self.now,self.day))
            self.assertTrue(claim(db,"2027-01-04:b:probe","worker2",self.now,self.day))
            self.assertFalse(claim(db,"2027-01-05:c:probe","worker2",self.now,self.day))
        finally:db.close()
    def test_expired_lease(self):
        self.assertTrue(claim(self.db,self.key,"old",self.now,self.day,1))
        later=self.now+dt.timedelta(minutes=2)
        self.assertTrue(claim(self.db,self.key,"new",later,self.day))
        with self.assertRaises(ValueError):finish(self.db,self.key,"old",later,"persisted",evidence_key="test")
        self.assertEqual(finish(self.db,self.key,"new",later,"persisted",evidence_key="test",source_version="sha"),"persisted")
        self.assertFalse(claim(self.db,self.key,"third",later,self.day))
    def test_retry_exhaustion(self):
        now=self.now
        for expected,hours in [("retry",2),("retry",4),("failed",0)]:
            self.assertTrue(claim(self.db,self.key,"worker",now,self.day))
            self.assertEqual(finish(self.db,self.key,"worker",now, "failed",error="synthetic"),expected)
            self.assertFalse(claim(self.db,self.key,"worker",now,self.day))
            now+=dt.timedelta(hours=hours)
        self.assertEqual(summary(self.db)["states"]["failed"],1)
    def test_evidence_and_quarantine(self):
        self.assertTrue(claim(self.db,self.key,"worker",self.now,self.day))
        with self.assertRaises(ValueError):finish(self.db,self.key,"worker",self.now,"unchanged")
        self.assertEqual(finish(self.db,self.key,"worker",self.now,"quarantined",error="synthetic"),"quarantined")
        self.assertFalse(claim(self.db,self.key,"worker",self.now,self.day))
    def test_unchanged_releases_source(self):
        self.assertTrue(claim(self.db,self.key,"worker",self.now,self.day))
        self.assertEqual(finish(self.db,self.key,"worker",self.now,"unchanged",evidence_key="test"),"unchanged")
        self.assertTrue(claim(self.db,self.other,"worker",self.now,self.day))
if __name__=="__main__":unittest.main()
