# Modelo e esforço no Claude Code (geração 5.5)

- **Pergunta:** qual modelo e qual esforço dão a melhor qualidade pelo menor uso no Claude Code — os
  números de índice, custo por tarefa e preço se confirmam? O que a documentação oficial confirma sobre
  esforço padrão, CLAUDE.md, regras, skills e subagentes? O que usuários experientes medem (planejar com o
  forte e executar com o barato, compactar × handoff, CLAUDE.md grande, subagentes, workflows)?
- **Data:** 03/10/2026
- **Projeto que pediu:** a janela da skill `uso-do-claude` (aberta em `C:\DESOSP`).
- **Onde a decisão mora (resumo, não cópia):**
  - `C:\CLAUDE\skills\uso-do-claude\fontes\claude-uso-modelos.md` — a pesquisa original (provisória, com
    19 links e marcadores de busca).
  - `C:\CLAUDE\skills\uso-do-claude\reference.md` §1 (fatos da documentação) e §4/§4b (esta verificação).
  - Aplicações: `C:\planilha-hc\docs\14_MODELO_E_ESFORCO.md`.
- **Fontes (principais; ~64 no corpo):**
  - https://artificialanalysis.ai/models/releases/claude-sonnet-5-5 e /claude-opus-5-5
  - https://www.anthropic.com/claude-sonnet-5-5 · https://www.anthropic.com/claude-opus-5-5
  - https://platform.claude.com/docs/en/about-claude/pricing
  - https://code.claude.com/docs/en/model-config · /memory · /skills · /sub-agents · /costs · /prompt-caching
  - https://claude.dev/blog/spending-your-effort (esforço × tempo × tokens)
- **Conclusão:**
  - No Claude Code, Opus 5.5 e Sonnet 5.5 vêm em `medium`; Fable 5.1 em `high`. Opus 5.5 é o modelo
    padrão no Max.
  - "Planejar com o forte e executar com o barato" só compensa em `low`/`medium`; acima disso o Opus dá a
    mesma nota por menos (Opus medium 51 por US$ 1,34 × Sonnet xhigh 52 por US$ 2,75).
  - `max` pode ser pior que `xhigh` (FrontierCode do Sonnet 5.5: 52,1% × 46,2%) — dado do fornecedor.
  - Trocar de esforço no meio da sessão mantém o cache; trocar de modelo (inclusive opusplan) não.
  - CLAUDE.md: a doc pede < 200 linhas; o único estudo controlado não achou perda de aderência até 500
    linhas, mas o custo em tokens é certo.
  - Subagentes em leque gastaram 2,6–5,9× os tokens de entrada da execução em série numa tarefa pequena.
  - Não há teste controlado de compactar × handoff na geração 5.5.
- **Conferir de novo depois de:** 03/11/2026 (modelo, preço e padrão de esforço envelhecem em semanas; o
  Haiku 5.5 estava anunciado e não lançado).
- **Como foi feita:**
  - Subagente de verificação independente, ~117 chamadas web — o relatório abaixo, sem mudança de conteúdo.
  - No mesmo dia, um segundo subagente conferiu a documentação oficial (memória, skills, subagentes) e
    marcou como "não encontrado" esforço padrão por modelo, `effortLevel`, ultracode e opusplan; isso
    ficou **obsoleto** — a verificação de 04/10 (`2026-10-04_verificacao-recursos-claude-code.md`) e o
    relatório abaixo responderam. O que ele confirmou está no `reference.md` §1.
  - Pesquisa anterior, superada: em 20/09 um workflow de 6 agentes no DESOSP levantou os níveis de esforço
    (low, medium, high, xhigh = "Extra", max; `ultracode` é modo, não nível; `/code-review ultra` é nuvem,
    disparado só pelo usuário). O texto dela em `C:\DESOSP_APP\docs\PROPOSTA_APP_DESOSP.md` está
    desatualizado; vale o desta pesquisa.

---

**Verification report on the Claude model claims, 3 Oct 2026**

Limits on this check:
- My tools can't fetch reddit.com, and search engines index almost no Reddit threads from the 5.5 era. Any Reddit claim below comes second-hand, through blogs, Hacker News or X summaries.
- The Artificial Analysis (AA) pages are live and their numbers drift a little between snapshots.

Evidence classes: A = controlled or reproducible benchmark, B = observable test, C = experience report, D = vendor, promo or opinion.

## The seven claims

**1. AA numbers: CONFIRMED. The scores match exactly; Sonnet's cost and latency figures have drifted. (A)**
- Sonnet 5.5 low→max scores 36/41/47/52/56 on the live pages. Cost per task is now $0.42/$0.59/$1.12/$2.75/$7.67.
  - The report's $0.41/$1.08/$2.74/$7.60 match an earlier snapshot. officechai, for example, quotes $7.60.
  - https://artificialanalysis.ai/models/releases/claude-sonnet-5-5
- Opus 5.5 matches exactly: low 42 $0.55, high 54 $1.82, xhigh 56 $3.46, max 58 $5.98. Medium, not in the report, is 51 $1.34.
  - https://artificialanalysis.ai/models/releases/claude-opus-5-5
- Latency: the live comparison page gives end-to-end time (500 tokens) of 6.65 s for Sonnet medium versus 14.90 s for Opus low. Time to first token is 1.21 s versus 7.86 s.
  - An older indexed snapshot showed 6.00 s versus 18.95 s. Sonnet is faster either way, but "18.5 s" is not current.
  - https://artificialanalysis.ai/models/comparisons/claude-sonnet-5-5-medium-vs-claude-opus-5-5-low

**2. FrontierCode worse at max than xhigh: CONFIRMED. (D)**
- Footnote 2 of https://www.anthropic.com/claude-sonnet-5-5 gives xhigh 52.1% versus max 46.2%.
- The footnote says: "At Max effort, Sonnet 5.5 more often ran Claude Code's code-review skill, which splits the review across many subagents, and in two cases Cognition examined, this led to a timeout or to extra edits beyond the task's scope."
- Independent support (B): in Simon Willison's test, Sonnet 5.5 at max used up the 128K output budget ($1.28) and returned no answer. Xhigh finished for 5.74¢. https://simonwillison.net/2026/Sep/28/claude-sonnet-5-5/

**3. Opus 5.5 beats Fable 5.1: CONFIRMED as vendor numbers. (D)**
- https://www.anthropic.com/claude-opus-5-5 gives 66.4 vs 55.8 (Terminal-Bench 4.0), 54.4 vs 50.3 (FrontierCode) and 57.8 vs 51.8 (CursorBench).
- Caveats on the same page:
  - The Terminal-Bench figure for Opus is at xhigh effort.
  - The CursorBench caption says that at default effort (medium), Opus scores 52.5% against Fable at max 51.8%.
  - Anthropic writes that "benchmark margins have become a less reliable guide."
- Independent check (A): Vals.ai Terminal-Bench 4.0, updated 1 Oct, has Opus 65.15% and Fable 58.08%.
  - 22 of the 198 Opus attempts were served by fallback models. Counting those as failures gives 58.08% for Opus and 50.00% for Fable.
  - https://www.vals.ai/benchmarks/terminal-bench-4

**4. Sonnet beats Opus on Terminal-Bench 4.0 per Anthropic: CONFIRMED. (D)**
- Anthropic reports 70.6% versus 66.4%.
- Independent results are mixed (A):
  - AA, using the mini-swe-agent harness, has Sonnet at max 63.6% and Opus 59.6%. https://artificialanalysis.ai/evaluations/terminalbench-4-0
  - Vals has Opus slightly ahead, 65.15% versus 64.14%, and Sonnet costs more per test there ($16.51 vs $13.20).

**5. Pricing: CONFIRMED exactly.**
- https://platform.claude.com/docs/en/about-claude/pricing
- Input/output per million tokens: Haiku 4.5 $1/$5, Sonnet 5.5 $2/$10, Opus 5.5 $4/$20, Fable 5.1 $10/$50.
- Cache reads: $0.10, $0.20, $0.20 (Opus at 0.05×) and $0.25 (Fable at 0.025×).

**6. Default effort: CONFIRMED, with one clarification.**
- In Claude Code, both Opus 5.5 and Sonnet 5.5 default to medium, and Fable 5.1 to high. https://code.claude.com/docs/en/model-config
- On the API, Sonnet 5.5 defaults to high, Opus 5.5 to medium and Fable 5.1 to high.
- The report's "Opus 5.5 default" line doesn't say what it means. Opus 5.5 is the default *model* on Max, and its default effort is medium.

**7. Haiku 5.5 announced, not released: CONFIRMED.**
- Anthropic said "in the coming weeks" in its 22 Sep and 28 Sep posts.
- The models overview still lists Haiku 4.5 as current, with retirement "not sooner than October 15, 2026." There is no Haiku 5.5 price. https://platform.claude.com/docs/en/models/overview

## What experienced users report

**(a) Plan with the strong model, execute with a cheaper one**
- The AA data say the saving holds only at low and medium effort:
  - Sonnet medium and Opus low score about the same (41 vs 42) at about the same cost ($0.59 vs $0.55), and Sonnet is about twice as fast.
  - Above that, Opus is cheaper for the same score: Opus medium scores 51 for $1.34 versus Sonnet xhigh 52 for $2.75. At max, Opus costs $5.98 versus Sonnet's $7.67.
- A reproducible creator test (A, 48 runs, files published) ran four well-scoped PHP tasks. https://wmedia.es/en/tips/claude-code-sonnet-5-5-vs-opus-5-5-benchmark
  - Sonnet 5.5 medium and Opus 5.5 medium both passed 12 of 12.
  - Sonnet cost $0.88 versus $1.91, with median times of 13.4 s versus 21.8 s.
- The docs say every opusplan plan-mode toggle is a model switch, which rebuilds the prompt cache. https://code.claude.com/docs/en/prompt-caching
- Addy Osmani on Anthropic's claude.dev blog: "Measure it on your own tasks before you make it a default." https://claude.dev/blog/what-a-task-costs-on-opus-5-5/
- I found no controlled test of opusplan on the 5.5 models.

**(b) Long sessions with compaction vs fresh sessions with handoff files**
- Anthropic's engineering post on long-running agents found compaction "isn't sufficient" and moved to progress files with fresh contexts (C/D). https://anthropic.com/engineering/effective-harnesses-for-long-running-agents
- The docs say `/compact` reads the whole conversation it summarizes, while `/clear` costs nothing.
- A controlled study (arXiv 2605.10039; 1,650 sessions; Sonnet 4.6 and Opus 4.6) found the odds of following an instruction fall about 5.6% for each additional function generated within a session. That finding was post-hoc, not pre-registered. (A, older models)
- Anthropic's own telemetry: context per request has grown 2.6×, and the Opus 5.5 cache-read price was cut 60% to make long sessions cheaper. (D)
- I found no controlled comparison of compaction versus handoff on the 5.5 models. Matt Pocock's "smart zone of about 100K tokens" (April 2026) is opinion.

**(c) Large CLAUDE.md files**
- The official docs say to "target under 200 lines... Longer files consume more context and reduce adherence." Imports don't reduce the cost, because imported files also load at launch.
- The only controlled study (the same arXiv paper) found no detectable effect on adherence between 25 and 500 lines, with Bayes factors supporting no effect. (A)
- So the token cost is certain, the adherence harm is unproven up to 500 lines, and nothing has been tested beyond that.
- Your `C:\DESOSP\CLAUDE.md` measures 2,602 lines and 178 KB by `wc`. My rough estimate is about 50K tokens; `/context` will give the real number.
- It loads into every main-session request (from cache), and also into every general-purpose or custom subagent.
  - The built-in Explore and Plan agents skip it.
  - A custom agent can skip it with `omitClaudeMd: true`. https://code.claude.com/docs/en/sub-agents

**(d) Subagents: do they save or cost tokens?**
- The docs say a subagent keeps the parent's context clean, but its own requests count toward your limits. Subagent caches last 5 minutes even on a subscription, versus 1 hour for the main session.
- A reproducible test (Systima, July 2026, older Opus and Fable 5) found 2- to 5-agent fan-outs used 2.6–5.9× the input tokens of doing the work in sequence, with no time saved on a small task. (A/B) https://systima.ai/blog/subagent-tax
- The common reading: subagents pay off for verbose output (tests, logs, searches) or when run on cheaper models, and cost extra on small tasks.

**(e) Agent teams, ultracode and workflows**
- Official figures:
  - Agent teams use about 7× more tokens when teammates run in plan mode.
  - With ultracode on, a session "reaches a session or weekly limit sooner," and the "Large workflow" warning (over 25 agents or 1.5M projected tokens) is switched off.
  - A run can have up to 1,000 agents, 16 at a time by default.
  - https://code.claude.com/docs/en/workflows and https://code.claude.com/docs/en/costs
- Anecdotes, second-hand (C):
  - A Max user burned 20% of the weekly limit on the first day of using workflows.
  - A Hacker News user ran 62 Opus 4.8 subagents and hit the 5-hour cap in 18 minutes.

**(f) Burning Max-plan limits with Fable or high effort**
- Official: on Max you can spend up to 50% of the weekly limit on Fable, and Fable uses limits "faster than other Claude models"; beyond that it bills usage credits. https://support.claude.com/en/articles/15424964-claude-fable-models-on-your-plan
- paddo.dev analysed 10 days of the author's own transcripts (B/C): Fable 5.1 produced 22% more output tokens per turn than Fable 5. It also relays Reddit reports of a 5-hour window gone in 15–20 minutes. https://paddo.dev/blog/fable-5-1-two-meters/
- AA (A): on its index, Sonnet 5.5 at max produced 420M output tokens versus 260M for Opus 5.5 at max.

**(g) Judgement-heavy text work, and planning/interview skills**
- HAQQ legal test (B; 10 prompts; 120 blind verdicts from non-Anthropic LLM judges): Opus 5.5, Opus 5 and Fable 5.1 could not be told apart, and Opus 5.5 cost about half as much as Fable. https://www.haqq.ai/blog/claude-opus-5-5-legal-benchmark
- AA-Omniscience factual accuracy (A): Opus 5.5 66%, Fable 5.1 67%, Sonnet 5.5 54%.
  - Secondary sources say Sonnet hallucinates less (47% vs 59%); I could not verify that on AA's page.
- A HealthBench Professional listing has Sonnet 69.2% and Opus 65.6%, but it is an aggregator and the source is unclear, so treat it as D.
- I found no data on which model runs grilling or interview skills better. Pocock (April 2026, before the 5.5 models) implemented with Sonnet and reviewed with Opus in a fresh context.

**(h) Matt Pocock's skills repo**
- `skills/productivity/grill-me/SKILL.md` is now a stub:
  - frontmatter `name: grill-me`, `description: A relentless interview to sharpen a plan or design.`, `disable-model-invocation: true`
  - body: *Call the Skill tool with "grilling".*
- The real logic is in `skills/productivity/grilling/SKILL.md`:
  - It maps the plan as a design tree.
  - Each round asks every question whose prerequisites are settled, numbered, each with a recommended answer.
  - It sends a sub-agent to look up facts rather than asking you.
  - It stops when no open questions remain, and does not act until you confirm.
- Install for Claude Code, per the README: `claude plugins install mattpocock-skills` (or `/plugin install mattpocock-skills`), then run `/setup-matt-pocock-skills` once per repository. It is a read-only bundle from the official marketplace that updates itself.
- Editable install: `npx skills@latest add mattpocock/skills`. skills.sh shows `npx skills add https://github.com/mattpocock/skills --skill grill-me`.
- The `skills` CLI installs to `.claude/skills/` in the project, or `~/.claude/skills/` with `-g`. It links to one shared copy by default, or copies the files.
- My inference: installing only grill-me leaves it calling a `grilling` skill that may not exist, so install both. This session already has a `grilling` skill available.

## New and well-supported (October 2026)

- **Advisor tool (experimental).** With Sonnet as the main model, `/advisor opus` lets Claude consult Opus at decision points. Turning it on or off doesn't break the cache. Advisor tokens count toward plan limits. Anthropic's April numbers, on older models: +2.7 points on SWE-bench Multilingual at 11.9% lower cost than Sonnet alone. https://code.claude.com/docs/en/advisor
- **Effort can change mid-session for free on the 5.5 models.** On Opus 5.5, Sonnet 5.5 and Fable 5.1, changing effort keeps the cache. Changing model does not, and that includes opusplan toggles, a skill whose frontmatter names a model, and safety fallbacks. So choose the model per window and adjust effort freely.
- **Safety-classifier fallback.** If a request on Opus 5.5 is flagged for biology content, it re-runs on Opus 5 and the session stays on Opus 5; Sonnet 5.5 just refuses. Clinical text could trip this. The session header shows the active model, and `switchModelsOnFlag: false` makes Claude Code ask instead of switching.
- **Auto-compaction comes very late.** Models with a 1M context window auto-compact only at about 967K tokens. `/autocompact 200k` compacts earlier.
- **Instruction-file housekeeping.**
  - `/doctor prompt-audit` (v2.1.283+) checks for outdated or conflicting instructions, and `/doctor` proposes trims to CLAUDE.md.
  - Block-level `<!-- -->` comments in CLAUDE.md are stripped before Claude sees them, so they cost no tokens.
  - Edits to CLAUDE.md apply only after `/clear`, `/compact` or a restart.
- **`/usage` shows where plan usage goes.** It attributes usage to skills, subagents, plugins and MCP servers, and flags long-context or cache-miss patterns. In the VS Code extension this is in the Account & usage dialog. It also shows a prompt-cache hit line with the likely cause of the last miss.
- **The word `ultracode` typed in any prompt starts a workflow**, including in the VS Code panel. Alt+W dismisses it, and the trigger can be turned off in `/config`.
- **Opus 5.5 launch perks.** The launch raised 5-hour limits and gave subscribers one banked limit reset (Settings > Usage). Secondary sources say the reset expires about 22 October.
- **Token estimates may undercount.** Since Opus 4.7 the tokenizer produces about 30% more tokens for the same text, so older estimates are low.
