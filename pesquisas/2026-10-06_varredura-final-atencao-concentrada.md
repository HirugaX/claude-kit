# Varredura final de recursos para a atenção concentrada (06/10/2026)

- **A pergunta:** que recursos servem a cinco necessidades do fluxo novo — nativos do Claude Code primeiro; depois skills,
  plugins e ferramentas de terceiros? (1) execução longa sem supervisão e sem parar à toa; (2) perguntas juntadas num só
  momento; (3) várias sessões em paralelo no mesmo PC Windows; (4) aviso no celular quando uma fase precisa dele ou
  termina; (5) observabilidade de tokens e de interação. Para cada candidato: o que faz, custo, risco, se roda no Windows
  nativo (e se exige WSL, tmux ou Mac) e veredito.
- **A data:** 06/10/2026 (Claude Code 2.1.291 neste notebook; o changelog já tem a 2.1.292, de hoje; estrelas e datas pela
  API do GitHub e pelas páginas do dia).
- **O projeto que pediu:** claude-kit (R1).
- **Conferir de novo depois de:** 06/11/2026 (agent view, Remote Control, Projects e mods são prévia; várias issues citadas
  estão abertas). Preços e limites de ntfy e Pushover: 06/01/2027.
- **Método:** documentação oficial lida em code.claude.com (páginas `.md` e `llms-full.txt`); `npx skills find` (só busca);
  READMEs e API do GitHub; issues de `anthropics/claude-code`. Nada instalado. Leituras locais: `claude --version`,
  `Get-Command`, `wsl -l -v`, `powercfg` e o `~\.claude\settings.json` do usuário (nunca transcritos). Marcas: [A] =
  afirmação do autor sem medição independente; [I] = inferência minha, não testada; [não achado] = a fonte não diz.
- **Neste notebook (Dell Latitude 3550, Windows 11 Home):** WSL não instalado (`wsl -l -v` falha); sem Bun, Docker, jq, uv,
  tmux, gh; com Git for Windows (Git Bash), Node 24.19, Python 3.12 e winget. O desktop dele: não verifiquei. Nenhum
  veredito AGORA ou QUANDO abaixo exige WSL.

## Conclusão em poucas linhas

1. **O nativo cobre quase tudo. Faltam três coisas:** uma fila de perguntas durante a execução (só com gancho próprio), um
   arquivo local de métricas (o OpenTelemetry exporta só por OTLP, Prometheus ou console; pedido aberto: [#97908][i-97908])
   e o aviso no celular fora do Remote Control.
2. **Execução longa.** O modo auto já é o padrão desde a 2.1.283 ([permission-modes][d-perm]). A espera automática do limite
   de uso já vem ligada, mas só em sessão interativa: não existe em `--bg` nem em `-p`, e com várias janelas só uma retoma
   ([interactive-mode][d-inter]; [#92004][i-92004]). O que mais para à toa é o pedido de permissão que ninguém vê: uma noite
   inteira parada, Windows 11, subagente em segundo plano, o pai sem aviso ([#99887][i-99887]). Antídotos documentados:
   gancho `PermissionRequest` que nega e registra em vez de esperar ([hooks][d-hooks-perm]), permissões pré-aprovadas, PC
   acordado.
3. **Perguntas.** Antes da execução, o `grilling` instalado já pergunta a fronteira inteira por rodada (arquivo do kit).
   Durante a execução, a fila nativa é o painel `claude agents`: grupo "Needs input" e resposta pela espiada
   ([agent-view][d-av-peek]). Para sessão que ele larga: `askUserQuestionTimeout` (só interativa) ou um gancho `PreToolUse`
   em `AskUserQuestion` que grava a pergunta e responde "adiada" ([hooks][d-hooks-ask]).
4. **Paralelo.** O nativo basta no Windows: abas do VS Code com ponto de status, `claude -w`, `claude agents`, app Desktop.
   As ferramentas de terceiros pedem tmux ou WSL, estão encerradas, ou são novas (herdr). Nenhuma entra agora. O teto de 3
   janelas da biblioteca de 04/10 pesa mais: cada sessão gasta a cota "N vezes mais rápido" ([agent-view][d-av-lim]).
5. **Celular.** Nativo = `PushNotification` + Remote Control. O `agentPushNotifEnabled` já está `true` no
   `~\.claude\settings.json` dele, mas só chega com o Remote Control conectado, e então o transcrito fica nos servidores da
   Anthropic ([remote-control][d-rc-sec]). Para o que não pode usar o Remote Control (`desosp-`): gancho `Notification` e
   `Stop` com texto fixo, para toast local ou ntfy. Para `--bg` falta um poller de `claude agents --json`, porque os eventos
   `agent_needs_input` e `agent_completed` só disparam com o painel aberto ([hooks][d-hooks-notif]).
6. **Tokens e interação.** O OTel tem `token.usage`, `cost.usage` e `active_time` (tipo `user` = teclado, `cli` = ferramenta e
   resposta). O texto do prompt só sai com `OTEL_LOG_USER_PROMPTS=1` (desligado por padrão); `user.email` sai sempre
   ([monitoring][d-otel]). No dia a dia bastam `/usage` (atribuição por skill, subagente, plugin e MCP; alerta "highly parallel
   sessions"), a statusline (`rate_limits`, `cost`) e o `session-report` (instalado). O ccusage lê os transcritos locais.
7. **Windows.** O `--bg` tem bugs abertos específicos do Windows ([#77754][i-77754], [#87812][i-87812], [#97273][i-97273]):
   fazer o teste de cinco minutos (no fim) antes de depender dele.
8. **Vereditos.** AGORA: ganchos `PermissionRequest`, `PreToolUse(AskUserQuestion)` e `Notification`/`Stop` com texto fixo;
   poller de `claude agents --json`; ntfy e toast como destinos; `/usage`, statusline e `session-report`; PC acordado;
   teste do `--bg`. QUANDO: `/goal`, `/loop` e `Monitor`, tarefas do Desktop, rotinas na nuvem (sem dado de paciente),
   `PushNotification` com Remote Control (fora dos `desosp-`), OTel (só métricas), ccusage, otel-tui,
   `askUserQuestionTimeout`, mensagens entre sessões, herdr, app Desktop, Projects, mods. NÃO: claude-squad, ccmanager,
   Nimbalyst, Vibe Kanban, Worktrunk, Channels, agent-notifications, BurntToast, Happy e parecidos, Pushover, Usage
   Monitor, claude-code-otel, hooks-observability, pacote ECC, agent-pulse, loop-me, batch-grill-me, ralph-loop.

## O que a biblioteca já tinha (não refeito) e o que é novo

**Já tinha:** não existe `/clear` programático e o encadeamento é `claude --bg` + gancho
([continuar-em-contexto-limpo][b-1006a]); `Notification` com `agent_completed` e `agent_needs_input`, `Stop` que bloqueia
até 8 vezes, `--bg` em prévia ([sessoes-memoria-plugins][b-1005]); teto de 3 janelas, 2 trabalhadoras + 1 integradora, e a
lista claude-squad, ccmanager, Crystal, Vibe Kanban, Conductor, Sculptor, container-use, ccusage e Usage Monitor
([janelas-paralelas][b-1004]); OMC, claude-mem, Headroom, Cartographer, o SDD e a regra do Workflow
([ferramentas-pedidas][b-1006b]); Remote Control + `--bg` [não achado] ([marketplace-local][b-1006c]); Remote Control,
`--cloud`, créditos e retenção ([nuvem][b-0928]).

**Novo nesta varredura:**

- os eventos `agent_*` só disparam com `claude agents` aberto; `claude agents --json --all` é a leitura suportada de fora;
- `askUserQuestionTimeout` e o `PreToolUse` que responde `AskUserQuestion` via `updatedInput.answers`;
- a espera do limite de uso (`autoContinueAtUsageLimit`) não existe em `--bg`; e o aviso `quota_auto_resume_*`;
- `PushNotification`: entrada, saída e as duas chaves de configuração; o transcrito do Remote Control vai à Anthropic;
- `--bg` comita e dá push da própria branch por padrão (nunca `main`), a menos que o CLAUDE.md diga o contrário;
- OTel: lista exata de métricas e eventos, o que leva texto, o que desliga, e o fato de não haver exportador de arquivo;
- `/usage` com atribuição e alertas; `/insights`; statusline com `rate_limits` e `prompt_cache`;
- as issues abertas que atingem o Windows e as noites sem supervisão (seção própria);
- `to-questionnaire` já está instalada; `batch-grill-me` aparece no skills.sh mas não está no repositório do Matt hoje; `loop-me` é novo (em-progresso);
- herdr (multiplexador com suporte nativo ao Windows) e o fim do BurntToast.

## Candidatos, necessidade, custo, risco, Windows, veredito e fonte

Necessidades: 1 execução longa; 2 perguntas em fila; 3 paralelo; 4 aviso no celular; 5 tokens e interação.

| candidato (o que faz) | nec. | custo | risco | Windows | veredito | fonte |
| --- | --- | --- | --- | --- | --- | --- |
| **Modo auto** (padrão no terminal e no VS Code desde a 2.1.283; um classificador revisa cada ação) + `permissions.allow` | 1 | grátis: a checagem roda no servidor, sem cobrança em Pro e Max | volta a perguntar após 3 bloqueios seguidos ou 20 no total (fixos); nenhum modo aprova `AskUserQuestion`; a lista de permissões dele guarda caminhos de scratchpad de sessões velhas (provavelmente inúteis [I]); `/fewer-permission-prompts` lê transcritos: não usar onde há dado de paciente [I] | padrão no Windows nativo desde a 2.1.233; sem sandbox no Windows | AGORA (já é o padrão; falta pré-aprovar o que ele barra) | [perm-modes][d-perm], [classifier][d-classif], [PowerShell][d-tools-ps] |
| **Gancho `PermissionRequest` em modo sem supervisão** (nega com `message` e registra, em vez de esperar) | 1 | script local; 0 token | não testado; negar faz o Claude contornar; sem decisão do gancho o prompt segue normal | sim (Python, ou `shell: powershell`) | AGORA, só nas execuções largadas, junto do portão Stop | [hooks][d-hooks-perm], [#99887][i-99887] |
| **Espera automática do limite de uso** (`autoContinueAtUsageLimit`, padrão ligado; avisos `quota_auto_resume_*`; no app Desktop, caixa "Auto-continue when limits reset") | 1 | grátis | só em sessão interativa com login claude.ai; não é oferecida em `--bg` nem `-p` (o que o `--bg` faz ao bater o limite: não achei); refaz no máximo 2 vezes seguidas; com várias janelas só uma retoma ([#92004][i-92004], app macOS); PC dormindo mais de 30 min pede Enter; Fable em `--bg`: o pedido de créditos não chega e o turno termina | sim, desde a 2.1.234 | AGORA (já liga sozinha; conferir em `/config`) | [interactive-mode][d-inter], [hooks][d-hooks-notif], [errors][d-errors] |
| **`/goal`** (condição de término; um modelo pequeno confere a cada turno) | 1 | tokens do avaliador, desprezíveis (doc) | vê só o que está na conversa; para após turnos sem ferramenta; some em erro que só ele resolve (login, crédito esgotado, contexto estourado, modelo indisponível); pausa em limite de uso; check-ins de 30 min, 1 h, 2 h; changelog 2.1.290 a 2.1.292 não mexe nele | sim | QUANDO (já decidido): fase com fim verificável | [goal][d-goal], [changelog][d-chlog] |
| **`/loop` sem intervalo** (`ScheduleWakeup`, 1 min a 1 h) + **`Monitor`** (vigia um comando e devolve cada linha) + `CronCreate` | 1 | tokens a cada volta; o `Monitor` evita sondar | só com a sessão aberta; expira em 7 dias; não recupera disparo perdido; `Monitor`: 5 min por padrão, máximo 30, e some com `DISABLE_TELEMETRY` ou `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`; a 2.1.292 corrige o `/loop` de sessão `--bg` que parava ao reiniciar o processo | sim; `Monitor` exige Git Bash (ele tem) | QUANDO: vigiar teste longo, CI ou PR | [scheduled-tasks][d-sched], [Monitor][d-tools-mon], [changelog][d-chlog] |
| **Tarefas agendadas do app Desktop** | 1 | grátis (mesma cota) | só com o app aberto e o PC acordado; em modo Manual a corrida para na permissão; uma corrida de recuperação ao acordar | Windows x64 | QUANDO: rotina local sem dado de paciente | [desktop-scheduled][d-deskcron] |
| **Rotinas na nuvem** (`/schedule`; ferramenta `RemoteTrigger`; gatilho agenda, API ou GitHub) | 1 | mesma cota; 100 execuções agendadas por hora por conta | clone novo do GitHub, sem seletor de permissão, sem arquivo local: o código sobe à nuvem | independe do SO | QUANDO: só projeto sem dado de paciente e com repositório no GitHub | [routines][d-routines], [tools][d-tools] |
| **PC acordado** (plano de energia; PowerToys Awake) | 1 | grátis | dormir para as sessões (as `--bg` sobrevivem à suspensão, mas não trabalham dormindo); Awake não funciona com a tela bloqueada | neste notebook a suspensão por inatividade já está em "nunca" (lido com `powercfg`); tampa fechada: não verifiquei | AGORA (conferir antes de largar) | [agent-view][d-agentview], [Awake][ms-awake], [powercfg][t-powercfg] |
| **`grilling` e `grill-me`** (instalados) | 2 | só os tokens da entrevista | pergunta a fronteira inteira numa rodada, numerada, com recomendação; não cobre pergunta que surge durante a execução | sim | AGORA (já instalado) | `claude-kit\skills\grilling\SKILL.md`, [docs do Matt][t-mattq] |
| **`to-questionnaire`** (instalada; só com `/to-questionnaire`) | 2 | tokens da entrevista | uma pessoa por documento; sem ramificação | sim | AGORA (já instalada) | [docs do Matt][t-mattq] |
| **Painel `claude agents`**: grupo "Needs input", espiar com Espaço e responder (opções por número); contador `← N agents` | 2, 3 | grátis; o resumo da linha vem de modelo pequeno | permissão, sandbox e pergunta de MCP só se respondem anexando; prévia; no VS Code não achei painel | sim, com bugs abertos (seção própria) | AGORA (já decidido o `--bg`) | [peek-and-reply][d-av-peek] |
| **`askUserQuestionTimeout`** (`60s`, `5m`, `10m`; por sessão `CLAUDE_AFK_TIMEOUT_MS`) | 2, 1 | grátis | fecha a pergunta e o Claude segue "no próprio julgamento" (pode perguntar de novo); só conta com a janela sem foco; nunca em `--bg` nem Remote Control; bug aberto: "60s" não continua ([#94372][i-94372], macOS) | Windows: não achei | QUANDO: sessão interativa que ele larga | [tools][d-tools-ask], [settings][d-set] |
| **Gancho `PreToolUse` em `AskUserQuestion`**: grava a pergunta em `PERGUNTAS.md` e responde "adiada" por `updatedInput.answers` | 2, 1 | script local; 0 token | se mal escrito decide por ele: só adiar, nunca escolher; texto livre fora dos rótulos: não achei; não testado em `--bg` | sim | AGORA, com o portão Stop; testar antes numa sessão curta | [hooks][d-hooks-ask] |
| **Projects** (claude.ai/code; painel "Waiting on you") | 2, 3 | cota da assinatura; prévia pública Pro e Max | nuvem: só repositório GitHub e arquivos enviados; skills e plugins locais não vão | independe do SO | QUANDO: projeto sem dado de paciente | [projects][d-proj] |
| **Channels** (Telegram, Discord; retransmite pedido de permissão) | 2, 4 | grátis | exige Bun (não há); prévia; `--channels` em cada sessão; o texto da ferramenta vai ao Telegram ou Discord | iMessage só macOS | NÃO | [channels][d-channels], [reference][d-chref] |
| **`loop-me`** (Matt; em-progresso): grilling para especificar rotinas; "empurrar o checkpoint para a direita" e entregar um "brief" | 2 | tokens da entrevista | cria `workflows/*.md` e `NOTES.md`; não instalada | sim | NÃO instalar; copiar o princípio para a `uso-do-claude` | [SKILL.md][t-mattloop] |
| **`batch-grill-me`** (skills.sh, 61 mil instalações) | 2 | — | não achei no repositório `mattpocock/skills` de hoje; o `grill-me` já faz rodadas | — | NÃO | [repositório][t-matt] |
| **VS Code**: várias abas ou janelas (ponto azul = permissão pendente, laranja = terminou com a aba oculta; lista de sessões com filtro "Needs input") | 3 | grátis; cada sessão gasta cota própria | `permission_prompt` chega ao gancho cerca de 6 s depois | sim | AGORA (já usa) | [vs-code][d-vscode], [hooks][d-hooks-notif] |
| **`claude -w`**, `EnterWorktree`, `isolation: worktree` | 3 | um cache por pasta | `.worktreeinclude` copia arquivo ignorado (dado!); por padrão a worktree sai de `origin/HEAD` (`worktree.baseRef`); teto de 3 janelas | sim (junções NTFS) | AGORA onde as partes forem disjuntas | [worktrees][d-wt] |
| **`claude --bg`, `/bg`, `/fork`, `claude agents`** (já decidido para encadear) | 1, 3 | cota: N sessões gastam N vezes mais rápido | isola em worktree sozinho e, ao fim, comita e dá push da própria branch (nunca `main`) se o CLAUDE.md não disser o contrário; congela com subagentes assíncronos até alguém abrir ([#92264][i-92264], macOS); as credenciais vêm do supervisor ([#87812][i-87812]) | sim, com bugs abertos ([#77754][i-77754], [#87812][i-87812], [#97273][i-97273]) | AGORA, depois do teste de cinco minutos | [agent-view][d-agentview], [isolamento][d-av-iso] |
| **App Desktop** (sessões em paralelo com opção worktree; notificação do SO ao terminar; Dispatch do celular; tarefas agendadas) | 3, 4 | grátis; Dispatch só Pro e Max | relato de a janela sair sozinha no Windows ([#91662][i-91662]); sem `--print`; Dispatch passa pelo app e pelo Cowork | Windows x64 | QUANDO: se preferir janela única às abas | [desktop][d-desktop] |
| **Mensagens entre sessões** (`SendMessage` com `notify_when_idle`) | 3, 4 | 0 token na sessão vigiada | só sessões locais; a assinatura expira em 12 h; só a conversa principal assina | sim: pipe nomeado, sem passar por servidor (2.1.234+) | QUANDO: janela coordenadora que espera as outras | [cross-session][d-xsession] |
| **herdr** (multiplexador de agentes em Rust; marca cada painel working, blocked ou idle) | 3 | grátis; Apache-2.0; 42,6 mil estrelas; push em 06/10; v0.9 | instalador por script de terceiros (`irm` e `iex`); plugins; projeto jovem | Windows nativo (ConPTY), "generally available" na doc | QUANDO: mais de 3 sessões de terminal e o painel nativo não bastar | [README][t-herdr], [Windows][t-herdr-win] |
| **claude-squad** | 3 | grátis; AGPL-3.0; 8,6 mil estrelas; push em 20/08 | exige tmux | sem Windows nativo (issues #275 e #248, na [biblioteca][b-1004]) | NÃO | [repositório][t-squad] |
| **ccmanager** | 3 | MIT; 1,3 mil estrelas; push em 27/09 | suporte oficial só Linux e macOS | só WSL | NÃO | [repositório][t-ccmgr] |
| **Nimbalyst** (sucessor do Crystal) | 3 | MIT; 1,8 mil estrelas; push em 05/10 | app Electron; análise anônima por PostHog (dá para desligar); servidor de sincronia | Windows (.exe) | NÃO | [README][t-nimb] |
| **Vibe Kanban** | 3 | Apache-2.0; 28,3 mil estrelas | a empresa encerrou em 10/04/2026; só comunidade | — | NÃO | [anúncio][t-vibe-blog] |
| **Worktrunk** (`wt`) | 3 | grátis; 8,9 mil estrelas; push em 06/10 | repete `claude -w` | `winget`; instala como `git-wt` porque `wt` é o Windows Terminal | NÃO | [README][t-wtrunk] |
| **Conductor, Sculptor, container-use** | 3 | — | Mac, Linux ou Docker | não nativo | NÃO | [biblioteca][b-1004] |
| **`PushNotification` + Remote Control** (`agentPushNotifEnabled`, já `true`; `inputNeededNotifEnabled`, ainda não) | 4 | grátis | só com o Remote Control conectado: o transcrito fica nos servidores da Anthropic e aparece no celular; texto até 200 caracteres; pula o push se ele está no terminal (`CLAUDE_CLIENT_PRESENCE_FILE`); bugs abertos [#99781][i-99781] e [#99792][i-99792] | sim | QUANDO (o Remote Control já está decidido); nunca nos `desosp-` (`remoteControlAtStartup: false` no projeto vale) | [remote-control][d-rc-push], [settings][d-set], [tools][d-tools] |
| **Gancho `Notification` e `Stop` com texto fixo** (`permission_prompt` após cerca de 6 s; `idle_prompt` após 60 s; `elicitation_dialog`; `quota_auto_resume_*`; `agent_*` só com o painel aberto) | 4 | script; 0 token | a entrada traz `message`, `transcript_path` e `cwd`: mandar só o tipo e o nome da pasta; `Stop` roda a cada turno (filtrar "fase concluída"); `idle_prompt` dispara com agentes ainda rodando ([#98373][i-98373]) | sim (`shell: powershell` no gancho) | AGORA | [hooks][d-hooks-notif], [guia][d-hooksguide] |
| **Aviso local no Windows**: MessageBox (exemplo oficial), toast WinRT por PowerShell sem módulo [I], `terminal_bell` | 4 | 0 | `preferredNotifChannel` só tem desktop em Ghostty, Kitty e iTerm2; o MessageBox pode abrir atrás do terminal | sim, sem instalar | AGORA (aviso no PC) | [guia][d-hooksguide], [terminal][d-termcfg], [toast][ms-toast] |
| **Poller de `claude agents --json --all`** (lê `state` e `waitingFor`) para ntfy ou toast | 4, 1 | script de cerca de 15 linhas, no Agendador de Tarefas a cada minuto | só estado, sem conteúdo da sessão | sim (PowerShell) | AGORA, se usar `--bg` sem o painel aberto | [agent-view][d-av-json] |
| **ntfy** (ntfy.sh grátis ou autohospedado; apps Android e iOS) | 4 | grátis; 250 mensagens por dia no ntfy.sh; 34,7 mil estrelas, Apache-2.0 | o tópico é a senha (nome longo e aleatório); o servidor guarda 12 h (`X-Cache: no` evita); o app da Play usa FCM; texto em aberto: só texto fixo, sem nome nem RA | sim, sem instalar (PowerShell `Invoke-RestMethod`) | AGORA como destino do gancho | [publish][t-ntfy-pub], [privacy][t-ntfy-priv] |
| **Telegram Bot API** e **Pushover** | 4 | Telegram grátis (1 mensagem por segundo por conversa); Pushover US$ 4,99 por plataforma e 10 mil mensagens por mês | a mensagem fica em servidor de terceiro; token do bot no PC; se a conversa com bot é criptografada ponta a ponta: não achei | sim | Telegram: QUANDO (reserva do ntfy). Pushover: NÃO (o ntfy cobre) | [Telegram][t-tg], [Pushover][t-pushover] |
| **agent-notifications** (ex-claude-notifications-go) | 4 | grátis; GPL-3.0; 814 estrelas | instala binário por script de terceiros, ganchos, servidor MCP e skill; mostra a pergunta atual e o nome da sessão; webhooks para Slack, Discord e Telegram | Windows via Git Bash | NÃO (10 linhas de gancho fazem o mesmo) | [README][t-agentnotif] |
| **BurntToast** | 4 | — | arquivado: "no longer maintained" | — | NÃO | [README][t-burnt] |
| **Happy, Omnara, Claude-Code-Remote, bot Claude Code Telegram** | 4 | Happy 24 mil estrelas (MIT); Omnara 2,9 mil; os outros 1,3 mil e 2,8 mil | Happy troca `claude` por `happy` e passa por servidor deles (criptografia ponta a ponta [A]); Omnara é nuvem; Claude-Code-Remote parado desde 12/2025; o bot não tem licença | Happy: npm | NÃO | [Happy][t-happy], [Omnara][t-omnara], [CCR][t-ccr], [bot][t-tgbot] |
| **OpenTelemetry nativo, métricas** (`CLAUDE_CODE_ENABLE_TELEMETRY=1`): `token.usage` (input, output, cacheRead, cacheCreation; modelo; `query_source` main, subagent ou auxiliary; esforço; skill, plugin, agente), `cost.usage` (USD, aproximado), `active_time.total` (`user` ou `cli`), `session.count`, `code_edit_tool.decision`, `lines_of_code`, `commit`, `pull_request` | 5 | grátis; precisa de um receptor rodando | só vai ao endpoint que ele configura, nunca à Anthropic; `user.email` e `organization.id` saem sempre ([#97908][i-97908]); `session.id` e `account_uuid` dá para tirar; as variáveis `OTEL_*` em settings de projeto são ignoradas (valem o shell e o `~\.claude\settings.json`); o projeto pode desligar um sinal (`OTEL_LOGS_EXPORTER=none`); bugs abertos de exportação silenciosa ([#91165][i-91165], [#46204][i-46204], [#89406][i-89406]) | sim; `claude --debug-file` mostra erros `[3P telemetry]` | QUANDO: depois de 1 a 2 semanas do fluxo novo, só métricas; "atenção" = `active_time` user ÷ cli e decisões manuais por hora [I] | [monitoring][d-otel] |
| **OpenTelemetry nativo, eventos** (`user_prompt`, `assistant_response`, `tool_result`, `tool_decision`, `api_request`, `api_error`, `compaction`, `subagent_completed`, `permission_mode_changed`, `hook_*`, `skill_activated`) | 5 | grátis; receptor | o texto do prompt NÃO vai por padrão (só `prompt_length`); `OTEL_LOG_USER_PROMPTS=1` liga prompt e resposta (a resposta se corta com `OTEL_LOG_ASSISTANT_RESPONSES=0`); `OTEL_LOG_TOOL_DETAILS=1` liga comandos e entradas; `OTEL_LOG_TOOL_CONTENT=1` e `OTEL_LOG_RAW_API_BODIES` levam arquivo e conversa inteira; todos desligados por padrão; para desligar, não definir | sim | NÃO ligar os `OTEL_LOG_*` nos `desosp-`; fora deles bastam `tool_decision` e `api_request` | [monitoring][d-otel] |
| **Exportar sem coletor** (`console`, `prometheus`) | 5 | grátis | não há exportador de arquivo; `console` é para depuração e onde escreve na TUI não achei (relato de saída vazia no Windows: [#46204][i-46204]); `prometheus` abre `localhost:9464/metrics`, que se lê com `curl`, mas o conflito de porta entre várias janelas não achei; saída: um receptor próprio em Python recebendo OTLP `http/json` e gravando JSONL [I] | sim | QUANDO, junto do teste de uma semana | [monitoring][d-otel], [#97908][i-97908] |
| **`/usage`, `/context`, `/insights`, statusline** (`cost`, `rate_limits` de 5 h e 7 dias, `prompt_cache`) | 5 | grátis; `/insights` gasta tokens | `/insights` varre transcritos de todos os projetos desta máquina, inclusive `desosp-` [I] | sim | AGORA (`/usage` e statusline); `/insights` fora dos `desosp-` | [costs][d-costs], [statusline][d-status], [commands][d-cmds] |
| **`session-report`** (oficial; instalado) | 5 | tokens só se pedir | lê transcritos locais | sim | AGORA (já instalado) | `~\.claude\settings.json` (`enabledPlugins`) |
| **ccusage** (`npx ccusage@latest`; relatórios por dia, semana, mês, sessão e bloco de 5 h) | 5 | grátis; o `npx` baixa o pacote a cada vez (fixar a versão); 18,9 mil estrelas; Rust; push em 06/10 | lê `~\.claude\projects\**\*.jsonl` (local); busca preços na rede (LiteLLM, models.dev) salvo `--offline` ou `CCUSAGE_OFFLINE=1`; só tokens e custo, não mede tempo; telemetria própria: não achei; o Claude apaga transcritos em 30 dias (`cleanupPeriodDays`): aumentar guarda dado de paciente por mais tempo | sim (Node já está aqui) | QUANDO: no teste de uma semana do paralelo | [README][t-ccusage], [Claude][t-ccusage-doc], [preços][t-ccusage-cost] |
| **Statusline que grava uma linha de CSV local** (custo, tokens, duração da API, % dos limites) [I] | 5 | script; 0 token | sem conteúdo; não testado | sim | QUANDO, junto da statusline decidida | [statusline][d-status] |
| **otel-tui** (visor de OTLP no terminal) | 5 | grátis; Apache-2.0; 1,1 mil estrelas; push em 05/10 | só em memória (buffer de 1000), sem arquivo | sim (binário ou `go install`) | QUANDO: ver as métricas ao vivo no teste | [README][t-oteltui] |
| **Claude-Code-Usage-Monitor** | 5 | MIT; 8,7 mil estrelas; push em 05/07; `uv tool install` | repete statusline e ccusage; limites por plano são estimativas | exige `uv` (não há) | NÃO | [README][t-monitor] |
| **claude-code-otel** (Grafana, Prometheus, Loki) | 5 | MIT; 512 estrelas; parado desde 06/2025 | exige Docker (não há) | — | NÃO | [repositório][t-cotel] |
| **claude-code-hooks-multi-agent-observability** | 5 | 1,5 mil estrelas; sem licença; parado desde 02/2026 | grava eventos de gancho num servidor local; Bun e `uv` (não há) | — | NÃO | [repositório][t-disler] |
| **Pacote ECC** (`affaan-m/ecc`: `unified-notifications-ops`, `claude-devfleet`, `autonomous-loops`) | 1, 3, 4 | 273,7 mil estrelas (skills.sh) | pacote enorme; o `devfleet` exige servidor próprio (porta 18801); o `unified-notifications-ops` é guia de triagem, não notificador | — | NÃO | [notificações][t-ecc-notif], [devfleet][t-ecc-fleet] |
| **`agent-pulse`** (skills.sh, 47,5 mil instalações) | 5 | `pip` (`agentpulse-cli`) | monitora atividade local de agentes; não achei o que lê | exige UTF-8 no Windows | NÃO por ora | [skills.sh][t-pulse] |
| **Mods** (plugin de funções, 2.1.287) | 1, 2, 4 | grátis | roda dentro do Claude com as permissões dele, sem sandbox; dias de vida; o `tool.check` foi corrigido hoje | CLI e Desktop; no VS Code é diferente | QUANDO: só se um gancho de shell não bastar | [mods][d-mods], [changelog][d-chlog] |
| **`ralph-loop`** (oficial) | 1 | — | mesma sessão, o contexto acumula; no Windows pede Git Bash, jq e perl | jq não há | NÃO | [biblioteca][b-1006a] |

## Pontos de atenção no Windows (issues abertas em 06/10/2026)

- [#77754][i-77754] (2.1.210): um `claude` iniciado de processo novo (PowerShell, cmd, terminal do VS Code) pode esperar 45 s e falhar
  com "background service did not become reachable"; de dentro de uma sessão já ligada funciona.
- [#87812][i-87812] (conta Team): o "proactive refresh" do supervisor trava cerca de 9 h e exige novo login; sessão `--bg` noturna pode pedir login.
- [#97273][i-97273]: `--bg` recusa pasta já confiável quando a caixa da chave de confiança difere da do disco (`c:/` e `C:\`).
- [#99887][i-99887]: noite parada por permissão de subagente em segundo plano (Desktop, Windows 11); o pai não é avisado. Mitigação
  do autor: proibir navegador, HTML, Artifact e computer use nos prompts de execução sem supervisão.
- [#81151][i-81151]: tarefa em segundo plano com `claude -p` aninhado é morta com a sessão ociosa; vale para o laço `claude -p`, já descartado.
- [#92264][i-92264] e [#92004][i-92004] (macOS): `--bg` congela com subagentes assíncronos; auto-continue só retoma uma sessão. No
  Windows: não achei relato igual.
- [#99781][i-99781] e [#99792][i-99792]: `PushNotification` diz "Remote Control inactive" em sessão `claude rc` (macOS); push do iOS sem som.
- [#89386][i-89386]: `DISABLE_TELEMETRY=0` ou `=false` LIGAM a desativação (qualquer valor conta).
- 2.1.292 (hoje) corrige o `/loop` de sessão `--bg` que parava ao reiniciar o processo: atualizar antes de depender dele ([changelog][d-chlog]).

## Armadilhas de privacidade versus recursos

- **Remote Control:** enquanto conectado, o transcrito (mensagens, respostas, atividade de ferramentas) fica nos servidores da
  Anthropic e aparece no celular; retenção de 30 dias com treino desligado e 5 anos com treino ligado ([remote-control][d-rc-sec],
  [data-usage][d-data]; conferir em claude.ai/settings/data-privacy-controls). `remoteControlAtStartup: true` só vale no
  `~\.claude\settings.json`; um `false` no projeto vale ([settings][d-set]).
- **`--bg` comita e dá push** da própria branch (nunca `main`) quando o repositório tem remoto; "as instruções de git do usuário
  vencem" ([agent-view][d-av-iso]). Escrever "não dar push" no CLAUDE.md dos projetos e manter o gancho de guarda de dado.
- **Gancho de aviso:** nunca enviar `message`, `transcript_path` nem nome ou RA; só o tipo e o nome da pasta.
- **OTel:** `OTEL_LOG_RAW_API_BODIES` leva a conversa inteira (inclusive em arquivo, `file:<dir>`); nunca nos `desosp-`.
- **`DISABLE_TELEMETRY` e `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`:** os dois desligam o `Monitor`; o segundo também desliga o Remote Control
  ([tools][d-tools-mon], [remote-control][d-rc]).
- **`/insights`, `/fewer-permission-prompts` e ccusage** leem transcritos; os transcritos ficam 30 dias em texto puro por padrão
  ([data-usage][d-data]).

## Não achei

- O que o `claude --bg` faz ao bater o limite de uso (a doc só diz que a espera automática não é oferecida em sessão em segundo plano).
- Se `Notification` com `permission_prompt` dispara numa sessão `--bg` sem o painel aberto.
- Agent view dentro da extensão do VS Code.
- Se `answers` do `AskUserQuestion` aceita texto livre, fora dos rótulos das opções, quando vem de um gancho.
- Se a parte "desktop" do `PushNotification` aparece no Windows Terminal ou no VS Code.
- Onde o exportador `console` do OTel escreve numa sessão interativa; conflito da porta 9464 entre várias janelas.
- Variável nativa que impeça a suspensão do Windows durante uma sessão.
- Telemetria própria do ccusage (só achei o download de preços); se a conversa com bot do Telegram é criptografada ponta a ponta.
- Push do celular a partir de sessão `--bg` (a biblioteca de 06/10 já registrava o `--bg` dentro do Remote Control como [não achado]).

## Teste de cinco minutos antes de depender do `--bg` (sem instalar nada)

1. `claude --version` (2.1.292 ou mais).
2. Num PowerShell novo e no terminal do VS Code: `claude daemon status` (se esperar 45 s, é o [#77754][i-77754]).
3. `claude --bg --name teste "responda ok e pare"` e depois `claude agents --json --all` (conferir `state`).
4. `/status`: a linha "Auto mode server" deve estar `Enabled`.
5. Uma pergunta de teste numa sessão `--bg` e ver se vira "Needs input" (e se o gancho `PreToolUse` a responde).
6. Um gancho `Notification` de teste com texto fixo, dentro e fora do painel aberto.

## Fontes (lidas em 06/10/2026)

**Documentação oficial (code.claude.com/docs/en):**

[d-perm]: https://code.claude.com/docs/en/permission-modes
[d-classif]: https://code.claude.com/docs/en/auto-mode-classifier-billing
[d-tools]: https://code.claude.com/docs/en/tools-reference
[d-tools-mon]: https://code.claude.com/docs/en/tools-reference#monitor-tool
[d-tools-ask]: https://code.claude.com/docs/en/tools-reference#question-auto-continue-timeout
[d-tools-ps]: https://code.claude.com/docs/en/tools-reference#powershell-tool
[d-hooks-notif]: https://code.claude.com/docs/en/hooks#notification
[d-hooks-perm]: https://code.claude.com/docs/en/hooks#permissionrequest
[d-hooks-ask]: https://code.claude.com/docs/en/hooks#allow-with-updatedinput
[d-hooksguide]: https://code.claude.com/docs/en/hooks-guide#get-notified-when-claude-needs-input
[d-inter]: https://code.claude.com/docs/en/interactive-mode#wait-for-a-usage-limit-to-reset
[d-errors]: https://code.claude.com/docs/en/errors#youve-hit-your-session-limit
[d-goal]: https://code.claude.com/docs/en/goal
[d-sched]: https://code.claude.com/docs/en/scheduled-tasks
[d-deskcron]: https://code.claude.com/docs/en/desktop-scheduled-tasks
[d-routines]: https://code.claude.com/docs/en/routines
[d-agentview]: https://code.claude.com/docs/en/agent-view
[d-av-peek]: https://code.claude.com/docs/en/agent-view#peek-and-reply
[d-av-json]: https://code.claude.com/docs/en/agent-view#read-session-state-from-a-script
[d-av-iso]: https://code.claude.com/docs/en/agent-view#how-file-edits-are-isolated
[d-av-lim]: https://code.claude.com/docs/en/agent-view#limitations
[d-wt]: https://code.claude.com/docs/en/worktrees
[d-desktop]: https://code.claude.com/docs/en/desktop
[d-vscode]: https://code.claude.com/docs/en/vs-code
[d-rc]: https://code.claude.com/docs/en/remote-control
[d-rc-push]: https://code.claude.com/docs/en/remote-control#mobile-push-notifications
[d-rc-sec]: https://code.claude.com/docs/en/remote-control#connection-and-security
[d-set]: https://code.claude.com/docs/en/settings-reference
[d-xsession]: https://code.claude.com/docs/en/cross-session-messaging
[d-channels]: https://code.claude.com/docs/en/channels
[d-chref]: https://code.claude.com/docs/en/channels-reference
[d-proj]: https://code.claude.com/docs/en/claude-projects
[d-termcfg]: https://code.claude.com/docs/en/terminal-config#get-a-terminal-bell-or-notification
[d-otel]: https://code.claude.com/docs/en/monitoring-usage
[d-costs]: https://code.claude.com/docs/en/costs
[d-status]: https://code.claude.com/docs/en/statusline
[d-cmds]: https://code.claude.com/docs/en/commands
[d-data]: https://code.claude.com/docs/en/data-usage
[d-mods]: https://code.claude.com/docs/en/plugins/mods/overview
[d-chlog]: https://code.claude.com/docs/en/changelog

Também lidos: [agents](https://code.claude.com/docs/en/agents), [mobile](https://code.claude.com/docs/en/mobile), [env-vars](https://code.claude.com/docs/en/env-vars) (`CLAUDE_CODE_DISABLE_NOTIFICATION_PRESENCE_CHECK`) e [llms-full.txt](https://code.claude.com/docs/llms-full.txt) (`PushNotification`: entrada `message` e `status`; saída `pushSent`, `localSent`, `disabledReason`).

**Issues de anthropics/claude-code (estado em 06/10/2026):**

[i-77754]: https://github.com/anthropics/claude-code/issues/77754
[i-87812]: https://github.com/anthropics/claude-code/issues/87812
[i-97273]: https://github.com/anthropics/claude-code/issues/97273
[i-99887]: https://github.com/anthropics/claude-code/issues/99887
[i-81151]: https://github.com/anthropics/claude-code/issues/81151
[i-92264]: https://github.com/anthropics/claude-code/issues/92264
[i-92004]: https://github.com/anthropics/claude-code/issues/92004
[i-99781]: https://github.com/anthropics/claude-code/issues/99781
[i-99792]: https://github.com/anthropics/claude-code/issues/99792
[i-94372]: https://github.com/anthropics/claude-code/issues/94372
[i-97908]: https://github.com/anthropics/claude-code/issues/97908
[i-91165]: https://github.com/anthropics/claude-code/issues/91165
[i-46204]: https://github.com/anthropics/claude-code/issues/46204
[i-89406]: https://github.com/anthropics/claude-code/issues/89406
[i-89386]: https://github.com/anthropics/claude-code/issues/89386
[i-98373]: https://github.com/anthropics/claude-code/issues/98373
[i-91662]: https://github.com/anthropics/claude-code/issues/91662

**Terceiros (estrelas e datas pela API do GitHub em 06/10/2026):**

[t-ccusage]: https://github.com/ccusage/ccusage
[t-ccusage-doc]: https://github.com/ccusage/ccusage/blob/main/docs/guide/claude/index.md
[t-ccusage-cost]: https://github.com/ccusage/ccusage/blob/main/docs/guide/cost-modes.md
[t-monitor]: https://github.com/Maciek-roboblog/Claude-Code-Usage-Monitor
[t-cotel]: https://github.com/ColeMurray/claude-code-otel
[t-oteltui]: https://github.com/ymtdzzz/otel-tui
[t-disler]: https://github.com/disler/claude-code-hooks-multi-agent-observability
[t-ntfy-pub]: https://docs.ntfy.sh/publish/
[t-ntfy-priv]: https://docs.ntfy.sh/privacy/
[t-pushover]: https://pushover.net/pricing
[t-tg]: https://core.telegram.org/bots/faq
[t-agentnotif]: https://github.com/777genius/agent-notifications
[t-burnt]: https://github.com/Windos/BurntToast
[t-herdr]: https://github.com/herdrdev/herdr
[t-herdr-win]: https://herdr.dev/docs/windows-beta/
[t-squad]: https://github.com/smtg-ai/claude-squad
[t-ccmgr]: https://github.com/kbwo/ccmanager
[t-nimb]: https://github.com/nimbalyst/nimbalyst
[t-vibe-blog]: https://vibekanban.com/blog/shutdown
[t-wtrunk]: https://github.com/max-sixty/worktrunk
[t-happy]: https://github.com/slopus/happy
[t-omnara]: https://github.com/omnara-ai/omnara
[t-ccr]: https://github.com/JessyTsui/Claude-Code-Remote
[t-tgbot]: https://github.com/overwirehq/claude-code-telegram
[t-matt]: https://github.com/mattpocock/skills
[t-mattq]: https://github.com/mattpocock/skills/blob/main/docs/productivity/to-questionnaire.md
[t-mattloop]: https://github.com/mattpocock/skills/blob/main/skills/in-progress/loop-me/SKILL.md
[t-pulse]: https://skills.sh/jane-o-o-o-o/agent-pulse-skill/agent-pulse
[t-ecc-notif]: https://skills.sh/affaan-m/ecc/unified-notifications-ops
[t-ecc-fleet]: https://skills.sh/affaan-m/ecc/claude-devfleet
[ms-awake]: https://learn.microsoft.com/en-us/windows/powertoys/awake
[ms-toast]: https://learn.microsoft.com/en-us/uwp/api/windows.ui.notifications.toastnotificationmanager
[t-powercfg]: https://www.elevenforum.com/t/change-when-to-put-computer-to-sleep-timeout-in-windows-11.5618

**Busca de skills (`npx skills find`, só busca):** notification, push notification, ntfy, claude code notify, parallel agents,
worktree, background agent, long running, autonomous, ask user question, questions, usage, tokens, ccusage, telemetry,
opentelemetry, token usage claude code, claude code cost, telegram, pushover, desktop notification, schedule, cron, queue,
interview, overnight, unattended, session manager, usage monitor, claude code monitor, handoff. Quase tudo era ruído
(Azure, Lark, marketing); o que sobrou está nas linhas acima.

**Biblioteca (já lida):**

[b-1006a]: 2026-10-06_continuar-em-contexto-limpo-sem-copiar-prompt.md
[b-1005]: 2026-10-05_sessoes-memoria-plugins-claude-code.md
[b-1004]: 2026-10-04_janelas-paralelas-e-tokens.md
[b-1006b]: 2026-10-06_ferramentas-pedidas-e-orquestradores.md
[b-1006c]: 2026-10-06_marketplace-local-e-skills-por-projeto.md
[b-0928]: 2026-09-28_claude-code-na-nuvem.md
