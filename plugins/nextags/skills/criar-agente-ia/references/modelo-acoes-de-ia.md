# Modelo do arquivo 3 – Ações de IA

## Como montar

1. Comece pela seção "Antes de configurar", com o que o cliente precisa criar na Nextags.
2. Escolha as regras da biblioteca abaixo conforme o objetivo e o segmento. Toda regra de transferência segue a mesma estrutura de ações: Etiqueta → Campo(s) → Transferir conversa para humano → Atribuir conversa a um administrador.
3. O "Quando" de cada regra descreve **o que o cliente disse** e **a frase fixa que o agente mandou**, citando entre aspas o começo exato dessa frase. É por esse texto literal que a regra se apoia; uma paráfrase ("o agente disse que passou para a equipe") é mais fraca. As frases entre aspas precisam existir no arquivo 1 (o validador confere).
6. Toda regra que tem "Transferir conversa para humano" também tem "Atribuir conversa a um administrador → [atendente]" (o validador avisa se faltar).
4. Diga também o que **não** vale ("Não vale se..."). Isso evita disparo antes da hora.
5. Termine com "Ações que ficaram de fora", explicando por que (principalmente Bloquear e Arquivar).

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

As regras usam as mensagens de transferência do system prompt ("[PREENCHER: frase principal]" e "Vou chamar alguém da nossa equipe para continuar seu atendimento"). Se você mudar essas frases no system prompt, revise o "Quando" das regras.
```

---

## Biblioteca de regras

### Regra principal – Pedido pré-confirmado (bloco A)

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

### Regra complementar – Salvar endereço de entrega (bloco A, se houver entrega)

Fica separada da regra principal para que um pedido de retirada não apague o endereço salvo.

**Quando**
O cliente aprovou o último resumo de um pedido para *entrega* (com endereço no resumo) e o [agente] respondeu com a mensagem "Prontinho! Seu pedido foi pré-confirmado e já passei para a nossa equipe". (Escreva o "Quando" completo, sem depender de outra regra: cada regra é avaliada sozinha.)

**O que a IA deve fazer?**
1. Definir Campo Personalizado → endereco_entrega
   Valor: o endereço do último resumo aprovado (rua, número, bairro e ponto de referência), em uma linha.

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
A ferramenta de agenda confirmou a criação do agendamento e o [agente] respondeu com a mensagem "Prontinho! Seu horário está agendado para".

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
O cliente escolheu pelo menos um item e o agente anotou, mas ainda não houve pré-confirmação.

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
