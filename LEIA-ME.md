# claude-kit — tudo o que é do Claude Code, num lugar só

Criado em 03/10/2026 em `C:\CLAUDE`; mudou para `C:\CLAUDE-PROJETOS\claude-kit` em 05/10/2026, ao lado dos
projetos (`desosp-censo`, `desosp-app`, `desosp-app-dados`, `desosp-hc`). Vale para todos os projetos desta
máquina. O original do kit é o do notebook; o desktop recebe uma cópia (por pendrive).

## O que mora aqui

| Pasta ou arquivo | O que é |
|---|---|
| `skills\` | as skills pessoais: `uso-do-claude` (modelo, esforço, janelas, contexto, a biblioteca de pesquisas; e o módulo `organizar-projetos`: reunir os projetos de um PC, GitHub e o sistema de cores das pastas, aplicado no notebook em 05/10), `recursos-do-projeto` (depois do `/grill-me`, que recursos um projeto usa e quais ficam de fora), `grill-me` e `grilling` (Matt Pocock: entrevista de planejamento); e as instaladas pelo `npx skills` (em 05/10, às 23:47, entraram 24, como `tdd`, `to-spec`, `wayfinder` e `chief-of-staff`; a lista é a própria pasta) |
| `pesquisas\` | a biblioteca: antes de pesquisar, procure no `INDICE.md`; depois, salve lá (regra na `uso-do-claude` §5) |
| `decisoes\` | os registros das entrevistas e das mudanças grandes (a de 04/10: `2026-10-04_pastas-e-reorganizacao.md`) |
| `fontes\` | as pesquisas que viraram skill (`claude-efficiency-report.md` → `recursos-do-projeto`) |
| `scripts\ligar_claude.py` | liga esta pasta ao Claude Code (abaixo); o teste dele está em `scripts\tests\` |
| `scripts\perguntas_controle.py` | prova por perguntas numa sessão nova (`uso-do-claude` §9b) |
| `_do_desktop\` | a comparação com a cópia do desktop: a base do notebook antes da mudança e o que vier de lá |
| `CLAUDE.md` | as suas regras pessoais, lidas por toda janela de todo projeto |
| `LEIA-ME.md` | este arquivo |

## Como o Claude Code acha o que está aqui

O Claude Code só procura skills em `C:\Users\ettor\.claude\skills` e só lê o `CLAUDE.md` pessoal em
`C:\Users\ettor\.claude\CLAUDE.md`. Os arquivos de verdade moram aqui, e lá ficam ligações:

- cada skill: uma **junção** (o atalho de pasta do Windows);
- o `CLAUDE.md`: um **hardlink** (o mesmo arquivo com dois endereços; editar um é editar o outro).

Instalou ou atualizou uma skill com `npx skills`? Ela cai na pasta do Claude Code. Rode:

```
python C:\CLAUDE-PROJETOS\claude-kit\scripts\ligar_claude.py
```

- Skill nova: vem para cá e fica a junção no lugar.
- Skill que já existe aqui com conteúdo diferente: o script **avisa e não mexe**. Rode de novo com
  `--pasta-vence` (é atualização do npx) ou `--kit-vence` (é uma cópia velha; o kit é o original).
- O kit mudou de lugar: rode de novo; junção sem alvo passa a apontar para cá sozinha (ou use
  `--raiz-antiga <lugar velho>`).
- `--conferir` só diz o que faria. Nada é apagado: o que sai vai para `skills\_substituidas\`.

🛑 **O hardlink do `CLAUDE.md` se separa quando o arquivo é gravado "trocando o arquivo inteiro"** — a
ferramenta Edit do Claude Code faz isso (visto em 05/10/2026). Depois de editar o `CLAUDE.md`, confira com
`fsutil hardlink list C:\Users\ettor\.claude\CLAUDE.md` (tem de listar os dois endereços). Se o
`ligar_claude.py` avisar que os dois ficaram diferentes, grave o texto certo **dentro** do arquivo de
`C:\Users\ettor\.claude\CLAUDE.md`, apague o do kit e rode o script de novo.

## O que NÃO veio para cá, e por quê

| O quê | Por que fica onde está |
|---|---|
| `C:\Users\ettor\.claude\settings.json`, o login, o histórico das conversas e as memórias de cada projeto | são do próprio Claude Code, que os escreve o tempo todo; a memória de cada projeto fica na chave do caminho dele (`~\.claude\projects\C--CLAUDE-PROJETOS-<projeto>`) |
| `skills\synced` (em `.claude\skills`) | skills que o claude.ai sincroniza sozinho; não mexer |
| os projetos | moram ao lado, em `C:\CLAUDE-PROJETOS\` (e o `conversation-core`, do Codex, em `C:\GPT\`) |

Os caminhos velhos (`C:\DESOSP`, `C:\DESOSP_APP`, `C:\DESOSP_APP_REAL`, `C:\planilha-hc`,
`C:\conversation-core`, `C:\CLAUDE`) viraram **lápides**: um arquivo vazio com o nome da pasta velha, para
que todo programa que ainda use o caminho antigo dê erro na hora, em vez de recriar uma pasta vazia.

## Onde ler mais

- Guia em linguagem simples: [Guia — skills e uso dos modelos do Claude](https://claude.ai/code/artifact/954e4c88-eb09-4a18-b4e5-f95f27004488)
- As regras: `skills\uso-do-claude\SKILL.md`; as fontes e medições: `skills\uso-do-claude\reference.md`
- Os recursos de um projeto: `skills\recursos-do-projeto\SKILL.md` e o `catalogo.md` ao lado; o exemplo
  aplicado: `C:\CLAUDE-PROJETOS\desosp-app\docs\RECURSOS_CLAUDE_DESOSP.md`
- A mudança de 04-05/10: `decisoes\2026-10-04_execucao-reorganizacao.md`
