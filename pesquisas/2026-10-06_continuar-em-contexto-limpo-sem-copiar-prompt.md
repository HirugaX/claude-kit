# Continuar em contexto limpo sem copiar prompt — como especialistas e projetos resolveram (06/10/2026)

- **A pergunta:** dividir o trabalho em janelas curtas economiza tokens, mas o Ettore vira "office boy" (copia o
  prompt da próxima janela, abre, cola, escolhe modelo e esforço). Como outros mantiveram a economia de contexto com
  menos intervenção humana? Fonte primária de cada padrão.
- **A data:** 05-06/10/2026 (estrelas e datas pela API do GitHub nesses dias).
- **O projeto que pediu:** claude-kit (fluxo de trabalho; entrevista de 05/10).
- **Conferir de novo depois de:** 06/01/2027 (padrões mudam a cada modelo; a Anthropic manda re-testar o harness).
- Marcas: [A] = afirmação do autor sem medição independente; [I] = inferência. Complementa
  `2026-10-05_sessoes-memoria-plugins-claude-code.md` (a parte oficial do Claude Code).

## Conclusão em poucas linhas

1. **Não existe `/clear` programático.** Três issues pediram (#20267, #24257 duplicatas; #35150 fechada por
   inatividade em 08/07/2026). Zero intervenção só com **processo novo** (script, `claude --bg`) ou **subagentes**
   na mesma sessão. Com `/clear` + gancho, sobram dois gestos humanos.
2. **A própria Anthropic (24/03/2026) tirou o reset de contexto do harness com o Opus 4.5**: sessão contínua com
   compactação automática; o reset "adds orchestration complexity, token overhead, and latency". O ganho de
   **qualidade** do reset depende do modelo; o de **custo** (cada chamada relê o contexto) não depende [I].
3. **Os padrões que se repetem:** (a) estado em arquivo + git, nunca na conversa; (b) uma tarefa por contexto,
   dentro da "zona boa" (40-60% da janela para Dex Horthy; ~100 mil no GSD e no wayfinder; 125-150 mil para Matt
   Pocock; ~170 mil para Huntley); (c) orquestrador fino + subagentes de contexto novo que devolvem pouco; (d) humano
   só nos pontos de alavancagem (especificação, plano, merge); (e) verificação determinística como freio.
4. **Riscos locais:** no Windows nativo o Claude Code roda comandos **sem sandbox** (só macOS, Linux, WSL2); nesta
   máquina não há WSL, Docker, `jq` nem `uv`. O `claude -p` conta na assinatura, mas a Anthropic chegou a anunciar
   (e pausou em 15/06/2026) tirá-lo dos limites do plano: laço de `claude -p` tem risco de política.
5. **Nenhuma medição independente** de economia de tokens foi achada para qualquer desses padrões.

## Quem dispara a janela nova, nos casos achados

| quem | exemplos |
|---|---|
| o humano, com `/clear` | GitHub Spec Kit, GSD, HumanLayer (padrão), `handoff` do Matt Pocock |
| um script externo | Ralph original (`while :; do cat PROMPT.md \| claude; done`), quickstart da Anthropic (laço Python) |
| o próprio agente, por processo novo | `claude --bg` (`claude-handoff` do Matt), `humanlayer launch`, `gt handoff` (Gas Town, tmux) |
| ninguém: a mesma sessão segue | subagente por tarefa (Superpowers, GSD, Roo), gancho Stop (`ralph-loop` oficial, `/goal`) |

## Por item (o essencial)

- **Anthropic, harness de longa duração (26/11/2025):** agente inicializador cria `claude-progress.txt`,
  `feature_list.json` e o 1º commit; cada sessão lê o progresso + `git log`, faz UMA funcionalidade e commita;
  laço Python com cliente novo. Exige chave de API (não a assinatura).
- **Dex Horthy / HumanLayer:** pesquisa → plano → implementação, contexto em 40-60%, revisão humana na pesquisa e no
  plano. Comandos `create_handoff` / `resume_handoff` (o humano cola o caminho na janela nova). O repositório diz que
  o código está depreciado (virou produto comercial); os comandos markdown seguem portáveis.
- **Ralph (Huntley):** processo novo a cada volta, estado em `PROMPT.md`/`fix_plan.md`, um item por volta, freio =
  testes. O plugin oficial `ralph-loop` **roda na mesma sessão** (gancho Stop reenvia o prompt; o contexto acumula) e
  no Windows pede Git Bash, `jq` e perl.
- **GSD (agora `open-gsd/gsd-core`):** orquestrador magro + subagentes com 200 mil limpos que escrevem `.planning/`
  (`STATE.md`, `PLAN.md`); o humano roda cada fase. A doc admite que a sessão orquestradora "fills up over time".
- **Superpowers (`subagent-driven-development`):** subagente novo por tarefa + revisão por tarefa, sem pausar entre
  tarefas; para em destrutivo, segurança, efeito fora do worktree (merge, push) ou plano quebrado. Admite o custo
  ("a fresh context per task and per review").
- **Matt Pocock:** `claude-handoff` = resumo + `claude --bg --name …` (elimina o office boy); `chief-of-staff` =
  sessão que só coordena subagentes; `wayfinder` = um ticket de decisão por sessão (~100 mil tokens). Diz que o
  trabalho multi-fase "requires constant human involvement" e que a maior parte do uso dele é com humano no laço.
- **Steve Yegge:** Beads = memória e fila de tarefas (gancho SessionStart injeta 1-2 mil tokens), não dispara
  sessão; Gas Town = orquestração de muitos Claude Code, pede WSL no fluxo completo e, nas palavras dele, "Do not
  use Gas Town if you care about money". Não serve a um dev solo.
- **Especificação em disco:** OpenAI ExecPlans (documento vivo com Progress, Surprises, Decision Log; "possible to
  restart from only the ExecPlan"); GitHub Spec Kit (o humano encadeia, uma fase por vez); Kiro (aprovação em
  requisitos e desenho).
- **Cline `/newtask`** faz o handoff para tarefa nova num comando; **Roo Orchestrator** arquivado; **Kilo** trocou o
  Orchestrator por subagentes. No Claude Code não há equivalente nativo de um comando.
- **Vozes:** Boris Cherny (sessões começam no modo plano; dar ao Claude um jeito de verificar o próprio trabalho);
  Simon Willison (subagentes poupam o contexto do topo); Addy Osmani (spec, plano, um passo por vez, commit como
  ponto de salvamento); Karpathy (define "context engineering"). Nenhum deles mediu economia.
- **`showClearContextOnPlanAccept: true`:** o menu de aprovação do plano ganha "Yes, clear context and …": aprova,
  limpa e implementa só com o plano. Escondido por padrão desde a 2.1.81. Não verificado na extensão do VS Code.
- **Gancho SessionStart + `clear` + arquivo:** existe em projetos pequenos (`STRML/cc-clear-handoff`, 0 estrelas, e
  outros 0-4 estrelas); o padrão é simples de escrever em Python, sem dependência.

## O encaixe para um dev solo, Windows, VS Code, dado de saúde [I]

Do menor ao maior risco: (1) plano em arquivo ao estilo ExecPlan + aprovar o plano limpando o contexto; (2) estado
em arquivo + gancho SessionStart(`clear`) próprio (dois gestos humanos), ou `claude --bg` (prévia; para em "Needs
input" se pedir permissão; o resumo vira linha de comando, então nada de dado pessoal nele); (3) subagente por
tarefa nas partes mecânicas, parando antes de merge e push; (4) laço `claude -p` só em fase mecânica com teste forte,
em clone com dado sintético, com limite de voltas, sem `--dangerously-skip-permissions` e sem `git push` — e só
depois de resolver sandbox (WSL2) e a política de cobrança. Evitar: `claude-mem` (capta tudo em SQLite + Chroma),
Continuous-Claude-v3 (parado), Gas Town.

## Fontes (lidas em 05-06/10/2026)

- https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding
- https://www.anthropic.com/engineering/harness-design-long-running-apps
- https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- https://www.anthropic.com/engineering/multi-agent-research-system
- https://github.com/humanlayer/advanced-context-engineering-for-coding-agents/blob/main/ace-fca.md
- https://github.com/humanlayer/humanlayer/tree/main/.claude/commands
- https://ghuntley.com/ralph/ · https://github.com/ghuntley/how-to-ralph-wiggum · https://github.com/snarktank/ralph
- https://github.com/anthropics/claude-plugins-official/tree/main/plugins/ralph-loop · https://code.claude.com/docs/en/goal
- https://github.com/open-gsd/gsd-core
- https://github.com/obra/superpowers/blob/main/skills/subagent-driven-development/SKILL.md
- https://github.com/mattpocock/skills · https://www.aihero.dev/ai-coding-dictionary/smart-zone · https://www.aihero.dev/tips-for-ai-coding-with-ralph-wiggum
- https://github.com/gastownhall/beads · https://github.com/gastownhall/gastown · https://steve-yegge.medium.com/welcome-to-gas-town-4f25ee16dd04
- https://github.com/openai/openai-cookbook/blob/main/articles/codex_exec_plans.md · https://github.com/github/spec-kit · https://kiro.dev/docs/specs/
- https://docs.cline.bot/core-workflows/using-commands · https://docs.roocode.com/features/boomerang-tasks · https://kilo.ai/docs/code-with-ai/agents/orchestrator-mode
- https://x.com/bcherny/status/2007179845336527000 · https://simonwillison.net/guides/agentic-engineering-patterns/subagents/
- https://addyosmani.com/blog/ai-coding-workflow/ · https://x.com/karpathy/status/1937902205765607626
- https://code.claude.com/docs/en/settings-reference · https://code.claude.com/docs/en/sandboxing · https://code.claude.com/docs/en/agent-view
- https://github.com/anthropics/claude-code/issues/35150 · https://github.com/STRML/cc-clear-handoff
- https://support.claude.com/en/articles/15036540-use-the-claude-agent-sdk-with-your-claude-plan
