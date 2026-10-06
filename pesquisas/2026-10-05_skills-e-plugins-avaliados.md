# Skills e plugins avaliados para o kit — o que entrou, o que ficou de fora e por quê (05/10/2026)

- **A pergunta:** das listas das pesquisas de 04-05/10 (`fontes\Relatorio_Claude_Code_Top_50_Skills_Plugins.md`,
  `fontes\claude-efficiency-report.md`, `fontes\Claude_Workbench_Prompts\`) e do marketplace oficial, o que vale
  instalar no notebook, sem redundância, para programação, decisão, UX, documentos, memória e controles?
- **A data:** 05/10/2026.
- **O projeto que pediu:** claude-kit (pedido do Ettore: "instale o que achar relevante; cuidado com as redundantes").
- **Conferir de novo depois de:** 05/12/2026, ou ao rodar `npx skills update -g` / `claude plugin update`.
- **Método:** cada candidato lido na fonte (repositório clonado, `SKILL.md`, ganchos, `plugin.json`) antes de decidir;
  o custo de contexto medido com `claude plugin details`. Estrelas não contaram como qualidade.

## Conclusão em poucas linhas

- **Entraram 24 skills no kit** (pelo `npx skills ... --copy` + `ligar_claude.py`) **e 4 plugins** (escopo de usuário).
  Das 24, 15 são "só `/`" (`disable-model-invocation: true`): não custam contexto até serem chamadas.
- **O núcleo é a família do grill (Matt Pocock)**, que já funcionava: entrevista → especificação → tarefas →
  implementação → retrospectiva, mais memória de decisão (glossário e ADR).
- **Ficaram de fora** as memórias automáticas de terceiros (captam conversa com dado de paciente e gastam cota),
  os "harnesses" que competem com o método do Ettore, e tudo o que repete um recurso nativo.
- **O CC Safety Net** acertou 13 de 15 comandos simulados; a lacuna (apagar dentro da pasta de trabalho) se fecha com
  a política `scripts\safety-net-politica.json`, que **o Ettore aplica** (o plugin não deixa o Claude mudá-la).

## O que entrou

| item | origem (commit lido) | como chama | por quê |
|---|---|---|---|
| `domain-modeling`, `diagnosing-bugs`, `tdd`, `codebase-design`, `prototype`, `writing-for-agents` | mattpocock/skills `4588b32` | sozinha | decisão em glossário/ADR; laço de diagnóstico; teste primeiro; desenho de módulo; protótipo; escrever skill e CLAUDE.md |
| `grill-with-docs`, `to-spec`, `to-tickets`, `implement`, `implement-spec`, `setup-matt-pocock-skills`, `improve-codebase-architecture`, `wayfinder`, `retro`, `claude-handoff`, `chief-of-staff`, `to-questionnaire`, `wait-what`, `teach` | mattpocock/skills `4588b32` | só `/` | a cadeia do grill até o código; trabalho de várias sessões; sessão nova em segundo plano; orquestração por subagentes (as duas últimas são "in-progress" no repositório) |
| `web-design-guidelines` | vercel-labs/agent-skills `063bee9` | sozinha | revisão de UI contra as Web Interface Guidelines (baixa a lista atual) |
| `property-based-testing`, `spec-to-code-compliance`, `goal-prompt` | trailofbits/skills `82fe822` | sozinha | testes de domínio inteiro (datas, âncoras); código contra o contrato; condição do `/goal` |
| `cc-safety-net` (plugin, 2.6.0) | kenryu42/cc-marketplace | gancho + skill só `/` | barra comando destrutivo e leitura de segredo no Bash **e no PowerShell** (`src/hosts/claude-code/hook.ts:8-9`); ~79 tokens fixos |
| `claude-md-management` | claude-plugins-official | sozinha + `/revise-claude-md` | auditar e enxugar CLAUDE.md; ~177 tokens fixos |
| `session-report` | claude-plugins-official | sozinha | relatório HTML de tokens, cache, prompts caros; ~72 tokens |
| `frontend-design` | claude-plugins-official | sozinha | direção visual de tela; ~80 tokens |

Já existiam e continuam: `grill-me`, `grilling` (iguais ao repositório, fora o fim de linha), `uso-do-claude`,
`recursos-do-projeto`; e as de documento sincronizadas pelo claude.ai (`xlsx`, `docx`, `pdf`, `pptx`, `docs`).

## O que ficou de fora

| item | motivo verificado |
|---|---|
| thedotmack/claude-mem `115540c` | ~20 skills no plugin (várias repetem `handoff`/`make-plan`/`do`), serviço próprio, captura das saídas de ferramenta, oferta de nuvem (cmem.ai) |
| Digital-Process-Tools/claude-remember `249cb73` | resume cada sessão chamando o Haiku pelo `claude` (gasta cota) e guarda resumos de conversa |
| OthmanAdi/planning-with-files `dab9d16` | `SKILL.md` de 38 KB; ganchos em SessionStart, UserPromptSubmit, Pre/PostToolUse, Stop: um segundo dono do estado |
| hookify (oficial) | ganchos chamam `python3`, que neste Windows é o atalho da Microsoft Store (falha: "Python não foi encontrado") |
| security-guidance (oficial) | revisão por LLM a cada `Stop` e instalação do Agent SDK no SessionStart; `/security-review` nativo cobre |
| GoogleChrome/modern-web-guidance `650eb83` | descrição "MANDATORY: Execute FIRST for all HTML/CSS and clientside JS tasks"; roda `npx -y modern-web-guidance@latest` a cada uso |
| nextlevelbuilder/ui-ux-pro-max-skill `477bcb2` | repete `frontend-design` + `revisar-tela`; a skill `design` gera logo por APIs externas |
| pyright-lsp (oficial) | no VS Code a integração da IDE já entrega os diagnósticos do editor ao Claude |
| superpowers, ECC, gstack, GSD, oh-my-claudecode, ruflo | harnesses que decidem o processo; conflitam entre si e com o método do kit (a pesquisa e o Workbench dizem o mesmo) |
| code-review, feature-dev, pr-review-toolkit, code-simplifier (oficiais); `code-review` do Matt | `/code-review`, `/simplify`, `/security-review` são nativos; o do Matt teria o mesmo nome |
| `handoff`, `research`, `ask-matt`, `triage`, `pr`, `wizard`, `git-guardrails-claude-code` (Matt) | gravam fora do repositório, ignoram a biblioteca de pesquisas, apontam para skills não instaladas, ou bloqueiam todo `git push` |
| Context7, GitHub MCP, Playwright/Chrome MCP | recusados com motivo no `desosp-app\docs\RECURSOS_CLAUDE_DESOSP.md` (04/10); nada mudou |
| K-Dense-AI/scientific-agent-skills `92ace75` | 177 skills num plugin só; útil para pesquisa clínica, não para os apps; onde instalar fica para a entrevista |
| duckdb/duckdb-skills `7feda8e` | 9 skills sempre no contexto (inclui S3 e geoespacial); útil para análise avulsa; decisão na entrevista |

## O teste do CC Safety Net (15 chamadas simuladas, nada executado)

Passaram, como devem: `git status`, `pytest`, `git push origin main`, `rm -rf ./build`, `Get-ChildItem`, ler README.
Barrados, como devem: `git reset --hard`, `git push --force`, `git clean -fd`, `git checkout -- .`, `bash -c "git reset --hard"`,
ler `.env`, ler `~\.claude\.credentials.json`. **Passaram e não deviam:** `rm -rf` e `Remove-Item -Recurse` numa pasta de
projeto **dentro** da pasta de trabalho (o plugin só barra apagar fora dela). Script: o `testar_safety_net.py` do
rascunho da sessão (entrega JSON ao gancho por `subprocess`, porque a ferramenta Bash engole a barra invertida).

## Fontes

- https://github.com/mattpocock/skills · https://github.com/vercel-labs/agent-skills · https://github.com/trailofbits/skills
- https://github.com/kenryu42/claude-code-safety-net · https://github.com/kenryu42/cc-marketplace
- https://github.com/anthropics/claude-plugins-official · https://github.com/anthropics/skills
- https://github.com/thedotmack/claude-mem · https://github.com/Digital-Process-Tools/claude-remember
- https://github.com/OthmanAdi/planning-with-files · https://github.com/GoogleChrome/modern-web-guidance
- https://github.com/nextlevelbuilder/ui-ux-pro-max-skill · https://github.com/K-Dense-AI/scientific-agent-skills
- https://github.com/duckdb/duckdb-skills
