# Reaproveitar — o que o PC já tem, antes de instalar qualquer coisa

A fase 0 do [ORGANIZAR.md](ORGANIZAR.md). O erro mais provável num PC novo não é faltar algo: é **instalar de novo
o que já existe** (uma segunda cópia da skill, um segundo gancho, uma linha repetida no CLAUDE.md, um segundo
pacote de ícones). Duas cópias divergem no dia em que uma delas muda.

```
python scripts\inventario.py [--kit <kit>] [--mae C:\CLAUDE-PROJETOS] [--raiz D:\ ...] [--json inventario.json]
```

Só lê. Não segue junção. Não abre conteúdo de projeto: lê metadados, os `settings.json`, os `desktop.ini` e os
`CLAUDE.md` (para contar e comparar linhas). Cada item sai com um veredito:

| veredito | quer dizer | o que fazer |
|---|---|---|
| **SERVE** | já existe e é o certo | nada; reaproveitar |
| **DUPLICARIA** | já existe igual | não instalar; ligar o que existe (ex.: a cópia da skill vira junção para o kit) |
| **FALTA** | não existe | instalar, com o "sim" |
| **ATENÇÃO** | existe diferente, ou num lugar perigoso | comparar e perguntar antes de mexer |

## O que ele olha, e a regra de cada coisa

| item | como se reaproveita | nunca |
|---|---|---|
| **skills** em `~\.claude\skills` (por nome e hash, comparadas com as do kit) | igual à do kit: vira junção (`ligar_claude.py`); diferente: comparar arquivo a arquivo e decidir quem vence (`--kit-vence`, `--pasta-vence`); só no PC: vem para o kit | apagar sem guardar (o `ligar_claude.py` guarda em `skills\_substituidas`); mexer na `synced` (é do claude.ai) |
| **ganchos** no `settings.json` de usuário e de cada projeto | o `pastas.py ligar-gancho` **acrescenta** o PostToolUse ao lado dos ganchos que existem (guarda uma cópia do settings antes) | sobrescrever a lista de ganchos; ligar o das cores duas vezes |
| **statusline** e `modelSettings` | ficam; o inventário só mostra | `effortLevel` de topo: não vale para o Opus 5.5 (uso-do-claude §4) — mostrar ao usuário |
| **CLAUDE.md pessoal** (linhas, quantos nomes o arquivo tem, as linhas que só ele tem) | o do kit é o original; as linhas que só existem no do PC entram no do kit **com o "sim"**; depois, hardlink (`ligar_claude.py`) | editar pela ferramenta Edit (separa o hardlink); ter dois CLAUDE.md pessoais diferentes |
| **`desktop.ini`** com marca (o nosso `; claude-pastas v1`, o de 30/09 `; DESOSP icones_pastas`, alheio) e as pastas de ícones (`%LOCALAPPDATA%\claude-pastas`, `%LOCALAPPDATA%\DESOSP\icones_pastas`) | o nosso: fica; o de 30/09: o `aplicar` troca; o alheio (ex.: `[LocalizedFileNames]`): fica, e o nosso se acrescenta | um segundo pacote de ícones (FolderPainter e afins não leem o mapa); `.ico` dentro de cada pasta |
| **scripts** do kit (`ligar_claude.py`, `perguntas_controle.py`) | os do kit; os de fora (como um gancho próprio do PC) ficam onde estão e entram no inventário | copiar script do kit para dentro de projeto |
| **pastas de projeto** (com `.git`, `CLAUDE.md`, `.claude` ou `AGENTS.md`) nas raízes de costume: a raiz do disco, a pasta do usuário, Documentos, Área de Trabalho, `OneDrive\Documentos\GitHub` e a mãe | cada uma: git, remote, sem commit, a enviar, memória do Claude (pela chave) | mexer antes da entrevista; **a raiz do disco como repositório** é pergunta ao usuário antes de tudo |
| **o kit e a mãe** | existe? há `CLAUDE.md` na raiz da mãe (não pode)? o sistema de cores já está instalado (`local.json`)? | — |

## Depois do inventário

1. Mostre ao usuário a lista, agrupada por veredito, com o que entra (FALTA aprovado), o que se liga (DUPLICARIA)
   e o que fica de fora — e por quê.
2. Os ATENÇÃO viram perguntas na entrevista ([perguntas.md](perguntas.md)), cada uma escrita como pergunta, com a
   recomendação e o que muda com cada resposta.
3. Instale só o que foi aprovado. Rode o inventário de novo no fim: o que era FALTA virou SERVE, e nada novo
   apareceu como DUPLICARIA.

## O que já se sabe do desktop (05/10/2026)

Pela cópia que veio de lá (`claude-kit\_do_desktop\desktop_2026-10-05\LEIA-ME.txt`):
- as quatro skills do kit estão como **pastas copiadas**, iguais à base de 04/10 (todo hash bate): o
  `ligar_claude.py --kit-vence` as troca por junção; se o app Claude Desktop esconder skill por junção, voltar ao modo
  cópia e anotar;
- **não há CLAUDE.md pessoal**: o do kit entra como novo (hardlink);
- o `settings.json` de usuário de lá tem **statusline** e um **gancho semanal** (`hooks\arquivo_ia.py`, que regera
  `D:\FINANCEIRO CLAUDE\_ia`): o `ligar-gancho` acrescenta ao lado deles, sem tocar;
- `effortLevel` de topo já saiu de lá; Opus 5.5 e Sonnet 5.5 estão em `medium`;
- um repositório direto na raiz do `C:` e arquivos de IA em pastas diferentes: fase 2 e pergunta na entrevista.
