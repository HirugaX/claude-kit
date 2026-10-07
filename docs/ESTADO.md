# Estado do claude-kit — 07/10/2026, fim do F1b

## Onde estamos

- **Feito:**
  - F1a: privacidade, isolamento, o kit no git;
  - R1: o objetivo, a medição e a última varredura;
  - F1b: o kit como marketplace.
- **Próxima:** o F2a (as skills), com o prompt do plano (`decisoes\2026-10-06_plano-fluxo.md`, "### F2a"). Depois vêm
  o F2b (ganchos, statusline, medição, pastas de teste), o F3a ∥ F3b, o F3c e, por fim, o F5a, quando o app volta.
- **Em paralelo, quando o Ettore quiser:**
  - a R0 (revisão do front do app), com o prompt do plano, que ganhou a linha da engenharia;
  - o desktop instala o kit pela `caixa\NB-002`.
- **Push:** feito em 07/10, no fim do F1b.

## Decisões do F1b (grill de 07/10)

| tema | decisão |
|---|---|
| grupos | `nucleo` e `kit` (nossos); `planejamento` e `engenharia` (terceiros). A tabela skill → grupo está no `LEIA-ME.md` e no guia |
| escopo | `nucleo` e `planejamento` no escopo de usuário. A `engenharia` **nunca** fica no escopo de usuário: cada projeto de código a liga na sua fase (R0 por `--scope local`; F5a, F6, F7, F8 e N pelo `instalar_kit.py --trecho codigo`). Até lá, o projeto fica sem ela |
| `organizar-projetos` | entrou no `nucleo` dentro da `uso-do-claude`, como estava. O F2a o quebra em 3 skills só `/` (`organizar-projetos`, `cores-das-pastas`, `icones`) no plugin `kit`, ligado só no kit e na janela da raiz |
| F2 | dividido em F2a (skills, Opus high) e F2b (ganchos etc., Opus medium) |
| desktop | instala já (NB-002); o F2a em diante chega por `git pull`; os projetos de lá esperam o F8 |
| janela da raiz `C:\CLAUDE-PROJETOS` | posto de manutenção: cores e ícones das pastas (os ícones novos se juntam e se desenham em lote, depois) e a sessão do balanço da medição (F2b) |
| cores | `metricas\` = eu-leio; `plugins\`, `.claude-plugin\`, `.claude\` e `config\` = nao-toco |

## O que existe agora

- **Marketplace local:**
  - `.claude-plugin\marketplace.json` lista `nucleo` (2 skills), `planejamento` (12) e `engenharia` (14);
  - as skills moram em `plugins\<grupo>\skills\` (a pasta `skills\` saiu);
  - cada plugin de terceiros tem o seu `origem.json`.
- **Nada carrega de cópia:** em `~\.claude\skills` não sobrou junção do kit, e `plugins\cache` não tem cópia do kit; o
  Claude Code lê os plugins direto da pasta.
- **O gancho das cores** é do plugin `nucleo` (`plugins\nucleo\hooks\hooks.json`, `${CLAUDE_PLUGIN_ROOT}`). Saiu do
  `~\.claude\settings.json`. O `local.json` das cores aponta para o módulo novo.
- **CLAUDE.md pessoal:** o `~\.claude\CLAUDE.md` é só a linha `@C:/CLAUDE-PROJETOS/claude-kit/CLAUDE.md`, um import.
  Testado numa sessão nova: as regras carregaram. Acabaram o hardlink e o `fsutil`, e a memória sobre o hardlink saiu.
- **`config\plugins.json`:** os marketplaces, os grupos, os plugins de fora e o escopo de cada um. O session-report saiu
  do escopo de usuário (Q40).
- **`scripts\instalar_kit.py`** (substitui o `ligar_claude.py`):
  - instala e confere;
  - `--verificar` acusa junção sobrando, nome repetido, grupo no escopo errado, gancho em dobro, `CLAUDE.md` na raiz e
    um CLAUDE.md pessoal que não seja o import;
  - `--trecho TIPO` dá o `enabledPlugins` de cada tipo de projeto;
  - sem o CLI no PATH, lista os comandos `/plugin` a colar no painel;
  - não troca um CLAUDE.md pessoal diferente do kit sem `--claude-md-kit-vence`;
  - 9 testes.
- **`scripts\atualizar_terceiros.py`:** baixa numa pasta de preparo, compara e, com `--aplicar`, troca a pasta e o
  `origem.json`. Testado com 2 skills, nas duas iguais.
- **Documentos:** `LEIA-ME.md` reescrito e `COMO_OPERAR.md` novo (só a parte "até o F3").
- **O guia** (`GUIA_DAS_SKILLS.docx`, fora do git) abre com a operação, agrupa as skills do kit pelo plugin e traz a
  tabela de que grupo cada pasta liga. Regenerado: 68 de 68, sem descrição faltando.
- **O guia antigo do Claude Docs** ganhou no topo um aviso que aponta para o `.docx` (Q28).
- **Backups de 07/10 em `~\.claude\backups`:**
  - `settings.json.2026-10-07_antes-do-F1b`;
  - `skills-juncoes-2026-10-07.txt`;
  - `CLAUDE.md.2026-10-07_hardlink-antes-do-import`;
  - `claude-pastas-local.json.2026-10-07_antes-do-F1b`.

## Riscos e pendências

- **Remote Control:** ligou sozinho no painel do VS Code. Em 07/10, o `PushNotification` respondeu "Mobile push
  requested". A `--bg` fica para o F3a.
- **Engenharia fora dos projetos:** `desosp-app`, `desosp-censo` e `desosp-hc` estão sem `tdd`, `diagnosing-bugs`,
  `web-design-guidelines` etc. até as fases deles, por decisão do Ettore. A R0 liga só no app, com `--scope local`.
- **`organizar-projetos` ainda cita o velho:** o `ORGANIZAR.md`, o `reaproveitar.md`, o `prompts.md` e o
  `inventario.py` falam de `ligar_claude.py`, junções e hardlink. O `pastas.py ligar-gancho` gravaria um 2º gancho no
  settings. **Não usar até o F2a**, que os atualiza.
- **`/reload-plugins` no painel:** não foi testado, porque não roda fora do painel. A edição já vale numa sessão nova
  (testado).
- **Achado: o `cc-plugin-telemetry`.**
  - É um mod embutido do Claude Code que manda registros de uso à Anthropic. Pelo README do mod, nenhum texto livre vai
    junto.
  - Desligar com `DISABLE_TELEMETRY` também desliga o `Monitor`. Com `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`, cai
    ainda o Remote Control.
  - Decisão do Ettore, para depois; nada mudou.
- **Nome repetido fora do kit:** `deep-research` existe embutido e como sincronizada do claude.ai.
- **Herdadas da R1:**
  - o esforço `max` nos subagentes (o F2a confere);
  - os bugs da `--bg` no Windows (o F3a);
  - o conector do Drive desligado;
  - as 6 lápides do `C:`;
  - o `gh` não instalado.

## Como retomar

1. `git pull --ff-only`, depois `python scripts\instalar_kit.py --verificar` (0 achados).
2. Ler este arquivo e o `caixa\INDICE.md`.
3. Abrir o F2a com o prompt do plano.
4. Antes de commit: `python scripts\checa_kit.py --tudo` (o gancho roda o `--staged`).
