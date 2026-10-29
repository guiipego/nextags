# Modelo do arquivo 3 – Ações de IA

## Como montar

1. Comece pela seção "Antes de configurar", com o que o cliente precisa criar na Nextags. No arquivo, cada regra começa com o título "## Regra N – [nome da regra]" e tem as partes **Quando** e **O que a IA deve fazer?** (é assim que o validador encontra as regras).
2. Escolha as regras da biblioteca abaixo conforme o objetivo, o segmento e o **modo de fechamento** (`modos-de-fechamento.md`). A regra principal muda com o modo: no modo 1 ela transfere; nos modos 2 a 5 ela só etiqueta e salva campos, e o humano entra por outras regras ("Comprovante recebido", "Problema no fechamento", a pré-confirmação de reserva e as exceções). O que cada modo muda nos 3 arquivos está no topo de `modos-de-fechamento.md`.
3. Toda regra de transferência segue a mesma estrutura de ações: Etiqueta → Campo(s) → Transferir conversa para humano → Atribuir conversa a um administrador. Toda regra que tem "Transferir conversa para humano" também tem "Atribuir conversa a um administrador → [atendente]" (o validador avisa se faltar).
4. O "Quando" de cada regra descreve **o que o cliente disse** e **a frase fixa que o agente mandou**, citando entre aspas o começo exato dessa frase. É por esse texto literal que a regra se apoia; uma paráfrase ("o agente disse que passou para a equipe") é mais fraca. As frases entre aspas precisam existir no arquivo 1 (o validador confere).
5. Diga também o que **não** vale ("Não vale se..."). Isso evita disparo antes da hora.
6. Termine com "Ações que ficaram de fora", explicando por que (principalmente Bloquear e Arquivar).

Troque `[atendente]` pelo nome do administrador que o cliente informou.

---

## Modelo do topo do arquivo

```markdown
# Ações de IA – [PREENCHER: nome do agente] ([PREENCHER: nome do negócio])

## Antes de configurar

Crie na Nextags:

**Etiquetas**
- [PREENCHER: uma por regra]

**Campos personalizados** (Fluxo > Campos Personalizados > Adicionar). Use exatamente estes nomes, porque o system prompt lê alguns deles:

| Nome do campo | Tipo | Para que serve |
|---|---|---|
| [PREENCHER] | [Texto/Número] | [PREENCHER] |

Se a Nextags gerar o nome do campo de outro jeito (ex.: com maiúsculas), ajuste os `{{...}}` no final do system prompt para bater com o nome real.

**Quem recebe:** nas ações "Atribuir conversa a um administrador", escolha [PREENCHER: nome].

As regras usam as frases fixas do system prompt ("[PREENCHER: frase de fechamento do modo escolhido]" e "Vou chamar alguém da nossa equipe para continuar seu atendimento"). Se você mudar essas frases no system prompt, revise o "Quando" das regras.
```

---

## Biblioteca de regras

### Regra principal – Pedido pré-confirmado (bloco A, modo 1)

**Quando**
O cliente aprovou o último resumo de pedido enviado pelo [agente] (com itens, quantidades e valor), respondendo algo como "sim", "pode", "confirmo" ou "isso", ou clicando no botão de confirmação do resumo, e o [agente] respondeu com a mensagem "Prontinho! Seu pedido foi pré-confirmado e já passei para a nossa equipe". Não vale se o cliente só pediu o resumo, fez uma pergunta, pediu alguma mudança ou respondeu de forma ambígua.

**O que a IA deve fazer?**
1. Adicionar Etiqueta → Pedido pré-confirmado
2. Definir Campo Personalizado → resumo_pedido
   Valor: itens com quantidade e preço, adicionais, total, retirada ou entrega, endereço, forma de pagamento (e troco) e observações, copiados do último resumo aprovado, em uma linha por informação.
3. Definir Campo Personalizado → valor_pedido
   Valor: o "Total" do último resumo aprovado (já com a taxa, se houver), só o número, com ponto. Ex.: 47.30
4. Transferir conversa para humano
5. Atribuir conversa a um administrador → [atendente]

Nos modos 3 e 4, acrescente antes da transferência "Remover Etiqueta → Aguardando pagamento", para quem trocou o Pix ou o link por dinheiro ou cartão.

### Regra complementar – Salvar endereço de entrega (bloco A, se houver entrega)

Fica separada da regra principal para que um pedido de retirada não apague o endereço salvo.

**Quando**
O cliente aprovou o último resumo de um pedido para *entrega* (com endereço no resumo) e o [agente] respondeu com a mensagem "Prontinho! Seu pedido foi pré-confirmado e já passei para a nossa equipe". (Escreva o "Quando" completo, sem depender de outra regra: cada regra é avaliada sozinha. Em outro modo de fechamento, cite todas as frases de fechamento que levam um endereço, ex.: no modo 4, "Fechou! Para concluir, faça o Pix de" ou "Prontinho! Seu pedido foi pré-confirmado e já passei para a nossa equipe".)

**O que a IA deve fazer?**
1. Definir Campo Personalizado → endereco_entrega
   Valor: o endereço do último resumo aprovado (rua, número, bairro e ponto de referência), em uma linha.

### Regra principal – Link de compra enviado (modo 2, checkout por ferramenta)

Não transfere: quem finaliza a compra é o cliente, no checkout.

**Quando**
O cliente confirmou o que vai levar e o [agente] respondeu com a mensagem "Fechou! Aqui está o link para finalizar sua compra", com os itens. Vale também para um link novo, depois de uma mudança. Não vale se o [agente] só mostrou produtos, mandou o link de um produto para o cliente ver, reenviou o mesmo link em texto porque o botão não abriu ou avisou que não conseguiu gerar o link.

**O que a IA deve fazer?**
1. Adicionar Etiqueta → Link de compra enviado
2. Definir Campo Personalizado → resumo_pedido
   Valor: os itens (produto, variação, tamanho e quantidade) e o total da mensagem de fechamento.
3. Definir Campo Personalizado → valor_pedido
   Valor: o total da mensagem de fechamento, só o número, com ponto. Ex.: 189.90
4. Opcional: Seguir (para lembrar quem não comprou, se o cliente usar acompanhamento)

### Regra principal – Link de pagamento enviado (modo 3, link fixo por item)

**Quando**
O cliente aprovou o último resumo e o [agente] respondeu com a mensagem "Fechou! Aqui está o link de pagamento do seu pedido". Não vale se o cliente ainda não aprovou o resumo, pediu mudança ou se o [agente] só reenviou o mesmo link em texto.

**O que a IA deve fazer?**
1. Adicionar Etiqueta → Aguardando pagamento
2. Definir Campo Personalizado → resumo_pedido
   Valor: itens, total e retirada ou entrega, copiados do último resumo aprovado.
3. Definir Campo Personalizado → valor_pedido
   Valor: o total do último resumo aprovado, só o número, com ponto.

### Regra principal – Pix enviado (modo 4)

**Quando**
O cliente aprovou o último resumo e o [agente] respondeu com a mensagem "Fechou! Para concluir, faça o Pix de", com o valor e a chave Pix. Não vale se o cliente só perguntou se aceita Pix ou pediu a chave antes de aprovar o resumo. (Dinheiro, cartão e pedido sem total fechado seguem a regra "Pedido pré-confirmado".)

**O que a IA deve fazer?**
1. Adicionar Etiqueta → Aguardando pagamento
2. Definir Campo Personalizado → resumo_pedido
   Valor: itens, total, retirada ou entrega, endereço e observações, copiados do último resumo aprovado.
3. Definir Campo Personalizado → valor_pedido
   Valor: o total do último resumo aprovado, só o número, com ponto.

### Comprovante recebido – conferir pagamento (modos 3 e 4)

Transfere para a equipe conferir o pagamento e liberar o pedido. O agente nunca confirma pagamento.

**Quando**
O cliente mandou o comprovante (foto, print ou PDF) depois do link de pagamento ou do Pix, e o [agente] respondeu com a mensagem "Recebi seu comprovante! Nossa equipe confere o pagamento". Não vale se o cliente só perguntou como pagar ou disse "já paguei" sem mandar o comprovante.

**O que a IA deve fazer?**
1. Adicionar Etiqueta → Pagamento a conferir
2. Remover Etiqueta → Aguardando pagamento
3. Transferir conversa para humano
4. Atribuir conversa a um administrador → [atendente]

### Regra principal – Pedido registrado (modo 5, registro no sistema)

Não transfere: o pedido já está no sistema.

**Quando**
O cliente aprovou o último resumo e o [agente] respondeu com a mensagem "Prontinho! Seu pedido foi registrado com o número", com o número do pedido. Não vale se o [agente] avisou que deu erro ou ainda está coletando os dados.

**O que a IA deve fazer?**
1. Adicionar Etiqueta → Pedido registrado
2. Definir Campo Personalizado → numero_pedido
   Valor: o número que a ferramenta devolveu, como aparece na mensagem.
3. Definir Campo Personalizado → resumo_pedido
   Valor: itens, total e retirada ou entrega, copiados do último resumo aprovado.

### Problema no fechamento (modos 2 a 5 e bloco B2)

Transfere quando o agente não consegue fechar sozinho. Sem esta regra, a mensagem de transferência sai, mas a conversa não chega a ninguém.

**Quando**
O [agente] respondeu com a mensagem "Não consegui concluir por aqui agora" (erro da ferramenta, link que não abriu nem em texto ou chave Pix que não funcionou); ou o cliente disse que já pagou e não conseguiu mandar o comprovante; ou quer mudar ou cancelar o pedido ou o agendamento depois do link, do Pix ou do registro e já pagou, não sabe se pagou, já finalizou a compra ou o pedido já foi registrado; e o [agente] avisou "Vou chamar alguém da nossa equipe para continuar seu atendimento". Não vale se o cliente só disse que o botão não abriu e o [agente] ainda não mandou o link em texto.

**O que a IA deve fazer?**
1. Adicionar Etiqueta → Problema no fechamento
2. Definir Campo Personalizado → motivo_transferencia
   Valor: o que deu errado ou o que o cliente quer mudar, e o pedido como está na conversa (itens e total, ou serviço, dia e hora), em uma ou duas frases.
3. Transferir conversa para humano
4. Atribuir conversa a um administrador → [atendente]

### Regra principal – Agendamento solicitado (bloco B)

**Quando**
O cliente aprovou o último resumo de agendamento enviado pelo [agente] (serviço, preferência de horário e nome), e o [agente] respondeu com a mensagem "Prontinho! Sua solicitação de agendamento foi registrada e já passei para a nossa equipe". Não vale enquanto o [agente] ainda está coletando os dados ou se o cliente pediu mudança.

**O que a IA deve fazer?**
1. Adicionar Etiqueta → Agendamento solicitado
2. Definir Campo Personalizado → resumo_pedido
   Valor: serviço, profissional (se houver), preferência de dia e horário, nome e valor, copiados do último resumo aprovado.
3. Transferir conversa para humano
4. Atribuir conversa a um administrador → [atendente]

### Regra principal – Lead qualificado (bloco C)

**Quando**
O cliente respondeu às perguntas de qualificação, aprovou o resumo enviado pelo [agente] e o [agente] respondeu com a mensagem "Perfeito! Já passei suas informações para um especialista da nossa equipe".

**O que a IA deve fazer?**
1. Adicionar Etiqueta → Lead qualificado
2. Definir Campo Personalizado → resumo_pedido
   Valor: as respostas de qualificação e o nome, uma por linha.
3. Transferir conversa para humano
4. Atribuir conversa a um administrador → [atendente/vendedor]

### Regra principal – Agendamento criado pela agenda (bloco B2, com MCP)

Com agenda conectada, o agente agenda sozinho; a regra só registra e avisa a equipe. Não transfira: a conversa segue com o agente.

**Quando**
O [agente] respondeu com a mensagem "Prontinho! Seu horário está agendado para", com o dia e a hora. Não vale se ele avisou erro, ofereceu horários ou ainda está coletando os dados.

**O que a IA deve fazer?**
1. Adicionar Etiqueta → Agendado pela IA
2. Definir Campo Personalizado → resumo_pedido
   Valor: serviço, dia e hora agendados e nome, como confirmados na conversa.

### Cliente pediu atendente (todos)

**Quando**
O cliente pediu claramente para falar com uma pessoa (atendente, humano, gerente, dono ou "alguém da loja") e o [agente] avisou "Vou chamar alguém da nossa equipe para continuar seu atendimento".

**O que a IA deve fazer?**
1. Adicionar Etiqueta → Pediu atendente
2. Transferir conversa para humano
3. Atribuir conversa a um administrador → [atendente]

### Reclamação ou problema (todos)

**Quando**
O cliente fez uma reclamação ou relatou um problema com pedido, produto, serviço ou atendimento (atraso, item errado, produto com defeito, cobrança errada, troca ou reembolso) e o [agente] avisou "Vou chamar alguém da nossa equipe para continuar seu atendimento".

**O que a IA deve fazer?**
1. Adicionar Etiqueta → Reclamação
2. Definir Campo Personalizado → motivo_transferencia
   Valor: resumo do problema em uma frase, com o produto ou serviço e o que aconteceu.
3. Transferir conversa para humano
4. Atribuir conversa a um administrador → [atendente]

### Alergia ou restrição (alimentação)

**Quando**
O cliente informou alergia ou restrição alimentar séria (leite ou lactose, amendoim, castanhas, glúten, soja, diabetes etc.) ao perguntar sobre um item, e o [agente] avisou "Vou chamar alguém da nossa equipe para continuar seu atendimento".

**O que a IA deve fazer?**
1. Adicionar Etiqueta → Alergia
2. Definir Campo Personalizado → motivo_transferencia
   Valor: a alergia ou restrição informada e o item de interesse.
3. Transferir conversa para humano
4. Atribuir conversa a um administrador → [atendente]

### Urgência ou questão de saúde (saúde)

**Quando**
O cliente relatou dor forte, sangramento, emergência ou pediu orientação clínica, e o [agente] orientou procurar atendimento ou o SAMU 192 (em emergência) e avisou "Vou chamar alguém da nossa equipe para continuar seu atendimento".

**O que a IA deve fazer?**
1. Adicionar Etiqueta → Urgência
2. Definir Campo Personalizado → motivo_transferencia
   Valor: o que o cliente relatou, em uma frase.
3. Transferir conversa para humano
4. Atribuir conversa a um administrador → [atendente]

### Encomenda grande ou evento (quando houver)

**Quando**
O cliente quer uma encomenda para festa, evento ou revenda, ou o pedido passou de R$ [valor], e o [agente] já enviou o resumo da encomenda com o valor estimado e avisou "Vou chamar alguém da nossa equipe para continuar seu atendimento". Não vale enquanto o [agente] ainda está fazendo as perguntas da encomenda.

**O que a IA deve fazer?**
1. Adicionar Etiqueta → Encomenda/Evento
2. Definir Campo Personalizado → resumo_pedido
   Valor: itens e quantidades, data e horário, retirada ou entrega, nome e valor estimado.
3. Definir Campo Personalizado → valor_pedido
   Valor: o valor estimado, só o número, com ponto.
4. Transferir conversa para humano
5. Atribuir conversa a um administrador → [atendente]

### Pedido especial (todos)

**Quando**
O cliente pediu desconto, brinde, fiado ou uma forma de pagamento que o negócio não aceita, ou insistiu numa dúvida que o [agente] não consegue responder, e o [agente] avisou "Vou chamar alguém da nossa equipe para continuar seu atendimento".

**O que a IA deve fazer?**
1. Adicionar Etiqueta → Atendimento humano
2. Definir Campo Personalizado → motivo_transferencia
   Valor: o que o cliente pediu ou perguntou, em uma frase.
3. Transferir conversa para humano
4. Atribuir conversa a um administrador → [atendente]

### Interesse comercial sem transferência (franquia, parceria, fornecedor)

**Quando**
O cliente disse que quer abrir uma franquia, ser parceiro, revendedor ou fornecedor. (O agente passa o contato certo.)

**O que a IA deve fazer?**
1. Adicionar Etiqueta → Interesse comercial

### Opcional – Recuperar quem parou no meio

Deixe desligado no começo, a menos que o cliente peça.

**Quando**
O cliente escolheu pelo menos um item e o agente anotou, mas a venda ainda não chegou ao fechamento (pré-confirmação, link, Pix ou registro).

**O que a IA deve fazer?**
1. Adicionar Etiqueta → Montando pedido
2. Seguir

Se usar, acrescente "Remover Etiqueta → Montando pedido" e "Remover do acompanhamento" na regra principal.

---

## Modelo do fim do arquivo

```markdown
## Ações que ficaram de fora

- **Bloquear contato** e **Arquivar:** não vale a pena deixar a IA decidir isso sozinha, porque um erro bloqueia ou some com um cliente real.
- **Enviar Fluxo:** só vale se houver um fluxo pronto (ex.: cardápio em PDF, pesquisa de satisfação).
- **Transferir conversa para bot** e **Remover atribuição:** são para a equipe usar quando terminar o atendimento humano.
- **Limpar Campo Personalizado:** não é necessário, porque os campos são sobrescritos.
```
