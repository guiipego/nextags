# Coleta do catálogo (produtos ou serviços)

## Sumário
1. Ordem de preferência das fontes
2. Sites: WordPress, WooCommerce, Shopify e outros
3. Apps de delivery, PDF, foto e planilha
4. Conferência das fotos
5. Problemas comuns nas descrições
6. Tamanhos, variações e serviços
7. Preços estimados
8. Formato do `catalogo.json`

---

## 1. Ordem de preferência das fontes

1. **Material do cliente** (planilha, PDF, lista colada): é o mais atual e tem preço.
2. **Site do negócio ou da rede:** costuma ter fotos com URL pública e descrições.
3. **Apps de delivery** (iFood, Anota AI, Goomer, aiqfome): têm preço, mas são difíceis de ler sem navegador.
4. **Instagram:** não dá para extrair de forma confiável. Peça ao cliente o cardápio.

Combine as fontes quando fizer sentido (ex.: produtos e fotos do site + preços da planilha do cliente).

## 2. Sites

Comece pela página inicial e pela página de produtos ou cardápio, para entender a estrutura. Depois procure um endpoint JSON, que é mais rápido e completo que ler o HTML.

### WordPress (o mais comum)
- `GET {site}/wp-json/` lista as rotas. Procure tipos de post personalizados (ex.: `/wp/v2/produtos`, `/wp/v2/cardapio`) e taxonomias (`/wp/v2/taxonomies`).
- `GET {site}/wp-json/wp/v2/{tipo}?per_page=100&_embed=wp:featuredmedia`: o título fica em `title.rendered`, a foto em `_embedded["wp:featuredmedia"][0].source_url` e as categorias em `{taxonomia}`. Os cabeçalhos `X-WP-Total` e `X-WP-TotalPages` dizem quantos itens existem. Pagine com `&page=2`.
- `GET {site}/wp-json/wp/v2/{taxonomia}?per_page=100` traz os nomes das categorias e a hierarquia (`parent`).
- **Descrição vazia no JSON?** Muitos sites (Elementor + JetEngine) guardam a descrição curta num campo que só aparece na listagem da página. Leia a listagem renderizada: cada item tem `data-post-id`. Se a listagem carrega por rolagem infinita, o atributo `data-nav` do elemento `.jet-listing-grid__items` traz a query e as configurações. Faça POST para a URL em `JetEngineSettings.ajaxlisting` com `action=jet_engine_ajax`, `handler=listing_load_more`, `query`, `widget_settings`, `page=N` e `page_settings` (com post_id, queried_id, element_id e page), codificados no formato de formulário do PHP (`query[post_type]=...`). A resposta traz `data.html` com mais itens.
- A página de cada produto pode ter ingredientes, alergênicos e detalhes. Guarde o link (`link` no JSON) para o agente mandar quando o cliente perguntar.

### WooCommerce
- `GET {site}/wp-json/wc/store/v1/products?per_page=100&page=1` é público e traz nome, preço (`prices.price`, em centavos, com `prices.currency_minor_unit`), imagens (`images[].src`), categorias, descrição curta e link.
- Variações (tamanho, cor) ficam em `variations` ou `attributes`.

### Shopify
- `GET {site}/products.json?limit=250&page=1` traz título, `body_html`, variantes com preço e imagens.

### Outros (Nuvemshop, Tray, VTEX, Wix, sites próprios)
- Tente o `sitemap.xml` para listar as páginas de produto e leia cada página.
- Os metadados `og:image`, `og:title` e `product:price:amount` costumam ter foto, nome e preço.

### Como fazer as requisições
- **Navegador disponível (Claude Code ou extensão):** rodar JavaScript na página (`fetch`) é o caminho mais fácil, porque usa os cookies e passa por proteções simples.
- **Sem navegador:** Python com `urllib.request` e um `User-Agent` comum resolve a maioria dos endpoints JSON. Se o site bloquear, peça ao cliente o material.
- Não use força bruta nem contorne bloqueios. Se o site recusar, mude de fonte.

## 3. Apps de delivery, PDF, foto e planilha

- **iFood, Anota AI, Goomer:** as páginas são montadas por JavaScript. Com navegador, leia o texto da página. Sem navegador, peça ao cliente um print ou a exportação do cardápio. As fotos desses apps podem ter URLs temporárias; prefira as do site.
- **PDF:** extraia o texto e confira preços e nomes com o cliente quando a formatação embaralhar as colunas.
- **Foto do cardápio:** transcreva e confirme os itens com o cliente.
- **Planilha:** peça colunas de nome, categoria, tamanho, preço, descrição e URL da foto.

## 4. Conferência das fotos

Para cada URL de foto:
- faça uma requisição e confira se volta HTTP 200 com `Content-Type` de imagem;
- descarte placeholders de carregamento preguiçoso (`data:image/svg+xml...`) e use a URL original (no WordPress, `source_url`, sem o sufixo `-300x300`);
- anote o formato e o peso. **O WhatsApp só aceita imagem png ou jpeg de até 5 MB**, e o Instagram png, jpeg ou gif de até 8 MB (limites oficiais da Nextags, ver `nextags-plataforma.md`, seção 6). WebP, comum em sites WordPress, não chega como imagem nesses canais: no teste aparece "Media upload error WebP image uploads are not currently supported". Cuidado também com PNG servido por CDN: o da Shopify, por exemplo, entrega WebP para PNG com fundo transparente, mesmo com `format=jpg` ou `format=pjpg` na URL. Parâmetro de formato na URL não resolve. Se houver fotos fora do padrão:
  1. avise o cliente com a contagem (ex.: "54 das 62 fotos são WebP e não vão chegar como imagem no WhatsApp");
  2. converta com `python3 scripts/converter_fotos.py catalogo.json fotos_convertidas/` (gera os JPGs com fundo branco e um `mapa_fotos.csv`). Acrescente `--incluir-png` se houver PNG, principalmente vindo de CDN de loja;
  3. o cliente sobe os JPGs num endereço público (biblioteca de mídia do próprio site, a hospedagem dele ou um serviço de imagens). Depois, rode de novo com `--base-url <endereço>` para gerar o `catalogo_jpg.json` com as URLs novas e remonte o catálogo;
  4. enquanto isso não acontece, entregue com as URLs originais e deixe o aviso na lista de pendências;
- anote **fotos repetidas** (dois produtos com a mesma URL) e acrescente ao item a observação "foto ilustrativa (a mesma do X)";
- produto sem foto fica com `"foto": null` (o script escreve "(sem foto)" e o agente descreve em texto).

Se a embalagem mostrar o tamanho (ex.: "1,5L", "240ml"), dá para ler na foto ampliada. Confirme os tamanhos ambíguos com o cliente.

## 5. Problemas comuns nas descrições

| Problema | Exemplo | O que fazer |
|---|---|---|
| Texto de preenchimento | "Lorem ipsum..." | Escrever a partir da foto + observação "descrição aproximada" |
| Descrição copiada de outro item | Dois copos de açaí com o mesmo texto e fotos diferentes | Reescrever pela foto + observação |
| Contradição | "Zero açúcar" com "leite condensado" | Corrigir para o que é seguro afirmar |
| Nome repetindo a categoria | "Milkshake" dentro de Milkshakes | Dar um nome claro ("Milkshake Tradicional") |
| Item sem descrição e sem foto | Cardápio colado só com "Calabresa G 52,90" | Não escreva ingredientes "de cabeça" (ex.: pela receita tradicional): o agente vai repetir isso ao cliente como fato. Use só o que o cliente informou e acrescente a observação "ingredientes a confirmar com a equipe"; liste nas pendências |
| Página de detalhes com a composição de outro produto | No caso real, 49 de 62 páginas mostravam os ingredientes errados (32 com o texto do "creme de cupuaçu") | Antes de usar o link de ingredientes, compare o texto de composição entre as páginas. Se o mesmo texto se repete em produtos diferentes, **não** coloque esses links no catálogo. Em pergunta de alergia, o agente transfere para a equipe, sem mandar link. Avise o cliente na entrega para corrigir o site |

## 6. Tamanhos, variações e serviços

- **Mesmo sabor em tamanhos diferentes:** são itens separados no catálogo, e o agente pergunta o tamanho quando o cliente não diz.
- **Produtos montados na hora** (copos, taças, combos): defina um tamanho único e diga isso no catálogo.
- **Adicionais:** lista separada, com preço e a quais itens se aplicam.
- **Serviços:** use `tamanho` para a duração (ex.: "45 min"). O preço pode ser número, faixa ("R$ 80,00 a R$ 120,00") ou "sob avaliação".

## 7. Preços estimados

Quando o cliente não tiver os preços e quiser simular:
- pense na realidade local (capital × interior, público, posicionamento da marca); uma estimativa razoável basta, sem pesquisa longa;
- defina **faixas por grupo**, com o mesmo preço para itens do mesmo grupo, salvo justificativa;
- respeite a hierarquia (básico < premium; tamanho maior < preço por litro menor; individual < compartilhado);
- termine os preços em ,00, ,50 ou ,90;
- avise na entrega: "os preços são estimativas para simulação, troque pela tabela real antes de ativar". O prompt não diz ao cliente final que o preço é estimado.

## 8. Formato do `catalogo.json`

É a entrada de `scripts/montar_catalogo.py`. A ordem das seções, dos grupos e dos itens é a ordem em que o agente mostra.

```json
{
  "secoes": [
    {
      "titulo": "PICOLÉS",
      "grupos": [
        {
          "titulo": "Picolés de Fruta",
          "itens": [
            {
              "nome": "Picolé Uva Natural",
              "tamanho": "unidade",
              "preco": 4.5,
              "descricao": "À base de água, feito com uvas frescas do Vale do Jequitinhonha!",
              "foto": "https://exemplo.com.br/wp-content/uploads/picole-uva.webp",
              "link": "https://exemplo.com.br/produtos/picole-uva-natural/",
              "obs": []
            }
          ]
        }
      ]
    }
  ],
  "adicionais": {
    "titulo": "ADICIONAIS (para copos, taças, barca e milkshakes)",
    "itens": [
      { "nome": "Leite condensado", "preco": 2.5 }
    ]
  }
}
```

Campos de cada item:
- `nome` e `descricao`: obrigatórios.
- `tamanho`: unidade, volume, peso ou duração.
- `preco`: número (4.5), texto ("a partir de R$ 80,00", "sob avaliação") ou `null` (o script escreve "consultar a equipe").
- `foto`: URL pública ou `null`.
- `link`: página do produto ou `null`. O script chama de "Detalhes/ingredientes". Use `null` se a página não for confiável (seção 5).
- `obs`: lista de observações para o agente (ex.: "descrição aproximada, a equipe confirma a montagem.", "foto ilustrativa (a mesma do Picolé Açaí com Ninho).").

Campos opcionais na raiz do JSON:
- `adicionais`;
- `rotulo_link`: nome do link de cada item no catálogo. O padrão é "Detalhes/ingredientes"; use "Ingredientes/alergênicos" para alimentos ou "Mais detalhes" para serviços.
