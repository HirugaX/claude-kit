# Claude Code na nuvem com repositório privado

- **Pergunta:** como trabalhar com o Claude Code na nuvem (claude.ai/code, celular, app do Windows,
  terminal) sobre repositórios privados do GitHub — inclusive dois repositórios lado a lado, um importando
  o outro —, o que vai e o que não vai para a nuvem, e como a nuvem conta no uso do plano e nos créditos.
- **Data:** 28/09/2026 (duas pesquisas) e 29/09/2026 (uma terceira, com a pergunta mais fechada).
- **Projeto que pediu:** DESOSP_APP (plano de trabalhar da nuvem e do celular).
- **Onde a decisão mora (resumo, não cópia):** `C:\DESOSP_APP\docs\GUIA_NUVEM_DESOSP.md`;
  `C:\DESOSP_APP\docs\HANDOFF_APP.md`, seção "Os fatos da nuvem — pesquisados na documentação oficial em
  28/09"; `C:\DESOSP_APP\docs\PROJETO_FLUXOS_DESOSP.md` §5.
- **Fontes (principais):**
  - https://code.claude.com/docs/en/claude-code-on-the-web
  - https://code.claude.com/docs/en/cloud-environments
  - https://code.claude.com/docs/en/web-quickstart · /mobile · /desktop · /remote-control · /data-usage · /costs
- **Conclusão:**
  - Repositório privado exige o Claude GitHub App instalado nele.
  - Uma sessão pode ter vários repositórios, mas aí **não lê** `.claude/settings.json`, ganchos nem
    `.mcp.json`. Onde ficam em disco não está documentado. O `--cloud` do terminal trabalha com um
    repositório por vez.
  - Repositório sem remoto no GitHub não vai para a nuvem; a saída é o **Remote Control** (a sessão roda
    na máquina e é guiada pelo celular ou navegador; MCP, ganchos e arquivos locais continuam valendo).
  - O CLAUDE.md do usuário, as skills do usuário, o `.env` e os MCPs locais não vão para a nuvem.
    Variável de ambiente não é segredo ("Anyone who uses the environment can read the values"); no
    Pro/Max, credencial de API fica fora da VM.
  - Nuvem divide a cota com todo o resto do plano; não há cobrança à parte de VM. "Usage credits" é o
    termo oficial para passar do limite; crédito promocional não aparece na documentação.
  - Comandos: `claude --cloud "tarefa"` (o `--remote` é apelido antigo), `claude --teleport [id]`,
    `claude -p "msg" --cloud <id>`; `claude remote-control` / `/remote-control`.
  - Ubuntu 24.04, 4 vCPU, 16 GB; script de setup é cacheado se terminar em ~5 min.
  - Retenção: 30 dias com treino desligado; 5 anos com treino ligado.
- **Conferir de novo depois de:** 04/11/2026 — a documentação da nuvem já mudou entre 28/09 e 04/10, e o
  `GUIA_NUVEM_DESOSP.md` diverge dela em alguns pontos. Rechecar os nomes de comandos antes de usar.
- **Como foi feita:** três subagentes `claude-code-guide`, só documentação oficial (12, 12 e 7 chamadas
  web). Abaixo, os três relatórios como voltaram, sem mudança de conteúdo. Eles divergem em detalhes (por
  exemplo, se o Windows tem limitação); vale o mais recente e, na dúvida, a página.

---

## Relatório 1 (28/09) — verificação de 14 afirmações

# Claude Code Web & Cloud Verification Report

## Summary
Verified 14 claims against official documentation from code.claude.com. **11 CONFIRMED, 0 CONTRADICTED, 3 NOT FOUND.**

## Verification Table

| # | Claim | Status | Source URL | Quote |
|---|-------|--------|------------|-------|
| 1 | Web at claude.ai/code; GitHub sign-in + app required; private repos need GitHub App | **CONFIRMED** | https://code.claude.com/docs/en/web-quickstart.md | "Visit claude.ai/code and sign in... Installing the Claude GitHub App on a repository also enables Auto-fix." |
| 2 | Cloud environments: network access (None/Trusted/Full/Custom), env vars, setup script, cached | **CONFIRMED** | https://code.claude.com/docs/en/cloud-environments.md | "The **Network access** field... takes one of four levels: None, Trusted, Full, Custom... When setup completes within roughly five minutes, Anthropic snapshots the filesystem and reuses that snapshot." |
| 3 | Multiple repos in session; .claude/settings.json, hooks, .mcp.json NOT loaded | **CONFIRMED** | https://code.claude.com/docs/en/cloud-environments.md | "Yes, in a session with one repository. A session with several repositories... starts above the clones and doesn't read them." |
| 4 | Mobile Code tab: pick repo, describe task, watch progress, open PR | **CONFIRMED** | https://code.claude.com/docs/en/mobile.md | "From the Code tab, select a repository and branch, describe the task, and submit it... Open a session in the app to check progress." |
| 5 | Windows Desktop: Cloud vs Local; Continue in → Terminal; teleport command | **CONFIRMED** | https://code.claude.com/docs/en/desktop-quickstart.md | "Select **Local** to run Claude on your machine... You can also select **Cloud**... Pull a cloud session into your terminal using `claude --teleport`" |
| 6 | Terminal: `claude --cloud`, `claude --teleport`, `claude -p ... --cloud <id>` | **CONFIRMED** | https://code.claude.com/docs/en/claude-code-on-the-web.md | "`claude --cloud "Fix the authentication bug..."` creates a new cloud session... `claude -p "your message" --cloud <session-id>` posts one message and exits" |
| 7 | Cloud session pushes branch; PR with "Create PR" button | **CONFIRMED** | https://code.claude.com/docs/en/web-quickstart.md | "When the diff looks right, select **Create PR** at the top of the diff view." |
| 8a | Cloud sessions count against subscription plan usage | **CONFIRMED** | https://code.claude.com/docs/en/claude-code-on-the-web.md | "Rate limits: cloud sessions share rate limits with all other Claude and Claude Code usage within your account." |
| 8b | Official documentation of credit promotion for cloud sessions | **NOT FOUND** | — | No page documenting promotional credits for Claude Code web/cloud. |
| 8c | How to view usage/consumption (settings, /usage command, etc.) | **PARTIALLY FOUND** | https://code.claude.com/docs/en/monitoring-usage.md | `/usage` command exists; analytics dashboard for Team/Enterprise; single unified method across plans not documented. |
| 9 | User ~/.claude/CLAUDE.md, .env, MCP servers NOT available in cloud | **CONFIRMED** | https://code.claude.com/docs/en/cloud-environments.md | "Your user ~/.claude/CLAUDE.md... No... Lives on your machine, not in the repo" (same for .env and user-scope MCP). |
| 10a | Data retention: 30 days standard (when training off) | **CONFIRMED** | https://code.claude.com/docs/en/data-usage.md | "Users who don't allow data use for model improvement: 30-day retention period." |
| 10b | Sandbox VM is Anthropic-hosted | **CONFIRMED** | https://code.claude.com/docs/en/data-usage.md | "Cloud sessions run in Anthropic-managed virtual machines by default instead of locally." |
| 11a | Remote Control: plan access (Pro/Max/Team/Enterprise) | **CONFIRMED** | https://code.claude.com/docs/en/remote-control.md | "Available on Pro, Max, Team, and Enterprise plans. API keys are not supported." |
| 11b | Remote Control: command syntax | **CONFIRMED** | https://code.claude.com/docs/en/remote-control.md | "`claude remote-control`, `claude --remote-control`, `/remote-control` documented. |
| 11c | Remote Control: GitHub required | **NOT REQUIRED** | https://code.claude.com/docs/en/remote-control.md | Remote Control is local-only; GitHub not needed. Works with MCP, filesystem, local tools. |
| 11d | Remote Control: counts against plan usage | **CONFIRMED** | https://code.claude.com/docs/en/data-usage.md | "Stored transcripts are retained under the Data usage policy." |
| 12 | Plan access: Pro/Max/Team/Enterprise for web and Remote Control | **CONFIRMED** | https://code.claude.com/docs/en/feature-availability.md | "Availability by subscription plan" table: Cloud sessions ✓ Pro/Max/Team/Enterprise; Remote Control ✓ Pro/Max/Team/Enterprise. |
| 13 | Windows native cloud/teleport flow; any documented limitations | **CONFIRMED (no limitations)** | https://code.claude.com/docs/en/desktop-quickstart.md | "Download for Windows: For x64 processors... For Windows ARM64, download the ARM64 installer..." Cloud and teleport work identically. |
| 14 | Two repositories side-by-side; clone second repo in setup script | **NOT FOUND** | — | No official guidance for this scenario. Multi-repo projects documented, but single setup-script clone method not described. |

## Key Facts for Users

### Credentials & Secrets
- **Pro/Max**: API credentials stored encrypted; never visible in session
- **Team/Enterprise**: API credentials not yet available
- **Setup script**: `.env` files excluded from bundled repos (macOS/Linux/WSL; not native Windows)

### Setup Script Performance
- Scripts >5 minutes won't cache; runs every session
- Use parallel installs: `cmd1 & cmd2 & wait`
- Bun has known proxy incompatibility; use npm/yarn

### Cloud Sessions - What's NOT Available
- User-scope plugins, skills, commands, MCP servers
- Interactive auth (AWS SSO)
- Transport/mTLS variables
- .claude/ configuration (hooks, settings, MCP) in multi-repo sessions

### Windows Notes
- Native Windows fully supports cloud + teleport (Desktop app or terminal)
- No x64 vs ARM64 feature differences
- "Continue in Terminal" works same as other platforms

### Remote Control Details
- Runs entirely on user's machine (no cloud)
- Requires Pro/Max/Team/Enterprise
- API key auth NOT supported (must use claude.ai account)
- Counts against plan rate limits
- No GitHub requirement

No promotional credits documented for cloud sessions. Users check account settings + monitoring-usage page for consumption tracking per plan type.

## Relatório 2 (28/09) — dois repositórios, celular, Windows, terminal (em português)

# Claude Code na Nuvem — Guia da Documentação Oficial (Português/BR)

## 1. Setup de Claude Code na Web: Conectar GitHub, App, Repositórios e Ambiente Cloud

### Conexão de GitHub
- **Dois métodos:**
  - **Browser:** Acessar `claude.ai/code` → "Sign in with GitHub" → autorizar Claude GitHub App → instalar Claude GitHub App em repositórios privados (necessário para acessá-los)
  - **Terminal via `/web-setup`:** Usar token `gh` local; executa `gh auth login` + `claude /web-setup` no CLI → envia token criptografado para conta Anthropic
- **Repositórios privados:** Requerem instalação do Claude GitHub App na organização/conta GitHub. Público funciona sem app instalado
- **URL oficial:** https://code.claude.com/docs/en/web-quickstart.md (seção "Connect GitHub")

### Cloud Environment (Ambiente Cloud)
- **O que é:** Configuração salva que controla acesso de rede, variáveis de ambiente e scripts de setup
- **Acesso à rede:** 4 níveis
  - **None:** Sem acesso (só Anthropic API, não bloqueado)
  - **Trusted** (padrão): Registros de pacotes (npm, PyPI, etc) + GitHub + cloud SDKs — veja lista completa em https://code.claude.com/docs/en/cloud-environments.md#default-allowed-domains
  - **Full:** Qualquer domínio
  - **Custom:** Sua própria lista de domínios permitidos
- **Variáveis de ambiente:** Formato `.env` (KEY=value); visíveis a quem usa o environment; qualquer sessão no environment copia os valores no startup; você pode editá-las depois (afeta sessões futuras, não as rodando)
- **Secrets/Credenciais API:** (Pro/Max apenas) Credenciais armazenadas fora da VM sandbox; proxy Anthropic anexa à requisição automaticamente; nunca entra na VM. Team/Enterprise não suporta ainda
- **Setup script:** Bash que roda antes de Claude começar (como root em Ubuntu 24.04); deve terminar em ~5 min para ser cacheado; deve fazer `exit 0`; pacotes instalados carregam em sessões futuras via cache de filesystem
- **URL oficial:** https://code.claude.com/docs/en/cloud-environments.md

---

## 2. Uma Sessão Cloud Pode Trabalhar com DOIS Repositórios?

**SIM, mas com limitações:**
- **Como:** Uma sessão cloud pode clonar múltiplos repositórios (documentação diz "You can add multiple repositories to work across them in one session")
- **Na prática:** Usar Projects (uma conversa que coordena múltiplas threads cloud em paralelo) ou, numa sessão única, adicionar repos ao seletor de repositório antes de submeter
- **LIMITAÇÃO CRÍTICA:** 
  - Sessions com múltiplos repos NÃO lêem `.claude/settings.json`, hooks (SessionStart) ou `.mcp.json` de nenhum repositório
  - Se a app repo precisa importar de segundo repo local (como seu caso): **não está documentado como suportar dois repos locais não-GitHub num setup automático**
  - **Workaround documentado:** Setup script pode clonar um segundo repo via git, mas requer credenciais passadas via environment variables (inseguro) ou SSH key copiada para environment (complexo)
  - **Alternativa:** Se o segundo repo está no GitHub, instalar Claude GitHub App nele, depois usar Projects ou `--cloud` com múltiplos repos no seletor

**Não encontrado na documentação:** Como uma sessão cloud obtém acesso a dois repositórios locais (não-GitHub) do mesmo usuário numa única sessão. A documentação assume repositórios GitHub ou um bundle local único.

**URL:** https://code.claude.com/docs/en/web-quickstart.md (seção "Start a task"); https://code.claude.com/docs/en/cloud-environments.md (limitações SessionStart)

---

## 3. Como Iniciar, Monitorar e Continuar Sessões Cloud de Diferentes Superfícies

### (a) Aplicativo Mobile Claude (iOS/Android)
- **Disponível:** Sim, Claude Code está na aba **Code** do app Claude (não é app separado)
- **O que fazer:**
  - Baixar Claude app para [iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) ou [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude)
  - Entrar com conta claude.ai
  - Tap **Code** → selecionar repositório e branch → descrever task → submit
  - App monitora progresso, permite deixar comentários inline, criar PR
  - Pusha notificações quando precisa de decisão (Remote Control) ou task termina
- **Limitações:**
  - Não pode executar comandos terminal-only (`/plugin`, `/resume`)
  - Permission modes: só Accept edits, Plan, Auto (não Manual/Bypass)
- **URL:** https://code.claude.com/docs/en/mobile.md

### (b) Desktop App Claude (Windows)
- **Como iniciar cloud session:** Dentro app → selecionar **Cloud** (ao invés de Local) no prompt → selecionar repo/branch → submeter task
- **Como monitorar:** Sessão roda em background; tab do app mostra progresso; notificações mobile (se Remote Control ativado)
- **Comandos específicos:** Nenhum CLI flag necessário (uso é visual)
- **Como trazer para terminal:** Menu "Continue in" → Terminal → copiar comando `claude --teleport <session-id>`
- **URL:** https://code.claude.com/docs/en/desktop.md

### (c) VS Code Extension + CLI (Terminal)
- **Iniciar cloud session:**
  ```bash
  claude --cloud "Descrição da task"
  ```
  CLI clona repositório do git remote (não do checkout local), roda setup script, Claude trabalha
  
- **De terminal, monitorar session que roda na nuvem:** `--cloud` cria sessão mas você continua no terminal; para interagir abra claude.ai/code ou mobile app
  
- **Teleportar cloud session de volta para terminal:**
  ```bash
  claude --teleport                    # picker interativo
  claude --teleport <session-id>       # ID específico
  # ou dentro de sessão CLI:
  /teleport
  /tp
  ```
  Requisitos: repo correto, branch pushed, clean git state, mesma conta Anthropic
  
- **Enviar follow-up para session cloud rodando:** (de qualquer máquina)
  ```bash
  claude -p "sua mensagem" --cloud <session-id>
  ```
  
- **Comandos deprecated:** `--remote` (alias antigo para `--cloud`); não confundir com `--remote-control` (diferentes)

- **URL:** 
  - https://code.claude.com/docs/en/claude-code-on-the-web.md (seções "From terminal to cloud", "From cloud to terminal", "Send follow-ups from the CLI")
  - https://code.claude.com/docs/en/quickstart.md

---

## 4. Como Cloud Sessions Entregam Mudanças (Branches, PRs, Auto-push)

- **Push automático:** Claude faz push de sua branch assim que atinge um ponto de parada. Usa GitHub proxy que mantém credenciais fora da VM
- **Criar PR:** Dentro claude.ai/code → abrir diff → botão "Create PR" → opções:
  - Full PR (pronto)
  - Draft
  - Ir para GitHub compose page com título/descrição gerada
- **Continuar depois de PR criado:** Sessão fica aberta; você pode mandar mais mensagens, Claude responde
- **Auto-fix PRs:** Se Claude GitHub App instalado, ativar auto-fix na session para Claude responder automaticamente a CI failures e review comments
  - URL: https://code.claude.com/docs/en/claude-code-on-the-web.md#auto-fix-pull-requests
- **Puxar mudanças localmente:** 
  - Branch é pushado no GitHub; `git fetch` + `git checkout` localmente
  - Ou: teleportar session (`claude --teleport <id>`) → branch é fetched e checkouted automaticamente

**URL:** https://code.claude.com/docs/en/web-quickstart.md (seção "Review and iterate")

---

## 5. Uso, Billing e Créditos Promocionais

### Contagem contra Limits de Plano
- **Cloud sessions contam como uso normal:** mesmos limits de prompt/tokens que chat ou local Claude Code
- **Rate limits compartilhados:** Com todo uso Claude (chat + Claude Code local + cloud)
- **5-hour session limits:** Doubled em May 6, 2026 (permanente). Weekly caps têm 25% boost desde Sept 14, 2026
- **Sem cobrança separada de VM:** Billing é por tokens (mesmos rates do modelo usado: Sonnet 5 = $2 input / $10 output per million tokens)

### Créditos Promocionais
- **NENHUMA informação oficial encontrada na documentação** sobre promoção específica de créditos para cloud sessions
- Documentação oficial (https://platform.claude.com/docs/en/about-claude/pricing) não menciona promoção
- Recomendação: Verificar em https://claude.com/pricing ou dentro da conta claude.ai/settings

### Ver Consumo
- **Na conta:** claude.ai → Settings → Billings/Usage (exato conteúdo não detalhado em docs públicas)
- **CLI:** Nenhum comando CLI oficial listado para ver consumo em tempo real

**URL não encontrada na documentação:** Detalhes de como ver exatamente tokens consumidos em cloud vs local

---

## 6. Limitações do Ambiente Cloud

### SO e Ferramentas Pré-instaladas (Anthropic-hosted)
- **SO:** Ubuntu 24.04, x86_64
- **Python:** Python 3.x com pip, poetry, uv, black, mypy, pytest, ruff
- **Node.js:** 20, 21, 22 com npm, yarn, pnpm, eslint, prettier, chromedriver
- **Ruby:** 3.1, 3.2, 3.3 com gem, bundler, rbenv
- **PHP:** 8.3 com Composer
- **Java:** OpenJDK 21 com Maven/Gradle
- **Go, Rust, C/C++, Docker, Databases:** Sim (PostgreSQL 16, Redis 7.0)
- **Utilities:** git, gh, jq, yq, ripgrep, tmux, vim, nano

### Instalação de Dependências
- **requirements.txt / pyproject.toml:** Sim, via setup script ou SessionStart hook
- **pip install:** Requer network access **Trusted** ou **Full** (padrão funciona)
- **pip install from local file (not in repo):** Não documentado (arquivo local não clonado)

### MCP Servers em Cloud Sessions
- **Disponibilidade:** MCP servers configurados em `.mcp.json` (repo scope) **são carregados numa sessão com um repo único**
- **Com múltiplos repos:** Não carregam (mesmo problema que hooks)
- **MCP connectors (claude.ai/customize/connectors):** Carregam automaticamente
- **Usar MCP tool que não está no default:** Precisa adicionar domínio ao network allowed domains
- **Obs:** Traffic de MCP connector passa por Anthropic, não pelo allowlist da VM
- **URL:** https://code.claude.com/docs/en/mcp.md

### Recursos de VM
- 4 vCPUs
- 16 GB RAM
- 30 GB disk

### Time Limits
- **Bash commands:** Padrão 2 min, máximo 10 min solicitado; timeout customizável via `BASH_DEFAULT_TIMEOUT_MS`
- **SessionStart hooks:** Default 600s (10min), customizável com `timeout` field
- **Setup script:** ~5 min para ser cacheado
- **Session idle:** Expira após inatividade; reabrir em claude.ai/code para provisionar VM nova com histórico restaurado

### Arquivo fora do Repo
- **User CLAUDE.md (~/.claude/CLAUDE.md):** NÃO carregado em cloud
- **User skills (~/.claude/skills/):** NÃO carregado; commit para repo `.claude/skills/`
- **Credenciais .env local:** NÃO carregado; use environment variables no cloud environment
- **MCP servers locais (~~.claude.json):** NÃO carregados; commit `.mcp.json` ao repo

### Limitações Windows-Specific
- **Não há limitações listadas:** Cloud sessions rodram em Linux Ubuntu, agnóstico a SO do cliente
- **De Windows:** Usar `claude --cloud` normalmente (CLI é cross-platform)

**URL:** https://code.claude.com/docs/en/cloud-environments.md (seções "What carries over from your setup", "Installed tools", "Resource limits", "Time limits")

---

## 7. Dados e Privacidade em Cloud Sessions

### Onde Dados Rodam
- **Anthropic-hosted (padrão):** VMs gerenciadas por Anthropic; repositório cloneado no VM isolado
- **Self-hosted environments:** Sua infraestrutura (equipes Enterprise)

### Retenção e Armazenamento
- **Pro/Max permitindo uso para treinamento:** 5 anos
- **Pro/Max bloqueando uso para treinamento:** 30 dias
- **Team/Enterprise:** 30 dias (padrão); Zero Data Retention disponível para qualified accounts
- **Transcript armazenado:** Servidores Anthropic (você volta à session depois)
- **Código da repo:** Clonado em VM isolado; sujeito a retenção

### Credenciais e Segurança
- **GitHub credentials:** Criptografadas em servidores Anthropic; nunca entram VM; proxy GitHub autentica on behalf
- **API credentials (Pro/Max):** Fora da VM; proxy Anthropic anexa à requisição
- **Traço de saída (/feedback):** Retém por 5 anos

### Transmissão
- **TLS 1.2+** em trânsito
- **Disco Anthropic:** AES-256
- **Proxy de segurança:** Todo tráfego egresso passa por proxy Anthropic (auditoria, rate limiting, content filtering)

### O Que NÃO Vai para Nuvem
- **Seu código executado:** Roda VM; code changes e output seguem retenção acima
- **Seus arquivos locais:** Não clonados (repo only); attachments do mobile app baixam e salvam em `~/.claude/uploads/` (local)

**URL:** https://code.claude.com/docs/en/data-usage.md; https://code.claude.com/docs/en/claude-code-on-the-web.md#security-and-isolation

---

## Resumo: Setup Recomendado para Seu Caso

Seu projeto: app (FastAPI + SQLite) em um repo que **importa de um segundo repo local**.

**Cenário 1: Ambos repos no GitHub**
1. Instalar Claude GitHub App nos dois repos (organization ou personal)
2. `claude /web-setup` (ou browser onboarding)
3. Iniciar cloud session com `claude --cloud` e selecionar ambos repos no seletor
4. **Limitação:** Hooks e MCP não carregam (múltiplos repos)
5. Se setup complexo, colocar em setup script do environment cloud

**Cenário 2: App público, segundo repo privado local (não-GitHub)**
- **Não documentado** como suportar automaticamente
- **Workaround:** 
  - Setup script que clona segundo repo (requer credenciais no env var — não ideal)
  - Ou: Push segundo repo para GitHub + Cenário 1
  - Ou: Usar bundle local (`CCR_FORCE_BUNDLE=1 claude --cloud`) — mas não pode fazer push de volta

**Cenário 3: Trabalho intensivo de local com steering remoto**
- Usar **Remote Control** (`claude remote-control` ou `/remote-control`) + mobile app/browser
- Ambiente é seu, MCP/hooks/configs locais carregam, você pode fazer `from second_repo import ...`
- URL: https://code.claude.com/docs/en/remote-control.md

---

## URLs da Documentação Oficial (Resumo)

1. **Web quickstart:** https://code.claude.com/docs/en/web-quickstart.md
2. **Cloud environments:** https://code.claude.com/docs/en/cloud-environments.md
3. **Claude Code na web (reference completo):** https://code.claude.com/docs/en/claude-code-on-the-web.md
4. **Mobile:** https://code.claude.com/docs/en/mobile.md
5. **Remote Control:** https://code.claude.com/docs/en/remote-control.md
6. **Data usage & privacy:** https://code.claude.com/docs/en/data-usage.md
7. **MCP:** https://code.claude.com/docs/en/mcp.md
8. **Pricing (Anthropic):** https://platform.claude.com/docs/en/about-claude/pricing
9. **Mapa completo de docs:** https://code.claude.com/docs/en/claude_code_docs_map.md

---

**Nota:** Documentação reflete estado de 28 de setembro de 2026. Para atualizações recentes (promoções, novos features), verificar claude.com/pricing e status.claude.com.

## Relatório 3 (29/09) — repetição com a pergunta mais fechada

# Claude Code Cloud Sessions Research — Official Documentation

## 1. Setup Steps: GitHub Connection & App Installation
**Source:** https://code.claude.com/docs/en/web-quickstart.md

**Steps:**
- **Visit claude.ai/code** and sign in with claude.ai account
- **Sign in with GitHub** — GitHub authorization page opens; approve authorization request
- **Install Claude GitHub App** at https://github.com/apps/claude/installations/new on each GitHub account/org whose private repos you want to use
  - "With this connection, a session can clone any public repository, but can work in a private repository only when the Claude GitHub App is installed on it"
  - Alternative: run `/web-setup` in CLI (requires `gh` CLI authenticated)
- **Set up Default environment** — network access level **Trusted** is pre-configured (no additional settings needed for basic use)

**Exact Setting Names:** The docs refer to these as **Quick web setup** (organization toggle at `claude.ai/admin-settings/claude-code`) and **Default environment** (no special naming beyond this).

**Not documented:** explicit settings panel names in claude.ai UI beyond "Admin settings > Claude Code" and "Admin settings > Connectors."

---

## 2. Multiple Repositories in One Cloud Session
**Source:** https://code.claude.com/docs/en/claude-code-on-the-web.md

**Can one session include multiple repositories?**
- "You can add multiple repositories to work across them in one session" (brief mention; no detailed workflow documented)
- At claude.ai/code: "Click the repository selector below the input box and choose a repository for Claude Code to work in. Each repository shows a branch selector."
- From CLI: "`--cloud` works with a single repository at a time" — you must start separate sessions for multiple repos

**Branch selection:** via repository selector UI dropdown at claude.ai/code; separate branch picker for each repo

**Disk paths:** **Not documented** — the docs do not specify how or where repositories are placed on disk in cloud sessions

**Private repos:** Claude GitHub App must be installed on each private repository; `/web-setup` method accesses any repo your `gh` token can reach

---

## 3. Cloud Environments Configuration
**Source:** https://code.claude.com/docs/en/cloud-environments.md

**Network Access Levels:**
- **None** — no outbound network access
- **Trusted** — allowlisted domains only (default); includes package registries, GitHub, cloud SDKs
- **Full** — any domain
- **Custom** — user-defined allowlist

**Environment Variables:**
- Format: `.env` syntax, one `KEY=value` per line
- **Are they secret?** No — "Anyone who uses the environment can read the values."
- **Recommendation:** "On Pro and Max plans, use an [API credential](https://code.claude.com/docs/en/cloud-environments.md#add-api-credentials) instead for a key the agent proxy can attach to a request"
- Not passed to `OTEL_*` variables (reserved for Claude Code telemetry)

**Setup Script:**
- Bash script runs **before Claude Code launches**, on fresh session startup only
- **When runs:** before every new session; skipped when [cached environment](#environment-caching) exists
- **Time limit:** roughly 5 minutes; if script exceeds ~5 min, the environment **isn't cached**
- **Caching behavior:** filesystem snapshot reused for subsequent sessions; keeps installed packages, Docker images, written files; does not keep running processes
- **Cache expiry:** roughly 7 days; also rebuilds when you change the setup script or network access

**OS/Image and Python:**
- **OS:** Ubuntu 24.04 x86_64
- **Python:** "Python 3.x with pip, poetry, uv, black, mypy, pytest, ruff" (pre-installed; exact minor version **not documented**)
- Also pre-installed: Node.js 20/21/22 (22 default), Ruby 3.1/3.2/3.3, PHP 8.3, Java OpenJDK 21, Go, Rust, C/C++, Docker, PostgreSQL 16, Redis 7.0, git, gh, jq, yq, ripgrep, tmux, vim, nano

---

## 4. Branch Pushing, PR Creation, Teleporting Back Local
**Source:** https://code.claude.com/docs/en/claude-code-on-the-web.md

**Branch naming:**
- Not fixed to a pattern like `claude/...` — docs state "when Claude reaches a stopping point, it pushes its branch to GitHub" without specifying naming
- PR bodies include session URL; commit messages include `Claude-Session: <url>` trailer (can disable with [`attribution.sessionUrl: false`](https://code.claude.com/docs/en/settings-reference#attribution-sessionurl))

**PR creation:**
- From diff view at claude.ai/code: select **Create PR**; options for full PR, draft, or jump to GitHub's compose page

**Bringing work back local:**
- **`claude --teleport <session-id>`** — pulls cloud session into your terminal
- **`claude --teleport`** (interactive) — opens session picker
- **`/teleport`** (from within existing CLI session) — opens picker without restarting
- **From claude.ai/code:** select **Open in > Terminal** to copy exact command
- Session must have pushed branch; teleport checks: clean git state, correct repository, branch available on remote, same account

---

## 5. Terminal Commands for Cloud Sessions
**Source:** https://code.claude.com/docs/en/claude-code-on-the-web.md

**Create cloud session:**
```bash
claude --cloud "Fix the authentication bug in src/auth/login.ts"
```

**Send follow-up message to running session:**
```bash
claude -p "your message" --cloud <session-id>
# or
echo "your message" | claude -p --cloud <session-id>
```
- Session-id can be bare ID (e.g., `session_...` or `cse_...`) or full URL

**Deprecated alias:**
- `--remote` is a deprecated alias for `--cloud`

**NOT `--remote-control`:** the docs explicitly state "`--cloud` creates cloud sessions. `--remote-control` is unrelated: it lets you monitor and steer a local CLI session from claude.ai or the Claude app."

---

## 6. Mobile & Desktop App: Starting Cloud Sessions
**Source:** https://code.claude.com/docs/en/mobile.md

**iOS/Android Code Tab:**
- Install Claude app for [iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) or [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude)
- Sign in with same claude.ai account
- Tap **Code** tab in app navigation
- Select repository, branch, permission mode (Accept edits / Plan / Auto), describe task, submit
- Sessions persist: task started on laptop is ready to review from phone

**Desktop App (Windows/Mac/Linux):**
- Select **Cloud** instead of **Local** when starting a session
- Choose environment, repository, branch, permission mode
- Submit task
- (Exact UI location not detailed in fetched docs, but documented as available)

---

## 7. Usage & Credits: Cloud Sessions Share Plan Limits
**Source:** https://code.claude.com/docs/en/costs.md

**Do cloud sessions share plan limits?**
- **Yes.** "Cloud sessions share rate limits with all other Claude and Claude Code usage within your account. Running multiple tasks in parallel consumes more rate limits proportionately. There is no separate compute charge for the cloud VM."

**Official terminology on "extra usage" / "credits":**
- **"Usage credits"** (official term): separate token bucket that depletes when you exceed your plan's base allowance
  - Available on Pro, Max, Team, and Enterprise plans
  - Turned on/off with `/usage-credits` command
  - "Usage credits let you keep working past your plan's usage limit"
- **No mention of "promotional credits"** in official docs
- **Where to see balance:** `/usage` command shows "Usage-credits" row with spend and limit; also at [claude.ai/settings/usage](https://claude.ai/settings/usage) (**Settings > Usage > Usage credits** section)

**Quote on limits:**
- Pro/Max: "your spend for the current month, measured against your monthly spend limit when you have set one. When you haven't set a limit, the row shows `Unlimited` and no spend figure"
- Team/Enterprise: "your own spend for the current month, measured against any limit your organization set that applies to you"

---

## 8. Remote Control: Command & Requirements
**Source:** https://code.claude.com/docs/en/remote-control.md

**Command (server mode):**
```bash
claude remote-control
```

**Command (interactive session with Remote Control enabled):**
```bash
claude --remote-control
# or
claude --rc
# optionally with name:
claude --remote-control "My Project"
```

**Command (from existing session):**
```
/remote-control
# or
/rc
# optionally with name:
/remote-control My Project
```

**Requirements:**
- **Subscription:** Pro, Max, Team, or Enterprise plan (API keys not supported)
- **Sign-in:** run `claude` + `/login` via claude.ai (not API key)
- **Organization policy (Team/Enterprise only):** Owner must enable Remote Control toggle at [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code)
- **Not available with:** Amazon Bedrock, Google Cloud Agent Platform, Microsoft Foundry, or custom `ANTHROPIC_BASE_URL` (unless Anthropic API)
- **Workspace trust:** first run asks "Trust this directory?" — answer `y` to save (except home directory, which asks every time)

**What it does:**
- Runs Claude Code locally on your machine
- Connects claude.ai/code and Claude mobile app to your local session
- Entire conversation, MCP servers, tools, project config stay available remotely
- Code execution and filesystem stay on your machine
- Session persists if laptop sleeps; reconnects automatically

---

## Summary: What Is and Isn't Documented

✅ **Documented clearly:**
- GitHub setup, app installation, basic cloud session workflow
- Environment variables, network access, setup script caching behavior
- Ubuntu 24.04 OS, pre-installed toolchains, Python 3.x
- Cloud sessions share plan rate limits, usage credits system
- `claude --cloud`, `--teleport`, `/teleport`, remote-control commands
- Mobile and Desktop app cloud session access
- Remote Control command syntax and requirements

❌ **Not documented or vague:**
- Exact disk paths where cloud session repositories are stored
- Fixed branch naming pattern (if one exists)
- Exact Python 3.x version (documented as "3.x" only)
- Detailed UI panel names in claude.ai settings beyond "Admin settings > Claude Code"
- How multiple-repository sessions choose which repo to work on (single mention; no workflow detail)
