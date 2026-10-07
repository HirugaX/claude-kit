# Plano do fluxo novo — fases, portões e prompts (06/10/2026)

> Janela do plano (notebook, Opus 5.5 · high). Base: `claude-kit\decisoes\2026-10-06_entrevista-fluxo.md` (Q1-Q15 na
> §5, §6, §12) + a rodada 3 desta janela (Q16-Q33). **Aprovado pelo Ettore em 06/10/2026** (aprovação do modo
> plano). As pesquisas desta janela: as três linhas de 06/10 no fim do `pesquisas\INDICE.md`.
> **R1 (06/10):** objetivo revisto e plano ajustado (Q34-Q48) — `decisoes\2026-10-06_R1-objetivo-medicao-recursos.md`.

## Contexto

O Ettore quer a melhor tarefa feita, com a maior qualidade, pelo menor uso de tokens, sem ser "office boy de
prompts", sem contexto desnecessário e com estado e decisões que sobrevivem entre sessões. O diagnóstico (§4 do
registro): o custo dominante é o tamanho da conversa (mediana de 199 a 317 mil tokens por chamada), não as skills;
~7 passos manuais por janela; estado que só cresce (handoffs de 575 e 376 KB); o mesmo método implementado três
vezes. Este plano leva o fluxo novo do kit aos projetos, em duas frentes, com portões conferidos por comando.

**Objetivo revisto na R1 (Q34):** atenção concentrada. O Ettore senta poucas vezes, quando escolhe, e responde de uma vez
o que precisa dele (grill, plano, fila de perguntas); entre uma sentada e outra o Claude trabalha sozinho por horas, em
fases curtas encadeadas e em tantas janelas quanto o trabalho independente permitir, e só o chama quando nada mais anda
sem ele — com a mesma qualidade, economia e padrão. A régua: retornos, sentadas, maior trecho sem ele e janelas ao mesmo
tempo ("Verificação de ponta a ponta"; registro em `decisoes\2026-10-06_R1-objetivo-medicao-recursos.md`).

## A cadeia

```
Agora     F0 (Ettore) · R0 revisão de front (desosp-app) ∥ F1a
Frente 1  F1a → R1 → F1b → F2a → F2b → (F3a ∥ F3b) → F3c → F5a → F5b → (F6 ∥ F7) → F8 → F9
Frente 2  (depois do F5b) N1 estudo → F5c porta de leitura → N2 comunicação → N3 organização → N4 produtividade → N5 pesquisa
No desktop, quando estiver lá: Fd (Drive)
```

Janelas ao mesmo tempo: tantas quanto houver trabalho independente, com um escritor por projeto (ou por worktree, até 3
no mesmo projeto), desde que o total de tokens fique igual ou menor que em série (Q37, R1); o app tem prioridade. Uma
janela = um projeto.

## Como você opera daqui em diante

**Até o F3 terminar (F1a até F3c), como hoje, pela última vez:**

1. Abra a janela na pasta que o prompt indica (painel do VS Code: abrir a pasta; terminal: `cd <pasta>` e `claude`).
2. Digite o `/effort` da 1ª linha do prompt. Se o prompt pedir Sonnet 5.5 para a janela, escolha-o **na lista** do
   `/model` — nunca digite `sonnet` (abre o Sonnet 5). O `/effort` digitado grava o padrão para as próximas janelas;
   não importa, porque todo prompt traz o seu (para valer só na sessão, use o seletor do `/effort` e a tecla `s`).
3. Cole o prompt. O Claude trabalha e para nos pontos da Q10: escrita em dado real não aprovada antes; rodada real ou
   reprocesso não aprovados; migração de banco ou de esquema; regra clínica nova; leitura de fonte nova; subir para
   Fable, `xhigh`, `max` ou ultracode (descer, se mantém a qualidade, não pergunta); o mesmo erro depois de duas
   tentativas diferentes; decisão que não está no `ESTADO.md` nem num ADR. Com o Remote Control ligado sozinho (R1;
   ADR-0001 D8), dá para responder pelo app do celular.
4. Responda no chat com a letra e a nuance ("a, mas sem X").
5. Ao fechar, a janela entrega o resumo (com "Sinais de insuficiência do modelo") e o prompt da próxima, já conferido.
   Copie, feche, abra a próxima. Paralelo só onde o plano diz: R0 ∥ F1a agora; F3a ∥ F3b; depois do F5b, F6 ∥ F7 ∥ N1.

**Depois do F3, se o laço passar (o F3c liga), você não carrega mais prompt:**

1. A janela que termina grava `docs\ESTADO.md` (onde estamos) e `docs\PROXIMO.md` (o prompt da próxima) e lança a fase
   seguinte sozinha: `claude --bg --name <fase> --model <modelo> --effort <nível> "Leia docs/PROXIMO.md e siga"` (ou
   numa aba interativa do terminal, com Remote Control, se o F3a mostrar melhor — Q9, R1).
2. Você acompanha no terminal: `claude agents` (o que está rodando), `claude attach <nome>` (entrar), `claude logs
   <nome>` (ver sem entrar). Uma dúvida que é sua vai para o `docs\PERGUNTAS.md` do projeto, e a fase segue com o que
   não depende dela (Q35); ela só para quando tudo o que sobra depende da fila — aí grava o `ESTADO.md` e avisa.
3. Você entra nas sentadas que escolher: responde a fila de uma vez (na janela do projeto ou pelo app) e aprova plano
   novo, que termina com a rodada de contingências — as "Decisões pré-aprovadas" do `PROXIMO.md` (Q36) — com "Yes,
   clear context and…": o planejamento sai do contexto e fica só o plano.
4. Reserva, no painel do VS Code: se o lançamento automático falhar, `/clear` e depois "siga" — o gancho injeta o
   `PROXIMO.md`.
5. Celular: o Remote Control liga sozinho em toda sessão interativa (R1; ADR-0001 D8). A fase avisa pelo
   `PushNotification` em três casos — parou porque tudo depende da fila; a cadeia terminou; falha que só você resolve —
   e você responde pelo app. Onde o Remote Control não ligar sozinho, não há aviso (o F3a confere o painel e a `--bg`).
6. Toda fase de execução começa com o `/goal` "portão ou fila" que vem pronto no `PROXIMO.md` (Q44). A cada 15 dias, o
   balanço das métricas aparece numa linha ao abrir uma janela, com as propostas na fila do kit (Q42).

**Onde olhar:** o estado de cada projeto em `docs\ESTADO.md` (uma página); o que vem em `docs\PROXIMO.md`; o porquê em
`docs\adr\` (no kit, `decisoes\`); no terminal, a statusline (modelo, esforço, % do contexto); o custo em
`python C:\CLAUDE-PROJETOS\claude-kit\plugins\nucleo\skills\uso-do-claude\medir_uso.py --sessoes` (o F2a o move para
`scripts\`); a semana em `claude-kit\metricas\uso-semanal.csv` (`scripts\medir_semana.py`; a planilha `metricas\uso.xlsx`
e os balanços em `metricas\balancos\`, a partir do F2b); as perguntas pendentes no `docs\PERGUNTAS.md` de cada projeto (a partir do
F2b); as skills na seção "Skills deste projeto" do CLAUDE.md e no `claude-kit\GUIA_DAS_SKILLS.docx`.

**O que continua sendo seu:** o `/effort` como comando; `max`, `xhigh`, Fable e ultracode só com motivo escrito; nunca
`/omc-setup`; mover ou apagar pasta de projeto e mexer na raiz do `C:` (o modo automático bloqueia); aplicar a política
do safety-net quando nascer pasta de dado nova (o plugin não deixa o Claude mudar a própria política; a fase imprime o
comando); o "sim" antes de qualquer mudança (o plano aprovado é o "sim" do que ele pede).

**Quando algo dá errado:** a fase falhou no mesmo ponto duas vezes → ela anota no `ESTADO.md` e para; você escolhe
repetir com esforço maior ou voltar ao `/grill-me`. Aviso de troca para o Opus 5 no meio da conversa → `/model` e
Opus 5.5. Duas janelas no mesmo projeto → feche uma e rode `git status`. Arquivo solto no Drive → `IA\00-entrada`.

## Decisões da rodada 3 (06/10)

Q1-Q15 continuam como no registro (§5). A rodada 3:

| # | decisão |
|---|---|
| Q16 | Isolamento: domínios com prefixo (`desosp-`, `pesquisa-`, `estudo-`, `pessoal-`; os do desktop no F8); informação só cruza pelos canais (caixas `docs\para_*` entre `desosp-`, `caixa\` do kit entre os PCs, `pesquisas\`); dado em `<projeto>-dados\`, pasta irmã fora do git, com `deny` + safety-net + `.ignore`; o dado do censo e do HC só muda na fase deles; uma janela = um projeto; a mãe e o kit não fazem trabalho de projeto. |
| Q17 | O kit vira marketplace local; skills em plugins por grupo (o nosso e o de terceiros separados; agrupados por onde se usam); cada projeto liga os seus por `enabledPlugins`; teste com um plugin antes de migrar. |
| Q18 | `orquestrar` nossa, fina, + SDD (4 skills avulsas). Menos de 4 tarefas → sessão + subagentes; plano no mesmo código → SDD; 4+ itens do mesmo formato, conferidos por comando, sem decisão no meio e sem dado de paciente → Workflow, teto 10 (acima: estimativa + "sim", Q13). Disputa SDD × OMC × sem orquestrador no F3b. |
| Q19 | F3a (o laço) ∥ F3b (as ferramentas), em pastas de teste separadas. claude-mem, se passar, primeiro no estudo. Cartographer no F6. |
| Q20 | A `recursos-do-projeto` decide (enxugada); o `claude-code-setup` é descoberta opcional; forma final depois do F3b. |
| Q21 | Escrita em dado real aprovada por fase (`PROXIMO.md`: comando, pasta, limite) e por rotina (a rodada do kernel); um gancho barra Write/Edit fora da lista. |
| Q22 | Comunicação com marcadores (`{{nome}}`, `{{matricula}}`, `{{telefone}}`) + script local; o ADR de privacidade pode rever. |
| Q23 · Q30 · Q31 | Frente 1: kit → app (principal) → kernel → planilha → desktop. Frente 2, depois do piloto do app: estudo → comunicação → organização → produtividade → pesquisa (por último). |
| Q24 | Três projetos pessoais no Claude Code: `estudo-residencia`, `pessoal-organizacao`, `pessoal-produtividade`. |
| Q25 · Q32 | Drive: tudo em `IA\<projeto>` (mais `IA\00-entrada`); arrumação numa janela curta no desktop, onde o `G:` existe. |
| Q26 | Fica só a `find-skills`; o Ettore desliga `llm-council` e `prompt-master` no claude.ai. |
| Q27 | `pesquisa-clinica`: raiz `projeto-ia`; `fontes` = `eu-forneco-fontes`. |
| Q28 | O guia do Claude Docs se aposenta, com aviso apontando para o `GUIA_DAS_SKILLS.docx`. |
| Q29 | Revisão de front do app já, em paralelo (R0), só leitura. |
| pedido | "Ensine como operar daqui em diante" → a seção acima; vira o `COMO_OPERAR.md` e a 1ª parte do guia em Word. |
| pedido | Mermaid nos documentos que o Claude lê → **não aplicado**: não reduz tokens (+33% a +62% de caracteres na regra real) e não há ganho de acerto comprovado para o Claude (ver Ficha, NÃO). |

## Decisões da R1 (06/10)

O registro completo, com o porquê e as nuances do Ettore: `decisoes\2026-10-06_R1-objetivo-medicao-recursos.md`.

| # | decisão |
|---|---|
| Q34 | Objetivo: atenção concentrada (ver Contexto). Régua: retornos, sentadas, maior trecho sem ele, janelas ao mesmo tempo; os gestos por fase passam a medida secundária. |
| Q35 | Fila: a dúvida vai para `docs\PERGUNTAS.md` e a fase segue com o que não depende dela; só para quando tudo depende da fila. Os pontos da Q10 continuam "nunca sem o sim", sem travar o resto. Vale a partir do F2, com os ganchos. |
| Q36 | `PROXIMO.md` com "Decisões pré-aprovadas" e "Sempre me pergunte"; rodada de contingências no fim de todo grill e plano (a Q21 generalizada). |
| Q37 | Janelas pela posse de arquivo e pelo total de tokens (iguais ou menores que em série, com a mesma qualidade); F6 ∥ F7 depois do F5b. |
| Q38 | andrej-karpathy-skills: 4º executor do F3b, com critério fixado antes (≥ 20% menos tokens ou menos mudanças fora do pedido, mesmos testes verdes, sem parar mais). |
| Q39 | Medição semanal automática (`scripts\medir_semana.py` → `metricas\uso-semanal.csv`); metas na "Verificação de ponta a ponta". |
| Q40 | session-report só nas pastas de teste, sempre com `--dir`, com um gancho que barra o comando sem ele. |
| Q41 | `cleanupPeriodDays: 90` até o F9 (gravado na R1). |
| Q42 | Planilha `metricas\uso.xlsx` e balanço automático a cada 15 dias, com as propostas na fila do kit. |
| Q43 · Q48 | Aviso só pelo Remote Control (ligado sozinho em todo projeto, inclusive nos `desosp-`) + `PushNotification`; onde ele não ligar, nenhum aviso (ADR-0001 D8). |
| Q44 | `/goal` "portão ou fila" em toda fase de execução. |
| Q45 | Sonda por arquivo + aviso de "pronto" ao vivo no mesmo domínio, só se o F3a mostrar ganho de tempo ou de tokens. |
| Q46 | F1b e F2 como neste plano, com as paradas; o modelo novo só vale com os controles (F2, F3). |
| Q47 | Frente 2 sem mudança. |

## Ficha de recursos — o fluxo novo (`recursos-do-projeto` §5)

Base: a entrevista de 05-06/10 e a rodada 3; o inventário das pesquisas de 05-06/10 e desta janela.

**AGORA (11)**

| recurso | por quê | como saber que funcionou | custo |
|---|---|---|---|
| 1. Kit como marketplace local, plugins por grupo; `config\plugins.json` com os plugins de fora (safety-net, claude-md-management, session-report — só nas pastas de teste, com `--dir` —, frontend-design, notion) e o escopo de cada | Q17, Q14, Q6, 6.1, Q40 | `instalar_kit.py --verificar`; numa pasta de rascunho, `engenharia` desligado some da lista e ligado aparece; `/grill-me` curto funciona | F1b; menos descrições onde o grupo está desligado |
| 2. `uso-do-claude` quebrada no plugin `nucleo`: núcleo ≤ 150 linhas + `modelo-e-esforco`, `fechar-janela`, `pesquisa`, `orquestrar`; `organizar-projetos` quebrada em 3 skills só `/` (`organizar-projetos`, `cores-das-pastas`, `icones`) no plugin `kit`, ligado no kit e na janela da raiz (07/10); o gancho das cores fica no `nucleo` | Q4, Q5; §4 (22 KB a cada disparo); F1b (07/10) | `wc -l` ≤ 150; `perguntas_controle.py` bate; tokens por disparo antes × depois | F2a |
| 3. Estado em arquivo: `docs\ESTADO.md` (≤ 1 página, reescrito), `docs\PROXIMO.md` (com "Escritas em dado real aprovadas"), `docs\adr\`, `GLOSSARY.md`. Desenho embasado (Q3): arquivo de progresso + `git log` (harness de longa duração da Anthropic), ExecPlan da OpenAI (Progress, Surprises, Decision Log, Outcomes; "recomeçar só com ele"), `STATE.md` do GSD, ADR + glossário do Matt Pocock (`domain-modeling`) | Q3, Q21 | no F3a uma sessão nova recomeça só com eles; no F5a o `ctx0` do app cai | ≤ 1 página por abertura |
| 4. Ganchos no `nucleo`, em duas camadas: **sempre** (todo projeto: `PreModelSwitch` barra o Sonnet 5; SessionStart avisa modelo e esforço errados e faz `git pull --ff-only` do kit, avisando se divergiu); **só onde existe `docs\ESTADO.md`** (o resto do SessionStart; portão `Stop`, até 8 bloqueios seguidos, que aceita fechar com a fila gravada; guarda de escrita em pasta de dado; a fila: `PermissionRequest` nega e enfileira na execução largada, `PreToolUse` em `AskUserQuestion` grava em `PERGUNTAS.md` e responde "adiada" — só adiar, nunca escolher) | Q3, Q9, Q10, Q12, Q21, Q35; lições 1-2 de `pesquisas\2026-10-05_fluxo-atual-dos-projetos.md` | `testar_ganchos.py` (JSON) verde; no F3a barram fechar sem estado, Write fora da lista e `/model sonnet`, e a fase segue com as decisões plantadas na fila | ~0 token; milissegundos por evento |
| 5. Encadeamento por `claude --bg` ou por sessão interativa numa aba nova (com Remote Control e a espera do limite de uso) — o F3a compara e o F3c escolhe; desligado em `config\fluxo.json` até o F3c ligar; reserva `/clear` + gancho + `showClearContextOnPlanAccept` | Q9, Q2, Q37 | no F3a a fase 2 começa sozinha; retornos e maior trecho sem ele medidos | um processo novo por fase |
| 6. SDD dentro da `orquestrar` | Q5, Q13, Q18 | disputa do F3b com números | ~8 mil tokens por uso + contexto novo por tarefa |
| 7. Statusline no terminal (modelo, esforço, % do contexto, % de 5 h e semanal) | Q1; lição 2 (`/effort` grava); Q39 | aparece no terminal; o % chega ao arquivo que o `medir_semana.py` lê | 0 token |
| 8. Medição semanal: `scripts\medir_semana.py` (protótipo da R1) → `metricas\uso-semanal.csv` (só números); planilha `metricas\uso.xlsx` (fora do git); gancho semanal sem imprimir; balanço a cada 15 dias (`metricas\BALANCO.md` → `metricas\balancos\`, propostas na fila do kit) | Q39, Q42 | a linha de 29/09 reproduzida; a planilha gerada; o 1º balanço com propostas | ~2 s e 0 token por semana; o balanço, algumas dezenas de milhares de tokens a cada 15 dias |
| 9. `/goal` "portão ou fila" em toda fase de execução, com a linha pronta no `PROXIMO.md` | Q44 | no F3a a fase não para antes do portão nem da fila | o avaliador custa pouco (documentação) |
| 10. Remote Control ligado sozinho (`remoteControlAtStartup: true`, gravado na R1) + `PushNotification` nos três casos, com texto só de projeto, fase e contagem | Q43, Q48; ADR-0001 D8 | no F1b: ligou no painel?; no F3a o aviso chega e se responde pelo app | 0 token |
| 11. `PROXIMO.md` com "Decisões pré-aprovadas" e "Sempre me pergunte"; rodada de contingências no fim de todo grill e plano | Q36, Q21 | no F3a a decisão pré-aprovada não para a fase | algumas linhas por fase |

**QUANDO**

| recurso | o gatilho |
|---|---|
| `claude-code-setup` | passou no F3b → passo opcional de descoberta da `recursos-do-projeto`, por `--plugin-dir` (sem instalar); no app, roda no F5a |
| OMC | só se vencer a disputa do F3b; contido por projeto; nunca `/omc-setup` |
| Headroom | cortou ≥ 20% dos tokens no F3b sem quebrar nada → só em sessões de terminal |
| claude-mem | passou no F3b → primeiro no `estudo-residencia`; nunca nos `desosp-` enquanto o banco for global (ADR-0001 D3) |
| Cartographer | F6, comparado com a `improve-codebase-architecture`, sem os passos 7 e 8 (os que editam o CLAUDE.md) |
| `chief-of-staff` (Matt) | só como lente, numa sessão supervisionada (já instalada, só `/`) |
| `implement-spec` (Matt) | só tickets independentes, até 3 implementadores, 1 ticket de teste antes, sem push (já instalada, só `/`) |
| Workflow e `/effort ultracode` | 4+ itens do mesmo formato, conferidos por comando, sem dado de paciente, teto 10; ultracode só com motivo escrito |
| Estilos de saída `learning` / `explanatory` | quando o Ettore quiser aprender o código de um projeto (12.5: vibe coder aprendendo) |
| Janela coordenadora pequena (lança fases e sondas e repassa tudo; o desenho do §6.3 do registro) | acima de 3 ou 4 janelas ao mesmo tempo (Q45) |
| Context7 | DASH (F8), bibliotecas que mudam rápido |
| Playwright MCP | só numa janela de depuração do app |
| GitHub MCP ou `gh` | quando houver issues, PRs ou nuvem |
| Plugin do Notion e conectores do claude.ai | ADR-0001 D4: nos `pessoal-*`, ligados; nos `desosp-`, todos negados pelo nome menos o Google Drive; em `pesquisa-` e `estudo-`, `disableClaudeAiConnectors: true` (+ `.mcp.json`) — no `.claude\settings.json` versionado |
| Conector PubMed (escopo de projeto), `paper-lookup`, `scientific-critical-thinking`, `pergunta-clinica` | `pesquisa-clinica` (N5) |
| `subagentPromptCacheTtl: "1h"` | se a medição semanal mostrar cache gravado alto nos subagentes |
| andrej-karpathy-skills | passou no critério do F3b (Q38) → `config\plugins.json` no F3c |
| Mensagens entre sessões (`SendMessage`, aviso de "pronto") | o F3a mostrou ganho de tempo ou de tokens (Q45); só dentro do mesmo domínio |
| `askUserQuestionTimeout` | sessão interativa que o Ettore larga (não vale em `--bg` nem no Remote Control) |
| OpenTelemetry só com métricas (nunca `OTEL_LOG_USER_PROMPTS` nem o corpo da API) | se a medição pelas transcrições não bastar |
| herdr | mais de 3 sessões de terminal ao mesmo tempo |
| Diagrama (Mermaid, mapa mental) **para gente** | no estudo (N1) e no guia, renderizado; nunca como fonte única de regra que o Claude lê |

**NÃO**

| recurso | por quê |
|---|---|
| `/omc-setup` | sobrescreve o `~\.claude\CLAUDE.md` e a statusline |
| GSD, planning-with-files, claude-remember | segundo dono do estado |
| `research` (Matt) | substituída pela nossa `pesquisa` (biblioteca → subagente → salvar) |
| Times de agentes | ~7× o custo; os painéis não funcionam no VS Code nem no Windows Terminal |
| Laço `claude -p` | sem sandbox no Windows nativo; risco de política de cobrança |
| `llm-council`, `prompt-master` | Q26 |
| `research-lookup` e tudo o que pede chave paga | custo; manda a pergunta a terceiros |
| Plugin `healthcare` inteiro | traz extração de nota clínica |
| hookify, security-guidance | `python3` da Loja; revisão por LLM a cada `Stop` |
| Mermaid no que o Claude lê (CLAUDE.md, ESTADO, skills, regras) | na regra real de roteamento: prosa 335 caracteres, lista 347, tabela 390, Mermaid 445-542; o único estudo direto (FlowBench, só GPT) dá ganho no passo seguinte mas sessão inteira igual à prosa; a Anthropic recomenda títulos, listas numeradas e tabelas, e 0 de 7 skills oficiais usam Mermaid. Reabrir só se surgir máquina de estados com laço que lista e tabela não deem conta |
| Aviso por gancho para ntfy, toast, Telegram ou Pushover | não deixa responder pelo celular; o aviso fica só com o Remote Control (Q43) |
| ccusage, Claude-Code-Usage-Monitor, claude-code-otel | repetem a medição semanal; os dois últimos exigem uv, Docker ou Bun |
| `/insights` | gasta tokens e escreve texto das conversas de todos os projetos |
| claude-squad, ccmanager | exigem tmux ou WSL; sem Windows nativo |
| Nimbalyst, Vibe Kanban | telemetria e servidor de sincronia; a empresa do Vibe Kanban encerrou |
| Channels (Telegram, Discord) | exige Bun e manda texto de ferramenta a terceiros |

**Regras para escrever**

- CLAUDE.md pessoal: a privacidade do ADR-0001 e o ponteiro do ADR-0002 (F1a); `instalar_kit.py` e
  `atualizar_terceiros.py` no lugar do `ligar_claude.py` (F1b). Desde 07/10 o `~\.claude\CLAUDE.md` é só o import
  `@C:/CLAUDE-PROJETOS/claude-kit/CLAUDE.md`: edita-se o do kit, sem hardlink nem `fsutil`. A exceção da Q15 (plano em janela nova acima de ~200 mil tokens) vai no núcleo da skill (F2a).
- CLAUDE.md de cada projeto (< 200 linhas): sem estado; "Skills deste projeto" (≤ 10 linhas); comandos e invariantes.
- `.claude\settings.json` de cada projeto (versionado): `enabledPlugins` dos grupos dele; `deny` das pastas de dado
  (ADR-0001 D6); conectores pela D4 do ADR-0001 (`desosp-`: todos negados menos o Drive; `pesquisa-` e `estudo-`:
  `disableClaudeAiConnectors: true`; `pessoal-*`: ligados).
- Memória automática só com preferência e correção; nunca estado.
- Texto de aviso no celular (`PushNotification`): só projeto, fase e contagem; nunca nome nem pseudônimo (ADR-0001 D8).
- No nível global, só dispara sozinha a skill que precisa disparar sem o Ettore lembrar (núcleo, `modelo-e-esforco`,
  `fechar-janela`, `orquestrar`, `pesquisa`); o resto é só `/`.
- Skill de domínio mora no projeto (`.claude\skills\`), nunca no kit.
- Toda fase que mudar skill, plugin ou o uso por projeto termina regenerando o guia em Word (12.6). O `.docx` fica fora
  do git; cada PC o regenera com o script.

**Decisões que ficaram para as fases:** o conteúdo do ADR-0001 (minientrevista no F1a); o que a IA faz dentro do app
(`app\ia\`, F5a); o grill de cada projeto novo (N1-N5); o que corrigir da R0 (F5a); mudar ou não o dado do censo e do
HC de lugar (F6, F7).

## As fases

Cada janela fecha pelo que vier primeiro: fim da fase, ~150 mil tokens ou troca de modelo (Q9) — por isso nenhuma fase
troca de modelo no meio; trocar o esforço no meio pode (não quebra o cache). Commit por caminho explícito; `git push`
livre no fim de fase com testes verdes, depois de `git log origin/main..` (Q10). Subagente com `model: sonnet` roda no
Sonnet 5.5 (conferido nesta janela); a armadilha do Sonnet 5 é só `/model sonnet` e `--model sonnet`.

| fase | onde | modelo · esforço | por quê | sinal para subir |
|---|---|---|---|---|
| R0 revisão de front | `desosp-app` | Opus 5.5 · medium; subagentes `sonnet` | julgamento com prova; o erro aparece na tela | achados genéricos sem prova → high |
| F1a privacidade, isolamento, git | `claude-kit` | Opus 5.5 · high → medium | regra de privacidade errada aparece tarde e em todo projeto | contradiz posição escrita dele → xhigh (com motivo) |
| R1 objetivo, medição, recursos (pedido de 06/10, depois do F1a) | `claude-kit` | Opus 5.5 · high → medium; pesquisa por subagentes `sonnet` | redefine o objetivo das fases seguintes; erro aqui se espalha | contradiz posição escrita dele → xhigh (com motivo) |
| F1b marketplace | `claude-kit` | Opus 5.5 · medium | reestruturação conferida por comando | skill some ou duplica sem ser notado → high |
| F2a skills do kit | `claude-kit` | Opus 5.5 · high | instrução errada guia toda sessão futura | perguntas de controle falham duas vezes → xhigh |
| F2b ganchos, medição, pastas de teste | `claude-kit` | Opus 5.5 · medium | conferido por teste com JSON | teste de gancho falha sem causa entendida → high |
| F3a o laço | `teste-fluxo` | Opus 5.5 · medium; fases `claude-sonnet-5-5` · medium | critérios escritos | critério falha sem causa entendida → high |
| F3b ferramentas | `teste-ferramentas` | Opus 5.5 · medium; executores Sonnet 5.5 · medium; revisor cego subagente `opus` | medição | números incoerentes entre execuções → high |
| F3c ajustes | `claude-kit` | Opus 5.5 · medium | aplicar resultados medidos | ajuste quebra critério que passava → high |
| F5a migração do app | `desosp-app` | Opus 5.5 · high | estado e regras: erro silencioso | contradiz regra escrita → xhigh |
| F5b correções da R0 | `desosp-app` | Opus 5.5 · medium; implementadores `sonnet` (SDD) | o navegador e o axe pegam o erro | a 2ª tentativa no mesmo teste falha → high |
| F5c porta de leitura | `desosp-app` | Opus 5.5 · medium | campo a mais é erro silencioso; teste com dado sintético prova | teste de "nenhum campo a mais" falha → high |
| F6 kernel | `desosp-censo` | Opus 5.5 · high; agentes do Workflow em Sonnet 5.5 · medium | regras com erro silencioso em dado vivo | casos de borda escapam → xhigh |
| F7 planilha | `desosp-hc` | Opus 5.5 · medium; comandos por subagentes `sonnet` | migração com testes | comando migrado diverge do original → high |
| F8 desktop | desktop | Opus 5.5 · medium | repetir o que o notebook provou | desktop diverge sem causa clara → high |
| Fd Drive | desktop, `G:\Meu Drive` | Sonnet 5.5 (da lista) · medium | classificar e mover com aprovação; reversível | mais de 1 em 10 classificado errado → Opus 5.5 · medium |
| F9 guia e retro | `claude-kit` | Opus 5.5 · medium | consolidar e medir | retrospectiva genérica, sem números → high |
| N1-N5 grill e montagem | cada projeto | Opus 5.5 · high (grill) → o que o plano do projeto disser | planejar | plano raso → xhigh |

**F0 — o Ettore (agora).** Feito: política do safety-net, as 5 skills do claude.ai, o gatilho do ultracode, a pasta
`pesquisa-clinica\fontes\artigos` (os artigos chegam quando ele for usar). Falta: desligar `llm-council` e
`prompt-master` no claude.ai (Q26); conferir a opção de treino em claude.ai/settings/data-privacy-controls; deixar a
pasta `IA` do Drive como "Restrito"; abrir a R0 (com a linha extra dos subagentes, se já estiver aberta).

**R0 — revisão de front do app (já, em paralelo ao F1a).** Só leitura; relatório priorizado em `docs\` (e capturas com
dado sintético, se úteis). Portão: o `git diff --stat` mostra só o relatório e as capturas; os 10 primeiros achados com
prova. As correções que o Ettore escolher (no F5a) viram o F5b.

**F1a — privacidade, isolamento e o kit no git.**
- Pré-condição: a janela das cores fechou (ela edita `skills\uso-do-claude\organizar-projetos\`, dentro do kit); se
  não, o 1º commit exclui essa pasta e ela entra depois.
- Check-in de F0 (uma pergunta). Q27 gravada pelo `pastas.py` se a janela das cores fechou (conferir antes o `--help`).
- ADR-0001 privacidade (`decisoes\adr\0001-privacidade.md`), por minientrevista: o que o Claude vê por domínio; dado de
  paciente em repositório privado; claude-mem e Headroom com dado; conectores do claude.ai com dado do trabalho;
  arquivo do trabalho na conta pessoal do Google; `deny` das pastas de dado de dentro do censo, do HC e do app. Os
  pontos que não dependem dele, ditos uma vez: política do hospital, LGPD art. 11 e art. 33, a opção de treino.
  Registra a Q22. Aplica agora no kit e no CLAUDE.md pessoal (com o ponteiro do ADR-0002); o resto vira tarefa do F5a,
  F6 e F7.
- ADR-0002 isolamento (Q16); `desosp-app-backups/` no `C:\CLAUDE-PROJETOS\.ignore`.
- `.gitignore` (fora: `_do_desktop\`, zips, retratos com nomes de arquivo dos projetos, caches, o `.docx` gerado,
  `desktop.ini`, `.vscode\`); varredura antes do 1º commit (reaproveitar o pre-commit de privacidade do `desosp-hc`);
  `git init`; repositório privado `HirugaX/claude-kit` (`gh`, se houver; senão o Ettore cria no site); push; `caixa\`
  (Q12).
- Portão: ADRs aprovados; varredura sem achado; `git status` limpo; push feito; hardlink do CLAUDE.md pessoal conferido.

**F1b — o kit como marketplace.**
- Teste com um plugin (`planejamento` com `grill-me` e `grilling` copiadas) numa pasta de rascunho: ligar e desligar,
  `/grill-me` curto, edição valendo com `/reload-plugins`, nenhuma cópia em `~\.claude\plugins\cache`.
- Grupos: `nucleo` (nosso; todo projeto), `kit` (nosso; só no kit), `planejamento` (terceiros; todo projeto),
  `engenharia` (terceiros; projetos de código). Tabela skill → grupo mostrada antes; `origem.json` nos de terceiros.
- Migração grupo a grupo (plugin → backup → remove a junção → confere). Ao mover o `organizar-projetos` (só com a
  janela das cores fechada), o caminho do gancho das cores no `~\.claude\settings.json` muda junto (com backup), e o
  portão confere que ele ainda dispara.
- `config\plugins.json` (marketplaces e plugins de fora, escopo de cada um); `scripts\instalar_kit.py` (substitui o
  `ligar_claude.py`: marketplace do kit, plugins de fora, `--verificar`, e imprime o comando da política do safety-net
  para o Ettore); `scripts\atualizar_terceiros.py`.
- CLAUDE.md pessoal (a regra nova); `LEIA-ME.md` do kit (estrutura, instalação nos dois PCs, guia e gerador);
  `COMO_OPERAR.md` só com a parte "até o F3" (a parte "depois do F3" entra no F3c, se o laço passar); guia em Word com a
  operação como 1ª parte; aviso no guia do Claude Docs (Q28).
- R1: na abertura, conferir se o Remote Control ligou sozinho (painel e terminal); nas paradas, um `PushNotification`
  "claude-kit · F1b · precisa de você"; o session-report sai do escopo de usuário (backup antes) e o `config\plugins.json`
  o registra só nas pastas de teste (Q40). O resto como está (Q46).
- Portão: `instalar_kit.py --verificar`; ligar e desligar `engenharia` muda a lista; `/grill-me` curto; nenhuma junção
  sobrando; o gancho das cores dispara; guia regenerado.
- **Feito em 07/10** (decisões do grill de 07/10 em `docs\ESTADO.md`):
  - os grupos `nucleo` (2), `planejamento` (12) e `engenharia` (14);
  - a `engenharia` **nunca** no escopo de usuário: cada projeto de código a liga na sua fase, e até lá fica sem ela;
  - o gancho das cores virou gancho do plugin `nucleo` (`hooks\hooks.json`);
  - o CLAUDE.md pessoal virou import (`@C:/CLAUDE-PROJETOS/claude-kit/CLAUDE.md`), sem hardlink;
  - o plugin `kit` nasce no F2a.

**F2 — as peças do kit — dividido em F2a e F2b em 07/10** (o F2 tinha 13 itens e ganhou a quebra do
`organizar-projetos`; o próprio prompt já trocava de esforço no meio). **F2a — as skills** (Opus high): a quebra da
`uso-do-claude` e do `organizar-projetos` (3 skills só `/` no plugin `kit`: `organizar-projetos`, `cores-das-pastas`,
`icones`; os scripts das cores ficam onde o gancho do `nucleo` os acha), a `recursos-do-projeto` enxuta, o SDD, os
modelos, o texto da fila, do aviso, das janelas e do esforço dos subagentes nas skills, as perguntas de controle e o
guia. **F2b — ganchos, settings, medição, pastas de teste** (Opus medium): os ganchos (inclusive os da fila), a
statusline, a medição e o balanço (a sessão do balanço roda na janela da raiz, decisão de 07/10) e as pastas
`teste-fluxo` e `teste-ferramentas`. O conteúdo de cada item segue abaixo.
- Quebra da `uso-do-claude` (núcleo ≤ 150 linhas + `modelo-e-esforco`, `fechar-janela`, `pesquisa`, `orquestrar`; o
  `reference.md` fica como consulta; o `medir_uso.py` vai para `scripts\` e as referências mudam). O núcleo traz os
  pontos de checagem de recursos novos (Q14) e a exceção da Q15. O `fechar-janela` cobre `ESTADO.md` reescrito,
  `PROXIMO.md`, caixa, resumo com "Sinais", fechar por fim de fase, ~150 mil ou troca de modelo, push pela Q10, e o
  lançamento por `--bg` desligado em `config\fluxo.json` até o F3c. A `orquestrar` traz o roteamento da Q18, os 3
  papéis, modelo por papel, as paradas da Q10, o teto 10 (acima: estimativa + "sim") e o cache de subagente.
- `recursos-do-projeto` enxuta (Q20). SDD num plugin de terceiros (cabeçalhos "Task N"; modelo fixo por despacho; o
  `ESTADO.md` continua dono do estado).
- Modelos de `ESTADO.md`, `PROXIMO.md`, ADR e `GLOSSARY.md`.
- Ganchos no `nucleo` (base: `desosp-app\.claude\hooks\abertura.py`), nas duas camadas da Ficha, item 4.
- Settings, com backup e a outra janela fechada: statusline, `showClearContextOnPlanAccept: true`, limpeza das 4
  permissões com caminho que não existe mais.
- Medição (Q39, Q42): `scripts\medir_semana.py` completo a partir do protótipo da R1 (planilha `metricas\uso.xlsx` com
  openpyxl, fora do git; `metricas\BALANCO.md`); o gancho de abertura roda a medição se a última linha tem mais de 7 dias
  (sem imprimir) e avisa o balanço vencido (15 dias); a statusline anota o % de 5 h e o semanal num arquivo local.
- Fila e execução largada (Q35, Q36, Q44): modelo de `PERGUNTAS.md`; o protocolo no `fechar-janela` e no `orquestrar`;
  os ganchos `PermissionRequest` e `PreToolUse` em `AskUserQuestion` (só adiar, nunca escolher); o `Stop` aceita fechar
  com a fila gravada; o modelo de `PROXIMO.md` com "Decisões pré-aprovadas", "Sempre me pergunte" e a linha `/goal`; a
  rodada de contingências na nossa skill (a `grilling` não se mexe).
- Aviso (Q43, Q48): a regra do `PushNotification` (três casos; texto da D8 do ADR-0001).
- Janelas e sonda (Q37, Q45), na `orquestrar`: um escritor por projeto ou worktree; o % de 5 h antes de abrir outra
  janela; a sonda por arquivo e o "pronto" ao vivo só no mesmo domínio, se o F3a mostrar ganho.
- Esforço dos subagentes: na semana de 29/09, 1.197 chamadas do Sonnet 5.5 em `max`, quase todas em subagentes;
  conferir se o subagente herda o esforço da janela e fixá-lo por papel.
- No fim, cria `C:\CLAUDE-PROJETOS\teste-fluxo\` e `teste-ferramentas\` vazias, com `git init` (o gancho das cores vai
  perguntar a cor: `sem-cor`); nas duas, o session-report ligado no `.claude\settings.json`, um gancho que barra o
  `analyze-sessions` sem `--dir` e o HTML no `.gitignore` (Q40).
- Portão: `testar_ganchos.py` verde (com os ganchos da fila); `perguntas_controle.py` (~10 perguntas) bate; núcleo ≤ 150
  linhas; custo fixo menor (número do `/context`); o `medir_semana.py` reproduz a linha de 29/09 do
  `metricas\uso-semanal.csv` e gera a planilha; as duas pastas de teste criadas; guia regenerado.

**F3a — o laço (`teste-fluxo`, dado sintético).** Critérios: aprovar plano limpando o contexto (painel e terminal);
fase 1 → `ESTADO.md` + `PROXIMO.md` → fase 2 em Sonnet 5.5 lançada de dois jeitos — por `--bg` e por sessão interativa
numa aba nova —, anotando se começa sozinha, se o Remote Control liga, se o aviso chega ao celular e se ela retoma depois
do limite de uso; a fila (duas decisões plantadas vão para o `PERGUNTAS.md` e a fase segue com o resto); `/goal` "portão
ou fila" numa sessão `--bg`; a sessão `--bg` trabalha em worktree e o resultado volta ao ramo principal; portão `Stop`;
guarda de escrita em `teste-fluxo-dados\`; reserva `/clear` + gancho; `/model sonnet` barrado; statusline; as mesmas 3
fases em série e em paralelo (tokens e tempo: a condição da Q37); a sonda (duas fases que precisam da mesma pesquisa:
cada uma sozinha × uma sonda que serve às duas; fica só se poupar tempo ou tokens, Q45); medição com o
`medir_semana.py`. Portão: `RESULTADO.md` com prova por critério; retornos e maior trecho sem ele medidos e a fila
funcionando; o resultado salvo em `claude-kit\pesquisas\` (sem mexer no `INDICE.md`).

**F3b — as ferramentas (`teste-ferramentas`, dado sintético, de preferência no terminal).** Disputa SDD × OMC × sem
orquestrador × sem orquestrador com a andrej-karpathy-skills por `--plugin-dir` (Q38) (plano de 5 tarefas; executores em
Sonnet 5.5 · medium; revisor cego `opus`, que conta também as mudanças fora do pedido e as paradas à toa; uma decisão e
um comando destrutivo plantados); Headroom; claude-mem; `claude-code-setup` por `--plugin-dir` só no projeto sintético
(no app, vai para o F5a); medição com o `medir_semana.py` (o session-report só com `--dir` na pasta das transcrições
deste projeto, Q40). Portão: `RESULTADO.md` com números e veredito por ferramenta (a andrej-karpathy-skills pelo critério
fixado na R1); desinstalação conferida das que saírem; o resultado salvo em `claude-kit\pesquisas\` (sem mexer no
`INDICE.md`).

**F3c — ajustes no kit.** As duas linhas no `INDICE.md`; `orquestrar` aponta o vencedor; forma final da descoberta
(Q20); onde entram claude-mem, Headroom e a andrej-karpathy-skills (pelo critério da Q38); a sonda e as mensagens entre
sessões pelo critério da Q45; corrigir o que falhou no F3a e repetir só esse critério; se o laço passou, o jeito de lançar
fases que o F3a mostrou melhor (`--bg` ou aba interativa), ligar o lançamento (`config\fluxo.json`) e o do balanço
quinzenal, e completar o `COMO_OPERAR.md` (fila, aviso no celular, balanço, janelas). Portão: os critérios que falharam
passam; INDICE com as duas linhas; guia regenerado.

**F5a — migração do app (principal).** Proteção de dado primeiro (as tarefas do app nas tabelas do ADR-0001 e do
ADR-0002: `deny` interno da D6, conectores da D4, pre-commit de nomes, CLAUDE.md pela D1); `docs\ESTADO.md` a partir do `HANDOFF_APP.md` (congelado
em `docs\historico\`, lido por busca); CLAUDE.md < 200 linhas com "Skills deste projeto"; `enabledPlugins`; o
`abertura.py` dá lugar ao gancho do `nucleo` (nada dele se perde); `docs\adr\` + `GLOSSARY.md`; memória sem status;
`claude-code-setup` só leitura, comparado com o `RECURSOS_CLAUDE_DESOSP.md` (as recusas de Context7, Playwright MCP e
GitHub MCP explicadas); a decisão do Ettore sobre o que a IA faz em `app\ia\` (ADR do app); a escolha das correções da
R0 e o `PROXIMO.md` do F5b. Portão: CLAUDE.md < 200 (`wc -l`); `ctx0` ≤ 40 mil; suíte verde (nenhum código mudou);
`ESTADO.md` ≤ 1 página; guia regenerado.

**F5b — correções da R0.** As tarefas escolhidas, pelo SDD se forem 4 ou mais; `revisar-tela` em cada tela mexida.
Portão: suíte de navegador + axe verdes; `revisar-tela` com prova por tela; aceite de 5 minutos do Ettore; uma fase
lançada por `--bg` de verdade (se o F3c ligou).

**F5c — porta de leitura (depois do N1, antes do N2).** Comando só de leitura em `app\ia\` que devolve o pseudônimo
(ADR-0001 D1) e os campos mínimos que a comunicação precisa, para arquivo local, nunca para o terminal. Portão: testes com o banco sintético, inclusive o
de "nenhum campo a mais"; ADR do app atualizado.

**F6 — kernel.** Proteção de dado primeiro (as tarefas do censo nas tabelas do ADR-0001 e do ADR-0002: `deny` e
`.ignore` do bruto pela D6, os scripts da rodada continuam lendo; conectores da D4; pre-commit de nomes; pseudônimo nas
saídas). Depois, o mesmo do F5a; desenvolvimento separado da operação da rodada (a skill `rodada`
como rotina aprovada, Q21); auditoria das 27 regras e das 8 sobre o `data_merge.py` por Workflow (só regras e código,
nunca dado); `MEMORY.md` sem a linha de 7,4 mil caracteres; Cartographer × `improve-codebase-architecture`; o lugar do
dado (o kernel vai ser aposentado) decidido pelo Ettore. Portão: CLAUDE.md < 200; `ctx0` ≤ 50 mil; `MEMORY.md` ≤ 200
linhas e sem status; suíte verde; uma rodada real sem passo manual a mais; guia regenerado.

**F7 — planilha HC.** Proteção de dado primeiro (as tarefas do HC nas tabelas do ADR-0001 e do ADR-0002; a memória
"console sem linha de paciente" pela D1); o mesmo do F5a; os 12 comandos viram skills? (Workflow candidato, só código); `/fechar-rodada`,
`/consolidar` e `/nova-versao` só por `/`; o lugar do dado. Portão: CLAUDE.md < 200; `ctx0` ≤ 45 mil; suíte verde; os 12
comandos funcionam; guia regenerado.

**F8 — desktop.** Janela no kit clonado prepara; cada projeto do desktop em janela própria. Retomar o que o Ettore
começou em 06/10 (`_do_desktop\`, `caixa\`); `instalar_kit.py` (o Ettore aplica a política do safety-net);
`organizar-projetos` lá (pasta-mãe, ícones); GitHub privado de Folha/RH e Acolhimento, com varredura; domínios e prefixos
do desktop (Q16); fluxo do DASH, Folha/RH e Acolhimento (prompts 10-12 do Workbench como checklist); `fechar-janela`
do DASH unificada; Context7 no DASH; o Apps Script que grava na raiz do Drive passa a gravar em `IA\<projeto>`. Portão:
`instalar_kit.py --verificar` no desktop; cada projeto com CLAUDE.md < 200, `ESTADO.md` e `enabledPlugins`; guia
regenerado.

**Fd — o Drive (desktop, quando estiver lá).** Tudo de IA em `IA\<projeto>` (os nomes das pastas do `CLAUDE-PROJETOS`),
o sem-dono em `IA\00-entrada`; o arquivo pessoal que não é de IA fica onde está; a regra "gravar só em `IA\<projeto>`"
para os escritores. Portão: tabela aprovada; raiz sem arquivo de IA solto; `IA\00-entrada\LEIA-ME.md` com o registro.

**F9 — guia e retrospectiva.** Guia final; `/retro` do redesenho com os números do `metricas\uso-semanal.csv` e dos
balanços contra a linha de base; limpar as chaves velhas da memória automática (`C--DESOSP`…, 10 arquivos divergentes),
com a lista mostrada antes; `cleanupPeriodDays` de volta a 30 (Q41, backup antes); retrospectiva salva em `pesquisas\`. Portão: guia regenerado; retrospectiva com números salva; memória velha limpa ou a lista do que ficou.

**Frente 2 (depois do F5b).** Cada projeto: grill próprio → `recursos-do-projeto` → plano → montagem → GitHub privado;
prefixo e pasta de dado pelo ADR-0002. Até o grill, o material extraído do chat do agente de produtividade fica em
`C:\CLAUDE-PROJETOS\pessoal-produtividade\fontes\`, sem janela.
- **N1 `estudo-residencia`:** acervo do cursinho; `/ingerir`, `/resumo`, `/quiz`, `/explica-de-novo`, `/flashcards`,
  `/simular`; Anki por TSV; simulações interativas (Artifacts); diagramas e mapas mentais para ele; skills e estilos
  `learning`/`explanatory` para o vibe coder aprender código; claude-mem se passou no F3b.
- **N2 `desosp-comunicacao`:** `desosp-comunicacao-dados\` com `deny` + safety-net antes de os e-mails chegarem; um
  script que faz cópias do acervo com marcadores no lugar dos identificadores e outro que preenche o texto final;
  `/email` e `/whatsapp`; porta de leitura do F5c; `stop-slop`, `internal-comms`; o Ettore confere a política do
  hospital para tirar os e-mails do PC do trabalho. O Claude nunca envia.
- **N3 `pessoal-organizacao` e N4 `pessoal-produtividade`:** o grill do N3 começa separando o escopo dos dois (a 12.2 e a
  12.5 se sobrepõem); migrar do claude.ai (instruções, arquivos, conversas-chave); Notion e agenda só aqui; base
  `pesquisas\2026-10-04_notion-filtros-e-visoes.md` e `2026-10-06_estudo-anki-e-produtividade.md`.
- **N5 `pesquisa-clinica` (por último):** `paper-lookup`, `scientific-critical-thinking`, `pergunta-clinica`; PubMed em
  escopo de projeto; o fluxo do OpenEvidence (ele cola a pergunta e as referências; o Claude confere no PubMed; nada do
  OpenEvidence no git); a memória das pesquisas (`INDICE.md`, `REGISTRO.md`, uma nota por pergunta,
  `referencias.csv`); nunca dado de paciente; o grill decide se os PDFs vão para o git.
- Portão de cada N: grill, ficha e plano aprovados; montagem inicial com push e varredura limpa; guia regenerado.

## Verificação de ponta a ponta

A régua da R1 (Q34, Q39) vem primeiro; as metas dela são conferidas nas semanas depois do F5b. Base: a semana de 29/09 a
05/10 no `metricas\uso-semanal.csv`.

| o que | antes | meta | como medir |
|---|---|---|---|
| retornos (mensagem dele depois de mais de 30 min com a sessão parada) | 29 na semana | metade | `scripts\medir_semana.py` |
| sentadas (mensagens dele em blocos com até 20 min entre elas) | 50 blocos, 613 min | metade dos blocos | idem |
| maior trecho do Claude sem ele (todas as janelas) | 92 min (mediana de 3 min) | o dobro | idem |
| janelas trabalhando ao mesmo tempo (máximo por dia) | 4 | sobe quando há trabalho independente, com tokens iguais ou menores que em série (F3a) | idem |
| contexto mediano por chamada | 307 mil (199-317 mil em 05/10) | ≤ 120 mil | idem |
| `ctx0` app / kernel / planilha | 58 / 66 / 55 mil | ≤ 40 / 50 / 45 mil | idem |
| CLAUDE.md app / kernel / planilha | 354 / 430 / 226 linhas | < 200 | `wc -l` |
| estado | handoffs de 575 e 376 KB | `ESTADO.md` ≤ 1 página | tamanho |
| chamadas no Sonnet 5 por engano / no Opus 5 (rebaixamento) | 296 / 77 na semana | 0 / 0 | `scripts\medir_semana.py` |
| gestos manuais por janela (secundária) | ~7 (4 de transporte) | ≤ 2 depois do F3 | contagem no F3a e no F5b |
| qualidade | — | suítes verdes; correções da R0 aceitas; `/retro` sem retrabalho atribuído ao fluxo | testes; F9 |

## Prompts das janelas

Cada janela confere e ajusta o prompt seguinte antes de entregá-lo (lição 7 de
`pesquisas\2026-10-05_fluxo-atual-dos-projetos.md`). Depois do F3c, se o laço passar, o prompt vai no `docs\PROXIMO.md`
e a fase é lançada por `--bg`.

### R0 — revisão de front (entregue em 06/10; a 1ª linha de "Limites" foi acrescentada depois; em 07/10, a linha da engenharia no "Antes")

```
Opus 5.5 · /effort medium — revisão de tela é julgamento com prova, e o erro aparece na própria tela (barato de descobrir); suba para /effort high se os achados vierem genéricos, sem arquivo:linha e sem prova.

Janela aberta em C:\CLAUDE-PROJETOS\desosp-app (só este projeto). Antes: git status sem arquivo de outra janela; nenhuma outra janela de implementação aberta no app. Desde o F1b (07/10) a engenharia (web-design-guidelines, prototype, tdd...) só liga por projeto: se /web-design-guidelines não aparecer ao digitar /, rode uma vez, neste projeto, claude plugin enable engenharia@claude-kit --scope local e abra uma janela nova (grava em .claude\settings.local.json, que não entra no commit; o F5a passa a ligação para o settings versionado).

## Contexto
O Ettore pediu uma revisão do front do app com as skills instaladas hoje. É SÓ LEITURA: sai um relatório priorizado; nenhuma correção sem o "sim" dele. As correções que ele aprovar viram a 1ª fase do app no fluxo novo (plano em C:\CLAUDE-PROJETOS\claude-kit\decisoes\2026-10-06_plano-fluxo.md, depois de aprovado).

## O que fazer
1. Inventário: as telas (rotas) e os arquivos de cada uma (templates, CSS, JS), por subagente Explore com model: sonnet.
2. As réguas, nesta ordem: a skill revisar-tela (lista de conferência com a prova de cada ponto); o PROJETO_FRONT §6.7 (o aceite de cinco minutos); a skill web-design-guidelines (Web Interface Guidelines da Vercel); para cor e contraste, C:\CLAUDE-PROJETOS\claude-kit\pesquisas\2026-09-30_paleta-clinica-evidencias.md; o frontend-design só para dizer a direção onde a hierarquia falha, sem redesenhar.
3. Comando antes de opinião: rode a suíte de navegador do app (com o axe-core de tests\vendor) e use cada falha como prova. O que ela não cobre (1366 px, foco pelo teclado, impressão, estados vazio/erro/antigo/parcial, tabelas longas), confira no navegador com o dado sintético da suíte.
4. Divida as telas em 3 a 5 grupos; um subagente (model: sonnet) por grupo aplica a revisar-tela e a web-design-guidelines e devolve cada achado assim: tela · problema · régua violada (item da revisar-tela ou regra da WIG) · prova (arquivo:linha, teste que falhou, ou captura com dado sintético) · gravidade (bloqueia o trabalho / atrapalha / polimento) · correção proposta · tamanho (P/M/G). Você junta, tira repetidos, confere por amostra um achado de cada subagente e prioriza.
5. Grave o relatório em docs\ (pela convenção do app; sem convenção, docs\revisoes\<data de hoje, AAAA-MM-DD>_revisao-front.md): os 10 primeiros; a tabela completa; o que ficou sem conferir e por quê; as fases de correção propostas (o que se corrige junto), com modelo e esforço sugeridos; onde a correção pede escolha visual, sugira protótipo (skill prototype).

## Limites
- Repasse a cada subagente os Limites de dado real deste prompt: nunca abrir workspace_dev\, docs\para_o_app\, desosp-app-dados nem desosp-app-backups.
- Nenhum template, CSS, JS ou teste alterado. Grava só o relatório (e capturas com dado sintético, se úteis).
- Nunca abrir dado real: desosp-app-dados, desosp-app-backups, workspace_dev\ (cópia do dado do Ettore), docs\para_o_app\ (nomes reais). O app roda só com o banco de teste da suíte; se não houver modo sintético, pare e pergunte. Nenhum nome de paciente no relatório nem em captura.
- Não ler o HANDOFF_APP.md inteiro (575 KB): busca por palavra, se precisar.
- Não mexer no claude-kit, no ~\.claude\settings.json nem nas cores das pastas (outras janelas trabalham neles; o /effort digitado grava no settings, e isso pode).
- Commit só do relatório, por caminho explícito; antes do push, git log origin/main.. (regra do projeto).

## Ao fechar
Resumo no chat: os 10 achados principais; as fases de correção propostas; a linha "Sinais de insuficiência do modelo: nenhum" (ou quais, com o exemplo). Não escreva o prompt da fase de correção: ela é o F5b do plano, depois que o Ettore escolher o que corrigir (no F5a).
```

### F1a — privacidade, isolamento e o kit no git

```
Opus 5.5 · /effort high — a 1ª parte decide as regras de privacidade de todos os projetos (erro descoberto tarde e em todo lugar); depois dos dois ADRs, digite /effort medium para o git e a varredura (conferidos por comando).

Janela no painel do VS Code aberta em C:\CLAUDE-PROJETOS\claude-kit. A revisão de front (R0) pode estar rodando no desosp-app: não mexa lá.

## Contexto
Plano aprovado: decisoes\2026-10-06_plano-fluxo.md — leia "A cadeia", "Como você opera", "Decisões da rodada 3", a "Ficha" e o bloco F1a. Do registro decisoes\2026-10-06_entrevista-fluxo.md, leia §5 (Q1-Q15), §9 (leis), §12.4 (isolamento) e §12.7 (posições de privacidade). Memória: recursos-antes-de-recusa (risco uma vez + contorno; a decisão é dele).

## O que fazer
1. Check-in numa pergunta só: desligou llm-council e prompt-master no claude.ai? conferiu a opção de treino (claude.ai/settings/data-privacy-controls)? a pasta IA do Drive está "Restrito"? a janela das cores fechou? Se fechou, grave a cor da pesquisa-clinica (raiz projeto-ia; fontes = eu-forneco-fontes) pelo pastas.py do organizar-projetos (veja antes o --help).
2. ADR-0001 privacidade (decisoes\adr\0001-privacidade.md) por minientrevista, uma rodada no formato da skill grilling (numeradas, com recomendação; cada pergunta com o problema, as opções e o que muda): o que o Claude pode ver em cada domínio (identificador; conteúdo clínico); dado de paciente em repositório privado; claude-mem e Headroom com dado de paciente; conectores do claude.ai com dado do trabalho; arquivo do trabalho na conta pessoal do Google; deny das pastas de dado que moram dentro do censo, do HC e do app. Os pontos que não dependem dele, ditos uma vez: política do hospital (dono do dado), LGPD art. 11 e art. 33, a opção de treino do claude.ai. Contorno antes de recusa. Registre a Q22 (marcadores na comunicação). Liste as regras que mudam e onde (CLAUDE.md pessoal; CLAUDE.md dos projetos; memórias "console sem linha de paciente" e "nome de paciente nunca em arquivo versionado"); aplique agora só as do kit e do CLAUDE.md pessoal, com o ponteiro do ADR-0002 (hardlink: gravar no próprio arquivo e conferir com fsutil hardlink list); as dos projetos viram tarefa do F5a, F6 e F7.
3. ADR-0002 isolamento (decisoes\adr\0002-isolamento.md): a Q16 inteira (domínios e prefixos, o que cruza, canais, <projeto>-dados, uma janela = um projeto, disableClaudeAiConnectors nos projetos que não usam conector). Acrescente desosp-app-backups/ ao C:\CLAUDE-PROJETOS\.ignore.
4. /effort medium. Git do kit — só com a janela das cores fechada; se não fechou, o 1º commit exclui skills\uso-do-claude\organizar-projetos\: .gitignore (fora: _do_desktop\, zips, retratos com nomes de arquivo dos projetos, caches, o GUIA_DAS_SKILLS.docx gerado, desktop.ini, .vscode\); varredura antes do 1º commit (segredos, CPF, CNS, telefone, caminhos de pasta de dado) — reaproveite o pre-commit de privacidade do desosp-hc se servir; git init; commits por caminho explícito; repositório privado HirugaX/claude-kit (gh, se estiver instalado e logado; senão, o Ettore cria no site e você liga o remote); push.
5. caixa\ (Q12) no formato das caixas dos projetos, com LEIA-ME.

## Limites
- Nada de reestruturar skills nem de mexer em plugins (é o F1b). Não editar o ~\.claude\settings.json (o /effort que o Ettore digita grava lá, e isso pode).
- Nenhuma regra de projeto alterada agora (só registrada como tarefa das fases deles).
- Nunca dado de paciente no kit, nos ADRs ou no resumo.

## Ao fechar
Portão: ADRs aprovados; varredura sem achado; git status limpo; push feito; hardlink conferido. Grave o ESTADO.md do kit (≤ 1 página). Resumo: os dois ADRs em 5 linhas, o link do repositório, o resultado da varredura e "Sinais de insuficiência do modelo: nenhum" (ou quais, com o exemplo). Confira e ajuste o prompt do F1b neste plano e entregue-o (modelo e /effort na 1ª linha).
```

### R1 — o objetivo, a medição e a última varredura de recursos (pedido do Ettore ao fechar o F1a, 06/10) — feita em 06/10

```
Opus 5.5 · /effort high — esta janela revê o objetivo do fluxo e decide o que as fases seguintes medem e instalam (erro aqui se espalha por todas); a pesquisa vai para subagentes sonnet; depois do grill, digite /effort medium para escrever.

Janela no painel aberta em C:\CLAUDE-PROJETOS\claude-kit. Antes: git pull --ff-only; git status limpo; leia docs\ESTADO.md e caixa\INDICE.md. Nenhuma outra janela no kit (o F1b vem depois desta).

## Contexto
O Ettore, ao fechar o F1a (06/10), nas palavras dele: "meu problema nem é tanto ser office boy de prompt, mas precisar dar atenção integral ao processo. Gostaria de o largar trabalhando por um tempo maior. Prefiro sentar e ser fritado por perguntas e rodar diversas janelas ao mesmo tempo, pois o tempo foi pontual, e não picado de ter que voltar aqui o tempo todo e resolver as coisas — mantendo qualidade, economia de tokens e o padrão. Foi esse o objetivo certo?" Pediu também: avaliar a andrej-karpathy-skills ("teria uso em todo o processo e potencial para economizar bastante; testar por um tempo e aferir"); um modo de aferir de fato, semana a semana, o uso de tokens e as interações dele; e uma última varredura de skills e recursos, com a skill que busca recursos (find-skills).
Leia: decisoes\2026-10-06_plano-fluxo.md ("A cadeia", "Como você opera", "Decisões da rodada 3", a Ficha, os blocos F2, F3a, F3b, F3c e a "Verificação de ponta a ponta"); docs\2026-10-06_o-que-mudou-e-como-operar.md (Parte 2); decisoes\adr\0001-privacidade.md e 0002-isolamento.md; pesquisas\INDICE.md antes de qualquer pesquisa (a biblioteca já tem o gist "LLM wiki" de Karpathy, que é outra coisa).

## O que fazer
1. Fatos primeiro (subagentes model: sonnet, em paralelo; cada um devolve fatos com fonte e salva em pesquisas\ no formato do INDICE):
   a. andrej-karpathy-skills: o repositório certo (autor, licença, data, estrelas), o que contém, como instala (plugin, skill, trecho de CLAUDE.md), quantos tokens fixos custa por sessão, a evidência de economia que alega (medida ou opinião), conflito com as nossas regras (CLAUDE.md pessoal, writing-for-agents, as do Matt) e com o comportamento do Opus 5.5.
   b. Medição: o que o medir_uso.py (skills\uso-do-claude\medir_uso.py; --sessoes, --desde) e o plugin session-report (já instalado) já medem; o que falta para uma linha por semana com: tokens por sessão (entrada, cache, saída), contexto mediano por chamada, ctx0 por projeto, mensagens dele por fase, "retornos" (mensagem dele depois de mais de 30 min parado) e o maior trecho trabalhando sem ele (a métrica do objetivo real), chamadas no Sonnet 5. Confira o cleanupPeriodDays (o Claude Code apaga transcrições antigas; o padrão era 30 dias): sem elas não há linha de base.
   c. Varredura final (find-skills e a internet): recursos para o objetivo real — execução longa sem supervisão, perguntas juntadas num só momento, várias janelas em paralelo (worktrees, --bg), aviso no celular quando uma fase precisa dele, observabilidade de tokens (OpenTelemetry do Claude Code, ccusage e parecidos). Só o que NÃO está na Ficha (AGORA, QUANDO, NÃO); cada um com custo, risco, Windows e veredito. Nada instalado.
2. O objetivo, por grill (skill grilling; uma ou duas rodadas, numeradas, com recomendação; cada pergunta com o problema, as opções e o que muda): o objetivo reescrito ("atenção concentrada: perguntas de uma vez, execução longa sem ele, várias janelas, com qualidade, economia e o padrão") e o confronto com o plano — Q2, Q9, Q10 (parada que bloqueia × pergunta guardada numa fila enquanto a fase segue com o que não depende dela), o limite de duas janelas (× limite por posse de arquivo), o aviso no celular, o /goal nas fases longas, as decisões pré-aprovadas no PROXIMO.md (como a Q21 faz com escrita em dado real). E as decisões da andrej-karpathy-skills (onde e como testar) e da medição.
3. Linha de base já: rode a medição dos dias que ainda existem e grave os números (só números) em claude-kit\metricas\ (CSV). Se o cleanupPeriodDays estiver baixo, proponha o valor ao Ettore e, com o "sim", grave no ~\.claude\settings.json (backup antes).
4. Grave: decisoes\2026-10-0X_R1-objetivo-medicao-recursos.md (as decisões e o porquê); as linhas novas do pesquisas\INDICE.md; no plano, só o que o Ettore aprovar (Q2, Q9, Q10, a Ficha, os blocos e prompts do F1b, F2, F3a e F3b — a medição semanal entra no F2, junto do medir_uso.py; a andrej-karpathy-skills, se passar, entra no config\plugins.json do F1b e na disputa do F3b, com o teste por um tempo e a aferição semanal).

## Limites
- Pesquisa por subagentes; a janela principal só julga e conversa. Nada instalado; nenhum projeto tocado; nada de reestruturar skill.
- As transcrições das sessões têm dado de paciente: lidas só por script que imprime números, nunca texto.
- Commit por caminho explícito; push no fim (git log origin/main.. antes).

## Ao fechar
Portão: as decisões gravadas e aprovadas; a linha de base em metricas\; as pesquisas no INDICE; git status limpo; push. ESTADO.md reescrito. Resumo: o objetivo como ficou, o veredito da andrej-karpathy-skills, a medição (o que mede, quando roda, quanto custa) e "Sinais de insuficiência do modelo". Confira e ajuste o prompt do F1b neste plano e entregue-o (modelo e /effort na 1ª linha).
```

### F1b — o kit como marketplace — feito em 07/10

```
Opus 5.5 · /effort medium — reestruturação conferida por comando a cada passo; suba para /effort high se uma skill sumir ou duplicar sem você notar.

Janela no painel aberta em C:\CLAUDE-PROJETOS\claude-kit. Antes: git pull --ff-only; git status limpo; leia docs\ESTADO.md e o caixa\INDICE.md (a janela das cores fechou em 06/10). Confira se o Remote Control ligou sozinho nesta janela (R1; ADR-0001 D8) e anote no ESTADO.md; se não ligou no painel, anote também para o F3a.

## Contexto
Plano: decisoes\2026-10-06_plano-fluxo.md (bloco F1b, Ficha, "Como você opera"). Q6, Q14, Q17 e §6.1 do registro decisoes\2026-10-06_entrevista-fluxo.md. Privacidade e isolamento: decisoes\adr\0001-privacidade.md e 0002-isolamento.md (o kit nunca recebe paciente; o pre-commit roda o scripts\checa_kit.py). Fatos e fontes: pesquisas\2026-10-06_marketplace-local-e-skills-por-projeto.md (pasta local serve de marketplace; plugin com caminho relativo carrega no lugar; skill de plugin atende pelo nome curto; enabledPlugins do projeto vence o do usuário; skillOverrides não vale para skill de plugin). R1: decisoes\2026-10-06_R1-objetivo-medicao-recursos.md — Q46: esta fase roda como está, com as paradas; ao parar para pedir o "sim", mande um PushNotification com o texto "claude-kit · F1b · precisa de você" (nada além disso; ADR-0001 D8). Q40: o session-report sai do escopo de usuário e fica só nas pastas de teste.

## O que fazer
1. Teste antes de tudo: .claude-plugin\marketplace.json na raiz do kit; plugins\planejamento\ com grill-me e grilling COPIADAS; claude plugin marketplace add C:\CLAUDE-PROJETOS\claude-kit; numa pasta de rascunho com .claude\settings.json, ligar e desligar o grupo e conferir a lista de skills, o /grill-me curto (com a junção antiga ainda lá haverá nome repetido: anote o que acontece), a edição valendo com /reload-plugins e nenhuma cópia em ~\.claude\plugins\cache. Falhou algo: pare e traga ao Ettore.
2. Grupos (o nosso e o de terceiros em plugins separados; por onde se usa): nucleo (nosso; todo projeto), kit (nosso; só no kit), planejamento (terceiros; todo projeto), engenharia (terceiros; projetos de código). Mostre a tabela skill → grupo em uma tela e espere o "sim". Cada plugin de terceiros com origem.json (skill → repositório → commit).
3. Migre grupo a grupo: plugin → backup da junção → remove a junção daquele grupo em ~\.claude\skills → confere. As nossas que o F2 vai quebrar entram como estão. O organizar-projetos (a janela das cores já fechou): ao movê-lo, ajuste o caminho do gancho das cores no ~\.claude\settings.json (backup antes) e confira que o gancho ainda dispara.
4. config\plugins.json (marketplaces e plugins de fora: cc-marketplace/cc-safety-net, claude-md-management, session-report — escopo de projeto, só em teste-fluxo e teste-ferramentas, sempre com --dir (Q40) —, frontend-design, notion; escopo de cada um); desligue o session-report no escopo de usuário (backup do ~\.claude\settings.json antes). scripts\instalar_kit.py (substitui o ligar_claude.py): marketplace do kit, plugins de fora, git config core.hooksPath .githooks, --verificar (junção sobrando, nome repetido, grupo faltando, hardlink do CLAUDE.md pessoal), o trecho de enabledPlugins por tipo de projeto e o comando da política do safety-net para o Ettore rodar. O hardlink quebra quando um git pull muda o CLAUDE.md (o git grava arquivo novo): antes de escrever o religamento, teste trocar o hardlink por um ~\.claude\CLAUDE.md com só a linha @C:/CLAUDE-PROJETOS/claude-kit/CLAUDE.md (import); se o import carregar o texto numa sessão nova, ele substitui o hardlink (e a regra do hardlink sai do CLAUDE.md e da memória). scripts\atualizar_terceiros.py: npx skills add numa pasta de preparo → copia para o plugin → atualiza o origem.json.
5. CLAUDE.md pessoal: a regra do ligar_claude.py passa a instalar_kit.py e atualizar_terceiros.py (hardlink: gravar no próprio arquivo; conferir com fsutil). LEIA-ME.md do kit: estrutura, instalação nos dois PCs, o guia e o gerador.
6. COMO_OPERAR.md na raiz do kit, só com a parte "até o F3" da seção "Como você opera" (a parte "depois do F3" entra no F3c, se o laço passar), a partir da Parte 2 de docs\2026-10-06_o-que-mudou-e-como-operar.md (não escreva de novo; aponte para ele); o gerar_guia_skills.py passa a gerar o GUIA_DAS_SKILLS.docx com a operação como 1ª parte e as skills por grupo. Regere.
7. Q28: no guia antigo do Claude Docs (https://claude.ai/code/artifact/954e4c88-eb09-4a18-b4e5-f95f27004488), um aviso no topo apontando para o GUIA_DAS_SKILLS.docx (carregue antes a skill de docs).

## Limites
- Não quebrar nem reescrever skill (é o F2). Nada em projeto (desosp-*, pesquisa-*).
- Commit por caminho explícito a cada grupo migrado; push no fim, com o portão verde.
- O CLAUDE.md da raiz é o ~\.claude\CLAUDE.md (hardlink): depois de qualquer git que reescreva arquivo (checkout, reset, pull, stash), confira com fsutil hardlink list.

## Ao fechar
Portão: instalar_kit.py --verificar passa; ligar e desligar engenharia numa pasta de rascunho muda a lista; /grill-me curto funciona; nenhuma junção sobrando dos grupos migrados; o gancho das cores dispara; guia regenerado; scripts\checa_kit.py --tudo sem achado. docs\ESTADO.md do kit reescrito; se o desktop tiver de fazer algo (o instalar_kit.py), uma mensagem NB nova na caixa\. Resumo com "Sinais de insuficiência do modelo". Confira e ajuste o prompt do F2 neste plano e entregue-o.
```

### F2a — as skills do kit

```
Opus 5.5 · /effort high — as skills do núcleo guiam toda sessão futura e o erro nelas é silencioso; suba para /effort xhigh (com motivo escrito) se as perguntas de controle falharem duas vezes.

Janela no painel aberta em C:\CLAUDE-PROJETOS\claude-kit. Antes: git pull --ff-only; git status limpo; python scripts\instalar_kit.py --verificar com 0 achados; leia docs\ESTADO.md e o caixa\INDICE.md. Confira que as regras pessoais carregaram pelo import (o ~\.claude\CLAUDE.md é só a linha @C:/CLAUDE-PROJETOS/claude-kit/CLAUDE.md): sem abrir arquivo, você sabe o pseudônimo de exemplo das regras? Se não souber, pare e avise.

## Contexto
Plano: decisoes\2026-10-06_plano-fluxo.md (blocos F2 e F2a, Ficha, "Como você opera"). Do registro decisoes\2026-10-06_entrevista-fluxo.md, leia §5 (Q3, Q4, Q5, Q9, Q10, Q13, Q14, Q15, Q18, Q20) e §6.2, §6.4 e §6.5. Pesquisas: 2026-10-06_continuar-em-contexto-limpo-sem-copiar-prompt.md; 2026-10-06_ferramentas-pedidas-e-orquestradores.md (SDD, regra do Workflow); 2026-10-05_fluxo-atual-dos-projetos.md (as lições). R1: decisoes\2026-10-06_R1-objetivo-medicao-recursos.md (seções 2, 5 e 6); ADR-0001 D8. F1b (07/10): docs\ESTADO.md — o kit é marketplace; as skills moram em plugins\<grupo>\skills; a engenharia liga só por projeto; o gancho das cores está em plugins\nucleo\hooks\hooks.json; config\plugins.json já prevê o grupo kit. Ao escrever skill, use a skill writing-for-agents. Q46: ao parar para o "sim", PushNotification com "claude-kit · F2a · precisa de você" (nada além; ADR-0001 D8).

## O que fazer
1. Quebrar a uso-do-claude no plugin nucleo: núcleo ≤ 150 linhas (princípio, escada, sinais de insuficiência, armadilhas — inclusive: subagente com model: sonnet roda no 5.5; o Sonnet 5 vem só de /model sonnet e --model sonnet —, contexto, uma janela, pontos de checagem de recursos da Q14, exceção da Q15) + modelo-e-esforco + fechar-janela (ESTADO.md reescrito, PROXIMO.md, caixa, resumo com "Sinais", fechar por fim de fase ou ~150 mil ou troca de modelo, push pela Q10; lançar a próxima por claude --bg só se config\fluxo.json disser lancar_bg: true — fica false até o F3c) + pesquisa (biblioteca → subagente → salvar) + orquestrar (roteamento da Q18, os 3 papéis, modelo por papel, paradas da Q10, teto 10 e acima disso estimativa + "sim", cache de subagente). Só disparam sozinhas as que precisam; o resto só /. O reference.md fica como consulta; o medir_uso.py vai para scripts\ e as referências mudam (recursos-do-projeto, COMO_OPERAR.md, o plano). Meça antes e depois (tamanho, /context).
2. Quebrar o organizar-projetos (hoje plugins\nucleo\skills\uso-do-claude\organizar-projetos\) em 3 skills só / num plugin novo, kit (no .claude-plugin\marketplace.json): organizar-projetos (pasta-mãe, GitHub, a fase 0 de reaproveitar, projeto novo — a pasta nasce na janela da raiz), cores-das-pastas (pastas.md, legenda, mapa, VS Code) e icones (os ícones; os pedidos de ícone novo se juntam e se desenham em lote; C:\CLAUDE-PROJETOS\prototipos-icones). Os scripts das cores (pastas.py, gancho.py, regras.py, mapa.json, testes) ficam onde o gancho do nucleo os acha, porque o gancho continua em todo projeto: escolha o lugar e conserte o hooks.json, o local.json (pelo instalar_kit.py) e o mapa. O pastas.py ligar-gancho deixa de gravar no settings.json (o gancho é do plugin); o inventario.py passa a olhar plugins\, não skills\; o ORGANIZAR.md, o reaproveitar.md, o prompts.md e o inventario.py ainda citam o ligar_claude.py, as junções e o hardlink do CLAUDE.md — passam ao instalar_kit.py e ao import. Ligue o kit no claude-kit\.claude\settings.json e rode o instalar_kit.py (ele grava o C:\CLAUDE-PROJETOS\.claude\settings.json da janela da raiz; cor dessa pasta: nao-toco). Confira: no kit e na raiz, /organizar-projetos aparece; numa pasta de rascunho, não; o gancho ainda dispara (pasta de teste); pastas.py conferir com 0 problemas; a suíte das cores verde.
3. recursos-do-projeto enxuta (Q20): SKILL ≤ ~100 linhas + catálogo sob demanda; passo opcional de descoberta com o claude-code-setup (forma final depois do F3b).
4. SDD: as 4 skills (subagent-driven-development, requesting-code-review, using-git-worktrees, finishing-a-development-branch) num plugin de terceiros próprio, trazidas pelo atualizar_terceiros.py (--repo, --grupo), com origem.json; na orquestrar, a nota de uso (cabeçalhos "Task N", modelo fixo por despacho, o ESTADO.md continua dono do estado, o livro-razão .superpowers\ é descartável).
5. Modelos: ESTADO.md (≤ 1 página: objetivo, progresso, surpresas, decisões → ADR, próximo passo, critério de pronto); PROXIMO.md (1ª linha com modelo e /effort; contexto; o que fazer; limites; "Escritas em dado real aprovadas"; "Decisões pré-aprovadas"; "Sempre me pergunte"; a linha /goal "portão ou fila"; ao fechar); docs\PERGUNTAS.md (problema, opções, recomendação, o que depende); ADR; GLOSSARY.
6. O texto das regras nas skills (os ganchos que as aplicam são do F2b):
   - a fila e a execução largada (Q35, Q36, Q44), no fechar-janela e no orquestrar: a dúvida vai para a fila; segue com o que não depende; para só quando tudo depende; os pontos da Q10 nunca sem o "sim";
   - a rodada de contingências no fim de todo grill e plano, na nossa skill (não mexa na grilling);
   - o aviso (Q43, Q48; ADR-0001 D8): PushNotification só nos três casos (tudo depende da fila; a cadeia terminou; falha que só ele resolve), com o texto "projeto · fase · N perguntas"; sem Remote Control, nenhum aviso;
   - janelas e sonda (Q37, Q45), na orquestrar: tantas janelas quanto houver trabalho independente, um escritor por projeto ou worktree (até 3), o % de 5 h antes de abrir outra; a sonda grava em arquivo e as janelas leem; o "pronto" por SendMessage só no mesmo domínio e só se o F3a mostrar ganho;
   - esforço dos subagentes: na semana de 29/09, 1.197 chamadas do Sonnet 5.5 rodaram em max, quase todas em subagentes; confira na documentação se o subagente herda o esforço da janela e, se der, fixe o esforço por papel na orquestrar.
7. perguntas_controle.py com ~10 perguntas (ex.: a 1ª linha do prompt; quando usar Workflow; onde mora o estado; onde ligar a engenharia) numa sessão nova: as respostas batem com as regras. Regenere o guia (CURADO das skills novas e do grupo kit).

## Limites
- Nada em projeto (desosp-*, pesquisa-*): os projetos entram nas fases deles.
- Ganchos, statusline, settings e medição são do F2b; aqui, só o texto das regras.
- Commit por assunto, caminho explícito; push no fim com o portão verde.

## Ao fechar
Portão: núcleo ≤ 150 linhas; perguntas_controle.py bate; /context com o custo fixo menor (o número, antes × depois); o kit com as 3 skills, ligado só no kit e na raiz; instalar_kit.py --verificar com 0 achados; o gancho das cores dispara; guia regenerado; scripts\checa_kit.py --tudo sem achado. docs\ESTADO.md do kit reescrito; se o desktop tiver de rodar o instalar_kit.py de novo, uma mensagem NB nova na caixa\. Resumo com "Sinais de insuficiência do modelo". Confira e ajuste o prompt do F2b neste plano e entregue-o.
```

### F2b — ganchos, settings, medição e pastas de teste

```
Opus 5.5 · /effort medium — ganchos e medição se conferem por teste com JSON e por número; suba para /effort high se um teste de gancho falhar sem causa entendida.

Janela no painel aberta em C:\CLAUDE-PROJETOS\claude-kit. Antes: F2a fechado; git pull --ff-only; instalar_kit.py --verificar com 0 achados; leia docs\ESTADO.md e o caixa\INDICE.md. Nenhuma outra janela aberta (o item 2 mexe no ~\.claude\settings.json).

## Contexto
Plano: decisoes\2026-10-06_plano-fluxo.md (blocos F2 e F2b, Ficha — itens 4, 7, 8, 9 e 10 —, "Como você opera"). Registro decisoes\2026-10-06_entrevista-fluxo.md: §5 (Q3, Q9, Q10, Q12, Q21, Q35) e §6.2. Pesquisas: 2026-10-05_sessoes-memoria-plugins-claude-code.md (ganchos); 2026-10-05_fluxo-atual-dos-projetos.md (lições 1-2); 2026-10-06_medicao-semanal-de-uso.md; 2026-10-06_varredura-final-atencao-concentrada.md; 2026-10-04_organizacao-com-claude-code.md:92 (gancho de plugin no Windows: ${CLAUDE_PLUGIN_ROOT} chega com /; a forma-shell roda no Git Bash). R1: decisoes\2026-10-06_R1-objetivo-medicao-recursos.md (seções 2, 5 e 6; Q39-Q42). As regras que os ganchos aplicam já estão nas skills (F2a). Ao parar para o "sim": PushNotification com "claude-kit · F2b · precisa de você".

## O que fazer
1. Ganchos no plugin nucleo (hooks\hooks.json, ao lado do gancho das cores; base: C:\CLAUDE-PROJETOS\desosp-app\.claude\hooks\abertura.py, só leitura), cada um testado por JSON (scripts\testar_ganchos.py), em duas camadas.
   - Sempre, em todo projeto: PreModelSwitch (barra o Sonnet 5, deixa o 5.5); SessionStart só com o aviso de modelo e esforço errados e o git pull --ff-only do kit (no máximo uma vez por hora; avisa se divergiu; depois do pull, o instalar_kit.py --verificar, e uma linha só se houver achado).
   - Só onde existir docs\ESTADO.md: o resto do SessionStart (estado curto, caixa, git de outra janela; no clear, injeta o PROXIMO.md); Stop (portão: fase dada como pronta sem ESTADO.md reescrito → bloqueia, até 8 vezes seguidas; aceita fechar com perguntas abertas se o ESTADO.md e o PERGUNTAS.md estiverem gravados); PreToolUse (Write/Edit em pasta de dado fora da lista aprovada → bloqueia); a fila (Q35, Q36, Q44): PermissionRequest (na execução largada, nega com mensagem e enfileira) e PreToolUse em AskUserQuestion (grava a pergunta no PERGUNTAS.md e responde "adiada": só adiar, nunca escolher).
   - Nos projetos ainda não migrados, os ganchos antigos deles continuam.
2. Settings, com backup e só com a outra janela fechada: statusline (modelo, esforço, % do contexto, e o % de 5 h e o semanal — rate_limits — gravados num arquivo local que o medir_semana.py lê); showClearContextOnPlanAccept: true; limpeza das permissões com caminho que não existe mais (o allow do ~\.claude\settings.json tem regras de C:\DESOSP e de um scratchpad velho).
3. Medição (Q39, Q42): complete o scripts\medir_semana.py (só números): a planilha metricas\uso.xlsx (openpyxl; uma aba com as semanas e outra com os gráficos da régua e a linha da meta; metricas/*.xlsx no .gitignore); o metricas\BALANCO.md (o prompt fixo do balanço: ler o CSV, comparar com as metas, gravar metricas\balancos\AAAA-MM-DD.md e pôr cada ajuste proposto na fila do kit); no gancho de abertura do nucleo, a linha semanal roda em segundo plano se a última tem mais de 7 dias (sem imprimir nada), e o balanço vencido (15 dias) vira uma linha só com números que manda abrir a janela da raiz (C:\CLAUDE-PROJETOS: é lá que roda a sessão do balanço, decisão de 07/10). Lançar a sessão do balanço sozinha fica para o F3c.
4. Crie C:\CLAUDE-PROJETOS\teste-fluxo\ e teste-ferramentas\ vazias, com git init e um LEIA-ME de uma linha (o gancho das cores vai perguntar a cor: sem-cor). Nas duas, o .claude\settings.json pelo instalar_kit.py --trecho teste (engenharia e session-report), com um gancho que barra o analyze-sessions sem --dir, e o HTML do session-report no .gitignore (Q40).
5. Regenere o guia.

## Limites
- Nada em projeto (desosp-*, pesquisa-*), salvo ler o abertura.py do app como base.
- Commit por assunto, caminho explícito; push no fim com o portão verde.

## Ao fechar
Portão: testar_ganchos.py verde (com os da fila); numa sessão nova, o SessionStart avisa modelo errado e o PreModelSwitch barra o /model sonnet; a statusline aparece no terminal e o % chega ao arquivo; o medir_semana.py reproduz a linha de 29/09 do metricas\uso-semanal.csv e gera a planilha; as duas pastas de teste criadas; instalar_kit.py --verificar com 0 achados; guia regenerado; scripts\checa_kit.py --tudo sem achado. docs\ESTADO.md do kit. Resumo com "Sinais de insuficiência do modelo". Confira e ajuste os prompts do F3a e do F3b neste plano e entregue os dois (rodam em paralelo).
```

### F3a — o laço

```
Opus 5.5 · /effort medium — esta janela orquestra e confere critérios escritos; as fases que ela lança rodam em Sonnet 5.5 · medium (claude-sonnet-5-5); suba para high se um critério falhar sem causa entendida.

Janela aberta em C:\CLAUDE-PROJETOS\teste-fluxo\ (criada no F2b). Crie a irmã teste-fluxo-dados\ para o teste do gancho. Em paralelo roda o F3b em teste-ferramentas\: não mexa lá.

## Contexto
Plano: claude-kit\decisoes\2026-10-06_plano-fluxo.md (bloco F3a, "Como você opera"). Do registro claude-kit\decisoes\2026-10-06_entrevista-fluxo.md, leia Q9 (§5), §6.3 (celular) e §6.5 (peças). Linha de base: claude-kit\metricas\uso-semanal.csv (R1: retornos, sentadas, maior trecho sem ele, tokens) e claude-kit\pesquisas\2026-10-05_fluxo-atual-dos-projetos.md (~7 passos manuais por janela). R1: claude-kit\decisoes\2026-10-06_R1-objetivo-medicao-recursos.md (Q35, Q37, Q43-Q45).

## O que fazer
1. Projeto sintético mínimo (ex.: CSV sintético de internações → relatório), especificação curta, plano de 3 fases com critério de pronto e testes. Para este teste, config\fluxo.json do kit vale como lancar_bg: true só aqui (variável de ambiente ou cópia local; não mude o do kit).
2. Rodar e anotar, com prova, cada critério (passou / falhou / como):
   a. aprovar o plano com "Yes, clear context" no painel e no terminal;
   b. a fase 1 fecha (fechar-janela) → ESTADO.md + PROXIMO.md → lança a fase 2 (claude-sonnet-5-5 · medium) de dois jeitos: por claude --bg --name … --model claude-sonnet-5-5 --effort medium "Leia docs/PROXIMO.md e siga" e por uma sessão interativa numa aba nova do terminal; para cada jeito: começou sozinha? o Remote Control ligou? o PushNotification chegou ao celular e deu para responder pelo app? ao bater o limite de uso, ela espera e retoma?; claude agents, attach e logs mostram;
   c. a fila (Q35): duas decisões plantadas na fase 2 vão para o docs\PERGUNTAS.md e a fase segue com o que não depende delas; os ganchos de AskUserQuestion e de PermissionRequest funcionam também em --bg; a fase só para quando tudo depende da fila;
   d. /goal "portão ou fila" numa sessão --bg (Q44);
   e. a sessão --bg trabalha em worktree? como o resultado volta ao ramo principal?
   f. o portão Stop barra fechar sem ESTADO.md e aceita fechar com a fila gravada;
   g. o gancho barra Write em teste-fluxo-dados\ fora da lista aprovada e deixa a que está na lista;
   h. reserva no painel: /clear + gancho injeta o PROXIMO.md; "siga" continua;
   i. /model sonnet é barrado; o Sonnet 5.5 pela lista passa; a statusline mostra modelo, esforço, % do contexto e os % de 5 h e semanal;
   j. paralelo (Q37): as mesmas 3 fases em série e em paralelo (3 sessões ao mesmo tempo, arquivos separados): tokens totais e tempo de relógio; vale se os tokens forem iguais ou menores;
   k. sonda (Q45): duas fases paralelas que precisam da mesma pesquisa — cada uma pesquisando sozinha × uma sonda que grava em arquivo e serve às duas, com o aviso de "pronto" por SendMessage; fica só se poupar tempo ou tokens;
   l. medir com o scripts\medir_semana.py: retornos, maior trecho sem ele, sentadas, tokens por fase.
3. RESULTADO.md: critério → resultado → prova; o que falhou vira tarefa do F3c.

## Limites
- Só dado sintético. Nada em desosp-*, pesquisa-*; no kit, só gravar o resultado em pesquisas\ ao fechar (sem mexer no INDICE.md, que é do F3c).
- No máximo 2 tentativas diferentes por critério; falhou, anota e segue.

## Ao fechar
Portão: RESULTADO.md com prova por critério; retornos e maior trecho sem ele medidos; a fila funcionou (as duas decisões ficaram na fila e a fase seguiu) — ou o motivo de não ter dado. Copie o RESULTADO.md para claude-kit\pesquisas\2026-10-XX_teste-do-laco.md (cabeçalho fixo da biblioteca). Resumo com "Sinais de insuficiência do modelo". O próximo é o F3c (prompt neste plano), depois que o F3b também fechar.
```

### F3b — as ferramentas

```
Opus 5.5 · /effort medium — esta janela organiza e mede; executores fixados em Sonnet 5.5 · medium para comparar igual; o revisor cego é um subagente opus; suba para high se os números não fecharem entre execuções.

Janela aberta em C:\CLAUDE-PROJETOS\teste-ferramentas\ (criada no F2b), de preferência no terminal (o Headroom quebra a extensão do VS Code). Em paralelo roda o F3a: não mexa em teste-fluxo\.

## Contexto
Plano: claude-kit\decisoes\2026-10-06_plano-fluxo.md (bloco F3b). Do registro claude-kit\decisoes\2026-10-06_entrevista-fluxo.md, leia §12.7. Q18, Q19, Q20 (tabela do plano). Pesquisa: claude-kit\pesquisas\2026-10-06_ferramentas-pedidas-e-orquestradores.md (custos, riscos, flags). R1: Q38 e Q40 (claude-kit\decisoes\2026-10-06_R1-objetivo-medicao-recursos.md) e claude-kit\pesquisas\2026-10-06_andrej-karpathy-skills.md. Nunca /omc-setup.

## O que fazer
1. Plano sintético de 5 tarefas ("Task 1" a "Task 5") com testes; três clones limpos.
2. Disputa: (i) SDD; (ii) OMC — claude plugin install oh-my-claudecode@omc --scope local; OMC_BUDGET_ENFORCE=active e OMC_RUN_BUDGET_TOKENS; ralplan → execute → verify; nada de autopilot, ralph, team, ask; (iii) uma sessão sem orquestrador; (iv) uma sessão sem orquestrador com a andrej-karpathy-skills carregada por claude --plugin-dir <clone de multica-ai/andrej-karpathy-skills> (sem instalar; Q38). Medir: tokens (scripts\medir_semana.py; o session-report só com --dir na pasta das transcrições deste projeto, Q40), tempo, testes, defeitos achados pelo revisor cego (sem saber qual executor), mudanças fora do pedido e paradas à toa (o revisor conta em todos), paradas respeitadas (uma decisão e um comando destrutivo plantados), intervenções humanas. Uma tentativa por executor; se um travar ou passar de 2 horas, pare-o e anote.
3. Headroom (só terminal; HEADROOM_BEACON=off, --no-subscription-tracking, --code-memory none): uma tarefa com e sem; passa se cortar ≥ 20% dos tokens com os mesmos testes e sem quebrar nada.
4. claude-mem (--scope local; DO_NOT_TRACK=1; recusar o observador na nuvem): duas sessões; passa se a 2ª responder 3 perguntas sobre a 1ª sem ler o ESTADO.md, se a compressão (Haiku) custar pouco (o número) e se o bloqueio de releitura não atrapalhar. Anote o que fica global (worker, porta 37777, ~/.claude-mem, Bun).
5. claude-code-setup sem instalar: claude --plugin-dir <clone do claude-plugins-official>\plugins\claude-code-setup, só neste projeto sintético (no app ele roda no F5a, na janela do app).
6. Veredito por ferramenta: adotar (onde), adotar com restrição, ou remover — e desinstalação conferida das que saírem (claude plugin list, processos, pastas). A andrej-karpathy-skills pelo critério fixado na R1: entra se, com os mesmos testes verdes, gastar ≥ 20% menos tokens que o (iii) ou fizer claramente menos mudanças fora do pedido, sem parar mais na decisão plantada; com uma tentativa, só efeito grande aparece.

## Limites
- Só dado sintético; nenhum projeto real aberto.
- No kit, só gravar o resultado em pesquisas\ ao fechar (sem mexer no INDICE.md, que é do F3c).

## Ao fechar
Portão: RESULTADO.md com números e veredito por ferramenta; desinstalação conferida. Copie para claude-kit\pesquisas\2026-10-XX_ferramentas-testadas.md (cabeçalho fixo da biblioteca). Resumo com "Sinais de insuficiência do modelo". O próximo é o F3c (prompt neste plano), depois que o F3a também fechar.
```

### F3c — ajustes no kit

```
Opus 5.5 · /effort medium — aplicar resultados medidos; suba para high se um ajuste quebrar um critério que já passava.

Janela no painel aberta em C:\CLAUDE-PROJETOS\claude-kit. Antes: F3a e F3b fechados; os dois resultados em pesquisas\ (2026-10-XX_teste-do-laco.md e 2026-10-XX_ferramentas-testadas.md).

## Contexto
Plano: decisoes\2026-10-06_plano-fluxo.md (blocos F3a, F3b, F3c; "Como você opera"). Q9, Q18, Q19, Q20. R1: decisoes\2026-10-06_R1-objetivo-medicao-recursos.md (seção 5).

## O que fazer
1. Leia os dois resultados e acrescente as duas linhas ao pesquisas\INDICE.md.
2. orquestrar aponta o vencedor da disputa, com os números; se o OMC venceu, mostre ao Ettore o custo de adotá-lo e espere o "sim".
3. recursos-do-projeto: forma final do passo de descoberta (claude-code-setup por --plugin-dir, ou nada).
4. claude-mem, Headroom e a andrej-karpathy-skills (pelo critério da Q38: no config\plugins.json ou fora): onde entram, ou a confirmação de que saíram. A sonda e as mensagens entre sessões pelo critério da Q45.
5. O que falhou no laço: corrija nos ganchos ou nas skills e repita só aquele critério em teste-fluxo\.
6. Se o laço passou: o jeito de lançar fases que o F3a mostrou melhor (--bg ou aba interativa com Remote Control) e lancar_bg: true no config\fluxo.json; o lançamento automático do balanço quinzenal (Q42); a parte "depois do F3" no COMO_OPERAR.md (a fila, o aviso no celular, o balanço, as janelas); se não passou, fica a reserva (/clear + gancho) e o COMO_OPERAR.md diz isso.
7. Regenere o guia.

## Limites
- Nada em projeto (desosp-*, pesquisa-*, estudo-*, pessoal-*).

## Ao fechar
Portão: os critérios que falharam passam; INDICE com as duas linhas; guia regenerado. ESTADO.md do kit. Resumo com "Sinais de insuficiência do modelo". Confira e entregue o prompt do F5a (deste plano).
```

### F5a — migração do app

```
Opus 5.5 · /effort high — estado e regras do app: o erro é silencioso e aparece fases depois; suba para xhigh (com motivo) se contradisser regra escrita.

Janela no painel aberta em C:\CLAUDE-PROJETOS\desosp-app. Antes: F3c fechado; R0 fechada (relatório em docs\); nenhuma outra janela no app.

## Contexto
Plano: claude-kit\decisoes\2026-10-06_plano-fluxo.md (bloco F5a, Ficha, "Como você opera"); claude-kit\decisoes\adr\0001-privacidade.md e 0002-isolamento.md. Q3, Q14, Q21 (§5 do registro claude-kit\decisoes\2026-10-06_entrevista-fluxo.md); §12.1 (a porta de leitura).

## O que fazer
1. Proteção de dado primeiro: as tarefas do app (F5a) nas tabelas "Tarefas por fase" do ADR-0001 e do ADR-0002 — o deny interno da D6 (confira a lista no lugar antes de aplicar), os conectores da D4 (os nomes exatos no /mcp), o pre-commit de nomes da D2, o CLAUDE.md pela D1; nenhum subagente nas pastas de dado. A política do safety-net: imprima o comando para o Ettore.
2. docs\ESTADO.md (≤ 1 página) a partir do HANDOFF_APP.md (busca por palavra; o handoff vai congelado para docs\historico\); CLAUDE.md < 200 linhas (o estado sai; regra de um tipo de arquivo vai para .claude\rules com paths:; "Skills deste projeto" ≤ 10 linhas); enabledPlugins pelo instalar_kit.py --trecho codigo (liga a engenharia; nucleo e planejamento vêm do escopo de usuário; o frontend-design sai do escopo de usuário e passa a ser só deste projeto, pelo config\plugins.json; tire a linha que a R0 pôs no .claude\settings.local.json); o abertura.py sai e o gancho do nucleo entra (confira que nada do abertura.py se perde); docs\adr\ + GLOSSARY.md (domain-modeling); a memória do app só com preferência e correção.
3. claude-code-setup só leitura (claude --plugin-dir <clone>\plugins\claude-code-setup numa sessão curta, aqui): compare com docs\RECURSOS_CLAUDE_DESOSP.md e explique ao Ettore cada sugestão de Context7, Playwright MCP e GitHub MCP.
4. Pergunte ao Ettore o que a IA faz dentro do app (app\ia\, o ponto de extensão da PROPOSTA §7) e se a porta de leitura para a comunicação é a 1ª coisa; registre num ADR do app.
5. Com o Ettore, escolha as correções da R0 que entram no F5b e escreva o docs\PROXIMO.md (tarefas "Task N"; "Escritas em dado real aprovadas": nenhuma).

## Limites
- Nenhuma mudança de código do app nesta fase (só documentos, settings, ganchos e regras).
- Nunca abrir dado real; nunca imprimir linha de dado.

## Ao fechar
Portão: CLAUDE.md < 200 (wc -l); ctx0 de uma sessão nova ≤ 40 mil (medir_uso.py); suíte verde; ESTADO.md ≤ 1 página; guia regenerado (scripts\gerar_guia_skills.py do kit). fechar-janela com "Sinais de insuficiência do modelo"; o F5b sai pelo PROXIMO.md (por --bg, se o F3c ligou).
```

### F5b — correções da R0

```
Opus 5.5 · /effort medium — esta janela controla o SDD; os implementadores rodam em subagente model: sonnet (Sonnet 5.5), com o navegador e o axe como prova; suba para high se o mesmo teste falhar na 2ª tentativa.

Janela aberta em C:\CLAUDE-PROJETOS\desosp-app (ou lançada por --bg). Antes: F5a fechado.

## O que fazer
Siga o docs\PROXIMO.md: as correções da R0 escolhidas pelo Ettore, em "Task N"; com 4 ou mais, pelo SDD (skill orquestrar); a revisar-tela em cada tela mexida; suíte de navegador + axe verdes.

## Limites
- Os mesmos de dado real do F5a, repassados a cada subagente. Commit por tarefa, caminho explícito.

## Ao fechar
Portão: suíte verde; revisar-tela com prova por tela; aceite de 5 minutos do Ettore. fechar-janela (ESTADO.md, PROXIMO.md, "Sinais de insuficiência do modelo"). Próximas: o N1 (frente 2) e o F6 (frente 1).
```

### F5c — porta de leitura (depois do N1, antes do N2)

```
Opus 5.5 · /effort medium — porta que devolve dado de paciente: campo a mais é erro silencioso; o teste com dado sintético é a prova; suba para high se o teste de "nenhum campo a mais" falhar.

Janela aberta em C:\CLAUDE-PROJETOS\desosp-app. Antes: o ADR do app sobre app\ia\ (F5a) e o grill do N2 dizendo que campos a comunicação precisa.

## O que fazer
1. Especificação curta: os campos mínimos, quem chama, saída em arquivo local (nunca no terminal).
2. Comando só de leitura em app\ia\ que devolve só esses campos; testes com o banco sintético da suíte, inclusive o de que nenhum outro campo sai.

## Limites
- Só leitura no banco; nunca imprimir linha de dado; testes só com dado sintético.

## Ao fechar
Portão: testes verdes, inclusive "nenhum campo a mais"; ADR do app atualizado. fechar-janela com "Sinais de insuficiência do modelo".
```

### F6 — kernel

```
Opus 5.5 · /effort high — regras do kernel com erro silencioso em dado vivo; os agentes do Workflow rodam em Sonnet 5.5 · medium (fixe o modelo no script); suba para xhigh se casos de borda escaparem.

Janela no painel aberta em C:\CLAUDE-PROJETOS\desosp-censo. Antes: nenhuma rodada em curso; nenhuma outra janela no censo.

## Contexto
Plano: claude-kit\decisoes\2026-10-06_plano-fluxo.md (bloco F6, Ficha); ADR-0001 e ADR-0002; claude-kit\pesquisas\2026-10-05_fluxo-atual-dos-projetos.md (o censo: CLAUDE.md de 430 linhas, 27 regras, MEMORY.md de 12 KB).

## O que fazer
1. Proteção de dado primeiro: as tarefas do censo (F6) nas tabelas "Tarefas por fase" do ADR-0001 e do ADR-0002 — deny e .ignore do bruto pela D6 (confira a lista no lugar; os scripts da rodada continuam lendo; a saida\ fica aberta), os conectores da D4, o pre-commit de nomes, o pseudônimo nas saídas que o Claude lê, o CLAUDE.md pela D1.
2. O mesmo do F5a: ESTADO.md a partir do HANDOFF_SPRINT2.md (congelado em docs\historico\), CLAUDE.md < 200, "Skills deste projeto", enabledPlugins (instalar_kit.py --trecho codigo: liga a engenharia), gancho do nucleo, docs\adr\ + GLOSSARY.md, MEMORY.md só com preferência e correção (a linha de 7,4 mil caracteres sai).
3. Desenvolvimento separado da operação: a skill rodada vira rotina com aprovação permanente dos comandos dela (Q21), escrita no modelo de PROXIMO.md da rodada.
4. Auditoria das 27 regras e das 8 que carregam juntas no data_merge.py, por Workflow (só regras e código, nunca dado; até 10 agentes), cada achado com prova; você consolida.
5. Cartographer (cópia sem os passos 7 e 8) × improve-codebase-architecture: qual mapa ajuda e quanto custa.
6. O lugar do dado: mostre ao Ettore mudar para desosp-censo-dados\ × ficar (o kernel vai ser aposentado); a decisão é dele.

## Limites
- Nenhuma rodada real além da prova do portão (aprovada pela rotina). Nunca imprimir linha de dado. Workflow nunca em pasta de dado.

## Ao fechar
Portão: CLAUDE.md < 200; ctx0 ≤ 50 mil; MEMORY.md ≤ 200 linhas e sem status; suíte verde; uma rodada real sem passo manual a mais; guia regenerado. fechar-janela com "Sinais de insuficiência do modelo".
```

### F7 — planilha HC

```
Opus 5.5 · /effort medium — migração com testes; os comandos migram por subagentes model: sonnet; suba para high se um comando migrado divergir do original.

Janela no painel aberta em C:\CLAUDE-PROJETOS\desosp-hc. Antes: nenhuma rodada HC em curso.

## O que fazer
1. Proteção de dado primeiro: as tarefas do HC (F7) nas tabelas "Tarefas por fase" do ADR-0001 e do ADR-0002 — deny e .ignore do bruto pela D6 (planilhas\, historico\, privado\, entrada\; rodada\, trabalho\ e saida\ ficam abertas; confira no lugar), os conectores da D4, o número do pseudônimo (o RA, se existir), a memória "console sem linha de paciente" pela D1.
2. O mesmo do F5a: ESTADO.md a partir do docs\12_PROXIMA_RODADA.md e da seção "Estado atual" do CLAUDE.md; CLAUDE.md < 200; enabledPlugins (instalar_kit.py --trecho codigo: liga a engenharia); o gancho do nucleo no lugar do caixa_pendente; docs\adr\ + GLOSSARY.md.
3. Os 12 comandos: viram skills? (Workflow candidato, 12 itens iguais, só código); /fechar-rodada, /consolidar e /nova-versao só por / (disable-model-invocation: true).
4. O lugar do dado: mostre ao Ettore e ele decide.

## Limites
- Nunca abrir planilha com dado real; nunca imprimir linha de dado.

## Ao fechar
Portão: CLAUDE.md < 200; ctx0 ≤ 45 mil; suíte verde; os 12 comandos funcionam; guia regenerado. fechar-janela com "Sinais de insuficiência do modelo".
```

### F8 — desktop

```
Opus 5.5 · /effort medium — repetir no desktop o que o notebook provou; suba para high se o desktop divergir sem causa clara.

No DESKTOP. Janela aberta em C:\CLAUDE-PROJETOS\claude-kit (depois do git clone do HirugaX/claude-kit). Antes: leia caixa\ e _do_desktop\ (o que o Ettore começou em 06/10).

## O que fazer
1. instalar_kit.py (marketplace, plugins, --verificar); o Ettore roda o comando da política do safety-net que o instalador imprime.
2. organizar-projetos (/, plugin kit): pasta-mãe CLAUDE-PROJETOS e ícones, se ainda faltar.
3. Para cada projeto do desktop (DASH, Folha/RH, Acolhimento), escreva o prompt da janela dele (uma janela por projeto, não esta): domínio e prefixo (ADR-0002); GitHub privado com varredura; CLAUDE.md < 200, ESTADO.md, enabledPlugins (instalar_kit.py --trecho <tipo>; os de código ligam a engenharia); prompts 10-12 de fontes\Claude_Workbench_Prompts como checklist; Context7 no DASH; fechar-janela do DASH unificada com a do kit; o Apps Script que grava na raiz do Drive passa a gravar em IA\<projeto>.

## Limites
- Nada de projeto do desktop nesta janela (cada um na sua).

## Ao fechar
Portão: instalar_kit.py --verificar passa; os prompts dos projetos do desktop prontos; guia regenerado. Resumo com "Sinais de insuficiência do modelo".
```

### F9 — guia e retrospectiva

```
Opus 5.5 · /effort medium — consolidar e medir; suba para high se a retrospectiva sair genérica, sem números.

Janela no painel aberta em C:\CLAUDE-PROJETOS\claude-kit.

## O que fazer
1. Guia final (gerar_guia_skills.py): a operação e as skills por grupo.
2. /retro do redesenho: os números do metricas\uso-semanal.csv e dos balanços contra a linha de base (tabela "Verificação de ponta a ponta" do plano), o que funcionou, o que cortar.
3. Chaves velhas da memória automática (C--DESOSP…, 10 arquivos divergentes): mostre a lista e espere o "sim" antes de limpar.
4. Salve a retrospectiva em pesquisas\ + INDICE.
5. cleanupPeriodDays volta a 30 no ~\.claude\settings.json (backup antes; Q41 da R1).

## Ao fechar
Portão: guia regenerado; retrospectiva com números salva; memória velha limpa ou a lista do que ficou. Resumo com "Sinais de insuficiência do modelo".
```

### Fd — o Drive (no desktop)

```
Sonnet 5.5 (escolha na lista do /model) · /effort medium — classificar e mover arquivos com aprovação; o erro é visível e se desfaz; suba para Opus 5.5 · medium se mais de 1 em 10 sair classificado errado.

No DESKTOP. Janela aberta em G:\Meu Drive, só para esta tarefa. Antes: o Google Drive para computador sincronizado.

## Contexto
Q25 e Q32 (06/10): tudo o que é de IA vai para G:\Meu Drive\IA\<projeto>, uma subpasta por projeto, com os nomes das pastas de C:\CLAUDE-PROJETOS (claude-kit, desosp-app, desosp-censo, desosp-hc, desosp-comunicacao, estudo-residencia, pessoal-organizacao, pessoal-produtividade, pesquisa-clinica e os do desktop); o que não tiver dono vai para IA\00-entrada. Arquivo pessoal que não é de IA fica onde está.

## O que fazer
1. Liste a raiz de G:\Meu Drive e de IA\ (nome, tipo, data). Nome que pareça ter dado de paciente: mostre só tipo e data e marque "trabalho?".
2. Proponha a tabela arquivo → destino (ou "fica") e espere o "sim" do Ettore.
3. Crie as subpastas que faltarem e mova (dentro do G:); grave IA\00-entrada\LEIA-ME.md com o registro do que moveu.
4. Diga quem provavelmente criou cada grupo (claude.ai, Gemini, zips do kit, Apps Script) e grave a regra "gravar no Drive só em IA\<projeto>" onde valer: o CLAUDE.md da pasta-mãe do desktop (se existir; senão, anote para o F8) e uma linha pronta para o Ettore colar nas instruções dos Projects do claude.ai.

## Limites
- Nada apagado. Nada fora de G:\Meu Drive. Nenhum arquivo aberto: só nome, tipo e data.
- Apps Script (Folha/RH, Acolhimento) que grava na raiz: anote para o F8 (é mudança de código).

## Ao fechar
Portão: tabela aprovada; raiz sem arquivo de IA solto; IA\00-entrada\LEIA-ME.md com o registro. Resumo: quantos movidos por pasta, o que ficou na entrada, os escritores achados e "Sinais de insuficiência do modelo".
```

### N1-N5 — projeto novo (o mesmo prompt; troque o que está entre < >)

```
Opus 5.5 · /effort high — planejar um projeto novo: erro de plano só aparece depois e custa caro; suba para xhigh se o plano sair raso ou ignorar restrição citada.

A pasta nasce na janela da raiz (C:\CLAUDE-PROJETOS), com /organizar-projetos (plugin kit, a partir do F2a): C:\CLAUDE-PROJETOS\<projeto>\ (estudo-residencia | desosp-comunicacao | pessoal-organizacao | pessoal-produtividade | pesquisa-clinica), as cores e o git; depois abra a janela nela. Modo plano desligado até o fim do grill.

## Contexto
Plano do fluxo: claude-kit\decisoes\2026-10-06_plano-fluxo.md (bloco "Frente 2", item <N>); claude-kit\decisoes\adr\0001-privacidade.md e 0002-isolamento.md. Base do projeto: <N1: claude-kit\pesquisas\2026-10-06_estudo-anki-e-produtividade.md | N2: §12.1 do registro claude-kit\decisoes\2026-10-06_entrevista-fluxo.md | N3 e N4: §12.2 e §12.5 do registro + claude-kit\pesquisas\2026-10-04_notion-filtros-e-visoes.md | N5: claude-kit\pesquisas\2026-10-06_espaco-de-pesquisa-clinica.md>.

## O que fazer
1. /grill-me do projeto (skill grilling; perguntas no formato do CLAUDE.md pessoal).
2. Confirmado o entendimento: recursos-do-projeto (a ficha).
3. Plano do projeto com fases, portões, modelo e esforço; espere o "sim".
4. Montagem inicial: CLAUDE.md < 200, ESTADO.md, enabledPlugins (instalar_kit.py --trecho <tipo>: codigo, pesquisa-estudo ou pessoal), disableClaudeAiConnectors (menos nos pessoal-* que usam conector); se houver dado, <projeto>-dados\ com deny e a política do safety-net (o Ettore aplica o comando); git, varredura e GitHub privado.

## Limites
- Nunca dado de paciente (N2: só por marcadores; o acervo só em cópias com marcadores).
- Nada fora desta pasta, salvo gravar pesquisa nova em claude-kit\pesquisas\ (com linha no INDICE).

## Ao fechar
Portão: grill, ficha e plano aprovados; montagem inicial com push e varredura limpa; guia regenerado. fechar-janela com "Sinais de insuficiência do modelo".
```

## Depois do "sim" (nesta janela)

1. Gravar este plano em `claude-kit\decisoes\2026-10-06_plano-fluxo.md`.
2. Salvar as três pesquisas desta janela em `claude-kit\pesquisas\`, com linha no `INDICE.md`:
   `2026-10-06_marketplace-local-e-skills-por-projeto.md` (marketplace local, `skillOverrides`, `syncClaudeAiSkills`,
   `disableClaudeAiConnectors`, gatilho do ultracode, Remote Control, o atalho `sonnet` no subagente);
   `2026-10-06_dados-e-drive-inventario.md` (pastas de dado e proteções; o Drive);
   `2026-10-06_mermaid-no-contexto-do-llm.md` (tokens e acerto; FlowBench, TextFlow, He 2024, GraphOmni, Talk like a
   Graph; orientação da Anthropic).
3. Atualizar a memória `redesenho-do-fluxo-2026-10-06.md` com o ponteiro do plano aprovado.
4. Resumo da janela (com "Sinais de insuficiência do modelo") e o prompt do F1a.

## Apêndice — fatos verificados nesta janela (fonte)

- **Safety-net:** `~\.cc-safety-net\policy.json` com `deny_paths` = `desosp-app-dados`, `desosp-app-backups`.
- **Skills do claude.ai:** as 5 indicadas na lixeira (`~\.claude\skills\.trash`, 06/10 09:29); ficam docs, docx, pdf,
  pptx, xlsx, skill-creator, stop-slop, find-skills, llm-council, prompt-master.
- **Ultracode:** `"workflowKeywordTriggerEnabled": false` em `~\.claude\settings.json:74`; continuam `/effort
  ultracode`, `claude --effort ultracode`, `/deep-research`, workflows salvos e o pedido explícito; tudo some só com
  `disableWorkflows` (code.claude.com/docs/en/workflows; settings-reference).
- **Atalho `sonnet` no subagente:** os 4 subagentes desta janela, chamados com `model: sonnet`, rodaram em
  `claude-sonnet-5-5` (transcritos da sessão, `subagents\*.jsonl`). A armadilha do Sonnet 5 é `/model sonnet` e
  `--model sonnet`.
- **Drive:** neste notebook nada escreve no Drive (sem Drive para computador; nenhum código; nenhuma ferramenta Google em
  552 transcritos; o `export` do Claude Docs só devolve o arquivo). Suspeitos: claude.ai com conector Google
  (`scripts\gerar_guia_skills.py:389`); o desktop, onde `G:` é o Drive (`_do_desktop\desktop_2026-10-05\LEIA-ME.txt:34-35`)
  e os zips do kit iam pelo Drive (`decisoes\2026-10-04_prompts-das-janelas.md:215`); o Gemini.
- **Dado fora do repositório:** só o app (`desosp-app-dados`, `-backups`; `deny` Read/Edit em
  `~\.claude\settings.json:18-21`). Censo e HC guardam dado dentro do repositório, só com `.gitignore`
  (`desosp-censo\.gitignore:2-12`; `desosp-hc\.gitignore:3-17`), sem `deny`. No app, dentro e ignorados:
  `workspace_dev\` e `docs\para_o_app\`. O `.ignore` da mãe não lista `desosp-app-backups/`.
- **Marketplace local** (code.claude.com/docs/en/plugins/install, /loading, /cli-reference, /skills): pasta local serve
  de marketplace; plugin com caminho relativo carrega no lugar (vale na sessão seguinte ou com `/reload-plugins`, sem
  versão); `/skill` curto quando não há conflito; `enabledPlugins` do projeto vence o do usuário e dispensa instalação
  para plugin de caminho relativo; `skillOverrides` (`on`/`name-only`/`user-invocable-only`/`off`) desliga skill de
  usuário por projeto, não a de plugin; `syncClaudeAiSkills: false` para a sincronização (pdf e xlsx sempre vêm);
  `disableClaudeAiConnectors: true` em qualquer settings desliga os conectores (o projeto desliga, não religa); `/mcp`
  liga e desliga cada um.
- **Celular:** `claude --bg` é comando de shell (prévia); rodá-lo de dentro do Remote Control não está documentado;
  mensagens entre sessões no Windows vão por named pipe (2.1.234+); `/reload-plugins` não roda pelo Remote Control.
- **Mermaid:** na regra real de roteamento, prosa 335 caracteres, lista 347, tabela 390, Mermaid 445-542; FlowBench
  (EMNLP 2024, só GPT): +4 a +11 pontos no passo seguinte, sessão inteira entre −2,1 e +2,6 (comparável); TextFlow:
  Claude 3.5 lendo Mermaid 80,0% × Graphviz 82,2%, sem braço de prosa; formato muda até 40% sem vencedor fixo (He 2024;
  GraphOmni); Anthropic recomenda títulos, listas numeradas e tabelas; 0 de 7 skills oficiais usam Mermaid; no chat da
  extensão o Mermaid aparece como código cru (issue 20529).
- **Gancho das cores:** `~\.claude\settings.json:32` chama `skills\uso-do-claude\organizar-projetos\scripts\gancho.py`
  (com `|| true`: falha calada) e grava `desktop.ini` em pasta nova.
- **Vazamento visto de novo:** o subagente leu arquivos do app e do censo, e as skills `revisar-tela` e `rodada`
  entraram na lista desta janela.
- **Cores:** raiz de projeto recebe a marca `projeto-ia`; fontes, `eu-forneco-fontes` (`organizar-projetos\mapa.json`).
