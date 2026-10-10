#!/usr/bin/env python3
"""Analise piloto do CSV TCESP. Nao assume que registros de empenho sejam liquidacoes."""
from urllib.request import Request,urlopen
from io import BytesIO,TextIOWrapper
from collections import Counter,defaultdict
import csv,json,re,zipfile,os,hashlib
import sys
slug=sys.argv[1] if len(sys.argv)>1 else "jundiai"
year=int(sys.argv[2]) if len(sys.argv)>2 else 2025
url=f"https://transparencia.tce.sp.gov.br/sites/default/files/csv/despesas-{slug}-{year}.zip"
req=Request(url,headers={"User-Agent":"Mozilla/5.0"})
timeout=int(os.environ.get('TCESP_TIMEOUT_SECONDS', '120'))
with urlopen(req,timeout=timeout) as response: data=response.read()
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
def ranked(mapping):
    return [list(k) + [round(cents/100, 2), cents]
            for k, cents in sorted(mapping.items(), key=lambda item: -item[1])]

all_program = ranked(by_program)
all_action = ranked(by_action)
total_cents = sum(by_program.values())
assert total_cents == sum(by_action.values()), "Totais de programas e acoes nao coincidem"
print(json.dumps({
    "slug":slug,"year":year,"url":url,"file":file,
    "sha256_zip":hashlib.sha256(data).hexdigest(),
    "rows":n,"columns":fields,"types":types,
    "organs":organs.most_common(12),"element_groups":elements,
    "months":months,"bad_values":bad,
    "totals_44_by_type":{k[0]:round(v/100,2) for k,v in totals.items() if k[1]=="44"},
    "investimento_44_liquidado_centavos":total_cents,
    "programas_44_liquidado_completos":all_program,
    "acoes_44_liquidado_completas":all_action,
    "top_program_44_liquidado":[item[:-1] for item in all_program[:12]],
    "top_action_44_liquidado":[item[:-1] for item in all_action[:12]]
},ensure_ascii=False,indent=2))
