#!/usr/bin/env python3
"""Analise piloto do CSV TCESP. Nao assume que registros de empenho sejam liquidacoes."""
from urllib.request import Request,urlopen
from io import BytesIO,TextIOWrapper
from collections import Counter,defaultdict
import csv,json,re,zipfile
import sys
slug=sys.argv[1] if len(sys.argv)>1 else "jundiai"
url=f"https://transparencia.tce.sp.gov.br/sites/default/files/csv/despesas-{slug}-2025.zip"
req=Request(url,headers={"User-Agent":"Mozilla/5.0"})
with urlopen(req,timeout=120) as response: data=response.read()
assert zipfile.is_zipfile(BytesIO(data))
with zipfile.ZipFile(BytesIO(data)) as z:
    file=z.namelist()[0]
    with z.open(file) as stream:
        reader=csv.DictReader(TextIOWrapper(stream,encoding="latin-1",newline=""),delimiter=";")
        fields=reader.fieldnames
        types=Counter();organs=Counter();elements=Counter();months=Counter()
        totals=defaultdict(int);by_program=defaultdict(int);by_action=defaultdict(int)
        n=0;bad=0
        for row in reader:
            n+=1
            tp=(row.get("tp_despesa") or "").strip()
            types[tp]+=1
            organs[(row.get("ds_orgao") or "").strip()]+=1
            element=(row.get("ds_elemento") or "").strip()
            code=element.split(" - ",1)[0]
            elements[code[:2]]+=1
            months[(row.get("mes_referencia") or "").strip()]+=1
            raw=(row.get("vl_despesa") or "0").replace(".","").replace(",",".")
            try: cents=round(float(raw)*100)
            except ValueError: bad+=1;continue
            totals[(tp,code[:2])]+=cents
            if code.startswith("44") and tp.strip().lower()=="valor liquidado":
                by_program[(row.get("cd_programa"),row.get("ds_programa"))]+=cents
                by_action[(row.get("cd_programa"),row.get("cd_acao"),row.get("ds_acao"))]+=cents
print(json.dumps({"slug":slug,"url":url,"file":file,"rows":n,"columns":fields,"types":types,"organs":organs.most_common(12),"element_groups":elements,"months":months,"bad_values":bad,"totals_44_by_type":{k[0]:round(v/100,2) for k,v in totals.items() if k[1]=="44"},"top_program_44_liquidado":[list(k)+[round(v/100,2)] for k,v in sorted(by_program.items(),key=lambda x:-x[1])[:12]],"top_action_44_liquidado":[list(k)+[round(v/100,2)] for k,v in sorted(by_action.items(),key=lambda x:-x[1])[:12]]},ensure_ascii=False,indent=2))
