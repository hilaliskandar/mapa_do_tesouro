#!/usr/bin/env python3
"""Auditoria offline dos boletins e fichas, sem acessar as fontes."""
import argparse, hashlib, html, json, pathlib, re
from html.parser import HTMLParser

class Reader(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links=[]
        self.texts=[]
        self._href=None
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if tag=="a":self._href=attrs.get("href")
    def handle_endtag(self,tag):
        if tag=="a":self._href=None
    def handle_data(self,data):
        self.texts.append(data)
    def handle_startendtag(self,tag,attrs):
        pass

def audit(folder):
    m=json.loads((folder/"manifest.json").read_text(encoding="utf-8"))
    ed=m.get("editions",[])
    profiles=m.get("municipal_profiles",[])
    assert len(ed)==10, f"Edicoes {len(ed)}"
    assert len(profiles)==280, f"Fichas {len(profiles)}"
    assert len({x["publication_id"] for x in ed})==10
    assert len({(x["publication_id"],str(x["codigo_ibge"])) for x in profiles})==280
    assert all(re.fullmatch(r"\d{7}",str(x["codigo_ibge"])) for x in profiles)
    totals=0
    for x in ed:
        uid=x["publication_id"]
        page=folder/uid/"index.html"
        raw=page.read_bytes()
        assert hashlib.sha256(raw).hexdigest()==x["html_sha256"],(uid,"hash HTML divergente")
        assert b"<html" in raw.lower() and b"</html>" in raw.lower()
        assert b"Fichas municipais" in raw
        assert b"Evolu" in raw
        matches=[p for p in profiles if p["publication_id"]==uid]
        assert len(matches)==x["member_count"],(uid,len(matches),x["member_count"])
        for p in matches:
            code=str(p["codigo_ibge"])
            fiche=folder/uid/"municipios"/f"{code}.html"
            raw_profile=fiche.read_bytes()
            assert hashlib.sha256(raw_profile).hexdigest()==p["html_sha256"],(uid,code,"hash ficha divergente")
            content=raw_profile.decode("utf-8")
            assert code in content,(uid,code,"codigo ausente")
            assert "Mediana do grupo" in content,(uid,code,"sem mediana")
            assert "../index.html" in content,(uid,code,"sem retorno")
            assert f"municipios/{code}.html" in raw.decode("utf-8"),(uid,code,"ficha nao vinculada ao boletim")
            assert ("Consultar os registros" in content or "API privada de homologação" in content or "Dados fiscais e metadados da versão candidata" in content),(uid,code,"sem fonte")
            if "Dados fiscais e metadados da versão candidata" in content:
                source=folder.parent/"data/api/v1/publication/universes"/uid/"municipalities"/f"{code}.json"
                assert source.is_file(),(uid,code,"fonte JSON relativa inexistente")
            assert "href=\"file://" not in content,(uid,code,"link local inacessivel")
            assert "http://" not in content,(uid,code,"referencia insegura")
            totals+=1
    print(f"QA estrutural: {len(ed)} universos, {totals} fichas, links locais e fontes OK")
    return True

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--out",default="build/editorial-universes")
    a=p.parse_args()
    audit(pathlib.Path(a.out))
