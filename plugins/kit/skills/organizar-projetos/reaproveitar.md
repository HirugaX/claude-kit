# Reaproveitar — o que o PC já tem, antes de instalar qualquer coisa

A fase 0 do `/organizar-projetos` ([SKILL.md](SKILL.md)). O erro mais provável num PC novo não é faltar algo: é **instalar de novo
o que já existe** (uma segunda cópia da skill, um segundo gancho, uma linha repetida no CLAUDE.md, um segundo
pacote de ícones). Duas cópias divergem no dia em que uma delas muda.

```
python C:\CLAUDE-PROJETOS\claude-kit\plugins\nucleo\pastas\scripts\inventario.py [--kit <kit>] [--mae C:\CLAUDE-PROJETOS] [--raiz D:\ ...] [--json inventario.json]
```

Só lê. Não segue junção. Não abre conteúdo de projeto: lê metadados, os `settings.json`, os `desktop.ini` e os
`CLAUDE.md` (para contar e comparar linhas). Cada item sai com um veredito:

| veredito | quer dizer | o que fazer |
|---|---|---|
| **SERVE** | já existe e é o certo | nada; reaproveitar |
| **DUPLICARIA** | já existe igual | não instalar; usar o que existe (ex.: a cópia de uma skill que um plugin do kit já traz sai) |
| **FALTA** | não existe | instalar, com o "sim" |
| **ATENÇÃO** | existe diferente, ou num lugar perigoso | comparar e perguntar antes de mexer |

## O que ele olha, e a regra de cada coisa

| item | como se reaproveita | nunca |
|---|---|---|
| **skills** em `~\.claude\skills` (por nome e hash, comparadas com as dos plugins do kit, `plugins\<grupo>\skills`) | as do kit chegam pelos plugins (`instalar_kit.py`), não por cópia nem junção. Junção antiga para o kit: o `instalar_kit.py` a tira. Cópia igual à de um plugin: nome repetido, sai (guardada antes). Cópia diferente: comparar e levar ao kit o que só ela tem. Só no PC: fica; se for de uso comum, vai para um plugin do kit (nossa) ou pelo `atualizar_terceiros.py` (de terceiros) | apagar sem guardar; mexer na `synced` (é do claude.ai); `npx skills add` direto (grava em `~\.claude\skills` e repete o nome) |
| **ganchos** no `settings.json` de usuário e de cada projeto | ficam; o das cores é do plugin `nucleo` e não se grava em settings. Achou o das cores num settings (de antes do F1b): `pastas.py desligar-gancho` | sobrescrever a lista de ganchos; o gancho das cores no settings e no plugin (dispara duas vezes) |
| **statusline** e `modelSettings` | ficam; o inventário só mostra | `effortLevel` de topo: não vale para o Opus 5.5 (uso-do-claude §4) — mostrar ao usuário |
| **CLAUDE.md pessoal** (é só a linha de import? as linhas que só ele tem) | o do kit é o original; as linhas que só existem no do PC entram no do kit **com o "sim"**; depois, `instalar_kit.py --claude-md-kit-vence` põe o import (`@C:/CLAUDE-PROJETOS/claude-kit/CLAUDE.md`) | ter dois CLAUDE.md pessoais diferentes |
| **`desktop.ini`** com marca (o nosso `; claude-pastas v1`, o de 30/09 `; DESOSP icones_pastas`, alheio) e as pastas de ícones (`%LOCALAPPDATA%\claude-pastas`, `%LOCALAPPDATA%\DESOSP\icones_pastas`) | o nosso: fica; o de 30/09: o `aplicar` troca; o alheio (ex.: `[LocalizedFileNames]`): fica, e o nosso se acrescenta | um segundo pacote de ícones (FolderPainter e afins não leem o mapa); `.ico` dentro de cada pasta |
| **scripts** do kit (`instalar_kit.py`, `atualizar_terceiros.py`, `perguntas_controle.py`) e o `instalar_kit.py --verificar` | os do kit; os de fora (como um gancho próprio do PC) ficam onde estão e entram no inventário | copiar script do kit para dentro de projeto |
| **pastas de projeto** (com `.git`, `CLAUDE.md`, `.claude` ou `AGENTS.md`) nas raízes de costume: a raiz do disco, a pasta do usuário, Documentos, Área de Trabalho, `OneDrive\Documentos\GitHub` e a mãe | cada uma: git, remote, sem commit, a enviar, memória do Claude (pela chave) | mexer antes da entrevista; **a raiz do disco como repositório** é pergunta ao usuário antes de tudo |
| **o kit e a mãe** | existe? há `CLAUDE.md` na raiz da mãe (não pode)? o sistema de cores já está instalado (`local.json`)? a janela da raiz liga o plugin `kit` (`<mãe>\.claude\settings.json`)? | — |

## Depois do inventário

1. Mostre ao usuário a lista, agrupada por veredito, com o que entra (FALTA aprovado), o que se liga (DUPLICARIA)
   e o que fica de fora — e por quê.
2. Os ATENÇÃO viram perguntas na entrevista ([perguntas.md](perguntas.md)), cada uma escrita como pergunta, com a
   recomendação e o que muda com cada resposta.
3. Instale só o que foi aprovado. Rode o inventário de novo no fim: o que era FALTA virou SERVE, e nada novo
   apareceu como DUPLICARIA.

## O desktop

Desde 07/10 o desktop recebe o kit por `git clone` + `instalar_kit.py` (`claude-kit\caixa\NB-002_2026-10-07_instalar-o-kit-novo.md`).
O que a cópia de 05/10 mostrou (`claude-kit\_do_desktop\desktop_2026-10-05\LEIA-ME.txt`) e ainda vale para a fase 0 lá:
- o `settings.json` de usuário tem **statusline** e um **gancho semanal** (`hooks\arquivo_ia.py`): ficam;
- as quatro skills antigas do kit estão como **pastas copiadas**: viram nome repetido com os plugins e saem (guardadas);
- não há CLAUDE.md pessoal: o `instalar_kit.py` grava o import;
- um repositório direto na raiz do `C:` e arquivos de IA em pastas diferentes: fase 2 e pergunta na entrevista.
