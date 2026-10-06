# Plano — protótipos de ícone, reorganização das pastas e sistema de cores (04/10/2026)

## Contexto

A entrevista de 04/10 (registro aprovado: `C:\CLAUDE\decisoes\2026-10-04_pastas-e-reorganizacao.md`) decidiu:
(1) concentrar todo o trabalho com o Claude em `C:\CLAUDE-PROJETOS\`, com nomes novos que fazem o caminho
esquecido **falhar na hora**; (2) um sistema de cores em que a pasta diz "o que eu faço com ela" (5 verbos, 3
marcas), aplicado uma vez por projeto e mantido por um gancho; (3) a biblioteca de pesquisas com a regra
"antes de pesquisar, procurar; depois, salvar". Este plano põe isso em passos verificáveis. O que está no
registro não se rediscute.

Respostas desta janela: o kit viaja por **cópia manual**; **não se sabe** se a janela do desktop mudou a cópia
de lá da `uso-do-claude`; a pasta do kit se chama **`claude-kit`**. A colheita terminou (7 pesquisas novas em
`C:\CLAUDE\pesquisas`, índice conferido por ela).

## O que vi agora (14:10, só leitura)

| fato | fonte |
|---|---|
| `C:\CLAUDE-PROJETOS` vazia; os projetos nos lugares velhos | `Get-ChildItem C:\` |
| **O app está ligado** (`python -m app.iniciar`, desde 08:41) | `Win32_Process` |
| **Foxit com `C:\DESOSP\saida\0210_T\ROUND_113_0210_T.pdf` aberto** | idem |
| O python órfão **21168** (29/09, pai inexistente) continua vivo | idem |
| Sessões ativas na última hora: kernel ×2 (14:07), app (14:06), colheita (14:09, terminou) e esta | `~\.claude\projects\*\*.jsonl` |
| Kernel e app limpos e em dia com `origin/main` (ref local); planilha com a caixa por confirmar | `git status`, `git log origin/main..` |
| Memória: kernel **19** arquivos (eram 16), app 6, planilha 3 | `~\.claude\projects\*\memory` |
| Skills = 4 junções para `C:\CLAUDE\skills`; `CLAUDE.md` pessoal = hardlink com 2 nomes | `Get-ChildItem ~\.claude\skills`, `fsutil hardlink list` |
| `~\.claude.json`: as chaves velhas só têm a confiança (0 permissões, 0 MCP): nada a levar | leitura por Python |
| `settings.json` de usuário sem ganchos; Python 3.12.10 + Pillow 12.3.0; `SegoeIcons.ttf` e `imageres.dll` presentes; sem `core.excludesFile`; sem Material Icon Theme nem Peacock | comandos |
| `ligar_claude.py` fixa `RAIZ = C:\CLAUDE`, recusa junção "para outro lugar", traria cópia velha por cima do kit (no desktop) e pinta com `+r` | `C:\CLAUDE\scripts\ligar_claude.py:23,52-70,112` |
| `C:\CLAUDE\skills` e `scripts` têm `+r` e `desktop.ini` de 30/09 | pesquisa de 30/09 §1c |
| Gerador de 30/09: Python puro, 25 caminhos fixos, `+r`, sem 20/40 px, sem teste — reaproveito o desenho (estilo 1) e o `SHChangeNotify` | `C:\DESOSP_APP\scripts\icones_pastas.py:87-198,245` |
| Clone velho `OneDrive\Documentos\GitHub\desosp-app` (30/09, com `CLAUDE.md`); 154 arquivos "somente leitura" em `Temp\claude\c--DESOSP\88629c23…\scratchpad\ihdl` (cópia de `arquivo\`) | `git log`, contagem |

Revisão isolada do rascunho (subagente Plan): 15 lacunas, todas incorporadas abaixo — as principais são a
lápide nos caminhos velhos (2.4), o retrato do kit antes da cópia sem `+r` (2.6), o comando e o escopo do gancho
(4.5) e o `ConfirmFileOp` fora (4.3).

## Ficha de recursos (skill `recursos-do-projeto`)

AGORA (7)

| recurso | por quê | como saber que funcionou |
|---|---|---|
| retrato antes/depois (contagem, bytes, sha256 do insubstituível, testes pulados) | mover dado real sem backup | o retrato depois é igual ao de antes |
| lápide em cada caminho velho | `mkdir` recriaria a pasta velha vazia, sem erro | `os.makedirs(r'C:\DESOSP\entrada')` dá erro |
| varredura de nomes (regex com `C:\`, `/c/` e as chaves velhas) | caminho esquecido tem de aparecer antes de rodar | lista por projeto; zero no kit e nos settings |
| pytest do pacote das pastas e do `ligar_claude.py` (pastas temporárias) | gancho em toda sessão + escrita em todas as pastas | `python -m pytest -q` verde |
| gancho `PostToolUse` + comando de conferência | "só gancho garante"; o que escapa, a conferência acha | pasta nova pintada; nada impresso sem pasta nova; `conferir` sai 0 |
| ignore global de `desktop.ini` no git | risco da seção 10 | `git check-ignore -v` em cada repositório |
| folha de prova PNG + pastas de amostra no Explorer de verdade | "ícones intuitivos" e escala de 125% | eu vejo a folha; o Ettore vê o Explorer |

QUANDO: Material Icon Theme e Peacock (no passo do VS Code); cache por data da pasta no gancho (se passar de
150 ms); plugin para o kit (se a cópia manual começar a divergir).
NÃO: FolderPainter, CustomFolder e afins (programa instalado que não lê o nosso mapa); `.ico` dentro de cada
pasta (o `fechar_rodada` da planilha o arquivaria); `CLAUDE.md` na raiz da mãe; `ConfirmFileOp=0` (tira o aviso
do Explorer ao apagar pasta vermelha); agentes em paralelo no pacote (arquivos compartilhados); MCP.

## Passo 1 — Protótipos de ícone (antes de qualquer outra mudança)

Em `C:\CLAUDE-PROJETOS\prototipos-icones\`; nada é aplicado em pasta de projeto.

- `gerar_prototipos.py` (Pillow + `ctypes`) desenha **3 estilos × 9 ícones**: os 5 verbos, "Não toco" com
  envelope (o correio, desenho a partir de 48 px) e as 3 marcas. Os estilos:
  1. **o desenho atual**, com as versões de 20 e 40 px e glifos novos para os verbos novos;
  2. **pasta no estilo Windows 11**, desenhada (aba mais escura, frente em degradê), com emblema da
     `SegoeIcons.ttf`;
  3. **a pasta do próprio Windows** (`imageres.dll`, extraída por tamanho com `PrivateExtractIconsW`),
     recolorida preservando o degradê, com o mesmo emblema.
- Emblemas propostos (nunca só cor): Eu alimento = seta entrando na bandeja · Eu forneço fontes = livro · Eu
  leio = olho · Trabalhamos juntos = lápis · Não toco = robô (é do Claude) · correio = robô + envelope · Projeto
  com IA = brilho ✦ · Dado real = cadeado · Provisória = "?". Os pontos de código da fonte são conferidos numa
  folha renderizada antes de usar.
- Cores: as de 30/09 ficam (laranja `#E8892B`, verde `#2E9E5B`, azul `#2F6FD6`); vermelho `#D23B3B` para dado
  real; cinza para provisória. Para **Eu forneço fontes, Trabalhamos juntos e Projeto com IA**, 3 candidatas
  cada (ex.: roxo/âmbar/marrom; ciano/magenta/verde-água; dourado/grafite/índigo).
- `VER_PROTOTIPOS.html`:
  - cada ícone em 16, 20, 32, 48 e 256 px, em fundo claro e escuro do Explorer, no **tamanho real de tela**
    (largura = px ÷ `devicePixelRatio`, para os 125% não enganarem);
  - abre com um **teste cego**: os ícones sem legenda ("o que esta pasta quer dizer?");
  - no fim, as cores propostas da moldura do Peacock para as 4 janelas (censo, app, hc, kit).
- `amostra-explorador\estilo-N\<verbo>\`: pastas com `desktop.ini` (atributo "sistema") apontando para os
  `.ico` do protótipo. Assim o Ettore vê os três estilos no Explorer de verdade (painel lateral, Detalhes,
  ícones grandes).
- Antes de mostrar, eu confiro: a folha `folha_de_prova.png` aberta por mim e cada `.ico` com os 8 tamanhos.
- **O Ettore escolhe** estilo, cores e emblemas. A escolha vai para `claude-kit\decisoes\` (2.9).

## Passo 2 — A reorganização (seção 6)

Roda **nesta janela** (`C:\CLAUDE-PROJETOS`, que não se move). Cada subpasso para no primeiro erro.

**2.0 Condições** (script `conferir_antes.py` no scratchpad, mais a palavra do Ettore):
- Fechadas: as janelas do Claude do kernel, do app e da colheita; toda janela do VS Code que não seja a de
  `C:\CLAUDE-PROJETOS`; o Explorador aberto dentro das pastas; o Foxit.
- **O app fechado pelo próprio app** (Ctrl+C na janela dele, não `Stop-Process`): nenhum `app.iniciar`, a porta
  8765 livre e o `-wal` do banco ausente ou vazio.
- O órfão 21168 encerrado por mim (`Stop-Process`).
- No kernel e no app, `git fetch` + `git log origin/main..` vazios. A planilha pode ir com a caixa por
  confirmar: mover preserva tudo.
- O script falha se achar processo com caminho velho na linha de comando, ou `.jsonl` de outra sessão escrito
  há menos de 5 minutos.

**2.1 Proteção da pasta de dados na mãe, antes de mover**:
- `C:\CLAUDE-PROJETOS\.ignore` com `desosp-app-dados/`: o ripgrep do Grep e do Glob o respeita.
- `.vscode\settings.json` da mãe com `files.watcherExclude` e `search.exclude` para a mesma pasta.
- Verificação (2.7): Grep **e** Glob na mãe por um nome que só existe nos dados não acham nada. O PowerShell
  continua vendo a pasta; o prompt do app avisa disso.

**2.2 Retrato antes** (`antes.json` no scratchpad: só caminhos, tamanhos e hashes, nenhum conteúdo):
- por pasta de origem, o número de arquivos e os bytes;
- sha256 de: `historico\*.json` do kernel; `desosp_app.db` (com `-wal`, `-shm` e `-journal`, se houver);
  `busca_fts.db` e `_backups\*` dos dados; `privado\*` da planilha; `fontes\*` do kernel; os
  `local_nomes.json`;
- `git rev-parse HEAD` e `git status --porcelain` de cada repositório, mais a lista dos 26 `desktop.ini`;
- a suíte de cada projeto uma vez, com `-q -rs`, em segundo plano (teto de 10 min cada). Guardo a linha final e
  a lista de testes pulados, para as janelas compararem depois. O banco não se abre entre os dois retratos.

**2.3 Os movimentos** — mesmo disco, então `os.rename` (instantâneo e atômico: se algo segura a pasta, falha e
nada se move). Um por vez, nesta ordem, conferindo cada um:
1. `C:\planilha-hc` → `C:\CLAUDE-PROJETOS\desosp-hc`
2. `C:\DESOSP_APP_REAL` → `C:\CLAUDE-PROJETOS\desosp-app-dados`
3. `C:\DESOSP_APP` → `C:\CLAUDE-PROJETOS\desosp-app`
4. `C:\DESOSP` → `C:\CLAUDE-PROJETOS\desosp-censo`
5. `C:\conversation-core` → `C:\GPT\conversation-core` (cria `C:\GPT`)

`C:\DESOSP ARQUIVO` fica onde está.

**2.4 As lápides** (um pedido de administrador, o UAC):
- Um arquivo de 0 byte, "somente leitura", com o nome exato de cada caminho velho: `C:\DESOSP`,
  `C:\DESOSP_APP`, `C:\DESOSP_APP_REAL`, `C:\planilha-hc`, `C:\conversation-core` e, no 2.6, `C:\CLAUDE`.
- Com elas, todo `mkdir` (o `.bat` antigo do app, a exportação, o `run_build`, o "Clone again" do GitHub
  Desktop) falha na hora, em vez de recriar a pasta vazia.
- Verificação: `os.makedirs(r'C:\DESOSP\entrada', exist_ok=True)` levanta erro.
- Até a janela do app terminar, **não abrir o app**. O manual explica as lápides; elas só saem quando a
  varredura daquele projeto der zero.

**2.5 A memória para as chaves novas** (copiar, não mover: as chaves velhas guardam o histórico):
- `C--DESOSP\memory` → `C--CLAUDE-PROJETOS-desosp-censo\memory`
- `c--DESOSP-APP\memory` → `C--CLAUDE-PROJETOS-desosp-app\memory`
- `c--planilha-hc\memory` → `C--CLAUDE-PROJETOS-desosp-hc\memory`

A chave é o caminho com todo caractere não alfanumérico trocado por `-`: confere com `c--CLAUDE-PROJETOS` e
`c--DESOSP-APP`, e o NTFS não distingue maiúscula. O `~\.claude.json` não se edita: cada projeto pede a
confiança uma vez ao abrir. Cada janela de projeto confere que a memória carregou.

**2.6 O kit copiado, religado e corrigido**:
1. Retrato `kit_antes.json` (sha256 de todo arquivo de `C:\CLAUDE`) **antes** da cópia: é a base da
   comparação com o desktop (passo 3).
2. `robocopy C:\CLAUDE C:\CLAUDE-PROJETOS\claude-kit /E /COPY:DAT /DCOPY:T /XJ /XF desktop.ini CLAUDE.md`, e
   depois `attrib -r /s /d` no `claude-kit`. Conferir que todo hash de `kit_antes` está no `claude-kit`.
3. `CLAUDE.md`: um novo nome para o mesmo arquivo, `os.link(~\.claude\CLAUDE.md, claude-kit\CLAUDE.md)`.
4. `claude-kit\scripts\ligar_claude.py`:
   - `RAIZ` derivada da posição do script;
   - junção com alvo na raiz antiga, ou sem alvo, passa a apontar para `claude-kit\skills` (apaga só a junção,
     com `os.rmdir`, nunca `rmtree`);
   - pasta de verdade em `~\.claude\skills` que difere do kit gera ATENÇÃO e **nunca** substitui o kit; com
     `--kit-vence`, ela vai para `_substituidas` e o kit fica;
   - `colorir()` sai (o pacote novo assume).

   Teste: `claude-kit\scripts\tests\test_ligar_claude.py` (junção nova, junção velha re-apontada, alvo
   intacto, cópia velha não vence, hardlink).
5. `ligar_claude.py --conferir`, depois `ligar_claude.py`. Conferir: as 4 junções apontam para `claude-kit`, o
   `SKILL.md` se lê por elas, o hardlink tem 3 nomes.
6. Os textos do kit que citam `C:\CLAUDE` mudam junto (seção 6 do registro):
   - a linha "Tudo do Claude Code mora em…" do `CLAUDE.md` pessoal;
   - `uso-do-claude\SKILL.md:234` e `reference.md:55`;
   - `recursos-do-projeto\SKILL.md`;
   - o `LEIA-ME.md`, reescrito para o lugar novo.

   Depois de cada gravação no `CLAUDE.md`, rodo `fsutil hardlink list`; se o hardlink se separar, o
   `ligar_claude.py` avisa e eu junto. Cada edição fica listada, para o passo 3 separar o que é meu do que é do
   desktop.
7. `C:\CLAUDE` → renomeado para `C:\CLAUDE-antigo-NAO-USAR`, mais a lápide `C:\CLAUDE`. Não é apagar: nada
   depende mais dele, e assim nenhuma janela grava pesquisa no lugar velho sem erro. Só se apaga no passo 6.

**2.7 Conferência depois**:
- `depois.json` igual ao `antes.json`: mesmos arquivos, bytes e hashes, mesmo HEAD e mesmo `git status`;
- os caminhos velhos são lápides;
- o ícone de 30/09 continua aparecendo (aponta para `%LOCALAPPDATA%`, que não se moveu);
- Grep e Glob da mãe não veem os dados;
- `test_ligar_claude.py` verde;
- o menu `/` de uma janela nova mostra as 4 skills.

**2.8 Varredura de nomes**:
- A regex é `(?i)(?:[a-z]:|/[a-z]|//[a-z])[\\/]+(desosp(_app(_real)?)?(?! arquivo)|planilha-hc|claude(?!-projetos)|conversation-core)\b`,
  mais os nomes das chaves velhas (`C--DESOSP`, `c--DESOSP-APP`, `c--planilha-hc`, `c--CLAUDE`).
- Onde: o kit; o `settings.json`; a memória das chaves novas; `.git\config` e `.claude\settings*.json` de cada
  repositório; os quatro repositórios (sem `.venv`, dados e rodadas).
- O resultado se separa em código, testes, documentos vivos e documentos históricos.
- Comparar sempre por partes do caminho, nunca por `startswith`: `desosp-app` é prefixo de `desosp-app-dados`.

**2.9 Os registros** (em `claude-kit\decisoes\`, sem dado de paciente): `2026-10-04_varredura-caminhos.md`
(uma seção por projeto), `2026-10-04_execucao-reorganizacao.md` (o que foi feito, retratos, horários, e o
**caminho de volta**), a escolha dos ícones, `2026-10-04_prompts-das-janelas.md`.
- **Volta**, se o kernel não estiver pronto em 06/10: tirar as lápides, renomear ao contrário. A memória velha
  continua nas chaves velhas, então a volta é limpa.
- Ettore, à mão: abrir as pastas novas no VS Code e registrá-las de novo no GitHub Desktop ("Locate").

## Passo 3 — Portão da paridade com o desktop (seção 8)

A **parte das pastas** (passo 4) não entra na `uso-do-claude` antes disto.
1. No desktop (prompt **desktop · enviar a cópia**): copiar para o pendrive, com manifesto sha256, tudo o que é
   do kit lá: `~\.claude\skills\`, `~\.claude\CLAUDE.md` e qualquer pasta de kit que a Parte 0 tenha criado.
2. No notebook, em `claude-kit\_do_desktop\2026-10-04\`: comparar com o **`kit_antes.json`** (o notebook antes
   das minhas edições).
   - Igual: o desktop não mudou nada e o portão abre.
   - Diferente: mostro a diferença, junto com as minhas edições (base = `kit_antes`) depois do "sim" do Ettore,
     e só então abro.

## Passo 4 — O sistema de cores (seções 2 a 4)

Construído na janela **claude-kit · sistema de pastas** (contexto novo; o pacote mora no kit), depois do
portão e da escolha dos ícones. Aplicado só depois que as três janelas de projeto terminarem (passo 7).

**4.1 O pacote** (dentro da `uso-do-claude`; o `SKILL.md` ganha só uma linha apontando para `pastas.md`)
```
skills\uso-do-claude\
  pastas.md            a regra: verbos, marcas, a pasta nova, o gancho, a conferência, projeto ou PC novo
  pastas\mapa.json     A TABELA ÚNICA: verbos (cor, emblema, dica), marcas, nunca-cor, cada projeto
  pastas\desenho.py    gera os .ico (16, 20, 24, 32, 40, 48, 64, 256) no estilo escolhido (Pillow)
  pastas\pastas.py     instalar | ligar-gancho | aplicar [--ver] | conferir | marcar <pasta> <verbo> | legenda | vscode | remover
  pastas\gancho.py     o gancho PostToolUse: sem Pillow, usa só a parte de leitura do mapa
  pastas\tests\        pytest em pastas temporárias
```
- `pastas.py instalar` (uma vez por PC):
  - grava `%LOCALAPPDATA%\claude-pastas\local.json` com a mãe e o caminho do kit;
  - gera os ícones em `%LOCALAPPDATA%\claude-pastas\icones\` (gerados em cada PC, nunca levados);
  - grava o ignore global do git (`%USERPROFILE%\.config\git\ignore` com `desktop.ini`).
- `pastas.py ligar-gancho`: separado, porque o Claude Code lê os ganchos ao abrir a sessão e o `settings.json`
  é gravado por ele. Roda só na onda 3, com as outras janelas fechadas.
- O código e o mapa se acham pelo `local.json`, nunca pelo `__file__`. No modo cópia, isso evita duas tabelas.
  O mapa usa caminhos relativos à mãe.

**4.2 A regra de cada pasta** (uma função, a mais testada; caminhos comparados por partes):
1. Nome na lista nunca-cor → sem cor, e não desce.
2. Entrada explícita no mapa → vale ela.
3. Regra do projeto (por exemplo, `saida\DDMM_P` sem cor, `saida\_*` Não toco) → vale ela.
4. Senão, herda da mãe; filha de pasta vermelha → Não toco.
5. Filha da raiz de um projeto, ou da mãe, sem entrada no mapa → **provisória**, e o Claude pergunta a cor.

**4.3 O `desktop.ini`**:
- UTF-16 LE com BOM e CRLF; `IconResource=<ico absoluto>,0`; `InfoTip=<dica> Legenda: C:\CLAUDE-PROJETOS\LEGENDA
  DAS PASTAS.html`; marca `; claude-pastas v1`; **sem `ConfirmFileOp`**.
- O arquivo fica oculto e de sistema. Na pasta: **`+s` e `-r`**.
- Só reescreve se o conteúdo mudou.
- `desktop.ini` alheio (o de `docs\gpt`, `[LocalizedFileNames]`): mantém as seções dele e acrescenta a nossa.
  O de 30/09 (marca `; DESOSP icones_pastas`) é trocado.
- Depois, `SHChangeNotify`.

**4.4 Testes** (`pytest`):
- formato do ini: BOM, UTF-16, CRLF, a dica terminando na legenda, sem `ConfirmFileOp`;
- pasta com `+s` e sem `+r`;
- **`copytree` + `rmtree` de pasta pintada funciona** (a regressão do WinError 5);
- cada regra do 4.2, inclusive `desosp-app` × `desosp-app-dados`;
- o vermelho não passa às filhas; pasta de rodada e pasta passageira nunca recebem ini;
- a troca do ini de 30/09; o ini alheio preservado;
- idempotência: a segunda rodada não escreve nada;
- o gancho:
  - fica calado sem pasta nova e calado fora da mãe;
  - pinta a pasta herdeira;
  - devolve a pergunta para pasta fora do escopo;
  - sai com 0 diante de entrada inválida, script de mapa ausente ou Python sem Pillow.

**4.5 O gancho** (`settings.json` de usuário, nos dois PCs):
- `PostToolUse`, matcher `Write|Edit|MultiEdit|NotebookEdit|Bash|PowerShell`, `timeout` 10 s.
- Comando com barras normais e saída sempre 0: `python "<kit>/skills/uso-do-claude/pastas/gancho.py" || true`.
  Os ganchos rodam no Git Bash, e o código 2 de um script ausente mostraria o erro ao Claude em todo comando.
- **Age só dentro da mãe**: fora dela, sai calado. Varre o projeto do arquivo, ou do `cwd`, pulando nunca-cor e
  rodadas; com o `cwd` na mãe, só o primeiro nível.
- Sem pasta nova, não imprime nada (zero token). Pasta nova no escopo: pinta calado. Fora do escopo: marca
  provisória e devolve `additionalContext`, pedindo ao Claude que pergunte a cor.
- Medida: 20 chamadas sem pasta nova, com o `cwd` no kernel e na mãe, p95 < 150 ms.
- Antes de ligar, um teste numa sessão nova (`claude -p`) confere que o formato do `additionalContext` chega.

**4.6 A conferência** (`pastas.py conferir`, sai 1 se achar algo):
- pasta sem ini que deveria ter;
- verbo diferente do mapa;
- pasta com `+r`;
- ini apontando para `.ico` ausente ou para o pacote de 30/09;
- ini em pasta nunca-cor ou de rodada;
- provisórias pendentes;
- `desktop.ini` visível no `git status` de algum repositório;
- ini com marca da web (`Zone.Identifier`);
- lápides ausentes;
- hash do mapa diferente entre o kit e `~\.claude\skills` (modo cópia).

**4.7 O manual**: `pastas.py legenda` gera `C:\CLAUDE-PROJETOS\LEGENDA DAS PASTAS.html` a partir do mesmo
`mapa.json`, com os ícones embutidos.
- Conteúdo:
  - os verbos, as cores e os desenhos;
  - o mapa de cada projeto;
  - a pasta de dados do app: o que é, por que existe, que não se mexe nela por fora do app;
  - as lápides;
  - `C:\GPT` fora do sistema;
  - como aplicar num projeto ou PC novo.
- Claro e escuro; sem atalho na Área de Trabalho.
- Teste: todo verbo e todo projeto do mapa aparecem.

**4.8 O espelho no VS Code**:
- Instalar `PKief.material-icon-theme` e `johnpapa.vscode-peacock` (`code --install-extension`) e pôr
  `workbench.iconTheme` no settings de usuário do VS Code.
- `pastas.py vscode` grava no `.vscode\settings.json` de cada projeto os
  `material-icon-theme.folders.customClones` (por nome de pasta, as mesmas cores) e o `peacock.color`.
- Põe `.vscode/settings.json` no `.git\info\exclude` de cada repositório: é gerado do mapa em cada PC, não se
  versiona.
- Conflito de nome dentro de um projeto (o Material casa por nome) sai na conferência e na legenda.

**4.9 O mapa completo — para o Ettore aprovar de uma vez** (o verbo de cada pasta; as filhas herdam, salvo
exceção)

| projeto | pastas |
|---|---|
| **a mãe** `C:\CLAUDE-PROJETOS` | marca **Projeto com IA** *(proposta: ela é "aqui a IA trabalha")* · `prototipos-icones`: Eu leio (sai depois) |
| **desosp-censo** | raiz: **Projeto com IA** · Não toco: `desosp`, `tests`, `scripts` (+`git`), `.claude` (+filhas), `docs` (+`gemini`, `guia`, `regras`, `scripts`, `templates`) · correio: `docs\para_o_app`, `para_o_kernel`, `para_a_planilha` · Eu leio: `docs\gpt`, `arquivo` · Eu alimento: `entrada` (dica cita SIST_, BRUTO_, PDF da UTI, HC_, PEND_, ADENDO; não cita EVOL_) · Trabalhamos juntos: `saida` · Eu forneço fontes: `fontes` (+filha) · **Dado real**: `historico` (dica: "o programa e você editam; sem backup") |
| exceções do censo | sem cor: `saida\DDMM_P`; **todas as filhas de `arquivo\`** (rodadas e `_RECUPERADO_*`), sem descer; pastas **passageiras** que o pipeline cria e apaga (`entrada\_ESPERA` e as que a janela do kernel listar), porque pasta pintada nunca fica vazia (`arquivo_rodada.py:149`) · Não toco: `saida\_extracao`, `saida\_revisao_02out` (+`backup`) |
| **desosp-app** | raiz: **Projeto com IA** · Não toco: `app` (+todas), `tests` (+`vendor`), `scripts` (+`git`), `.claude` (+filhas), `workspace_dev` (+`_backups`, `_envios`, `_fotos`), `docs` · correio: `docs\para_o_app`, `para_o_kernel`, `para_a_planilha` · Eu forneço fontes: `docs\fontes` (+7 filhas) |
| **desosp-app-dados** | raiz: **Dado real** (a pasta inteira) · filhas (`arquivo`, `saida`, `historico`, `entrada`, `_backups`, `_envios` e netas): Não toco · rodadas em `arquivo\` e `saida\`: sem cor · o destino novo dos backups (a janela do app propõe) entra no mapa antes da onda 3 |
| **desosp-hc** | raiz: **Projeto com IA** · Não toco: `scripts` (+`leitor_pdf`, `migracao`), `tests`, `.githooks`, `.claude` (+`commands`), `trabalho` (+`logs`, `rec`, `testes_antes_depois`), `modelos` (+7), `docs` (+`legado`, `mudancas`), `historico\_arquivo_tecnico` (+filhas) · correio: `docs\para_a_planilha`, `para_o_app`, `para_o_kernel` · Eu alimento: `entrada` · Eu leio: `saida` (+`boletins`), `planilhas` (+`v315`), `historico`, `historico\placar`, `historico\rodadas` · Eu forneço fontes: `docs\premiacoes` (+filhas) *(o levantamento o pôs em "alimento"; confirmar)* · **Dado real**: `privado` |
| exceções do hc | sem cor: as filhas de `historico\rodadas\` (rodadas) e as passageiras que a janela da planilha listar |
| **claude-kit** | raiz: **Projeto com IA** · Não toco: `skills` (+cada skill, `_substituidas`), `scripts`, `_do_desktop` · Eu forneço fontes: `fontes`, `skills\uso-do-claude\fontes` · Eu leio: `pesquisas`, `decisoes` |
| nunca cor | `.git`, `.vscode`, `__pycache__`, `.pytest_cache`, `.mypy_cache`, `.ruff_cache`, `node_modules`, `.venv`, `*.egg-info`, `.claude\worktrees`, `build`, `dist`, `htmlcov`, as temporárias, as rodadas; `C:\GPT` e `C:\DESOSP ARQUIVO` inteiros |

## Passo 5 — A biblioteca (seção 5), feita no 2.6 junto com os textos do kit
- `uso-do-claude\SKILL.md` §5 ganha o item "**Antes de pesquisar, procurar; depois, salvar**":
  - onde: `claude-kit\pesquisas\INDICE.md`, um arquivo por pesquisa com o cabeçalho fixo;
  - o subagente devolve a pesquisa e a janela principal a salva;
  - nunca dado de paciente nem trecho de documento da operadora.
- `CLAUDE.md` pessoal ganha uma linha: "Antes de pesquisar (internet ou varredura grande), procure em
  `C:\CLAUDE-PROJETOS\claude-kit\pesquisas\INDICE.md`; depois, salve lá no formato do índice."
- As duas edições entram na lista de edições minhas do passo 3.

## Passo 6 — Apagar o `C:\CLAUDE-antigo-NAO-USAR` (o último de todos)
1. Só quando tudo isto estiver certo:
   - as 4 junções apontam para `claude-kit`;
   - o desktop está em paridade;
   - todo hash de `kit_antes` está no `claude-kit` (ou na lista de edições);
   - a varredura não acha `C:\CLAUDE` vivo;
   - as cores estão aplicadas e conferidas.
2. Então, nesta ordem:
   1. `os.unlink` do `CLAUDE.md` de lá (senão o hardlink vai junto para a Lixeira);
   2. `attrib -r` nas pastas;
   3. conferir que não há ponto de reparo dentro;
   4. mandar a pasta para a **Lixeira** (recuperável).
3. Depois: `fsutil hardlink list` mostra 2 nomes, e o menu `/` mostra as 4 skills.

## Passo 7 — As janelas e a ordem (pesquisa das janelas paralelas: no máximo 2 trabalhando ao mesmo tempo)

```
agora     [esta janela] 1 protótipos → Ettore escolhe → (/compact) → 2 reorganização, 5 → prompts
onda 1    [desosp-censo] ║ [desosp-hc]          ║ Ettore no desktop: "enviar a cópia" (passo 3.1)
onda 2    [desosp-app]   ║ [claude-kit: passo 3.2 e construir o pacote, 4.1-4.8]
          (o app depois do kernel: lê a AT dele e testa a puxada no lugar novo)
onda 3    [claude-kit: aplicar] o mapa aprovado, ligar o gancho, VS Code; as três suítes de novo e a conferência = 0;
          o Ettore olha → passo 6
onda 4    [desktop · kit e cores]
```
- Em paralelo, só o que não se cruza: repositórios diferentes, e nenhuma janela escreve no arquivo de outra (o
  correio é o protocolo de caixas que já existe).
- Em sequência, o que depende de decisão ou resultado de outra janela.
- A aplicação das cores espera três coisas: os caminhos corrigidos, a planilha sem apagar `desktop.ini` e as
  rodadas de prova.
- Na onda 3, as suítes rodam de novo já com as cores, porque o censo real (07 ou 08/10) é a primeira execução
  com elas.

**Os prompts** (o texto completo vai para `claude-kit\decisoes\2026-10-04_prompts-das-janelas.md` e para o
chat; sem nome de paciente, de funcionário ou da operadora). Todos levam:
- o registro e a varredura do projeto, como leitura;
- "não aplicar cores nem mexer em `desktop.ini`" (exceto o kit);
- a lista das pastas passageiras do projeto (para o mapa) e dos `listdir`, `iterdir` e `glob('*')` sobre
  pastas que serão pintadas;
- a suíte com `-rs` e o mesmo número de pulados do retrato 2.2, com cada pulado explicado;
- commit por caminho explícito;
- o resumo com a linha "Sinais de insuficiência do modelo".

| janela (pasta) | 1ª linha | o que faz |
|---|---|---|
| **desosp-censo** (`…\desosp-censo`) | Opus 5.5 · `/effort high`: a raiz de dados errada escreve a rodada no lugar errado sem erro | confiança e memória (corrigir os caminhos velhos dela); `CONFIG_DESOSP.py` com a raiz derivada da posição; o teste que fixa `C:\DESOSP` (`test_regressoes.py:5265-5277`) e o `REF_medir_relevancia_hd.py`; as regras; o "rodar da raiz" do `CLAUDE.md`; o `ESTRUTURA.md` (fontes, `.claude`, caixas, rodadas); regerar o guia em Word; a suíte; a **rodada de prova**, que não escreve em `historico` nem na rodada corrente (propor o modo ao Ettore); AT ao app; push |
| **desosp-hc** (`…\desosp-hc`) | Opus 5.5 · `/effort high`: o `fechar_rodada` arquiva e apaga, e erro de poda aparece tarde | o `fechar_rodada.py` deixa de arquivar e apagar o `desktop.ini` (com teste); `desktop.ini` no `.gitignore`; confirmar a caixa (AP-007, AP-008, KP-001, KP-002, INDICE); os caminhos; o guia em Word (3 menções, sem gerador: propor como editar); a memória; os testes; push |
| **desosp-app** (`…\desosp-app`), depois do kernel | Opus 5.5 · `/effort high`: mexe na amarração do dado real e nos backups do banco | recriar o `.venv`; amarrar `desosp-app-dados` como "a vizinha com o meu nome + `-dados`" (config, `.bat`, ajuda e os testes `test_raiz_real` e `test_iniciar:202`); `_e_do_kernel` e `_e_dado_real` comparando por partes do caminho; `DESOSP_KERNEL` no lugar novo; tirar os backups de dentro da pasta do banco (propor o destino ao Ettore) e sinalizar isso no app; aposentar o `icones_pastas.py` e a `LEGENDA_CORES_PASTAS.md` (apontar para o manual); os 289 caminhos gravados no banco só se informam, não se reescrevem sem o Ettore; avisar que Grep e Glob não veem os dados (o `.ignore` da mãe); AK ao kernel; o teste da puxada no lugar novo; push |
| **claude-kit · sistema de pastas** (`…\claude-kit`) | Opus 5.5 · `/effort high`: o gancho roda em toda sessão e o aplicador escreve em todas as pastas | os passos 3.2, 4 e 6 deste plano, com ele como especificação; aplicar e ligar o gancho só depois do "pronto" das três janelas |
| **desktop · enviar a cópia** (desktop) | Sonnet 5.5 (escolhido na lista do `/model`) · `/effort medium`: cópia com hashes, erro visível | anotar o que a janela da `uso-do-claude` concluiu (Partes 0-2); copiar o que é do kit lá (3.1), com o manifesto; não mudar nada no desktop |
| **desktop · kit e cores** (desktop), por último | Opus 5.5 · `/effort medium`: aplica um pacote testado, e o erro aparece no Explorer na hora | trazer o `claude-kit` para `C:\CLAUDE-PROJETOS\claude-kit`; tirar as cópias velhas de `~\.claude\skills` e ligar com `--kit-vence` (no modo cópia, se o app Desktop esconder skill por junção); o `CLAUDE.md` pessoal novo; Pillow; `pastas.py instalar` e `ligar-gancho` (testar o comando do gancho lá: Git Bash ou não); o mapa do app financeiro (propor ao Ettore); Material + Peacock; conferência = 0 |
| **GPT** | — | nada além da mudança; commit e remote do `conversation-core` são decisão do Ettore, no Codex |

## Verificação de cada passo
- **1:** a folha de prova vista por mim; cada `.ico` com 8 tamanhos; o Ettore vê o HTML e as amostras no Explorer.
- **2:**
  - `conferir_antes.py` verde e o retrato depois igual ao de antes;
  - as lápides recusam `mkdir`;
  - Grep e Glob da mãe não veem os dados;
  - as junções e o hardlink conferidos, e `test_ligar_claude.py` verde;
  - as 4 skills no menu `/`;
  - a varredura gravada.
- **3:** a comparação com o `kit_antes`.
- **4:**
  - `pytest` verde, e a medida do gancho dentro do limite;
  - `pastas.py conferir` = 0, e `git check-ignore -v desktop.ini` nos repositórios;
  - uma pasta nova numa sessão de teste ganha o verbo; uma na raiz gera a pergunta;
  - as três suítes repetidas com as cores;
  - o Ettore olha o Explorer (ícone, dica, coluna Comentários) e o VS Code.
- **6:** o hardlink com 2 nomes; as skills no menu `/`; nenhuma referência viva a `C:\CLAUDE`.
- **Cada janela de projeto:** a suíte com os mesmos pulados, a rodada de prova e a varredura do seu
  repositório sem caminho velho vivo.

## Decisões que ficaram (para o Ettore, no fim desta janela)
1. **As sobras em `Temp\…\88629c23…\scratchpad\ihdl`**: 154 arquivos, cópia de `arquivo\` com dado real,
   presos pelo "somente leitura" desde 01/10. Apago (`attrib -r` + Lixeira)? Recomendo que sim: é dado real
   fora do lugar.
2. **O clone `OneDrive\Documentos\GitHub\desosp-app`** (30/09, com `CLAUDE.md`, dentro do OneDrive, que o
   Claude Code deve evitar): apagar, ou você o mantém de propósito? Recomendo apagar, depois de conferir que
   não tem commit que falte no GitHub.
3. **O app financeiro do desktop** vai para `C:\CLAUDE-PROJETOS` de lá? O registro não decide isso. A mãe
   tem de existir lá de qualquer jeito, porque o manual e a dica apontam para ela.
4. No mapa: a **mãe com a marca** Projeto com IA, e `docs\premiacoes` da planilha em **Eu forneço fontes**.
