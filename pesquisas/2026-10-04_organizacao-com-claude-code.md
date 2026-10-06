# Como outros organizam projetos com o Claude Code — estrutura, marca do que é da IA, portabilidade, ganchos

- **Pergunta:** como outros usuários organizam arquivos, pastas e projetos com o Claude Code no Windows —
  distinguir o que a IA cria, manter legenda, levar a configuração a outro computador, aplicar o padrão em
  projeto novo? Há skill pronta? Como um gancho pode reagir à criação de pasta?
- **Data:** 04/10/2026
- **Projeto que pediu:** entrevista das cores de pasta (notebook).
- **Fontes (principais; as demais no corpo):**
  - https://code.claude.com/docs/en/claude-directory
  - https://code.claude.com/docs/en/hooks
  - https://code.claude.com/docs/en/plugins/overview e https://code.claude.com/docs/en/plugins/host-marketplace
  - https://learn.microsoft.com/en-us/windows/win32/shell/how-to-customize-folders-with-desktop-ini
  - https://github.com/karanb192/claude-code-hooks
  - O Reddit não estava acessível às ferramentas.
- **Conclusão:** ninguém usa cor ou ícone de pasta para separar o que é da IA do que é do humano; o mais comum
  é pasta separada + um índice mantido pela IA. Regra escrita é probabilística; só gancho garante. Para levar
  skills + ganchos + scripts entre PCs, o caminho documentado é um plugin num repositório git privado
  (CLAUDE.md pessoal e rules vão por git comum). Riscos do arranjo do notebook: o hardlink do CLAUDE.md pode
  se separar quando o Claude grava trocando o arquivo inteiro; skill ligada por junção some do menu `/` do
  app Desktop.
- **Conferir de novo depois de:** 04/11/2026 (o Claude Code muda toda semana).
- **Como foi feita:** subagente Explore (Sonnet), 161 chamadas de ferramenta. O texto abaixo é o relatório
  dele, sem mudança de conteúdo.

---

**Limites:** Reddit não é acessível às ferramentas (domínio bloqueado), então não há evidência de Reddit
[INCERTO]. Base: docs oficiais e changelog (Claude Code 2.1.289, 03/out/2026), HN, GitHub (estrelas e status
de issues pela API).

## 1. Estrutura de projeto
- Padrão oficial e mais usado: `CLAUDE.md` na raiz + `.claude/` (settings.json, rules/, skills/, agents/) no
  git; `settings.local.json` e `CLAUDE.local.md` fora; `~/.claude` é pessoal; commands/ virou skills.
  https://code.claude.com/docs/en/claude-directory [VERIFICADO EM FONTE]
- CLAUDE.md por pasta: os de pastas acima carregam no início; os de subpastas só quando Claude lê arquivos
  ali; meta <200 linhas; `.claude/rules/*.md` com `paths:` para escopo.
  https://code.claude.com/docs/en/large-codebases [VERIFICADO EM FONTE]
- AGENTS.md: ~60k projetos (https://agents.md). Claude o lê direto desde v2.1.277 se não houver CLAUDE.md;
  com ambos, `@AGENTS.md` dentro do CLAUDE.md (a doc desaconselha symlink no Windows). HN 741 pts:
  https://news.ycombinator.com/item?id=49760187 [VERIFICADO EM FONTE]
- Por quê: instruções são probabilísticas, só hook garante
  (https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more); CLAUDE.md curto,
  detalhes em pasta (https://www.humanlayer.dev/blog/writing-a-good-claude-md, HN 748 pts) [VERIFICADO EM FONTE]
- Rascunho/handoff: scratchpad nativo por sessão em `%TEMP%\claude\<projeto>\<sessão>\scratchpad\` (só com
  login claude.ai; hooks recebem `scratchpad_dir`) e auto memory
  (`~/.claude/projects/<proj>/memory/MEMORY.md`, local da máquina) [VERIFICADO EM FONTE]. "Memory Bank" da
  Cline (https://docs.cline.bot/prompting/cline-memory-bank) e `handoff.md` via hooks são padrões de
  comunidade; adoção real [INCERTO].

## 2. Marcar o que é de IA
- Nativo: só commits/PRs (trailer `Co-Authored-By`, ajustável em `attribution`).
  https://code.claude.com/docs/en/settings-reference [VERIFICADO EM FONTE]
- Marca da Anthropic (modelos lançados desde 02/ago/2026; anteriores em transição): marca-d'água invisível
  em texto e C2PA em png/jpg/svg, inclusive no Claude Code. A página não diz que código/markdown em disco é
  marcado e chama a detecção de "não conclusiva"; não serve como sistema próprio.
  https://support.claude.com/en/articles/16266773-how-claude-marks-ai-generated-content [VERIFICADO EM FONTE]
- Git: git-ai (nota por linha, suporta Claude Code, 2,8k estrelas) https://github.com/git-ai-project/git-ai;
  spec Agent Trace https://www.infoq.com/news/2026/02/agent-trace-cursor/ [VERIFICADO EM FONTE]; não testado.
- Pasta dedicada + manifesto (padrão mais frequente): fonte humana imutável / wiki escrita pela IA +
  `index.md` + `log.md` (Karpathy) https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f;
  `_ORG/_MANIFEST.md`, underscore = contabilidade da IA (57 estrelas)
  https://github.com/smithjoshua/claude-code-cowork-skills-file-organizer; sistema `AGNT` só da IA dentro de
  Johnny.Decimal (4 estrelas) https://github.com/jabez007/johnny-decimal-zettelkasten [VERIFICADO EM FONTE]
- `.gitattributes linguist-generated` existe, mas só visto em uso para código gerado por ferramenta;
  cabeçalho ou prefixo "IA" em arquivos: sem convenção difundida [INCERTO].
- Registro por hook: session-logger (async, 529 estrelas) https://github.com/karanb192/claude-code-hooks. Sem
  hook: as transcrições `~/.claude/projects/*/*.jsonl` guardam cada Write (apagadas após 30 dias por padrão)
  [VERIFICADO EM FONTE]
- Ícone/cor de pasta para IA x humano: não encontrado. O mecanismo existe: `desktop.ini` com `IconFile`,
  `IconIndex` e `InfoTip` (tooltip = legenda) + `attrib +s` na pasta.
  https://learn.microsoft.com/en-us/windows/win32/shell/how-to-customize-folders-with-desktop-ini
  [VERIFICADO EM FONTE]

## 3. Portabilidade no Windows
- `~/.claude` = `%USERPROFILE%\.claude`; `CLAUDE_CONFIG_DIR` move tudo; `~/.claude.json` (OAuth, estado) não
  se sincroniza. [VERIFICADO EM FONTE]
- Caminho recomendado pelo subagente, 2 camadas (inferência; a doc reserva plugin para "instalar em vários
  projetos", https://code.claude.com/docs/en/plugins/overview) [INCERTO]: repo git para o que plugin não leva
  (CLAUDE.md pessoal, rules, settings.json) + plugin em marketplace git privado (skills, hooks, scripts).
- Plugin leva skills, agents, `hooks/hooks.json`, MCP, `bin/`, scripts. NÃO leva CLAUDE.md ("ponha em
  skill") nem rules; settings do plugin só `agent`/`subagentStatusLine`.
  https://code.claude.com/docs/en/plugins/manifest-reference [VERIFICADO EM FONTE]
- `/plugin marketplace add dono/repo`, URL `.git` ou pasta local ("no Windows `C:\` funciona", carrega no
  lugar, `/reload-plugins` sem subir versão). Privado usa as credenciais git da máquina, sem prompt (SSH sem
  passphrase, ou `gh auth login` + `gh auth setup-git`). Auto-update vem desligado: ligar em /plugin >
  Marketplaces ou `autoUpdate:true`; sem `version` acompanha o commit.
  https://code.claude.com/docs/en/plugins/host-marketplace · https://code.claude.com/docs/en/plugins/cli-reference
  [VERIFICADO EM FONTE]
- Máquina nova: `extraKnownMarketplaces` + `enabledPlugins` no settings.json de usuário, e ao abrir o Claude
  Code clona e baixa em segundo plano (precisa de git e credenciais). Terminal, VS Code e app local leem os
  mesmos settings. https://code.claude.com/docs/en/plugins/loading [VERIFICADO EM FONTE]
- Hooks de plugin no Windows: `${CLAUDE_PLUGIN_ROOT}` chega com `/`; forma-shell roda no Git Bash; use
  `args` ou `"shell":"powershell"`; `.sh` por caminho nu falha, use `bash "${CLAUDE_PLUGIN_ROOT}/x.sh"`
  (https://github.com/anthropics/claude-code/issues/95673, aberta). Hook igual em settings e plugin roda 2x.
  [VERIFICADO EM FONTE]
- Setup junção/hardlink: (a) Claude grava `.md` por temp+rename (evidência em macOS:
  https://dev.to/arthur_teb/claude-code-writes-md-files-atomically-and-that-silently-kills-live-preview-20en),
  então o hardlink do CLAUDE.md pode se separar; teste com `fsutil hardlink list` [INCERTO no Windows];
  (b) a retenção apagava a junção de `~/.claude/plans` (issue #92692, aberta); o changelog 2.1.280 corrigiu
  "cleanup deleting a directory symlink or junction", mas se cobre `plans` [INCERTO]; (c) o app Desktop não
  lista skills via junção no menu `/` (#68318, "not planned"); (d) `~/.claude/skills` como symlink (#38051)
  foi fechada como "completed" em 24/mar/2026; (e) `/rewind` pula symlink/hardlink
  (https://code.claude.com/docs/en/checkpointing). [VERIFICADO EM FONTE]
- Evite OneDrive (Edit/Write com erro, `.claude.json` corrompido: #65229, #29153); `C:\` raiz evita.
  [VERIFICADO EM FONTE]
- Dotfiles: chezmoi exige Developer Mode ou privilégio de symlink
  (https://www.chezmoi.io/user-guide/machines/windows/); o guia típico sincroniza CLAUDE.md, settings.json e
  skills/ e ignora projects/, sessions/, history.jsonl, cache/, debug/, sem tratar Windows
  (https://www.frxiaobei.com/en/posts/2026/04/chezmoi-claude-code/). Guia maduro Windows-nativo: não achado
  [INCERTO].

## 4. Skills/plugins existentes
- https://github.com/johnnydecimal/skills — oficial do Johnny.Decimal (`jdex`, usa o CLI `jd`; 14 estrelas);
  aproveitável se usar JD.
- smithjoshua (PARA + manifesto, nunca apaga; acima) e Composio `file-organizer` (bash find/mv; o README
  manda instalar em `~/.config/claude-code/skills/`, diferente do oficial `~/.claude/skills/`)
  https://github.com/ComposioHQ/awesome-claude-skills/tree/master/file-organizer
- https://github.com/barannikov07/scaffold-project — gera AGENTS.md "roteador" e docs (0 estrelas).
- `hook-auto-docs@dev-gom-plugins` — PostToolUse(Write)+Stop gera `.project-structure.md`, Node, 98 estrelas,
  último push jan/2026. https://github.com/Dev-GOM/claude-code-marketplace
- https://github.com/anthropics/skills (180k estrelas) não tem organização de pastas; skills.sh não é listável
  por fetch (use `npx skills find`). Ícone, desktop.ini, legenda: nenhum.
- Veredito: nenhum cobre Windows + marca IA/humano + legenda + ícone; escrever o próprio, pequeno, copiando
  os padrões acima. [VERIFICADO EM FONTE: ausência nas buscas]

## 5. Métodos pessoais
- JD, PARA (`0-Inbox`...`4-Archive`) e prefixos numéricos já são combinados com agentes (repos acima): humano
  define a estrutura, IA propõe e mantém `index.md`/JDex e `log.md`. [VERIFICADO EM FONTE]

## 6. Hooks — https://code.claude.com/docs/en/hooks
- Eventos (mais de 30): SessionStart, UserPromptSubmit, PreToolUse, PermissionRequest, PostToolUse,
  PostToolUseFailure, PostToolBatch, SubagentStart/Stop, Stop, InstructionsLoaded, ConfigChange, CwdChanged,
  FileChanged, Pre/PostCompact, SessionEnd e outros. [VERIFICADO EM FONTE]
- Entrada comum: `session_id`, `transcript_path`, `cwd`, `permission_mode`, `hook_event_name`.
  PostToolUse+Write: `tool_name:"Write"`, `tool_input:{file_path,content}`,
  `tool_response:{filePath,type:"create"}`, `tool_use_id`. Bash/PowerShell: `tool_input.command`
  (+description, timeout, run_in_background); `tool_response.bashEditDiff.changedFiles` (v2.1.269+, beta, só
  em repo git). Sem Git Bash só existe a ferramenta PowerShell: use matcher `Bash|PowerShell`. `file_path`
  chega absoluto, com `\`. [VERIFICADO EM FONTE]
- Hook em `~/.claude/settings.json` vale em todos os projetos; níveis somam; mesmos eventos em terminal, IDE e
  Desktop. [VERIFICADO EM FONTE]
- Timeout em segundos (padrão 600; SessionEnd 1,5 s, sobe até 60 s pelo `timeout` do hook); `async:true` não
  bloqueia. Falhar sem bloquear: só exit 2 bloqueia (em PostToolUse só mostra stderr ao Claude); exit 1,
  script ausente e timeout não bloqueiam; `echo` no profile do shell quebra JSON de saída. Use try/catch e
  `exit 0`. [VERIFICADO EM FONTE]
- Pasta/arquivo criado: Write cobre arquivo; `PostToolUse(Edit|Write)` não dispara quando Bash reescreve;
  `mkdir`/`New-Item` só via `tool_input.command`, `bashEditDiff` ou varredura no `Stop`. Exemplo pronto para
  pasta: não achado. Esboço do subagente, não testado [INCERTO]: matcher `Write|Bash|PowerShell`,
  `"shell":"powershell"`, `"async":true`, comando `& "$env:USERPROFILE\.claude\hooks\log-created.ps1"`; o
  script grava JSONL (ts, session_id, cwd, tool, file_path/command) se `type=="create"` ou o comando casar
  `mkdir|New-Item|md`, e termina em `exit 0`.
- Exemplos oficiais: log de comandos Bash e re-injeção de contexto após compactação (SessionStart `compact`,
  útil para a legenda) https://code.claude.com/docs/en/hooks-guide [VERIFICADO EM FONTE]

## O que vale a pena copiar
1. CLAUDE.md pessoal curto + rules/skills; detalhe em pasta própria.
2. Separar por pasta com manifesto: `_ORG/_MANIFEST.md` ou `index.md` + `log.md`; humano = fonte, IA = escreve.
3. Um hook global PostToolUse async (Write|Bash|PowerShell) gravando JSONL central; sempre `exit 0`; não
   confiar na marca da Anthropic.
4. Legenda curta no CLAUDE.md pessoal + `InfoTip` em desktop.ini nas pastas-raiz; reinjetar via
   SessionStart(compact).
5. Plugin privado (skills + hooks + scripts em Node/PowerShell) + `extraKnownMarketplaces`/`enabledPlugins`/
   `autoUpdate` no settings; CLAUDE.md pessoal por git/dotfiles.
6. Junção só em diretórios, hardlink testado com `fsutil`, Claude Code 2.1.280 ou mais novo, nada em OneDrive.
7. Reaproveitar padrões (skills de JD se usar JD) e escrever o restante.

## Complemento (04/10/2026, mesma janela)
- O hardlink do `CLAUDE.md` pessoal foi conferido com `fsutil hardlink list` antes e depois de uma gravação
  feita por script que reescreve o mesmo arquivo: os dois nomes (`C:\CLAUDE\CLAUDE.md` e
  `~\.claude\CLAUDE.md`) continuaram ligados, com o mesmo conteúdo.
