# Como a Nextags organiza um agente de IA

Esta referência resume, na versão atual da plataforma, tudo o que importa para montar e ajustar o agente: as 3 partes da configuração, as ações, os campos, os tipos de resposta, os limites por canal e os sintomas mais comuns nos testes. Use só ela. Não consulte a central de ajuda nem a documentação da Nextags, porque parte das páginas de lá é de versões anteriores (veja a seção 12 e "Fonte da verdade" no SKILL.md).

## Sumário
1. As 3 partes da configuração
2. Ações disponíveis (e quando usar cada uma)
3. Prompt da ação (padrão da plataforma)
4. Campos do sistema úteis no prompt
5. Campos personalizados (CUFs)
6. Tipo de resposta da IA (texto, imagem, botões, carrossel) e limites por canal
7. Modelo de IA
8. Ferramentas de IA do IA Hub (Arquivos, leitores, Web Search, Funções, MCP)
9. Configurações do modelo (modelo, max tokens, reasoning effort, verbosity)
10. Palavras-chave
11. Sintomas nos testes: causa e correção
12. Versões anteriores: o que não usar

---

## 1. As 3 partes da configuração

**Mensagem do sistema (Prompt).** Caixa de texto com as instruções gerais do agente. Há também o botão "Adicionar mensagens ao prompt", que serve para dividir textos muito longos (ex.: o catálogo numa mensagem separada).

**Configurações do agente**, na mesma área:
- **Tipo de resposta da IA** (Texto, Imagem | Vídeo | Áudio | Arquivo, Texto + Botões, Carrossel): seção 6;
- **Modelo, Max tokens, Reasoning effort e Verbosity:** seção 9;
- **Ferramentas de IA** ligadas (Image Reader, Document Reader, Web Search, Arquivos, Funções, servidores MCP) e websites autorizados para a pesquisa: seção 8.

**Ações de IA.** "Permita que a IA execute ações automaticamente enquanto conversa com os clientes." São **regras**, e cada uma tem:
- um título;
- **Quando**: descrição em texto livre da situação que dispara a regra;
- **O que a IA deve fazer?**: lista ordenada de ações (Ação 1, Ação 2...), cada uma escolhida de um menu e com sua configuração (etiqueta, campo, administrador etc.).

**Prompt da ação.** Fica no ícone de ajustes das Ações de IA. São as instruções gerais que o modelo usa para decidir quais regras disparar e como preencher os valores. Vale para todas as regras.

O texto do "Quando" é lido pelo modelo, junto com a conversa e a resposta atual do agente, para decidir se a regra dispara (a plataforma diz que "várias regras podem disparar na mesma resposta"). Por isso:
- o "Quando" precisa descrever algo **observável na conversa** (o cliente disse X, e o agente respondeu Y);
- a resposta do agente nos momentos-chave precisa ser **fixa e reconhecível**, como a frase de transferência;
- o "Quando" também deve dizer o que **não** vale (ex.: "não vale se o cliente só pediu o resumo").

## 2. Ações disponíveis

| Ação | Para que serve | Recomendação |
|---|---|---|
| Enviar Fluxo | Dispara um fluxo pronto da Nextags | Use se o cliente já tiver um fluxo (ex.: cardápio em PDF, pesquisa de satisfação, agendamento) |
| Atribuir conversa a um administrador | Entrega a conversa a uma pessoa específica | Junto com "Transferir para humano", para a pessoa certa receber |
| Remover atribuição | Tira a pessoa atribuída | Uso manual da equipe; raramente na IA |
| Transferir conversa para humano | Pausa a IA e passa para atendimento humano | Ação central de toda regra de transferência |
| Adicionar Etiqueta | Marca o contato | Toda regra deve etiquetar, para a equipe filtrar e medir |
| Remover Etiqueta | Tira uma etiqueta | Útil para tirar uma etiqueta de etapa (ex.: "Montando pedido") quando o contato avança |
| Definir Campo Personalizado | Salva um valor no contato (a IA preenche a partir da conversa) | Para guardar resumo do pedido, valor, endereço, motivo da transferência |
| Limpar Campo Personalizado | Apaga um campo | Raramente necessário; campos são sobrescritos |
| Seguir | Coloca o contato em acompanhamento | Para recuperar conversa abandonada, se o cliente quiser |
| Remover do acompanhamento | Tira do acompanhamento | Junto com a pré-confirmação, se usar "Seguir" |
| Transferir conversa para bot | Devolve a conversa para a IA | Uso da equipe ao terminar o atendimento humano |
| Arquivar | Arquiva a conversa | **Não** automatize: um erro some com um cliente real |
| Bloquear contato | Bloqueia o contato | **Não** automatize: um erro bloqueia um cliente real |

Ordem recomendada das ações numa regra de transferência: Adicionar Etiqueta → Definir Campo(s) → Transferir conversa para humano → Atribuir conversa a um administrador.

## 3. Prompt da ação (padrão da plataforma)

Este é o texto que vem por padrão (em inglês):

```
- Match a rule only when its description is clearly satisfied by the conversation.
- Do not match a rule based on assumptions.
- Multiple rules may match in the same response.
- When a matched rule requires values from the conversation, populate them using information available in the conversation.
- Never invent missing values.
- Never mention rule IDs, rule matching, structured output, or internal configuration to the customer.
```

A skill entrega uma versão em português ajustada ao negócio, que mantém esses princípios e acrescenta: aprovação só do último resumo, não repetir transferência para o mesmo assunto, formato de dinheiro por tipo de campo e regras que podem ou não disparar juntas. Veja `modelo-prompt-da-acao.md`.

## 4. Campos do sistema úteis no prompt

A sintaxe é `{{nome_do_campo}}`; a plataforma troca o nome pelo valor. Os mais úteis para um agente de atendimento:

| Campo | O que traz | Uso no prompt |
|---|---|---|
| `{{current_user_time}}` | Hora local atual do usuário, pelo fuso horário | Bom dia/boa tarde, saber se a loja está aberta, avisar perto do fechamento |
| `{{first_name}}` | Primeiro nome do usuário | Cumprimentar e confirmar o nome do pedido em vez de perguntar |
| `{{full_name}}` | Nome completo | Pedidos e agendamentos formais |
| `{{phone}}` | Telefone do usuário | Geralmente não precisa ir para o prompt: a equipe já tem. Diga ao agente para não pedir telefone |
| `{{user_city}}` / `{{user_state}}` | Cidade e estado | Pré-checar área de entrega (é só um palpite; confirme o endereço) |
| `{{timezone}}` | Fuso horário | Normalmente dispensável se usar `current_user_time` |
| `{{user_tags}}` | Etiquetas do contato | Use com cuidado: etiquetas antigas podem confundir o agente |
| `{{last_interaction}}` / `{{last_seen}}` | Última interação | Retomar a conversa ("que bom te ver de novo") |
| `{{user_notes}}` / `{{last_user_note}}` | Notas da equipe sobre o contato | Contexto de atendimentos anteriores, se a equipe usa notas |
| `{{chat_history}}` | Últimas 50 mensagens | Normalmente o agente já tem o histórico; só use se a Nextags pedir |
| `{{account_name}}` | Nome da conta | Dispensável se o nome do negócio já está no prompt |

Há também campos de e-commerce (Catálogo META: `{{cart_total}}`, `{{order_products}}` etc.) e de agendamento (`{{booking_date}}`, `{{booking_link}}`), que só servem para quem usa esses recursos da Nextags.

**Onde colocar:** numa seção "CONTEXTO DESTE ATENDIMENTO" no **final** do system prompt. A parte fixa e grande (regras e catálogo) fica igual em todas as conversas, o que favorece o cache de prompt do modelo. Diga ao agente que, se um valor vier vazio ou ainda entre chaves, ele deve tratar como "não disponível".

## 5. Campos personalizados (CUFs)

São a "memória permanente" do contato: ficam salvos entre conversas, diferente do histórico de uma sessão.
- **Criar:** Fluxo → Campos Personalizados → Adicionar → nome, tipo e descrição.
- **Tipos:** Texto, Número, Data, Data e hora, Verdadeiro/Falso, Texto longo. O limite é de 10.000 caracteres por campo; os campos de conta de texto longo vão até 16 milhões.
- **No prompt:** `{{nome_do_campo}}`.
- **Preencher:** pela ação "Definir Campo Personalizado" numa regra; a IA preenche com dados da conversa.

Boas práticas:
- Nomes em snake_case sem acento (`resumo_pedido`, `endereco_entrega`), idênticos no arquivo 1 (onde são lidos) e no arquivo 3 (onde são gravados). Peça ao cliente para conferir como a Nextags salvou o nome e ajustar se for diferente.
- Campos do tipo Número: valor só com o número e ponto decimal (47.30). Campos de texto: formato brasileiro (47,30).
- Um campo que só faz sentido em alguns casos (ex.: endereço só na entrega) vai numa regra separada, com um "Quando" específico. Assim, um caso diferente não apaga o valor salvo.

Campos que costumam valer a pena:

| Campo | Tipo | Gravado por | Lido pelo agente para |
|---|---|---|---|
| resumo_pedido | Texto | Regra de pré-confirmação | Atender "o mesmo de antes" |
| valor_pedido | Número | Regra de pré-confirmação | Relatórios (não precisa ir ao prompt) |
| endereco_entrega | Texto | Regra só de entrega | Oferecer o endereço da última vez |
| motivo_transferencia | Texto | Regras de transferência antecipada | A equipe saber o motivo (não precisa ir ao prompt) |
| servico_interesse / data_preferida | Texto | Regra de agendamento | Retomar o agendamento |

## 6. Tipo de resposta da IA e limites por canal

Na configuração do agente, o campo **"Tipo de resposta da IA"** é de escolha múltipla:
- **Texto:** sempre ligado.
- **Imagem | Vídeo | Áudio | Arquivo:** o agente envia mídia de verdade (a foto chega como imagem, não como link).
- **Texto + Botões:** mensagem com botões clicáveis.
- **Carrossel:** até **10 cards** roláveis para o lado, cada um com foto, um texto curto e, se quiser, um botão de link.

A plataforma faz a conversão por trás: o prompt **não** precisa (e não deve) pedir JSON nem formato técnico. Basta marcar os tipos que o agente pode usar e dizer no prompt, em texto, **quando** usar cada um (veja a seção 12).

**Padrão recomendado: ligar os 4 tipos** (Texto, Imagem | Vídeo | Áudio | Arquivo, Texto + Botões e Carrossel) e, no prompt, dizer quando usar cada um. Desligue um tipo só se o cliente pedir, e aí tire do prompt a instrução correspondente.

Quando usar cada tipo:
- **Tem fotos de produto ou serviço?** Use **Imagem**. No prompt: "envie a foto como imagem, usando a URL do campo Foto do catálogo, com a legenda *Nome* e o preço". O texto da resposta pode ir na própria legenda (uma mensagem só, em vez de foto + texto). Sem esse tipo ligado, a foto só sai como link no texto.
- **Carrossel:** para mostrar de 2 a 10 itens de uma vez (o limite é 10 cards; de 3 a 6 costuma ficar melhor). Cada card tem a foto, um texto simples "Nome – R$ X,XX" (até 60 caracteres, sem asterisco) e, se houver link, um botão de URL (ex.: "Ver produto"). **O carrossel sempre vai com uma mensagem de Texto enviada logo antes, na mesma resposta** (o "texto do carrossel"): a Nextags junta as duas, e no WhatsApp o texto aparece em cima dos cards, como uma mensagem só. Sem essa mensagem de Texto, ou com o texto colocado dentro do carrossel, o WhatsApp mostra um "." no lugar do texto. O texto do carrossel diz o que foi separado e termina com a pergunta seguinte, e pode ter um 👇 no fim apontando para os cards.
- **Texto + Botões:** para escolhas fechadas (Retirada / Entrega; Confirmar / Alterar). Use no máximo 3 botões com títulos curtos (até ~20 caracteres, limite do WhatsApp). Um clique num botão vale como resposta do cliente. Se o botão for de confirmação do resumo, ele conta como aprovação para a regra de pré-confirmação.
- **Arquivo:** para mandar cardápio em PDF, tabela de preços ou contrato, quando houver URL pública do arquivo.

Limites oficiais por canal (doc "Tipos de arquivos e limites nos canais"):

| Canal | Imagem | Vídeo | Áudio | Documento |
|---|---|---|---|---|
| WhatsApp | **png, jpeg, até 5 MB** | 3gp, mp4, até 16 MB | aac, m4a, ogg, mp4, mp3, amr, até 16 MB | qualquer, até 25 MB |
| Instagram | png, jpeg, gif, até 8 MB | mp4, ogg, avi, mov, webm, até 25 MB | aac, m4a, wav, mp4, até 25 MB | não aceita |
| Messenger | png, jpeg, gif, até 25 MB | mp4, ogg, avi, mov, webm, até 25 MB | aac, m4a, wav, mp4, até 25 MB | qualquer, até 25 MB |
| Telegram | png, jpeg, webp, até 5 MB | mp4, até 20 MB | mpeg, até 20 MB | qualquer, até 20 MB |

**WebP não está na lista do WhatsApp nem do Instagram.** No teste, aparece o erro "Media upload error WebP image uploads are not currently supported" e a foto não chega, mesmo com o tipo Imagem ligado. Fotos WebP são muito comuns em sites WordPress. Também acontece com fotos que viram WebP no caminho: o CDN da Shopify, por exemplo, entrega WebP para PNG com fundo transparente, mesmo com `format=jpg` ou `format=pjpg` na URL. O caminho é converter para JPG com fundo branco e hospedar numa URL pública (`scripts/converter_fotos.py`, com `--incluir-png` quando houver PNG; ver `coleta-catalogo.md`, seção 4). Confira também o peso: foto acima de 5 MB não vai no WhatsApp.

## 7. Modelo de IA

A Nextags conecta vários provedores (OpenAI, Google Gemini, Claude, xAI e DeepSeek); o mais comum é a OpenAI (GPT). O que funciona melhor com todos eles:
- seções com títulos (`#`) e regras numeradas;
- prioridades explícitas ("esta regra vale acima das outras");
- nenhuma contradição entre regras e exemplos, porque o modelo imita os exemplos;
- formato de saída mostrado com um modelo exato;
- limites claros de tamanho de mensagem.

## 8. Ferramentas de IA do IA Hub

No IA Hub, a aba **Ferramentas de IA** tem três áreas: **Arquivos**, **Funções de IA** e **Servidores MCP**. Na configuração do agente, o campo "Ferramentas de IA" é onde se liga cada uma. Também aparecem ali os leitores nativos (**Image Reader**, **Document Reader**) e a **Web Search**, que tem uma lista de "Websites autorizados para a ferramenta de Pesquisa Web".

Na entrevista, pergunte quais estão ligadas ou podem ser ligadas, e escreva no system prompt **quando** o agente deve usar cada uma. Uma ferramenta ligada sem instrução no prompt é usada ao acaso ou ignorada.

| Ferramenta | O que faz | Quando vale a pena | O que escrever no prompt |
|---|---|---|---|
| **Arquivos** | Upload de PDFs, planilhas etc.; a IA consulta antes de responder | FAQ grande, políticas, manual técnico, tabela de preços enorme | "Para dúvidas sobre X, consulte os arquivos da base antes de responder; se não encontrar, diga que vai confirmar com a equipe." |
| **Image Reader** | A IA entende imagens que o cliente envia | Cliente manda print do cardápio, foto do produto com defeito, foto do local para orçamento, comprovante | Dizer o que fazer com cada tipo de imagem. Comprovante de pagamento: **nunca** confirme o pagamento; agradeça e diga que a equipe confere |
| **Document Reader** | A IA lê PDFs e documentos que o cliente envia | Pedido de orçamento em PDF, lista de materiais, receita, guia de exame | Resumir e usar o conteúdo; em saúde, nunca interpretar exame ou receita |
| **Web Search** | A IA pesquisa na web, limitada aos sites autorizados | Catálogo muda muito e está no site do cliente; detalhes/ingredientes nas páginas do produto | Autorize só o domínio do próprio negócio. "Use a pesquisa só no site X, para detalhes de produto. Preço e disponibilidade são os do catálogo." |
| **Funções de IA** | Funções que a IA chama, como `connect_user_to_human` (transferir para humano) ou disparar um fluxo pela intenção | Quando o cliente prefere que a própria IA dispare a ação no meio da resposta | Ver o aviso logo abaixo |
| **Servidores MCP** | A IA consulta e opera sistemas externos: e-commerce (Shopify etc.: produtos, pedidos, carrinho abandonado), agenda | Loja online com estoque e pedidos; agenda real | Ver a subseção MCP abaixo |

**Aviso sobre transferência em dobro.** Transferir pela função `connect_user_to_human` e por uma regra de Ações de IA ao mesmo tempo pode transferir duas vezes, ou transferir sem etiqueta e sem campos. Escolha um mecanismo principal. A skill recomenda as **Ações de IA**, porque etiquetam, salvam campos e atribuem na mesma regra. Se o cliente já usa a função, o prompt precisa dizer exatamente quando chamá-la, e as regras de transferência das Ações de IA saem.

### Servidores MCP

Um servidor MCP expõe **ferramentas** com nome, descrição e parâmetros. Para escrever bem o prompt, você precisa da lista dessas ferramentas:
- **Com acesso à internet (Claude Code):** `python3 scripts/listar_ferramentas_mcp.py <URL do servidor>` lista as ferramentas sem executar nenhuma (usa só os métodos `initialize` e `tools/list` do protocolo).
- **Sem acesso:** peça ao cliente o nome e a descrição de cada ferramenta ou um print da tela do servidor na Nextags.

Exemplo real: o servidor `agenda_nextags` (`https://nextags.app.br/mcp/nextags/agenda`) tem 4 ferramentas:
- `Consultar_Agenda` (startTime, endTime em ISO 8601) → horários livres de 30 min;
- `Criar_Agendamento` (start, attendeeName, attendeeEmail, attendeePhone com DDI, guests) → reunião de 30 min com Google Meet;
- `Buscar_Agendamentos` (attendeeEmail) → agendamentos futuros com uid;
- `Reagendar` (bookingUid, newStart, reason).

Como escrever as instruções de MCP no system prompt (seção FERRAMENTAS do modelo):
1. **Para que serve e quando usar** cada ferramenta, em linguagem de negócio ("para ver horários livres, use Consultar_Agenda").
2. **Ordem obrigatória:** consultar antes de criar (Consultar_Agenda → oferecer 2 ou 3 horários → o cliente escolhe → confirmar os dados → Criar_Agendamento). Para reagendar, buscar antes.
3. **Confirmação antes de ações que criam ou alteram algo:** o agente mostra o resumo e só chama a ferramenta depois do "sim" do cliente.
4. **Dados obrigatórios:** quais pedir ao cliente (ex.: e-mail) e quais já existem (telefone: `{{phone}}`; nome: `{{first_name}}`). Datas em ISO 8601 calculadas a partir de `{{current_user_time}}`, com atenção ao fuso.
5. **Sucesso e erro:** só diga "agendado" depois que a ferramenta retornar sucesso, e repita data, hora e link. Se der erro ou não houver horário, diga isso e ofereça transferir para a equipe.
6. **Limites:** o que a ferramenta não faz (ex.: cancelar) vai para o humano.

Para e-commerce (Shopify e similares), o padrão é o mesmo: buscar produto, estoque e preço **na ferramenta**, e não num catálogo colado no prompt, que pode ficar velho. Consultar status de pedido pede um dado que identifique o cliente (número do pedido, e-mail) e nunca expõe pedidos de outra pessoa. Com MCP de catálogo, o CATÁLOGO do prompt pode ser só um resumo das categorias.

## 9. Configurações do modelo

Ficam na mesma tela do tipo de resposta. **Configuração padrão recomendada** (para quem usa OpenAI; é a que a Nextags indica como melhor custo-benefício):

| Configuração | Valor padrão | Por quê |
|---|---|---|
| Tipo de resposta da IA | Texto + Imagem/Vídeo/Áudio/Arquivo + Texto + Botões + Carrossel | O agente pode mandar foto de verdade, botões e carrossel; o prompt diz quando usar cada um |
| Modelo (OpenAI) | **GPT-6 Luna** | Ótimo custo-benefício para atendimento com catálogo e regras |
| Max tokens | **32768** | Folga para respostas com resumo, fotos e carrossel |
| Reasoning effort | **Média** | Ajuda nas contas do resumo e em seguir as regras; Baixa erra mais em pedidos com vários itens |
| Verbosity | **Baixa** | Combina com mensagens curtas de WhatsApp e com a regra de no máximo 3 parágrafos |

Recomende sempre esse padrão no checklist de entrega. Se o cliente usa outro provedor (Gemini, Claude, xAI, DeepSeek), mantenha os mesmos tipos de resposta, Reasoning Média e Verbosity Baixa (quando existirem) e escolha o modelo de custo-benefício equivalente desse provedor.

Se o cliente mudar o modelo depois, peça para repetir os testes da Etapa 5 da skill: modelos diferentes seguem as regras de jeitos diferentes.

## 10. Palavras-chave

O IA Hub também tem **Palavras-chave**: palavras ou frases que disparam um fluxo ou uma mensagem pronta, sem passar pela IA. Se o cliente usa palavras-chave, confira se elas não brigam com o agente (ex.: a palavra "cardápio" disparar um fluxo enquanto o agente também responde). Na dúvida, deixe o agente cuidar da conversa e use palavras-chave só para campanhas específicas.

## 11. Sintomas nos testes: causa e correção

Quando o usuário voltar dos testes com um problema, procure aqui antes de qualquer outra coisa. Corrija o arquivo indicado, rode o validador e diga ao usuário qual arquivo recolar.

| O que aparece no teste | Causa | Correção | Arquivo |
|---|---|---|---|
| Carrossel chega com um "." no lugar do texto | O carrossel foi enviado sem a mensagem de Texto antes, ou com o texto dentro do carrossel | Instruir: "envie, na mesma resposta, uma mensagem de Texto e logo depois a mensagem de Carrossel"; nada de texto dentro dos cards além do "Nome – R$ X,XX" | 1 |
| "Media upload error WebP image uploads are not currently supported" | Foto em WebP (ou PNG que o CDN entrega como WebP) | Converter para JPG com fundo branco (`converter_fotos.py --incluir-png`) e trocar as URLs no catálogo | 1 |
| Foto chega como link, não como imagem | Tipo de resposta Imagem desligado, ou o prompt manda colar a URL no texto | Ligar Imagem no agente e instruir "envie a foto como imagem" (variante 1 do modelo) | config. e 1 |
| Aparecem asteriscos duplos, "#" ou "\|" soltos | O prompt usa Markdown de site (o modelo imita) | Tirar `**`, títulos e tabelas das partes que o agente copia; regra de formatação de WhatsApp | 1 |
| Mensagens em bloco corrido, sem destaque | Falta a seção FORMATAÇÃO DAS MENSAGENS | Incluir a seção do modelo: linha em branco entre as partes, *negrito* em nome/preço/total, _itálico_ em observação curta, listas com "•" | 1 |
| Botões não aparecem ou aparecem cortados | Mais de 3 botões, título longo ou tipo Texto + Botões desligado | No máximo 3 botões, títulos de até 20 caracteres, sem formatação; ligar o tipo | config. e 1 |
| A transferência não dispara | A frase que o agente mandou não é a citada no "Quando" (paráfrase, emoji no meio, frase mudada) | Deixar a frase fixa idêntica nos arquivos 1 e 3, citada entre aspas no "Quando" | 1 e 3 |
| A transferência dispara antes da hora | O "Quando" não exclui o simples envio do resumo, perguntas ou mudanças | Acrescentar o "Não vale se..." e a aprovação do último resumo | 3 (e 2) |
| Transfere duas vezes | Função `connect_user_to_human` ligada junto com regras que transferem | Manter um mecanismo só (de preferência as Ações de IA) | config. |
| O agente inventa preço, horário ou ingrediente | Dado ausente sem regra de `[A DEFINIR]`, ou descrição "de cabeça" | Marcar `[A DEFINIR]`/"a confirmar" e a regra de responder que a equipe confirma | 1 |
| O agente não sabe se está aberto | `{{current_user_time}}` fora do prompt | Seção CONTEXTO DESTE ATENDIMENTO no final do prompt | 1 |
| `{{campo}}` aparece cru na conversa | Nome do campo diferente do criado na Nextags | Conferir o nome exato do campo personalizado e ajustar os arquivos 1 e 3 | 1 e 3 |

Se o sintoma não estiver na tabela, pergunte ao usuário o que ele esperava ver (um print ajuda) e ajuste a instrução em texto simples. Não procure a resposta na central de ajuda.

## 12. Versões anteriores: o que não usar

A central de ajuda e a documentação da Nextags ainda têm páginas de versões anteriores da plataforma. Se você, o usuário ou um material citar algo destes, saiba que **não vale mais**:

| Versão anterior (não usar) | Como é hoje |
|---|---|
| "JSON Agente", "respostas do agente em JSON", "respostas elaboradas": o agente responde em JSON no padrão da Messenger Platform (chaves "messages", "attachment", "payload", "template_type", "recipient") | O prompt descreve em texto o que enviar, e a Nextags converte pelo **Tipo de resposta da IA** (Texto, Imagem/Vídeo/Áudio/Arquivo, Texto + Botões, Carrossel) |
| Ações dentro do JSON da resposta (chave "actions": add_tag, set_field_value, transfer_conversation_to, assign_conversation, send_flow) | Ações configuradas nas **Ações de IA** (regras com "Quando" + ações do menu) |
| Foto como URL colada no texto, para o WhatsApp mostrar a prévia do link | Foto enviada como imagem (tipo Imagem ligado), com legenda |
| Prompt pedindo "retorne somente JSON válido" | O agente escreve mensagens normais, com a formatação de WhatsApp |

Se o usuário pedir uma dessas formas, explique em uma frase que é de uma versão anterior e que hoje a Nextags faz isso sozinha. Só siga diferente se ele, já sabendo disso, insistir.
