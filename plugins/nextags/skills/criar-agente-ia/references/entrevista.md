# Banco de perguntas da entrevista

Use como checklist, não como questionário: pule tudo o que já veio no material do cliente (site, cardápio, conversa). Faça no máximo 3 ou 4 perguntas por mensagem, na ordem dos blocos. O que o cliente não souber vira `[A DEFINIR]`.

Legenda: **(mínimo)** = necessário para começar a escrever. O resto pode ficar pendente.

## Bloco 1 – O negócio
1. **(mínimo)** Nome do negócio e da unidade. Cidade e bairro.
2. **(mínimo)** Onde estão os produtos ou serviços: site, cardápio (PDF/foto), planilha, iFood/Anota AI, Instagram ou lista colada.
3. É franquia ou rede? Se for, há site ou contato da rede (para quem pergunta sobre franquia)?
4. Uma ou duas frases sobre a história ou o diferencial (vira tom e argumento de venda).

## Bloco 2 – O agente
5. **(mínimo)** Objetivo principal. Ofereça as opções:
   - **Pedido/venda:** mostra os produtos, monta o pedido, fecha o valor e transfere para o humano confirmar.
   - **Agendamento:** mostra os serviços, coleta o serviço e o dia/horário preferido e transfere para o humano confirmar a agenda.
   - **Orçamento/lead:** faz perguntas de qualificação, resume a necessidade e transfere para um vendedor.
   - **Suporte/dúvidas:** responde perguntas frequentes e transfere o que não souber.
6. Nome do agente. Sugira algo ligado à marca (ex.: "Migo" para "Sorvete Amigo").
7. Tom: descontraído, acolhedor ou formal? Pode usar regionalismo (ex.: mineiro, nordestino, gaúcho)? Pode usar emojis?
8. Canal: WhatsApp, Instagram ou os dois. Isso muda a formatação: o Instagram não aceita negrito com asterisco.

## Bloco 3 – Produtos ou serviços
9. Os preços estão no material? Se não, prefere passar a tabela ou quer uma **estimativa de mercado** para simular agora?
10. Tem tamanhos, variações, adicionais ou combos? Com que preço?
11. Tem fotos? (No site, as URLs são coletadas automaticamente.)
12. Algum produto ou serviço que não deve ser oferecido pelo agente (fora de linha, só no balcão)?

## Bloco 4 – Operação
13. Endereço completo.
14. Horário de funcionamento: dias úteis, sábado, domingo e feriados.
15. Retirada no local: sim ou não.
16. Entrega ou atendimento em domicílio: sim ou não. Área atendida, taxa (fixa, por bairro, grátis acima de certo valor), pedido mínimo e tempo médio.
17. Formas de pagamento.
18. Para agendamento: duração de cada serviço, profissionais, antecedência mínima e política de cancelamento ou falta.

## Bloco 5 – Transferência e Nextags
19. **(mínimo)** Quem recebe as conversas transferidas: o nome do administrador na Nextags.
20. Além do pedido pré-confirmado, quando deve ir direto para o humano? Sugira o padrão: pediu atendente, reclamação, alergia ou saúde, desconto ou fiado, pedido grande ou evento (acima de R$ X), dúvida sem resposta.
21. Quer usar etiquetas e campos personalizados para memória ("o mesmo de antes", endereço salvo) e relatórios? Recomende que sim.
22. Quer recuperar quem para no meio do pedido (ações "Seguir"/acompanhamento)? Pode ficar desligado no começo.

## Bloco 5b – Ferramentas de IA e formato das respostas
Pergunte só o que se aplica. Muitos clientes não sabem o que está ligado: explique em uma linha e recomende.
23. **Tipo de resposta da IA:** o que o agente pode mandar? Texto (sempre), **Imagem** (a foto chega como imagem; sem isso vai como link), **Texto + Botões** (escolhas rápidas como Retirada/Entrega) e **Carrossel** (até 10 produtos com foto, lado a lado). O padrão recomendado é ligar os 4. Só pergunte se o cliente quer desligar algum.
24. **Ferramentas ligadas no agente** (IA Hub → Ferramentas de IA):
   - *Image Reader:* o cliente manda foto ou print (cardápio, defeito, comprovante) e a IA entende.
   - *Document Reader:* o cliente manda PDF (orçamento, lista de materiais).
   - *Web Search:* a IA pesquisa só nos sites autorizados (recomende só o site do próprio negócio).
   - *Arquivos:* PDFs ou planilhas na base de conhecimento (FAQ, políticas, tabela grande).
25. **Servidor MCP conectado?** Loja online (Shopify e similares: produtos, estoque, pedidos) ou agenda. Se tiver, peça a URL para listar as ferramentas, ou o nome e a descrição de cada uma.
26. **Função `connect_user_to_human` ligada?** Se estiver, combine qual mecanismo transfere (função ou Ações de IA), para não transferir duas vezes.
27. **Palavras-chave** que já disparam fluxos (ex.: "cardápio", "promoção"): anote para não brigar com o agente.

## Bloco 6 – Regras especiais (pergunte só o que se aplica ao segmento)
28. Assuntos que o agente nunca deve tratar ou prometer (prazo exato, diagnóstico, desconto, estoque).
29. Política de troca, devolução ou reembolso.
30. Promoções em vigor (com data de validade, para o agente não oferecer promoção vencida).
31. Restrições legais ou sensíveis: venda de álcool só para maiores de 18, saúde, crianças, LGPD.

---

## Extras por segmento

**Alimentação / delivery:** alergênicos e link de ingredientes; adicionais e montagem; pedido para evento ou festa; taxa por bairro; tempo de preparo; horário da cozinha diferente do horário da loja.

**Varejo (roupas, calçados, cosméticos):** grade de tamanhos e cores; estoque é confirmado pelo humano; troca; frete e correios; parcelamento.

**Saúde (clínica, odonto, estética):** o agente **nunca** diagnostica nem indica tratamento; pede o mínimo de dados (nome, serviço, preferência de horário, nome do convênio), sem CPF, número de carteirinha ou detalhes clínicos pelo WhatsApp; em urgência, orienta a procurar atendimento ou ligar para o SAMU 192; convênios aceitos; preparo para exames; o humano confirma a agenda.

**Beleza (salão, barbearia):** serviço + profissional + duração; encaixe; atrasos; pacotes.

**Imobiliária:** compra ou aluguel; bairro; faixa de preço; quartos; financiamento; o agente qualifica e transfere para o corretor, sem prometer visita.

**Educação (cursos, escolas):** turmas, horários, valores, matrícula, bolsa; o humano fecha a matrícula.

**Serviços técnicos / orçamento (reforma, ar-condicionado, oficina):** tipo de serviço, fotos do problema, endereço, urgência; o agente coleta e transfere para orçamento, sem dar preço fechado sem avaliação.

---

## Resumo de confirmação (fim da entrevista)

Antes de escrever, mande algo assim e peça um "ok":

> Pelo que entendi:
> • *Agente:* Migo, tom descontraído com jeitinho mineiro, para WhatsApp
> • *Objetivo:* mostrar os produtos, montar o pedido, fechar o valor e transferir para a equipe confirmar
> • *Transfere antes:* pediu atendente, reclamação, alergia, desconto ou fiado, pedido acima de R$ 300
> • *Operação:* retirada e entrega em toda a cidade, taxa de R$ 5 (grátis a partir de R$ 50); Pix, dinheiro e cartão
> • *Pendente:* horário de feriados
> Posso montar os arquivos?
