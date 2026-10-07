# Referência — fontes, medições e correções (03/10/2026)

Material de apoio da skill `uso-do-claude` e das peças dela (`modelo-e-esforco`, `fechar-janela`, `pesquisa`,
`orquestrar`); as seções citadas como §N nos textos antigos são as da `uso-do-claude` de antes do F2a (07/10). Ler quando precisar justificar uma regra, conferir
se um fato ainda vale, ou recalibrar com dados novos.

## 1. Fatos verificados na documentação oficial em 03/10/2026

Lidos direto das páginas (não de memória), com a frase que sustenta cada um.

| Fato | Fonte |
|---|---|
| Padrão de esforço: `high` em todo modelo, **exceto Opus 5.5 e Sonnet 5.5 (`medium`)** e Opus 4.7 (`xhigh`) | [model-config](https://code.claude.com/docs/en/model-config) |
| *"Opus 5.5 at medium matches or exceeds Opus 5 at high on coding and knowledge-work evaluations. At a given level, Opus 5.5 tends to think more per turn than Opus 5. When you move from Opus 5 to Opus 5.5, start at medium rather than carrying over the level you used on Opus 5."* | model-config |
| O `effortLevel` de topo no `settings.json` **não vale para o Opus 5.5**; o nível fica por modelo em `modelSettings` | model-config |
| `max` vale só para a sessão (salvo `CLAUDE_CODE_EFFORT_LEVEL`); *"may show diminishing returns and is prone to overthinking, so test before adopting it broadly"* | model-config |
| Esforço maior: *"tested more edge cases and verified more of its work… It also made more choices on its own"* | model-config |
| `ultracode` é configuração, não nível; `--effort ultracode` liga e põe `xhigh`; `/effort ultracode` mantém o nível (v2.1.284+; antes punha `xhigh`) | model-config |
| `ultrathink` no prompt: *"adds an in-context instruction. The effort level sent to the API is unchanged"* — vale um turno | model-config |
| `opusplan`: Opus no modo plano, Sonnet na execução; cada alternância é troca de modelo (cache recomeça) | model-config, [prompt-caching](https://code.claude.com/docs/en/prompt-caching) |
| **Mudar o esforço mantém o cache** no Opus 5.5, Sonnet 5.5 e Fable 5.1 (assinatura ou chave de API); em outros modelos, quebra | prompt-caching |
| **`/model` quebra o cache**: a chamada seguinte relê a conversa inteira | prompt-caching |
| Cache dura 1 h na assinatura; 5 min com créditos avulsos | [costs](https://code.claude.com/docs/en/costs) |
| *"Claude Code sends your full conversation with every request… a one-line question in a session that has been open all day still draws usage for the whole conversation"* | costs |
| Compactar contexto grande é uma chamada grande; `/clear` não custa nada | costs |
| Agent teams: ~7× tokens com os colegas em modo plano | costs |
| `CLAUDE.md`: *"target under 200 lines… Longer files consume more context and reduce adherence"*; aviso na abertura e no `/status`; regras com `paths:` carregam só ao mexer nos arquivos; skills carregam sob demanda | [memory](https://code.claude.com/docs/en/memory), costs |
| `MEMORY.md`: só as primeiras 200 linhas ou 25 KB carregam | memory |
| Skill: campos `model` e `effort` no cabeçalho valem **só para o turno** em que a skill roda; `disable-model-invocation: true` = só por `/nome` | [skills](https://code.claude.com/docs/en/skills) |
| Subagente: modelo por parâmetro > definição > `CLAUDE_CODE_SUBAGENT_MODEL` > o da janela; o Explore não carrega `CLAUDE.md`; `effort` herda da sessão salvo definição | [sub-agents](https://code.claude.com/docs/en/sub-agents) |
| `/goal`: um avaliador confere a condição depois de cada turno; não roda comandos, julga pelo que a conversa mostra | [goal](https://code.claude.com/docs/en/goal) |
| Modo auto: classificador aprova ações; padrão de abertura no terminal e no VS Code a partir da v2.1.283 | [permission-modes](https://code.claude.com/docs/en/permission-modes) |
| `/doctor prompt-audit`: confere `CLAUDE.md`, rules, skills etc. e propõe edições sem aplicar; *"requires Claude Code v2.1.283 or later"* | memory |
| `@import` não economiza: *"imported files also load at launch"*; regra com `paths:` carrega quando o Claude usa Read, Write ou Edit num arquivo que casa | memory |
| Preço por MTok: Opus 5.5 US$ 4 / 20, **leitura de cache US$ 0,20 (0,05×)**; Sonnet 5.5 US$ 2 / 10, **leitura de cache US$ 0,20**; Fable 5.1 US$ 10 / 50, leitura 0,025×; Haiku 4.5 US$ 1 / 5 | [pricing](https://platform.claude.com/docs/en/about-claude/pricing) |

Fornecedor, não independente: [Spending your effort](https://claude.dev/blog/spending-your-effort/)
(Thariq Shihipar, 25/09/2026). O mesmo pedido levou 1,5 min em `low`, 4 em `medium`, 11 em
`high` e 67 em `max`; esforço maior ajuda *"tasks with lots of hidden edge cases"* mas *"does
not fix when the model has the wrong approach"*. Ciclo sugerido: entrevista sobre a
especificação → implementar em `low` → verificar e testar em `high`.

## 2. A pesquisa de 03/10 (`fontes/claude-uso-modelos.md`) — o que se confirmou

| Afirmação da pesquisa | Verificação |
|---|---|
| Opus 5.5 e Sonnet 5.5 com padrão `medium`; `max` não é padrão | confirmada |
| `ultracode` não é nível acima de `max` | confirmada (e o comportamento mudou na v2.1.284) |
| `ultrathink` é artefato histórico, não existe mais | **errada**: existe, vale um turno, não muda o esforço |
| Mudar o esforço invalida o cache | **errada para Opus 5.5, Sonnet 5.5 e Fable 5.1** na assinatura; certa para os outros |
| Leitura de cache igual em Opus 5.5 e Sonnet 5.5 | confirmada na tabela de preços |
| Janela curta nem sempre economiza | confirmada; e no uso medido, 72–88% do volume é conversa acumulada (abaixo) |
| Não cita o `opusplan` | existe |
| Números da Artificial Analysis e benchmarks Opus × Fable | ver §4 |

## 2b. A pesquisa de 04/10 (`C:\CLAUDE-PROJETOS\claude-kit\fontes\claude-efficiency-report.md`) — o que se confirmou

Uma pesquisa sobre stack e recursos (contexto, skills, ganchos, MCPs, interface, dados, verificação),
virada na skill `recursos-do-projeto`. Conferida em 04/10/2026: um subagente leu as páginas e citou; o que
sustenta regra foi relido direto (model-config e settings-reference). As citações da pesquisa (`citeturn…`)
não têm endereço: não servem de fonte.

| Afirmação da pesquisa | Verificação |
|---|---|
| `CLAUDE.md` com menos de 200 linhas; regra com `paths:` só carrega ao mexer no arquivo | confirmada (memory): *"Rules without a `paths` field are loaded unconditionally… Path-scoped rules trigger when Claude uses the Read, Write, or Edit tool on a file matching the pattern"* |
| subagente com modelo, ferramentas, skills, memória e esforço próprios | confirmada (sub-agents): `name`, `description`, `tools`, `disallowedTools`, `model`, `permissionMode`, `maxTurns`, `skills`, `mcpServers`, `hooks`, `memory`, `background`, `omitClaudeMd`, `effort`, `isolation`, `color`, `initialPrompt` |
| "o Explore pode usar Haiku" | **em parte**: o padrão é *"the main conversation's model"*; Haiku só pelo parâmetro `model` ou por um subagente próprio chamado `Explore` com `model: haiku` (*"overrides the built-in and keeps its own model field"*) |
| subagente retomado mantém contexto e cache | confirmada com ressalva: pelo `SendMessage`, *"retain their full conversation history"*; o cache do subagente dura *"five minutes even on a subscription"* |
| MCP põe esquemas grandes no contexto | **desatualizada para o Claude Code**: *"MCP tool definitions are deferred by default, so only tool names and server instructions enter context until Claude uses a specific tool"* (costs). O **resultado** continua pesando |
| Playwright: CLI + skills gasta menos contexto que o MCP | confirmada, palavra por palavra (README do `microsoft/playwright-mcp`): *"Modern coding agents increasingly favor CLI–based workflows exposed as SKILLs over MCP because CLI invocations are more token-efficient: they avoid loading large tool schemas and verbose accessibility trees into the model context"*. O CLI oficial: `@playwright/cli` (npm), `playwright-cli install --skills` |
| Sonnet 5.5 como padrão; Opus sob escalada | **em parte**: *"Sonnet handles most coding tasks well and costs less than Opus. Reserve Opus for complex architectural decisions or multi-step reasoning"* (costs); mas o padrão do Claude Code nos planos pagos é o Opus 5.5, e no índice da AA o Opus 5.5 `low` empata ou supera o Sonnet 5.5 `medium` pelo mesmo custo (§4). Na skill: Sonnet onde há verificação que pega o erro |
| preços (Sonnet 5.5 2/10, Opus 5.5 4/20, Haiku 4.5 1/5) | confirmados (§1) |
| Sonnet 5.5 >30% mais rápido e ~30% mais barato por tarefa que o Sonnet 5 | fornecedor (D); não conferido |
| ganchos bloqueiam ou pedem aprovação, inclusive em chamada MCP | confirmada (hooks) |
| skills: a descrição sempre, o conteúdo sob demanda | confirmada, com um dado novo: a lista ocupa ~1% da janela e, quando estoura, *"Claude Code drops some descriptions"* |
| fichas de ferramenta (Context7, GitHub MCP, Figma, Storybook, axe, Sentry, bancos…) | não são do Claude Code; a evidência de cada uma, com a classe, está no `catalogo.md` da skill `recursos-do-projeto` |

**Achados ao conferir, que não estavam em pesquisa nenhuma:**

| Fato | Fonte |
|---|---|
| o `/effort` **grava**: *"`Enter` in the `/effort` slider or the `/model` picker, or a level typed after `/effort`: save the level as your default and apply it in later sessions"*; *"`s`… apply the level to this session only. Requires Claude Code v2.1.257 or later"*; *"Claude Code saves the level per model, under the `modelSettings` key in your user settings"*; o seletor do VS Code grava igual | model-config, settings-reference |
| `modelSettings` em vários arquivos: *"Across files, Claude Code resolves each model separately: the highest-precedence settings file that sets either an `effortLevel` for that model or a top-level `effortLevel` that applies to that model decides"* — o do projeto vence o do usuário | settings-reference |
| o `sonnet` por fornecedor: na API da Anthropic, Sonnet 5.5; no Bedrock e no Agent Platform, Sonnet 4.5; na AWS Platform, Sonnet 4.6 — e o medido no Claude Code 2.1.234 foi o Sonnet 5 (§3). Escolher na lista | model-config |
| o `SessionStart` recebe `source`, `model` (*"It can be omitted, for example after `/clear`"*), `agent_type`; o que ele imprime em texto vai ao contexto do Claude | hooks |
| o `PostToolUse` com saída 0 escreve só no log de depuração; para o Claude ver: saída 2 (stderr) ou `additionalContext` | hooks |
| a statusline recebe `model.id`, `model.display_name` e `effort.level` (*"Reflects the live session value"*) | statusline |

**Provas por sessão nova (`perguntas_controle.py`, 04/10, Sonnet 5.5):** duas perguntas pós-`/grill-me`
(projeto novo; implementação nova num projeto existente) — as **duas** sessões chamaram a
`recursos-do-projeto` sozinhas, uma citando a linha do `CLAUDE.md` pessoal (US$ 0,92 as duas). E uma sessão
aberta em `C:\DESOSP_APP` copiou o texto do gancho de abertura: ele roda no Windows (Git Bash) e chega ao
contexto também no `-p` (US$ 0,17).

## 3. O uso medido (registros locais, só números)

Pesquisa original: `fontes/claude-uso-modelos.md` (nesta pasta). Medido com `medir_uso.py` (hoje em `claude-kit\scripts\`) em 03/10/2026. Rodar de novo para atualizar.

| Projeto | Chamadas | Contexto médio | Parte fixa | Chamadas ≥ 400k | Custo de abrir a janela | US$ (equiv. API) |
|---|---:|---:|---:|---:|---:|---:|
| DESOSP (kernel), 19/08–03/10 | 6.137 | 354k | 25% | 34% | 33k (19/08) → 128k (03/10) | 809 |
| DESOSP (kernel), desde 23/09 | 2.507 | 401k | 28% | 41% | ~125k | 371 |
| DESOSP_APP | 2.183 | 360k | 15% | 37% | ~55k | 392 |
| planilha-hc | 806 | 450k | 12% | 52% | ~55k | 173 |

- Quase tudo em Opus (5 e 5.5), com o Opus 5.5 gravado em `xhigh`. Sonnet: 75 de 9.126
  chamadas. Fable: ~410 chamadas, ~3× o custo por chamada do Opus 5.5.
- Compactação quase nunca usada; subagente raro e quase sempre herdando o Opus.
- O `CLAUDE.md` do kernel (2.602 linhas, 178 KB) responde por ~75 mil tokens de cada chamada.
  **Depois do KN42 (03/10)**, num A/B limpo (a mesma sessão `claude -p`, o mesmo modelo, só o
  arquivo trocado), o contexto da 1ª chamada caiu de **138 mil para 69 mil**.
- Visto nos registros (03/10, Claude Code 2.1.234): `--model sonnet` rodou como `claude-sonnet-5`,
  e não como `claude-sonnet-5-5`. A janela de 01/10, com o modelo escolhido na lista, rodou como
  `claude-sonnet-5-5`.
- Conclusão: o maior custo é o contexto acumulado; depois, o esforço; por último, o modelo.

**Medido de novo em 04/10** (`medir_uso.py --desde 2026-09-30 --sessoes`, só números):

- DESOSP_APP, 30/09–04/10: 781 chamadas, contexto médio 230k, parte fixa 25%, `ctx0` de 54k a 63k;
- 🛑 a FF-P3c do app (03/10, 19h–20h) rodou **as 188 chamadas no `claude-sonnet-5`**; o prompt e o registro
  da janela dizem "Sonnet 5.5 · medium". A armadilha do atalho já estava na skill desde as 13h;
- 🛑 o `settings.json` do usuário tinha `claude-opus-5-5: xhigh` às 00h08 de 04/10 e `high` às 00h15 (um
  `/effort` confirmado numa janela): é o mecanismo do *"Opus 5.5 gravado em `xhigh`"* da tabela acima e da
  contradição *"padrões do settings.json diferentes do que os documentos dizem"* (§4b);
- o app tinha, em 04/10: `CLAUDE.md` de 335 linhas (22 KB) e `HANDOFF_APP.md` de 538 KB (6.351 linhas); o
  kernel, `CLAUDE.md` de 413 linhas (depois do KN42) e `HANDOFF_SPRINT2.md` de 315 KB.

## 4. Evidência independente (internet, 03/10/2026)

Classes: A = teste controlado/reproduzível · B = teste observável · C = relato · D = fornecedor.
O Reddit não pôde ser aberto diretamente; o que vem de lá chegou por blogs, HN e resumos (C).

| Achado | Classe | Fonte |
|---|---|---|
| Índice da Artificial Analysis confirmado: Sonnet 5.5 low→max 36/41/47/52/56 (US$ 0,42 / 0,59 / 1,12 / 2,75 / 7,67 por tarefa); Opus 5.5 low 42 (0,55), **medium 51 (1,34)**, high 54 (1,82), xhigh 56 (3,46), max 58 (5,98). Opus `medium` ≈ Sonnet `xhigh` pela metade do custo | A | [AA Sonnet 5.5](https://artificialanalysis.ai/models/releases/claude-sonnet-5-5), [AA Opus 5.5](https://artificialanalysis.ai/models/releases/claude-opus-5-5) |
| Latência: Sonnet `medium` ~6,7 s × Opus `low` ~14,9 s (500 tokens) | A | [AA comparação](https://artificialanalysis.ai/models/comparisons/claude-sonnet-5-5-medium-vs-claude-opus-5-5-low) |
| FrontierCode: Sonnet 5.5 52,1% em `xhigh` × 46,2% em `max` (mais revisões por subagente, timeout, edição fora do escopo) | D | [Sonnet 5.5](https://www.anthropic.com/claude-sonnet-5-5), nota 2 |
| Sonnet 5.5 em `max` esgotou 128K de saída sem responder; `xhigh` resolveu por 5,7¢ | B | [Simon Willison](https://simonwillison.net/2026/Sep/28/claude-sonnet-5-5/) |
| Opus 5.5 > Fable 5.1 em código: 66,4 × 55,8 (Terminal-Bench 4.0), 54,4 × 50,3, 57,8 × 51,8; independente: Vals 65,15 × 58,08 | D / A | [Opus 5.5](https://www.anthropic.com/claude-opus-5-5), [Vals TB4](https://www.vals.ai/benchmarks/terminal-bench-4) |
| Tarefas bem delimitadas (48 execuções): Sonnet 5.5 `medium` e Opus 5.5 `medium` 12/12 cada; Sonnet US$ 0,88 × 1,91, mais rápido | A | [wmedia.es](https://wmedia.es/en/tips/claude-code-sonnet-5-5-vs-opus-5-5-benchmark) |
| Julgamento jurídico às cegas: Opus 5.5, Opus 5 e Fable 5.1 indistinguíveis; Opus 5.5 pela metade do custo do Fable | B | [HAQQ](https://www.haqq.ai/blog/claude-opus-5-5-legal-benchmark) |
| Acerto factual (AA-Omniscience): Opus 5.5 66%, Fable 5.1 67%, Sonnet 5.5 54% | A | Artificial Analysis |
| Agente longo: compactar "isn't sufficient"; arquivo de progresso + contexto novo funciona melhor | C/D | [Anthropic Engineering](https://anthropic.com/engineering/effective-harnesses-for-long-running-agents) |
| Seguir instrução cai ~5,6% por função a mais gerada na mesma sessão (1.650 sessões, modelos 4.6, análise post-hoc) | A (modelos antigos) | arXiv 2605.10039 |
| `CLAUDE.md` de 25 a 500 linhas: nenhum efeito detectável na aderência; acima de 500, não testado. O custo em token é certo | A | arXiv 2605.10039 |
| Subagentes em tarefa pequena: 2,6× a 5,9× mais entrada, sem ganho de tempo | A/B | [Systima](https://systima.ai/blog/subagent-tax) |
| Workflows/ultracode: o aviso de workflow grande é desligado; até 1.000 agentes. Revisão ultracode do app (F2): 165 agentes, 13,4M tokens, ~52 min, cortada pelo limite de sessão | D / medido | [workflows](https://code.claude.com/docs/en/workflows) |
| Fable no Max: até 50% da cota semanal; gasta a cota mais rápido que os outros | D | [suporte](https://support.claude.com/en/articles/15424964-claude-fable-models-on-your-plan) |
| Advisor (experimental): com Sonnet na janela, `/advisor opus` consulta o Opus nos pontos de decisão; ligar não quebra o cache | D | [advisor](https://code.claude.com/docs/en/advisor) |

Lacunas: nenhum teste controlado de `opusplan` na geração 5.5; nenhum de compactação ×
handoff na 5.5; nenhum de qual modelo conduz melhor uma entrevista (`/grill-me`); nada
específico de texto clínico em português. Desde 04/10: nenhum teste de se um `modelSettings` no
`settings.json` do projeto atrapalha um `/effort` no meio da janela.

## 4b. O que a varredura dos três projetos mostrou (03/10)

- Kernel: fase E = Opus `xhigh` "nas 2 próximas rodadas, depois alto" — nunca desceu; fase C =
  Sonnet escrita, **0 de 289 commits do kernel em Sonnet**; E e C juntas na mesma janela em ao
  menos 7 rodadas, a pedido do Ettore ("tudo numa janela", "o censo antes de tudo").
- Incidente antigo (era V6.6, outro produto): *"Esforço médio já produziu substituição em vez de
  merge no censo de 31/07 M"* — o motivo para não descer a `medium` em regra de dado clínico.
- App: Fable para desenho e revisão de texto, Opus `xhigh` nas fases de erro silencioso,
  `high` nas de erro visível; Ettore, 28/09: *"use o Fable só para o que ele tiver realmente
  diferencial"*; cota acompanhada (69% semana / 43% Fable em 28/09).
- planilha-hc: nenhuma tabela de modelo; só a instrução legada "Opus em esforço alto, sessão
  dedicada, hospitais em lotes de 3; documentos e discussão de regras: Sonnet".
- Contradições a resolver em cada projeto: "máximo" ambíguo (`max` × `xhigh`); revisão
  adversarial `max` no kernel × `ultracode` no app; o app proíbe mudar esforço depois do plano
  aprovado (no Opus 5.5 isso não quebra cache nem contexto); padrões do `settings.json` diferentes
  do que os documentos dizem.

## 5. Como recalibrar com dados próprios

O que falta na literatura é comparar estratégias no mesmo projeto. Experimento mínimo:

1. Duas tarefas reais congeladas por commit: uma curta e modular, uma longa e com estado
   (importação com reconciliação, ou regra com data e identidade).
2. Rodada 1: modelo e esforço fixos (Opus 5.5 `medium`), variar a estratégia de sessão —
   contínua; contínua com `/compact` em pontos naturais; janelas por fase com handoff;
   principal + subagentes.
3. Rodada 2: a melhor estratégia fixa, variar modelo e esforço (Sonnet 5.5 `medium`/`high`,
   Opus 5.5 `low`/`medium`/`high`). Nunca as duas variações na mesma rodada.
4. Três execuções por condição. Medir: testes de aceitação, `medir_uso.py --sessoes`
   (chamadas, contexto, custo), minutos de revisão humana, arquivos fora do escopo, retrabalho.
5. Resultado útil é do tipo "a estratégia X gastou menos mas exigiu 2 redescobertas", não "X
   economizou 17%".
