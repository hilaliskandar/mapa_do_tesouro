#!/usr/bin/env python3
"""Independent IBGE-2025 municipality x Seade RA/RG spatial crosswalk.

NO voting stations, TSE IDs or electoral zones are read. Read-only on source and
repository. Output is a *candidate* pending temporal/normative review.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,time,urllib.request,zipfile
from pathlib import Path
from collections import Counter,defaultdict
from datetime import datetime,timezone
import geopandas as gpd

IBGE="https://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/malhas_municipais/municipio_2025/UFs/SP/SP_Municipios_2025.zip"
EL_BASE="https://raw.githubusercontent.com/hilaliskandar/el2026/main/dados_referencia/regionalizacao_seade/fontes_originais/"
SOURCES={"ibge":(IBGE,None),"ra":(EL_BASE+"regiao_administrativa.zip","951dc1c9b8e608c076d3838dadbe5824742a023be3803fbdcc51ed905340929c"),
 "rg":(EL_BASE+"regiao_de_governo.zip","6610569fff8fe7cbef5bffc1c658b4af63839be9a2152b930213b8cd6baa1a22")}
EXPECTED=Path("governance/INV_SP645_CROSSWALK_RA_RG_RM_AU_EL2026_CANDIDATO_2026_11_14.csv")

def download(url,path,expected_sha):
    errors=[]
    for i in range(4):
        try:
            req=urllib.request.Request(url,headers={"User-Agent":"SP645-IBGE-Seade-geo-audit/1.0"})
            with urllib.request.urlopen(req,timeout=110) as response, path.open("wb") as f:
                h=hashlib.sha256()
                while True:
                    c=response.read(1024*1024)
                    if not c:break
                    f.write(c);h.update(c)
            sha=h.hexdigest()
            if expected_sha and sha!=expected_sha:raise RuntimeError("checksum mismatch")
            with zipfile.ZipFile(path) as z:
                member=z.testzip()
                if member:raise RuntimeError("CRC fail: "+member)
                if len([n for n in z.namelist() if n.lower().endswith(".shp")])!=1:
                    raise RuntimeError("expected one SHP per ZIP")
            return {"url":url,"file":str(path),"sha256":sha,"bytes":path.stat().st_size}
        except Exception as e:
            errors.append(str(e)[:160])
            if path.exists():path.unlink()
            if i<3:time.sleep(2+i*3)
    raise RuntimeError("download blocked "+url+": "+"; ".join(errors))

def check(g,kind):
    if g.crs is None:raise RuntimeError(kind+" lacks CRS")
    if g.geometry.isna().any() or g.geometry.is_empty.any() or not g.is_valid.all():
        raise RuntimeError(kind+" invalid or empty geometry")
    return g.to_crs("EPSG:4674")

def main():
    a=argparse.ArgumentParser();a.add_argument("--out-dir",required=True);args=a.parse_args()
    dest=Path(args.out_dir);dest.mkdir(parents=True,exist_ok=True)
    report={"status":"in_progress","time":datetime.now(timezone.utc).isoformat(),"sources":{},"scope":"municipal IBGE 2025 x official Seade administrative polygons 2021; NON electoral"}
    def save(): (dest/"manifest_regionalizacao_ibge_seade.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    save()
    try:
        g={}
        for kind,(url,sha) in SOURCES.items():
            p=dest/(kind+".zip")
            report["sources"][kind]=download(url,p,sha);save()
            g[kind]=check(gpd.read_file("zip://"+str(p)),kind)
            report["sources"][kind]["rows"]=len(g[kind]);report["sources"][kind]["columns"]=list(g[kind].columns)
            save()
        mun,ra,rg=g["ibge"],g["ra"],g["rg"]
        assert len(mun)==645 and len(ra)==16 and len(rg)==43,"unexpected feature counts"
        needed={"CD_MUN","NM_MUN"}
        if not needed.issubset(mun.columns):raise RuntimeError("IBGE column drift: "+str(list(mun.columns)))
        if not {"GID_RA","RA"}.issubset(ra.columns) or not {"GID_RG","RG"}.issubset(rg.columns):
            raise RuntimeError("Seade column drift")
        ibs=[str(v).strip() for v in mun["CD_MUN"]]
        if len(set(ibs))!=645 or any(len(v)!=7 or not v.startswith("35") for v in ibs):
            raise RuntimeError("IBGE ID uniqueness or format error")
        with EXPECTED.open(encoding="utf-8-sig",newline="") as f:
            expected={r["codigo_ibge"] for r in csv.DictReader(f,delimiter=";")}
        if expected!=set(ibs):raise RuntimeError("canonical IBGE municipality set mismatch")
        ra_list=[(str(r["GID_RA"]).strip(),str(r["RA"]).strip(),geom) for _,r in ra.iterrows() for geom in [r.geometry]]
        rg_list=[(str(r["GID_RG"]).strip(),str(r["RG"]).strip(),geom) for _,r in rg.iterrows() for geom in [r.geometry]]
        if len({r[0] for r in ra_list})!=16 or len({r[0] for r in rg_list})!=43:raise RuntimeError("duplicate Seade region IDs")
        records=[];issues=[];parent=defaultdict(set);regions=defaultdict(set)
        for _,r in mun.iterrows():
            ib=str(r["CD_MUN"]).strip()
            p=r.geometry.representative_point()
            hits={}
            for key,features in (("ra",ra_list),("rg",rg_list)):
                found=[(code,name,geometry) for code,name,geometry in features if geometry.covers(p)]
                if len(found)!=1:
                    issues.append({"ibge":ib,"problem":key+"_point_matches_"+str(len(found))})
                    continue
                hits[key]=found[0]
            if len(hits)!=2:continue
            code_ra,name_ra,_=hits["ra"];code_rg,name_rg,_=hits["rg"]
            parent[code_rg].add(code_ra)
            regions["ra_"+code_ra].add(ib);regions["rg_"+code_rg].add(ib)
            records.append({"codigo_ibge":ib,"municipio_ibge_2025":str(r["NM_MUN"]),
                "ra_codigo_seade_2021":code_ra,"ra_nome_seade_2021":name_ra,
                "rg_codigo_seade_2021":code_rg,"rg_nome_seade_2021":name_rg,
                "metodo":"ponto_representativo_interno_do_poligono_municipal_ibge_2025",
                "estado":"CANDIDATO_ESPACIAL_VERIFICAR_VIGENCIA"})
        if len(records)!=645 or len(parent)!=43 or any(len(v)!=1 for v in parent.values()):
            raise RuntimeError("incomplete municipal mapping or RG -> RA conflicts: "+str({"mapped":len(records),"issues":issues[:12],"rg_parents":{k:list(v) for k,v in parent.items() if len(v)!=1}}))
        # Examine shared-border/version effects before normative promotion.
        # Representative points serve only to select candidates, not to certify legal areas.
        records.sort(key=lambda r:r["codigo_ibge"])
        out=dest/"dim_sp645_ibge2025_seade2021_ra_rg_candidata.csv"
        with out.open("w",encoding="utf-8",newline="") as f:
            w=csv.DictWriter(f,fieldnames=list(records[0]),delimiter=";");w.writeheader();w.writerows(records)
        qa={"ibge645":645,"ra_count":len(ra_list),"rg_count":len(rg_list),
            "mapped":len(records),"missing":len(issues),"rg_cross_ra":sum(len(v)!=1 for v in parent.values()),
            "regional_ra_sum":sum(len(v) for k,v in regions.items() if k.startswith("ra_")),
            "regional_rg_sum":sum(len(v) for k,v in regions.items() if k.startswith("rg_")),
            "sha256_csv":hashlib.sha256(out.read_bytes()).hexdigest()}
        assert qa["regional_ra_sum"]==645 and qa["regional_rg_sum"]==645
        report["qa"]=qa;report["status"]="qa_pass_spatial_candidate_not_normative_homologation"
        report["warnings"]=["Polygons are Seade 2021, municipalities are IBGE 2025; different reference years",
            "Point-in-polygon does not prove official 2026 municipal regional membership",
            "No electoral-zones or voting locations used; no fiscal data involved",
            "No R2, Drive or canonical database write"]
        save()
        print(json.dumps({"status":report["status"],"qa":qa},ensure_ascii=False),flush=True)
    except Exception as e:
        report["status"]="blocked";report["error"]=repr(e);save();raise
if __name__=="__main__":main()
