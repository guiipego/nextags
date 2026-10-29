# Nextags – skills para o Claude Code

Skills oficiais da Nextags para montar agentes de atendimento com IA usando o Claude Code.

## O que vem aqui

| Skill | Comando | O que faz |
|---|---|---|
| criar-agente-ia | `/nextags:criar-agente-ia` | Faz as perguntas sobre o seu negócio, coleta produtos ou serviços (site, cardápio, planilha) e entrega os 3 textos para colar na Nextags: Mensagem do sistema, Prompt da Ação e Ações de IA. Você escolhe como a venda termina: o agente pré-confirma e passa para a equipe, ou fecha sozinho com Pix, link de pagamento, checkout da loja ou registro no sistema. Também ajusta o agente depois dos seus testes |

## Instalar

No terminal:

```
claude plugin marketplace add guiipego/nextags
claude plugin install nextags@nextags
```

Depois, no Claude Code, digite `/nextags:criar-agente-ia` ou só peça: "quero criar meu agente de atendimento na Nextags".

## Atualizar

```
claude plugin marketplace update nextags
claude plugin update nextags@nextags
```

Depois, feche e abra o Claude Code (ou digite `/reload-plugins` numa sessão aberta). Para receber as atualizações sozinho, abra `/plugin` → aba **Marketplaces** → **nextags** → **Enable auto-update**.

## Requisitos

- Claude Code com plano Pro, Max, Team ou Enterprise
- Python 3 instalado (os scripts da skill usam só a biblioteca padrão)

## Novidades

- **1.2.0**: o dono do negócio escolhe como a venda (ou o agendamento) termina: o agente pré-confirma e passa para a equipe, ou fecha sozinho com o link de checkout da loja (MCP/API), um link de pagamento, a chave Pix (a equipe confere o comprovante) ou o registro direto no sistema; regras de segurança para cobrar (só links e chaves cadastrados, só o total aprovado, nunca dados de cartão, nunca confirmar pagamento por comprovante); regras prontas nas Ações de IA para cada modo, inclusive comprovante recebido e problema no fechamento (erro no link, no checkout ou no Pix); passo a passo para trocar o jeito de fechar de um agente pronto; o validador avisa quando o prompt mistura dois jeitos de fechar.
- **1.1.0**: a skill passa a ser a única fonte de instruções sobre a Nextags (não consulta mais a central de ajuda, que tem páginas de versões anteriores, como as de respostas em JSON); regras de formatação de WhatsApp e de carrossel (texto + cards); etapa de ajustes depois dos testes, com tabela de sintomas; conversão de fotos PNG/WebP para JPG com fundo branco.
- **1.0.0**: primeira versão.
