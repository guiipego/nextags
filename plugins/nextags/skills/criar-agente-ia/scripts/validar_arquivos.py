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

# Começo das frases fixas de fechamento (references/modos-de-fechamento.md e modelo-system-prompt.md)
FRASES_FECHAMENTO = [
    "Seu pedido foi pré-confirmado e já passei para a nossa equipe",
    "Aqui está o link para finalizar sua compra",
    "Aqui está o link de pagamento do seu pedido",
    "Para concluir, faça o Pix de",
    "Recebi seu comprovante",
    "Seu pedido foi registrado com o número",
    "Sua solicitação de agendamento foi registrada",
    "Seu horário está agendado para",
    "Já passei suas informações para um especialista",
    "Não consegui concluir por aqui agora",
]
FRASES_COBRANCA = FRASES_FECHAMENTO[1:4]
FRASE_PRE_CONFIRMACAO = FRASES_FECHAMENTO[0]
# frases que passam a conversa para a equipe: a regra que as cita precisa transferir
FRASES_TRANSFERE = [FRASE_PRE_CONFIRMACAO, "Recebi seu comprovante", "Não consegui concluir por aqui agora",
                    "Sua solicitação de agendamento foi registrada", "Já passei suas informações para um especialista",
                    "Vou chamar alguém da nossa equipe para continuar seu atendimento"]
# proibição que vale só para um caso ("para dinheiro", "nesses casos", "em encomendas", "se for")
ESCOPO = re.compile(r"\b(?:para|em|com|no|na|nos|nas|pelo|pela)\s+(?:o\s+|a\s+|os\s+|as\s+)?"
                    r"(?:dinheiro|cart[ãa]o|encomendas?|eventos?|pedidos?\s+grandes?)\b"
                    r"|\bness[ea]s?\s+casos?\b|\bse\s+(?:for|o\s+cliente)\b", re.I)

CHAVE_PIX = re.compile(
    r"pix[^\n]{0,60}?(?:[\w.+-]+@[\w-]+(?:\.[\w-]+)+"      # e-mail
    r"|\d{3}\.?\d{3}\.?\d{3}-?\d{2}"                       # CPF
    r"|\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}"                # CNPJ
    r"|\(?\d{2}\)?\s?9?\d{4}-?\d{4}"                        # telefone
    r"|[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})",  # aleatória
    re.I)
LINK_PAGAMENTO = re.compile(
    r"https?://[^\s)>\]\"']*(?:mpago\.la|mercadopago|pag\.ae|pagseguro|pagbank|infinitepay|asaas|"
    r"sumup|stripe|paypal|picpay|cielo|getnet|checkout|/pay|pagar|pagamento)", re.I)


def norm(texto):
    texto = unicodedata.normalize("NFKC", texto).casefold()
    return re.sub(r"\s+", " ", texto).strip(" .,!?;:\"'“”")


def citacoes(texto):
    """Trechos entre aspas, pareando as aspas na ordem em que aparecem (retas e tipográficas)."""
    return re.findall(r'"([^"\n]*)"', texto) + re.findall(r"“([^”\n]*)”", texto)


def tabela_de_links_pendente(texto):
    """Uma tabela cujo cabeçalho fala de link e que tem alguma linha [A DEFINIR]."""
    cabecalho = None
    for linha in texto.splitlines():
        if not linha.lstrip().startswith("|"):
            cabecalho = None
            continue
        if cabecalho is None:
            cabecalho = linha
        elif "link" in cabecalho.lower() and "[A DEFINIR]" in linha:
            return True
    return False


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

    # Regras do arquivo 3: cada bloco "## ..." com **Quando** (título, "Quando" e ações)
    regras = []
    for bloco in re.split(r"^#{2,3} ", ac, flags=re.M)[1:]:
        titulo = bloco.splitlines()[0].strip()
        m_quando = re.search(r"\*\*Quando:?\*\*:?", bloco)
        if not m_quando:
            if re.match(r"Regra\b", titulo):
                avisos.append(f"'{titulo}' não tem a parte **Quando** reconhecível: o validador não confere essa regra")
            continue
        quando, _, acoes = bloco[m_quando.end():].partition("**O que a IA deve fazer?**")
        regras.append({"titulo": titulo, "quando": quando, "acoes": acoes,
                       "transfere": "Transferir conversa para humano" in acoes})
    topo = "\n".join(l for l in ac.splitlines() if l.startswith("As regras usam"))

    # 7. Frases citadas no "Quando" das regras (e na lista do topo) precisam existir no system prompt
    sp_norm = norm(sp)
    vistas = set()
    for texto in [r["quando"] for r in regras] + [topo]:
        for frase in citacoes(texto):
            if (len(frase) < 25 or frase[:1] in " ,.;:)|" or "→" in frase or norm(frase) in ACOES
                    or norm(frase) in sp_norm or frase in vistas):
                continue
            vistas.add(frase)
            avisos.append(f"arquivo 3 cita uma frase que não está no system prompt: \"{frase[:70]}\"")

    # 8. Estrutura das regras
    n_regras = len(regras)
    if n_regras == 0:
        erros.append("arquivo 3 sem regras (cada uma com título '## Regra N – nome' e **Quando**)")
    if not any(r["transfere"] for r in regras):
        erros.append("nenhuma regra usa 'Transferir conversa para humano'")
    for r in regras:
        if r["transfere"] and "Atribuir conversa a um administrador" not in r["acoes"]:
            avisos.append(f"'{r['titulo']}' transfere, mas não atribui a ninguém (falta 'Atribuir conversa a um administrador')")
        if r["transfere"] and not any(len(c) >= 20 for c in citacoes(r["quando"])):
            avisos.append(f"'{r['titulo']}': o 'Quando' não cita entre aspas a frase fixa que o agente manda ao transferir")
    for perigosa in ("Bloquear contato", "Arquivar"):
        if re.search(rf"^\s*\d+\.\s*{perigosa}", ac, re.M):
            avisos.append(f"uma regra executa '{perigosa}' automaticamente: um erro da IA afeta um cliente real")
    if len(pa.strip()) < 200:
        avisos.append("Prompt da Ação muito curto")
    info.append(f"regras no arquivo 3: {n_regras}")

    # 9. Modo de fechamento (references/modos-de-fechamento.md)
    quandos = norm(" ".join(r["quando"] for r in regras))
    quandos_transferem = norm(" ".join(r["quando"] for r in regras if r["transfere"]))
    for frase in dict.fromkeys(FRASES_FECHAMENTO + FRASES_TRANSFERE):
        if norm(frase) not in sp_norm:
            continue
        if norm(frase) not in quandos:
            avisos.append(f"o system prompt manda a frase fixa \"{frase}\", mas o \"Quando\" de nenhuma regra do "
                          "arquivo 3 a cita: a regra desse fechamento não vai disparar")
        elif frase in FRASES_TRANSFERE and norm(frase) not in quandos_transferem:
            avisos.append(f"a frase fixa \"{frase}\" passa a conversa para a equipe, mas nenhuma regra que a cita tem "
                          "'Transferir conversa para humano': a conversa não chega a ninguém")
    cobra = any(norm(f) in sp_norm for f in FRASES_COBRANCA)
    manda_pix = norm("Para concluir, faça o Pix de") in sp_norm
    manda_link = any(norm(f) in sp_norm for f in FRASES_COBRANCA[:2])
    tem_chave = CHAVE_PIX.search(sp)
    tem_link = LINK_PAGAMENTO.search(sp)
    # o que a regra de Pagamento proíbe mandar em todo pedido (proibição de um caso só não conta)
    regra_pag = "\n".join(l for l in sp.splitlines() if re.match(r"\s*(?:\d+\.|[-•])\s*\*{1,2}Pagamento", l))
    proibidos = set()
    for m_ in re.finditer(r"(n[ãa]o|nunca)\s+(envie|mande|passe)\b", regra_pag, re.I):
        fim_frase = min([i for i in (regra_pag.find(s, m_.end()) for s in (". ", "; ", ": ", "\n")) if i >= 0]
                        or [len(regra_pag)])
        trecho = regra_pag[m_.end():fim_frase]
        inicio = max(regra_pag.rfind(s, 0, m_.start()) for s in (". ", "; ", ": ", "\n")) + 1
        janela = regra_pag[max(inicio, m_.start() - 40):m_.start()]
        if (ESCOPO.search(janela) or re.search(r"\boutr[oa]s?\b", trecho, re.I) or re.search(
                r"\bantes\s+(?:de\s+o\s+cliente\s+aprovar|d[oa]\s+(?:último\s+)?resumo|de\s+fechar|da\s+aprova)",
                trecho, re.I)):
            continue
        if re.search(r"chave\s+pix", trecho, re.I):
            proibidos.add("a chave Pix")
        if re.search(r"link\s+de\s+pagamento", trecho, re.I):
            proibidos.add("link de pagamento")
    if ("a chave Pix" in proibidos and manda_pix) or ("link de pagamento" in proibidos and manda_link):
        avisos.append("a regra de Pagamento proíbe mandar " + " e ".join(sorted(proibidos))
                      + ", mas a etapa de fechamento do próprio prompt manda. Se a proibição vale para todo pedido, é "
                      "sobra de outro modo: use a regra de Pagamento do modo combinado (modos-de-fechamento.md); "
                      "se vale só para um caso, diga qual (ex.: \"para dinheiro ou cartão\")")
    elif not cobra and (("a chave Pix" in proibidos and tem_chave) or ("link de pagamento" in proibidos and tem_link)):
        avisos.append("a regra de Pagamento proíbe mandar " + " e ".join(sorted(proibidos)) + ", mas o prompt tem "
                      + ("uma chave Pix" if tem_chave else "um link de pagamento")
                      + ": se o agente deve cobrar, use o texto do modo 3 ou 4 (modos-de-fechamento.md); "
                      "se não, tire a chave ou o link do prompt")
    if manda_pix:
        if re.search(r"(?:chave(?:\s+pix)?|\bpix\s*:)\s*(?:\([^)]*\)\s*)?:?\s*(?:(?:cpf|cnpj|e-?mail|telefone|celular"
                     r"|aleat[óo]ria)\s*)?:?\s*\[A DEFINIR\]", sp, re.I):
            erros.append("o agente fecha por Pix, mas a chave Pix está [A DEFINIR]: ele não tem o que mandar. "
                         "Use o modo 1 até ter a chave (modos-de-fechamento.md, seção 1)")
        elif re.search(r"(?:em\s+nome\s+de|recebedor|favorecido)\s*:?\s*\[A DEFINIR\]", sp, re.I):
            erros.append("o agente fecha por Pix, mas o recebedor (o nome que aparece para quem paga) está [A DEFINIR]. "
                         "Use o modo 1 até ter a chave e o recebedor (modos-de-fechamento.md, seção 1)")
        elif not tem_chave:
            avisos.append("o fechamento por Pix está no prompt, mas não achei a chave Pix "
                          "(e-mail, telefone, CPF, CNPJ ou aleatória) perto da palavra Pix")
        exemplos = secao(sp, "EXEMPLOS")
        for m_ in re.finditer(r"\*Pagamento:\*\s*Pix", exemplos, re.I):
            depois = exemplos[m_.end():]
            proximo = re.search(r"^#{2,3} |\*Pagamento:\*", depois, re.M)
            resto = norm(depois[:proximo.start()] if proximo else depois)
            i_pix = resto.find(norm("Para concluir, faça o Pix de"))
            i_pre = resto.find(norm(FRASE_PRE_CONFIRMACAO))
            if i_pre != -1 and (i_pix == -1 or i_pre < i_pix):
                avisos.append("nos EXEMPLOS, um pedido pago por Pix termina na mensagem de pré-confirmação: é sobra do "
                              "modo 1, e o agente imita os exemplos")
                break
    if norm("Aqui está o link de pagamento do seu pedido") in sp_norm:
        if re.search(r"links?\s+de\s+pagamento[^\n\[]{0,40}\[A DEFINIR\]", sp, re.I) or tabela_de_links_pendente(sp):
            erros.append("o agente fecha por link de pagamento, mas há link [A DEFINIR]: ele não tem o que mandar. "
                         "Use o modo 1 até ter os links (modos-de-fechamento.md, seção 1)")
        elif not tem_link and not re.search(r"link\s+de\s+pagamento[^\n]{0,40}https?://", sp, re.I):
            avisos.append("o fechamento por link de pagamento está no prompt, mas não achei nenhum link de pagamento")
    if cobra:
        if not re.search(r"(nunca|n[ãa]o)\s+confirme\s+(o\s+)?pagamento", sp, re.I):
            avisos.append("o agente cobra (link ou Pix), mas o prompt não proíbe confirmar pagamento por comprovante ou print")
        if not re.search(r"(nunca|n[ãa]o)\s+pe[çc]a[^.\n]{0,60}cart[ãa]o", sp, re.I):
            avisos.append("o agente cobra (link ou Pix), mas o prompt não proíbe pedir dados de cartão")
        if (re.search(r"taxa[^\n]{0,40}\[A DEFINIR\]", sp, re.I)
                and norm(FRASE_PRE_CONFIRMACAO) not in sp_norm):
            avisos.append("o agente cobra, a taxa de entrega está [A DEFINIR] e o prompt não tem a mensagem de "
                          "pré-confirmação para o pedido sem Total fechado (modos-de-fechamento.md, seção 2)")
    linhas_pa = [l for l in pa.splitlines() if "Exceção" in l or "não transfere:" in l]
    titulos = norm(" ".join(r["titulo"] for r in regras))
    for nome_regra in dict.fromkeys(c for l in linhas_pa for c in citacoes(l)):
        if norm(nome_regra) not in titulos:
            avisos.append(f"o Prompt da Ação cita a regra \"{nome_regra}\", que não está nos títulos do arquivo 3 "
                          "(o nome da regra principal muda com o modo de fechamento)")
    m_exc = re.search(r"Exceção:?\s*se\s+(.*?)\s+disparar", pa)
    for nome_regra in citacoes(m_exc.group(1)) if m_exc else []:
        regra = next((r for r in regras if norm(nome_regra) and norm(nome_regra) in norm(r["titulo"])), None)
        if regra and not regra["transfere"]:
            avisos.append(f"a exceção do Prompt da Ação cita \"{nome_regra}\", que não transfere: ela vai na linha "
                          "das regras que não transferem (modelo-prompt-da-acao.md)")

    # 10. Tamanho e URLs
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
