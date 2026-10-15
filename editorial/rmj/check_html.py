#!/usr/bin/env python3
"""Validacao estrutural do boletim HTML RMJ, sem dependencias externas."""
from html.parser import HTMLParser
from pathlib import Path
import re
import sys

class Audit(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.refs = []
        self.sections = []
        self.scripts = []
        self.script = False
        self.external_urls = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if "id" in d:
            self.ids.append(d["id"])
        if tag == "section" and "id" in d:
            self.sections.append(d["id"])
        if tag == "a" and d.get("href", "").startswith("#"):
            self.refs.append(d["href"][1:])
        if tag == "a" and d.get("href", "").startswith(("https://", "http://")):
            self.external_urls.append(d["href"])
        if tag == "script":
            self.script = True

    def handle_endtag(self, tag):
        if tag == "script":
            self.script = False

    def handle_data(self, data):
        if self.script:
            self.scripts.append(data)

def main():
    html = Path(sys.argv[1]).read_text(encoding="utf-8")
    p = Audit()
    p.feed(html)
    ids = set(p.ids)
    errors = []
    if len(ids) != len(p.ids):
        errors.append("IDs HTML duplicados")
    for ref in p.refs:
        if ref not in ids:
            errors.append(f"Link interno aponta para ID inexistente: {ref}")
    for ref in re.findall(r'getElementById\(["\']([^"\']+)["\']\)', html):
        if ref not in ids:
            errors.append(f"JavaScript usa ID inexistente: {ref}")
    for required in ["resumo", "municipios", "historico", "sintese", "legais", "perfis", "funcoes", "contas", "receitas", "reais", "metodo", "fontes"]:
        if required not in p.sections:
            errors.append(f"Secao obrigatoria ausente: {required}")
    if len(p.scripts) != 1:
        errors.append(f"Esperado um bloco JS inline; encontrados {len(p.scripts)}")
    required_domains = ("drive.google.com", "finbra-tic-tim-referencia.pages.dev", "github.com")
    for domain in required_domains:
        if not any(domain in url for url in p.external_urls):
            errors.append(f"Link de fonte externa obrigatorio ausente: {domain}")
    if "Referência principal: 2024 e 2025; séries históricas selecionadas: 2021–2025" not in html:
        errors.append("Escopo temporal do boletim nao foi explicitado")
    if "todos os montantes permanecem" not in html:
        errors.append("Ressalva sobre valores nominais nao encontrada")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        raise SystemExit(1)
    Path(sys.argv[2]).write_text("\n".join(p.scripts), encoding="utf-8")
    print(f"PASS: {len(ids)} IDs, {len(p.sections)} secoes, {len(p.refs)} links internos")

if __name__ == "__main__":
    main()
