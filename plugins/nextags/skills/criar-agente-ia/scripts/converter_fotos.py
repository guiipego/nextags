#!/usr/bin/env python3
"""Converte as fotos do catálogo que o WhatsApp não aceita (WebP, GIF ou acima de 5 MB) para JPG.

Uso:
    python3 converter_fotos.py catalogo.json <pasta_saida> [--incluir-png] [--base-url https://site.com/fotos/]

O que faz:
  1. baixa cada foto WebP/GIF ou com mais de 5 MB (e PNG, com --incluir-png) para <pasta_saida>/originais/;
  2. converte para JPG com fundo branco (no máximo 1600 px no lado maior, qualidade 85) em <pasta_saida>/jpg/;
  3. grava <pasta_saida>/mapa_fotos.csv (produto, URL original, arquivo JPG).
Com --base-url, grava também catalogo_jpg.json com as URLs novas
(base-url + nome do arquivo). Use depois que o cliente subir os JPGs nesse endereço.

Use --incluir-png quando houver PNG, principalmente de CDN de loja: o CDN da Shopify, por exemplo,
entrega WebP para PNG com fundo transparente, e o WhatsApp recusa ("WebP image uploads are not
currently supported"). Transparência vira fundo branco.

Converte com Pillow, se estiver instalado. Se não estiver, usa o `sips` do macOS.
"""
import csv
import json
import re
import shutil
import subprocess
import sys
import unicodedata
import urllib.request
from pathlib import Path

LIMITE_WHATSAPP = 5 * 1024 * 1024


def slug(texto):
    texto = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", texto.lower()).strip("-") or "foto"


def baixar(url, destino):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        destino.write_bytes(r.read())
        return r.headers.get("Content-Type", "")


def converter(origem, destino):
    try:
        from PIL import Image  # type: ignore
        with Image.open(origem) as im:
            if im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info):
                rgba = im.convert("RGBA")
                fundo = Image.new("RGB", rgba.size, (255, 255, 255))
                fundo.paste(rgba, mask=rgba.split()[3])  # transparente vira branco, não preto
                im = fundo
            else:
                im = im.convert("RGB")
            im.thumbnail((1600, 1600))
            im.save(destino, "JPEG", quality=85, optimize=True)
        return True
    except ImportError:
        pass
    if shutil.which("sips"):
        info = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(origem)],
                              capture_output=True, text=True).stdout
        lados = [int(n) for n in re.findall(r"pixel(?:Width|Height):\s*(\d+)", info)]
        reduzir = ["-Z", "1600"] if lados and max(lados) > 1600 else []  # -Z também amplia
        r = subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "85", *reduzir,
                            str(origem), "--out", str(destino)],
                           capture_output=True, text=True)
        return r.returncode == 0
    print("Sem Pillow e sem sips: instale Pillow (pip install pillow).")
    sys.exit(1)


def precisa(url, caminho_local, incluir_png):
    ext = url.lower().split("?")[0].rsplit(".", 1)[-1]
    if ext in ("webp", "gif") or (incluir_png and ext == "png"):
        return True
    with open(caminho_local, "rb") as f:
        cabecalho = f.read(16)
    if cabecalho[:4] == b"RIFF" and cabecalho[8:12] == b"WEBP":  # WebP com outra extensão
        return True
    return caminho_local.stat().st_size > LIMITE_WHATSAPP


def main():
    args = sys.argv[1:]
    if len(args) < 2:
        print(__doc__)
        sys.exit(2)
    catalogo_p, saida = Path(args[0]), Path(args[1])
    base = args[args.index("--base-url") + 1] if "--base-url" in args else None
    incluir_png = "--incluir-png" in args
    dados = json.loads(catalogo_p.read_text(encoding="utf-8"))
    (saida / "originais").mkdir(parents=True, exist_ok=True)
    (saida / "jpg").mkdir(parents=True, exist_ok=True)

    feitos, mapa, usados = {}, [], set()
    for sec in dados.get("secoes", []):
        for g in sec.get("grupos", []):
            for item in g.get("itens", []):
                url = item.get("foto")
                if not url:
                    continue
                if url in feitos:
                    nome_jpg = feitos[url]
                else:
                    base_nome = slug(item["nome"])
                    nome_jpg, n = f"{base_nome}.jpg", 2
                    while nome_jpg in usados:
                        nome_jpg, n = f"{base_nome}-{n}.jpg", n + 1
                    original = saida / "originais" / (base_nome + Path(url.split("?")[0]).suffix)
                    try:
                        baixar(url, original)
                    except Exception as e:  # noqa: BLE001
                        print(f"  falhou ao baixar {item['nome']}: {e}")
                        continue
                    if not precisa(url, original, incluir_png):
                        continue
                    if not converter(original, saida / "jpg" / nome_jpg):
                        print(f"  falhou ao converter {item['nome']}")
                        continue
                    usados.add(nome_jpg)
                    feitos[url] = nome_jpg
                mapa.append({"produto": item["nome"], "url_original": url, "arquivo_jpg": nome_jpg})
                if base:
                    item["foto"] = base.rstrip("/") + "/" + nome_jpg

    with open(saida / "mapa_fotos.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["produto", "url_original", "arquivo_jpg"])
        w.writeheader()
        w.writerows(mapa)
    if base:
        (saida / "catalogo_jpg.json").write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"ok: {len(feitos)} foto(s) convertida(s) para JPG em {saida / 'jpg'}")
    print(f"mapa: {saida / 'mapa_fotos.csv'}" + (f" | catálogo novo: {saida / 'catalogo_jpg.json'}" if base else ""))


if __name__ == "__main__":
    main()
