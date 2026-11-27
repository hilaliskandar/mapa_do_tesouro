#!/usr/bin/env python3
"""Triagem documental das ausencias DCA, sem mudar status ou imputar zero."""
import argparse,json,pathlib,collections
import yaml

TARGETS=("dca_inversoes_financeiras_liquidada","dca_operacoes_credito",
         "dca_alienacao_bens","dca_func_habitacao_liquidada",
         "dca_func_saneamento_liquidada")
def audit(root,mapping):
    m=json.loads((root/"publicacoes/manifest.json").read_text(encoding="utf-8"))
    catalog=yaml.safe_load(mapping.read_text(encoding="utf-8"))["variables"]
    result={"total_fichas":len(m["municipal_profiles"]),"contas":{},"casos_especiais":[]}
    assert result["total_fichas"]==280
    for key in TARGETS:
        spec=catalog[key]
        result["contas"][key]={"criterio_exato":{k:spec.get(k) for k in ("annex","column","rotulo","cod_conta","conta_regex")},
                              "status":collections.Counter(),"exemplos_ausentes":[]}
    for entry in m["municipal_profiles"]:
        code=str(entry["codigo_ibge"]);uid=entry["publication_id"]
        path=root/"data/api/v1/publication/universes"/uid/"municipalities"/(code+".json")
        obj=json.loads(path.read_text(encoding="utf-8"))
        for key in TARGETS:
            variable=(obj.get("variables") or {}).get(key) or {}
            latest=variable.get("latest") or {}
            status=str(latest.get("status") or "sem_registro")
            value=latest.get("value")
            if status=="observado" and value==0:status="observado_zero"
            result["contas"][key]["status"][status]+=1
            if status in ("ausente","sem_registro") and len(result["contas"][key]["exemplos_ausentes"])<4:
                result["contas"][key]["exemplos_ausentes"].append({"universo":uid,"codigo_ibge":code,"municipio":obj.get("municipality",{}).get("nome")})
    for key in TARGETS:result["contas"][key]["status"]=dict(result["contas"][key]["status"])
    result["interpretacao"]="O identificador de rubrica exata e o status da API nao provam inexistencia de movimento. Confronto dos itens brutos do anexo DCA e necessario antes de qualquer correcao."
    return result

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--root",type=pathlib.Path,required=True)
    p.add_argument("--mapping",type=pathlib.Path,default=pathlib.Path("data/mappings/dca_canonical_v1.yml"))
    p.add_argument("--out",type=pathlib.Path,required=True)
    a=p.parse_args();report=audit(a.root,a.mapping)
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"total_fichas":report["total_fichas"],"status":{k:v["status"] for k,v in report["contas"].items()}},ensure_ascii=False))
