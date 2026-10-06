# O fluxo de trabalho atual e o inventário dos projetos do notebook (foto de 05/10/2026)

- **A pergunta:** como o Ettore trabalha hoje com o Claude Code (o ciclo de uma janela, os passos manuais, onde mora
  o estado) e o que cada projeto tem (CLAUDE.md, `.claude/`, handoff, caixa, testes, custo de abrir)?
- **A data:** 05/10/2026, à noite (depois da mudança para `C:\CLAUDE-PROJETOS`).
- **O projeto que pediu:** claude-kit (refinar o fluxo; base da entrevista de 05/10).
- **Conferir de novo depois de:** qualquer mudança no fluxo de janelas ou nos CLAUDE.md (é foto de 05/10).
- **Fontes:** os próprios arquivos (caminho:linha abaixo), `git`, e `medir_uso.py --sessoes --desde 2026-10-01`
  (só números). Nenhuma pasta de dado foi aberta. Siglas: APP/CEN/HC = `desosp-app`, `desosp-censo`, `desosp-hc`;
  HA = `APP\docs\HANDOFF_APP.md`; HS = `CEN\docs\HANDOFF_SPRINT2.md`; PJ = `decisoes\2026-10-04_prompts-das-janelas.md`.

## Conclusão em poucas linhas

1. **O método-base é um só, em três implementações.** Uma fase por janela, handoff, prompt da próxima no chat,
   caixas `docs\para_*\` entre projetos, pergunta no chat. Cada projeto inventou o gancho de abertura (APP completo,
   HC só a caixa, CEN nenhum), o lugar do estado e o formato do prompt; a regra comum foi copiada em cada CLAUDE.md.
2. **Cada janela tem ~7 passos manuais fixos; 4 são transporte puro** (abrir, copiar, colar, `/effort`). A rodada
   diária do kernel soma 6 a 8 transportes. Em 29/09-05/10 o app teve ~18 janelas, ~7 delas de implementação.
3. **O contexto é grande mesmo com janelas curtas:** mediana de `ctx_med` 218 mil (app), 143 mil (hc), 95 mil
   (censo, todas as sessões) a 317 mil (censo, sessões com 20+ chamadas); picos de 673 a 865 mil; só 4 compactações,
   todas no hc. 85 sessões desde 01/10; quase tudo no Opus 5.5; as 15 sessões mais caras são 80% do custo.
4. **O estado se acumula e envelhece.** HA 6.708 linhas/575 KB e HS 4.147 linhas/376 KB, crescendo (+357 e +497
   linhas desde 04/10); estado velho no `APP\CLAUDE.md:53` e no `HA:11`; o `MEMORY.md` do censo tem 12 KB (uma linha
   de 7,4 mil caracteres) repetindo o status do handoff e entra em toda sessão; não há `docs\adr` em nenhum projeto.
5. **A mesma regra mora em 4 a 9 lugares** ("pergunta no chat", modelo e esforço, caixa, sinais de insuficiência).

## O ciclo de hoje

1. Abrir janela na pasta do projeto; colar o prompt; digitar `/effort <nível>` (1ª linha do prompt).
2. Ao abrir: APP roda `abertura.py` (`APP\.claude\settings.json:3-13`): git, arquivo sem commit de outra janela,
   caixa pendente, topo do handoff, esforço gravado, aviso de modelo. HC injeta só a caixa
   (`HC\.claude\settings.json:7-19`, `scripts\caixa_pendente.py`). CEN não tem gancho: o ritual é texto no prompt.
3. Trabalhar: uma fase, um commit por assunto, decisão perguntada no chat, nada muda sem "sim".
4. Fechar: seção nova no alto do handoff; mensagem AT/AK/AP/KP na caixa do vizinho + linha no índice; push;
   resumo com "Sinais de insuficiência do modelo"; prompt da próxima no chat e gravado (HS "### Prompt N"; HA; PJ).
5. Quem leva o prompt é o Ettore, colando. Modelo e esforço: tabela por projeto, critério "custo de descobrir tarde".

Esqueleto do prompt (`skills\uso-do-claude\organizar-projetos\prompts.md:3-47`): `<Modelo> · /effort <nível> — porquê`
/ pasta e pré-condição / `## Contexto` / `## O que fazer` / `## Limites` / `## Ao fechar`. Variantes por projeto.

## Inventário

| | app | censo (kernel) | hc (planilha) |
|---|---|---|---|
| stack | FastAPI + Jinja2, SQLAlchemy + Alembic, SQLite, pytest, Playwright/Edge | Python 3.12 global, openpyxl, xlrd, pypdf, pytest; sem banco | Python, openpyxl, reportlab, python-docx, pytest; Node exceljs; LibreOffice |
| CLAUDE.md | 354 linhas / 24,5 KB | 430 / 33,9 KB | 226 / 20,3 KB (com seção "Estado atual") |
| `.claude/` | gancho SessionStart; 1 regra (`front.md`); skill `revisar-tela` | 27 regras com `paths:` (3.000 linhas / 203 KB, globs sobrepostos em `data_merge`, `loaders`, `mensagens`); skill `rodada` | gancho da caixa; `autoCompactWindow: 400000`; 12 comandos |
| estado | HA | HS + regras + skill `rodada` | `docs\12_PROXIMA_RODADA.md` + `RODADA.json` + checklist |
| caixa | `docs\para_o_app\` (AT, PA) | `docs\para_o_kernel\` (AK, PK) | `docs\para_a_planilha\` (AP, KP) |
| testes | 55 arquivos, 665 funções (736 passam, 387 s) | 1 arquivo de 12 mil linhas, 612 funções | 13 arquivos, 82 funções |
| custo de abrir (`ctx0`) | ~58 mil tokens | ~66 mil (caiu de 128-140 mil após o KN42, 03/10) | ~55 mil |
| git | HirugaX/desosp-app, 130 commits, pre-push | HirugaX/desosp-censo, 98 commits, pre-push | HirugaX/desosp-hc, 59 commits, pre-commit de privacidade |

`prototipos-icones`: sem git, CLAUDE.md, testes ou memória (gerador Pillow + prévias HTML).

Memória automática: app 6 arquivos, censo 20 (MEMORY.md 12 KB), hc 7, mãe 4; chaves velhas (`C--DESOSP` etc.) ainda
existem, com cópias divergentes em 10 arquivos.

## Lições registradas que o fluxo novo precisa respeitar

1. O atalho `sonnet` abriu o Sonnet 5 (188 chamadas da FF-P3c); regra em texto não chega lá, gancho sim.
2. `/effort` confirmado grava para todos os projetos; `xhigh` reapareceu gravado em 04 e 05/10.
3. Correção que fica só no chat não existe na janela seguinte.
4. Duas janelas na mesma pasta se atropelam; o push leva commit alheio.
5. Cópia de índice apagou a coluna de status do destinatário, duas vezes.
6. O modo automático bloqueia mover pasta, apagar na raiz do `C:`, push em massa: o comando passa a ser do Ettore.
7. O prompt seguinte tem de ser conferido pela janela que fecha.
8. A nuvem pediu conferência no PC, merge e prompt de volta; pausada desde 03/10.

## Observado durante a foto

O `~\.claude\settings.json` foi regravado por outra janela enquanto era lido (gancho do organizar-projetos; `model`
passou a `opus[1m]`; o esforço do Opus 5.5 voltou a `medium`). Permissões avulsas: 12, quatro com caminhos que não
existem mais.
