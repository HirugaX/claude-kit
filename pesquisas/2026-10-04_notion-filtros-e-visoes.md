# Notion: filtro, ordenação, densidade e agrupamento nas visões de banco

- **Pergunta:** como o Notion resolve filtro, ordenação, densidade/largura e agrupamento nas visões de
  tabela e lista — com os rótulos exatos em inglês e em português — e como outros apps (Airtable, Linear,
  GitHub, Gmail) rotulam a direção da ordenação?
- **Data:** 04/10/2026
- **Projeto que pediu:** DESOSP_APP (tela de pendências).
- **Onde a decisão mora:** só aqui — a pesquisa não foi gravada em documento do projeto.
- **Fontes (principais; 15 no corpo):**
  - https://www.notion.com/help/views-filters-and-sorts · pt: https://www.notion.com/pt/help/views-filters-and-sorts
  - https://thomasjfrank.com/formulas/formulas-in-database-filters/
  - https://support.airtable.com/docs/sorting-records-in-airtable-views
- **Conclusão:**
  - Filtro e ordenação ficam em "Configurações de visualização" (`View settings`): **Filtro**, **Ordenar**,
    **Agrupar**. Filtro simples mira uma propriedade; o avançado combina **E/OU** em grupos, até 3 níveis.
  - A mudança vale só para você até **"Salvar para todos"** (`Save for everyone`).
  - Ordenação: **Crescente/Decrescente**, várias regras com prioridade arrastável (ícone `⋮⋮`).
  - A tradução oficial dos operadores em português não foi achada.
  - Padrão comum entre apps: a pílula curta mostra **propriedade + seta**, e o menu explica a direção em
    palavras; em datas, texto ("mais antiga primeiro") é mais claro que "crescente".
- **Conferir de novo depois de:** 04/01/2027 (rótulos de interface mudam).
- **Como foi feita:** subagente de pesquisa, 14 buscas de página e 15 buscas web. Abaixo, o relatório como
  voltou, sem mudança de conteúdo, **menos a seção final** ("Proposta: 5 rótulos de ordenação para a lista
  de pendências"), que é do projeto e cita a numeração interna do hospital — essa seção ficou de fora.

---

## Pesquisa: filtro, ordenação, densidade e agrupamento no Notion, mais rótulos de ordenação de outros apps

Legenda de confiança: **[oficial]** = está na ajuda do Notion; **[guia]** = tutorial de terceiro; **[não confirmado]** = sei de uso, mas não achei fonte que confirme.

### 1. Filtros
- **Onde fica.** No menu de configurações da base: `Filter` em `View settings`, depois a propriedade. Em pt-BR: `Filtro` em `Configurações de visualização`. Os guias também mostram um botão **Filter** na barra da base. **[oficial]** https://www.notion.com/help/views-filters-and-sorts · pt: https://www.notion.com/pt/help/views-filters-and-sorts (título: "Visualizações, filtros, classificações e grupos")
- **Como se monta.** Thomas Frank descreve a regra como **Propriedade → [Critério] → Valor**. Num Select dá para marcar **um ou mais valores**. **[guia]** https://thomasjfrank.com/notion-databases-the-ultimate-beginners-guide/
  - Não achei o rótulo literal "is any of" no Notion. Na interface, o critério continua `Is` com caixas de seleção, e marcar vários valores funciona como OU. Na API, `equals` em select casa "any of the provided values" (https://developers.notion.com/reference/post-database-query-filter).
  - "is any of" / "is none of" são rótulos do **Airtable** **[não confirmado]**.
- **Operadores (inglês, da interface)**, segundo https://thomasjfrank.com/formulas/formulas-in-database-filters/:
  - **Texto:** Is, Is not, Contains, Does not contain, Starts with, Ends with, Is empty, Is not empty
  - **Número:** = ≠ > < ≥ ≤, Is empty, Is not empty
  - **Data:** Is, Is before, Is after, Is on or before, Is on or after, Is within, Is empty, Is not empty. Datas relativas como "today" e "within the past month" entram desde 2022 (https://www.notion.com/releases/2022-04-14).
  - **Checkbox:** Is / Is not, com os valores Checked / Unchecked
- **Operadores em pt-BR:** não achei a tradução oficial. Os prováveis seriam "é", "não é", "contém", "não contém", "começa com", "termina com", "está vazio", "não está vazio" **[não confirmado]**.
- **Filtro simples × avançado** **[oficial]**:
  - `Add advanced filter` / **"Adicionar filtro avançado"**. Combina **AND/OR** em grupos de filtros, com até **3 níveis** de aninhamento.
  - Em pt-BR os operadores lógicos são **"E" / "OU"**.
  - Um filtro simples vira avançado por `••• → Add to advanced filter`.
  - O guia chama de "Simple Filter" o que mira uma propriedade e de "Advanced Filter" um conjunto de filtros ou grupos.
- **Como os filtros ativos aparecem.** A ajuda oficial não usa a palavra "pill". Os guias mostram cada filtro ativo como uma pílula na barra abaixo das abas de view, e cada uma abre seu editor ao clicar. Não achei fonte para o formato "Status: Done, In progress" nem para um contador de filtros **[não confirmado]**.
- **Remover um filtro.** `••• → Delete filter`, em pt-BR **"Excluir filtro"** **[oficial]**.
- **A view lembra os filtros?** Sim. O filtro novo vale **só para você** até clicar `Save for everyone` (**"Salvar para todos"**). `Reset` descarta a mudança. **[oficial + guia]**
  - pt-BR: "Filtros rápidos" e o menu "Opções de visualização" (https://www.notion.com/pt/help/guides/databases-reimagined-whats-changed).
  - Não achei o pt-BR de "Reset"; "Redefinir" é provável **[não confirmado]**.

### 2. Ordenação (Sort)
- **Onde fica.** `Sort` em `View settings`, depois a propriedade. Em pt-BR: **"Ordenar"** em "Configurações de visualização"; a seção da ajuda se chama "Ordenações". O texto oficial diz "em ordem **crescente** ou **decrescente**". **[oficial]** https://www.notion.com/pt/help/views-filters-and-sorts
- **Direções.** Em inglês, `Ascending` / `Descending`. Em pt-BR, **Crescente / Decrescente**: os termos aparecem no texto da ajuda, mas não achei captura do menu.
- **Várias regras.** Cada uma tem prioridade e se reordena **arrastando pelo ícone `⋮⋮`** ("arrastando-as para cima ou para baixo usando o ícone ⋮⋮"). Remove-se pelo **`X`** ao lado da regra. `Save for everyone` / "Salvar para todos" vale como no filtro. **[oficial]**
- **Selects.** Em Select e Multi-select, a ordem segue a ordem das opções da propriedade ("you get to define what sorting order means") **[oficial]**.
- **Setas.** Não achei fonte sobre o ícone da pílula de ordenação: ↑↓ com o nome da propriedade, ou "N sorts" quando há várias regras **[não confirmado]**.

### 3. Densidade e largura
- **Full width.** `•••` no canto superior direito da página → `Full width`, que "shrink the margins … widen your content area" **[oficial]**.
- **Small text.** No mesmo menu `•••` → `Small text`: "the text on your page shrinks… fit more on a page". As fontes da página são `Default`, `Serif` e `Mono`. **[oficial]** https://www.notion.com/help/customize-and-style-your-content
- **Tamanhos.**
  - Corpo de 16px, Small text de cerca de 14px, e coluna padrão de cerca de 708px (contêiner de 900px menos 96px de margem de cada lado) **[não confirmado]**: é medição conhecida, não documentação.
  - Linhas de tabela: não há controle de altura. A altura só cresce com a quebra de texto, partindo de cerca de 33px **[não confirmado]**.
- **Quebra de texto.**
  - Por coluna: o cabeçalho mostra o toggle `Wrap column` (https://www.notion.com/releases/2022-04-14) **[oficial]**.
  - Para todas as colunas: `Wrap all columns`, ao lado de `Show vertical lines`, em `••• → Layout` **[guia]** https://allthings.how/how-to-wrap-text-in-a-notion-table/
  - A ajuda geral fala em "Wrap text"; em pt-BR, **"Quebrar texto"** (https://www.notion.com/pt/help/tables).

### 4. Agrupamento
- Fica no mesmo menu, junto de Filter e Sort: **`Group`** / **"Agrupar"**, e **`Sub-group`** / **"Subgrupo"** **[oficial]**.
- Opções: esconder ou mostrar cada grupo, ordem manual ou alfabética dos grupos, `Hide empty groups` / **"Ocultar grupos vazios"**, e `Remove grouping` / **"Remover agrupamento"** **[oficial]**.
- O menu lista ainda `Layout` e `Property visibility` / "Visibilidade da propriedade".

### 5. Rótulos de ordenação em outros apps
- **Airtable.** Texto `A → Z` / `Z → A`; número `1 → 9` / `9 → 1`; data também `1 → 9` (mais antiga primeiro) / `9 → 1`; select `First → Last` / `Last → First`. https://support.airtable.com/docs/sorting-records-in-airtable-views
- **Linear.** O menu "Display options" tem "Ordering" com Manual, Status, Priority, `Last created`, `Last updated`, `Due date`, Link count, mais um botão que inverte a direção. https://linear.app/docs/display-options
- **GitHub.** O dropdown "Sort" traz `Newest`, `Oldest`, `Most commented`, `Least commented`, `Recently updated`, `Least recently updated`. https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/filtering-and-searching-issues-and-pull-requests
- **Gmail.** Na busca, alterna entre `Most relevant` e `Most recent`; em pt-BR, "Mais relevantes" / "Mais recentes" **[não confirmado]**. https://blog.google/products-and-platforms/products/gmail/gmail-search-update-relevant-emails/
- **O que se repete:**
  - a pílula curta mostra **propriedade + seta**;
  - o menu explica a direção em palavras ("mais antiga primeiro", "1 → 9");
  - para datas, os apps preferem texto ("Newest/Oldest") a "crescente", que é ambíguo em data.

*(Seção "Proposta: 5 rótulos de ordenação para a lista de pendências" omitida — ver o cabeçalho.)*

Fontes:
- https://www.notion.com/help/views-filters-and-sorts
- https://www.notion.com/pt/help/views-filters-and-sorts
- https://www.notion.com/pt/help/guides/databases-reimagined-whats-changed
- https://www.notion.com/help/customize-and-style-your-content
- https://www.notion.com/help/tables
- https://www.notion.com/pt/help/tables
- https://www.notion.com/releases/2022-04-14
- https://thomasjfrank.com/notion-databases-the-ultimate-beginners-guide/
- https://thomasjfrank.com/formulas/formulas-in-database-filters/
- https://developers.notion.com/reference/post-database-query-filter
- https://allthings.how/how-to-wrap-text-in-a-notion-table/
- https://support.airtable.com/docs/sorting-records-in-airtable-views
- https://linear.app/docs/display-options
- https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/filtering-and-searching-issues-and-pull-requests
- https://blog.google/products-and-platforms/products/gmail/gmail-search-update-relevant-emails/
