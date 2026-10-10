#!/usr/bin/env python3
"""Inspeciona links de Despesa Detalhada do TCESP sem inventar URLs."""
import html
from html.parser import HTMLParser
from urllib.request import Request, urlopen
from urllib.parse import urljoin
import json
import sys

class A(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack=[]
        self.anchors=[]
    def handle_starttag(self,tag,attrs):
        if tag=="a":
            self.stack.append({"attrs":dict(attrs),"text":""})
    def handle_data(self,data):
        if self.stack:
            self.stack[-1]["text"]+=data
    def handle_endtag(self,tag):
        if tag=="a" and self.stack:
            self.anchors.append(self.stack.pop())

urls=["https://transparencia.tce.sp.gov.br/municipio/jundiai/2025"]
for url in urls:
    try:
        req=Request(url,headers={"User-Agent":"Mozilla/5.0 RMJ-Research/1.0"})
        with urlopen(req,timeout=30) as resp:
            raw=resp.read()
        text=raw.decode("utf-8","replace")
        p=A();p.feed(text)
        matches=[{"text":a["text"].strip(),"href":urljoin(url,a["attrs"].get("href","")),"attrs":a["attrs"]} for a in p.anchors if "despesa detalhada" in a["text"].lower()]
        marker=text.lower().find("despesa detalhada")
        print(json.dumps({"page":url,"status":"html_obtido","bytes":len(raw),"links":matches,"near_marker_html":text[max(0,marker-280):marker+430] if marker>=0 else ""},ensure_ascii=False,indent=2))
        if matches:
            from io import BytesIO
            import zipfile
            reqzip=Request(matches[0]["href"],headers={"User-Agent":"Mozilla/5.0"})
            with urlopen(reqzip,timeout=90) as zresp:
                blob=zresp.read(30000000)
                mime=zresp.headers.get("Content-Type")
            if not zipfile.is_zipfile(BytesIO(blob)):
                raise ValueError("O arquivo retornado nao e ZIP valido")
            with zipfile.ZipFile(BytesIO(blob)) as archive:
                files=[{"nome":v.filename,"tamanho":v.file_size} for v in archive.infolist()]
                sample=archive.read(archive.infolist()[0])[:1800].decode("utf-8","replace") if archive.infolist() else ""
            print(json.dumps({"status":"zip_validado","url":matches[0]["href"],"bytes":len(blob),"mime":mime,"files":files,"sample":sample},ensure_ascii=False,indent=2))
    except Exception as e:
        print(json.dumps({"page":url,"status":"erro","error":str(e)},ensure_ascii=False))
        sys.exit(1)
