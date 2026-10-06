# Janelas paralelas e economia de tokens no Claude Code

- **Pergunta:** rodar 2 a 4 janelas do Claude Code ao mesmo tempo, cada uma com um pedaço do trabalho, e uma
  janela para juntar e verificar — faz sentido para acelerar sem gastar mais tokens? Quem já faz, com que
  ferramentas (no Windows), e como evitar o "Frankenstein"?
- **Data:** 04/10/2026
- **Projeto que pediu:** entrevista das cores de pasta (notebook); a decisão é da janela da `uso-do-claude`.
- **Fontes (principais; as demais no corpo):**
  - https://code.claude.com/docs/en/worktrees · /agent-teams · /costs · /best-practices
  - https://www.anthropic.com/engineering/multi-agent-research-system
  - https://www.anthropic.com/engineering/building-c-compiler
  - https://cognition.com/blog/dont-build-multi-agents
  - https://simonwillison.net/2025/Oct/5/parallel-coding-agents/
  - https://metr.org/blog/2026-02-24-uplift-update/
- **Conclusão:** quem poupa token é a janela curta, não o paralelo; o paralelo compra tempo de relógio e gasta
  a cota mais depressa (10 agentes ≈ 10× mais rápido). Faz sentido só para partes independentes e
  verificáveis por teste: 2 trabalhadoras + 1 integradora, teto de 3, com interfaces congeladas, testes
  escritos antes por outra janela, arquivos que não se cruzam e gabarito clínico. Não paralelizar regra
  clínica, arquivo compartilhado, caça a bug, migração. No Windows nativo: `claude --worktree`, o app
  Desktop ou `claude agents`.
- **Conferir de novo depois de:** 04/11/2026.
- **Como foi feita:** subagente Explore (Sonnet), 103 chamadas de ferramenta. O texto abaixo é o relatório
  dele, sem mudança de conteúdo.

---

**Método.** Consultas feitas em 2026-10-04. Em cada seção, tudo é [VERIFICADO EM FONTE] (página lida) salvo
marcação [INCERTO] (fonte secundária, sem página primária ou inferência do subagente). Estrelas e datas vêm
da API do GitHub do dia. Os tweets de Boris foram lidos por espelho (api.fxtwitter.com), porque x.com devolve
HTTP 402.

## 1. Documentação oficial
- **Worktrees nativas.** `claude --worktree <nome>` (`-w`) cria `.claude/worktrees/<nome>/` na branch
  `worktree-<nome>` e exige pelo menos 1 commit. "A worktree is a fresh checkout, so initialize your
  development environment there" (venv, dependências). Arquivos ignorados, como `.env`, só entram via
  `.worktreeinclude`. **Pegadinha:** por padrão a worktree sai do branch padrão remoto (`origin/HEAD`), não do
  HEAD local; commits locais só entram com `worktree.baseRef: "head"`. A doc trata de junções NTFS, logo o
  Windows nativo é suportado. O Desktop tem opção "worktree" por sessão (Ctrl+N no Windows).
  code.claude.com/docs/en/worktrees ; /common-workflows ; /desktop
- **Subagentes.** `isolation: worktree` no frontmatter, ou "use worktrees for your agents". Cada subagente
  "spends tokens of its own" e conta nos mesmos limites. `/batch` divide uma mudança em 5 a 30 subagentes,
  cada um em worktree. code.claude.com/docs/en/sub-agents ; /best-practices
- **Agent view** (`claude agents`, `claude --bg`; research preview). Cada sessão vai para worktree própria
  antes de editar. "running ten agents in parallel uses quota roughly ten times as fast as running one."
  code.claude.com/docs/en/agent-view
- **Agent teams.** Experimental e desligado (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`). Custo: "approximately
  7x more tokens than standard sessions when teammates run in plan mode" (/costs). "Start with 3-5 teammates";
  5-6 tarefas por teammate. "Two teammates editing the same file leads to overwrites"; não há worktree por
  teammate (você particiona os arquivos). "For sequential tasks, same-file edits, or work with many
  dependencies, a single session or subagents are more effective." Comece por pesquisa e revisão, sem a
  coordenação da implementação paralela. Painéis divididos não funcionam no Windows Terminal nem no terminal
  do VS Code; só o modo in-process. code.claude.com/docs/en/agent-teams ; /agents
- **Nuvem** (`claude --cloud`). "Running multiple tasks in parallel consumes more rate limits
  proportionately." code.claude.com/docs/en/claude-code-on-the-web
- **Boas práticas.** O contexto "fills up fast, and performance degrades as it fills". Writer/Reviewer: "A
  fresh context improves code review since Claude won't be biased toward code it just wrote"; "have one
  Claude write tests, then another write code to pass them". Spec boa: "name the files and interfaces
  involved, state what is out of scope, and end with an end-to-end verification step", executada em sessão
  nova. code.claude.com/docs/en/best-practices
- **Pesquisa multiagente.** "agents typically use about 4× more tokens than chat interactions, and
  multi-agent systems use about 15× more tokens than chats". "Most coding tasks involve fewer truly
  parallelizable tasks than research, and LLM agents are not yet great at coordinating and delegating to
  other agents in real time." Também: domínios com contexto compartilhado ou muitas dependências "are not a
  good fit". anthropic.com/engineering/multi-agent-research-system
- **Harness longo.** Agente inicializador, mais agente de código; `claude-progress.txt`; lista de
  funcionalidades toda "failing"; "work on only one feature at a time"; commit por feature; "leave the
  environment in a clean state". Falhas: tentar "one-shot" e "declare the job done". É um fluxo sequencial,
  não paralelo. anthropic.com/engineering/effective-harnesses-for-long-running-agents
- **Cache.** "Two sessions in different directories therefore build different prefixes and miss each
  other's cache", então cada worktree paga o seu. TTL de 1 h no chat principal da assinatura e de 5 min em
  subagentes/teammates. Leitura de cache = 0,1× do preço de entrada; escrita = 1,25× (5 min) ou 2× (1 h), com
  exceções por modelo. code.claude.com/docs/en/prompt-caching ;
  platform.claude.com/docs/en/build-with-claude/prompt-caching
- **O "87%".** O `/usage` sinaliza comportamentos acima de 10% do uso, como "long context" e "highly parallel
  sessions". code.claude.com/docs/en/vs-code

## 2. Como criadores trabalham
- **Boris Cherny.** "1/ I run 5 Claudes in parallel in my terminal. I number my tabs 1-5, and use system
  notifications…" e "2/ I also run 5-10 Claudes on claude.ai/code" (2/1/2026). "Spin up 3–5 git worktrees at
  once… the single biggest productivity unlock… Personally, I use multiple git checkouts" (31/1/2026). Sobre
  verificação: "give Claude a way to verify its work. If Claude has that feedback loop, it will 2-3x the
  quality… Make sure to invest in making this rock-solid." Fontes:
  api.fxtwitter.com/bcherny/status/2007179833990885678 (e …2007179836704600237, …2017742743125299476,
  …2007179861115511237). A soma "10-15 sessões" é secundária [INCERTO]. Ele é o autor da ferramenta e depende
  de verificação automática.
- **Simon Willison.** "I can only focus on reviewing and landing one significant change at a time."
  Paraleliza pesquisa, manutenção e provas de conceito; "Code that started from your own specification is a
  lot less effort to review". Não usa worktrees ("fresh checkout, often into /tmp"). Com 4 agentes: "by like
  11 AM, I am wiped out for the day." simonwillison.net/2025/Oct/5/parallel-coding-agents/ ;
  simonwillison.net/2026/Apr/2/lennys-podcast/
- **Armin Ronacher.** "a second check-out will do"; gerencie o estado compartilhado (arquivos, bancos). Em
  2026 critica a "competition… to run as many of these agents in parallel with almost no quality control" e
  diz que revisar um PR "takes many times longer". lucumr.pocoo.org/2025/6/12/agentic-coding/ ;
  lucumr.pocoo.org/2026/1/18/agent-psychosis/
- **Mitchell Hashimoto.** "I'm not [yet?] running multiple agents, and currently don't really want to";
  agente de fundo útil em 10-20% do dia; "Context switching is very expensive".
  mitchellh.com/writing/my-ai-adoption-journey
- **Peter Steinberger** (citado por Simon). "3-8 in parallel… most of them in the same folder", sem
  worktrees. Arriscado para este caso. simonwillison.net/2025/Oct/14/agentic-engineering/
- **Addy Osmani.** "ceiling… three to four threads"; "Your cognitive bandwidth doesn't parallelize."
  addyosmani.com/blog/cognitive-parallel-agents/
- **Leitura.** O teto prático é 3-5; quem trabalha sozinho e cuida de qualidade fica em 1-4. O limite é
  revisão e verificação, não geração.

## 3. Ferramentas
As nativas resolvem o Windows sem instalar nada: `claude -w`, Desktop com worktree, `claude agents`.
- **claude-squad**: 8.567★, push 20/8/2026. Precisa de tmux e gh. **Sem Windows nativo**: issues #275
  ("error starting tmux session: unsupported") e #248 abertas; só WSL. github.com/smtg-ai/claude-squad
- **Crystal**: depreciado em fev/2026, substituído por **Nimbalyst** (1.830★, MIT, push no dia; "macOS,
  Windows, Linux" na descrição do repo). github.com/nimbalyst/nimbalyst. Qualidade no Windows: [INCERTO].
- **Conductor**: só Mac ("on your Mac"), código fechado. conductor.build
- **ccmanager**: 1.257★, push 27/9/2026. O mantenedor diz "official support is only available for Linux and
  macOS"; no Windows, WSL. github.com/kbwo/ccmanager/issues/164
- **Vibe Kanban**: 28.259★, mas "sunsetting" desde 10/4/2026 (edição comunitária). vibekanban.com/blog/shutdown
- **uzi**: 581★, último push em 4/6/2025 (parado); usa tmux.
- **Claude Flow, hoje Ruflo**: 73.831★, ativo; `npx ruflo init` roda no PowerShell. É um enxame de agentes,
  com mais tokens por desenho. Uma auditoria de terceiro alega 15-25 mil tokens de overhead por sessão e "99%
  theater" (gist.github.com/roman-rr/ed603b676af019b8740423d2bb8e4bf6) [INCERTO, não reproduzido].
- **Sculptor** (Imbue): 235★, Mac/Linux, "experimental research preview".
- **container-use** (Dagger): 4.055★, "early development", instalação para macOS/Linux, exige Docker; issue
  #159 "Native windows support" aberta.
- **Custo de tokens**: gerenciadores de terminal/worktree não declaram custo próprio, mas nada foi medido
  [INCERTO]. Os que orquestram agentes de LLM (agent teams, Ruflo) adicionam tokens.

## 4. Decomposição que evita o "Frankenstein"
- **spec-kit** (140.072★). Template de tarefas: "[P]: Can run in parallel (different files, no
  dependencies)"; "Tests MUST be written and FAIL before implementation"; a fase Foundational "BLOCKS all
  user stories". github.com/github/spec-kit
- **Kiro** roda tarefas independentes em "waves" (kiro.dev/docs/specs/). **Taskmaster** (28.136★, tarefas
  com dependências) e **BMAD** (53.766★, papéis): paralelismo não verificado [INCERTO].
- **O Frankenstein documentado.** Cognition: "Actions carry implicit decisions, and conflicting decisions
  carry bad results". Subagentes em paralelo montam partes incompatíveis (exemplo do Flappy Bird); eles
  recomendam "a single-threaded linear agent". cognition.com/blog/dont-build-multi-agents
- **Compilador C da Anthropic (Carlini).** 16 agentes, quase 2.000 sessões, "just under $20,000", 2 bilhões
  de tokens de entrada e 140 milhões de saída.
  - "Merge conflicts are frequent, but Claude is smart enough to figure that out."
  - "Every agent would hit the same bug, fix that bug, and then overwrite each other's changes. Having 16
    agents running didn't help."
  - "the task verifier is nearly perfect, otherwise Claude will solve the wrong problem."
  - Ele quebrava funcionalidades existentes até montarem CI. anthropic.com/engineering/building-c-compiler
- **Cursor.** Com locks, "Twenty agents would slow down to the effective throughput of two or three"; a
  solução foi planejadores, operários e juiz. cursor.com/blog/scaling-agents
- **Receita comum** (contrato antes, posse de arquivos, um branch por vez, um integrador). Aparece em blogs,
  é coerente com a doc de agent teams e não traz medição de retrabalho [INCERTO]:
  mindstudio.ai/blog/parallel-agentic-development-claude-code-worktrees

## 5. Economia de tokens e limites
- **Mecanismo.** "Claude Code sends your full conversation with every request"; "a one-line question in a
  session that has been open all day still draws usage for the whole conversation"; `/clear` "costs
  nothing"; `/compact` "is itself a large request"; CLAUDE.md "under 200 lines". code.claude.com/docs/en/costs.
  Retomar sessão com mais de 100 mil tokens e mais de 1 h parada oferece "resume from summary" (/sessions).
- **Document & Clear** (Shrivu Shankar): "dump its plan and progress into a .md, /clear the state, then start
  a new session"; "Don't trust auto-compaction." blog.sshh.io/p/how-i-use-every-claude-code-feature. A
  Anthropic recomenda notas persistidas e subagentes que devolvem 1.000-2.000 tokens:
  anthropic.com/engineering/effective-context-engineering-for-ai-agents
- **Medição.** ccusage (18.863★; relatórios por dia e sessão, "5-Hour Blocks", cache criado e lido
  separados; `npx ccusage@latest`): github.com/ryoppippi/ccusage. Claude Code Usage Monitor (8.731★): os
  limites por plano do README são estimativas da comunidade [INCERTO].
- **Paralelo e cota.** Pro/Max compartilham limites entre Claude e Claude Code
  (support.claude.com/en/articles/11145838). A janela de 5 h e o limite semanal vêm de trecho de busca de
  support.claude.com/en/articles/11049741 (página não aberta) [INCERTO leve]. Oficial: cada sessão usa a cota
  "independently", e 10 agentes gastam cerca de 10× mais rápido. Relato: ao lançar cerca de 10 sessões de uma
  vez após o reset, só as 3-4 primeiras rodaram; as outras receberam "Server is temporarily limiting requests
  (not your usage limit)", e a issue foi fechada como "not planned".
  github.com/anthropics/claude-code/issues/53922 (caso único).
- **"Mesmo total, só mais rápido?" Não** [INFERÊNCIA do subagente, a partir do mecanismo acima]. O total
  tende a ser maior que o sequencial, por quatro motivos:
  1. cada janela abre com custo próprio (a doc simula cerca de 7,9 mil tokens de partida);
  2. os mesmos arquivos são relidos em várias janelas;
  3. há a janela integradora;
  4. há retrabalho.
  - Contrapeso: janelas menores custam menos por turno, porque cada turno relê o contexto inteiro. Exemplo,
    com base de 10 mil tokens e +4 mil por turno: 60 turnos numa janela releem cerca de 7,9 M tokens; em 3
    janelas de 20 turnos, cerca de 3,1 M.
  - Esse ganho vem das janelas curtas, e não do paralelismo. O paralelo compra tempo de relógio. O peso exato
    do cache read na cota da assinatura não é publicado [INCERTO].

## 6. Críticas
- **METR 2025.** 16 devs, 246 tarefas, "19% longer" (IC +2% a +39%); esperavam −24% e acreditaram −20%.
  metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/
- **METR, atualização de 24/2/2026.** Veteranos −18% (IC −38% a +9%), novos −4% (IC −15% a +9%); o sinal
  negativo significa menos tempo. De 30% a 50% dos devs evitaram tarefas sem IA. A medição é "unreliable for
  the fraction of developers who use multiple AI agents concurrently", e o estudo está sendo redesenhado.
  Conclusão: não existe boa medição do paralelo. metr.org/blog/2026-02-24-uplift-update/
- **Faros 2025** (10 mil+ devs, 1.255 equipes). +21% tarefas, +98% PRs, tempo de revisão +91%, tamanho de PR
  +154%, bugs +9% por dev; sem correlação no nível da empresa. faros.ai/blog/ai-software-engineering
- **Revisão e atenção.** Simon, Armin, Osmani e Mitchell (seção 2). Anthropic: poucas tarefas de código são
  paralelizáveis (seção 1).

## Síntese para este usuário (do subagente)
**Faz sentido?** Em parte.
- A economia de tokens vem de janelas curtas com handoff, que já são feitas. O paralelo gasta a cota até N×
  mais rápido e soma custo de integração.
- O ganho real é tempo de relógio, e só quando as partes são disjuntas e verificáveis por teste.
- No domínio clínico (erro silencioso), o gargalo é a verificação, não a geração. Boris, Carlini e a doc de
  boas práticas convergem: paralelo só com verificador "rock-solid".

**Condições, todas necessárias:**
- Interfaces congeladas em código (stubs e assinaturas) antes de dividir.
- Testes de aceitação por parte, escritos na janela de planejamento ou por outra janela, nunca pela própria
  trabalhadora.
- Posse de arquivos sem interseção. Constantes, schemas, enums, config e `conftest` só o integrador toca.
- Cada parte com pytest próprio, rodável isolado.
- Um oráculo para as regras clínicas (saídas já validadas, "golden files"), análogo ao GCC de Carlini.

**Quantas janelas:** 2 trabalhadoras e 1 integradora (que só abre quando as outras terminam). Teto de 3.
Referências: 3-5 (agent teams e Boris), 3-4 (Osmani), 1 (Mitchell). Com um único revisor humano e erro
silencioso, fique no lado baixo.

**Protocolo (planejar → N trabalhadoras → integradora):**
1. **Planejar** (plan mode ou entrevista, gerando SPEC.md): tarefas, arquivos donos, interfaces como código,
   critério de pronto, `[P]` só nas disjuntas. Fazer o commit na base e dar push (ou usar
   `worktree.baseRef: "head"`).
2. **Trabalhadoras:** `claude -w parte-a`, `claude -w parte-b`. No VS Code, abrir cada worktree numa janela
   própria. Cada uma instala o ambiente, lê só o seu cartão de tarefa, fica abaixo de cerca de 100 mil
   tokens, roda o pytest da sua parte, faz commit e escreve o handoff (o que tocou, decisões, pendências).
3. **Integradora** (contexto limpo, no papel de Reviewer): faz o merge de um branch por vez, em ordem de
   dependência, e roda a suíte completa a cada merge. Compara `git diff --stat` com a posse de arquivos (fora
   do escopo volta para a dona). Usa subagente revisor adversarial contra o SPEC.md, pedindo "gaps, not
   style". Conflito semântico volta para a trabalhadora dona.
4. **Portão final:** pytest completo, golden clínicos e a leitura do Ettore das regras alteradas.
5. **Teste de uma semana:** medir com ccusage (blocos de 5 h, tokens), tempo e número de correções do
   integrador. Manter o paralelo só se o tempo ganho superar o retrabalho [INFERÊNCIA].

**Não paralelizar:**
- lógica de regra clínica nova ou alterada ("actions carry implicit decisions");
- qualquer arquivo compartilhado;
- depuração de um único bug (Carlini: agentes sobrescrevendo-se);
- trabalho exploratório de muito vai-e-vem (a doc manda ficar na conversa principal);
- migrações de esquema ou de dados;
- tarefas encadeadas;
- dados de entrada compartilhados: worktrees não trazem arquivos ignorados, e copiá-los via
  `.worktreeinclude` duplica dado sensível [INFERÊNCIA];
- enxames e agent teams (7-15× tokens, sem isolamento).

**Paralelizar:** testes de caracterização do código existente, documentação, adaptadores e IO isolados,
refatoração mecânica em arquivos disjuntos, pesquisa e revisão somente leitura.

**Windows nativo:** usar `claude -w`, Desktop ou `claude agents`. Evitar claude-squad, ccmanager, Conductor,
Sculptor e container-use, que não têm suporte nativo.
