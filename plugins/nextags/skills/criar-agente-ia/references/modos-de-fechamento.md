# Modos de fechamento: como a venda (ou o agendamento) termina

Quem decide como a conversa termina é o dono do negócio, não a skill. Se ele tem um jeito de cobrar ou de registrar que o agente consiga usar (checkout da loja, link de pagamento, chave Pix, sistema conectado por MCP ou API), o agente pode fechar sozinho. Se não tem, ou se prefere conferir tudo antes, o agente pré-confirma e transfere.

## O que o modo muda nos 3 arquivos

Lista completa. Use ao escrever um agente novo e ao trocar o modo de um agente pronto (seção 9).

**Arquivo 1 – Mensagem do sistema**
- IDENTIDADE: a frase com o papel do agente.
- OBJETIVO: o final principal e o "Você não...".
- DADOS DO NEGÓCIO: a chave Pix e o recebedor (modo 4) ou os links de pagamento (modo 3, que também podem ficar no catálogo).
- A pergunta do fim do resumo e o botão de aprovação.
- A etapa final do FLUXO: o texto pronto do modo (seções 3 a 7).
- TRANSFERÊNCIA: o caso principal lista só as mensagens que transferem. Nos modos 2 a 5, acrescente que a mensagem de fechamento não transfere.
- REGRAS IMPORTANTES: a regra de *Pagamento* do modo.
- EXEMPLOS: o caminho feliz termina na mensagem de fechamento do modo (no Pix, no comprovante).

**Arquivo 3 – Ações de IA**
- A regra principal do modo e as que vêm com ela ("Comprovante recebido", "Problema no fechamento" e a pré-confirmação, quando o modo a usa como caminho de reserva).
- O "Quando" de "Salvar endereço de entrega", com todas as frases de fechamento que levam um endereço.
- A linha do topo que lista as frases fixas, e as etiquetas e os campos de "Antes de configurar".

**Arquivo 2 – Prompt da Ação**
- A exceção, só com as regras principais que transferem, e a linha das regras principais que não transferem.

**Combinar modos pode**, desde que o prompt diga quando vale cada caminho e cada um tenha a sua frase fixa e a sua regra (ex.: Pix para quem paga por aqui e pré-confirmação para dinheiro ou cartão na entrega; checkout com a pré-confirmação de reserva). **O que não pode** é instrução que se contradiz no mesmo caso, como "não envie chave Pix" na regra de *Pagamento* de um prompt que manda o Pix.

## Sumário
1. Como escolher
2. Regras que valem em todo modo que cobra (2 a 5)
3. Modo 1 – Pré-confirma e transfere
4. Modo 2 – Checkout gerado por ferramenta (loja online)
5. Modo 3 – Link de pagamento fixo por item
6. Modo 4 – Pix
7. Modo 5 – Registro direto no sistema
8. Agendamento e orçamento
9. Trocar o modo de um agente pronto

---

## 1. Como escolher

Pergunte na entrevista (pergunta 6), em linguagem simples:
1. Como o cliente paga hoje? (na entrega ou retirada, Pix, link de pagamento, checkout do site, maquininha)
2. Tem loja online, sistema de pedidos ou agenda conectado à Nextags por MCP (ou por API, via Função de IA ou Fluxo)? Quais ferramentas aparecem? (liste com `scripts/listar_ferramentas_mcp.py`)
3. Tem links de pagamento prontos, um por produto, kit ou serviço?
4. Quer que o agente cobre sozinho, ou prefere que a equipe confira antes de cobrar?

Recomende pelo que existe e confirme com o dono:

| Modo | Use quando | O agente, no fim | O humano entra |
|---|---|---|---|
| 1. Pré-confirma e transfere | Não há como cobrar ou registrar sozinho, ou o dono quer controle (estoque variável, preço sob consulta) | Resumo + aprovação → transfere | Sempre, para confirmar e cobrar |
| 2. Checkout por ferramenta | Loja online com MCP/API que monta o carrinho e devolve o link (Shopify, Nuvemshop, WooCommerce...) | Confirma os itens → gera o link → manda o botão "Comprar agora" | Só nas exceções (pós-venda, reclamação, erro da ferramenta) |
| 3. Link de pagamento fixo | Cada produto, kit ou serviço tem o próprio link com preço fixo (Mercado Pago, PagSeguro, InfinitePay, Asaas...) | Resumo + aprovação → manda o link do item, quando o pedido é exatamente aquele item | Exceções e pedidos que nenhum link cobre |
| 4. Pix | Aceita Pix e a equipe confere o comprovante | Resumo + aprovação → manda o total e a chave Pix → pede o comprovante | Para conferir o pagamento e liberar o pedido |
| 5. Registro no sistema | Sistema de pedidos ou agenda conectado por MCP/API que cria o registro | Resumo + aprovação → registra pela ferramenta → manda o número | Exceções e erro da ferramenta |

**O modo que cobra ou registra só vale com o dado na mão:** a chave Pix e o recebedor (modo 4), o link de cada item (modo 3), o servidor MCP ligado no agente ou os nomes reais das ferramentas (modos 2 e 5). Chave e link nunca ficam `[A DEFINIR]`: nesses modos a regra principal não transfere, e o cliente ficaria esperando um dado que ninguém manda. Se faltar, escreva o modo 1 e anote nas pendências: "passar para o modo X quando mandar a chave (ou os links, ou ligar o MCP)".

Na dúvida, ou se o dono não souber responder, use o modo 1 e anote nas pendências que dá para evoluir depois.

## 2. Regras que valem em todo modo que cobra (2 a 5)

Os textos prontos das seções 4 a 7 já trazem estas regras. Ao adaptar, confira se nenhuma ficou de fora:
- *Links e chaves:* só os que estão nos DADOS DO NEGÓCIO ou no catálogo, ou os que a ferramenta devolveu, copiados sem nenhuma alteração. Nunca monte, adivinhe, encurte ou "corrija" um link ou uma chave.
- *Valor fechado:* cobre só a linha *Total:* do último resumo aprovado (no agendamento com sinal, a linha *Sinal:*) ou o total que a ferramenta devolveu. Se o resumo não tiver *Total* fechado (taxa a confirmar, item com preço "a consultar", faixa ou "sob avaliação"), não mande link nem Pix: use a mensagem de pré-confirmação do modo 1, que transfere.
- *Antes de cobrar:* o cliente aprova o último resumo. No modo 2, ele confirma itens, tamanhos e quantidades antes de o link ser gerado.
- *Dados de cartão:* nunca peça número de cartão, senha, código de segurança ou código recebido por SMS.
- *Pagamento confirmado:* nunca confirme pagamento por comprovante, print ou "já paguei". Quem confirma é a ferramenta ou a equipe. Com o comprovante na mão: nos modos 3 e 4, quando a equipe confere pelo WhatsApp, responda com a mensagem fixa do comprovante; nos outros, diga quem confirma e como (texto do modo), sem começar com "Recebi seu comprovante".
- *Mudou o pedido depois do link, do Pix ou do registro:* se a conversa não deixar claro, pergunte antes se o cliente já pagou (ou já finalizou a compra no checkout). Se não pagou: resumo novo, aprovação e o link ou o valor novo, avisando que o anterior não vale mais e não deve ser pago. Se já pagou, ou não sabe: não mande cobrança nova nem calcule diferença; escreva em uma linha o que ele quer mudar e transfira (mensagem "Outros casos"). No modo 2, se o dono combinar, um acréscimo depois da compra pode ir num link só com as peças novas, como outro pedido. No modo 5, nunca crie um segundo pedido.
- *Deu errado:* se a ferramenta der erro (tente mais uma vez), se o link não abrir nem mandado em texto ou se a chave não funcionar depois de reenviada, responda exatamente "Não consegui concluir por aqui agora." e, na mesma mensagem, a mensagem "Outros casos". A regra "Problema no fechamento" transfere.
- *Frase fixa de fechamento:* a mensagem que acompanha o link, o Pix ou o registro é fixa, e a regra das Ações de IA cita o começo dela entre aspas. Com o tipo Texto + Botões ligado, o link vai num botão de URL, que vai sozinho na mensagem (sem botões de resposta junto); se o cliente disser que o botão não abriu, mande o mesmo link num texto, sozinho na linha.

## 3. Modo 1 – Pré-confirma e transfere

É o que está nos blocos A e B do `modelo-system-prompt.md`: resumo, aprovação do último resumo e a frase "Prontinho! Seu pedido foi pré-confirmado e já passei para a nossa equipe". A equipe confirma disponibilidade, pagamento e prazo.

Regra de *Pagamento* (arquivo 1), só quando o modo 1 vale para todos os pedidos:
```
7. *Pagamento:* anote a forma de pagamento que o cliente pretende usar. Não envie chave Pix nem link de pagamento: a equipe envia na confirmação. Nunca peça número de cartão, senha ou código.
```
Quando a pré-confirmação é o caminho de reserva de outro modo (dinheiro ou cartão no modo 4, pedido sem total fechado), não copie essa regra: a etapa do outro modo já diz quando usar a pré-confirmação.

Arquivo 3: regra "Pedido pré-confirmado" (ou "Agendamento solicitado") da biblioteca, com transferência.

## 4. Modo 2 – Checkout gerado por ferramenta (loja online)

Colete: os nomes das ferramentas de busca de produto e de carrinho/checkout e o que cada uma devolve (link, total, itens esgotados); o texto do botão ("Comprar agora"); o que acontece depois da compra (pós-venda, rastreio); e o que fazer quando o cliente quer acrescentar algo depois de finalizar a compra. Preço, estoque e foto vêm da ferramenta, e o CATÁLOGO do prompt pode ser só um resumo das categorias.

Etapa final do FLUXO (arquivo 1, no lugar das etapas de resumo e pré-confirmação):
```
## [N]. Fechamento
Quando o cliente escolher o que vai levar (produto, variação, tamanho e quantidade confirmados):
1. Chame [PREENCHER: ferramenta de carrinho/checkout] com a lista completa.
2. Responda exatamente com esta mensagem, com um botão de URL "[PREENCHER: Comprar agora]" com o link que a ferramenta devolveu:
"Fechou! Aqui está o link para finalizar sua compra [emoji]"
   Logo abaixo, os itens do link, um por linha (quantidade, produto, variação e tamanho), o total que a ferramenta devolveu, em negrito, e o que muda no checkout (frete, desconto). Essa mensagem não transfere: você continua no atendimento.
3. Se a ferramenta avisar que algum item esgotou, diga isso e ofereça outro antes de mandar o link.
4. Se o cliente quiser mudar algo depois do link e a conversa não deixar claro se ele já finalizou a compra, pergunte antes. Se não finalizou, gere um link novo com a lista completa e mande a mensagem de fechamento de novo, avisando que o link anterior não vale mais. Se ele já finalizou, não gere link com as peças já compradas: [PREENCHER com o dono: mande um link só com as peças novas, avisando que é outro pedido, com frete próprio / escreva em uma linha o que ele quer mudar e use a mensagem "Outros casos"].
5. Se ele disser que o botão não abriu, mande o mesmo link num texto, sozinho na linha.
6. Se a ferramenta der erro ou não devolver o link, tente mais uma vez. Se falhar de novo, ou se o link não abrir nem em texto, responda exatamente "Não consegui concluir por aqui agora." e, na mesma mensagem, a mensagem "Outros casos". Nunca monte um link.
7. Você não conclui a compra nem confirma pagamento: quem finaliza é o próprio cliente, no checkout.
```
Regra de *Pagamento* (arquivo 1):
```
7. *Pagamento:* o pagamento é feito no checkout, pelo link que a ferramenta devolve. Mande só esse link, sem nenhuma alteração; nunca monte ou adivinhe um link. Nunca peça dados de cartão. Não confirme pagamento por comprovante: se o cliente mandar um, diga que [PREENCHER: a loja confirma por e-mail / o pós-venda confere].
```
Arquivo 3: regra principal "Link de compra enviado" (sem transferência) e "Problema no fechamento". Opcional: "Seguir" para lembrar quem não comprou.

## 5. Modo 3 – Link de pagamento fixo por item

Colete o link de pagamento de cada produto, kit ou serviço (com o preço igual ao do catálogo) e coloque no `catalogo.json`, num item `obs` ("Link de pagamento: https://..."), ou numa tabela em DADOS DO NEGÓCIO. O link cobra um valor fixo, então só serve quando o pedido é exatamente aquele item. Combine com o dono o que fazer nos outros casos (quantidade maior que 1, vários itens, taxa de entrega, adicional): o Pix do total (texto do modo 4) ou a pré-confirmação (modo 1). Pergunte também se o negócio aceita dinheiro ou cartão na entrega ou na retirada e se a equipe confere o pagamento pelo WhatsApp (comprovante) ou por outro meio.

A pergunta do fim do resumo depende do caminho: "Posso te mandar o link de pagamento?" só quando o cliente vai pagar pelo link e o pedido é exatamente o item de um link; nos outros casos, a pergunta do caminho combinado ("Posso te passar o Pix?" ou a do modo 1).

Etapa final do FLUXO (arquivo 1):
```
## [N]. Pagamento
Quando o cliente aprovar o último resumo:
1. Se o cliente vai pagar pelo link e o pedido for exatamente o item de um link (1 unidade, sem taxa e sem adicional, com o *Total* igual ao preço do link), responda exatamente com esta mensagem, com um botão de URL "[PREENCHER: Pagar agora]" com o link de pagamento do item, copiado do catálogo:
"Fechou! Aqui está o link de pagamento do seu pedido [emoji]"
   Logo abaixo, o total em negrito e o que acontece depois do pagamento ([PREENCHER: ex.: "a equipe confirma e separa seu pedido"]). Essa mensagem não transfere.
2. Resumo sem *Total* fechado (taxa a confirmar, item sem preço fechado)[PREENCHER se o negócio aceita: ou pagamento em dinheiro ou cartão na entrega ou na retirada]: não mande link nem Pix. Responda exatamente com esta mensagem (é ela que passa o pedido para a equipe):
"Prontinho! Seu pedido foi pré-confirmado e já passei para a nossa equipe [emoji] Assim que possível alguém da loja te chama aqui para confirmar a disponibilidade, o pagamento e o tempo de preparo/entrega."
3. Nos outros casos (quantidade maior que 1, mais de um item, taxa de entrega, adicional, item sem link), não mande link: [PREENCHER: o que o dono combinou: o Pix do total, com o texto do modo 4 / a mensagem de pré-confirmação do item 2].
4. Quando o cliente mandar o comprovante (foto, print ou PDF), responda exatamente com esta mensagem: "Recebi seu comprovante! Nossa equipe confere o pagamento e confirma seu pedido por aqui [emoji]" [PREENCHER: apague este item se a equipe não confere o pagamento pelo WhatsApp e diga, no lugar, quem confirma e como.]
5. Se ele disser que o botão não abriu, mande o mesmo link num texto, sozinho na linha. Se nem assim abrir, responda exatamente "Não consegui concluir por aqui agora." e, na mesma mensagem, a mensagem "Outros casos".
6. Se o cliente mudar o pedido depois do link, pergunte se ele já pagou (se a conversa não deixar claro). Se não pagou, envie o resumo novo e, com a aprovação, siga esta etapa de novo, avisando que o link anterior não vale mais. Se já pagou, ou não sabe, não cobre de novo: escreva em uma linha o que ele quer mudar e use a mensagem "Outros casos".
```
Regra de *Pagamento* (arquivo 1):
```
7. *Pagamento:* mande só os links de pagamento do catálogo, copiados sem alteração, e só quando o pedido aprovado for exatamente o item do link (etapa [N]). Nunca monte, adivinhe ou encurte um link. Nunca peça dados de cartão. Nunca confirme pagamento por comprovante ou print: [PREENCHER: responda com a mensagem do comprovante da etapa N / diga quem confirma e como].
```
Arquivo 3: regra principal "Link de pagamento enviado" (sem transferência), "Problema no fechamento", "Pedido pré-confirmado" (resumo sem *Total* fechado, dinheiro ou cartão e, se for o caminho combinado, os outros casos), "Pix enviado" (se o caminho combinado for o Pix) e, se a equipe confere o pagamento pelo WhatsApp, "Comprovante recebido" (com transferência). Se a equipe não confere pelo WhatsApp, a mensagem sobre o comprovante não começa com "Recebi seu comprovante" e essa regra fica de fora.

## 6. Modo 4 – Pix

Colete: o tipo e a chave Pix, o nome que aparece para quem paga (recebedor), o que a equipe faz depois de conferir (separa, prepara, confirma o horário) e se o negócio também aceita dinheiro ou cartão na entrega ou na retirada. Em DADOS DO NEGÓCIO (arquivo 1):
```
- Pix: chave [PREENCHER: tipo] [PREENCHER: chave], em nome de [PREENCHER: recebedor]
```
A pergunta do fim do resumo depende do caminho: "Posso te passar o Pix?" só quando o pagamento é Pix e o resumo tem *Total* fechado; com dinheiro ou cartão, ou sem *Total* fechado, a pergunta do modo 1 ("Posso enviar para a equipe confirmar?").

Etapa final do FLUXO (arquivo 1, no lugar da pré-confirmação):
```
## [N]. Pagamento
Quando o cliente aprovar o último resumo:
1. *Pix, com Total fechado:* responda exatamente com esta mensagem:
"Fechou! Para concluir, faça o Pix de *R$ [Total do último resumo]*"
   Na mesma mensagem, em linhas separadas: a chave Pix (sozinha na linha, para copiar), o nome do recebedor e o pedido para mandar o comprovante aqui. Essa mensagem não transfere: você continua no atendimento até o comprovante chegar.
2. *Dinheiro ou cartão na entrega ou na retirada, ou resumo sem Total fechado* (taxa a confirmar, item sem preço fechado): não mande a chave Pix. Responda exatamente com esta mensagem (é ela que passa o pedido para a equipe):
"Prontinho! Seu pedido foi pré-confirmado e já passei para a nossa equipe [emoji] Assim que possível alguém da loja te chama aqui para confirmar a disponibilidade, o pagamento e o tempo de preparo/entrega."
3. *Comprovante:* quando o cliente mandar o comprovante (foto, print ou PDF), responda exatamente com esta mensagem:
"Recebi seu comprovante! Nossa equipe confere o pagamento e confirma seu pedido por aqui [emoji]"
   Não comente valor, data ou nome do comprovante, e nunca diga que o pagamento foi feito, caiu ou foi confirmado.
4. *"Já paguei" sem comprovante:* peça o comprovante uma vez. Se o cliente não conseguir mandar, use a mensagem "Outros casos".
5. *A chave não funcionou:* mande a chave de novo, sozinha na mensagem. Se ainda não der certo, responda exatamente "Não consegui concluir por aqui agora." e, na mesma mensagem, a mensagem "Outros casos".
6. *Mudou o pedido depois do Pix:* se a conversa não deixar claro, pergunte se ele já fez o Pix. Se não fez, envie o resumo novo e, com a aprovação, siga esta etapa de novo, avisando que o valor anterior não vale mais. Se já fez, ou não sabe, não cobre de novo: escreva em uma linha o que ele quer mudar e use a mensagem "Outros casos".
```
Regra de *Pagamento* (arquivo 1):
```
7. *Pagamento:* para Pix, mande só a chave dos DADOS DO NEGÓCIO, copiada sem alteração, com o *Total* do último resumo aprovado e só depois da aprovação; se o cliente pedir a chave antes, diga que você passa assim que fecharem o pedido. Dinheiro e cartão são pagos na entrega ou na retirada; nesses casos, a chave fica de fora. Nunca confirme pagamento por comprovante, print ou "já paguei": quem confere é a equipe. Nunca peça dados de cartão.
```
Arquivo 3: regra principal "Pix enviado" (etiqueta "Aguardando pagamento", sem transferência); "Comprovante recebido" (etiqueta "Pagamento a conferir", com transferência e atribuição, para a equipe conferir e liberar); "Pedido pré-confirmado" (dinheiro ou cartão e pedido sem total fechado, com transferência); "Problema no fechamento"; e "Salvar endereço de entrega" citando as duas frases (a do Pix e a da pré-confirmação). No Prompt da Ação, "Pedido pré-confirmado" entra na exceção e "Pix enviado" na linha das regras que não transferem.

## 7. Modo 5 – Registro direto no sistema

Colete: as ferramentas de criar, consultar e alterar pedido (ou agendamento), os dados obrigatórios de cada uma e o que elas devolvem (número, link, status). Liste com `scripts/listar_ferramentas_mcp.py`.

Etapa final do FLUXO (arquivo 1):
```
## [N]. Registro do pedido
Quando o cliente aprovar o último resumo:
1. Chame [PREENCHER: ferramenta de criar pedido] com os itens, o total e os dados do cliente.
2. Só depois de a ferramenta confirmar, responda exatamente com esta mensagem:
"Prontinho! Seu pedido foi registrado com o número [número que a ferramenta devolveu] [emoji]"
   Logo abaixo, o que acontece agora ([PREENCHER: pagamento na entrega / link de pagamento que a ferramenta devolveu / prazo]). Essa mensagem não transfere.
3. Se a ferramenta der erro, tente mais uma vez. Se falhar de novo, não diga que registrou: responda exatamente "Não consegui concluir por aqui agora." e, na mesma mensagem, a mensagem "Outros casos".
4. Se o cliente quiser mudar algo depois do registro, nunca chame [PREENCHER: ferramenta de criar pedido] de novo: [PREENCHER: use a ferramenta de alterar pedido com o número já registrado e mande o resumo atualizado / sem ferramenta de alterar, escreva em uma linha o que ele quer mudar e use a mensagem "Outros casos"].
```
Regra de *Pagamento* (arquivo 1): a do modo de pagamento combinado (na entrega, link devolvido pela ferramenta ou Pix), com as regras da seção 2.

Arquivo 3: regra principal "Pedido registrado" (etiqueta + campo `numero_pedido`, sem transferência) e "Problema no fechamento".

## 8. Agendamento e orçamento

- **Agendamento:** o bloco B (o humano confirma o horário) é o modo 1. O bloco B2 (agenda conectada por MCP, o agente consulta e agenda) é o modo 5, com a mesma frase de erro ("Não consegui concluir por aqui agora." + "Outros casos") e a regra "Problema no fechamento". Cobrança de sinal pode seguir o modo 3 ou 4: combine com o dono o valor (ou o percentual) do sinal, ponha em DADOS DO NEGÓCIO, mostre a linha *Sinal:* no resumo e cobre só ela.
- **Orçamento/lead (bloco C):** o fechamento costuma ser humano (o vendedor). Se houver agenda conectada, o agente pode marcar a reunião ou a visita (modo 5, com o bloco B2).

## 9. Trocar o modo de um agente pronto

Quando o dono pede para mudar como o agente fecha (ex.: "quero que ele mande a chave Pix"):
1. Refaça as perguntas 6 e 18 da entrevista. Sem o dado do modo novo (seção 1), não troque: explique o que falta.
2. Aplique a lista completa do topo deste arquivo nos 3 arquivos, de uma vez, com o texto pronto do modo novo.
3. Procure no arquivo 1 as frases do modo antigo, inclusive nos EXEMPLOS, na TRANSFERÊNCIA e na pergunta do resumo (ex.: "pré-confirmado", "Posso enviar para a equipe confirmar?", "Não envie chave Pix"), e deixe só as que o modo novo usa.
4. Rode o validador.
5. Entregue ao dono a lista para a Nextags, regra por regra: o que editar (ex.: o "Quando" de "Salvar endereço de entrega"), o que criar ("Pix enviado", "Comprovante recebido", "Problema no fechamento"), o que apagar e o que manter ("Pedido pré-confirmado", se continua valendo para dinheiro ou cartão), mais as etiquetas e os campos novos. Os 3 textos mudam e precisam ser recolados.
