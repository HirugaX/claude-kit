# Sessões, memória, plugins e ganchos no Claude Code — o que a documentação confirma (05/10/2026)

- **A pergunta:** uma sessão consegue abrir outra com contexto limpo, sem o usuário copiar e colar o prompt? Como
  funcionam a memória entre sessões, os plugins (por projeto, entre dois PCs, custo de contexto) e os ganchos úteis
  ao fluxo de janelas? O que mudou entre a 2.1.234 e a 2.1.290?
- **A data:** 05/10/2026 (changelog até a 2.1.290, do mesmo dia).
- **O projeto que pediu:** claude-kit (refinar o fluxo de trabalho: `uso-do-claude` + `recursos-do-projeto`).
- **Conferir de novo depois de:** 05/11/2026 (agent view e Projects são "research preview"/beta; mods têm dias).
- Complementa, sem repetir: `2026-10-04_janelas-paralelas-e-tokens.md`, `2026-10-04_verificacao-recursos-claude-code.md`,
  `2026-09-28_claude-code-na-nuvem.md`, `2026-10-04_organizacao-com-claude-code.md`.

## Conclusão em poucas linhas

1. **Nenhum recurso oficial abre sozinho uma aba interativa nova e envia o prompt.** Os quatro que tiram a cópia
   manual: (a) `/clear` + gancho `SessionStart` com matcher `clear`, que injeta até 10.000 caracteres (um arquivo
   "próximo passo") antes do primeiro prompt; o usuário ainda digita algo para começar; (b) o link
   `vscode://anthropic.claude-code/open?prompt=<texto>` abre aba nova com o prompt **preenchido, sem enviar**
   (no Windows: `Start-Process "vscode://..."`); (c) `showClearContextOnPlanAccept: true`: aprovar o plano com a
   opção que limpa o contexto do planejamento; (d) `claude --bg "prompt" --model X --effort Y --name N`
   (agent view, *research preview*): sessão nova em segundo plano, gerida por `claude agents|attach|logs|stop`.
2. `/fork` e `--bg` com retomada copiam a conversa: não dão contexto limpo. `claude -p` é sessão nova que sai com o
   resultado (retoma por `session_id`). Mensagens entre sessões (`SendMessage`) só falam com sessões vivas.
3. **Modelo e esforço por projeto:** `model` no `settings.json` do projeto vale a cada sessão nova; `modelSettings`
   (2.1.251+) grava esforço por modelo. Gancho não troca modelo; `PreModelSwitch` (2.1.251+) pode **bloquear** a
   troca para um modelo indesejado (o atalho `sonnet` que abre o Sonnet 5). A statusline recebe `model.id`,
   `effort.level` e `context_window.used_percentage`.
4. **Memória automática:** carrega só as primeiras **200 linhas ou 25 KB** do `MEMORY.md`; é por repositório e por
   máquina (não sincroniza); `autoMemoryDirectory` muda o lugar. Existe `~/.claude/rules/` (regras de usuário,
   carregam antes das de projeto). Subagente pode ter memória própria (`memory: user|project|local`).
5. **Plugins:** nome e descrição de cada skill entram em toda sessão onde o plugin está ligado; ganchos não custam
   contexto; `claude plugin details <nome>` mostra o custo. Skill com `disable-model-invocation: true` sai do
   contexto (confirmado na sessão de 05/10: só as skills "sozinhas" apareceram na lista). `enabledPlugins` por
   projeto liga e desliga; `true` só no settings de projeto não baixa o plugin numa máquina nova.
6. **Dois PCs:** marketplace privado num repositório GitHub privado funciona com as credenciais git da máquina
   (HTTPS precisa de `gh auth login` + `gh auth setup-git`; ou SSH sem senha). Atualização automática vem
   desligada. Plugin e skill de usuário valem igual no terminal, na extensão do VS Code e no app Desktop.
7. **Ganchos:** `SessionStart` (fontes `startup`, `resume`, `clear`, `compact`, `fork`); `Stop` com
   `decision: "block"` faz o Claude continuar (até 8 vezes seguidas) e serve de portão ("o handoff foi
   gravado?"), mas roda a cada turno; `PreCompact` existe; `Notification` tem `agent_completed` e
   `agent_needs_input`.
8. **A extensão do VS Code embute o próprio CLI** e não põe `claude` no PATH: o `claude` do PATH é outro binário,
   que só atualiza com `claude update` (estava na 2.1.234; atualizado para a 2.1.290 em 05/10).

## Novidades 2.1.234 → 2.1.290 que mexem no fluxo

| versão | o quê |
|---|---|
| 2.1.251 | `/effort` grava por modelo (`modelSettings`); ganchos `PreModelSwitch`/`PostModelSwitch`; custo de recache no SessionStart |
| 2.1.252 | `/skill-doctor` (custo e uso de cada skill) |
| 2.1.257 | `--bg` com `--resume`; `/effort` só da sessão (`s` no seletor) |
| 2.1.265 | o VS Code arquiva sessões paradas há 14 dias |
| 2.1.269 | `claude plugin eval` |
| 2.1.271 | `omitClaudeMd` para agente próprio |
| 2.1.273 | plugins e marketplaces sincronizados do claude.ai |
| 2.1.277 | `AGENTS.md` como alternativa; `/tasks` no VS Code |
| 2.1.283 | modo automático padrão; MCP carregado sob demanda |
| 2.1.287 | **mods** (plugin de funções: `$.prompt.submit`, troca de modelo/esforço por requisição); "Run in background" no VS Code |
| 2.1.288 | `--resume` não perde o contexto restaurado pela compactação |
| 2.1.290 | `claude attach`/`logs` por nome parcial; subagente retomado mantém o cache |

## Não achado na documentação (não afirmar)

Comando `/handoff` nativo; o agent view dentro do VS Code; se o `PreCompact` bloqueia; se um gancho ou o Claude
pode chamar `claude --bg` (é um comando de shell comum, sem prescrição); "FleetView" (não é nome oficial).

## Fontes (lidas em 05/10/2026)

- Subagentes: https://code.claude.com/docs/en/sub-agents · Workflows: https://code.claude.com/docs/en/workflows
- Agent teams: https://code.claude.com/docs/en/agent-teams · Headless: https://code.claude.com/docs/en/headless
- CLI: https://code.claude.com/docs/en/cli-reference · Agent view: https://code.claude.com/docs/en/agent-view
- Mensagens entre sessões: https://code.claude.com/docs/en/cross-session-messaging
- VS Code: https://code.claude.com/docs/en/vs-code · Deep links: https://code.claude.com/docs/en/deep-links
- Modos de permissão: https://code.claude.com/docs/en/permission-modes · Settings: https://code.claude.com/docs/en/settings-reference
- Ganchos: https://code.claude.com/docs/en/hooks-guide e https://code.claude.com/docs/en/hooks
- Comandos: https://code.claude.com/docs/en/commands · Sessões: https://code.claude.com/docs/en/sessions
- Modelo: https://code.claude.com/docs/en/model-config · Skills: https://code.claude.com/docs/en/skills
- Memória: https://code.claude.com/docs/en/memory · Boas práticas: https://code.claude.com/docs/en/best-practices
- Plugins: https://code.claude.com/docs/en/plugins/install, /plugins/loading, /plugins/measure, /plugins/host-marketplace
- Avaliação de plugin: https://code.claude.com/docs/en/plugin-evals · Mods: https://code.claude.com/docs/en/plugins/mods/reference
- Statusline: https://code.claude.com/docs/en/statusline · Rotinas: https://code.claude.com/docs/en/routines
- Projects: https://code.claude.com/docs/en/claude-projects · Changelog: https://code.claude.com/docs/en/changelog
