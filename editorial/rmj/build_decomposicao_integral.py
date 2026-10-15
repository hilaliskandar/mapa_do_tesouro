#!/usr/bin/env python3
"""Reproduz a decomposição TCESP RMJ 2023-2025 a partir dos 21 JSON originais."""
import csv,json,sys
from collections import defaultdict
from pathlib import Path
CITIES={'cabreuva':'Cabreúva','campo-limpo-paulista':'Campo Limpo Paulista','itupeva':'Itupeva','jarinu':'Jarinu','jundiai':'Jundiaí','louveira':'Louveira','varzea-paulista':'Várzea Paulista'}
FIELDS=['nivel','municipio','ano_inicial','ano_final','codigo_programa','codigo_acao','descricao_ano_inicial','descricao_ano_final','situacao','liquidado_inicial_centavos','liquidado_final_centavos','variacao_centavos']
def records(doc,level):
    arr=doc['programas_44_liquidado_completos'] if level=='programa' else doc['acoes_44_liquidado_completas']
    result={}
    for row in arr:
        if level=='programa':
            program,name,_,cents=row;key=(str(program),'')
        else:
            program,action,name,_,cents=row;key=(str(program),str(action))
        assert key not in result,(doc['slug'],doc['year'],key)
        result[key]=(str(name).strip(),int(cents))
    assert sum(v[1] for v in result.values())==int(doc['investimento_44_liquidado_centavos'])
    return result
def main(source,dest):
    source=Path(source);dest=Path(dest);dest.mkdir(parents=True,exist_ok=True)
    docs={}
    for slug in CITIES:
        for year in (2023,2024,2025):
            p=source/f'{slug}_{year}.json'
            d=json.loads(p.read_text(encoding='utf-8'))
            assert d['slug']==slug and d['year']==year and not d['bad_values'],p
            docs[(slug,year)]=d
    output=[];checks=0
    for slug,city in CITIES.items():
        for start,end in ((2023,2024),(2024,2025)):
            for level in ('programa','acao'):
                a=records(docs[(slug,start)],level);b=records(docs[(slug,end)],level)
                delta=0
                for key in sorted(set(a)|set(b)):
                    name0,c0=a.get(key,('',0));name1,c1=b.get(key,('',0))
                    status=('somente_ano_final' if key not in a else 'somente_ano_inicial' if key not in b else 'mesmo_codigo_mesmo_nome' if name0==name1 else 'mesmo_codigo_nome_alterado')
                    output.append(dict(zip(FIELDS,[level,city,start,end,key[0],key[1],name0,name1,status,c0,c1,c1-c0])))
                    delta+=c1-c0
                assert delta==docs[(slug,end)]['investimento_44_liquidado_centavos']-docs[(slug,start)]['investimento_44_liquidado_centavos']
                checks+=1
    p=dest/'rmj_decomposicao_programas_acoes_2023_2025.csv'
    with p.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS,delimiter=';');w.writeheader();w.writerows(output)
    assert checks==28
    print(json.dumps({'linhas':len(output),'conciliacoes':checks,'arquivo':str(p)},ensure_ascii=False))
if __name__=='__main__':main(*sys.argv[1:3])
