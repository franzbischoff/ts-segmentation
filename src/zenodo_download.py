from __future__ import annotations
import argparse
import requests
import os
from pathlib import Path

CHUNK = 1024 * 128

def download_record(record_id: str, out_dir: str):
    url = f"https://zenodo.org/api/records/{record_id}"
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    data = r.json()
    files = data.get('files', [])
    if not files:
        print("Nenhum ficheiro encontrado no record.")
        return []
    os.makedirs(out_dir, exist_ok=True)
    downloaded = []
    for f in files:
        fname = f.get('key') or f.get('filename')
        furl = f.get('links', {}).get('self') or f.get('links', {}).get('download')
        size = f.get('size')
        if not fname or not furl:
            continue
        dest = Path(out_dir) / fname
        if dest.exists() and dest.stat().st_size == size:
            print(f"[SKIP] {fname} já existe com tamanho esperado.")
            downloaded.append(str(dest))
            continue
        print(f"[GET] {fname} ({size} bytes)")
        with requests.get(furl, stream=True, timeout=60) as resp:
            resp.raise_for_status()
            with open(dest, 'wb') as out_f:
                for chunk in resp.iter_content(CHUNK):
                    if chunk:
                        out_f.write(chunk)
        if size and dest.stat().st_size != size:
            print(f"[WARN] Tamanho divergente para {fname}: esperado {size}, obtido {dest.stat().st_size}")
        downloaded.append(str(dest))
    return downloaded


def parse_args():
    ap = argparse.ArgumentParser(description='Download de ficheiros de um record Zenodo')
    ap.add_argument('--record-id', required=True, help='ID do record no Zenodo (ex: 6879233)')
    ap.add_argument('--out-dir', default='data/zenodo_record', help='Diretório de saída')
    return ap.parse_args()


if __name__ == '__main__':
    args = parse_args()
    files = download_record(args.record_id, args.out_dir)
    print("Ficheiros baixados:")
    for f in files:
        print(f" - {f}")
