"""Initial TCESP 2026 missing-only acquisition, candidate slug verified against source."""
import argparse,collections,csv,datetime,decimal,hashlib,io,json,pathlib,time,urllib.request,zipfile,unicodedata,re
p=argparse.ArgumentParser();p.add_argument("--offset",type=int,required=True);p.add_argument("--limit",type=int,default=10);p.add_argument("--output",type=pathlib.Path,required=True);a=p.parse_args()
root=a.output;root.mkdir(parents=True,exist_ok=True)
def sha(b):return hashlib.sha256(b).hexdigest()
def normalize(s):return re.sub(r"[^a-z0-9]+"," ",unicodedata.normalize("NFKD",s.casefold()).encode("ascii","ignore").decode()).strip()
def cents(v):
    if not v or not v.strip():raise ValueError("missing monetary value")
    d=decimal.Decimal(v.strip().replace(".","").replace(",","."))
    assert d.is_finite() and d*100==(d*100).to_integral_value()
    return int(d*100)
def collect(e,old):
    url=old["fonte"];code=e["codigo_ibge"];domain=e["dominio"]
    assert url==f"https://transparencia.tce.sp.gov.br/sites/default/files/csv/{domain}-{e['slug']}-2026.zip"
    err=None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0","Accept":"application/zip"}),timeout=120) as r: data=r.read(200_000_001)
            assert len(data)<=200_000_000
            break
        except Exception as exc:err=exc;time.sleep(2**attempt)
    else:raise err
    source_hash=sha(data)
    if e.get("source_sha256") and source_hash==e["source_sha256"]:
        return {"status":"unchanged","source_sha256":source_hash,"months":old["meses_observados"],"previous_months":old["meses_observados"]}
    dest=root/"raw"/code/(domain+".zip");dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
    months=set();by=collections.defaultdict(int);counts=collections.Counter();bad=collections.Counter();codes=set();names_seen=set();years=set();n=0
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        names=[x for x in z.namelist() if x.lower().endswith(".csv")];assert len(names)==1
        with z.open(names[0]) as f:
            reader=csv.DictReader(io.TextIOWrapper(f,encoding="latin-1",newline=""),delimiter=";")
            required={"mes_referencia","ds_orgao"}|({"ds_elemento","tp_despesa","vl_despesa","cd_programa","cd_acao"} if domain=="despesas" else {"ds_tipo","vl_arrecadacao"})
            assert required<=set(reader.fieldnames or [])
            fields=reader.fieldnames
            for r in reader:
                n+=1
                if r.get("ds_municipio"):names_seen.add(normalize(r["ds_municipio"]))
                if r.get("ano_exercicio"):years.add(r["ano_exercicio"].strip())
                if r.get("codigo_municipio_ibge"):codes.add(r["codigo_municipio_ibge"].strip())
                m=(r.get("mes_referencia") or "").strip()
                if not m.isdigit() or not 1<=int(m)<=12:bad["invalid_month"]+=1;continue
                m=int(m);months.add(m)
                if domain=="despesas":
                    if not (r.get("ds_elemento") or "").split(" - ",1)[0].strip().startswith("44"):continue
                    key=(m,)+tuple((r.get(k) or "").strip() for k in ("tp_despesa","ds_orgao","ds_funcao_governo","ds_subfuncao_governo","cd_programa","ds_programa","cd_acao","ds_acao","ds_elemento","ds_fonte_recurso"))
                    v=r.get("vl_despesa")
                else:
                    nature=(r.get("ds_tipo") or "").split(" - ",1)[0].strip()
                    tax=next((t for p,t in (("111250","IPTU"),("111253","ITBI"),("111451","ISS")) if nature.startswith(p)),None)
                    if not tax:continue
                    key=(m,tax,nature,(r.get("ds_orgao") or "").strip());v=r.get("vl_arrecadacao")
                try:by[key]+=cents(v);counts[(m,key[1])]+=1
                except (ValueError,decimal.InvalidOperation,AssertionError):bad["invalid_value"]+=1
    if codes and codes!={code}:bad["municipality_mismatch"]+=1
    if not codes and names_seen!={normalize(e["municipio"])}:bad["municipality_name_mismatch"]+=1
    if years!={"2026"}:bad["year_mismatch"]+=1
    if not months:bad["empty_months"]+=1
    if not set(old["meses_observados"])<=months:bad["coverage_regression"]+=1
    output={"codigo_ibge":code,"dominio":domain,"ano":2026,"source_url":url,"source_sha256":source_hash,"captured_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"months":sorted(months),"previous_months":old["meses_observados"],"source_rows":n,"fields":fields,"identity_codes":sorted(codes),"identity_status":"ibge_verified" if codes=={code} else "source_name_verified" if not codes and names_seen=={normalize(e["municipio"])} else "mismatch","errors":dict(bad),"counts":[{"month":k[0],"type":k[1],"rows":v} for k,v in sorted(counts.items())],"aggregates":[{"keys":list(k),"cents":v} for k,v in sorted(by.items())],"publication_authorized":False}
    out=root/"derived"/code/(domain+".json");out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(output,ensure_ascii=False))
    return {"status":"quarantined" if bad else "updated","source_sha256":source_hash,"months":sorted(months),"previous_months":old["meses_observados"],"errors":dict(bad),"file":str(out.relative_to(root)),"raw_file":str(dest.relative_to(root)),"derived_sha256":sha(out.read_bytes())}

with open("governance/DIM_SP645_IBGE_RA_RG_RM_AU_CONSOLIDADA_2026_11_14.csv",encoding="utf-8-sig") as f:roster=list(csv.DictReader(f,delimiter=";"))
assert len(roster)==645
pending=[r for r in roster if r["rm_au_nome"]!="Região Metropolitana de Ribeirão Preto" and r["codigo_ibge"] not in {"3550308","3548906"}]
assert len(pending)==609
pending.sort(key=lambda r:r["codigo_ibge"])
selected=pending[a.offset:a.offset+a.limit]
results=[]
for city in selected:
    code=city["codigo_ibge"];slug=normalize(city["municipio"]).replace(" ","-")
    for domain in ("despesas","receitas"):
        e={"codigo_ibge":code,"municipio":city["municipio"],"slug":slug,"dominio":domain}
        old={"fonte":f"https://transparencia.tce.sp.gov.br/sites/default/files/csv/{domain}-{slug}-2026.zip","meses_observados":[]}
        try:r=collect(e,old)
        except Exception as exc:r={"status":"unavailable","error":f"{type(exc).__name__}: {str(exc)[:200]}"}
        results.append({**e,**r});time.sleep(0.5)
summary={"offset":a.offset,"municipalities":len(selected),"expected":2*len(selected),"status_counts":dict(collections.Counter(r["status"] for r in results)),"publication_authorized":False}
(root/"coverage.json").write_text(json.dumps({"summary":summary,"results":results},ensure_ascii=False,indent=2))
print("TCESP_STATE_PILOT",json.dumps(summary))
