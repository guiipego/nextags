#!/usr/bin/env python3
"""Lista as ferramentas de um servidor MCP (HTTP) sem executar nenhuma.

Uso:
    python3 listar_ferramentas_mcp.py <url> [--header "Authorization: Bearer XXX"] [--json]

Faz só `initialize` e `tools/list` do protocolo MCP: nada é criado ou alterado
no sistema do cliente. Use a saída para escrever a seção FERRAMENTAS do prompt
(quando usar cada uma, ordem, dados obrigatórios).
"""
import json
import sys
import urllib.request


def post(url, corpo, headers):
    req = urllib.request.Request(url, data=json.dumps(corpo).encode(), method="POST", headers=headers)
    with urllib.request.urlopen(req, timeout=30) as r:
        texto = r.read().decode("utf-8", "replace")
        sessao = r.headers.get("Mcp-Session-Id")
    # Respostas podem vir como JSON puro ou como SSE ("data: {...}")
    dados = [l[5:].strip() for l in texto.splitlines() if l.startswith("data:")]
    bruto = dados[-1] if dados else texto.strip()
    return (json.loads(bruto) if bruto else {}), sessao


def main():
    args = sys.argv[1:]
    if not args or args[0].startswith("--"):
        print(__doc__)
        sys.exit(2)
    url = args[0]
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "User-Agent": "Mozilla/5.0",
    }
    for i, a in enumerate(args):
        if a == "--header" and i + 1 < len(args):
            k, _, v = args[i + 1].partition(":")
            headers[k.strip()] = v.strip()

    init, sessao = post(url, {
        "jsonrpc": "2.0", "id": 1, "method": "initialize",
        "params": {"protocolVersion": "2025-03-26", "capabilities": {},
                   "clientInfo": {"name": "nextags-criar-agente-ia", "version": "1.0"}},
    }, headers)
    if sessao:
        headers["Mcp-Session-Id"] = sessao
    try:
        post(url, {"jsonrpc": "2.0", "method": "notifications/initialized"}, headers)
    except Exception:  # noqa: BLE001 - alguns servidores respondem 202 sem corpo
        pass
    lista, _ = post(url, {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}, headers)

    ferramentas = lista.get("result", {}).get("tools", [])
    if "--json" in args:
        print(json.dumps(ferramentas, ensure_ascii=False, indent=2))
        return
    nome_srv = init.get("result", {}).get("serverInfo", {}).get("name", "?")
    print(f"Servidor: {nome_srv} – {len(ferramentas)} ferramenta(s)\n")
    for t in ferramentas:
        esquema = t.get("inputSchema", {})
        obrig = set(esquema.get("required", []))
        print(f"• {t['name']}")
        print(f"  {(t.get('description') or '').strip()}")
        for p, info in esquema.get("properties", {}).items():
            marca = " (obrigatório)" if p in obrig else ""
            print(f"    - {p}{marca}: {info.get('description', info.get('type', ''))}")
        print()
    if lista.get("error"):
        print("Erro do servidor:", lista["error"])


if __name__ == "__main__":
    main()
