# R1 — o objetivo, a medição e a última varredura de recursos (06/10/2026)

> Janela R1 (notebook, Opus 5.5; aberta por engano na pasta-mãe, nenhum projeto tocado). Grill em duas rodadas (Q34 a
> Q48), feito sobre as três pesquisas da R1. **Confirmado pelo Ettore em 06/10/2026** ("prossiga, confirmo"). O plano
> `2026-10-06_plano-fluxo.md` recebeu só o que está aqui.

## 1. O objetivo (Q34)

Nas palavras do Ettore, ao fechar o F1a: "meu problema nem é tanto ser office boy de prompt, mas precisar dar atenção
integral ao processo. Gostaria de o largar trabalhando por um tempo maior. Prefiro sentar e ser fritado por perguntas e
rodar diversas janelas ao mesmo tempo, pois o tempo foi pontual, e não picado de ter que voltar aqui o tempo todo e
resolver as coisas — mantendo qualidade, economia de tokens e o padrão."

**O objetivo, reescrito e aprovado:** atenção concentrada.
- O Ettore senta poucas vezes, quando ele escolhe, e responde de uma vez o que precisa dele: o grill, o plano e a fila
  de perguntas.
- Entre uma sentada e outra, o Claude trabalha sozinho por horas, em fases curtas encadeadas (nunca numa janela
  gigante) e em tantas janelas quanto o trabalho independente permitir.
- O Claude só o chama quando nada mais anda sem ele.
- Tudo isso mantendo:
  - a qualidade (suítes verdes, regra clínica decidida por ele);
  - a economia (contexto curto);
  - o padrão (ADRs, privacidade, estado em arquivo).

"Longo" quer dizer longo no relógio, com cada fase curta no contexto. É isso que impede o objetivo de brigar com a
economia de tokens.

**Por que a régua mudou.** O plano media os gestos de transporte (no máximo 2 por fase) e o tamanho do contexto. Uma
fase pode ter 2 gestos e mesmo assim chamá-lo 6 vezes fora de hora. Três peças iam contra o objetivo:
- cada ponto da Q10 travava a fase;
- o plano limitava a "no máximo duas janelas";
- o F1b tinha paradas no meio.

## 2. A régua (Q34, Q39)

Medida toda semana (terça a segunda) por `scripts\medir_semana.py`, com só números gravados em
`metricas\uso-semanal.csv`. As metas são conferidas nas semanas depois do F5b, o primeiro uso real do laço completo.

| medida | definição | base (29/09 a 05/10) | meta |
|---|---|---|---|
| retornos | mensagem dele depois de mais de 30 min sem evento na sessão (a 1ª da sessão não conta) | 29 na semana; por dia 7, 3, 1, 0, 6, 5, 7 | metade |
| sentadas | as mensagens dele de todas as sessões, em blocos com intervalo de até 20 min | 50 blocos, 613 min | metade dos blocos |
| maior trecho sem ele | o trabalho do Claude em qualquer sessão, sem lacuna maior que 15 min, cortado por qualquer presença dele em qualquer sessão | 92 min (mediana de 3 min) | o dobro (cerca de 3 h) |
| janelas ao mesmo tempo | o máximo de sessões dele com trabalho na mesma janela de 10 min, por dia | 4 | sobe quando há trabalho independente |
| contexto mediano por chamada | entrada + cache lido + cache gravado; a mediana da semana, na janela principal | 307 mil | até 120 mil |
| ctx0 por projeto | o contexto da 1ª chamada; a mediana por projeto | mediana de 58 mil | a do plano (F5a, F6, F7) |
| modelo fora do previsto | chamadas no Sonnet 5 por engano e no Opus 5 (rebaixamento silencioso) | 296 e 77 | 0 |
| gestos por fase (secundária) | os passos manuais de transporte | cerca de 7 | no máximo 2 |

- **Variantes:** o CSV guarda os retornos com 20 e 60 min e as sentadas com 10 e 30 min. Assim uma definição pode mudar
  depois sem as transcrições.
- **Fora das medidas de interação:** as sessões automáticas (o lote de 03/10) entram só nos tokens.
- **A régua e os limites de cada medida:** `pesquisas\2026-10-06_medicao-semanal-de-uso.md`, §4 e "Limites desta
  medição".

**Linha de base** (`metricas\uso-semanal.csv`; a semana de 08/09 é parcial, porque os dados começam em 09/09):

| semana (terça) | sessões | chamadas (de subagente) | contexto mediano | mensagens dele / respostas | retornos (estrito / amplo) | sentadas (blocos / min) | maior trecho global / mediana (min) | janelas dele ao mesmo tempo | Sonnet 5 / Opus 5 | esforço max / xhigh | limites batidos |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 08/09 (parcial) | 1 | 50 (0) | 134.638 | 4 / 0 | 0 / 0 | 3 / 4 | 22 / 6 | 1 | 0 / 50 | 0 / 50 | 0 |
| 15/09 | 13 | 4.671 (2.656) | 276.457 | 64 / 17 | 11 / 14 | 24 / 210 | 43 / 3 | 2 | 0 / 4.548 | 694 / 2.522 | 4 |
| 22/09 | 30 | 7.306 (3.084) | 357.070 | 103 / 31 | 20 / 24 | 50 / 264 | 80 / 4 | 3 | 62 / 3.305 | 2.055 / 3.829 | 83 |
| 29/09 | 98 | 7.089 (1.693) | 307.005 | 155 / 61 | 29 / 35 | 50 / 613 | 92 / 3 | 4 | 296 / 77 | 3.058 / 389 | 0 |

- **Como se conferiu:** o `scripts\medir_semana.py` reproduziu sem nenhuma diferença os números da pesquisa (§4 e §7):
  112 de 112 valores do protótipo, 96 de 96 da §7 e 32 de 32 da §4. A conta das 4 semanas levou 12 s.
- **O trecho global** fica abaixo do trecho por sessão (108 min em 29/09), porque qualquer presença dele, em qualquer
  janela, o corta.
- **O Opus 5** era o modelo em uso até a semana de 22/09, quando aparece o Opus 5.5. O "rebaixamento" só vale a partir
  da semana de 29/09.

## 3. As decisões

| # | decisão | o porquê e a nuance do Ettore |
|---|---|---|
| Q34 | **(a)** O objetivo e a régua das seções 1 e 2; os gestos por fase passam a medida secundária. | Aceito como proposto. |
| Q35 | **(a) Fila.** A dúvida vai para `docs\PERGUNTAS.md` (o problema, as opções, a recomendação e o que depende dela), e a fase segue com o que não depende. A fase só para quando tudo o que sobra depende da fila; aí grava o `ESTADO.md`, avisa e fecha. Os pontos da Q10 continuam **proibidos sem o "sim"**, mas deixam de travar o resto. "Mesmo erro depois de 2 tentativas" estaciona só aquela linha de trabalho. A decisão técnica de rotina continua decidida e anotada. | O perigo é executar a ação, não seguir com o resto. Vale a partir do F2, garantido por gancho (Q46). |
| Q36 | **(a)** O `PROXIMO.md` ganha "Decisões pré-aprovadas" (situação → o que fazer → limite) e "Sempre me pergunte". Todo grill e toda aprovação de plano terminam com uma **rodada de contingências** aprovada em lote. | É a Q21 generalizada: as perguntas da execução respondidas antes dela. A regra global "decisão técnica de rotina se resolve sem perguntar" continua. |
| Q37 | **(a)** Tantas janelas quanto houver trabalho independente, com um escritor por projeto (ou por worktree, até 3 no mesmo projeto). Depois do F5b, F6 ∥ F7 (∥ N1). | "Não faz mal gastar a cota mais rápido se o trabalho for feito mais rápido (…) prefiro ter 4 tratores e tampar mais rápido, desde que a qualidade e eficiência sejam exatamente as mesmas (…) contanto que o gasto de tokens seja o mesmo, ou menor." Três fatos ajustam a conta: a cota semanal é o tanque (o paralelo não o aumenta, só o esvazia antes); no limite de 5 h, só uma janela retoma sozinha (relato de macOS, #92004; no Windows, o F3a confere) e a `--bg` nem espera; e os tokens só ficam iguais em trabalho independente. O F3a mede série × paralelo. |
| Q38 | **(b)** A andrej-karpathy-skills vira o **4º executor do F3b**, por `--plugin-dir`, sem instalar. | "Vamos pelo menos testar os resultados com a skill para validar se ela de fato faz diferença." **Critério fixado antes do teste:** com os mesmos testes verdes, ela entra (no F3c, no `config\plugins.json`) se gastar pelo menos 20% menos tokens ou fizer claramente menos mudanças fora do pedido (contadas pelo revisor cego), sem parar mais na decisão plantada. Com uma tentativa por executor, só um efeito grande aparece (dito antes da escolha). |
| Q39 | **(a)** A linha semanal automática, com as colunas, as definições e as metas da seção 2. | Pediu junto a planilha e o balanço automático a cada 15 dias (Q42). |
| Q40 | **(b)** O session-report fica **só nas pastas de teste** (`teste-fluxo`, `teste-ferramentas`), sempre com `--dir` na pasta das transcrições daquele projeto. Um gancho do projeto barra o comando sem `--dir`, e o HTML vai para o `.gitignore`. | A recomendação era tirá-lo. O risco foi dito uma vez: ele lê as transcrições de todos os projetos e grava no HTML o texto dos 100 prompts mais caros. O contorno existe porque o script aceita `--dir` (`analyze-sessions.mjs:12,45`). O custo de 100 a 130 mil tokens por uso continua. |
| Q41 | **(b)** `cleanupPeriodDays: 90` até o F9, que o devolve a 30. | A recomendação era manter 30. Gravado na R1, com backup. |
| Q42 | **(a)** A planilha `metricas\uso.xlsx` sai do CSV (openpyxl, já instalado; fora do git). A cada 15 dias, o gancho de abertura avisa que o balanço venceu (e, depois do F3c, lança uma sessão curta no kit). O balanço grava `metricas\balancos\AAAA-MM-DD.md` e põe cada ajuste proposto na fila do kit. A próxima janela mostra uma linha só com números. | "Tudo automático, com ganchos automáticos." A opção de voltar a esta janela ficou de fora: ela relê o contexto sem cache e envelhece. |
| Q43 | **(c)** Aviso só pelo **Remote Control mais o `PushNotification`**. Onde o Remote Control não ligar sozinho, não há aviso. | "Se o Claude conseguir ativar remote control, consigo decidir pelo celular; se não conseguir, o aviso não me serve muito (…) preciso voltar ao PC para resolvê-lo, então deixaria sem aviso." O fato: `remoteControlAtStartup: true` liga o Remote Control em toda sessão interativa. Ainda não conferido: o painel do VS Code e a `--bg` (F1b e F3a). |
| Q44 | **(a)** `/goal` "portão ou fila" em toda fase de execução; a linha vem pronta no `PROXIMO.md`. | O portão `Stop` impede fechar sem estado; o `/goal` impede parar antes da hora. |
| Q45 | **(a)** A sonda por arquivo (pesquisa uma vez; as janelas leem), mais um aviso ao vivo de "pronto" (`SendMessage`) só dentro do mesmo domínio (ADR-0002). | A ideia é dele ("uma sonda às vezes serve a duas janelas"), com a condição: "precisa de fato economizar ou tempo ou tokens; se não entendermos que isso acontece, não vale tentar". O F3a mede; sem ganho, sai. |
| Q46 | **(c)** O F1b e o F2 rodam **como no plano**, com as paradas. O modelo novo (fila, pré-aprovação, `/goal`) só vale com os controles: os ganchos do F2 e o laço do F3. | "Corremos o risco de perder o trabalho (…) ou gastar recurso extra. Melhor não aplicar agora, guardamos para quando for possível fazer com os controles." A frase da janela "tudo se desfaz pelo git" queria dizer que qualquer erro se desfaz; foi esclarecida, e ele confirmou o entendimento. |
| Q47 | **(b)** A Frente 2 continua como está; os grills N1 a N5 não se adiantam. | A recomendação era adiantar os grills. |
| Q48 | **(a)** O Remote Control vale em **todos os projetos, inclusive os `desosp-`**. | ADR-0001 D8: o risco, os contornos e o texto do aviso. |

## 4. O confronto com o plano (o que o prompt da R1 pediu)

- **Q2 (b):** continua. "Para só em decisão ou falha" passa a "a decisão vai para a fila; a fase para quando tudo o que
  sobra depende dela", a partir do F2.
- **Q9:** o encadeamento continua. O F3a compara dois jeitos de lançar a fase seguinte, e o F3c escolhe:
  - por `--bg`;
  - por uma sessão interativa numa aba nova do terminal, que tem o Remote Control e espera o limite de uso.
- **Q10:** a lista continua como "nunca sem o 'sim'" e deixa de travar a fase (Q35).
- **Limite de duas janelas:** passa a ser posse de arquivo e total de tokens (Q37).
- **Celular:** Remote Control ligado sozinho, mais o `PushNotification` nos três casos (Q43, Q48).
- **`/goal`:** em toda fase de execução (Q44).
- **Pré-aprovações:** no `PROXIMO.md` (Q36), como a Q21 faz com a escrita em dado real.

## 5. O que muda em cada fase

- **F1b:**
  - na abertura, conferir se o Remote Control ligou sozinho (painel e terminal);
  - nas paradas, um `PushNotification` "claude-kit · F1b · precisa de você";
  - o session-report sai do escopo de usuário e entra no `config\plugins.json` com escopo de projeto (Q40);
  - o resto, como no plano (Q46).
- **F2:**
  - **medição:** `medir_semana.py` completo, planilha, gancho semanal sem imprimir nada, aviso dos 15 dias,
    `metricas\BALANCO.md`, e a statusline anotando o % de 5 h e o semanal;
  - **fila:** o modelo de `PERGUNTAS.md`, o protocolo no `fechar-janela` e no `orquestrar`, e os ganchos
    `PermissionRequest` e `PreToolUse` em `AskUserQuestion`. Os ganchos só adiam, nunca escolhem, e são testados por
    JSON. O `Stop` passa a aceitar fechar com a fila gravada;
  - **`PROXIMO.md`:** com as duas seções e a linha `/goal`; a rodada de contingências na nossa skill;
  - **aviso:** a regra da D8;
  - **janelas e sonda:** na `orquestrar`;
  - **pastas de teste:** o session-report com o gancho do `--dir`;
  - **esforço dos subagentes:** conferir se o subagente herda o esforço da janela e, se der, fixar o esforço por papel.
- **F3a:**
  - lançar a fase 2 por `--bg` e por aba interativa, conferindo o Remote Control, o aviso e o limite de uso;
  - a fila, com duas decisões plantadas;
  - o `/goal` numa sessão `--bg`;
  - as mesmas 3 fases em série e em paralelo;
  - a sonda;
  - a medição pelo `medir_semana.py`;
  - o portão passa a ser "retornos e trecho medidos; a fila funcionou".
- **F3b:**
  - o 4º executor com a andrej-karpathy-skills, pelo critério da Q38;
  - o revisor cego conta as mudanças fora do pedido e as paradas à toa em todos os executores;
  - a medição pelo `medir_semana.py`, e o session-report só com `--dir`.
- **F3c:**
  - decide a andrej-karpathy-skills e a sonda pelos critérios;
  - escolhe o jeito de lançar fases;
  - escreve a parte "depois do F3" do `COMO_OPERAR.md`, com a fila, o aviso, o balanço e as janelas;
  - liga o balanço automático junto com o lançamento.
- **F9:** o `cleanupPeriodDays` volta a 30 (backup antes); a `/retro` usa o `metricas\` e os balanços.

## 6. Achados da medição que viram tarefa

- **Esforço `max`:** na semana de 29/09, o Opus 5.5 fez 1.807 chamadas em `max`, e o Sonnet 5.5 fez 1.197, quase todas
  em subagentes. Tudo indica que os subagentes herdam o esforço da janela. Fica com o F2 (o esforço por papel). Esta
  própria janela rodou em `max`, e o prompt da R1 pedia `high`.
- **Opus 5:** 77 chamadas, provavelmente o rebaixamento silencioso. A linha semanal as destaca, e o gancho do F2 avisa.
- **Nomes de pasta:** o mesmo projeto aparece com 2 ou 3 nomes de pasta depois da reorganização. O mapa está em
  `metricas\pastas-projetos.csv`.
- **Lote de 03/10:** 31 sessões (Sonnet 5 pelo atalho, uma mensagem cada). Ficam fora das medidas de interação.
- **O que o `medir_uso.py` não vê:** os subagentes (14% dos tokens) e a saída. O `medir_semana.py` cobre os dois.

## 7. Os vereditos da varredura que viram Ficha

- **AGORA:**
  - os ganchos da fila (`PermissionRequest`, `PreToolUse` em `AskUserQuestion`);
  - o `/goal`;
  - o Remote Control mais o `PushNotification`;
  - a medição semanal, a planilha e o balanço;
  - a espera do limite de uso, que já vem ligada: só a sessão interativa a tem.
- **QUANDO:**
  - a andrej-karpathy-skills, pelo critério do F3b;
  - as mensagens entre sessões, se o F3a mostrar ganho;
  - o `askUserQuestionTimeout`, para uma sessão interativa largada;
  - o OpenTelemetry só com métricas, se a medição por transcrição não bastar;
  - o herdr, acima de 3 sessões de terminal;
  - a janela coordenadora, acima de 3 ou 4 janelas.
- **NÃO:**
  - ntfy, toast, Telegram e Pushover: não deixam responder pelo celular (Q43);
  - ccusage: repete a medição;
  - `/insights`: gasta tokens e escreve texto de todos os projetos;
  - claude-squad e ccmanager: não têm Windows nativo;
  - Nimbalyst: telemetria e servidor de sincronia;
  - Vibe Kanban: a empresa encerrou;
  - Channels: exige Bun e manda texto a terceiros;
  - BurntToast: arquivado.

## 8. As pesquisas

- `pesquisas\2026-10-06_andrej-karpathy-skills.md`
- `pesquisas\2026-10-06_medicao-semanal-de-uso.md`
- `pesquisas\2026-10-06_varredura-final-atencao-concentrada.md`

## 9. Sinais de insuficiência do modelo (R1)

Nenhum. Houve duas imprecisões de comunicação, corrigidas na própria janela:
- a issue #92004 foi citada sem a ressalva de que o relato é de macOS;
- a frase "tudo se desfaz pelo git" saiu ambígua (Q46).
