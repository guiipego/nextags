#!/usr/bin/env python3
"""Gera a seção CATÁLOGO do system prompt a partir de um catalogo.json.

Uso:
    python3 montar_catalogo.py catalogo.json catalogo.md

O formato do JSON está em references/coleta-catalogo.md (seção 8).
O texto gerado não usa ** nem tabelas: o modelo tende a copiar a formatação
do contexto para o WhatsApp, onde ** aparece literal.
"""
import json
import sys


def brl(valor):
    texto = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {texto}"


def preco_texto(preco):
    if preco is None or preco == "":
        return "consultar a equipe"
    if isinstance(preco, (int, float)):
        return brl(float(preco))
    return str(preco).strip()


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    entrada, saida = sys.argv[1], sys.argv[2]
    dados = json.load(open(entrada, encoding="utf-8"))
    rotulo_link = dados.get("rotulo_link", "Detalhes/ingredientes")

    linhas, avisos, erros = [], [], []
    nomes, total = {}, 0
    fotos = {}

    for secao in dados.get("secoes", []):
        linhas.append(f"## {secao['titulo']}\n")
        for grupo in secao.get("grupos", []):
            linhas.append(f"### {grupo['titulo']}\n")
            for item in grupo.get("itens", []):
                total += 1
                nome = (item.get("nome") or "").strip()
                desc = (item.get("descricao") or "").strip()
                if not nome:
                    erros.append(f"item sem nome no grupo '{grupo['titulo']}'")
                    continue
                if not desc:
                    avisos.append(f"{nome}: sem descrição")
                if "lorem ipsum" in desc.lower():
                    erros.append(f"{nome}: descrição com 'Lorem ipsum' (reescreva a partir da foto)")
                if nome.lower() in nomes:
                    avisos.append(f"{nome}: nome repetido (também em '{nomes[nome.lower()]}')")
                nomes[nome.lower()] = grupo["titulo"]

                if item.get("preco") in (None, ""):
                    avisos.append(f"{nome}: sem preço (vai como 'consultar a equipe')")
                foto = item.get("foto")
                if foto:
                    if not str(foto).startswith("http"):
                        erros.append(f"{nome}: foto não é URL ({foto[:40]})")
                    fotos.setdefault(foto, []).append(nome)
                else:
                    avisos.append(f"{nome}: sem foto")

                cabecalho = f"- {nome}"
                if item.get("tamanho"):
                    cabecalho += f" | {item['tamanho']}"
                cabecalho += f" | {preco_texto(item.get('preco'))}"
                bloco = [cabecalho, f"  - Descrição: {desc or '(sem descrição)'}"]
                bloco.append(f"  - Foto: {foto if foto else '(sem foto)'}")
                for obs in item.get("obs") or []:
                    bloco.append(f"  - Obs.: {obs}")
                if item.get("link"):
                    bloco.append(f"  - {rotulo_link}: {item['link']}")
                linhas.append("\n".join(bloco))
            linhas.append("")

    for url, donos in fotos.items():
        if len(donos) > 1:
            sem_obs = [n for n in donos if not any(
                "ilustrativa" in o for sec in dados["secoes"] for g in sec["grupos"]
                for i in g["itens"] if i.get("nome") == n for o in (i.get("obs") or []))]
            if sem_obs:
                avisos.append(
                    f"mesma foto em {', '.join(donos)}: marque como 'foto ilustrativa' em obs")

    adicionais = dados.get("adicionais")
    if adicionais and adicionais.get("itens"):
        linhas.append(f"## {adicionais.get('titulo', 'ADICIONAIS')}\n")
        for a in adicionais["itens"]:
            linhas.append(f"- {a['nome']}: {preco_texto(a.get('preco'))}")
        linhas.append("")

    if erros:
        print("ERROS (corrija antes de seguir):")
        for e in erros:
            print("  -", e)
        sys.exit(1)

    open(saida, "w", encoding="utf-8").write("\n".join(linhas).rstrip() + "\n")
    webp = sum(1 for u in fotos if u.lower().split("?")[0].endswith(".webp"))
    print(f"ok: {total} itens -> {saida}")
    print(f"fotos: {len(fotos)} URLs distintas ({webp} em WebP)")
    if avisos:
        print("AVISOS:")
        for a in avisos:
            print("  -", a)


if __name__ == "__main__":
    main()
