# Estado do claude-kit — 09/10/2026, fim do F2b

## Objetivo

O fluxo novo do plano (`decisoes\2026-10-06_plano-fluxo.md`): atenção concentrada — o Ettore senta poucas vezes e
responde de uma vez; entre as sentadas o Claude trabalha sozinho, com a mesma qualidade e economia. O kit leva as peças
(skills, ganchos, medição) e o laço testado aos projetos.

## Onde estamos

- **Feito:** F1a; R1; F1b (marketplace); F2a (skills, 07/10); **F2b (ganchos, statusline, medição, pastas de teste), 09/10.**
- **Próximo passo:** F3a (`teste-fluxo`) ∥ F3b (`teste-ferramentas`), com os prompts do plano (conferidos em 09/10).
  Depois, F3c e F5a.
- **Critério de pronto do F3a e do F3b:** o `RESULTADO.md` de cada um, com prova por critério (F3a) e números com
  veredito por ferramenta (F3b), copiado para `pesquisas\`.
- **Em paralelo, quando o Ettore quiser:** a R0 (front do app); o desktop instala pela `caixa\NB-004` (soma-se à NB-003).

## O que o F2b deixou

- **Ganchos** em `plugins\nucleo\ganchos\` (um script por gancho, `comum.py`), pelo `hooks\hooks.json`. Todo projeto:
  abertura (modelo e esforço errados, `git pull` do kit por hora, medição semanal em segundo plano, balanço vencido),
  `PreModelSwitch` (barra o `claude-sonnet-5`), lembrete de `effort` no `Agent`. Onde há `docs\ESTADO.md`: estado
  curto, fila, caixa e git na abertura; `PROXIMO.md` no `/clear`; portão `Stop`; guarda de pasta de dado; a fila.
  `scripts\testar_ganchos.py`: 52 verdes. Estado local por PC em `~\.claude\kit-local\`.
- **Settings** (backup `~\.claude\backups\settings.json.2026-10-09_antes-do-F2b`): statusline, `showClearContextOnPlanAccept`,
  3 permissões mortas fora; o `instalar_kit.py` instala e confere os dois primeiros.
- **Medição:** `medir_semana.py --planilha` (`metricas\uso.xlsx`, fora do git) e o % semanal da statusline;
  `metricas\metas.json` (fonte única das metas); `metricas\BALANCO.md` (roda na janela da raiz; 1º vence em 24/10).
- `teste-fluxo` e `teste-ferramentas` com `git init`, settings do tipo `teste`, sem cor.

## Surpresas

- **`/model sonnet` e `--model sonnet` já abrem o Sonnet 5.5** (2.1.291, provado por `claude -p`). A regra do CLAUDE.md,
  da `uso-do-claude` e do COMO_OPERAR ainda diz que abrem o 5; mudar é decisão do Ettore (no resumo do F2b).
- **O SessionStart em `-p` não traz o `model`**: a abertura lê o `--model` da linha de comando do processo (~1,5 s).
- **`CLAUDE_CODE_SESSION_ATTENDED`** vale 1 na sessão com gente e 0 em `-p` (não documentado): é o sinal da execução
  largada. O `PermissionRequest` não dispara em `-p` nem em `--bg` (documentação).
- **O painel do VS Code não roda a statusline**: o % só chega ao arquivo pelo terminal.
- O `pastas.py marcar` resolve o caminho a partir do diretório atual: rode-o da pasta-mãe.
- Heredoc do Git Bash comeu barras de novo (consertado pelo Edit); o safety-net barra `git checkout --`.

## Decisões

- Execução largada = `ATTENDED=0`, `KIT_LARGADA=1` ou `.claude\largada` (texto na `orquestrar` §4).
- O `AskUserQuestion` largado é **negado** com "Adiada" (nunca `answers`): o gancho não escolhe.
- "Fase dada como pronta" = a última mensagem traz "Sinais de insuficiência do modelo"; "reescrito" = o hash do
  `ESTADO.md` mudou desde a abertura.
- A regra de leitura da memória `c--DESOSP` ficou no allow (a pasta existe; a limpeza é do F9).

## Riscos

- A 2ª camada age no próprio kit (tem `ESTADO.md`): fechar uma fase do kit sem reescrevê-lo é bloqueado.
- Herdados: os bugs da `--bg` no Windows (F3a); o conector do Drive desligado; as 6 lápides do `C:`; o `gh` ausente;
  `deep-research` com nome repetido; `pastas.py conferir` acusa 2 pastas de outra janela no `desosp-censo`.

## Como retomar

1. `git pull --ff-only`; `python scripts\instalar_kit.py --verificar` (0 achados); `python scripts\testar_ganchos.py`.
2. Abrir o F3a e o F3b com os prompts do plano, cada um na sua pasta. Antes de commit: `python scripts\checa_kit.py --tudo`.
