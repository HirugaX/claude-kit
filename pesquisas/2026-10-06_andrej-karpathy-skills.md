# andrej-karpathy-skills — o que é, o que custa, que evidência há e o que já temos (06/10/2026)

- **A pergunta:** a andrej-karpathy-skills (quatro princípios de comportamento para o Claude escrever código) serve ao
  fluxo do Ettore? Quem fez, de onde vem, o que contém, como instala, quantos tokens fixos custa por sessão, que
  evidência de economia ou qualidade existe, o que repete ou contradiz as nossas regras e o comportamento do Opus 5.5, e
  se o "pergunte / pare" dela atrapalha o trabalho longo sem supervisão.
- **A data:** 06/10/2026 (números do GitHub lidos pela API às 20:42 UTC).
- **O projeto que pediu:** claude-kit (R1).
- **Conferir de novo depois de:** 06/11/2026. Antes, se o repositório receber commit (o último é de 20/04/2026), se sair
  benchmark independente com modelo Claude 5.x, ou se mudarem no Claude Code os textos "Delivering work", "Doing tasks"
  e "Auto mode" (ver o CHANGELOG do repositório Piebald-AI/claude-code-system-prompts). Estrelas e forks mudam por dia.
- **Método:** repositório clonado e lido por inteiro; API do GitHub; documentação da Anthropic baixada em 06/10; textos de
  terceiros lidos na íntegra quando abriram. Nada foi instalado. Marcas: [A] afirmação de autor sem medição independente;
  [I] inferência minha; [não achado] procurei e não achei. Tokens: estimativa por caracteres (método na seção 4).
- **Não confundir:** o gist "LLM wiki" do Karpathy, que a biblioteca já tem, é outra coisa.

## Conclusão em poucas linhas

1. **O que é.** Um `CLAUDE.md` de 65 linhas (e o mesmo texto como skill/plugin), feito por Jiayuan Zhang ("forrestchang",
   dono do Multica) em 27/01/2026, sete horas depois de um post do Karpathy. O Karpathy descreveu os erros; as quatro
   regras são de quem empacotou. Não achei endosso dele. 217 mil estrelas; sem arquivo LICENSE (MIT só declarada); último
   commit em 20/04/2026; 102 PRs abertos e issues desligadas.
2. **Custo fixo pequeno.** `CLAUDE.md`: ≈ 600 tokens em toda sessão (faixa 480–670). Plugin ou skill: ≈ 60–100 tokens
   por sessão e ≈ 560–720 quando a skill dispara. O que pesa é o efeito no comportamento, não o texto.
3. **Evidência fraca.** O repositório não mede nada. A única medição independente com Claude Code (Augment, 40 PRs,
   Opus 4.7) deu custo −10% e duração −7%, mas qualidade −0,07 (correção −0,07). O "41% → 11% → 3%" é de uma pessoa, sem
   dados [A]. O próprio Karpathy escreve que tentativas de corrigir isso pelo CLAUDE.md não resolveram.
4. **Quase tudo já existe.** Os princípios 2 e 3 estão, com o mesmo conteúdo, no prompt do sistema do Claude Code 2.1.292
   (extração de terceiros) e nas páginas de prompting da Anthropic. O 4 já está no kit (§8, §11, `goal-prompt`, `tdd`,
   `diagnosing-bugs`). Só são novos para nós: "diga se há caminho mais simples", "mencione, não apague, código morto
   alheio", "remova só o órfão que a sua mudança criou" e "200 linhas que cabem em 50: reescreva".
5. **O princípio 1 conflita com o objetivo novo.** "Se incerto, pergunte; se confuso, pare" contradiz o modo auto do
   Claude Code ("Minimize interruptions"), o "Delivering work" dele (assuma e siga), a lista fechada de paradas da Q10 e
   o §8 da `uso-do-claude`. A própria Anthropic publica a versão "registre a suposição e siga".
6. **Veredito proposto [I]:** não instalar (nem plugin, nem `CLAUDE.md`). Antes de qualquer texto, medir se o Opus 5.5
   ainda faz o que o arquivo corrige; só o resíduo medido entra, em duas ou três linhas. Seção "Veredito" no fim.

## Fontes (lidas em 06/10/2026)

- Repositório (commit 2c60614, 20/04/2026): https://github.com/multica-ai/andrej-karpathy-skills — `CLAUDE.md`,
  `skills/karpathy-guidelines/SKILL.md`, `.claude-plugin/plugin.json` e `marketplace.json`, `README.md`, `EXAMPLES.md`.
- API do GitHub: https://api.github.com/repositories/1142983825 (estrelas, forks, licença, datas); busca de repositórios por
  nome; PRs #25, #47, #54, #84, #131, #136, #157, #169, #186, #191 em `.../multica-ai/andrej-karpathy-skills/pull/<n>`.
- skills.sh: https://skills.sh/multica-ai/andrej-karpathy-skills/karpathy-guidelines
- Post do Karpathy: https://x.com/karpathy/status/2015883857489522876 (texto lido pelo espelho api.fxtwitter.com).
- Evidência: Augment Code https://www.augmentcode.com/blog/karpathy-skills-on-openclaw-agents-don-t-write-better-code-but-they-do-it-more-efficiently ·
  @Mnilax https://x.com/Mnilax/article/2053116311132155938 (lido pelo espelho api.fxtwitter.com/Mnilax/status/2053116311132155938) ·
  retomadas https://agentpedia.codes/blog/karpathy-claude-md-rules-extended, https://theaiarchitects.com/blog/karpathy-claude-md-rules,
  https://www.aibuilderclub.com/blog/karpathy-claude-md-rules · ETH https://arxiv.org/abs/2602.11988 ·
  DEV https://dev.to/yimtheppariyapol/andrej-karpathy-skills-review-a-single-189k-star-claudemd-4f78 ·
  Clixlogix https://www.clixlogix.com/karpathy-github-claude-md-engineering-teams/ ·
  HN https://news.ycombinator.com/item?id=48383438, https://news.ycombinator.com/item?id=47765204, https://news.ycombinator.com/item?id=48160604
- Anthropic, prompting: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices e, na mesma
  pasta, `prompting-claude-opus-5-5`, `prompting-claude-opus-5`, `prompting-claude-sonnet-5-5`, `prompting-claude-sonnet-5`,
  `prompting-claude-fable-5`, `prompting-claude-fable-5-1`. Blog (Thariq Shihipar, 24/07/2026):
  https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models (redireciona 308 para claude.dev/blog/…).
- Claude Code: https://code.claude.com/docs/en/skills · /memory · /best-practices · /plugins/measure · /discover-plugins ·
  /plugins-reference. Tokens por caractere: https://platform.claude.com/docs/en/about-claude/glossary e .../pricing.
- Prompt do sistema do Claude Code (extração de terceiros do código compilado; índice "as of v2.1.292, 06/10/2026"):
  https://github.com/Piebald-AI/claude-code-system-prompts — `system-prompt-doing-tasks-no-unnecessary-additions.md`,
  `...-no-unnecessary-error-handling.md`, `system-prompt-delivering-work-at-full-scope.md`,
  `system-prompt-autonomous-operation-guidelines.md`, `system-prompt-auto-mode.md`.
- Locais: `C:\Users\ettor\.claude\CLAUDE.md`; `C:\Users\ettor\.claude\skills\{writing-for-agents,grilling,tdd,diagnosing-bugs,
  codebase-design,prototype,implement,goal-prompt}\SKILL.md`; `C:\CLAUDE-PROJETOS\claude-kit\skills\uso-do-claude\SKILL.md`;
  `C:\CLAUDE-PROJETOS\claude-kit\decisoes\2026-10-06_plano-fluxo.md`.

## 1. O repositório certo

- **Endereço atual:** https://github.com/multica-ai/andrej-karpathy-skills (organização Multica). O endereço antigo,
  `forrestchang/andrej-karpathy-skills`, responde 301 para ele (id 1142983825): é o mesmo repositório, transferido. O
  README e os comandos de instalação ainda citam `forrestchang/`; o PR #189 (aberto) propõe trocar.
- **Autor:** Jiayuan Zhang, conta `forrestchang` (blogs escrevem "Forrest Chang" e "Jiayuan Chang"). 19 dos 28 commits;
  o `CLAUDE.md` nasceu num commit só dele (8462496, 27/01/2026). O README abre com propaganda do Multica, projeto dele
  (README:3-5). Outros: Shehab Tarek (plugin), Szymon Kocot (estrutura para o skills.sh), Joseph Ayanda (EXAMPLES),
  Herobrine (tradução), Andriy Zakharko (Cursor).
- **Relação com o Karpathy:** derivado de um post dele no X, 26/01/2026 20:25 UTC ("A few random notes from claude coding
  quite a bit last few weeks"; 40,7 mil curtidas e 7,85 milhões de visualizações em 06/10). O repositório diz "derived
  from Andrej Karpathy's observations" (README:7); não diz que ele escreveu nem que endossa. O post é uma lista de
  notas: o erro "suposições erradas sem checar", o "overcomplicate", o "mexe no que não entende" e, em "Leverage", a
  ideia de dar critério de sucesso e testes primeiro. As quatro regras e o texto são de quem empacotou. Três das quatro
  citações do README estão condensadas, não literais (conferi contra o post; só a de "Leverage" bate).
  Declaração do Karpathy sobre o repositório: [não achado]. Um agregador no HN (item 48383438) diz que ele não escreveu
  nem endossou [A].
- **Licença:** README:169-171, `SKILL.md`:4 e `plugin.json`:8 dizem "MIT". Não existe arquivo LICENSE e a API devolve
  `license: null`. O PR #47 (adicionar o LICENSE) foi fechado sem merge.
- **Datas:** criado em 27/01/2026 03:53 UTC; último commit e último push em 20/04/2026 10:05 UTC (2c60614, "Sync
  Chinese README…"). 28 commits. Sem tags nem releases: só dá para seguir o ramo `main`.
- **Números (API, 06/10/2026 20:42 UTC):** 217.247 estrelas; 21.876 forks; 1.266 observadores. Issues e discussões
  desligadas (`has_issues=false`). A conversa ficou nos PRs: 102 abertos, 61 fechados, 12 mesclados; nenhum mesclado
  depois de 20/04/2026. Havia a issue #65, "Why aren't Karpathy's LLM coding principles Claude Code defaults?" (HN
  47765204, 14/04/2026); hoje devolve 404 e não consegui lê-la.
- **Mesmo nome:** a busca por `andrej-karpathy-skills` no nome devolve 118 repositórios, cópias e não forks do GitHub.
  Maiores: vtroisWhite (427 estrelas, cópia literal), mbeijen/…-cursor-vscode (273), duolahypercho (248, reescrita para
  o Codex), LearnPrompt (106), swarmclawai (51). Comparei byte a byte: vtroisWhite (`CLAUDE.md` e `SKILL.md`) e
  PureTokens (`SKILL.md`) são idênticos ao original; o `SKILL.md` do swarmclawai só não tem a linha `license: MIT`.
  Dono diferente, mesmo nome: confira o dono antes de instalar.

## 2. O que contém

Nove arquivos, sem script, gancho nem MCP (o `plugin.json` só declara uma skill, :10).

| arquivo | linhas | caracteres | entra no contexto do modelo? |
|---|---|---|---|
| `CLAUDE.md` | 65 | 2.345 (358 palavras) | só se colado num CLAUDE.md |
| `skills/karpathy-guidelines/SKILL.md` | 67 | 2.506 (cabeçalho 281 + corpo 2.225) | nome e descrição sempre; corpo ao disparar |
| `EXAMPLES.md` | 522 | 14.790 | não: nada o referencia |
| `README.md` | 171 | 6.162 | não |
| `.cursor/rules/karpathy-guidelines.mdc` | 70 | 2.626 | só no Cursor (`alwaysApply: true`) |
| `README.zh.md`, `CURSOR.md`, `plugin.json`, `marketplace.json` | 171, 28, 11, 29 | — | não |

Os princípios, em uma linha cada (`CLAUDE.md` do commit 2c60614):

1. **Think Before Coding** (:7-15): declare as suposições; mostre as interpretações; diga se há caminho mais simples;
   "se incerto, pergunte"; "se algo está confuso, pare, diga o que confunde, pergunte".
2. **Simplicity First** (:17-27): o mínimo de código; nada além do pedido, nem abstração de uso único, nem
   configurabilidade, nem tratamento de erro "impossível"; se 200 linhas cabem em 50, reescreva.
3. **Surgical Changes** (:29-43): toque só no necessário; não "melhore" o vizinho; siga o estilo existente; mencione código
   morto alheio, não apague; remova só o órfão que a sua mudança criou; toda linha mudada tem de ligar ao pedido.
4. **Goal-Driven Execution** (:45-61): vire a tarefa em critério verificável (teste primeiro); plano curto com "verify"
   por passo; critério forte deixa o agente repetir sozinho, critério fraco ("faça funcionar") pede esclarecimento.

Mais duas frases: "Tradeoff: bias toward caution over speed" (:5) e "working if: … clarifying questions come before
implementation" (:65). Estilo: 10 das 65 linhas são proibições ("No…", "Don't…"); 0 ocorrências de MUST, CRITICAL, NEVER,
ALWAYS ou IMPORTANT; uma palavra em maiúsculas ("YOUR", :40).

## 3. Como instala (nada foi instalado)

| forma | comandos | o que carrega em toda sessão |
|---|---|---|
| plugin (README:101-113) | `/plugin marketplace add forrestchang/andrej-karpathy-skills` e `/plugin install andrej-karpathy-skills@karpathy-skills`. Marketplace `karpathy-skills`, plugin `andrej-karpathy-skills`, versão 1.0.0, skill `karpathy-guidelines` (aparece como `andrej-karpathy-skills:karpathy-guidelines`). Pelo terminal: `claude plugin marketplace add multica-ai/andrej-karpathy-skills`, `claude plugin install andrej-karpathy-skills@karpathy-skills --scope user\|project\|local` | só nome e descrição da skill; o corpo entra quando ela dispara |
| skill avulsa (skills.sh; o README não lista, o PR #84 aberto propõe) | `npx skills add https://github.com/multica-ai/andrej-karpathy-skills --skill karpathy-guidelines` (39 mil instalações; auditorias Gen Agent Trust Hub, Socket e Snyk "Pass") | igual ao plugin, sem o prefixo |
| trecho de CLAUDE.md (README:115-126) | `curl -o CLAUDE.md https://raw.githubusercontent.com/forrestchang/andrej-karpathy-skills/main/CLAUDE.md`; para acrescentar: `echo "" >> CLAUDE.md` e `curl <mesma url> >> CLAUDE.md` | o texto inteiro, em toda sessão e toda chamada |
| Cursor (CURSOR.md) | copiar `.cursor/rules/karpathy-guidelines.mdc` | não se aplica ao Claude Code |

- **Regra oficial do que carrega** (https://code.claude.com/docs/en/skills, tabela "When loaded into context"): "Description
  always in context, full skill loads when invoked". Invocada, a skill "stays in context across turns"; depois da
  compactação o Claude Code recoloca a mais recente, só os primeiros 5.000 tokens (25.000 no total).
- **CLAUDE.md:** "loaded every session"; chega como mensagem de usuário depois do prompt do sistema, sem garantia de
  cumprimento (https://code.claude.com/docs/en/memory). Meta oficial: menos de 200 linhas.
- **Escopo do plugin:** `--scope project` ou `local` liga só naquele repositório (https://code.claude.com/docs/en/discover-plugins).
- **Duplicação possível:** o PR #136 (aberto desde 15/05/2026) diz que o `"skills"` do `plugin.json` mais a varredura
  padrão registram a skill duas vezes (saída colada do `claude plugin details`: "Skills (2)", "~206 tok"). Um comentário
  de 25/08/2026 não conseguiu reproduzir (2.1.241). Contestado. A referência do plugin diz que `skills` no manifesto
  "adds to the default `skills/` scan" (https://code.claude.com/docs/en/plugins-reference).

## 4. Custo fixo por sessão

**Método.** Caracteres contados no texto bruto baixado (UTF-8, sem CRLF). Tokens por dois fatores oficiais: "1 token ≈ 4
caracteres ou 0,75 palavra em inglês" (página de preços) e "≈ 3,5 caracteres" (glossário). Não há tokenizador do Claude
local; erro de ±20%. A medida exata sem instalar existe: `claude --plugin-dir <pasta> plugin details andrej-karpathy-skills`
(documentada em https://code.claude.com/docs/en/plugins/measure; carrega o plugin só naquele comando). Não rodei porque o
limite desta pesquisa era "nada no Claude Code".

| o que | caracteres | tokens (÷4 a ÷3,5) |
|---|---|---|
| `CLAUDE.md` inteiro | 2.345 | 586 a 670 (por palavras: 477) |
| `SKILL.md` inteiro / só o corpo | 2.506 / 2.225 | 626 a 716 / 556 a 636 |
| entrada da skill na listagem (nome + descrição) | 242 (265 com o prefixo do plugin) | 60 a 76 |
| `EXAMPLES.md` (não carrega) | 14.790 | 3.698 a 4.226 |

| forma | sempre | quando dispara | observação |
|---|---|---|---|
| `CLAUDE.md` do projeto | ≈ 600 | — | só nos projetos onde for colado |
| `CLAUDE.md` pessoal | ≈ 600 | — | em toda janela, até a que não é código; o arquivo de hoje tem 3.118 caracteres (≈ 780–890): +75% |
| plugin ou skill avulsa | ≈ 60–100 (a PR #136 mediu "~103 tok" com o `claude plugin details`; ≈ 206 se duplicar) | + 560–720 (corpo ou arquivo inteiro), e fica na janela | a descrição diz "Use when writing, reviewing, or refactoring code": numa janela de código dispara quase sempre [I] |
| regra `.claude/rules/*.md` com `paths:` (adaptação nossa, não do repositório) | 0 | ≈ 600 ao tocar nos arquivos do `paths` | https://code.claude.com/docs/en/memory |

Escala: o portão do plano é ctx0 ≤ 40 mil (`plano-fluxo.md`:601); 600 tokens são 1,5%. Com o cache a US$ 0,20/MTok
(`uso-do-claude/SKILL.md`:97), 600 tokens custam ≈ US$ 0,0001 por chamada [I]. A listagem de skills tem teto de 1% da
janela e corta as descrições das menos usadas (https://code.claude.com/docs/en/skills): mais uma entrada disputa esse
espaço [I].

## 5. Evidência de economia ou de qualidade

| fonte | o que mediu | resultado | peso |
|---|---|---|---|
| o repositório | nada: sem benchmark, sem teste (README:140-147 só lista sinais para o usuário observar) | — | opinião |
| Augment Code, 30/04/2026 (atualizado 18/06) | 40 PRs do OpenClaw (100–300 linhas), 6 execuções por configuração, juiz LLM; ~2,5 mil caracteres das regras antepostos a um AGENTS.md de ~18 mil | **Claude Code (Opus 4.7):** duração −7%, chamadas de ferramenta −8%, custo −10%, qualidade −0,07 (correção −0,07, completude −0,06), ~5% menos arquivos tocados. Auggie (Opus 4.7): −3%, −3%, −3%, qualidade 0,00. Codex (GPT-5.4): −7%, −6%, −8%, 0,00. "Documentação não pedida" melhor em +0,05 a +0,06. Em outro repositório, cujas instruções já se sobrepunham, "no statistically significant difference". Os autores: "the code itself didn't reliably get better, but the path got shorter" | a melhor medição achada; o fornecedor vende um agente concorrente; Opus 4.7, não 5.5 |
| PR #186 (aberto, 06/07/2026, 0 comentários) | microbenchmark de um contribuidor: 3 tarefas, chamadas únicas à API, sem agente | Gemini 3.5 flash: tokens de saída −79,7% (PR); no README do mesmo PR, prompt + saída **+59,2%**. GPT-5.3-codex (15/07/2026, 30 chamadas): skill completa em toda tarefa **+203,6%** de tokens visíveis da requisição e +34,6% de latência, aprovação 66,7% → 100%; versão "adaptativa": −45,1% (IC95% −64,6% a −16,4%). Conclusão do autor: "The original always-loaded rules did not lower token cost" | tamanho de amostra mínimo; o próprio autor diz "not a full repository-editing agent benchmark" |
| @Mnilax, 09/05/2026 (X, 4,5 mi de visualizações) | "50 tarefas representativas em 30 repositórios por 6 semanas": taxa de erro = tarefa que precisou de correção ou reescrita | sem CLAUDE.md ~41%; 4 regras ~11%; 12 regras ~3% (conformidade 78% → 76%) | [A]: uma pessoa, sem modelo nomeado, sem dados nem código publicados; o texto termina com divulgação de canal no Telegram |
| AI Builder Club (22/05/2026), The AI Architects, agentpedia | repetem o número do Mnilax; o AI Builder Club o usa só no título, sem método | — | [A] |
| ETH Zurique, arXiv 2602.11988 (versão de 29/09/2026) | arquivos de contexto (AGENTS.md) de repositórios reais, SWE-bench | "does not generally improve task success rates"; custo "by over 20% on average"; "instructions … are well followed"; úteis para "non-standard coding practices" | pesquisa independente, mas sobre arquivos de contexto em geral, não sobre este |
| Tessl (PR #25, aberto desde 25/02/2026) | nota da descrição da skill: 84% → 96%; conteúdo 100% | mede se a descrição é fácil de achar, não o comportamento | vendor |
| DEV (yimtheppariyapol), Clixlogix (28/06/2026), outros blogs | resenhas | nenhum número medido; a Clixlogix vende consultoria | opinião |
| HN | 3 itens: a issue #65, o agregador, "Ask HN: Do you still spend time maintaining Claude.md…" (16/05/2026) | sem dado; comentários dizem que regra de comportamento "constantly not followed" ou que ajuda se for curta e positiva | opinião |
| Reddit | a ferramenta de busca bloqueia o domínio | [não achado] | — |

Também: o post do Karpathy diz "All of this happens despite a few simple attempts to fix it via instructions in
CLAUDE.md" e "if you have any code you actually care about I would watch them like a hawk, in a nice large IDE on the
side": ele descreve uso supervisionado, e a tentativa por CLAUDE.md dele não resolveu.

## 6. Redundância e conflito com as nossas regras

Legenda: **coberto** (onde); **conflita** (como); **novo**. "Harness" = o prompt do sistema do Claude Code 2.1.292
(extração de terceiros; não verifiquei em quais janelas e modelos cada trecho está ativo).

| regra do repositório (`CLAUDE.md`) | veredito | onde / como |
|---|---|---|
| 1a. declare as suposições; "se incerto, pergunte" (:12) | **coberto** a metade "declare"; **conflita** a metade "pergunte" | planejar: `grilling/SKILL.md`:8 e :28 ("nothing left silently assumed"; recomendação em cada pergunta); `prototype/SKILL.md`:17 (declara a suposição e segue); harness "Delivering work" (declare a suposição e siga). Conflito: `plano-fluxo.md`:34-37 (paradas só na lista fechada da Q10), `uso-do-claude/SKILL.md`:205-206 (tentativas esgotadas → registrar o bloqueio e parar aquela linha) e `CLAUDE.md` pessoal:15-16 ("decisão técnica de rotina se resolve sem perguntar") |
| 1b. mostre as interpretações (:13) | **coberto** | `grilling/SKILL.md`:8-22: rodadas numeradas, opções e resposta recomendada, tudo de uma vez |
| 1c. diga se há caminho mais simples; discorde (:14) | **novo** (parcial no harness: "state the concern in a sentence or two, then keep building") | nenhuma regra nossa pede isso |
| 1d. "se confuso, pare e pergunte" (:15) | **conflita** | contra o modo auto ("Minimize interruptions"), o "Autonomous operation" ("asking … will block the work"), a Q10 e o objetivo de 06/10 (`plano-fluxo.md`:426) |
| 2a-c. nada além do pedido; sem abstração de uso único; sem configurabilidade (:21-23) | **coberto** | harness "no unnecessary additions" ("Don't add features, refactor, or introduce abstractions beyond what the task requires… Don't design for hypothetical future requirements"); `tdd/SKILL.md`:36 ("no speculative features"); `codebase-design/SKILL.md`:63-65 (teste da exclusão; "um adaptador é seam hipotético") |
| 2d. sem tratamento de erro "impossível" (:24) | **coberto**, com cuidado nos `desosp-` | harness "no unnecessary error handling" ("Only validate at system boundaries"). Nos projetos clínicos o "impossível" tem de ser julgado com as invariantes (`uso-do-claude/SKILL.md`:78) [I] |
| 2e. "200 linhas que cabem em 50: reescreva" (:25) | **novo** | reescrever gasta tokens e tempo; o Opus 5.5 "tends to finish the same task with fewer tokens" (Anthropic) [I] |
| 3a-b. não melhore o vizinho; não refatore o que não quebrou (:34-35) | **coberto** | harness ("A bug fix doesn't need surrounding cleanup"); `uso-do-claude/SKILL.md`:74 (sinal "mexe no que não devia", verificação "diff restrito") e :204 (escopo: o que pode e o que não pode mexer); :192 (commit por caminho explícito); `CLAUDE.md` pessoal:17-21 (nenhuma alteração sem mostrar e esperar o "sim") |
| 3c. siga o estilo existente (:36) | **coberto** | o texto novo do sistema: "Write code that reads like the surrounding code: match its comment density, naming, and idiom" (blog da Anthropic, 24/07/2026) |
| 3d. código morto alheio: mencione, não apague (:37) | **novo** | a Anthropic traz o equivalente: "mention it at the end instead of doing it" (Sonnet 5.5), "report it as a follow-up in your summary" (Fable 5.1) |
| 3e. remova só o órfão que a sua mudança criou (:40-41) | **novo** | provavelmente já é o padrão [I]; não achei trecho oficial |
| 3f. toda linha mudada liga ao pedido (:43) | **coberto em parte** | `uso-do-claude/SKILL.md`:206-207 (prova de término: diff e o que ficou de fora) |
| 4a. critério de sucesso, repetir até verificar (:47, :61) | **coberto** | `uso-do-claude/SKILL.md`:22-25 (§1), :204-210 (§8, `/goal`), :280-283 (§11, verificar por comando); `goal-prompt/SKILL.md`:15-27 (estado final, checagem, invariantes, parada); `CLAUDE.md` pessoal:10-11 |
| 4b. "validar → teste primeiro"; "bug → teste que reproduz" (:50-51) | **coberto** | `tdd/SKILL.md`:36 ("red before green"); `diagnosing-bugs/SKILL.md`:57-66 e :116-128; `implement/SKILL.md`:9-11 |
| 4c. "refatorar → testes passam antes e depois" (:52) | **coberto em parte** | `tdd/SKILL.md`:38 põe a refatoração fora do laço, na revisão; `uso-do-claude/SKILL.md`:74 (mudança mecânica: "diff restrito + testes afetados") |
| 4d. plano curto com "verify" por passo (:54-59) | **coberto em parte** | `uso-do-claude/SKILL.md`:206 (checkpoint por commit); `implement-spec/SKILL.md`:13 (grafo de tarefas); a página do Opus 5.5 pede uma lista de pendências para corrida sem supervisão |
| estilo do arquivo | **conflita** com `writing-for-agents` | :74 (negação puxa o comportamento proibido: 10 de 65 linhas são "No/Don't"); :81 (instrução que o modelo já cumpre é no-op); :78 (duplicação); :24 (carga de contexto) |

Tensões menores [I]: o "Loop until verified" é uma instrução genérica de verificação, do tipo que a página do Opus 5 manda
remover (seção 7), diferente do critério por tarefa do `/goal`; "Think Before Coding" pede texto antes do código, e o
nosso fluxo põe a conversa na entrevista (`grilling`), antes da execução. E o arquivo é só pedido em texto: o §11 da
`uso-do-claude` (:277-278) diz que "não mexa fora do módulo" no prompt é orientação, e que o controle é permissão, gancho
e teste; o PR #54 do repositório (aberto) tenta isso com ganchos que só avisam e não bloqueiam.

## 7. O que a documentação da Anthropic diz (Opus 5.5 e família Claude 5)

Fatos, com trechos curtos. A página geral avisa: onde uma técnica nomeia um modelo, "treat it as measured on that model
and re-check it against your own evals before applying it to another". A página do Opus 5.5 diz que os padrões da do
Opus 5 "remain a reasonable starting point".

- **Excesso de engenharia.** Geral, "Overeagerness": "Claude Opus 4.5 and Claude Opus 4.6 have a tendency to overengineer by
  creating extra files, adding unnecessary abstractions, or building in flexibility that wasn't requested", com um
  prompt-modelo: "Don't add features, refactor code, or make 'improvements' beyond what was asked. A bug fix doesn't need
  surrounding code cleaned up… Don't add error handling, fallbacks, or validation for scenarios that can't happen…
  Don't create helpers, utilities, or abstractions for one-time operations." **É o equivalente dos princípios 2 e 3.**
  Para o Claude 5 a tendência continua descrita: Opus 5 "can also expand the scope of a task"; Sonnet 5.5
  "tends to add tests, documentation, and small supporting files… Most teams will welcome this"; Fable 5.1 "may fix
  nearby code… or commit more test files than the change warrants".
- **Mudanças além do pedido (o texto pronto).** Opus 5: "Deliver what was asked, at the scope intended. Make routine
  judgment calls yourself, and check in only when different readings of the request would lead to materially different
  work. If the request seems mistaken or a better approach exists, say so in a sentence and continue with the task as
  asked…". Sonnet 5.5: "Don't add features, tests, files, docs or refactors that weren't asked for. If you think one
  would help, mention it at the end instead of doing it." Fable 5.1: "If, while working or testing, you find a pre-existing
  bug… don't fix, optimize or extend it in this change… report it as a follow-up in your summary" e "unrequested
  additions and committed test code drop substantially with no measurable change in task success".
- **Instruções enfáticas.** Geral, "Tool usage": para o Opus 4.5 e 4.6, "The fix is to dial back any aggressive language.
  Where you might have said 'CRITICAL: You MUST use this tool when…', you can use more normal prompting like 'Use this
  tool when…'". Para o Claude 5 não achei trecho sobre CRITICAL/MUST [não achado]; há o diagnóstico geral: "we were
  overconstraining Claude Code, both through our system prompt and in our CLAUDE.md files and skills" (blog, que removeu
  "over 80%" do prompt do sistema "with no measurable loss on our coding evaluations"); Sonnet 5 "interprets prompts
  literally"; Fable 5: "Skills developed for prior models are often too prescriptive… and can degrade output quality.
  Review and consider removing older instructions if default performance is better". O Claude Code ensina: "If you
  emphasize many lines, none of them stands out". **A andrej-karpathy-skills tem 0 MUST/CRITICAL, então o risco de excesso
  de gatilho por ênfase é baixo; o risco é a redundância e o "pergunte / pare".**
- **Verificação.** Opus 5: "verifies its own work without being told to. If your prompt contains explicit verification
  instructions ('include a final verification step for any non-trivial task'…), remove them: … cause over-verification…
  removing them reduces wasted tokens with no loss in quality". Sonnet 5.5: "generally checks its work before it reports a
  change as done"; a falha aparece no esforço `low`, e a instrução extra a reduz. Geral: "Avoid focusing on passing tests
  and hardcoding" (o contrapeso do princípio 4: "Tests are there to verify correctness, not to define the solution").
- **Perguntar × agir.** Geral: `<default_to_action>`: "If the user's intent is unclear, infer the most useful likely
  action and proceed, using tools to discover any missing details instead of guessing" (e há a versão conservadora, para
  quem quer o contrário). Fable 5.1, "Delivering work": "Read ambiguity the way a careful colleague would… keep building
  under stated assumptions"; "do everything that doesn't depend on the answer; then state the assumption you made, or —
  when going ahead on a wrong guess would be unsafe or would make the work useless — put the question at the end of a
  turn that also delivers that progress". Sonnet 5.5: "Keep working until everything the user asked for is done, and only
  stop to ask when you can't go on without the user or before a risky step". Fable 5: "Pause for the user only when the
  work genuinely requires them: a destructive or irreversible action, a real scope change, or input that only they can
  provide".
- **Manutenção do arquivo** (https://code.claude.com/docs/en/best-practices): "For each line, ask: 'Would removing this
  cause Claude to make mistakes?' If not, cut it"; exclua "Self-evident practices like 'write clean code'"; "If Claude
  already does something correctly without the instruction, delete it or convert it to a hook"; "test changes by
  observing whether Claude's behavior actually shifts". Instruções que se contradizem: "Claude may pick one arbitrarily"
  (https://code.claude.com/docs/en/memory).
- **O próprio Claude Code já carrega isso** (Piebald, v2.1.292; cada trecho traz a versão em que mudou pela última vez):
  "Don't add features, refactor, or introduce abstractions beyond what the task requires. A bug fix doesn't need
  surrounding cleanup; a one-shot operation doesn't need a helper. Don't design for hypothetical future requirements"
  (2.1.161); "Don't add error handling, fallbacks, or validation for scenarios that can't happen… Only validate at system
  boundaries" (2.1.53); o "Delivering work" inteiro (2.1.218), que é o texto do Fable 5.1 acima.

**Resposta à pergunta "a documentação já traz trecho equivalente?":** sim para 2 e 3 (mesmo conteúdo no Claude Code e
nas páginas do Opus 4.5/4.6, Sonnet 5.5 e Fable 5.1); para 1, só com o sentido de execução invertido (assuma e siga);
para 4, em parte (verificar com uma checagem real; e o aviso contra o excesso).

## 8. A tensão com o objetivo novo (atenção concentrada, execução longa sem o Ettore)

**Fatos.**
- O princípio 1 manda "If uncertain, ask" (:12) e "If something is unclear, stop… Ask" (:15); o arquivo se declara
  "bias toward caution over speed" (:5) e conta "clarifying questions come before implementation" como sinal de que
  funciona (:65).
- O Claude Code já instrui o contrário para execução contínua. Auto mode (2.1.139): "Minimize interruptions — Prefer
  making reasonable assumptions over asking questions for routine decisions". Autonomous operation (2.1.227): "The user
  is not watching in real time… asking 'Want me to…?' or 'Shall I…?' will block the work. For reversible actions… proceed
  without asking. Stop only for destructive actions or genuine scope changes". Quando duas instruções se contradizem,
  "Claude may pick one arbitrarily" (docs de memória).
- A Anthropic descreve parada precoce como falha conhecida de corrida longa: Opus 5.5, "Unattended agentic runs" (um
  turno que termina em texto, depois de relatar progresso, encerra o laço); Sonnet 5.5 em `low` e `medium` "sometimes
  checks in before a coding task is done… ask a question it could answer itself, or stop after one part of a multipart
  task to ask whether to continue". Fable 5.1 avisa que o bloco de "não pergunte" "can also make the model less likely to
  ask about ambiguous requests, so check that trade-off on your own tasks" (há troca nos dois sentidos).
- O plano do kit já tem o desenho: o Claude para só na lista da Q10 (`plano-fluxo.md`:34-37), e a R1 pede decidir entre
  "parada que bloqueia" e "pergunta guardada numa fila enquanto a fase segue" (:426).
- Versões que trocam "pergunte" por "registre a suposição e siga": **PR #169** (aberto desde 03/06/2026, 3 linhas):
  "In headless / non-interactive mode… document assumptions inline, pick the most general interpretation, and proceed";
  nunca mesclado. **duolahypercho/andrej-karpathy-skills** (248 estrelas, reescrita para o Codex): "Ask a concise
  clarifying question when guessing would create real risk. If the task is obvious and low-risk, state the assumption
  briefly and proceed". **PR #191** (aberto): faixa "Claude 5 models should skip this file", dizendo que "If uncertain,
  ask" contradiz o treino do Claude 5; foi escrita por uma instância do Claude a pedido do usuário ("make it funny"), e o
  blog da Anthropic que ela cita **não** diz isso (o blog não trata de perguntar) [A]. **Clixlogix**: "In headless or
  non-interactive mode, do not stall" [A, consultoria]. **PR #186**: "Ask when ambiguity affects correctness; otherwise
  state the conservative assumption… ask one concise question and stop" (ainda para). No template do Mnilax (regra 6,
  texto em agentpedia): "Stop and ask if a task is trending past its budget" (ainda pergunta). Issue sobre isso no
  repositório: [não achado] (issues desligadas; a #65 não abre).
- Medição de quantas perguntas a mais o arquivo provoca: [não achado]. O Augment não reporta.

**Juízo [I].**
- Em janela supervisionada o princípio 1 ajuda; numa execução longa sem o Ettore ele aumenta as paradas, e cada parada
  custa tempo parado, não tokens. O texto do próprio repositório pede essas perguntas como sinal de sucesso.
- O encaixe com o objetivo é o da Anthropic e o do plano: perguntar tudo antes (a entrevista `grilling`), depois seguir
  registrando a suposição no resumo, e parar só nas paradas da lista fechada.

## Veredito proposto [opinião; decisão é do Ettore]

**Não instalar a andrej-karpathy-skills** (nem plugin, nem `CLAUDE.md` pessoal, nem entrar no `config\plugins.json`). Porquê:
(a) 2 e 3 o Claude Code já diz, com o mesmo conteúdo; (b) 4 o kit já tem, com comando e prova; (c) 1 contradiz o objetivo e a
lista da Q10; (d) a evidência com Claude Code é −10% de custo e −0,07 de qualidade, em Opus 4.7, e o resto é [A]; (e) a
Anthropic manda podar o que o modelo já faz.

**Testar como (se o Ettore quiser aferir, como pediu):** primeiro o problema, depois a solução.
1. **Linha de base, sem nenhum texto novo.** 10 tarefas reais pequenas, cada uma com um comando de aceite (testes) e a
   lista de arquivos esperados, em janelas novas, Opus 5.5 e `/effort medium`, modelo pelo ID completo. Medir por tarefa:
   arquivos e linhas fora do pedido (`git diff --stat` contra a lista), paradas para perguntar, tokens (`medir_uso.py
   --sessoes`), aceite, tempo.
2. **Se a linha de base já vier limpa** (no máximo 1 mudança fora do pedido em 10), não há o que corrigir: fim do teste.
3. **Se vier suja**, braço B com só o resíduo medido, em 2 ou 3 linhas num arquivo `.claude/rules/` com `paths:` só para
   os arquivos de código (0 token fora deles). Texto-candidato, paráfrase dos trechos da Anthropic: "Algo útil fora do
   pedido (limpeza, doc, teste extra, código morto alheio): mencione no resumo, não faça" e "Dúvida que não bloqueia:
   registre a suposição no resumo e siga; pare só nos pontos da Q10". Mesmas 10 tarefas, ordem alternada.
4. **Regra de decisão** (emprestada do PR #186): aceite não pior que a linha de base; tokens ou tempo pelo menos 10% menores
   ou menos mudanças fora do pedido; sem depender de uma tarefa só.
5. **Limite do teste:** com 10 tarefas só se vê efeito grande ou dano grande (mais paradas, aceite pior). Efeito de 3 a
   10% em custo, como o do Augment, exigiu 40 PRs × 18 execuções e não se mede aqui.

**O que mudaria o veredito:** linha de base suja de forma repetida no Opus 5.5; benchmark independente com Claude 5.x a
favor; ou o Ettore decidir que quer o arquivo como "cinto de segurança" em janelas de código supervisionadas (aí:
`claude plugin install … --scope local`, só no repositório de código, e `claude plugin details` para conferir o custo).

## O que não consegui

- Contar tokens com o tokenizador do Claude (só estimativa por caracteres); rodar `claude plugin details` (limite: nada
  no Claude Code).
- Saber em quais janelas e modelos cada trecho do prompt do Claude Code (Piebald) está ativo; o índice é de terceiros.
- A taxa real de disparo da skill nas janelas de código; os dados brutos do Mnilax; threads do Reddit (domínio bloqueado
  na busca); a resenha do Medium (HTTP 403); a issue #65 do repositório (404).
- Nenhum dado de paciente entrou nesta pesquisa; nenhuma transcrição foi aberta.
