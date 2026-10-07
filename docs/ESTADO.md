# Estado do claude-kit — 06/10/2026, fim da R1

## Onde estamos

- **Feito:**
  - F1a (privacidade, isolamento, o kit no git);
  - R1 (o objetivo, a medição, a andrej-karpathy-skills e a última varredura).
- **As decisões da R1** estão em `decisoes\2026-10-06_R1-objetivo-medicao-recursos.md`. O objetivo passou a ser a atenção
  concentrada: perguntas de uma vez, execução longa sem o Ettore, várias janelas. O plano foi ajustado só no que ele
  aprovou.
- **Próxima:** o F1b, com o prompt do plano ("### F1b"). Ele roda como está, com as paradas (Q46).
- **Push:** feito em 06/10, no fim da R1.
- **Em paralelo:** a R0 (revisão de front) pode estar aberta no `desosp-app`; nada do kit mexe lá.

## O que existe agora

- **Repositório privado `github.com/HirugaX/claude-kit`** (ramo `main`).
  - `.githooks\pre-commit` roda `scripts\checa_kit.py --staged`.
  - `.githooks\pre-push` só aceita esse remoto.
  - `core.hooksPath` está ligado neste PC; no desktop, o NB-001 manda ligar.
  - Fora do git: `_do_desktop\`, zips, o `GUIA_DAS_SKILLS.docx` gerado, `desktop.ini`, `.vscode\` e caches.
- **ADRs:**
  - `0001-privacidade.md`, que ganhou na R1 a D8: o Remote Control liga sozinho em todo projeto, e o texto do aviso no
    celular leva só projeto, fase e contagem;
  - `0002-isolamento.md`.
- **Medição (R1):**
  - `scripts\medir_semana.py`: um protótipo que só imprime números;
  - em `metricas\`: a linha de base de 08/09 a 29/09 (`uso-semanal.csv`), o `ctx0-por-projeto.csv` e o
    `pastas-projetos.csv`;
  - o F2 completa a planilha, o gancho semanal, o balanço a cada 15 dias e o % do limite.
- **`~\.claude\settings.json` (R1):**
  - `cleanupPeriodDays: 90`, até o F9;
  - `remoteControlAtStartup: true`;
  - backup em `~\.claude\backups\settings.json.2026-10-06_antes-da-R1`.
- **`caixa\`:** séries NB e DK. A NB-001 (o desktop clona o kit) está `enviado`.
- **O documento do Ettore:** `docs\2026-10-06_o-que-mudou-e-como-operar.docx`, com a fonte `.md` ao lado. A Parte 2 (as
  metas e o "depois do F3") foi superada pela R1 e se reescreve no `COMO_OPERAR.md` do F3c.
- **CLAUDE.md pessoal:** é hardlink com o `CLAUDE.md` da raiz do kit; conferido com `fsutil` no fim da R1.

## Riscos e pendências

- **Remote Control:** liga sozinho nas sessões novas, mas ainda não foi conferido no painel do VS Code nem em `--bg`. O
  F1b confere o painel, e o F3a, a `--bg`. Para o celular: bloqueio de tela e verificação em duas etapas na conta Claude
  (D8).
- **session-report:** continua no escopo de usuário até o F1b. **Não invocar**: ele lê as transcrições de todos os
  projetos e grava texto de prompts no HTML.
- **Esforço `max`:** na semana de 29/09 houve 1.807 chamadas do Opus 5.5 e 1.197 do Sonnet 5.5 (nos subagentes) em
  `max`. O F2 confere se o subagente herda o esforço da janela.
- **`--bg` no Windows:** há bugs abertos (#77754, #87812, #97273); o F3a testa antes de o fluxo depender dela.
- **Hardlink × git:** checkout, reset, pull e stash que reescrevem o `CLAUDE.md` separam o hardlink. Conferir com
  `fsutil hardlink list C:\Users\ettor\.claude\CLAUDE.md`. A lixeira guarda um 3º link, sobra da limpeza de 06/10, que
  some quando ela for esvaziada. O F1b testa trocar o hardlink por um import (`@...`).
- **Cores:** `pastas.py conferir` saía com 0 problemas no fim do F1a.
- **O que os ADRs mandam aos projetos:** ainda não foi aplicado. Fica com o F5a, F5c, F6, F7, F3b e N2; até lá, valem
  as regras antigas de cada projeto.
- **Conector do Google Drive:** ainda não está ligado no claude.ai (ADR-0001 D4).
- **As 6 lápides do `C:`:** só depois das rodadas de 07, 08 e 09/10 (`decisoes\2026-10-05_organizar-projetos.md`).
- **O `gh`:** não está instalado.

## Como retomar

1. `git pull --ff-only` e ler este arquivo e o `caixa\INDICE.md`.
2. Abrir o F1b com o prompt do plano.
3. Antes de commit: `python scripts\checa_kit.py --tudo` (o gancho roda o `--staged`).
