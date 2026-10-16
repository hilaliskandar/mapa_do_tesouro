"""Montagem privada de pacote navegavel com API e HTMLs da mesma fonte.

Nao realiza deploy. Manifesto identifica hashes dos JSONs e HTMLs reescritos.
"""
import argparse,hashlib,json,shutil
from pathlib import Path

SOURCE_NOTE="Fonte: API privada de homologação, com proveniência registrada no manifesto do artefato. Sem endereço público."

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def build(api:Path,editorial:Path,output:Path):
    if output.exists():
        raise ValueError("Diretorio de destino existente: "+str(output))
    (output/"data/api/v1").parent.mkdir(parents=True,exist_ok=True)
    shutil.copytree(api,output/"data/api/v1")
    shutil.copytree(editorial,output/"publicacoes")
    manifest_path=output/"publicacoes/manifest.json"
    manifest=json.loads(manifest_path.read_text(encoding="utf-8"))
    if len(manifest["editions"])!=10 or len(manifest["municipal_profiles"])!=280:
        raise ValueError("Universos ou fichas inesperados")
    for item in manifest["editions"]:
        uid=item["publication_id"]
        target=output/"publicacoes"/uid/"index.html"
        link=f'Fonte: <a href="../../data/api/v1/publication/universes/{uid}/context.json">Contexto fiscal e metadados da versão candidata</a>.'
        original=target.read_text(encoding="utf-8")
        if original.count(SOURCE_NOTE)!=1:raise ValueError(f"Proveniencia inesperada: {uid}")
        target.write_text(original.replace(SOURCE_NOTE,link),encoding="utf-8")
        item["html_sha256"]=digest(target)
    for item in manifest["municipal_profiles"]:
        uid=item["publication_id"];code=str(item["codigo_ibge"])
        target=output/"publicacoes"/uid/"municipios"/f"{code}.html"
        link=f'Fonte: <a href="../../../data/api/v1/publication/universes/{uid}/municipalities/{code}.json">Dados fiscais e metadados da versão candidata</a>.'
        original=target.read_text(encoding="utf-8")
        if original.count(SOURCE_NOTE)!=1:raise ValueError(f"Proveniencia inesperada: {uid}/{code}")
        target.write_text(original.replace(SOURCE_NOTE,link),encoding="utf-8")
        item["html_sha256"]=digest(target)
    manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    files=[p for p in output.rglob("*") if p.is_file()]
    checks={str(p.relative_to(output)):digest(p) for p in files}
    release={"status":"private-preview-only","api_source":"SP645 private build GitHub Actions 38905063653","editorial_source":"same approved private API","public_deploy":False,"api_json_count":sum(1 for p in (output/"data/api/v1").rglob("*.json")),"bulletins":10,"municipal_profiles":280,"files":checks}
    (output/"PREVIEW_MANIFEST.json").write_text(json.dumps(release,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return release

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--api",type=Path,required=True);p.add_argument("--editorial",type=Path,required=True);p.add_argument("--output",type=Path,required=True)
    a=p.parse_args();r=build(a.api,a.editorial,a.output);print("Pacote candidato:",r["bulletins"],r["municipal_profiles"],"API JSONs:",r["api_json_count"])
