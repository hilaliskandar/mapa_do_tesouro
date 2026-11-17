#!/usr/bin/env python3
"""Aquisição somente-leitura de arquivo oficial de convênios do Estado de SP.

URL obtida por inspeção da página oficial com Crawl2AI (16/11/2026).
Por padrão não faz qualquer acesso de rede; exige --download.
Não presume que ZIP tenha períodos completos ou schema estável.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from zipfile import ZipFile, BadZipFile

SOURCE = "https://www.transparencia.sp.gov.br/Dados%20Abertos/Convenios/convenio.zip"
HOST = "www.transparencia.sp.gov.br"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--download", action="store_true", help="habilita requisição à URL oficial")
    parser.add_argument("--outdir", type=Path, default=Path("out/sp_convenios"))
    args = parser.parse_args()
    if not args.download:
        parser.error("execução segura: usar --download para obter o snapshot oficial")
    url = SOURCE
    if urlparse(url).hostname != HOST:
        raise ValueError("host não autorizado")
    out = args.outdir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    dest = out / f"sp_convenios_{timestamp}.zip"
    request = Request(url, headers={"User-Agent": "MapaDoTesouro/1.0 (coleta de dados publicos)", "Accept": "application/zip,application/octet-stream"})
    with urlopen(request, timeout=90) as response, dest.open("wb") as target:
        status = response.status
        content_type = response.headers.get("Content-Type", "")
        final_url = response.geturl()
        if status != 200 or urlparse(final_url).hostname != HOST:
            raise RuntimeError(f"resposta HTTP inesperada: {status}, {final_url}")
        total = 0
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            total += len(chunk)
            if total > 1_000_000_000:
                raise RuntimeError("limite de tamanho de arquivo excedido")
            target.write(chunk)
    manifest = {
        "fonte_id": "SP_CONV",
        "url": url,
        "final_url": final_url,
        "http_status": status,
        "content_type": content_type,
        "collected_utc": datetime.now(timezone.utc).isoformat(),
        "path": str(dest),
        "bytes": dest.stat().st_size,
        "sha256": sha256_file(dest),
        "qa_status": "pendente",
        "zip_members": [],
        "errors": [],
    }
    try:
        with ZipFile(dest) as archive:
            bad = archive.testzip()
            if bad:
                raise RuntimeError(f"CRC inválido: {bad}")
            for member in archive.infolist():
                entry = {"name": member.filename, "uncompressed_bytes": member.file_size, "crc": member.CRC}
                if member.filename.lower().endswith(".csv") and not member.is_dir():
                    # Estatística sem armazenar identificadores de beneficiários em log.
                    with archive.open(member) as stream:
                        entry["line_count_including_header"] = sum(1 for _ in stream)
                manifest["zip_members"].append(entry)
            manifest["qa_status"] = "validado_estrutura"
    except (BadZipFile, RuntimeError, OSError) as exc:
        manifest["qa_status"] = "bloqueado"
        manifest["errors"].append(str(exc))
    manifest_file = dest.with_suffix(".manifest.json")
    manifest_file.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"manifest": str(manifest_file), "zip": str(dest), "qa_status": manifest["qa_status"], "bytes": manifest["bytes"], "sha256": manifest["sha256"]}, ensure_ascii=False))
    if manifest["qa_status"] != "validado_estrutura":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
