"""Refresh partial TCESP snapshots, preserving original ZIPs and independent stages."""
import collections,csv,datetime,decimal,hashlib,io,json,os,pathlib,tarfile,time,urllib.request,zipfile
from deployment.download_r2_source import download_r2_object
root=pathlib.Path("build/tcesp-refresh");root.mkdir(parents=True,exist_ok=True)
def sha(b):return hashlib.sha256(b).hexdigest()
def get(key,path):
    download_r2_object(account_id=os.environ["CLOUDFLARE_ACCOUNT_ID"],api_token=os.environ["CLOUDFLARE_API_TOKEN"],bucket=os.environ["CLOUDFLARE_R2_BUCKET"],object_key=key,output=path)
prefix="tcesp/rmrp/2026/run_40229219185"
get(prefix+"/manifest.json",root/"previous_manifest.json")
manifest=json.loads((root/"previous_manifest.json").read_text())
get(prefix+"/extratos.tar.gz",root/"previous.tar.gz")
assert sha((root/"previous.tar.gz").read_bytes())==manifest["archive_sha256"]=="848d6ec74fb81f101d2600baaa5ee9bf7b28633906f073cb4c6e82aa1102ace2"
priority={"3505609","3518602","3533601","3534302","3539509","3544905","3553203","3553658"}
entries=sorted(manifest["documentos"],key=lambda e:(e["codigo_ibge"] not in priority,e["codigo_ibge"],e["dominio"]))
assert len(entries)==68 and len({(e["codigo_ibge"],e["dominio"]) for e in entries})==68
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
    if source_hash==e["source_sha256"]:
        return {"status":"unchanged","source_sha256":source_hash,"months":old["meses_observados"],"previous_months":old["meses_observados"]}
    dest=root/"raw"/code/(domain+".zip");dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
    months=set();by=collections.defaultdict(int);counts=collections.Counter();bad=collections.Counter();codes=set();n=0
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        names=[x for x in z.namelist() if x.lower().endswith(".csv")];assert len(names)==1
        with z.open(names[0]) as f:
            reader=csv.DictReader(io.TextIOWrapper(f,encoding="latin-1",newline=""),delimiter=";")
            required={"mes_referencia","ds_orgao"}|({"ds_elemento","tp_despesa","vl_despesa","cd_programa","cd_acao"} if domain=="despesas" else {"ds_tipo","vl_arrecadacao"})
            assert required<=set(reader.fieldnames or [])
            fields=reader.fieldnames
            for r in reader:
                n+=1
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
    if not months:bad["empty_months"]+=1
    if not set(old["meses_observados"])<=months:bad["coverage_regression"]+=1
    output={"codigo_ibge":code,"dominio":domain,"ano":2026,"source_url":url,"source_sha256":source_hash,"captured_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"months":sorted(months),"previous_months":old["meses_observados"],"source_rows":n,"fields":fields,"identity_codes":sorted(codes),"identity_status":"ibge_verified" if codes=={code} else "slug_from_verified_prior_manifest" if not codes else "mismatch","errors":dict(bad),"counts":[{"month":k[0],"type":k[1],"rows":v} for k,v in sorted(counts.items())],"aggregates":[{"keys":list(k),"cents":v} for k,v in sorted(by.items())],"publication_authorized":False}
    out=root/"derived"/code/(domain+".json");out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(output,ensure_ascii=False))
    return {"status":"quarantined" if bad else "updated","source_sha256":source_hash,"months":sorted(months),"previous_months":old["meses_observados"],"errors":dict(bad),"file":str(out.relative_to(root)),"raw_file":str(dest.relative_to(root)),"derived_sha256":sha(out.read_bytes())}
results=[]
with tarfile.open(root/"previous.tar.gz") as tf:
    for e in entries:
        raw=tf.extractfile(e["path"]).read();assert sha(raw)==e["json_sha256"]
        old=json.loads(raw)
        try:r=collect(e,old)
        except Exception as exc:r={"status":"unavailable","error":f"{type(exc).__name__}: {str(exc)[:250]}"}
        results.append({"codigo_ibge":e["codigo_ibge"],"domain":e["dominio"],"previous_sha256":e["source_sha256"],**r})
        time.sleep(0.5)
        print("TCESP_REFRESH_PAIR",json.dumps(results[-1],ensure_ascii=False),flush=True)
        (root/"coverage.json").write_text(json.dumps({"results":results,"publication_authorized":False},ensure_ascii=False,indent=2))
summary={"expected":68,"examined":len(results),"status_counts":dict(collections.Counter(r["status"] for r in results)),"advanced_months":sum(max(r.get("months") or [0])>max(r.get("previous_months") or [0]) for r in results if r["status"]=="updated"),"publication_authorized":False}
(root/"coverage.json").write_text(json.dumps({"summary":summary,"results":results},ensure_ascii=False,indent=2))
print("TCESP_REFRESH_SUMMARY",json.dumps(summary),flush=True)
