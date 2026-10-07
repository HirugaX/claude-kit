# Medição semanal de uso do Claude Code: o que as transcrições medem, com que regra e a que custo (06/10/2026)

- **A pergunta:** dá para aferir, semana a semana, o uso de tokens e as interações do Ettore (atenção concentrada: o maior
  trecho em que o Claude trabalha sem ele e quantas vezes ele precisa voltar) só com os registros locais? Qual a regra de
  cada métrica, o que o `medir_uso.py` e o plugin `session-report` já fazem, o que falta, quanto custa e o que a retenção
  (`cleanupPeriodDays`) apaga?
- **A data:** 06/10/2026.
- **O projeto que pediu:** claude-kit (R1).
- **Conferir de novo depois de:** 06/11/2026, ou quando o Claude Code passar da versão medida (2.1.289) e mudar o esquema
  das transcrições (campos `origin`, `promptSource`, `queue-operation`, `cost-state`) ou a doc de retenção.
- **Método:** scripts Python que leem as transcrições e só imprimem números, datas, IDs de modelo, nomes de chave e nomes
  de pasta de projeto. Nenhum texto, comando, caminho ou título foi lido, impresso ou gravado aqui. O texto das mensagens
  só foi testado ("começa com tal marcador?") ou comparado por hash. As regras foram conferidas com contagens (seção 3) e
  com duas recontagens independentes (a função `ler()` do próprio `medir_uso.py` e uma contagem separada de mensagens do
  humano). A doc foi lida em `.md` cru: o `WebFetch` resumido errou o padrão do `cleanupPeriodDays` (respondeu 90 dias;
  a doc diz 30).

## Conclusão em poucas linhas

1. **Dá para medir tudo só com as transcrições e sem gastar token.** O protótipo lê a semana (159 arquivos, 289 MB,
   52.158 eventos) em 1,8 s e gera uma linha de 28 colunas. Tokens, chamadas e contexto conferem 100% com
   `medir_uso.ler()`: 5.396 chamadas dos arquivos principais, contexto total 1.826.154.505, mediana 307.005.
2. **O `medir_uso.py` cobre uma parte:** contexto, ctx0 e família de modelo por sessão, só nos arquivos principais. Não
   soma a saída, não conta subagentes (1.693 das 7.089 chamadas da semana; 14% dos tokens) e não mede humano, retorno,
   trecho, concorrência nem sentada. O `--desde` filtra pela hora UTC do 1º evento da sessão e não tem teto. O US$ falta
   em 53 de 98 sessões.
3. **O `session-report` não serve:** grava o texto dos prompts (100 prompts, com vizinhos e quebras de cache) em JSON e HTML
   na pasta atual; o modelo lê o JSON e o reescreve inteiro (estimativa para esta semana: 45 a 60 mil tokens lidos, outro
   tanto escritos, mais ~8 mil do modelo de página); mede concorrência por "span" de sessão. Fere a regra de isolamento:
   texto de outros projetos entra nesta janela.
4. **Três armadilhas medidas:** (a) humano = `origin.kind == "human"` (mais `queued_command`); sem isso entram 49 mensagens
   de um lote de 49 sessões da v2.1.234, sem campo `origin`, que fabricam "32 sessões ao mesmo tempo" e "71 mensagens" em
   03/10; (b) "evento da sessão" não pode incluir `attachment`: em 28 de 29 retornos havia um `total_tokens_reminder`
   gravado menos de 2 s antes da mensagem; (c) o trecho literal infla com respostas a perguntas (61 na semana) e com
   espera de tarefa em segundo plano (3h13 sem nenhum evento): o trecho contínuo (lacuna ≤ 15 min) tem de andar junto.
5. **Semana 29/09 a 05/10 (terça a segunda):** 98 sessões com chamada (48 com mensagem do humano); 7.089 chamadas;
   2,136 bilhões de tokens (cache lido 97,9%; saída 0,39%); 155 mensagens do humano e 61 respostas a perguntas; 29 retornos
   (> 30 min); maior trecho 4h08 (literal), 3h14 (sem ação dele), 1h48 (contínuo); no máximo 4 sessões do humano na mesma
   janela de 10 min; 50 sentadas, 613 min somados.
6. **Retenção:** `cleanupPeriodDays` não está definido em lugar nenhum, então vale o padrão de 30 dias (doc), com varredura
   ao iniciar sessão. O 1º evento mais antigo no disco é de 09/09. O histórico some em 30 dias: gravar a linha toda
   semana e preencher já as semanas de 15/09 e 22/09 (linhas na seção 7).
7. **Nativo:** `/usage` (`/cost` e `/stats` são alias) e o diálogo "Account & usage" do VS Code mostram barras do plano e
   custo da sessão, sem saída para máquina. O status line recebe `rate_limits.five_hour` e `seven_day` com
   `used_percentage` (a única fonte do % do limite semanal), mas a doc do VS Code não cita status line.
   `--output-format json` com `total_cost_usd` e custo por modelo só existe em `claude -p`.

## 1. O que o `medir_uso.py` mede hoje

Arquivo: `C:\CLAUDE-PROJETOS\claude-kit\skills\uso-do-claude\medir_uso.py` (88 linhas).

- **Opções:** `--desde AAAA-MM-DD` (compara com a hora UTC do 1º evento da sessão, 16 caracteres; sem teto superior;
  linhas 57 e 67) e `--sessoes` (uma linha por sessão; linhas 58 e 81-84). Não há outras.
- **O que lê:** só `*.jsonl` direto na pasta do projeto (linha 65). Não entra em `<sessão>\subagents\` e não testa
  `isSidechain`: **não conta subagentes**.
- **Chamada:** um `message.id` único, entradas `assistant` com `model` e sem `<synthetic>`; vale a última entrada do id
  (linhas 44-50).
- **Contexto da chamada:** `input_tokens + cache_read_input_tokens + cache_creation_input_tokens` (linha 49). A saída é
  lida e não aparece em nenhuma coluna.
- **ctx0:** contexto da 1ª chamada da sessão, ordenada pelo timestamp (linhas 51 e 74). **ctx_med:** mediana superior
  (`sorted(ctx)[n // 2]`, linha 74). **ctx_max:** pico. **comp:** compactações (`isCompactSummary` ou `compact_boundary`,
  linha 40). **US$:** último `cost-state.totalCostUSD` da sessão (linhas 42-43).
- **Modelo:** família por trecho do ID (`fable-5-1, fable-5, opus-5-5, opus-5, sonnet-5-5, sonnet-5, haiku-4-5`; fora
  disso, os 14 últimos caracteres do ID; linhas 19-27).
- **Cabeçalho por projeto:** chamadas, contexto médio, `%fixo` (soma de ctx0 × chamadas ÷ soma do contexto), US$, `faixas`
  de contexto (< 100k, 100-200k, 200-400k, 400-700k, ≥ 700k) e `modelos` (chamadas por família) (linhas 70-80).
- **Só números?** Sim. As 158 linhas da saída casaram com 4 padrões (cabeçalho, faixas, modelos, linha de sessão); 0 fora
  do padrão. Imprime nome de pasta de projeto, números, famílias de modelo e data/hora (16 caracteres).
- **Rodado** com `--sessoes --desde 2026-09-29` (1,9 s): 12 projetos, 98 sessões (95 começaram até 05/10; 3 começaram
  depois), 5.274 chamadas, ctx0 mediana 69k (mín. 39k, máx. 140k), ctx_med mediana 119k, ctx_max máx. 897k, 4 compactações,
  US$ 938 de soma (53 sessões sem custo), chamadas por família: opus-5-5 4.864; sonnet-5 296; fable-5-1 70; sonnet-5-5 43;
  haiku-4-5 1. Sessões por tamanho: 48 com até 5 chamadas, 15 com 6-30, 28 com 31-200, 7 com mais de 200. Só as 95 que
  começaram na semana: 5.160 chamadas, US$ 893.

## 2. O plugin `session-report`

- **Onde:** `C:\Users\ettor\.claude\plugins\cache\claude-plugins-official\session-report\d4226d062928\skills\session-report\`
  (`SKILL.md`, `analyze-sessions.mjs`, `template.html`); cópia em
  `...\plugins\marketplaces\claude-plugins-official\plugins\session-report\`. Instalado em 06/10/2026 02:47 UTC (escopo
  user), ligado em `settings.json` (`enabledPlugins`). O `node` v24.19.0 está instalado: ele rodaria. **Não foi rodado.**
- **O que mede** (`analyze-sessions.mjs`): tokens (entrada sem cache, cache gravado, cache lido, saída) por total, projeto,
  tipo de subagente e skill; chamadas deduplicadas por `requestId` e `uuid`, com o maior `output_tokens` (linhas 226-230 e
  304-321); mensagens "humanas" (linhas 420-480); horas de relógio e "ativas" (lacunas < 5 min entre quaisquer entradas;
  linhas 50 e 238-241); quebras de cache (> 100k de entrada nova numa chamada; linhas 386-404); subagentes por tipo, lendo
  `.meta.json` (linhas 111-156); skills e comandos `/` com tokens atribuídos (linhas 287-292 e 451-460); os 100 prompts
  mais caros; por dia, o pico de concorrência em janelas de 10 min, usando o intervalo do primeiro ao último evento da
  sessão (linhas 681-720).
- **Custa tokens?** Sim. `SKILL.md` (linhas 12-35): o modelo roda o script, **lê o JSON**, copia o modelo de página,
  **reescreve** o `<script id="report-data">` com o JSON inteiro (Edit) e escreve 3-5 achados e 1-4 recomendações.
  Estimativa para esta semana, com a regra do plugin e sem rodá-lo: 158 prompts, 23 quebras de cache, JSON de ~180 KB, ou
  45 a 60 mil tokens lidos, outro tanto escritos, mais 7 a 9 mil do modelo de página (26 KB). Cerca de 100 a 130 mil
  tokens por relatório.
- **O que o relatório mostra em texto (risco):** `top_prompts[].text` (até 240 caracteres de cada mensagem do humano, sem
  tags) para 100 prompts; `context[]` (texto das ±2 mensagens vizinhas) em cada prompt e em cada quebra de cache (linhas
  482-512 e 651-676); nomes de skill e comando; pasta de projeto e ID de sessão na dica do gráfico; o modo texto imprime
  `"<texto>"` (linha 794). O HTML vai para a pasta atual e o JSON para `/tmp`. Não existe opção para tirar o texto.
  Texto de paciente iria para um repositório e para o contexto de outro projeto (ADR 0001 e 0002).
- **Lacunas para o objetivo:** não conta mensagem digitada com o Claude ocupado (`queued_command`) nem resposta a
  `AskUserQuestion`; conta como humano o lote legado e a saída `<local-command-stdout>`; não tem retorno, trecho nem
  sentada; a concorrência por "span" (mesmo método, recalculado no protótipo; o plugin não foi rodado) dá pico 33 em
  03/10, contra 4 sessões do humano.

## 3. Esquema das transcrições (contagens)

Base: 142 transcrições principais + 418 de subagentes, 131.845 linhas, 601,7 MB, 0 erros de JSON; versões 2.1.234 a
2.1.289. O campo `entrypoint` é `claude-vscode` em todas as 109.846 entradas que o têm: não há sessão de terminal nos
dados. Fuso local UTC-3, sem horário de verão.

| O quê | Como se reconhece | Contagem que confirma |
|---|---|---|
| (a) mensagem digitada pelo humano | `type=user`, `isSidechain` falso, `isMeta` falso, sem `isCompactSummary`, sem bloco `tool_result`, `origin.kind="human"` (com `promptSource="sdk"`, `turnOrigin="human"` nas versões novas; `permissionMode` presente) | 227 entradas; cada uma abre um `promptId` novo (os 278 `promptId` novos de `user` não-`tool_result` vêm dessas 227 + 51 sem `origin`, abaixo) |
| (a') digitada com o Claude ocupado | `attachment.type="queued_command"` com `origin.kind="human"` (`commandMode="prompt"`; `humanTurn=true` em 97); não vira entrada `user` | 106; `queue-operation` `remove` com `reason="absorbed_mid_turn"` em 290; dupla contagem com `user` de mesmo texto (hash) num raio de 10 min: 0 |
| (a'') lote legado, não é humano | `user` sem `origin`, `promptSource="sdk"`; 49 são da v2.1.234; o texto entra por `queue-operation` `enqueue` ≤ 0,6 s antes | 51 no total (49 na v2.1.234); na semana, 49 (classe HL) |
| (b) resultado de ferramenta | `type=user` com bloco `tool_result` (+ `toolUseResult`, `sourceToolAssistantUUID`) | 14.453 no principal (14.070 dict, 337 str, 46 lista), contra 14.454 entradas `assistant` com `tool_use` |
| (c) injetada: `isMeta` | `isMeta=true` | 136 no principal (inclui 20 de `origin.kind="peer"`, 13 `<local-command-caveat>`) |
| (c) injetada: comando `/` | texto começa com `<command-name>` (ou `<command-message>`), `isMeta` falso | 13 no total (todos `/model`); a saída vem como `<local-command-stdout>`: 13 |
| (c) injetada: tarefa em segundo plano | `origin.kind="task-notification"`, texto `<task-notification` | 45 `user` + 126 absorvidas como `queued_command` |
| (c) injetada: resumo de compactação | `isCompactSummary=true` + `system` com `subtype="compact_boundary"` | 5 + 5 no principal (+1 de cada em subagentes) |
| (c) injetada: aviso de gancho | `attachment` (não `user`) com `attachment.type` = `hook_additional_context` ou `hook_success` | 274 e 20 |
| (d) interrupção | `user` com texto `[Request interrupted by user]` ou `... for tool use]` | 3 no principal e 3 em subagentes; `interruptedByShutdown`: 2 |
| subagentes | `<projeto>\<sessão>\subagents\agent-<id>.jsonl` + `.meta.json` (chaves: `agentType, description, toolUseId, spawnDepth, requestShape, requestNonInteractive, model, workflowPhase, parentAgentId`); entradas com `isSidechain=true` e `agentId` | 418 arquivos; 46.009 entradas `isSidechain=true`, todas em subagentes (0 no principal) |
| tempo | `timestamp` de topo, ISO-8601 UTC com ms e `Z` | 112.776 entradas, 0 fora do formato; 4.066 (3,6%) fora de ordem no arquivo: ordenar |
| uso | `message.usage`: `input_tokens`, `cache_read_input_tokens`, `cache_creation_input_tokens`, `output_tokens` (+ `cache_creation.ephemeral_5m/1h`, `server_tool_use`, `iterations`) | presentes em 49.173 de 49.173 entradas `assistant` |
| modelo | `message.model` | ver a lista abaixo |

- **Uma resposta da API = várias entradas `assistant`** (uma por bloco) com o mesmo `message.id`: 49.173 entradas para
  20.342 ids (1 a 32 blocos). Em 16.627 de 16.627 ids com vários blocos, o último bloco tem o maior `output_tokens` e o
  mesmo contexto. Regra: valer a última entrada do id. Nenhum id se repete entre arquivos (0 de 8.776 na semana).
- **Sem timestamp:** `last-prompt, ai-title, atis-latch, file-history-snapshot, cost-state, bridge-session, mode,
  custom-title, agent-name`, o diário de workflows (`started, result, failed, launched`) e `artifact-*`.
- **IDs de modelo:** `claude-opus-5-5`, `claude-opus-5`, `claude-sonnet-5-5`, `claude-sonnet-5` (o "por engano"),
  `claude-fable-5-1`, `claude-haiku-4-5-20251001` e `<synthetic>` (95 mensagens de erro de API). O sufixo `[1m]` não
  aparece em `message.model`; aparece nas chaves de `cost-state.modelUsage` (`claude-opus-5-5[1m]`, `claude-opus-5[1m]`).
  `effort` fica em cada entrada `assistant` (`medium, high, xhigh, max`).
- **`cost-state`** (sem timestamp): em 90 dos 142 arquivos principais (só sessão encerrada normalmente). Chaves:
  `totalCostUSD, totalAPIDuration, totalToolDuration, totalLinesAdded, totalLinesRemoved, totalDuration, startTime,
  modelUsage` (por modelo: `inputTokens, outputTokens, thinkingTokens, cacheReadInputTokens, cacheCreationInputTokens,
  webSearchRequests, costUSD`). Não serve de fonte do total semanal.
- **Limite batido:** 87 mensagens sintéticas com `quotaLimits` (`rateLimitType="five_hour"`, `status="rejected"`):
  4 em 21/09 e 83 em 22/09. Nenhuma de 23/09 em diante.
- **Espera pelo humano (tool_use → tool_result, principal):** `AskUserQuestion` n=75, mediana 229 s, p90 2.756 s, máx.
  33,8 h; `ExitPlanMode` n=23, mediana 67 s, máx. 8,7 h; `Bash` n=8.446, mediana 1,6 s, p90 10,5 s, 3 acima de 10 min.

## 4. Regras por métrica e números da semana 29/09 a 05/10 (terça a segunda, hora local)

Semana = 7 dias de 00:00 a 23:59 locais. Eventos por timestamp, não por arquivo.

**Conjuntos usados.** *Humano estrito* = H + HQ + HC (mensagem digitada, digitada com o Claude ocupado, comando `/`).
*Presença ampla* = estrito + HA (resposta a `AskUserQuestion`/`ExitPlanMode` ou recusa `toolDenialKind="user-rejected"`) + HI
(interrupção). *Trabalho do Claude (W)* = chamada do modelo + resultado de ferramenta, no principal e nos subagentes.
*Evento da sessão* = W + notificação de tarefa + mensagem sintética de erro + presença ampla.

**Classes na semana:** A (chamada) 18.429; T (resultado de ferramenta) 9.652; H 107; HQ 43; HC 5; HA 61; HI 2; N
(notificação de tarefa) 102; HL (legado) 49; X (demais, fora das regras) 14.412; 0 não classificadas.

### 4.1 Tokens por sessão e total da semana
- **Regra:** por arquivo (principal + subagentes somados à sessão-mãe), uma chamada por `message.id` com o uso da última
  entrada, excluindo `<synthetic>`; somar os 4 campos de `message.usage`; janela pelo timestamp da chamada.
- **`medir_uso`:** soma só o contexto (3 campos) por sessão; não soma saída, não tem subagentes nem total semanal.
- **Semana:** total 2.136.128.265 = entrada 16.470 + cache lido 2.091.074.056 + cache gravado 36.677.247 + saída 8.360.492.
  Principal 1.834.066.125; subagentes 302.062.140 (14,1%). Por sessão (98): mediana 519.383, p90 77.643.027, máx.
  154.423.233. Por dia: 288,6 M, 100,9 M, 118,0 M, 34,8 M, 605,0 M, 446,3 M, 542,6 M. Sessões do humano: 99,5% dos tokens;
  as 50 sem mensagem do humano: 121 chamadas, 0,5%.

### 4.2 Contexto mediano por chamada
- **Regra:** `input + cache_read + cache_creation` por chamada; mediana sobre as chamadas da semana, principal e subagentes
  separados. **`medir_uso`:** mediana por sessão e média por projeto; não dá a mediana semanal.
- **Semana:** principais n=5.396, mediana 307.005, p90 616.289, máx. 897.334; subagentes n=1.693, mediana 162.174, p90
  321.199, máx. 449.721.

### 4.3 ctx0 por projeto
- **Regra:** contexto da 1ª chamada do arquivo principal (por timestamp), só sessões do humano cuja 1ª chamada cai na
  semana; agrupar por pasta de projeto. **`medir_uso`:** ctx0 por sessão, sem agrupar, com as sessões automáticas.
- **Semana (45 sessões; mediana 58.394; todas as 95 sem filtro: 68.574, igual ao 69k do `medir_uso`):**

| pasta de projeto | sessões | ctx0 mediana | mín. | máx. |
|---|---|---|---|---|
| C--DESOSP | 15 | 64.515 | 62.499 | 140.235 |
| c--DESOSP-APP | 15 | 55.589 | 53.861 | 62.616 |
| C--CLAUDE-PROJETOS-desosp-censo | 5 | 65.968 | 65.157 | 66.000 |
| c--planilha-hc | 3 | 53.916 | 53.265 | 57.183 |
| c--CLAUDE-PROJETOS | 3 | 45.889 | 44.455 | 105.520 |
| C--CLAUDE-PROJETOS-desosp-app | 2 | 57.053 | 56.163 | 57.943 |
| C--CLAUDE-PROJETOS-desosp-hc | 1 | 55.293 | 55.293 | 55.293 |
| c--CLAUDE | 1 | 46.337 | 46.337 | 46.337 |

O mesmo projeto aparece com 2 ou 3 nomes de pasta depois da reorganização (`c--DESOSP-APP`, `C--DESOSP`,
`C--CLAUDE-PROJETOS-desosp-app`): falta uma tabela pasta → projeto.

### 4.4 Mensagens do humano por sessão (sessão = fase)
- **Regra:** contagem de H, HQ e HC por arquivo principal; HA e HI à parte. **`medir_uso`:** não faz.
- **Semana:** H 107 + HQ 43 + HC 5 = **155** estritas; HA 61; HI 2. 51 sessões com evento do humano: mediana 2, p90 7,
  máx. 10; 24 delas com 1 só mensagem; 47 sessões iniciadas por ele. Fora da conta: 49 mensagens HL (lote legado).
- **Recontagem independente (outro código):** 107 `user` com `origin.kind="human"`, 43 `queued_command` humanos e 4
  `<command-name>` (o protótipo conta 5 porque inclui 1 `<command-message>`).

### 4.5 Retornos (mensagem do humano depois de > 30 min sem evento na sessão)
- **Regra:** por sessão (principal + subagentes), eventos ordenados por timestamp; retorno = evento do humano, que não seja
  o 1º da sessão, com lacuna > 30 min desde o evento anterior. O evento anterior **não** pode ser `attachment`,
  `queue-operation`, `system` nem `file-history-delta` (variante "qualquer entrada": 1 retorno estrito contra 29; em 28 de
  29 havia `total_tokens_reminder` com menos de 2 s de distância). **`medir_uso`:** não faz.
- **Semana:** estrito **29**; amplo **35**. Por dia (estrito, 29/09 a 05/10): 7, 3, 1, 0, 6, 5, 7. Lacuna antes de cada
  evento humano (amplo, exceto o 1º): < 1 min 79; 1-5 min 28; 5-20 min 21; 20-30 min 7; 30-60 min 19; 1-3 h 7; > 3 h 9.
- **Sensibilidade (estrito / amplo):** 10 min 39 / 56; 15 min 35 / 48; 20 min 32 / 42; **30 min 29 / 35**; 45 min 19 / 24;
  60 min 14 / 16; 120 min 8 / 10. Não há platô em 30 min.

### 4.6 Maior trecho do Claude sem ele
- **Regra literal (A):** de cada mensagem do humano estrita até o último W antes da mensagem estrita seguinte (ou o fim
  da sessão). **B:** o mesmo, mas a fronteira é qualquer presença ampla. **C (contínuo):** corridas de W sem lacuna maior
  que 15 min, cortadas por presença ampla. **`medir_uso`:** não faz.
- **Semana:**

| variante | trechos | mediana | p90 | maior | ≥ 1 h | ≥ 2 h | 5 maiores (dia, hora de início, duração) |
|---|---|---|---|---|---|---|---|
| A literal | 144 | 5 min | 50 min | **4h08** | 11 | 3 | 03/10 19:26 4h08; 02/10 20:24 3h14; 05/10 16:12 2h26; 04/10 01:03 1h48; 29/09 18:33 1h32 |
| B | 205 | 3 min | 27 min | **3h14** | 4 | 1 | 02/10 20:24 3h14; 04/10 01:03 1h48; 03/10 19:00 1h20; 29/09 20:52 1h14; 04/10 08:35 0h56 |
| C contínuo | 244 | 2 min | 24 min | **1h48** | 3 | 0 | 04/10 01:03 1h48; 03/10 19:00 1h20; 29/09 20:52 1h14; 04/10 08:35 0h56; 03/10 17:23 0h55 |

- **Por que as três:** o trecho A de 4h08 contém respostas do humano a perguntas (B o parte em trechos de até 1h20); o trecho de 3h14
  (02/10) tem 10 eventos de trabalho e uma lacuna de 3h13 depois de `end_turn`, encerrada por duas notificações de tarefa
  em segundo plano (`N`): é espera, não trabalho. O C é estável: 108 min para lacuna de 10, 15, 30 ou 60 min (56 min com
  2 min; 74 min com 5 min). Nas semanas de 15/09 e 22/09: A 616 e 643 min; B 616 e 139 min; C 57 e 89 min.

### 4.7 Concorrência
- **Regra:** por dia local, janelas de 10 min; contar sessões distintas com ao menos um W (principal ou subagente, que
  entra na sessão-mãe). "Sessão do humano" = o arquivo tem ao menos uma mensagem H ou HQ. Horas com 2+: solto = 2 ou mais
  sessões com W na mesma hora de relógio; janela = 2 ou mais na mesma janela de 10 min. **`medir_uso`:** não faz;
  o `session-report` usa o intervalo primeiro-último evento da sessão.
- **Semana:**

| dia | máx. sessões na janela (bruta) | (do humano) | (do humano, ≥ 10 min de trabalho) | horas com 2+ do humano (solto / janela) | pico por span (método do session-report, recalculado) |
|---|---|---|---|---|---|
| 29/09 | 2 | 2 | 2 | 4 / 3 | 3 |
| 30/09 | 2 | 2 | 2 | 5 / 2 | 3 |
| 01/10 | 1 | 1 | 1 | 0 / 0 | 1 |
| 02/10 | 1 | 1 | 1 | 1 / 0 | 1 |
| 03/10 | **32** | 4 | 3 | 8 / 8 | 33 |
| 04/10 | 6 | 4 | 4 | 6 / 5 | 6 |
| 05/10 | 4 | 4 | 3 | 7 / 7 | 4 |

- **O 32 é um lote:** as 32 sessões ativas em 03/10 às 11:30 são todas de `C--DESOSP`; 31 delas são o lote legado (v2.1.234,
  `claude-sonnet-5` com esforço `xhigh`, 1 mensagem cada, `permissionMode` padrão); o grupo tem mediana de 4 chamadas e de
  0 min de duração, e as 1ªs mensagens ficam entre 10:58 e 11:34, com mediana de 0 s entre inícios consecutivos. O prompt
  entra por `queue-operation`. Não parecem janelas abertas por ele; contam só na coluna "bruta". A 32ª é uma sessão normal
  (opus-5-5, v2.1.286).
- **Semana:** máx. bruta 32; máx. do humano **4** (03, 04 e 05/10); horas com 2+ do humano: solto 31, janela 25, de 60 horas
  de relógio com algum trabalho.

### 4.8 Sentadas
- **Regra:** juntar os eventos do humano de todas as sessões, ordenados; um bloco continua enquanto o intervalo for ≤ 20 min;
  contar blocos por dia (pelo início) e somar (último − primeiro) de cada bloco. Bloco de 1 mensagem dura 0 e conta como
  1. **`medir_uso`:** não faz.
- **Semana (estrito):** **50** blocos, **613 min** somados (cerca de 10h13), 19 blocos de 1 mensagem, maior bloco 1h09.
  Por dia (blocos / min / mensagens): 29/09 10 / 55 / 22; 30/09 6 / 134 / 24; 01/10 4 / 13 / 10; 02/10 2 / 47 / 8; 03/10
  10 / 98 / 26; 04/10 8 / 131 / 27; 05/10 10 / 131 / 38. **Ampla** (com respostas e interrupções): 52 blocos, 12h48.
- **Sensibilidade ao intervalo (estrito, blocos / min):** 5 min 98 / 102; 10 min 75 / 255; 15 min 61 / 425; **20 min 50 / 613**;
  30 min 42 / 810; 45 min 32 / 1.178; 60 min 23 / 1.663. A duração somada não tem platô.

### 4.9 Chamadas por modelo (message.id únicos na semana; principal | subagente)
`claude-opus-5-5` 4.909 | 418; `claude-sonnet-5-5` 43 | 1.248; `claude-sonnet-5` (o "por engano") 296 | 0; `claude-opus-5`
77 | 0; `claude-fable-5-1` 70 | 12; `claude-haiku-4-5-20251001` 1 | 15. Total 7.089. Esforço (principal + subagente):
`opus-5-5` high 2.816, max 1.807, medium 433, xhigh 271; `sonnet-5-5` max 1.197 (quase todos em subagentes), medium 71,
high 13, xhigh 10; `sonnet-5` medium 188, xhigh 108; `fable-5-1` max 54, high 28. **`medir_uso`:** conta chamadas por
família no principal; com a mesma janela de datas ele reproduz o protótipo (conferido: 5.396 chamadas, contexto total
1.826.154.505); não separa subagente nem esforço.
O Haiku quase não aparece em mensagens, mas o `cost-state` o registra em 119 entradas (títulos e resumos em segundo
plano): para tokens de Haiku, usar `modelUsage`.

## 5. `cleanupPeriodDays`

- **Valor atual:** não definido. `C:\Users\ettor\.claude\settings.json` não tem a chave; `settings.local.json` não existe;
  os dois `.claude\settings.json` de projeto (`desosp-app`, `desosp-hc`) não a têm; não há `managed-settings.json`
  (`C:\Program Files\ClaudeCode` e `C:\ProgramData\ClaudeCode` não existem); nenhuma variável de ambiente relacionada.
  Vale o padrão.
- **Padrão e limites (doc em `.md` cru, 06/10/2026):** padrão 30 dias, mínimo 1; `0` falha na validação; para guardar por
  muito tempo, usar um valor alto como 3650 (`settings-reference.md`, entrada `cleanupPeriodDays`, linhas 5837-5851;
  `claude-directory.md`, "Cleaned up automatically", linha 1534). `data-usage.md`, linha 56: o Claude Code guarda as
  transcrições em texto puro em `~/.claude/projects/`, 30 dias por padrão.
- **Quando apaga:** em varredura em segundo plano depois que uma sessão começa (`settings-reference.md`, linha 5839); sem
  mensagem; a sessão sem uso por mais que o prazo some do `/resume`. Se o Claude Code não consegue determinar o prazo com
  segurança (arquivo de configuração ilegível ou com erro na chave), a varredura pausa e o `/status` avisa
  (`claude-directory.md`, linha 1574). `claude -p --bare` não varre (linha 1573). O arquivo
  `C:\Users\ettor\.claude\.last-cleanup` (não documentado) guarda `2026-10-06T16:53:32Z`, 13:53 local: provavelmente a
  última varredura.
- **O que apaga (mais velhos que o prazo):** `projects/<projeto>/<sessão>.jsonl` (e versões `orphaned`/`superseded`),
  `<sessão>/subagents/` (junto com a transcrição-mãe), `<sessão>/tool-results/`, `file-history/<sessão>/` (guarda os 100
  checkpoints mais recentes), `plans/`, `debug/`, `paste-cache/`, `image-cache/`, `uploads/`, `dev-mods/`, `session-env/`,
  `tasks/`, `shell-snapshots/`, relatórios do `/insights` em `usage-data/`, rascunhos de feedback e as pastas legadas
  (`todos/`, `statsig/`, `logs/`). **Não apaga:** `sessions/` (removida ao fechar a sessão), a memória automática
  `projects/<projeto>/memory/`, e o `history.jsonl` (só na configuração HIPAA). Valor muito alto: na prática, nunca apaga
  (a doc não fixa máximo).
- **Idade no disco (por script; só datas e contagens):** 142 transcrições principais, 418 de subagentes. Por idade (mtime):
  até 7 dias 101; 8-14 dias 27; 15-21 dias 14; 22-30 dias 0; mais de 30 dias 0.

| pasta de projeto | principais | subagentes | mtime mais antigo | 1º evento mais antigo (local) |
|---|---|---|---|---|
| C--DESOSP | 86 | 362 | 18/09 | 09/09 |
| c--DESOSP-APP | 28 | 15 | 27/09 | 23/09 |
| c--planilha-hc | 6 | 9 | 28/09 | 26/09 |
| c--CLAUDE-PROJETOS | 6 | 25 | 05/10 | 04/10 |
| C--CLAUDE-PROJETOS-desosp-censo | 5 | 1 | 05/10 | 05/10 |
| C--CLAUDE-PROJETOS-desosp-hc | 1 | 2 | 05/10 | 05/10 |
| C--CLAUDE-PROJETOS-desosp-app | 2 | 1 | 05/10 | 05/10 |
| C--CLAUDE-PROJETOS-claude-kit | 1 | 0 | 05/10 | 05/10 |
| c--CLAUDE | 1 | 3 | 04/10 | 04/10 |
| C--Users-ettor-AppData-Local-Temp (3 pastas de scratchpad e temporária) | 6 | 0 | 03/10 | 03/10 |

- **Tamanho:** `C:\Users\ettor\.claude\projects` = 635,3 MB em 1.264 arquivos (a medição cresce com esta própria janela).
  `file-history` 65,5 MB; `plugins` 26,8 MB; `skills` 17,2 MB; `plans` 0,4 MB.
- **Consequência:** a semana de 08/09 só tem dados a partir de 09/09 (1 sessão, 50 chamadas). O arquivo principal mais
  antigo tem mtime de 18/09, então as transcrições das semanas de 15/09 e 22/09 começam a sumir por volta de 18/10.
  Aumentar o prazo guarda mais texto de paciente em arquivo puro (`claude-directory.md`, "Plaintext storage"); guardar só
  a linha de números resolve sem isso.

## 6. Outros jeitos nativos de ver uso (versão 2.1.289)

| Recurso | O que dá | Serve a uma linha semanal? |
|---|---|---|
| `/usage` (`/cost` e `/stats` são alias; `commands.md` linhas 77, 147 e 163) | Bloco da sessão (custo estimado ao preço de lista, duração da API e de parede, linhas, tokens por modelo); para Pro/Max, barras do plano (sessão e semana) e atribuição por skill, subagente, plugin e MCP, com alternância 24 h/7 dias, calculada do histórico local desta máquina (`costs.md`) | Não: é uma tela, sem saída para máquina; o custo da sessão não é de cobrança para quem tem assinatura |
| Diálogo "Account & usage" no VS Code (`vs-code.md`, "Check account and usage") | As mesmas barras do plano e a atribuição | Não: mesma limitação |
| Status line (`statusline.md` linhas 180-199) | JSON por stdin com `cost.total_cost_usd`, `total_duration_ms`, `total_api_duration_ms`, `context_window.*`, `effort.level`, `session_id` e, só para Pro/Max, `rate_limits.five_hour` e `rate_limits.seven_day` com `used_percentage` e `resets_at`; roda local e não gasta token | Em parte: é a única fonte do % do limite semanal. A doc do VS Code não menciona status line (0 ocorrências): confirmar no terminal antes de contar com isso |
| `claude -p --output-format json` (`headless.md`; `agent-sdk/cost-tracking.md`) | `total_cost_usd` e custo por modelo (`modelUsage`) de cada execução | Não: só para execuções `-p`, não para as janelas interativas |
| `/insights` (`costs.md`, "Analyze your usage patterns") | Relatório HTML de padrões de trabalho (até 200 sessões por rodada), em `~/.claude/usage-data/` | Não: lê as sessões com o modelo, gasta tokens e escreve texto; o relatório não existe aqui (pasta ausente) |
| OpenTelemetry (`monitoring-usage.md` linhas 600-607) | `claude_code.token.usage`, `cost.usage`, `active_time.total`, `session.count`, por modelo | Não por ora: precisa de coletor e exportador |
| `cost-state` nas transcrições | Custo, tempo de API e de ferramenta, tokens por modelo (com `[1m]`) | Só em sessões encerradas (90 de 142 arquivos) |

## 7. O que falta para uma linha por semana

- **Colunas (28 no protótipo):** `semana_inicio, sessoes_com_chamada, chamadas, chamadas_subagente, tok_entrada,
  tok_cache_lido, tok_cache_gravado, tok_saida, ctx_mediano_principal, ctx0_mediano, msgs_humano_estrito,
  respostas_perguntas, retornos_30min_estrito, retornos_30min_amplo, maior_trecho_A_min, maior_trecho_B_min,
  maior_trecho_C_min, conc_max_humano, conc_max_bruta, horas_2mais_humano_janela10, sentadas_estrito,
  sentadas_min_estrito` e uma coluna de chamadas por modelo (6 IDs). **Faltam:** limites batidos na semana
  (`quotaLimits`: 0 nesta), % do limite semanal (status line ou cópia manual do `/usage`), chamadas por esforço, ctx0 por
  projeto em arquivo à parte (formato longo) e a tabela pasta → projeto.
- **Onde gravar:** um CSV no kit, por exemplo `C:\CLAUDE-PROJETOS\claude-kit\medicoes\uso-semanal.csv`, só com números
  (sem texto e sem paciente), uma linha por semana; o script ao lado do `medir_uso.py`.
- **Como rodar:** `python medir_semana.py --inicio AAAA-MM-DD --csv <arquivo>` (a semana de terça a segunda; rodar às terças,
  com `--inicio` na terça anterior). O protótipo já aceita `--inicio`, `--dias`, `--csv`, `--so-linha` e os limiares
  `--retorno-min`, `--sentada-min`, `--gap-continuo-min`. Agendar no Agendador de Tarefas do Windows custa 0 token.
- **Custo:** 1,8 s para uma semana (289 MB); 5,5 s para o histórico inteiro (602 MB). Em tokens: 0 se rodar pelo terminal;
  cerca de 0,5 mil se o modelo rodar e ler só a linha. O `session-report`: 100 a 130 mil por relatório.
- **Linhas já medidas** (para o histórico antes da varredura de 30 dias; 08/09 é parcial, os dados começam em 09/09):

| coluna | 08/09 | 15/09 | 22/09 | 29/09 |
|---|---|---|---|---|
| sessões com chamada | 1 | 13 | 30 | 98 |
| chamadas (subagente) | 50 (0) | 4.671 (2.656) | 7.306 (3.084) | 7.089 (1.693) |
| tokens: cache lido | 6.546.742 | 860.124.846 | 1.968.440.776 | 2.091.074.056 |
| tokens: saída | 66.717 | 5.219.751 | 10.254.735 | 8.360.492 |
| contexto mediano (principal) | 134.638 | 276.457 | 357.070 | 307.005 |
| mensagens do humano (estrito) / respostas | 4 / 0 | 64 / 17 | 103 / 31 | 155 / 61 |
| retornos > 30 min (estrito / amplo) | 0 / 0 | 11 / 14 | 20 / 24 | 29 / 35 |
| maior trecho A / B / C (min) | 34 / 34 / 22 | 616 / 616 / 57 | 643 / 139 / 89 | 249 / 194 / 108 |
| concorrência máx. (do humano / bruta) | 1 / 1 | 2 / 2 | 3 / 3 | 4 / 32 |
| sentadas (blocos / min) | 3 / 4 | 24 / 210 | 50 / 264 | 50 / 613 |
| chamadas por modelo: opus-5-5, opus-5, sonnet-5-5, sonnet-5, fable-5-1, haiku | 0, 50, 0, 0, 0, 0 | 0, 4.548, 0, 0, 103, 20 | 3.827, 3.305, 0, 62, 96, 16 | 5.327, 77, 1.291, 296, 82, 16 |

(A coluna `tok_entrada` é desprezível: 100; 12.202; 17.284; 16.470.)

## Limites desta medição

- Aprovações de permissão não deixam evento próprio (só o atraso do resultado da ferramenta); em modo `auto` (267 de 345
  prompts) quase não há. O tempo de leitura e de raciocínio dele não aparece. Só entra o que está em `~/.claude\projects`
  desta máquina: nada de outro PC, do claude.ai ou do terminal (todas as entradas são `claude-vscode`).
- O 1º evento do humano de cada sessão conta como início, não como retorno. A mensagem digitada com o Claude ocupado entra
  pelo instante em que foi absorvida; o instante da digitação não é conhecido (o `enqueue` só casou por hash num caso).
- As regras 4.4 a 4.8 dependem de `origin`, `promptSource`, `queued_command` e `isMeta`. Mensagens sem `origin` (49 no lote
  da v2.1.234) ficam fora do conjunto humano; se uma versão gravar mensagem digitada sem `origin`, a regra a subconta
  (nas semanas de 15/09 e 22/09 isso foi 2 e 0 mensagens). Revalidar a cada mudança de versão.
- O limiar de 30 min (retorno) e de 20 min (sentada) é convenção: a sensibilidade está em 4.5 e 4.8.

## Fontes (lidas em 06/10/2026)

- Código local: `C:\CLAUDE-PROJETOS\claude-kit\skills\uso-do-claude\medir_uso.py`;
  `C:\Users\ettor\.claude\plugins\cache\claude-plugins-official\session-report\d4226d062928\skills\session-report\SKILL.md`,
  `analyze-sessions.mjs` e `template.html`; `C:\Users\ettor\.claude\settings.json`;
  `C:\Users\ettor\.claude\plugins\installed_plugins.json`; `C:\Users\ettor\.claude\.last-cleanup`.
- Doc do Claude Code (baixada em `.md`): https://code.claude.com/docs/en/settings-reference.md ·
  https://code.claude.com/docs/en/claude-directory.md · https://code.claude.com/docs/en/data-usage.md ·
  https://code.claude.com/docs/en/costs.md · https://code.claude.com/docs/en/commands.md ·
  https://code.claude.com/docs/en/statusline.md · https://code.claude.com/docs/en/vs-code.md ·
  https://code.claude.com/docs/en/headless.md · https://code.claude.com/docs/en/monitoring-usage.md ·
  https://code.claude.com/docs/en/agent-sdk/cost-tracking.md
- Protótipo e scripts de medição (scratchpad da janela de 06/10, não copiados para o kit):
  `C:\Users\ettor\AppData\Local\Temp\claude\c--CLAUDE-PROJETOS\f3f2e21c-058d-4b67-856b-d016fa5d9309\scratchpad\medicao\`:
  `semana.py` (protótipo), `esquema.py`, `esquema2.py`, `esquema3.py`, `diag.py`, `diag2.py`, `idade.py`,
  `agregar_medir_uso.py`, `conferir_tokens.py`, `conferir_humanos.py`, `estimar_session_report.py`, `limites.py`,
  `uso-semanal_prototipo.csv` (as 4 linhas semanais).
