# Nextags – skills para o Claude Code

Skills oficiais da Nextags para montar agentes de atendimento com IA usando o Claude Code.

## O que vem aqui

| Skill | Comando | O que faz |
|---|---|---|
| criar-agente-ia | `/nextags:criar-agente-ia` | Faz as perguntas sobre o seu negócio, coleta produtos ou serviços (site, cardápio, planilha) e entrega os 3 textos para colar na Nextags: Mensagem do sistema, Prompt da Ação e Ações de IA |

## Instalar

No Claude Code, digite:

```
/plugin marketplace add guiipego/nextags
/plugin install nextags@nextags
```

Na instalação, escolha **Install for you (user scope)**. Depois, digite `/nextags:criar-agente-ia` ou só peça: "quero criar meu agente de atendimento na Nextags".

## Atualizar

```
/plugin marketplace update nextags
```

Para receber as atualizações sozinho, abra `/plugin` → aba **Marketplaces** → **nextags** → **Enable auto-update**.

## Requisitos

- Claude Code com plano Pro, Max, Team ou Enterprise
- Python 3 instalado (os scripts da skill usam só a biblioteca padrão)

Versão 1.0.0
