# Verificação de 11 afirmações sobre recursos do Claude Code

- **Pergunta:** um relatório de terceiros sobre a stack do Claude Code (`C:\CLAUDE\fontes\claude-efficiency-report.md`)
  diz coisas sobre o modelo do Explore, os campos de subagente, a retomada de subagente, o MCP adiado, os
  ganchos, a statusline, a precedência de `modelSettings`, regras com `paths:`, skills, Playwright CLI × MCP
  e qual modelo usar. O que a documentação oficial confirma, com citação literal?
- **Data:** 04/10/2026
- **Projeto que pediu:** DESOSP_APP (escolha de recursos e stack, skill `recursos-do-projeto`).
- **Onde a decisão mora (resumo, não cópia):** `C:\CLAUDE\skills\uso-do-claude\reference.md` §2b;
  `C:\DESOSP_APP\docs\RECURSOS_CLAUDE_DESOSP.md`.
- **Fontes (principais):**
  - https://code.claude.com/docs/en/sub-agents · /hooks · /statusline · /settings-reference · /memory · /skills · /model-config · /costs
  - https://github.com/microsoft/playwright-mcp · https://github.com/microsoft/playwright-cli
- **Conclusão:**
  - O Explore **herda o modelo da sessão** (Haiku só se você definir um Explore próprio com `model: haiku`);
    Plan e general-purpose também herdam.
  - Subagente aceita `model`, `tools`, `skills`, `memory`, `effort`, `omitClaudeMd` (v2.1.271+), `isolation`,
    entre outros. Retoma-se por `SendMessage`; Explore e Plan não se retomam. Cache de subagente: 5 min.
  - Definições de MCP ficam adiadas por padrão.
  - Gancho `PostToolUse` devolve mensagem ao Claude por exit 2 (stderr) ou `additionalContext`; stdout com
    exit 0 vai só para o log.
  - A statusline recebe `model.id` e `effort.level`.
  - Em `modelSettings`, vence o arquivo de maior precedência (local > projeto > usuário), modelo a modelo.
  - Regra sem `paths` carrega sempre; com `paths`, quando o Claude lê ou edita arquivo que casa.
  - Playwright recomenda a CLI (`@playwright/cli`) com skills em vez do MCP, por gastar menos tokens.
  - O padrão no Max é Opus 5.5, não Sonnet.
- **Conferir de novo depois de:** 04/11/2026.
- **Como foi feita:** subagente de verificação, ~42 buscas de página e 1 busca web, mais duas leituras
  diretas (`model-config`, `settings-reference`) na sessão. Abaixo, o relatório como voltou, sem mudança de
  conteúdo. Ele avisa que parte das páginas em inglês veio por um leitor que resume, conferida em cópias
  zh-CN.

---

1. VERDICT: partly (Haiku only via override; the default is not Haiku). Explore: "Model: the main conversation's model." (Fable sessions: "the Opus model that the `opus` alias resolves to".) Plan: "inherits from the main conversation". General-purpose: "the `CLAUDE_CODE_SUBAGENT_MODEL` model if you set one ... otherwise the main conversation's model". Override: "A user or project subagent named `Explore` overrides the built-in and keeps its own `model` field, so define one with `model: haiku`". https://code.claude.com/docs/en/sub-agents

2. VERDICT: confirmed. Table fields: `name`, `description`, `tools`, `disallowedTools`, `model`, `permissionMode`, `maxTurns`, `skills`, `mcpServers`, `hooks`, `memory`, `background`, `omitClaudeMd`, `effort`, `isolation`, `color`, `initialPrompt`, `experimental`. `skills`: "The full skill content is injected, not only the description." `memory`: "`user`, `project`, or `local`". `effort`: "Overrides the session effort level. Default: inherits from session." `omitClaudeMd`: "Set to `true` to launch this subagent without the user, project, and local CLAUDE.md files ... Requires Claude Code v2.1.271 or later". https://code.claude.com/docs/en/sub-agents#supported-frontmatter-fields

3. VERDICT: confirmed. "Claude uses the `SendMessage` tool with the agent's ID or name as the `to` field to resume it." "Resumed subagents retain their full conversation history, including all previous tool calls, results, and reasoning." The resumed run "can keep reading the prompt cache the original run warmed", but subagent requests "get five minutes even on a subscription" (TTL). Explore and Plan are "one-shot and return no agent ID, so Claude can't resume them." https://code.claude.com/docs/en/sub-agents#resume-subagents ; https://code.claude.com/docs/en/prompt-caching#subagents-and-the-cache

4. VERDICT: confirmed. "MCP tool definitions are deferred by default, so only tool names and server instructions enter context until Claude uses a specific tool." (costs) "Set `ENABLE_TOOL_SEARCH=auto` to load schemas upfront when they fit within 10% of the context window" (context-window); SDK page: "`auto:5` activates when those definitions reach 5% of the context window". Gap: English `mcp#scale-with-mcp-tool-search` was truncated by my fetcher; the zh-CN table agrees. https://code.claude.com/docs/en/costs ; /context-window ; /agent-sdk/tool-search

5. VERDICT: confirmed (c partly verified). (a) SessionStart adds `source`, optional `model`, `agent_type`, `session_title`; `model`: "The active model identifier. It can be omitted, for example after `/clear`". (b) Yes: "Claude Code adds stdout it treats as plain text to Claude's context"; `additionalContext`: "String added to Claude's context at the start of the conversation, before the first prompt." (c) Yes. Exit 2: "| `PostToolUse` | No | Shows stderr to Claude; the tool already ran |". Or `hookSpecificOutput.additionalContext`, placed "next to the tool result". Plain exit-0 stdout does not reach Claude: "It is written to the debug log only." `decision: "block"`: English section is past my fetcher's truncation; zh-CN says it adds `reason` beside the result, original output still visible. https://code.claude.com/docs/en/hooks ; /hooks-guide

6. VERDICT: confirmed. "`model.id`, `model.display_name` | Current model identifier and display name"; "`effort.level` | Current reasoning effort (`low`, `medium`, `high`, `xhigh`, or `max`). Reflects the live session value, including mid-session `/effort` changes. Absent when the current model does not support the effort parameter". Sample: `"model": {"id": "claude-opus-5-5", ...}`, `"effort": {"level": "high"}`. https://code.claude.com/docs/en/statusline#available-data

7. VERDICT: confirmed. "In order, highest precedence first: 1. Managed settings ... 2. Command line arguments ... 3. Project local settings (`.claude/settings.local.json`) 4. Shared project settings (`.claude/settings.json`) ... 5. User settings (`~/.claude/settings.json`)". `model` and `modelSettings` both have scope `Any file`, and "`Any file` means all four" files, so project beats user (local beats project). "Across files, Claude Code resolves each model separately: the highest-precedence settings file ... decides". https://code.claude.com/docs/en/settings#settings-precedence ; /settings-reference#modelsettings

8. VERDICT: confirmed. "Rules without a `paths` field are loaded unconditionally and apply to all files. Path-scoped rules trigger when Claude uses the Read, Write, or Edit tool on a file matching the pattern, not on every tool use." https://code.claude.com/docs/en/memory#path-specific-rules

9. VERDICT: confirmed. Project row: "`.claude/skills/<skill-name>/SKILL.md` | Sessions in this repository". Cost: "Descriptions at start, full content when used | Low (descriptions every request)". "The listing always contains every skill name, but ... Claude Code drops some descriptions to fit the listing's character budget ... The budget scales at 1% of the model's context window." https://code.claude.com/docs/en/skills ; /features-overview ; /context-window

10. VERDICT: confirmed. playwright-mcp README, "Playwright MCP vs Playwright CLI": "Modern **coding agents** increasingly favor CLI–based workflows exposed as SKILLs over MCP because CLI invocations are more token-efficient: they avoid loading large tool schemas and verbose accessibility trees into the model context, allowing agents to act through concise, purpose-built commands." Official CLI: repo `microsoft/playwright-cli`, npm `@playwright/cli` (Microsoft); install: `npm install -g @playwright/cli@latest`, then `playwright-cli install --skills`. https://github.com/microsoft/playwright-mcp ; https://github.com/microsoft/playwright-cli

11. VERDICT: partly. Aliases: "`sonnet` | Uses the latest Sonnet model for daily coding tasks"; `opus` "for complex reasoning tasks"; `haiku` "for simple tasks"; `fable` "for your hardest and longest-running tasks". Costs: "Sonnet handles most coding tasks well and costs less than Opus. Reserve Opus for complex architectural decisions or multi-step reasoning." But the default is Opus, not Sonnet: "Pro, Max, Team, Enterprise, and Anthropic API: defaults to Opus 5.5". Fable: "the most capable models in Claude Code, suited to tasks larger than a single sitting". Blog (2026-07-07): "Pick a smaller model when the work is routine ... Pick a larger model when the problem is genuinely hard." On the API `opus` = Opus 5.5, `sonnet` = Sonnet 5.5; Haiku 4.5 by name: NOT FOUND. https://code.claude.com/docs/en/model-config ; /costs ; https://claude.com/blog/claude-model-and-effort-level-in-claude-code

Reliability: English sub-agents, hooks, skills, model-config and settings-reference pages came via a summarizing fetcher (wording may be slightly off); frontmatter, skill paths, default model and SessionStart fields were re-checked against raw zh-CN copies.
