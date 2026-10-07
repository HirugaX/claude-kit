# Catálogo — os recursos, com o gatilho de cada um

Material da skill `recursos-do-projeto`. Ler a seção que a ficha precisa, não o arquivo inteiro.
Evidência: **Doc** = documentação oficial conferida em 04/10/2026 · **A** = teste controlado ou reproduzível ·
**B** = teste observável · **C** = relato · **D** = afirmação do fornecedor. Estrelas no GitHub não são qualidade.

## 1. O núcleo — todo projeto

| Recurso | Pronto quando | Evidência |
|---|---|---|
| **`CLAUDE.md` curto**: comandos, invariantes, "nunca/sempre", onde mora cada documento | menos de 200 linhas; nenhuma frase de estado ("a próxima fase é…"); nenhum histórico | Doc (*"target under 200 lines… reduce adherence"*); A: de 25 a 500 linhas não se mediu efeito na aderência — o custo em token é certo |
| **Handoff curto + histórico à parte** | a janela nova sabe onde está lendo só o handoff (estado, fila, decisões abertas, o próximo prompt); o histórico é lido por busca | C/D (Anthropic Engineering: arquivo de progresso + contexto novo funciona melhor que compactar) |
| **Testes desde o primeiro commit**, o comando do laço rápido no `CLAUDE.md` | toda regra nova nasce com o teste; nas críticas, a mutação conferida (o teste cai quando a regra quebra) | prática do DESOSP; Doc (verificação é o que mais rende no esforço alto) |
| **Gancho de abertura** (`SessionStart`) | o resumo do que a janela precisa saber (git, caixa, fase, esforço e modelo) entra sem ninguém lembrar e sem ler arquivo inteiro | Doc (ganchos); modelo pronto: `C:\CLAUDE-PROJETOS\desosp-app\.claude\hooks\abertura.py` |
| **Modelo e esforço por tipo de tarefa** | cada fase com modelo e esforço escritos, e o `/effort` explícito na 1ª linha do prompt | skill `uso-do-claude` §3 |
| **Leitura volumosa por subagente** | busca, varredura, log e documentação longa voltam como conclusão, não como arquivo | Doc (o Explore não carrega o `CLAUDE.md`; modelo por parâmetro) |

## 2. Os condicionais — gatilho → recurso

### 2.1 Contexto e jeito de trabalhar

| Gatilho (resposta da entrevista ou achado do inventário) | Recurso | Custo e risco |
|---|---|---|
| há domínios com regras próprias (tela, dados, testes, migração) | `.claude/rules/<domínio>.md` com `paths:` — carrega só ao ler ou editar arquivo que casa | baixo; regra sem `paths:` carrega sempre (é `CLAUDE.md` com outro nome) |
| procedimento de vários passos que se repete 3 vezes ou mais | skill do projeto | baixo; dezenas de skills que se sobrepõem atrapalham a escolha |
| decisão com alternativas reais e consequência longa | registro de decisão curto (`docs/adr/`) | burocracia se usado para detalhe |
| vários repositórios que conversam | caixa de entrada em arquivo, lida ao abrir (o modelo DESOSP: `docs/para_o_<projeto>/`, um arquivo por envio) | mensagem entre sessões custa o contexto inteiro de quem recebe; arquivo não |
| outro agente (Codex, Cursor) no mesmo repositório | `AGENTS.md` com a parte portátil; `CLAUDE.md` só com o específico do Claude | a mesma regra nos dois diverge |
| sessão longa sem supervisão | objetivo verificável, `/goal`, política de falha, commit por checkpoint | skill `uso-do-claude` §8 |
| janelas em paralelo no mesmo repositório | `worktree`, ou arquivos disjuntos e commit por caminho | o gancho de abertura mostra arquivo modificado de outra janela |

### 2.2 Verificação determinística — o comando no lugar do raciocínio

Um comando que responde "linha 43 viola X" vale mais que o modelo tentar provar de cabeça que não há erro. E é a
verificação que **permite descer de modelo e de esforço** (skill `uso-do-claude` §1).

| Gatilho | Recurso | Custo e risco |
|---|---|---|
| Python | **Ruff** (`ruff check` com F e E9 no mínimo) no laço rápido | muito baixo; formatar o projeto existente inteiro vira um diff gigante — formatador só em projeto novo |
| TypeScript | typecheck + lint do ecossistema como portão | baixo |
| tela web | **testes no navegador** (Playwright) para o fluxo real: layout, foco, teclado, impressão, fotos confiáveis | baixo a médio; em Python, o pacote `playwright` pode usar o navegador já instalado (`channel="msedge"`) sem baixar outro |
| tela web | **axe-core** dentro dos testes de navegador: a parte objetiva da acessibilidade (contraste, rótulos, papéis) | baixo; cobre só parte do WCAG — o resto é olho |
| tela com componentes | catálogo de componentes com **todos os estados** (Storybook em React; uma página `/kit` quando o servidor renderiza) | médio; amostra escolhida a dedo não mostra o estado que quebra |
| comportamento em JavaScript | teste que **executa** o JS (navegador, ou o Node sobre um DOM) | assert sobre o HTML servido prova a marcação, não o comportamento |
| importa arquivos (XLS, CSV, PDF) | fixtures, invariantes (contagens, totais), arquivos-gabarito | médio; o erro de importação é silencioso |
| há segredos (chaves, tokens) | **Gitleaks** no pre-commit ou no CI | baixo |
| dado pessoal ou de saúde | varredura própria do que não pode ir ao git (nomes, identificadores), como teste | nenhuma ferramenta pronta conhece os nomes do seu domínio |
| exposto à internet | **Semgrep** no CI | baixo a médio |

### 2.3 Interface

| Gatilho | Recurso | Por quê |
|---|---|---|
| o design existe no Figma | Figma MCP | frames, variáveis e componentes em vez de descrição em texto |
| sem Figma | a fonte de verdade visual é o documento de design + os tokens + o catálogo | MCP não substitui decisão de design |
| React | shadcn/ui + Radix + Tailwind, **com os tokens definidos antes** | sem tokens, vira o "app shadcn genérico" |
| o servidor renderiza (Jinja2, Django) | kit de macros sobre tokens CSS; componente nativo (`<details>`, `<dialog>`) antes de JS próprio | shadcn e Radix são React; Tailwind pede build |
| a máquina de uso não tem internet | tudo vendorizado, nada de CDN, fontes locais | — |
| tela densa de trabalho (tabelas, filtros, estados) | uma skill de revisão de tela do projeto, com a prova de cada ponto (o modelo: `revisar-tela` do app DESOSP) | densidade controlada, estados visíveis, ação perto do objeto, retorno imediato, navegação previsível |

**Nenhum MCP substitui julgamento de UX.** As ferramentas conferem a implementação; a revisão de tela confere o
que dá para provar; o usuário julga o resto.

### 2.4 Navegador — CLI (testes) × MCP

| Cenário | Testes / CLI | Playwright MCP | Chrome DevTools MCP |
|---|---|---|---|
| teste repetível, regressão permanente, CI | **melhor** | médio | ruim |
| economia de contexto | **melhor** | pior | pior |
| navegação exploratória com estado | bom | **melhor** | ótimo |
| console, rede, desempenho | limitado | bom | **melhor** |

Padrão: testes. MCP de navegador só na janela de depuração que precisa dele, desligado depois.

### 2.5 Produção e segurança

| Gatilho | Recurso | Quando NÃO |
|---|---|---|
| produção com usuários e o dado pode sair da máquina | Sentry (+ o MCP dele, para o Claude ler o erro real em vez do relato) | dado de saúde ou pessoal que não pode sair; máquina sem internet |
| dado que não pode sair, ou sem internet | log local com rotação, sem dado pessoal na mensagem; o Claude lê o log | — |
| vários serviços distribuídos | OpenTelemetry | app único: infraestrutura sem retorno |

### 2.6 Informação de fora — MCP e CLI

Regra: **CLI antes de MCP** para o que é determinístico (git, testes, lint, navegador em teste). Um MCP traz
descrições, esquemas e resultados grandes (árvore de acessibilidade, páginas) para o contexto; use-o para estado
externo ou introspecção interativa. Servidor "de referência" do repositório oficial de MCP é exemplo
educacional, não produção.

| Gatilho | Recurso | Cuidado |
|---|---|---|
| o Claude precisa ler PRs, issues, Actions | `gh` (CLI); GitHub MCP oficial em modo só leitura se precisar de mais | credencial; injeção de prompt em conteúdo externo |
| depende de API externa que muda (SDK novo, autenticação, configuração) | Context7 (CLI + skill), com o `libraryId` e a versão | índice com conteúdo da comunidade e backend fechado: em migração, autenticação e criptografia, conferir a documentação primária |
| depuração interativa de navegador | Chrome DevTools MCP, só naquela janela | acesso amplo ao navegador; nunca numa sessão com dado sensível aberto |
| plugins e MCPs ligados que o projeto não usa | desligar | as descrições das skills deles entram em toda sessão |

## 3. Dados — a árvore

```
aplicação transacional
  ├─ um usuário, local, sem servidor .................. SQLite
  └─ vários escrevendo ao mesmo tempo, relacional ...... PostgreSQL
        ├─ quer autenticação, storage e tempo real prontos .. Supabase
        └─ scale-to-zero ou banco por ramo é requisito ...... Neon
analisar CSV, Parquet, joins e agregações grandes ...... DuckDB (nunca como banco transacional)
dataframes: compatibilidade ........................... pandas
dataframes: volume, colunar ........................... Polars
.xlsx que precisa preservar fórmula e formatação ...... biblioteca XLSX própria (openpyxl)
planilha como interface para gente
  ├─ automação dentro da planilha ...................... Apps Script
  ├─ programa de fora lendo e escrevendo ............... Sheets API
  └─ relações + concorrência + integridade + histórico . banco, não planilha (o Google sugere migrar perto de 10 milhões de células)
```

Firebase só como escolha deliberada: muda o modelo da arquitetura, não só a hospedagem.

## 4. Os "não"

| Prática | Por que não |
|---|---|
| 15 a 30 MCPs sempre ligados; plugins sem uso | contexto, superfície de ataque, escolha de ferramenta pior |
| `CLAUDE.md` enciclopédia; estado e histórico dentro dele | custo em toda chamada; o estado envelhece e contradiz o handoff |
| handoff que só cresce | a janela não sabe o que ainda vale; ler o alto vira ler um parágrafo de 40 linhas |
| Opus ou Fable para tudo; `xhigh`/`max` como padrão | custo e espera sem retorno em tarefa simples (skill `uso-do-claude` §2) |
| enxame de agentes por padrão (planejador, arquiteto, backend, frontend, segurança, testador, revisor) | repasses e inferências repetidas; revisores do mesmo modelo erram juntos |
| vetorizar o código antes de um problema medido | o Claude Code já busca no código sozinho |
| captura de tela como única prova de interface; "parece certo" | não pega foco, teclado, layout em outra largura, impressão |
| Context7 sem conferir a fonte primária em coisa crítica | conteúdo da comunidade, backend fechado |
| instalar o que a pesquisa listou | a pergunta é qual problema deste projeto cada um resolve |
| ferramenta que manda o dado para fora (SaaS de erro, MCP de terceiro) em projeto com dado de saúde | sigilo |
| lembrete em texto onde cabe controle (permissão, gancho, teste) | texto é orientação; o controle é o que vale (skill `uso-do-claude` §11) |
