# Varredura dos caminhos velhos — por projeto (05/10/2026)

- **O que é:** onde cada projeto ainda cita um caminho velho (`C:\DESOSP`, `C:\DESOSP_APP`, `C:\DESOSP_APP_REAL`,
  `C:\planilha-hc`, `C:\CLAUDE`, `C:\conversation-core`, também na forma `/c/...` e `C:\...`) ou o nome de uma
  chave de memória velha (`C--DESOSP`, `c--DESOSP-APP`, `c--planilha-hc`, `c--CLAUDE`). Feita antes da mudança, nos
  caminhos velhos; os números de linha valem para os arquivos como estavam em 05/10, de manhã.
- **Para quem:** a janela de cada projeto (prompt em `2026-10-04_prompts-das-janelas.md`). Corrija o **código, os
  testes, a configuração e os documentos vivos**; os **históricos** (HANDOFF, AT/AK/AP/PA/KP, INDICE, caixas) não se
  reescrevem — eles contam o que aconteceu.
- **Como:** `varredura.py` (regex por linha; fora `.git` — menos o `.git\config` —, `.venv`, `node_modules` e as pastas
  de dado). Mostra só arquivo, linha e o caminho achado; nenhum conteúdo.
- **Prefira caminho derivado da posição do código** (a pasta do projeto vem de `__file__`; o vizinho, do pai dela), para
  a próxima mudança não quebrar nada.

## desosp-censo (era `C:\DESOSP`)

Totais: config 1 arquivo(s), 1 ocorrência(s) · código 4 arquivo(s), 14 ocorrência(s) · doc vivo 5 arquivo(s), 12 ocorrência(s) · histórico 47 arquivo(s), 190 ocorrência(s) · teste 1 arquivo(s), 12 ocorrência(s).

**código**

- `desosp/CONFIG_DESOSP.py`: linhas 9, 14, 44, 45, 54, 55, 57, 395, 396 — `C:\DESOSP`, `C:\DESOSP_APP`
- `docs/guia/gerar_guia_rodada.py`: linhas 495, 515, 520 — `C:\\DESOSP`, `C:\\DESOSP_APP`
- `docs/scripts/REF_medir_relevancia_hd.py`: linhas 14 — `C:\DESOSP`
- `scripts/prova_multicenso.py`: linhas 9 — `C:\DESOSP`

**teste**

- `tests/test_regressoes.py`: linhas 5, 3477, 3478, 3498, 5163, 5205, 5265, 5266, 5276, 5276, 5277, 9802 — `C:\DESOSP`, `C:\\DESOSP`

**config**

- `.gitignore`: linhas 14 — `C:\DESOSP`

**doc vivo**

- `.claude/rules/series-at-ak.md`: linhas 35, 47 — `C:\DESOSP_APP`, `C:\planilha-hc`
- `.claude/skills/rodada/SKILL.md`: linhas 137 — `C:\CLAUDE`
- `CLAUDE.md`: linhas 49, 51, 334, 359, 362, 370, 373 — `C:\DESOSP`, `C:\DESOSP_APP`, `C:\planilha-hc`
- `ESTRUTURA.md`: linhas 6 — `C:\DESOSP`
- `docs/MEDICAO_RELEVANCIA_HD.md`: linhas 475 — `C:\DESOSP`

**histórico** (47 arquivos, não reescrever): `.claude/rules/pastas-e-arquivo.md`, `desosp/arquivo_rodada.py`, `docs/HANDOFF_SPRINT2.md`, `docs/para_a_planilha/INDICE_KP.md`, `docs/para_a_planilha/KP-001_2026-10-04_fungos_em_dias_corridos_no_kernel.md`, `docs/para_a_planilha/KP-002_2026-10-04_pesquisa_de_bk_2_dias_uteis.md`, `docs/para_o_app/AT-001_2026-09-25_LP-mais_e_pares_23-25-09.md`, `docs/para_o_app/AT-002_2026-09-25_matricula_especialidade_altas.md`, `docs/para_o_app/AT-003_2026-09-25_fechamento_uti_enfermaria.md`, `docs/para_o_app/AT-004_2026-09-25_identidade_tres_niveis_matricula.md`, `docs/para_o_app/AT-005_2026-09-25_aba_LP-mais.md`, `docs/para_o_app/AT-006_2026-09-26_especialidade_manual_hc_protocolo.md` …

## desosp-app (era `C:\DESOSP_APP`)

Totais: config 1 arquivo(s), 2 ocorrência(s) · código 13 arquivo(s), 60 ocorrência(s) · doc vivo 21 arquivo(s), 267 ocorrência(s) · histórico 53 arquivo(s), 440 ocorrência(s) · teste 8 arquivo(s), 13 ocorrência(s).

**código**

- `app/config.py`: linhas 7, 12, 18, 33, 67, 114, 125, 133, 225, 236, 258 — `C:\DESOSP`, `C:\DESOSP_APP_REAL`, `C:\\DESOSP`
- `app/db/models.py`: linhas 766 — `C:\DESOSP`
- `app/dominio/anotacoes.py`: linhas 39 — `C:\\DESOSP_APP_REAL`
- `app/dominio/comparador.py`: linhas 9 — `C:\\DESOSP`
- `app/dominio/exportar.py`: linhas 7, 15 — `C:\\DESOSP`
- `app/dominio/puxar.py`: linhas 8, 8, 29, 30, 33, 248, 253, 672, 673 — `C:\DESOSP`, `C:\\DESOSP`, `C:\\DESOSP_APP_REAL`
- `app/iniciar.py`: linhas 14, 201 — `C:\\DESOSP_APP_REAL`
- `app/templates/ajuda.html`: linhas 189, 190 — `C:\DESOSP`, `C:\DESOSP_APP_REAL`
- `app/web/rotas.py`: linhas 333 — `C:\\DESOSP`
- `docs/PALETAS_DESOSP.html`: linhas 576 — `C:\DESOSP_APP_REAL`
- `iniciar_app_real.bat`: linhas 2, 4 — `C:\DESOSP_APP_REAL`
- `scripts/icones_pastas.py`: linhas 52, 53, 54, 55, 56, 57, 58, 59, 61, 62, 63, 64, 65, 67, 68, 69, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80 — `C:\CLAUDE`, `C:\DESOSP`, `C:\DESOSP_APP`, `C:\DESOSP_APP_REAL`, `C:\planilha-hc`
- `scripts/paletas_escolhas.py`: linhas 29 — `C:\DESOSP_APP_REAL`

**teste**

- `tests/_fabrica.py`: linhas 262 — `C:\DESOSP`
- `tests/test_config.py`: linhas 14, 62 — `C:\\DESOSP`
- `tests/test_exportar.py`: linhas 4, 109, 113 — `C:\DESOSP`, `C:\\DESOSP`, `C:\\\\DESOSP`
- `tests/test_puxar.py`: linhas 4 — `C:\\DESOSP`
- `tests/test_raiz_real.py`: linhas 4 — `C:\\DESOSP_APP_REAL`
- `tests/test_revisao_f2.py`: linhas 306 — `C:\\DESOSP`
- `tests/test_rodada_ponta_a_ponta.py`: linhas 6, 12, 330 — `C:\\DESOSP`
- `tests/varredura_nomes.py`: linhas 4 — `C:\DESOSP`

**config**

- `.gitignore`: linhas 62, 80 — `C:\DESOSP`, `C:\planilha-hc`

**doc vivo**

- `CLAUDE.md`: linhas 4, 17, 21, 50, 62, 151, 152, 168, 169, 170, 171, 172, 190, 228, 267, 338, 345 — `C:\CLAUDE`, `C:\DESOSP`, `C:\DESOSP_APP`, `C:\DESOSP_APP_REAL`, `C:\planilha-hc`
- `README.md`: linhas 4, 7, 8, 14, 24, 68 — `C:\DESOSP`, `C:\DESOSP_APP`
- `docs/APRESENTACAO_DESOSP.md`: linhas 21, 24, 72, 74, 88, 89, 93, 94, 194, 277, 397, 397, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 465, 466 — `C:\DESOSP`, `C:\DESOSP_APP`
- `docs/AVALIACAO_NOVA_ANALISE_GPT.md`: linhas 130 — `C:\DESOSP_APP`
- `docs/ENTRADA_FF-P2_AJUSTES.md`: linhas 24, 25, 29, 116, 134 — `C:\DESOSP`, `C:\DESOSP_APP`, `C:\DESOSP_APP_REAL`
- `docs/GUIA_NUVEM_DESOSP.md`: linhas 79, 99, 150, 150, 150, 154, 154, 154 — `C:\DESOSP`, `C:\DESOSP_APP`, `C:\planilha-hc`
- `docs/LEGENDA_CORES_PASTAS.md`: linhas 23, 24, 25, 26, 27, 31 — `C:\CLAUDE`, `C:\DESOSP`, `C:\DESOSP_APP`, `C:\DESOSP_APP_REAL`, `C:\planilha-hc`
- `docs/LEIA-ME.md`: linhas 1, 7, 10, 45, 46, 48, 54 — `C:\DESOSP`, `C:\DESOSP_APP`, `C:\planilha-hc`
- `docs/PLANO_REVISTO_DESOSP.md`: linhas 89, 93, 97, 138, 246, 388, 397, 703, 747, 895, 909, 912 — `C:\DESOSP`, `C:\DESOSP_APP`, `C:\planilha-hc`
- `docs/PLATAFORMA_DESOSP.md`: linhas 17, 20, 321 — `C:\DESOSP`, `C:\DESOSP_APP`
- `docs/PROJETO_FLUXOS_DESOSP.md`: linhas 4, 4, 4, 15, 15, 31, 31, 31, 45, 46, 47, 53, 54, 73, 75, 107, 107, 107, 115, 115, 116, 116, 117, 117, 118, 118, 119, 119, 120, 120, 233, 252, 253, 262, 267, 270, 278, 281, 289, 294, 295, 298, 310, 311, 320, 320, 321, 322, 349, 356, 357, 362, 370, 371, 371, 372, 372, 375, 376, 377, 389, 389, 389, 406, 406, 415, 444, 477, 528, 613, 626, 665, 695, 695, 695, 764, 768, 834, 834 — `C:\DESOSP`, `C:\DESOSP_APP`, `C:\DESOSP_APP_REAL`, `C:\planilha-hc`
- `docs/PROJETO_FRONT_DESOSP.md`: linhas 856, 940, 1035, 1110, 1184, 1238, 1323, 1324, 1344, 1382, 1384, 1770, 1828, 2048, 2049 — `C:\CLAUDE`, `C:\DESOSP`, `C:\DESOSP_APP`, `C:\planilha-hc`
- `docs/PROPOSTA_APP_DESOSP.md`: linhas 5, 6, 13, 14, 16, 18, 21, 439, 455, 581, 581, 582, 616, 616, 619, 658, 711, 712, 714, 715, 729, 1068, 1079, 1092, 1139, 1145, 1150, 1166, 1175, 1333, 1334, 1338, 1343, 1394, 1395, 1396, 1402, 1411, 1412, 1417 — `C:\CLAUDE`, `C:\DESOSP`, `C:\DESOSP_APP`, `C:\planilha-hc`
- `docs/RECURSOS_CLAUDE_DESOSP.md`: linhas 4, 5, 94, 190, 192 — `C:\CLAUDE`, `C:\DESOSP_APP`
- `docs/REFERENCIA_TECNICA.md`: linhas 3, 4, 24, 27, 48, 103, 675, 700, 700, 715, 716, 725 — `C:\DESOSP`, `C:\DESOSP_APP`
- `docs/UX_DESOSP.md`: linhas 15, 29, 32, 170, 1147 — `C:\DESOSP`, `C:\DESOSP_APP`, `C:\planilha-hc`
- `docs/VARREDURA_AT_PLANILHA.md`: linhas 17, 337, 341 — `C:\planilha-hc`
- `docs/VARREDURA_BRAINSTORM.md`: linhas 187, 383 — `C:\DESOSP`, `C:\DESOSP_APP`
- `docs/fontes/BRAINSTORM_APP.md`: linhas 42, 46, 50, 63, 1213 — `C:\DESOSP`, `C:\DESOSP_APP`
- `docs/fontes/DESOSP_PACOTE_COMPLETO_DOCUMENTOS/00_DESOSP_PACOTE_COMPLETO.md`: linhas 1569 — `C:\DESOSP`
- `docs/fontes/LEIA-ME.md`: linhas 7, 10, 12, 20, 21, 27, 40, 82, 113, 136 — `C:\DESOSP`, `C:\DESOSP_APP`, `C:\planilha-hc`

**histórico** (53 arquivos, não reescrever): `docs/HANDOFF_APP.md`, `docs/para_a_planilha/AP-001_2026-09-28_caixa_e_corrido_util.md`, `docs/para_a_planilha/AP-002_2026-09-28_github_privado.md`, `docs/para_a_planilha/AP-003_2026-09-28_caixa_na_leitura_habitual.md`, `docs/para_a_planilha/AP-004_2026-09-29_mecanismo_neutro_fungos_indicadores.md`, `docs/para_a_planilha/AP-005_2026-09-30_serie_PA_indice_proprio_e_a_nuvem.md`, `docs/para_a_planilha/AP-006_2026-09-30_nome_desosp-hc_e_o_gancho.md`, `docs/para_a_planilha/AP-007_2026-09-30_icones_das_pastas_desktop_ini.md`, `docs/para_a_planilha/AP-008_2026-09-30_home_care_e_laboratorio_na_rodada_R30.md`, `docs/para_a_planilha/INDICE.md`, `docs/para_o_app/AT-001_2026-09-25_LP-mais_e_pares_23-25-09.md`, `docs/para_o_app/AT-002_2026-09-25_matricula_especialidade_altas.md` …

## desosp-hc (era `C:\planilha-hc`)

Totais: doc vivo 4 arquivo(s), 9 ocorrência(s) · histórico 16 arquivo(s), 56 ocorrência(s).

**doc vivo**

- `CLAUDE.md`: linhas 5, 150, 151, 154, 166, 167 — `C:\CLAUDE`, `C:\DESOSP`, `C:\DESOSP_APP`
- `docs/09_AMBIENTE.md`: linhas 64 — `C:\planilha-hc`
- `docs/14_MODELO_E_ESFORCO.md`: linhas 3 — `C:\CLAUDE`
- `modelos/checklists/CHECKLIST_NOVA_VERSAO.md`: linhas 33 — `C:\DESOSP_APP`

**histórico** (16 arquivos, não reescrever): `docs/00_INDICE.md`, `docs/para_a_planilha/AP-001_2026-09-28_caixa_e_corrido_util.md`, `docs/para_a_planilha/AP-002_2026-09-28_github_privado.md`, `docs/para_a_planilha/AP-003_2026-09-28_caixa_na_leitura_habitual.md`, `docs/para_a_planilha/AP-004_2026-09-29_mecanismo_neutro_fungos_indicadores.md`, `docs/para_a_planilha/AP-005_2026-09-30_serie_PA_indice_proprio_e_a_nuvem.md`, `docs/para_a_planilha/AP-006_2026-09-30_nome_desosp-hc_e_o_gancho.md`, `docs/para_a_planilha/AP-007_2026-09-30_icones_das_pastas_desktop_ini.md`, `docs/para_a_planilha/AP-008_2026-09-30_home_care_e_laboratorio_na_rodada_R30.md`, `docs/para_a_planilha/INDICE.md`, `docs/para_a_planilha/INDICE_KP.md`, `docs/para_a_planilha/KP-001_2026-10-04_fungos_em_dias_corridos_no_kernel.md` …

## Fora dos repositórios

- **A memória do kernel** (copiada para a chave nova `C--CLAUDE-PROJETOS-desosp-censo`; a janela do kernel corrige):
  - `app-desosp-plano.md`: linhas 3, 3, 11, 12, 13, 66, 87, 88, 106, 109, 129, 132, 143, 146, 233
  - `expor-pesquisa-antes-de-alterar.md`: linhas 13, 13
  - `falha-se-corrige-nos-dois-processos.md`: linhas 47
  - `manual-desosp-fontes.md`: linhas 25
  - `MEMORY.md`: linhas 2, 3, 13, 18, 18
  - `plano-correcoes-janela-1609-1809.md`: linhas 3, 21, 22, 31, 45, 72
  - `protocolo-de-janelas-e-dois-projetos.md`: linhas 25, 25, 26, 26, 28, 28, 67, 96, 96, 98
  - `reorganizacao-claude-projetos.md`: linhas 3, 11, 11, 11, 13, 13, 13, 13, 13, 13, 16, 18, 18
  - `uso-do-claude-skill.md`: linhas 3, 11, 12, 13, 16, 17, 18, 19, 20, 21, 22, 23, 24, 40
- A memória do app e a da planilha: nenhuma ocorrência.
- `~\.claude\settings.json`: 4 regras `allow` antigas e pontuais (scratchpads de setembro, um `Read` da memória velha do
  kernel, um `Copy-Item`); não fazem mal — deixam de casar sozinhas. Limpeza opcional.
- **O kit** (`C:\CLAUDE-PROJETOS\claude-kit`): corrigido por esta janela; sobram só as citações de propósito (a base
  em `_do_desktop`, a lista das lápides no `LEIA-ME.md`, a especificação de 04/10 e `reference.md:91`, que contam
  história).

