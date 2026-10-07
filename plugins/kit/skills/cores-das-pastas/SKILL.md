---
name: cores-das-pastas
description: O sistema de cores das pastas — a pasta diz "o que eu faço com ela"; pintar, conferir, marcar a provisória, legenda, mapa, VS Code. Só por /cores-das-pastas.
disable-model-invocation: true
---

# O sistema de cores das pastas — a pasta diz "o que eu faço com ela"

Decidido na entrevista de 04/10 (`C:\CLAUDE-PROJETOS\claude-kit\decisoes\2026-10-04_pastas-e-reorganizacao.md`, seções 2
a 4) e nos ícones de 05/10 (`2026-10-05_icones-escolha.md`). O **módulo** é
`C:\CLAUDE-PROJETOS\claude-kit\plugins\nucleo\pastas\`: a tabela única é o `mapa.json`; os comandos são do
`scripts\pastas.py`. Os desenhos dos ícones: `/icones`. PC novo: `/organizar-projetos`, fases 0 e 8.

## Os verbos e as marcas

| | o que significa para o usuário | desenho | cor |
|---|---|---|---|
| **Eu alimento** | deposito os arquivos de cada rodada; o programa os consome e arquiva | seta para baixo | `#D97722` |
| **Eu forneço fontes** | trago documento de referência; a IA consulta; ninguém altera | mão com chip | `#7B5CD6` |
| **Eu leio** | o programa ou o Claude produz para mim; abro e copio; posso apagar rodada velha | livro aberto com brilho | `#25824D` |
| **Trabalhamos juntos** | o programa escreve e eu também edito à mão | cabeça com circuitos | `#0F9BA8` |
| **Não toco** | é do Claude: código, testes, rascunhos, documentos técnicos | braço de robô | `#2F6FD6` |
| **Não toco (correio)** | a caixa de mensagens entre as janelas do Claude | braço de robô + envelope (≥ 48 px) | `#2F6FD6` |
| *marca* **Projeto com IA** | a raiz de cada projeto e a mãe: "aqui a IA trabalha; dentro, siga as cores" | engrenagem com "AI" | `#105C40` |
| *marca* **Dado real / sem cópia** | a pasta inteira: só o programa mexe; sem backup | cadeado no circuito | `#D23B3B` |
| *marca* **Criada pela IA — falta classificar** | pasta nova fora do mapa, à espera da cor | robô com `?` | `#8C8C8C` |

## A regra de cada pasta (`regras.py`)

1. Nome na lista `nunca_cor` (`.git`, `node_modules`, `.venv`, `__pycache__`, ...) → sem cor, e não desce.
2. Entrada no mapa (exata; depois padrão com `* ? [ ]`, parte a parte) → vale ela.
3. Senão, herda da pasta de cima pelo campo `filhas` do verbo: **Dado real → Não toco** (o vermelho não passa às
   filhas); **correio → Não toco**; **Projeto com IA → provisória** (filha da raiz sem linha no mapa: o Claude
   pergunta); **provisória → sem cor** (as filhas esperam a decisão da mãe delas).
4. `sem-cor` é a pasta de rodada ou passageira: nenhum `desktop.ini`, e o sistema não desce nela.

Caminho se compara **por partes, sem diferenciar maiúscula**, nunca por `startswith` (`desosp-app` é prefixo de
`desosp-app-dados`). Junção e link nunca se seguem.

### Pastas passageiras — sempre sem cor

O ícone é um `desktop.ini` **dentro** da pasta. Pasta com `desktop.ini` nunca fica vazia, e programa que só apaga
pasta vazia a deixa para sempre; programa que move "todo arquivo da pasta" leva o ícone junto. Por isso toda pasta
que um programa cria e apaga (a rodada corrente, a área de espera, as subpastas que um fechamento esvazia) entra no
mapa como `sem-cor`. **Quem lista é a janela de cada projeto**, lendo o código; o kit só registra (campo
`_passageiras` de cada projeto no `mapa.json`).

## O `desktop.ini`

```
; claude-pastas v1 eu-alimento
[.ShellClassInfo]
IconResource=C:\Users\<você>\AppData\Local\claude-pastas\icones\eu-alimento.ico,0
InfoTip=Eu alimento — <a dica>. Legenda: C:\CLAUDE-PROJETOS\LEGENDA DAS PASTAS.html
```

- UTF-16 LE com BOM e CRLF; o arquivo oculto e de sistema; a pasta com `+s` e **sem `+r`** (o `+r` deixou cópia
  impossível de apagar: WinError 5). Nunca `ConfirmFileOp`.
- Só se reescreve se mudou. O `desktop.ini` alheio (ex.: `[LocalizedFileNames]`) mantém as seções dele; o de 30/09
  (`; DESOSP icones_pastas`) se troca inteiro.
- A dica (`InfoTip`) aparece ao passar o mouse e na coluna **Comentários** do Explorador.

## Os comandos (`python <módulo>\scripts\pastas.py ...`)

| comando | quando | o que faz |
|---|---|---|
| `instalar [--mae ...] [--lapide C:\VELHO ...]` | uma vez por PC (Pillow) | `%LOCALAPPDATA%\claude-pastas\local.json` (a mãe, o módulo, os ícones, as lápides); os `.ico` nas cores do mapa; `desktop.ini` no ignore global do git. Depois de mover o módulo, o `instalar_kit.py` do kit conserta o `"modulo"` |
| `aplicar --ver` | sempre antes de aplicar | conta por projeto e por verbo; lista as provisórias; não escreve nada |
| `aplicar [projeto]` | depois do "sim" | escreve os `desktop.ini`; troca o de 30/09; tira o `+r`; tira o nosso ini de pasta que virou sem cor. Antes de mexer num `desktop.ini` alheio ou de 30/09, guarda o de antes em `%LOCALAPPDATA%\claude-pastas\antes\<data_hora>\` |
| `conferir` | depois de aplicar, e quando quiser | sai 1 se achar: pasta sem ini, verbo diferente do mapa, `+r`, `.ico` ausente ou de 30/09, ini em pasta sem cor (ou dentro dela), provisória pendente, `desktop.ini` no `git status`, marca da web, lápide ausente, o gancho fora do plugin `nucleo` ou também num `settings.json`. Avisa (sem falhar) o conflito de nome no VS Code |
| `marcar <pasta> <verbo>` | a resposta à pergunta da provisória | grava a linha no `mapa.json` e pinta a pasta (e as filhas que herdam) |
| `legenda` | depois de mudar o mapa | `<mãe>\LEGENDA DAS PASTAS.html`, gerado do mesmo mapa |
| `vscode [--ver]` | depois de aplicar | no `.vscode\settings.json` de cada projeto: `material-icon-theme.folders.customClones` e `peacock.color`; o arquivo vai para o `.git\info\exclude`. Não mexe em `settings.json` versionado nem em JSON com comentário |
| `desligar-gancho` | se o `conferir` ou o `inventario.py` acharem o gancho num `settings.json` | tira o gancho antigo (de antes do F1b) do settings, guardando cópia; os outros ganchos ficam |
| `remover [pasta]` | para desfazer | tira os nossos `desktop.ini`; o alheio fica, sem as nossas linhas |

## O gancho (`gancho.py`)

- É do plugin `nucleo` (`plugins\nucleo\hooks\hooks.json`): liga em todo projeto onde o `nucleo` está ligado, sem
  gravar nada em `settings.json`. `PostToolUse`, matcher `Write|Edit|MultiEdit|NotebookEdit|Bash|PowerShell`, timeout
  10 s, comando `python "${CLAUDE_PLUGIN_ROOT}/pastas/scripts/gancho.py" || true` (os ganchos rodam no Git Bash; o
  `|| true` impede que um erro apareça ao Claude em todo comando).
- Fora da mãe, ou sem o sistema instalado: sai calado. Dentro: varre o projeto do arquivo tocado (ou do `cwd`); com o
  `cwd` na mãe, só o primeiro nível.
- Pasta nova (com cor no mapa e sem `desktop.ini`): pinta calado. Provisória: pinta com o `?` e devolve
  `additionalContext` pedindo ao Claude que pergunte a cor e rode o `marcar`.
- Sem pasta nova, não imprime nada. Sai 0 sempre. Não usa Pillow. p95 bem abaixo de 150 ms numa árvore de ~600 pastas.
- Pintar com as suítes paradas: a guarda do app fotografa as pastas de dado durante a suíte, e um `desktop.ini` criado
  no meio dela a faz falhar.

## O VS Code

- Extensões (com o "sim"): `code --install-extension PKief.material-icon-theme` e
  `code --install-extension johnpapa.vscode-peacock`; `"workbench.iconTheme": "material-icon-theme"` no settings
  de usuário do VS Code.
- O `customClones` aceita cor `#RRGGBB`; as bases usadas (`download`, `resource`, `docs`, `shared`, `src`, `mail`,
  `robot`, `secure`, `temp`) existem no Material Icon Theme (`claude-kit\pesquisas\2026-10-05_material-icon-theme-e-peacock.md`).
  O Peacock aplica o `peacock.color` sozinho ao abrir a pasta.
- O Material casa **por nome**: duas pastas com o mesmo nome e verbos diferentes no mesmo projeto ficam sem cor no
  VS Code (o `conferir` e o `vscode --ver` avisam).

## Projeto novo, ou cor nova

- **Projeto novo**: o Claude propõe as linhas dele no `mapa.json` (raiz `projeto-ia`, o verbo de cada pasta, as
  passageiras `sem-cor`, a cor da moldura); o usuário aprova; `aplicar --ver`, `aplicar`, `legenda`, `vscode`.
- **Mudar uma cor**: no `mapa.json` (o `.ico` se recolore na montagem); depois `instalar` de novo em cada PC e
  `aplicar`. Mudar um desenho: `/icones`.
- O mesmo `mapa.json` serve aos dois PCs: projeto que não existe no PC é ignorado.
