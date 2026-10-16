"""Testes deterministas sem rede da integracao do RGF monetario no SQLite."""
import csv,hashlib,sqlite3
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from pipeline.build.integrate_rgf_gate_e import FIELDS, integrate

class GateERGFIntegrationTest(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root=Path(self.tmp.name)
        self.database=root/"sample.sqlite"
        self.reference=root/"rgf.csv"
        self.report=root/"qa.json"
        con=sqlite3.connect(self.database)
        con.execute("CREATE TABLE observacao (codigo_ibge TEXT,ano INTEGER,variavel_id TEXT,status TEXT,valor_num REAL,valor_texto TEXT,fonte_id TEXT,referencia_origem TEXT,PRIMARY KEY(codigo_ibge,ano,variavel_id))")
        for i in range(645):
            code=str(3500000+i)
            for year in (2023,2024):
                for name in FIELDS:
                    con.execute("INSERT INTO observacao(codigo_ibge,ano,variavel_id,status) VALUES (?,?,?,'nao_aplicavel')",(code,year,name))
        con.commit();con.close()
        with self.reference.open("w",encoding="utf-8",newline="") as h:
            writer=csv.DictWriter(h,fieldnames=["cod_ibge","ano",*FIELDS])
            writer.writeheader()
            for i in range(645):
                for year in (2023,2024):
                    writer.writerow({"cod_ibge":str(3500000+i),"ano":year,**{name:float(i+1) for name in FIELDS}})
        self.pin=hashlib.sha256(self.reference.read_bytes()).hexdigest()

    def test_integrate_only_verified_status(self):
        with patch("pipeline.build.integrate_rgf_gate_e.PIN",self.pin):
            result=integrate(self.database,self.reference,self.report)
        self.assertEqual(result["reference_rows"],1290)
        self.assertEqual(result["changed"],3870)
        with sqlite3.connect(self.database) as con:
            self.assertEqual(con.execute("SELECT COUNT(*) FROM observacao WHERE status='observado'").fetchone()[0],3870)

    def test_reject_hash_mismatch_without_writes(self):
        with self.assertRaisesRegex(ValueError,"SHA Gate E"):
            integrate(self.database,self.reference,self.report)
        with sqlite3.connect(self.database) as con:
            self.assertEqual(con.execute("SELECT COUNT(*) FROM observacao WHERE status='observado'").fetchone()[0],0)

    def test_reject_conflicting_observed_record(self):
        with sqlite3.connect(self.database) as con:
            con.execute("UPDATE observacao SET status='observado',valor_num=999 WHERE codigo_ibge='3500000' AND ano=2023 AND variavel_id='rgf_despesa_total_pessoal'")
        with patch("pipeline.build.integrate_rgf_gate_e.PIN",self.pin):
            with self.assertRaisesRegex(ValueError,"Conflito"):
                integrate(self.database,self.reference,self.report)
        with sqlite3.connect(self.database) as con:
            self.assertEqual(con.execute("SELECT COUNT(*) FROM observacao WHERE status='nao_aplicavel'").fetchone()[0],3869)

if __name__=="__main__":
    unittest.main()
