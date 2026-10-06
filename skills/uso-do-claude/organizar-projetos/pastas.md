# O sistema de cores das pastas — a pasta diz "o que eu faço com ela"

Decidido na entrevista de 04/10 (`claude-kit\decisoes\2026-10-04_pastas-e-reorganizacao.md`, seções 2 a 4) e nos
ícones de 05/10 (`2026-10-05_icones-escolha.md`). Aqui: como funciona e como se usa. A tabela única é o
[mapa.json](mapa.json); os comandos são do `scripts\pastas.py`.

## Os verbos e as marcas

| | o que significa para o usuário | desenho | cor |
|---|---|---|---|
| **Eu alimento** | deposito os arquivos de cada rodada; o programa os consome e arquiva | seta para baixo | `#D97722` |
| **Eu forneço fontes** | trago documento de referência; a IA consulta; ninguém altera | mão com chip | `#7B5CD6` |
| **Eu leio** | o programa ou o Claude produz para mim; abro e copio; posso apagar rodada velha | livro aberto com brilho | `#25824D` |
| **Trabalhamos juntos** | o programa escreve e eu também edito à mão | cabeça com circuitos | `#0F9BA8` |
| **Não toco** | é do Claude: código, testes, rascunhos, documentos técnicos | braço de robô | `#2F6FD6` |
| **Não toco (correio)** | a caixa de mensagens entre as janelas do Claude | braço de robô + envelope (≥ 48 px) | `#2F6FD6` |
| *marca* **Projeto com IA** | a raiz de cada projeto e a mãe: "aqui a IA trabalha; dentro, siga as cores" | engrenagem com "AI" | `#105C40` (a cor original do desenho) |
| *marca* **Dado real / sem cópia** | a pasta inteira: só o programa mexe; sem backup | cadeado no circuito | `#D23B3B` |
| *marca* **Criada pela IA — falta classificar** | pasta nova fora do mapa, à espera da cor | robô com `?` (o `?` sozinho em 16-24 px) | `#8C8C8C` |

Os desenhos são a **versão 4**, aprovada pelo Ettore em 05/10/2026 (`claude-kit\decisoes\2026-10-05_icones-escolha.md`):
o pacote dele (versão 3) e, das referências dele, o braço de robô, o chip, o cadeado no circuito e o robô, redesenhados
no mesmo estilo. A origem de cada ícone está no `icones\quadros.json`.

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
mapa como `sem-cor`. **Quem lista é a janela de cada projeto**, lendo o código; o kit só registra. Os registros de
05/10 estão no `mapa.json` (campo `_passageiras` de cada projeto).

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
- O `.ico` se monta em cada PC (`pastas.py instalar`, a partir de `icones\`): desde junho de 2026 o Windows ignora
  `desktop.ini` com marca da web, e `.ico` baixado pronto pode vir marcado.
- A dica (`InfoTip`) aparece ao passar o mouse e na coluna **Comentários** do Explorador.

## Os comandos

| comando | quando | o que faz |
|---|---|---|
| `pastas.py instalar [--mae ...] [--lapide C:\VELHO ...]` | uma vez por PC (Pillow) | `%LOCALAPPDATA%\claude-pastas\local.json` (a mãe, o módulo, os ícones, as lápides); os `.ico` nas cores do mapa; `desktop.ini` no ignore global do git |
| `pastas.py aplicar --ver` | sempre antes de aplicar | conta por projeto e por verbo; lista as provisórias; não escreve nada |
| `pastas.py aplicar [projeto]` | depois do "sim" | escreve os `desktop.ini`; troca o de 30/09; tira o `+r`; tira o nosso ini de pasta que virou sem cor. Antes de mexer num `desktop.ini` alheio ou de 30/09, guarda o de antes em `%LOCALAPPDATA%\claude-pastas\antes\<data_hora>\` (a volta é exata) |
| `pastas.py conferir` | depois de aplicar, e quando quiser | sai 1 se achar: pasta sem ini, verbo diferente do mapa, `+r`, `.ico` ausente ou de 30/09, ini em pasta sem cor (ou dentro dela), provisória pendente, `desktop.ini` no `git status`, marca da web, lápide ausente, mapa diferente entre o kit e a cópia de `~\.claude\skills`. Avisa (sem falhar) o conflito de nome no VS Code |
| `pastas.py marcar <pasta> <verbo>` | a resposta à pergunta da provisória | grava a linha no `mapa.json` e pinta a pasta (e as filhas que herdam) |
| `pastas.py legenda` | depois de mudar o mapa | `<mãe>\LEGENDA DAS PASTAS.html`, gerado do mesmo mapa (sem atalho na Área de Trabalho) |
| `pastas.py vscode [--ver]` | depois de aplicar | no `.vscode\settings.json` de cada projeto: `material-icon-theme.folders.customClones` (as mesmas cores, por nome de pasta) e `peacock.color`; o arquivo vai para o `.git\info\exclude` (não se versiona). Não mexe em `settings.json` versionado nem em JSON com comentário |
| `pastas.py ligar-gancho` / `desligar-gancho` | com as outras janelas fechadas | o PostToolUse no `settings.json` de usuário, ao lado dos ganchos que existem (guarda cópia antes) |
| `pastas.py remover [pasta]` | para desfazer | tira os nossos `desktop.ini`; o alheio fica, sem as nossas linhas |

## O gancho (`gancho.py`)

- `PostToolUse`, matcher `Write|Edit|MultiEdit|NotebookEdit|Bash|PowerShell`, timeout 10 s, comando
  `python "<módulo>/scripts/gancho.py" || true` (os ganchos rodam no Git Bash; o `|| true` impede que um erro apareça
  ao Claude em todo comando).
- Fora da mãe, ou sem o sistema instalado: sai calado. Dentro: varre o projeto do arquivo tocado (ou do `cwd`); com o
  `cwd` na mãe, só o primeiro nível.
- Pasta nova (com cor no mapa e sem `desktop.ini`): pinta calado. Provisória: pinta com o `?` e devolve
  `additionalContext` pedindo ao Claude que pergunte a cor e rode o `marcar`.
- Sem pasta nova, não imprime nada. Sai 0 sempre. Não usa Pillow. Medido nos testes: p95 bem abaixo de 150 ms
  numa árvore de ~600 pastas.
- Antes de ligar: um teste numa sessão nova (`claude -p`) confere que o `additionalContext` chega (uso-do-claude §9b).

## O VS Code

- Extensões (com o "sim"): `code --install-extension PKief.material-icon-theme` e
  `code --install-extension johnpapa.vscode-peacock`; `"workbench.iconTheme": "material-icon-theme"` no settings
  de usuário do VS Code.
- O `customClones` aceita cor `#RRGGBB`; as bases usadas (`download`, `resource`, `docs`, `shared`, `src`, `mail`,
  `robot`, `secure`, `temp`) existem no Material Icon Theme (conferido em 05/10,
  `claude-kit\pesquisas\2026-10-05_material-icon-theme-e-peacock.md`). O Peacock aplica o `peacock.color` sozinho ao
  abrir a pasta. Conferir na primeira janela: se o clone não pegar no settings do projeto, ele vai para o de usuário.
- O Material casa **por nome**: duas pastas com o mesmo nome e verbos diferentes no mesmo projeto ficam sem cor no
  VS Code (o `conferir` e o `vscode --ver` avisam).

## Projeto novo, ou PC novo

- **Projeto novo**: o Claude propõe as linhas dele no `mapa.json` (raiz `projeto-ia`, o verbo de cada pasta, as
  passageiras `sem-cor`, a cor da moldura); o usuário aprova; `aplicar --ver`, `aplicar`, `legenda`, `vscode`.
- **PC novo**: o [ORGANIZAR.md](ORGANIZAR.md), fases 0 e 8. O mesmo `mapa.json` serve aos dois PCs: projeto que não
  existe no PC é ignorado.
- **Mudar uma cor ou um desenho**: a cor muda no `mapa.json` (o `.ico` se recolore na montagem); o desenho, em
  `icones\<id>\<px>.png`. `desenho.py quadros <pacote>` refaz tudo pela receita (`ORIGEM`, no `desenho.py`) a partir
  do pacote do Ettore, enquanto ele existir em `prototipos-icones\amostra_gerada_ettore`. Depois da limpeza (fase 9),
  os quadros do kit passam a ser a única fonte. Depois de mudar, `instalar` de novo em cada PC e `aplicar`.
