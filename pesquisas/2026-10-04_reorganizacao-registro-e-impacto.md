# A reorganização das pastas — o registro de 30/09 e o tamanho do impacto (foto de 04/10/2026)

- **Pergunta:** o que foi decidido em 30/09 sobre juntar as pastas dos projetos numa pasta-mãe, o que falta,
  quanto do código e da configuração depende dos caminhos atuais, e se é o momento de fazer.
- **Data:** 04/10/2026
- **Projeto que pediu:** entrevista das cores de pasta (notebook).
- **Fontes:** levantamento local, sem internet — `C:\DESOSP_APP\docs\HANDOFF_APP.md` (seção L990–L1001),
  transcrições de 30/09, busca dos caminhos nos três repositórios e em `C:\CLAUDE`, `~\.claude\projects`,
  `~\.claude\settings.json`, `~\.claude.json`, `schtasks`, atalhos `.lnk`, `git status` e `git log`.
- **Conclusão:** decidido em 30/09 (pasta-mãe com `desosp-censo`, `desosp-app`, `desosp-hc`, `dados-app`),
  nada executado, sem data e sem aviso aos projetos. São ~1.050 menções aos caminhos, mas dois terços em
  documentos históricos; o código depende de poucos pontos (o kernel tem um ponto central; o app, um central
  mais cópias; a planilha, nenhum). Fora dos repositórios: a memória do Claude presa ao nome da pasta, o
  `.venv` do app, os guias em Word, GitHub Desktop e VS Code. Risco novo: se a mãe se chamar `C:\DESOSP`, todo
  caminho esquecido erra em silêncio. Tem de ser mover, nunca reclonar. (Depois deste levantamento, em 04/10,
  o Ettore escolheu um nome novo para a mãe e fazer a mudança no mesmo dia.)
- **Conferir de novo depois de:** qualquer commit nos três repositórios (é uma foto de 04/10/2026, 10:43).
- **Como foi feita:** subagente Explore (Sonnet), 140 chamadas de ferramenta. O texto abaixo é o relatório
  dele, sem mudança de conteúdo.

---

**Convenções.** K=`C:\DESOSP` · A=`C:\DESOSP_APP` · R=`C:\DESOSP_APP_REAL` · P=`C:\planilha-hc` ·
CL=`C:\CLAUDE`. Dia: domingo 04/10/2026; instantâneo 10:43-10:47. Tudo somente leitura, nenhum dado clínico
copiado. **[novo]** = item que não consta na lista de pendências do plano (A\docs\HANDOFF_APP.md L1001).

## 1. O registro da decisão

| Fato | Fonte |
|---|---|
| **Decidido em 30/09 às 17:40 (hora local; a nota diz "noite")**, por pergunta estruturada. *Quando* = "Depois do censo de 6ª". *Arrumação* = "C:\DESOSP com 4 dentro". Alvo: `C:\DESOSP\{desosp-censo (era K), desosp-app (era A), desosp-hc (era P), dados-app (era R, fora de todo repositório)}` mais a legenda de cores na raiz. | A\docs\HANDOFF_APP.md L1001 (seção L990); transcrição `~\.claude\projects\c--DESOSP-APP\cdda1cf7-….jsonl` L329/L333 |
| Origem: 30/09 às 11:09 o Ettore pediu que o Claude renomeasse as pastas para os nomes do GitHub ("pode mudar você e enviar informação aos demais"). Ele já renomeara o repositório para `desosp-hc`. | sessão `15a63646-…` L922; A\docs\para_a_planilha\AP-006…md §1 |
| **Pendente** ("janela própria depois do censo de 6ª, Opus·médio"): K vira `desosp-censo` dentro da pasta-mãe; recriar o `.venv` do app; trocar caminhos (`app/config.py` PADRAO_REAL e kernel, `.bat`, CLAUDE.md e guias dos três, memória em `~\.claude\projects\`); mapa `icones_pastas.py` e LEGENDA; testes dos três (um por vez) e censo de prova; AK e AP com a ordem de cada projeto. **Nada executado** (não existe `C:\DESOSP\desosp-*`). **Sem data**: não está no calendário (A\docs\PROJETO_FRONT_DESOSP.md §7.1, L2029-2038) nem em prompt. **Sem AK/AP**: o AP-006 §2, nos dois repositórios, ainda diz "em aberto"; AP-007/008 tratam de ícones e HC. | idem |
| **Análise de impacto: só qualitativa.** É a lista acima mais a pergunta de 17:37 (venv, atalhos, caminhos app→censo, config da planilha, memória por nome de pasta, censo de prova). Cenário vizinho, mover os projetos para CL: CL\LEIA-ME.md L46-57 (03/10) cita memória por caminho, "C:\DESOSP em centenas de lugares" e histórico que fica no caminho velho. Sugere uma janela por projeto (planilha, app, censo), diferente do plano de uma janela só. Nenhuma contagem nem inventário externo existia. | idem; CL\LEIA-ME.md |
| Nenhum CLAUDE.md, regra, handoff do kernel/planilha ou memória cita a decisão (só o HANDOFF_APP). Regra em tensão: "Uma janela pertence a um projeto só" (K\docs\HANDOFF_SPRINT2.md L3-14); esta janela toca quatro. | grep nos 3 repos, CL e 3 `memory\` |

## 2. Tamanho do impacto

### 2a. Ocorrências em repositório (arquivos / ocorrências)
Regex `(C:|/c)(\|\\|/)(DESOSP|DESOSP_APP|DESOSP_APP_REAL|planilha-hc)`, sem distinguir maiúsculas. Excluídos
`.git`, `.venv`, `node_modules`, caches e pastas de dado.

| Tipo | K | A | P | CL |
|---|---|---|---|---|
| Código .py | 4/12 (2 executáveis: `desosp\CONFIG_DESOSP.py:57`, `docs\scripts\REF_medir_relevancia_hd.py:14`) | 10/52 (31 executáveis: `scripts\icones_pastas.py` 23, `app\config.py` 2, `puxar.py` 3, `iniciar.py` 1, `anotacoes.py` 1, `paletas_escolhas.py` 1) | 0 | 2/3 (docstring) |
| Testes | 1/12 (9 executáveis; `tests\test_regressoes.py:5265-5277` fixa `RAIZ=='C:\\DESOSP'`) | 8/12 (docstring); 20 arquivos de teste usam as constantes (57 linhas) | 0 | - |
| Gerador do guia | 1/3 (`docs\guia\gerar_guia_rodada.py` L488/508/513, texto do guia) | - | - | - |
| Config (.json/.toml/.ini/.cfg, settings do projeto) | 0 | 0 | 0 | 0 |
| Ganchos (`.claude\hooks`, `.githooks`, `scripts\git`, `.git\hooks`) | 0 | 0 | 0 | - |
| Skills | 0 | 0 | - | 4/5 |
| Regras `.claude\rules` | 2/3 | 0 | - | - |
| Lançadores .bat | - | 1/2 (`iniciar_app_real.bat`) | - | - |
| Docs vivos (.md) | 3/9 | 16/239 | 3/8 | 1/6 |
| Docs históricos/append-only (HANDOFF, AT/AK/AP/PA/KP, INDICE) | 44/180 | 57/461 | 15/54 | - |
| Outros (.gitignore, `ajuda.html`, html) | 1/1 | 3/5 | 0 | - |
| **Total** | **56/220** | **95/771** | **18/62** | **7/14** |

- Dos 1.053 hits, 695 estão em documentos históricos, que a política manda não reescrever (AP-006 §3).
- Variantes (K/A/P/CL): barra invertida 207/738/62/14; string Python `\\` 13/33/0/0; `/` ou `/c/`: 0;
  `c:` minúsculo: 0.
- Top-10 em K: HANDOFF_SPRINT2 47 · test_regressoes 12 · CONFIG_DESOSP 9 · AK-003 8 · CLAUDE.md 7 · AT-020 7 ·
  AK-005 7 · AT-005 6 · AK-002 5 · KP-001 4.
- Top-10 em A: HANDOFF_APP 276 · PROJETO_FLUXOS 79 · PROPOSTA 39 · APRESENTACAO 25 · icones_pastas.py 23 ·
  CLAUDE.md 16 · PROJETO_FRONT 14 · PLANO_REVISTO 12 · REFERENCIA_TECNICA 12 · config.py 11.
- Top-10 em P (todos .md): AP-005 6 · CLAUDE.md 5 · AP-001 5 · PA-001 5 · AP-002/008, KP-001/002 4 cada ·
  AP-003/004 3 cada.
- CL (7 arquivos): LEIA-ME 6 · perguntas_controle.py 2 · uso-do-claude/SKILL.md 2 · 4 arquivos com 1.
- Fora do total, em P: `trabalho\` 14 (10 arquivos), `historico\` 16, `modelos\` 1.
- **Ponto central?** Em K, sim: `CONFIG_DESOSP.py:57` (`RAIZ = DESOSP_RAIZ or r"C:\DESOSP"`), e a raiz do
  código vem de `__file__`. Em A, central com duplicatas: `app\config.py:33` (PADRAO_KERNEL) e `:236`
  (PADRAO_REAL), com overrides `DESOSP_KERNEL`/`RAIZ`/`TERMINAL`. As duplicatas são o `.bat` (fixado por
  `tests\test_iniciar.py:202`), `icones_pastas.py` e os textos de ajuda (`app\templates\ajuda.html:189-190`).
  Em P, nenhum caminho absoluto em código; roda "da raiz do repositório" (P\CLAUDE.md L57).

### 2b. Fora dos repositórios

| Item | Fato |
|---|---|
| `~\.claude\projects\` | `C--DESOSP`: memory 16 arquivos/84,5 KB; 92 sessões + 362 de subagentes; 344 MB. `c--DESOSP-APP`: 6 arquivos/7,7 KB; 28+14; 135 MB. `c--planilha-hc`: 3 arquivos/2,9 KB; 6+9; 38 MB. Mais 3 chaves de Temp/scratchpad com memory vazia. Sem chave para R nem CL (nunca abertos no Claude Code). A memória de `C--DESOSP` tem 38 caminhos escritos em 8 arquivos. |
| `~\.claude\settings.json` | Sem hooks nem additionalDirectories. 4 das 12 regras `allow` citam `C:\DESOSP` ou `c--DESOSP` (Read da memória, 2 scratchpads, 1 Copy-Item), todas ad hoc. |
| `~\.claude.json` | 3 ocorrências, só chaves de `projects`: `C:/DESOSP`, `c:/DESOSP` (duplicada por maiúscula), `C:/DESOSP_APP`. Há também `c:/conversation-core`. Sem chave de P, R ou CL. Cada chave guarda trust, allowedTools e MCP. |
| Tarefas agendadas | 278 lidas; 0 citam DESOSP/planilha/python/claude. Run, serviços, PATH, variáveis de ambiente e perfis de shell: 0. |
| `.lnk` | Área de Trabalho (OneDrive\Desktop, 10), Menu Iniciar (33+67), Pública (7), Links, Barra e SendTo: **0 apontam**. Recentes: 98 de 258 (K 59, A 30, P 9), automáticos. Acesso Rápido: nada fixado; 3 pastas frequentes de K (`entrada`, `saida\0110_M`, `saida\0210_M`) e 15 arquivos recentes. |
| `.code-workspace` / editores | 0 arquivos `.code-workspace`. O VS Code lembra K, A e P (`workspaceStorage` + `storage.json`, 6 refs). O GitHub Desktop tem K, A e P registrados. |
| `%LOCALAPPDATA%\DESOSP` | `icones_pastas\` com `codigo.ico` 4.204 B, `leitura.ico` 3.270 B, `deposito.ico` 3.264 B. Existem 26 `desktop.ini` nas pastas (25 do pacote + 1 alheio em `K\docs\gpt`). |
| Fora da decisão | `C:\DESOSP ARQUIVO` (0 referências nos repos; ficará ao lado da mãe com nome parecido) e `C:\conversation-core`. As junções `~\.claude\skills\*` e o hardlink do CLAUDE.md apontam para CL e não mudam. |

### 2c. O que mais depende do nome atual
1. **[novo] `C:\DESOSP` passa a ser a pasta-mãe, então constante esquecida não falha: erra em silêncio.**
   - Em `A\app\config.py`, `_areas_de_teste` (L60), `_e_do_kernel` (L110), `_e_dado_real` (L132) e
     `estado_da_raiz` (L254) tratam tudo dentro de `PADRAO_KERNEL` como produção. Com ele inalterado,
     `dados-app` e `desosp-app\workspace_dev` viram "kernel" e o pytest recusa `workspace_dev`.
   - `A\app\dominio\exportar.py:139` faz `mkdir(parents=True)` em `raiz_terminal()\entrada`, então exportaria
     insumos para a mãe.
   - Em K, `CONFIG_DESOSP.py:57` inalterado aponta a RAIZ de dados para a mãe. O guarda do pytest
     (`K\tests\conftest.py`) olha as pastas do repositório, não `CONFIG.RAIZ` (inferência: ficaria cego).
   - Mudam juntas: 3 constantes e 3 testes que fixam valores (`test_regressoes` 5265-5277, `test_raiz_real`
     24-27, `test_iniciar` 202).
2. **[novo] Memória e sessão.** A chave de `C:\DESOSP` é `C--DESOSP`, a mesma do kernel hoje.
   - O kernel em `desosp-censo` nasce sem memória nem histórico (chave esperada `C--DESOSP-desosp-censo`).
   - Uma sessão aberta na mãe carregaria a memória do kernel e enxergaria `dados-app\` (dado real). Hoje R é
     irmã de K/A/P, fora do alcance de busca.
   - A justificativa de R ficar "fora de todo repositório" (L1001) não se apoia em nenhuma regra deny (não há
     nenhuma).
3. **[novo] Banco do app** (`R\desosp_app.db`): 289 valores com caminho absoluto em 6 colunas.
   - Colunas: `insumo.caminho` 100, `mensagem.caminho` 119, `execucao.pasta`/`censo_xlsx` 33+33,
     `puxada.origem`/`destino` 2+2.
   - Nenhum código encontrado que reabra arquivo por elas (inferência: é auditoria).
   - `R\_RAIZ_REAL.json` guarda `origem: C:\DESOSP` (informativo).
   - Os manifestos do kernel (`K\arquivo\**\_RODADA.json`: 66 JSON, 346 ocorrências) são tolerados: o
     arquivador procura o nome do arquivo (`arquivo_rodada.py::_insumo_desta_raiz`, 01/10).
4. **[novo] Execução.**
   - Como a mãe tem o nome do K atual, é preciso renomear K para um nome temporário, criar a mãe e mover os
     quatro. Mesmo volume, então instantâneo; caminho mais longo 141 caracteres, sem risco de MAX_PATH.
   - Tem de ser mover, não reclonar. Só existem no disco, fora do GitHub: `entrada/saida/arquivo/historico/fontes`
     do K, `desosp\local_nomes.json`, `local_nomes.json` e `.venv` do A, `docs\para_o_app` e `docs\fontes\*`
     do A, `planilhas/privado/historico` da P.
5. **[novo] Ferramentas e estado gravado.** GitHub Desktop (3 repos), VS Code, trust e allowedTools em
   `~\.claude.json`, e as 98 entradas de Recentes.
6. **Guias e `.venv`.**
   - `.venv` do A: 16 `.exe` de console, `activate*` e `pyvenv.cfg` embutem `A\.venv`. As 2.118 `.pyc`
     também, mas são inócuas. K usa o Python global.
   - O gerador do guia grava em caminho relativo; é preciso regenerar `docs\GUIA_DA_RODADA.docx` e
     `entrada\_GUIA_DA_RODADA.docx` (50.367 B, 04/10 09:47). Exige python-docx via `--target` e conferência
     no Word.
   - **[novo]** `P\GUIA_DE_TRABALHO_COM_O_CLAUDE.docx` tem 3 menções a `C:\planilha-hc` e nenhum gerador no
     repo. A ajuda do app (`ajuda.html`) mostra os caminhos ao usuário.
7. Regra "rodar da raiz (`C:\DESOSP`)": só em K\CLAUDE.md L48. Os comandos de A (CLAUDE.md L168-172) usam
   `C:\DESOSP_APP\.venv\...` por extenso.
8. Ícones: o mapa `PASTAS` tem 25 caminhos, dos quais 23 mudam e 2 são CL. Os `.ico` e `desktop.ini`
   sobrevivem à renomeação. O `--remover` com o mapa velho não acharia as pastas.

## 3. O momento (04/10, 10:43)

| Repo | Branch | `git status --short` | À frente de origin/main* | Sessão mais recente |
|---|---|---|---|---|
| K | main | 3 (D, R, `??` em `docs/gpt/`); eram 1 às 10:30 | 2 (`fe1edc1` 10:22, `9f2eb5e` 10:39) | `b09b59bd`, 04/10 10:30, viva ("busy") |
| A | main | 0 | 0 (`547e32d` 09:27) | `75a5501a`, 04/10 10:08, viva ("busy" às 10:40) |
| P | main | 9: `M docs/para_a_planilha/INDICE.md`; `??` AP-007, AP-008, INDICE_KP, KP-001, KP-002, 3x `desktop.ini` | 0 (`c6bc80f` 03/10) | `80720e07`, 03/10 11:14:57, sem sessão viva |

*Contra a ref local `origin/main`, sem `fetch`.

- **Em execução no instantâneo:** 3 sessões Claude vivas (a da entrevista e `b09b59bd` em K, `75a5501a` em A)
  e 26 processos VS Code. O servidor do app (`iniciar_app_real.bat`, desde 08:41, porta 8765) roda sobre R com
  o SQLite aberto. O Foxit tem `K\saida\0210_T\ROUND_113_0210_T.pdf` aberto. Há um python órfão (PID 21168,
  criado às 21:40 da véspera, pai inexistente).
- **Datas.** O último censo foi 02/10 T, reprocessado em 03/10 às 09:21; `entrada\` ainda guarda os insumos
  dele. A pré-condição "depois do censo de 6ª" está cumprida. **Próximo uso do Ettore: 07 ou 08/10**
  (K\docs\HANDOFF_SPRINT2.md L2095 e L2400). A janela 13 do kernel (KN49, muda o contrato da Discussão que o
  app lê) é "a PRÓXIMA", sem data (L2723). A próxima do app é a FF-2b, no PC e com o kernel (HANDOFF_APP L44),
  sem data. A planilha não tem data.
- **Leitura (inferência).** O estado no instantâneo impede a mudança. Pelas datas, há espaço entre segunda
  05/10 e terça 06/10. Para isso as sessões precisam estar fechadas, o kernel commitado e enviado, o app parado
  e a janela 13 decidida antes ou depois da mudança, não no meio. (Depois deste levantamento, o Ettore decidiu
  fazer a mudança no próprio 04/10, com as mesmas condições físicas.)

## Lacunas
- Não testado o comportamento do Claude Code: herança de "trust" do pai, `/resume` por pasta, formato exato
  das chaves (inferido do padrão observado).
- Não testado mover o `.venv`; `python.exe -m` pode continuar funcionando (inferência).
- Não visto quem segura cada pasta: faltam handles e o diretório corrente dos processos.
- Não varridos xlsx/xlsm/pdf (links externos, VBA); só abertos os 3 `.docx` de guia.
- Os caminhos gravados no banco do app foram conferidos só por busca no código e nos templates.
- O horário "noite" da nota é 17:40 local. A fala do Ettore sobre a pasta-mãe só existe como resposta
  estruturada; não achado texto livre.
- O `schtasks` só mostra o que o usuário comum enxerga.
- Pastas de dado e `trabalho\` da P só foram contadas, não lidas.
