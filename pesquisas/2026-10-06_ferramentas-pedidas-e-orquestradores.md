# Ferramentas pedidas pelo nome e orquestradores de agentes — o que serve e onde (06/10/2026)

- **A pergunta:** o Ettore pediu Cartographer, Claude Code Setup, claude-mem, Headroom e "Ominiclaude", e "uma skill
  para orquestrar os agentes de modo eficiente". O que cada uma faz de verdade, quanto custa, que risco traz (dado de
  paciente, cota, Windows) e onde instalar? Qual orquestrador e qual regra para o Workflow/ultracode?
- **A data:** 06/10/2026 (estrelas e versões pela API do GitHub nesse dia).
- **O projeto que pediu:** claude-kit (fluxo de trabalho; rodada 3 do grill — `decisoes\2026-10-06_entrevista-fluxo.md` §7).
- **Conferir de novo depois de:** 06/12/2026 (OMC, claude-mem e Headroom soltam versões quase diárias).
- **Método:** repositórios clonados e lidos (manifestos, ganchos, `SKILL.md`, docs) + documentação oficial; nada foi
  instalado nem executado. Marcas: [A] afirmação do autor sem medição independente; [I] inferência. Tokens fixos =
  (nome + descrição)/4 [I].

## Conclusão em poucas linhas

1. **Nada disso entra no nível global.** Cartographer, `claude-code-setup`, `claude-mem` e Headroom: **não instalar**.
   OMC ("Ominiclaude"): **só numa pasta de teste**, contido, sem o `/omc-setup` (que reescreve o `~\.claude\CLAUDE.md`).
2. **Orquestrador principal: `subagent-driven-development` (SDD) do Superpowers**, instalado como skill avulsa com as 3
   de que depende — sem o plugin (o gancho dele injeta `using-superpowers` em toda sessão). Serial, com paradas que
   coincidem com a Q10 (destrutivo, segurança, efeito fora do worktree, plano quebrado) e livro-razão em arquivo.
3. **Workflow nativo / ultracode:** só para muitos itens iguais e independentes (≥ 20), sem decisão humana no meio e
   sem dado de paciente. A palavra "ultracode" num prompt dispara execução: desligar o gatilho em `/config`.
4. **Memória de pesquisa de literatura não é memória automática:** precisa de fato citável e conferível (DOI/PMID,
   citação literal com página, "conferido na fonte"), em arquivo e no git — não resumo de atividade comprimido por
   modelo.

## As cinco ferramentas pedidas

| ferramenta (fonte) | o que é | custo | riscos | veredito |
|---|---|---|---|---|
| **Cartographer** — [kingbootoshi/cartographer](https://github.com/kingbootoshi/cartographer) (748 estrelas, último commit 12/05/2026; homônimos com 0-18) | 1 skill + `scan-codebase.py`: o Opus orquestra, subagentes Sonnet leem **todo** o código e gravam `docs/CODEBASE_MAP.md`; o passo 7 **edita o CLAUDE.md** | fixo ≈120 tokens; por uso, o repositório inteiro lido (o autor fala em "significant tokens" [A]) | exclui só binário e `.gitignore`: `csv`, `json`, `txt` entram — dado de paciente solto iria para o mapa e para o CLAUDE.md [I]; o mapa envelhece ao lado do ESTADO/ADR; `python3` no Windows | **não instalar**; para repositório legado ou alheio, copiar a skill, apagar os passos 7 e 8 e rodar sem dado de paciente |
| **Claude Code Setup** — [plugin oficial](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/claude-code-setup) v1.0.0 | 1 skill (`claude-automation-recommender`): relatório no chat, 1-2 recomendações por categoria (MCP, skills, ganchos, subagentes, plugins); diz que não cria nem altera arquivo | fixo ≈95 tokens; por uso 11 KB + 32 KB de referências | as listas pendem para web/JS e sugerem Context7, Playwright MCP e GitHub MCP — os três já recusados com motivo em 04/10 | **não instalar**; se quiser comparar com a `recursos-do-projeto`, `--scope local` numa pasta de teste |
| **claude-mem** — [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem) (96,8 mil estrelas, 356 versões, Apache-2.0) | ganchos em quase todo evento: **PostToolUse `*` grava entrada e saída de toda ferramenta**; PreToolUse `Read` nega reler arquivo já "observado"; worker residente (Bun, porta 37777); SQLite + Chroma em `~/.claude-mem/` | 22 skills ≈ 1,6 mil tokens fixos [I]; compressão por **Haiku 4.5 via Agent SDK, cobrada da assinatura** (até 2 agentes simultâneos) | captura tudo o que o Claude vê (inclusive dado de paciente); `<private>` é manual; **telemetria PostHog ligada** (`DO_NOT_TRACK=1`); o instalador oferece login num "observador" na nuvem deles; exige Bun (não instalado aqui) | **não instalar**, nem no espaço de pesquisa; dá para ligar só numa pasta (`--scope local`), mas worker, banco e config seguem globais [I] |
| **Headroom** — [headroomlabs-ai/headroom](https://github.com/headroomlabs-ai/headroom) (74,5 mil estrelas, antes `chopratejas/headroom`) | proxy local (MITM) que comprime saídas de ferramenta, logs e JSON antes do modelo (`headroom wrap claude`, porta 8787, `ANTHROPIC_BASE_URL`) | ganhos do autor: busca 21%, exploração 42%, logs/incidentes até 57% [A]; código-fonte passa sem compressão; Python + Markdown ganham pouco [I] | vê tudo em texto puro e guarda os originais **sem criptografia por 30 min**; beacon anônimo ligado; com URL base própria o Claude Code perde o Tool Search, e **na extensão do VS Code isso quebra a renderização** (a doc manda desligar); o Defender barrou um binário na instalação | **não instalar**; teste só no terminal, pasta sintética, com `HEADROOM_BEACON=off`, `--no-subscription-tracking`, `--code-memory none` |
| **"Ominiclaude" = oh-my-claudecode (OMC)** — [Yeachan-Heo/oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode) (39,6 mil estrelas, v5.6.2 de 06/10, MIT); o homônimo exato `OmniNode-ai/omniclaude` (4 estrelas) é camada de outra plataforma e não serve | 47 skills, 19 agentes (7 fixados em Opus), 21 comandos, MCP, **30 registros de gancho em 11 eventos**; estado em `.omc/` por projeto; modos `autopilot`, `ralph`, `team`, `execute`, `verify`, `ralplan`, `deep-interview`, `ultragoal` (`ultrawork` saiu na 5.0.0; não existe `eco`) | fixo ≈ 3,5 mil tokens com o bloco no CLAUDE.md [I]; `team` ≈ 16 mil por uso; "economiza 30-50%" é [A] | **`/omc-setup` sobrescreve o `~\.claude\CLAUDE.md`** e a statusline; segundo dono do estado (`.omc/` × `ESTADO.md`); ganchos Stop mandam continuar ("The boulder never stops"), contra o "parar para decisão"; memória concorrente; `omc ask` manda código a outros fornecedores; Windows nativo "experimental" (WSL2 recomendado) | **só numa pasta de teste com git e dado sintético**: `claude plugin install oh-my-claudecode@omc --scope local`, **sem** `/omc-setup`. Valem `deep-interview`, `ralplan`, `execute`, `verify`, `review`. Evitar `autopilot`, `ralph`, `team`, `ask`, `wait`, notificações, `remember`/`wiki`/`self-improve`/`skillify`. Teto: `OMC_BUDGET_ENFORCE=active` + `OMC_RUN_BUDGET_TOKENS`; desligar: `DISABLE_OMC` |

## Orquestradores comparados

| opção | mecanismo e quando serve | custo | onde para para o humano | veredito |
|---|---|---|---|---|
| **SDD do Superpowers** ([skill](https://github.com/obra/superpowers/blob/main/skills/subagent-driven-development/SKILL.md); 295,8 mil estrelas, v6.4.2) | o controlador lê o plano; **um implementador novo por tarefa, nunca em paralelo**; revisão de especificação e de qualidade por tarefa (até 5 rodadas); revisão final no modelo mais capaz; livro-razão em arquivo | `SKILL.md` 32 KB (≈ 8 mil) + 20 KB de prompts; ≥ 2 contextos novos por tarefa + 1 final | destrutivo, segurança, efeito fora do worktree (merge, push, publicar), plano quebrado; no fim, lista as decisões que tomou | **principal**, dentro de UMA fase, com ≥ 4 tarefas |
| OMC | plano → execução → revisão → verificação; `autopilot`/`ralph` por gancho Stop; `team` | ≈ 3,5 mil fixos | `autopilot`/`ralph` só ao verificar ou cancelar | só teste contido (acima) |
| GSD ([open-gsd/gsd-core](https://github.com/open-gsd/gsd-core)) | 72 skills, ~35 agentes, ganchos; estado em `.planning/`; `gsd-autonomous` encadeia fases | ≈ 1,6 mil fixos [I]; skills pesadas declaram `effort: max` | só decisão ou bloqueio | não instalar (segundo dono do estado) |
| `chief-of-staff` (Matt) | 1,2 KB: uma sessão longa só coordena subagentes por ponteiros | ≈ 0 fixo; a sessão cresce | nenhuma definida | só como lente, numa sessão supervisionada (já instalada) |
| `implement-spec` (Matt) | tickets como grafo; um implementador por ticket em worktree, **em paralelo**; mesclador; revisão final | 2,8 KB; sem teto de paralelismo | nenhuma; termina com PR pronto | só tickets independentes, ≤ 3 implementadores, 1 ticket de teste antes, sem push (já instalada) |
| **Workflow nativo** ([docs](https://code.claude.com/docs/en/workflows)) | script que o Claude escreve; agentes em segundo plano; 16 simultâneos, 1.000 por execução | aviso acima de 25 agentes ou 1,5 milhão de tokens (só aviso); os agentes herdam o modelo da sessão | aprovação ao lançar; **sem entrada no meio** | só pela regra abaixo |

**Instalar o SDD** (comando da documentação do CLI, não executado):
`npx skills add obra/superpowers --skill subagent-driven-development --skill requesting-code-review --skill using-git-worktrees --skill finishing-a-development-branch -g -a claude-code --copy -y`
— as três extras são necessárias (o SDD aponta para `../requesting-code-review/code-reviewer.md` e chama as outras). Atritos [I]: o
plano precisa de cabeçalhos "Task N"; referências com prefixo `superpowers:`; fixar o modelo em cada despacho (sem ele, herda o
da sessão). O `docs\ESTADO.md` continua dono do estado; o livro-razão `.superpowers/sdd/` é descartável.

## A regra do Workflow e do ultracode (proposta [I], a reconciliar com a Q13)

- **Roteamento:** menos de 4 tarefas → sessão normal e subagentes comuns; 4 a ~20 tarefas de um plano → SDD (serial,
  custo previsível); ≥ 20 itens independentes do mesmo formato (arquivos, módulos, artigos), só leitura ou cópia
  isolada, verificáveis por teste ou revisor, sem decisão humana no meio e sem dado de paciente → Workflow.
- **`/effort ultracode`:** nunca por padrão, só com motivo escrito — vale para toda tarefa da sessão e **desliga** o
  aviso de execução grande, o limite de simultâneos e a aprovação do modo automático.
- **Desligar o "Ultracode keyword trigger" em `/config`:** citar a palavra num prompt dispara execução.
- **Teto técnico:** `workflowSizeGuideline: "small"` (< 5 agentes; conselho), `CLAUDE_CODE_WORKFLOW_MAX_CONCURRENT_AGENTS=4`
  (teto duro de simultâneos), `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=2`; antes, uma fatia pequena; agentes de leitura em
  Sonnet. (A Q13 fixou o teto em 10 agentes sem perguntar: o plano reconcilia os dois.)
- **`/deep-research`:** vale para pergunta de literatura sem dado de paciente, em tamanho pequeno, conferindo as fontes.
- **Times de agentes** (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`): manter desligado (≈ 7× o custo [A]; painéis não
  funcionam no VS Code nem no Windows Terminal).

## Fontes (lidas em 06/10/2026)

- https://github.com/kingbootoshi/cartographer
- https://github.com/anthropics/claude-plugins-official/tree/main/plugins/claude-code-setup
- https://github.com/thedotmack/claude-mem (hooks: `plugin/hooks/hooks.json`)
- https://support.claude.com/en/articles/15036540-use-the-claude-agent-sdk-with-your-claude-plan
- https://github.com/headroomlabs-ai/headroom (docs: `security-model.mdx`, `limitations.mdx`, `troubleshooting.mdx`)
- https://github.com/Yeachan-Heo/oh-my-claudecode · https://github.com/OmniNode-ai/omniclaude
- https://github.com/obra/superpowers/blob/main/skills/subagent-driven-development/SKILL.md
- https://github.com/open-gsd/gsd-core
- https://github.com/mattpocock/skills (in-progress/chief-of-staff, engineering/implement-spec)
- https://code.claude.com/docs/en/workflows · https://code.claude.com/docs/en/costs · https://code.claude.com/docs/en/discover-plugins
- https://github.com/vercel-labs/skills (CLI do `npx skills`)
