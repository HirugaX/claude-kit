# Estado do claude-kit — 07/10/2026, fim do F2a

## Objetivo

O fluxo novo do plano (`decisoes\2026-10-06_plano-fluxo.md`): atenção concentrada — o Ettore senta poucas vezes e
responde de uma vez; entre as sentadas o Claude trabalha sozinho, com a mesma qualidade e economia. O kit leva as peças
(skills, ganchos, medição) e o laço testado aos projetos.

## Onde estamos

- **Feito:** F1a (privacidade, isolamento, git); R1 (objetivo, medição); F1b (marketplace); **F2a (as skills), 07/10.**
- **Próximo passo:** o F2b (ganchos, settings, statusline, medição, pastas de teste), com o prompt do plano ("### F2b",
  conferido em 07/10). Depois, F3a ∥ F3b, F3c, F5a.
- **Critério de pronto do F2b:** o portão do prompt (`testar_ganchos.py` verde com os da fila; numa sessão nova o
  `SessionStart` avisa modelo errado e o `PreModelSwitch` barra o `/model sonnet`; `medir_semana.py` reproduz 29/09).
- **Em paralelo, quando o Ettore quiser:** a R0 (front do app); o desktop instala pela `caixa\NB-003` (substitui a NB-002).
- **Push:** feito em 07/10, no fim do F2a.

## O que o F2a deixou

- **Grupos:** `nucleo` 6 (usuário) · `planejamento` 12 (usuário) · `kit` 3, só `/` (no kit e na raiz) · `engenharia` 14
  e `sdd` 4 (por projeto de código; teste). O kit e a janela da raiz ligam o `kit`; o `instalar_kit.py` grava a raiz.
- **`uso-do-claude`** virou núcleo (123 linhas, 9,7 KB por disparo; eram 298 e 22,3 KB) + `modelo-e-esforco`,
  `fechar-janela` (com `modelos\`: ESTADO, PROXIMO, PERGUNTAS, ADR, GLOSSARY), `pesquisa`, `orquestrar`. Consulta:
  `reference.md` e `testar-instrucao.md`. **Custo fixo** (`claude -p "/context"`, pasta de rascunho): descrições do
  `nucleo` ~470 → ~290 tokens; skills 6,4 mil → 6,2 mil (total 31,4 mil, arredondado igual).
- **Módulo das pastas** em `plugins\nucleo\pastas\` (scripts, testes, mapa, quadros dos ícones, planos); o gancho do
  `nucleo` o chama por `${CLAUDE_PLUGIN_ROOT}/pastas/...`; o `ligar-gancho` não grava mais em settings. Suíte: 150
  verdes; `pastas.py conferir` = 0; o gancho disparou numa sessão nova.
- **`config\fluxo.json`** com `lancar_bg: false` (o F3c liga). `scripts\medir_uso.py` (movido).
  `scripts\perguntas_nucleo.txt`: 11 de 11 batem (Sonnet 5.5, US$ 1,16 as 12 sessões).
- **`.gitattributes`:** scripts bash dos plugins sempre em LF (o `task-brief` do SDD quebra com CRLF).

## Surpresas

- **Descrição de skill com `: ` sem aspas some** (o YAML quebra e a skill não carrega, sem aviso). As do `nucleo` estão
  entre aspas; confira com `claude -p "/context"` ou a 1ª linha do `stream-json`.
- **Quebrar uma skill em cinco aumenta as descrições fixas**, se não forem enxutas: a 1ª versão foi para ~590 tokens.
- **A pergunta 9 falhou** até o CLAUDE.md pessoal apontar a rodada de contingências: regra só dentro da skill não chega
  à sessão que responde pelo CLAUDE.md.
- **Heredoc do Git Bash come barras invertidas**: `\n` de `plugins\nucleo` virou quebra de linha no plano (consertado e
  conferido). Editar por arquivo `.py` ou pela ferramenta Edit.
- **Pasta com o diretório do shell dentro não se move** no Windows (`Permission denied`).
- **Esforço do subagente:** a documentação não diz se herda; a ferramenta Agent (desta versão) e o `agent()` do
  Workflow aceitam `effort`. A `orquestrar` manda fixá-lo em todo despacho.

## Decisões

- O módulo das pastas inteiro no `nucleo` (todos os scripts importam o `regras.py`); as skills do `kit` só com texto.
- `sdd` de escopo de projeto (tipos `codigo` e `teste`), nunca no usuário.
- O CLAUDE.md pessoal aponta as peças do núcleo e a rodada de contingências (§3 e §7 da `uso-do-claude`).
- No prompt do F2b entrou um gancho a mais: `PreToolUse` em `Agent` lembra o `effort` quando falta (não bloqueia).

## Riscos

- **Engenharia e sdd fora dos projetos** até as fases deles (decisão do Ettore). A R0 liga só no app, `--scope local`.
- **`cc-plugin-telemetry`:** decisão do Ettore, para depois (desligar tira o `Monitor` e o Remote Control).
- Herdados: os bugs da `--bg` no Windows (F3a); o conector do Drive desligado; as 6 lápides do `C:`; o `gh` ausente;
  `deep-research` com nome repetido (embutida e do claude.ai).

## Como retomar

1. `git pull --ff-only`; `python scripts\instalar_kit.py --verificar` (0 achados); ler este arquivo e o `caixa\INDICE.md`.
2. Abrir o F2b com o prompt do plano. Antes de commit: `python scripts\checa_kit.py --tudo`.
