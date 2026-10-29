#!/usr/bin/env python3
"""Confere os 3 arquivos do agente Nextags antes da entrega.

Uso:
    python3 validar_arquivos.py <pasta> [--checar-urls]

Espera na pasta:
    1_mensagem_do_sistema.md, 2_prompt_da_acao.md, 3_acoes_de_ia.md

ERRO  = precisa corrigir.  AVISO = avalie (pode ser intencional).
Com --checar-urls, testa cada URL do system prompt (precisa de internet).
"""
import re
import sys
import unicodedata
import urllib.request
from pathlib import Path

ARQUIVOS = ["1_mensagem_do_sistema.md", "2_prompt_da_acao.md", "3_acoes_de_ia.md"]

CAMPOS_SISTEMA = {
    "first_name", "last_name", "full_name", "email", "phone", "user_country", "user_state",
    "user_city", "inbox_link", "gender", "locale", "locale2", "username", "profile_pic",
    "timezone", "user_id", "subscribed_date", "fb_chat_link", "me", "webchat", "user_code",
    "last_btt_title", "last_interaction", "last_order", "last_seen", "last_text_input",
    "last_input", "last_input_type", "consecutive_failed_reply", "last_ref", "last_ad",
    "user_channel", "user_hash", "user_tags", "user_external_id", "user_source",
    "assigned_admin_name", "assigned_admin_id", "current_user_time", "chat_history",
    "chat_history_large", "chat_history_details", "chat_history_details_large", "last_points",
    "user_notes", "last_user_note", "last_call_recorded", "last_step", "current_step",
    "account_name", "account_id", "account_image", "ig_user_name", "last_latitude",
    "last_longitude", "booking_date", "booking_link", "booking_id", "booking_calendar",
    "cart_total", "cart_subtotal", "order_products", "order_total", "order_status",
}

ACOES = {
    "enviar fluxo", "atribuir conversa a um administrador", "remover atribuição",
    "transferir conversa para humano", "adicionar etiqueta", "remover etiqueta",
    "definir campo personalizado", "limpar campo personalizado", "seguir",
    "remover do acompanhamento", "transferir conversa para bot", "arquivar", "bloquear contato",
    "adicionar mensagens ao prompt",
}

EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿⭐⭕]")


def norm(texto):
    texto = unicodedata.normalize("NFKC", texto).casefold()
    return re.sub(r"\s+", " ", texto).strip(" .,!?;:\"'“”")


def secao(texto, titulo):
    """Trecho de um título '# TITULO' até o próximo título de nível 1."""
    m = re.search(rf"^# {re.escape(titulo)}.*$", texto, re.M)
    if not m:
        return ""
    resto = texto[m.end():]
    fim = re.search(r"^# ", resto, re.M)
    return resto[: fim.start()] if fim else resto


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    checar_urls = "--checar-urls" in sys.argv
    if len(args) != 1:
        print(__doc__)
        sys.exit(2)
    pasta = Path(args[0])
    erros, avisos, info = [], [], []

    textos = {}
    for nome in ARQUIVOS:
        p = pasta / nome
        if not p.exists():
            erros.append(f"arquivo faltando: {nome}")
        else:
            textos[nome] = p.read_text(encoding="utf-8")
    if erros:
        relatorio(erros, avisos, info)
        return

    sp, pa, ac = (textos[n] for n in ARQUIVOS)

    # 1. Placeholders de modelo esquecidos
    for nome, t in textos.items():
        for ph in sorted(set(re.findall(r"\{\{[A-Z_]+\}\}|\[PREENCHER[^\]]*\]|<PREENCHER[^>]*>|\{[a-z_]+\}(?!\})", t))):
            if not ph.startswith("{{") or ph.strip("{}").isupper():
                erros.append(f"{nome}: placeholder de modelo não preenchido: {ph}")
        if "lorem ipsum" in t.lower():
            erros.append(f"{nome}: contém 'Lorem ipsum'")

    # 2. Variáveis da Nextags x campos personalizados criados no arquivo 3
    cufs = set(re.findall(r"Definir Campo Personalizado\s*→\s*`?([a-z0-9_]+)", ac))
    cufs |= set(re.findall(r"^\|\s*`?([a-z0-9_]+)`?\s*\|", ac, re.M))
    usadas = sorted(set(re.findall(r"\{\{([a-z0-9_]+)\}\}", sp)))
    for v in usadas:
        if v not in CAMPOS_SISTEMA and v not in cufs:
            erros.append(f"system prompt usa {{{{{v}}}}}, mas esse campo não é do sistema nem é criado no arquivo 3")
    if usadas:
        info.append("variáveis Nextags no system prompt: " + ", ".join("{{%s}}" % v for v in usadas))
    gravados = set(re.findall(r"Definir Campo Personalizado\s*→\s*`?([a-z0-9_]+)", ac))
    tabela = set(re.findall(r"^\|\s*`?([a-z0-9_]+)`?\s*\|", ac, re.M)) - {"nome_do_campo"}
    for c in sorted(tabela - gravados):
        avisos.append(f"campo '{c}' está na tabela do arquivo 3, mas nenhuma regra grava nele")

    # 3. Contexto dinâmico no final (cache de prompt)
    pos_cat = sp.find("# CATÁLOGO")
    pos_ctx = sp.find("{{current_user_time}}")
    if pos_ctx != -1 and pos_cat != -1 and pos_ctx < pos_cat:
        avisos.append("{{current_user_time}} aparece antes do catálogo: deixe o contexto dinâmico no final do prompt")
    if pos_ctx == -1:
        avisos.append("system prompt não usa {{current_user_time}}: o agente não vai saber dia/hora (horário de funcionamento)")

    # 4. [A DEFINIR] em aberto
    for i, linha in enumerate(sp.splitlines(), 1):
        if "[A DEFINIR]" in linha and "`[A DEFINIR]`" not in linha:
            info.append(f"pendente (linha {i}): {linha.strip()[:100]}")

    # 5. Markdown de site no prompt (o modelo copia ** para o WhatsApp)
    cat = secao(sp, "CATÁLOGO")
    if not cat:
        avisos.append("system prompt sem seção '# CATÁLOGO'")
    negritos = re.findall(r"\*\*[^*\n`]+?\*\*", sp)
    if negritos:
        avisos.append(f"system prompt tem {len(negritos)} trecho(s) com ** (ex.: {negritos[0][:40]}): "
                      "troque por *um asterisco* ou MAIÚSCULAS, porque o modelo imita e o ** sai literal no WhatsApp")

    # 6. Emojis fora da lista declarada
    m = re.search(r"(?:só|somente|apenas) estes:?(.*)$", sp, re.M | re.I)
    if m:
        permitidos = set(EMOJI.findall(m.group(1)))
        usados = set(EMOJI.findall(sp.replace(m.group(0), "")))
        fora = usados - permitidos
        if fora:
            avisos.append("emojis usados fora da lista permitida: " + " ".join(sorted(fora)))
    else:
        avisos.append("não achei a lista fechada de emojis ('só estes: ...') no TOM DE VOZ")

    # 7. Frases citadas nas regras precisam existir no system prompt
    sp_norm = norm(sp)
    for linha in ac.splitlines():
        for frase in re.findall(r"[\"“]([^\"”\n]{25,}?)[\"”]", linha):
            if frase[:1] in " ,.;:)|" or norm(frase) in ACOES or norm(frase) in sp_norm:
                continue
            avisos.append(f"arquivo 3 cita uma frase que não está no system prompt: \"{frase[:70]}\"")

    # 8. Estrutura das regras
    n_regras = len(re.findall(r"^## Regra", ac, re.M))
    if n_regras == 0:
        erros.append("arquivo 3 sem regras ('## Regra ...')")
    if "Transferir conversa para humano" not in ac:
        erros.append("nenhuma regra usa 'Transferir conversa para humano'")
    for bloco in re.split(r"^## (?=Regra)", ac, flags=re.M)[1:]:
        titulo = bloco.splitlines()[0].strip()
        if "Transferir conversa para humano" in bloco and "Atribuir conversa a um administrador" not in bloco:
            avisos.append(f"'{titulo}' transfere, mas não atribui a ninguém (falta 'Atribuir conversa a um administrador')")
        if "Transferir conversa para humano" in bloco:
            quando = bloco.split("**Quando**", 1)[-1].split("**O que a IA deve fazer?**", 1)[0]
            if not re.search(r"[\"“][^\"”\n]{20,}[\"”]", quando):
                avisos.append(f"'{titulo}': o 'Quando' não cita entre aspas a frase fixa que o agente manda ao transferir")
    for perigosa in ("Bloquear contato", "Arquivar"):
        if re.search(rf"^\s*\d+\.\s*{perigosa}", ac, re.M):
            avisos.append(f"uma regra executa '{perigosa}' automaticamente: um erro da IA afeta um cliente real")
    if len(pa.strip()) < 200:
        avisos.append("Prompt da Ação muito curto")
    info.append(f"regras no arquivo 3: {n_regras}")

    # 9. Tamanho e URLs
    info.append(f"system prompt: {len(sp):,} caracteres (~{len(sp) // 4:,} tokens)".replace(",", "."))
    urls = sorted(set(re.findall(r"https?://[^\s)>\]\"']+", sp)))
    webp = [u for u in urls if u.lower().split("?")[0].endswith(".webp")]
    info.append(f"URLs no system prompt: {len(urls)} ({len(webp)} WebP)")
    if webp and re.search(r"whats\s?app|instagram", sp, re.I):
        avisos.append(f"{len(webp)} foto(s) em WebP: WhatsApp e Instagram só aceitam png/jpeg. "
                      "Converta com scripts/converter_fotos.py ou avise o cliente")
    if re.search(r"JSON v[aá]lido|\{\s*\"messages\"|\"attachment\"\s*:|\"template_type\"|\"actions\"\s*:\s*\[", sp):
        erros.append("o prompt pede respostas em JSON (formato de versão anterior da Nextags): "
                     "escreva em texto quando enviar texto, imagem, botões ou carrossel; "
                     "a Nextags converte pelo 'Tipo de resposta da IA'")
    if re.search(r"carross", sp, re.I) and not re.search(
            r"texto do carrossel|mensagem de texto[^\n]{0,160}(antes|logo depois|em seguida)", sp, re.I):
        avisos.append("o prompt usa carrossel, mas não manda enviar a mensagem de Texto logo antes dele, "
                      "na mesma resposta: sem isso, o WhatsApp mostra um '.' no lugar do texto")
    for nome, t_ in textos.items():
        if re.search(r"(ajuda|help|docs)\.nextags\.com\.br", t_):
            avisos.append(f"{nome} tem link para a central de ajuda/documentação da Nextags: o agente "
                          "não deve mandar o cliente final para lá nem seguir páginas de versões anteriores")
    if checar_urls:
        for u in urls:
            status, tipo = testar(u)
            if status != 200:
                erros.append(f"URL não abre ({status}): {u}")
            elif re.search(r"\.(webp|jpe?g|png|gif)(\?|$)", u, re.I) and not tipo.startswith("image/"):
                avisos.append(f"URL de foto não devolve imagem ({tipo}): {u}")
            elif "webp" in tipo.lower() and not u.lower().split("?")[0].endswith(".webp"):
                avisos.append(f"foto chega como WebP mesmo sem a extensão .webp (CDN): converta para JPG: {u}")

    relatorio(erros, avisos, info)


def testar(url):
    # Accept com image/webp imita um navegador/servidor de mensagens: alguns CDNs (ex.: Shopify)
    # só entregam WebP quando o cliente aceita, e o WhatsApp recusa WebP.
    req = urllib.request.Request(url, method="GET", headers={
        "User-Agent": "Mozilla/5.0", "Accept": "image/avif,image/webp,image/*,*/*;q=0.8"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.status, r.headers.get("Content-Type", "")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception as e:  # noqa: BLE001 - relatório, não aborta
        return type(e).__name__, ""


def relatorio(erros, avisos, info):
    for titulo, itens in (("ERROS", erros), ("AVISOS", avisos), ("INFO", info)):
        if itens:
            print(f"\n{titulo}:")
            for i in itens:
                print("  -", i)
    print(f"\nResultado: {len(erros)} erro(s), {len(avisos)} aviso(s)")
    sys.exit(1 if erros else 0)


if __name__ == "__main__":
    main()
