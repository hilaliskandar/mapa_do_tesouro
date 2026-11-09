#!/usr/bin/env python3
"""G05-C: cartography using the unmodified IBGE 2022 SP municipal boundaries (SIRGAS 2000).
No geometry simplification, no area or distance computation, 37/37 code-based joins.
"""
from __future__ import annotations
import csv,hashlib,json,zipfile,os
from pathlib import Path
from decimal import Decimal
import shapefile
from shapely.geometry import shape, mapping
from pyproj import CRS
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as PatchPoly
from matplotlib.collections import PatchCollection
from matplotlib.colors import TwoSlopeNorm,Normalize
from matplotlib.cm import ScalarMappable

ROOT=Path("build/rmsjrp-g05c")
ROOT.mkdir(parents=True,exist_ok=True)
ZIP=ROOT/"SP_Municipios_2022.zip"
assert ZIP.is_file() and ZIP.stat().st_size>1000000
sha_zip=hashlib.sha256(ZIP.read_bytes()).hexdigest()
with zipfile.ZipFile(ZIP) as z:
    members=z.namelist()
    assert any(n.lower().endswith(".shp") for n in members)
    assert any(n.lower().endswith(".dbf") for n in members)
    assert any(n.lower().endswith(".shx") for n in members)
    assert any(n.lower().endswith(".prj") for n in members)
    z.extractall(ROOT/"raw")
folder=ROOT/"raw"
shp=next(folder.rglob("*.shp"))
prj=next(folder.rglob("*.prj"))
crs=CRS.from_wkt(prj.read_text(encoding="utf-8-sig"))
assert crs.to_epsg()==4674,crs.to_epsg()
reader=shapefile.Reader(str(shp),encoding="utf-8")
fields=[x[0] for x in reader.fields[1:]]
assert "CD_MUN" in fields,fields
features={}
for feat in reader.iterShapeRecords():
    properties=feat.record.as_dict()
    code=str(properties["CD_MUN"])
    if code in features:raise ValueError("duplicate geometry code "+code)
    geom=shape(feat.shape.__geo_interface__)
    if code in features:raise ValueError("duplicate "+code)
    features[code]=geom
assert len(features)==645,len(features)
codes={}
with Path("editorial/rmsjrp/MUNICIPIOS_SUBREGIOES_2025.csv").open(encoding="utf-8") as f:
    for r in csv.DictReader(f,delimiter=";"):codes[r["cod_ibge"]]=r
assert len(codes)==37
selected={k:features[k] for k in codes if k in features}
assert len(selected)==37,{"missing":sorted(set(codes)-set(selected))}
invalid=[k for k,g in selected.items() if g.is_empty or not g.is_valid]
assert not invalid,invalid
# Approved classification table from exact SHA-256 G05 source.
tab=Path("build/rmsjrp-g05c/G05_CONTRIBUICOES_MUNICIPAIS.csv")
assert hashlib.sha256(tab.read_bytes()).hexdigest()=="670ca3079eabb9a8d6218d104b8762ee8e8de7239ba6d1f0bc9273e80f87136c"
rows=[]
with tab.open(encoding="utf-8-sig",newline="") as f:
    rows=list(csv.DictReader(f,delimiter=";"))
change={r["cod_ibge"]:float(r["variacao_investimento_real_pct"]) for r in rows if r["inicio"]=="2024" and r["fim"]=="2025"}
assert set(change)==set(codes)
# Use 2025 real per-capita from G04 municipal R2 snapshot.
p=Path("build/rmsjrp-g05c/SERIES_MUNICIPAIS_2013_2025.csv")
assert hashlib.sha256(p.read_bytes()).hexdigest()=="1f0413304c54edbe57fe129a506d088da2cd296d767f901992c02f803fbd62e5"
per={}
with p.open(encoding="utf-8-sig",newline="") as f:
    for r in csv.DictReader(f,delimiter=";"):
        if r["ano"]=="2025" and r["cod_ibge"] in codes:
            per[r["cod_ibge"]]=float(r["dca_investimentos_liquidada_real_pc_set2026"])
assert set(per)==set(codes)
# Use polygon boundaries at source fidelity; no simplification.
def as_patches(geom):
    geoms=[geom] if geom.geom_type=="Polygon" else list(geom.geoms)
    patches=[]
    for g in geoms:
        patches.append(PatchPoly(list(g.exterior.coords),closed=True))
    return patches
minx=min(g.bounds[0] for g in selected.values())
miny=min(g.bounds[1] for g in selected.values())
maxx=max(g.bounds[2] for g in selected.values())
maxy=max(g.bounds[3] for g in selected.values())
padx=(maxx-minx)*.045;pady=(maxy-miny)*.05
def render(metric,title,subtitle,out,norm):
    fig,ax=plt.subplots(figsize=(11,8.5))
    plt.subplots_adjust(left=.055,right=.93,top=.86,bottom=.06)
    allpatch=[];vv=[]
    for code in sorted(codes):
        pp=as_patches(selected[code])
        allpatch.extend(pp);vv.extend([metric[code]]*len(pp))
    coll=PatchCollection(allpatch,cmap="coolwarm" if metric is change else "viridis",norm=norm,linewidths=.42,edgecolor="white")
    coll.set_array(vv)
    ax.add_collection(coll)
    ax.set_xlim(minx-padx,maxx+padx)
    ax.set_ylim(miny-pady,maxy+pady)
    ax.set_aspect("equal",adjustable="box")
    ax.axis("off")
    fig.suptitle(title,x=.06,y=.985,ha="left",fontsize=16,fontweight="bold")
    fig.text(.06,.923,subtitle,fontsize=10,ha="left")
    cb=fig.colorbar(coll,ax=ax,fraction=.025,pad=.016,shrink=.77)
    cb.set_label("Variação real (%)" if metric is change else "R$ por habitante",fontsize=10)
    for code,label in [("3549805","São José do Rio Preto"),("3533908","Olímpia"),("3531407","Monte Aprazível")]:
        pt=selected[code].representative_point()
        ax.plot([pt.x],[pt.y],marker=".",markersize=3,color="black")
        ax.annotate(label,(pt.x,pt.y),xytext=(4,4),textcoords="offset points",fontsize=7)
    fig.text(.06,.025,"Fonte: IBGE, malha municipal SP 2022, EPSG:4674; FINBRA/DCA 2023–2025. Sem simplificação geométrica.",fontsize=8)
    fig.savefig(ROOT/out,dpi=180,bbox_inches="tight")
    plt.close(fig)
render(change,"RMSJRP | Variação real dos investimentos, 2024–2025","Investimentos municipais liquidados (grupo 44); preços de setembro/2026", "MAPA_G05_VAR_INVEST_2024_2025.png",TwoSlopeNorm(vmin=min(change.values()),vcenter=0,vmax=max(change.values())))
render(per,"RMSJRP | Investimento real por habitante, 2025","Investimentos liquidados, R$ de setembro/2026 / população da base DCA","MAPA_G05_INVESTIMENTO_PC_2025.png",Normalize(vmin=min(per.values()),vmax=max(per.values())))
# Audit 37 source geometries unmodified and source provenance; regional GeoJSON selectively reproduces source vertices.
geojson={"type":"FeatureCollection","name":"RMSJRP_IBGE2022_37_EPSG4674","crs":{"type":"name","properties":{"name":"EPSG:4674"}},
         "features":[{"type":"Feature","properties":{"CD_MUN":code,"NM_MUN":codes[code]["municipio"],"subregiao_pdui":codes[code]["subregiao_pdui"],"variacao_investimento_real_pct_2024_2025":change[code],"investimento_pc_real_set2026_2025":per[code]},"geometry":mapping(selected[code])} for code in sorted(codes)]}
(ROOT/"RMSJRP_37_IBGE2022_EPSG4674.geojson").write_text(json.dumps(geojson,ensure_ascii=False,separators=(",",":"))+"\n",encoding="utf-8")
artifacts=[]
for name in ["RMSJRP_37_IBGE2022_EPSG4674.geojson","MAPA_G05_VAR_INVEST_2024_2025.png","MAPA_G05_INVESTIMENTO_PC_2025.png"]:
    file=ROOT/name;artifacts.append({"name":name,"bytes":file.stat().st_size,"sha256":hashlib.sha256(file.read_bytes()).hexdigest()})
qa={"status":"pass","source_url":"https://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/malhas_municipais/municipio_2022/UFs/SP/SP_Municipios_2022.zip",
    "source_sha256":sha_zip,"source_crs_epsg":crs.to_epsg(),"source_features":len(features),"selected_features":len(selected),"invalid_selected":invalid,
    "municipality_join":"37/37","geometry_simplification":False,"qa_level":"EPSG + shapely validity + keyed join, not complete polygon-overlap audit","artifacts":artifacts}
(ROOT/"QA_G05C_CARTOGRAFIA.json").write_text(json.dumps(qa,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"status":"pass","epsg":qa["source_crs_epsg"],"selected":37,"source_sha256":sha_zip,"artifacts":artifacts},ensure_ascii=False))
