#!/usr/bin/env python3
"""FED01: QA local de pacotes ZIP privados RMRP, sem publicar linhas individuais.

Uso: python pipeline/qa/qa_rmrp_private_acquisition_zips.py \
 --transferegov /caminho/Transferegov.zip --obrasgov /caminho/Obrasgov.zip \
 --output /caminho/manifesto-qa.json
A saída registra apenas hashes, nomes de membros, CRC, cabeçalhos e contagens.
"""
import argparse
import csv
import hashlib
import io
import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path

def inspect_zip(path):
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(path)
    sha = hashlib.sha256()
    with path.open("rb") as stream:
        while True:
            chunk = stream.read(1024 * 1024)
            if not chunk:
                break
            sha.update(chunk)
    report = {"file_name": path.name, "size_bytes": path.stat().st_size,
              "sha256": sha.hexdigest(), "members": []}
    with zipfile.ZipFile(path, "r") as archive:
        files = [i for i in archive.infolist() if not i.is_dir()]
        if not files:
            raise ValueError("ZIP vazio: " + path.name)
        for info in files:
            member = {"name": info.filename, "bytes": info.file_size,
                      "crc32": format(info.CRC, "08x")}
            if info.filename.lower().endswith((".csv", ".jsonl")):
                with archive.open(info) as binary:
                    # Apenas contar linhas, sem expor registros ou campos pessoais.
                    count = sum(1 for _ in binary)
                member["physical_lines_including_header"] = count
                member["note"] = "Linhas fisicas; CSV multilinha requer parser para contar registros."
            report["members"].append(member)
        invalid = archive.testzip()
        if invalid:
            raise ValueError("CRC invalido no membro: " + invalid)
    report["crc_status"] = "pass"
    return report

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--transferegov", required=True)
    parser.add_argument("--obrasgov", required=True)
    parser.add_argument("--output", required=True)
    a = parser.parse_args()
    result = {"gate": "G-FED-01", "checked_at_utc":
              datetime.now(timezone.utc).isoformat(),
              "privacy": "aggregates_only", "scope": "RMRP34",
              "transferegov": inspect_zip(a.transferegov),
              "obrasgov": inspect_zip(a.obrasgov),
              "financial_qa": "pending",
              "proponent_is_not_execution_location": True}
    target = Path(a.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n",
                      encoding="utf-8")
    print(json.dumps({"gate": result["gate"], "crc": "pass",
                      "manifest_path": str(target)}, ensure_ascii=False))

if __name__ == "__main__":
    main()
