# Mapa das pastas e dos fluxos de troca com a IA — os projetos do notebook (foto de 04/10/2026)

- **Pergunta:** para cada pasta dos projetos do notebook — para que serve, quem escreve, quem lê, se está no
  git, e qual é a situação do Ettore com ela (só alimenta, só lê, não toca, os dois escrevem, fontes, correio
  entre janelas, dado real)? E o que é o `C:\DESOSP_APP_REAL`?
- **Data:** 04/10/2026
- **Projeto que pediu:** entrevista das cores de pasta (notebook).
- **Fontes:** levantamento local, sem internet — CLAUDE.md, regras, handoffs, LEIA-ME e a LEGENDA de cada
  projeto; `git log --all --since=3.weeks --name-only`; datas e prefixos dos arquivos nas pastas ignoradas pelo
  git (sem abrir conteúdo).
- **Conclusão:** as pastas se dividem em sete situações: (A) o Ettore só alimenta; (B) só lê; (C) não toca;
  (D) os dois escrevem; (E) fontes que ele traz; (F) correio entre janelas; (G) dado real ou sem backup. A
  legenda de 30/09 diverge do uso real: o laranja cita os `EVOL_` (quem os cria é o Claude) e esquece o
  `BRUTO_` e o PDF da UTI; o verde diz "não apague", mas o Ettore limpa o `arquivo`, edita a Base Censo em
  `saida` e o `historico` à mão; o `docs` está verde, mas é quase todo do Claude. O `C:\DESOSP_APP_REAL` é a
  pasta de dados do app (cópias das rodadas + o banco com o que se digita nas telas): só o app escreve nela,
  nunca vai ao GitHub, e apagá-la perde o banco e os dois backups dele, que ficam na mesma pasta.
- **Conferir de novo depois de:** a reorganização das pastas (é uma foto de 04/10/2026, manhã).
- **Como foi feita:** subagente Explore (Sonnet), 120 chamadas de ferramenta. O texto abaixo é o relatório
  dele, sem mudança de conteúdo.

---

Convenções. K=C:\DESOSP, A=C:\DESOSP_APP, R=C:\DESOSP_APP_REAL, P=C:\planilha-hc, CL=C:\CLAUDE,
CC=C:\conversation-core. "3s a/b" = a toques (arquivo×commit) / b arquivos distintos, de
`git log --all --since=3.weeks --name-only`. K: o main é órfão de 30/09; somado o ramo local historico (275
commits, 16/09–04/10, só caminhos). A: 265 commits (repo de 20/09). P: 41 (27/09). Ignoradas: arquivos de
13/09 em diante, por prefixo. Dia = 04/10. Há 25 pastas coloridas no disco (desktop.ini), iguais ao mapa de
A:scripts/icones_pastas.py:50-81. Nada foi modificado.

## O que as regras escritas dizem
- K: Ettore deposita em entrada\ SIST_ (sempre), BRUTO_, CENSO_UTIA_*.pdf, HC_, PEND_, *_ADENDO; não cria
  EVOL_ (Claude na fase E, GPT no plano B) nem censo (K:.claude/skills/rodada/SKILL.md:26-34;
  K:docs/guia/gerar_guia_rodada.py:243,265-278). Só lê saida\DDMM_P\. Edita à mão a Base Censo do
  CENSO_*.xlsx (guia:438-442) e historico\*.json (K:desosp/hc_evolucao.py:26).
- A: abre o app pelos .bat e digita nas telas (A:CLAUDE.md:93-99). P: deposita em entrada\ as 9 planilhas de
  unidade + MASTER baixadas do SharePoint (P:CLAUDE.md:68-70); lê saida\ (P:saida/LEIAME.txt); trabalho\ e
  historico\_arquivo_tecnico\ "são do Claude" (P:README.md:54).
- Entre janelas: o remetente escreve só em docs\para_o_destino\ do outro, sem commitar; o destinatário
  confirma no INDICE e commita (A:docs/PROJETO_FLUXOS_DESOSP.md:99-137; K:CLAUDE.md:356-373). Ciclo de 04/10:
  AK-012 depositada 02:44, confirmada no kernel 09:33 (3765125), AT-029 depositado 09:50 (cf9117e). Ettore só
  cola no chat o prompt da próxima janela (A:CLAUDE.md:274). Abertura: gancho em A e P, regra em K.

## 1. Mapa por projeto

**K C:\DESOSP (git main+historico)**

| pasta | serve | escreve | lê | git | sit. | evidência |
|---|---|---|---|---|---|---|
| desosp\ tests\ scripts\ | código, testes, gancho pre-push | Claude | pipeline, pytest | sim | C | ESTRUTURA.md:13-37; 3s 350/32, 159/3, 11/5 |
| .claude\ | regras por módulo, roteiro da rodada | Claude | Claude | sim | C | CLAUDE.md:7-8; 65/28 (nasceu 03/10) |
| docs\ soltos, templates, guia, scripts, regras, gemini | contrato da fonte, Knowledge, handoff, Guia .docx, formato das mensagens, cópias REF_ | Claude | Claude; Ettore só o Guia | sim | C | mensagens.py:19; 189/32 e 60/21 |
| docs\gpt\ | pacote que Ettore sobe ao GPT (plano B) | Claude (run_doc_gpt) | Ettore | sim | B | rules/docs-gpt.md:38; 22/9 |
| docs\para_o_app\ | 29 AT (kernel→app) | kernel | app | sim | F | rules/series-at-ak.md:14-22; 82/30 |
| docs\para_o_kernel\ | CAIXA: 12 AK do app | app deposita, kernel confirma | kernel | sim | F | CLAUDE.md:356-373; 24/13 |
| docs\para_a_planilha\ | 2 KP | kernel | planilha | sim | F | series-at-ak.md:46-50; 4/3 |
| entrada\ | insumos da rodada | Ettore; Claude (EVOL_, _GUIA_…docx); pipeline move para arquivo | pipeline | ignorada (.gitignore:8) | A (+D) | CLAUDE.md:37,235-251; 7 arq. de 01–04/10: SIST_ 2 (um _IHDL), EVOL_ 2, HC_ 1, PEND_ 1, guia 1; APP_ 0 |
| saida\ | rodada corrente DDMM_P\ (MSG_, RELATORIO_, ROUND_, CENSO, state.pkl) | pipeline; Ettore edita Base Censo | Ettore; pipeline (censo = prior) | ignorada (:9) | B+D, alerta G | CLAUDE.md:38; 71 de 73 arq. ≤21d; destruída pelo pytest em 09/09 (docs/regras/RECUPERAR_RODADA.md) |
| arquivo\ | 29 rodadas (12 M, 17 T) + 3 especiais | pipeline move; Ettore apaga as velhas | Claude (reprocesso) | ignorada (:10) | B+G | ESTRUTURA.md:108-114; 445 de 563 arq. ≤21d: MSG_ 130, RELATORIO_ 63, json 57, CENSO xlsx 36, LOG_ 34, state.pkl 32, EVOL_ 23, ROUND_ pdf 21, SIST_ 15, HC_ 13, BRUTO_ 9, PEND_ 2 |
| historico\ | HC_EVOLUCAO.json, HD_CARIMBO.json | pipeline e Ettore à mão | pipeline | ignorada (:12) | D+G sem backup | CLAUDE.md:41; guia:434; 2 arq. de 03/10 |
| fontes\ | 2 manuais da operadora, 5 PDFs-modelo do censo da UTI | Ettore (autoria dos PDFs não documentada) | Claude | ignorada (:43-44, *.pdf) | E+G | CLAUDE.md:202-205; 7 arq. |
| raiz | CLAUDE.md, ESTRUTURA.md | Claude | Claude | sim | C | 69/5 |

**A C:\DESOSP_APP (git main)**

| pasta | serve | escreve | lê | git | sit. | evidência |
|---|---|---|---|---|---|---|
| app\ tests\ scripts\ .claude\ | código, testes, icones_pastas.py, gancho de abertura | Claude | app em execução, Claude | sim | C | CLAUDE.md:30-39; 3s 590/99, 291/65, 13/7, 7/5 |
| workspace_dev\ | raiz de TESTE sem dado real: banco, _fotos das telas | testes, fotografar_telas | Claude | ignorada (.gitignore:11) | C | workspace_dev/LEIA-ME.md:1-8; _fotos 11 arq. de 04/10 09:00 |
| docs\ soltos | HANDOFF_APP (prompt da próxima janela), PROJETO_*, UX, LEGENDA | Claude | Claude; Ettore lê a LEGENDA | sim | C (+B) | 168/19 |
| docs\fontes\ | brainstorms, pacote GPT, sugestões de front GPT/Gemini | Ettore fornece | Claude | sim | E | docs/LEIA-ME.md; 96/40 |
| docs\para_o_app\ | CAIXA: 29 AT + PA-001 | kernel e planilha depositam; app confirma | app | ignorada (:67) | F | CLAUDE.md:139-161; 32 arq. ≤21d |
| docs\para_o_kernel\ para_a_planilha\ | originais: 12 AK, 8 AP | app | kernel; planilha | sim | F | 31/13, 20/9 |
| raiz | iniciar_app.bat, iniciar_app_real.bat, local_nomes.json (nomes, ignorado) | Claude; Ettore clica nos .bat | — | sim | H | 56/9 |

**R C:\DESOSP_APP_REAL (fora de todo git)**

| pasta | serve | escreve | lê | sit. | evidência |
|---|---|---|---|---|---|
| arquivo\ saida\ | cópia de 25 rodadas, a última 2609_T | só a puxada | app | B | puxar.py:1-30; 448 arq., todos criados 28/09 20:00 |
| historico\ | cópia dos 2 JSON + _PUXADA.json | puxada | app | B+G | puxar.py:16-17; é de 27/09, o do kernel é de 03/10 |
| entrada\ | APP_/SIST_/EVOL_ da rodada do app | o app, não o Ettore | pipeline via app | H | LEGENDA:25; 0 arq. |
| desosp_app.db, busca_fts.db | banco do app; índice de busca | app em execução | app | G (banco); índice regenerável | models.py:419,645,680,782; busca.py:13-16; banco 4,7 MB, 04/10 08:41 |
| _envios\ _backups\ | espera e cópias de leitura; cópias do banco antes de migrar | app | app | C; backups = G (mesma pasta) | envios.py:46; 26 e 2 arq. |

**P C:\planilha-hc (git main, GitHub desosp-hc)**

| pasta | serve | escreve | lê | git | sit. | evidência |
|---|---|---|---|---|---|---|
| scripts\ tests\ .githooks\ .claude\commands | código; 12 comandos /rodada etc. | Claude | Claude; Ettore digita os comandos | sim | C | CLAUDE.md:52-59; 144/64, 26/14, 4/2, 28/13 |
| trabalho\ | temporários (rec\ nunca entregar, logs, testes A/B) | scripts, Claude | Claude | ignorada (:7) | C | README.md:54; 536 arq., 535 de um A/B de 29/09 |
| entrada\ | 9 planilhas das unidades + MASTER do dia | Ettore | scripts | ignorada (:3) | A | CLAUDE.md:68-70; em 04/10 só LEIAME.txt |
| saida\ | planilhas corrigidas "para subir", boletins PDF, relatórios, placar | scripts | Ettore | ignorada (:5) | B | saida/LEIAME.txt; em 04/10 vazia |
| planilhas\v315\ | última entrega às equipes, base da próxima | fechar_rodada | Ettore, scripts | ignorada (:9) | B+G | CLAUDE.md:42; 10 xlsx + ENTREGA.json de 26–27/09 |
| historico\ | placar 5, rodadas 51, _arquivo_tecnico 146 arq. | fechar_rodada | Ettore (placar); resto Claude | ignorada (:10) | B+G | README.md:38-54; 167 de 203 ≤21d (última 29/09): HC_ xlsx 11, RELATORIO_ 18, BOLETIM_ 8 |
| privado\ | senha e hashes do detector de privacidade | autoria não documentada | scripts | ignorada (:11) | G | CLAUDE.md:51,126; 3 arq. de 27/09 |
| modelos\, docs\ soltos, mudancas, legado | molde, textos-modelo, spec 00–14 | Claude | Claude, scripts | sim | C | 27/15, 76/18 |
| docs\premiacoes\ | artes do placar geradas no ChatGPT | Ettore | grupo, Claude | sim | A | docs/13_PLACAR_MENSAL.md:98,126; 9/8 |
| docs\para_a_planilha\ | CAIXA: 8 AP + 2 KP | app e kernel depositam; planilha confirma | planilha | sim | F | CLAUDE.md:148-170; git status: 5 não rastreados + INDICE alterado = sem confirmação |
| docs\para_o_app\ para_o_kernel\ | originais PA (1), PK (0) | planilha | app; kernel | sim | F | 3/2, 1/1 |
| raiz | GUIA_DE_TRABALHO_COM_O_CLAUDE.docx | Claude | Ettore | sim | B | CLAUDE.md:33 |

**CL C:\CLAUDE (sem git)**

| pasta | serve | escreve | lê | sit. | evidência |
|---|---|---|---|---|---|
| skills\ | 4 skills (2 do Ettore, 2 de terceiros) | Claude, npx skills | Claude Code, por 4 junções | C+G | LEIA-ME.md:9,24; 10 arq. de 03–04/10 |
| scripts\ | ligar_claude.py | Claude | Ettore roda após instalar skill | C | LEIA-ME.md:18-36 |
| fontes\, skills\uso-do-claude\fontes | pesquisas que viraram skill | Ettore traz | Claude | E | LEIA-ME.md:10 |
| CLAUDE.md | regras pessoais, hardlink de ~\.claude\CLAUDE.md | Ettore dita, Claude edita | toda janela de todo projeto | D+G | LEIA-ME.md:12,25 |

**CC C:\conversation-core (1 commit de 01/09, sem remote, 0 commits em 3s, 14 alterados + 4 novos sem commit)**

| pasta | serve | escreve | lê | git | sit. | evidência |
|---|---|---|---|---|---|---|
| src\ apps\ tests\ docs\ | código Python, shell web, docs | Claude | Claude | sim | C | CLAUDE.md |
| entry\ | exports de conversa, 2 arq. (4 MB) | Ettore | CLI, web | ignorada (:4) | A+G | docs/PRIVACY.md:26 |
| data\processed\ | 79 arq. derivados (47 parquet, 26 json, 4 html), 28/08–01/09 | programa | Ettore, Claude | ignorada (:3) | B+G | idem |
| .test-tmp* (28), build\, .venv\ | lixo de teste e ambiente | programa | — | ignorada | C | .gitignore:26-35 |

(Nota de 04/10, depois do levantamento: o Ettore informou que o conversation-core é um projeto do Codex com
o GPT; ele vai para `C:\GPT` e fica fora dos processos do Claude.)

**Subpastas criadas pelo Claude, amarelas dentro de pasta colorida (rodadas excluídas)**

| mãe (cor) | subpastas | sit. |
|---|---|---|
| K docs\ (verde) | para_o_app, para_o_kernel, para_a_planilha | F |
| K docs\ | templates, guia, scripts, regras, gemini | C |
| K docs\ | gpt (tem desktop.ini velho, de 25/08, sem ícone: o script o pularia) | B |
| K saida\ (verde) | _extracao (pacote da fase E, regenerável) · _revisao_02out (44 arq. de 02–03/10: dossiês, scripts, RETOMAR.md) | C · C+G |
| K arquivo\ (verde) | _RECUPERADO_0909_T, _RECUPERADO_HC_EVOLUCAO_0110, _anterior_ao_padrao | B+G |
| K entrada\ (laranja) | _ESPERA (só durante um refazer; em 04/10 ausente) | C |
| K scripts\ (azul) | git\ | C |
| A docs\ (verde) | para_o_app (ignorada), para_o_kernel, para_a_planilha · fontes\ e 7 filhas | F · E |
| A workspace_dev\ (azul) | _fotos, _envios, _backups | C |
| P docs\ (verde) | para_* (3) F · premiacoes e 2 filhas A · mudancas, legado C | |
| P historico\ (verde) | placar B · rodadas B+G · _arquivo_tecnico e 6 filhas C+G | |
| P saida\ (verde), trabalho\ e scripts\ (azul) | boletins (+ relatorios_email, placar na rodada) B · logs, rec, testes_antes_depois, leitor_pdf, migracao C | |
| CL skills\ (azul) | 4 skills, uso-do-claude\fontes | C+G · E |

**Divergências entre a legenda de 30/09 e os fatos**
- Laranja cita "os EVOL_": Ettore não os cria; faltam BRUTO_ e o PDF da UTI (SKILL.md:27,31-32).
- Verde diz "não apaga nem renomeia": mas arquivo\ é limpo por ele (ESTRUTURA.md:113), saida\ ele edita
  (guia:438) e historico\ é editável e sem backup (CLAUDE.md:41).
- Sem cor e com papel próprio: fontes (K, CL), docs\fontes (A), modelos, planilhas, privado (P), entry (CC),
  as 9 caixas para_* (F), a raiz do A (.bat que ele clica).

## 2. C:\DESOSP_APP_REAL, em linguagem simples
1. O que é: a pasta de dados que o aplicativo abre quando se clica iniciar_app_real.bat, que define
   DESOSP_RAIZ (A:iniciar_app_real.bat:4; app/config.py:236). Tem cópias das rodadas reais do censo e o banco
   do app, onde fica o que se digita nas telas (A:docs/PROJETO_FLUXOS_DESOSP.md:353-379; _RAIZ_REAL.json).
   Estava aberta no levantamento: o app subiu às 08:41, porta 8765.
2. Por que separada: workspace_dev\ é só de teste; o app não pode escrever em C:\DESOSP, que o processamento
   do censo move e arquiva (os dois caminhos precisam ser independentes para comparar); e fica fora de todo
   repositório para não subir ao GitHub nem aparecer em busca do Claude (A:docs/HANDOFF_APP.md:1001;
   PROJETO_FLUXOS:626-640).
3. Quem escreve: a puxada, que copia de C:\DESOSP (botão "Puxar do kernel" ou comando, nunca ao abrir; feita
   uma vez, 28/09 20:00; o kernel já tem 4 rodadas mais novas: 0110_M, 0110_T, 0210_M, 0210_T) e o app em
   execução. O Ettore não escreve à mão.
4. Abrir, mexer, apagar: abrir só pelo app, que escreve ali "à vontade" (app/templates/ajuda.html:189).
   Nenhum documento manda apagar, nem descreve o que ocorre se apagar.
5. GitHub: nenhuma relação; a raiz real "nunca sobe" (PROJETO_FLUXOS §5.4). O repositório do app é
   C:\DESOSP_APP.
6. Se apagada (dedução de puxar.py e models.py): as rodadas voltam com nova puxada; perde-se o banco
   (anotações, itens escritos nos pacientes, estado das tarefas, notas da navegação) e os 2 backups dele, que
   estão na mesma pasta.
7. Pendente: renomear para dados-app\ sob uma pasta-mãe (decidido 30/09, não executado; HANDOFF_APP.md:1001).
   Busca de "_REAL": CLAUDE.md:50, HANDOFF (13), PROJETO_FLUXOS (11), scripts/icones_pastas.py:66-69;
   .claude\: 0.

## Lacunas
- Leitura pelo Ettore não deixa rastro: git e datas mostram quem escreve; "quem lê" vem das regras escritas.
- O banco não foi aberto (WAL em uso): não se sabe quantas anotações ou tarefas existem.
- Raiz do app em uso no levantamento: dedução (processo lançado por iniciar_app_real.bat às 08:41; WAL de
  09:10).
- Exportar do app para o kernel: nenhum APP_ em entrada\ ou arquivo\.
- Autoria dos PDFs de K\fontes e de P\privado não documentada; backup externo do C: desconhecido.
- ESTRUTURA.md (K) está defasado: sem fontes\, .claude\, docs\para_*, saida\DDMM_P.
- desktop.ini: P mostra 3 não rastreados no git status (AP-007 sem resposta).
- CC: sem documento de fluxo de pastas; classificado por README, PRIVACY e .gitignore.
