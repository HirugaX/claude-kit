# O pacote de ícones de pasta de 30/09 — como foi feito e o que significa

- **Pergunta:** o que é o pacote de ícones de pasta (verde, azul, laranja) criado em 30/09 — onde estão os
  ícones, como foram aplicados, o que cada cor quer dizer —, que pastas o Claude Code usa no notebook e que
  riscos o `desktop.ini` traz aos projetos.
- **Data:** 04/10/2026
- **Projeto que pediu:** entrevista das cores de pasta (janela aberta em `C:\DESOSP`, no notebook).
- **Fontes:** levantamento local, sem internet — os `.ico` e `desktop.ini` no disco,
  `C:\DESOSP_APP\scripts\icones_pastas.py`, `C:\DESOSP_APP\docs\LEGENDA_CORES_PASTAS.md`,
  `C:\CLAUDE\scripts\ligar_claude.py`, as transcrições das sessões de 30/09 e 03/10 em
  `~\.claude\projects\`, `git status` e o código dos três repositórios.
- **Conclusão:** o pacote foi pedido, aprovado e feito em 30/09 numa janela do app. O gerador é o
  `C:\DESOSP_APP\scripts\icones_pastas.py` (Python puro, 25 caminhos fixos, sem teste); os três ícones ficam
  em `%LOCALAPPDATA%\DESOSP\icones_pastas\`, em 6 tamanhos (sem 20 e 40 px). Sentido: azul = código, onde o
  Claude mexe; verde = para ler; laranja = entrada; amarela = pastas do usuário e raízes. A legenda existe,
  em Markdown, nos documentos do app. Riscos: a planilha apaga os próprios `desktop.ini` a cada fechamento e
  não os ignora no git; o atributo "somente leitura" da pasta impede apagar cópias (WinError 5); pasta de
  rodada não pode ter ícone.
- **Conferir de novo depois de:** qualquer mudança no pacote de ícones ou na estrutura das pastas (é uma
  foto de 04/10/2026).
- **Como foi feita:** subagente Explore (Sonnet), 115 chamadas de ferramenta. O texto abaixo é o relatório
  dele, sem mudança de conteúdo; o complemento no fim é um teste feito depois, na mesma janela.

---

**Síntese.** O pacote já existe e está aplicado. Foi pedido, aprovado e feito em **30/09/2026** (não em
01–04/10) e estendido a `C:\CLAUDE` em 03/10. Gerador: `C:\DESOSP_APP\scripts\icones_pastas.py`. São 25
pastas pintadas; os `.ico` ficam fora dos repositórios. Horários abaixo são locais (as transcrições estão em
UTC; local = UTC-3).

## 1. O pacote

**1a. .ico** (todos em `C:\Users\ettor\AppData\Local\DESOSP\icones_pastas\`, criados 30/09 17:24)

| arquivo | bytes | conteúdo |
|---|---|---|
| codigo.ico | 4204 | 6 imagens PNG 32 bpp (16, 24, 32, 48, 64, 256 px); azul #2F6FD6, `< >` |
| leitura.ico | 3270 | idem; verde #2E9E5B, três linhas de texto |
| deposito.ico | 3264 | idem; laranja #E8892B, seta para baixo |

Não há .ico/.png/.svg de origem em nenhuma das raízes pedidas: o desenho é procedural (o único .svg é o
sprite Lucide do app, sem relação). Em 16 px não há desenho, só cor. Cópias e prévias PNG voláteis em
`C:\Users\ettor\AppData\Local\Temp\claude\c--DESOSP-APP\cdda1cf7-9bbe-4eb8-af5b-212e346de223\scratchpad\`.

**1b. desktop.ini.** Achei 26: 25 do pacote e 1 alheio. Nos 25: UTF-16 LE com BOM; linhas terminam em CR CR
LF (efeito de `write_text` no Windows; o Explorer aceita); arquivo Hidden+System+Archive; pasta **ReadOnly**
(sem System). Conteúdo, mudando só `<cat>` e `<dica>`: `[.ShellClassInfo]` /
`IconResource=C:\Users\ettor\AppData\Local\DESOSP\icones_pastas\<cat>.ico,0` / `InfoTip=<dica>` /
`; DESOSP icones_pastas`.

| cat | InfoTip | pastas |
|---|---|---|
| codigo, azul (12) | Código — onde o Claude mexe | DESOSP: desosp, tests, scripts · DESOSP_APP: app, tests, scripts, workspace_dev · planilha-hc: scripts, tests, trabalho · CLAUDE: skills, scripts |
| leitura, verde (11) | Para ler — o que o sistema e o Claude produzem | DESOSP: docs, saida, arquivo, historico · DESOSP_APP: docs · DESOSP_APP_REAL: saida, arquivo, historico · planilha-hc: docs, saida, historico |
| deposito, laranja (2) | Entrada — onde você deposita os arquivos | DESOSP\entrada, planilha-hc\entrada |

Datas: 30/09 17:24:25–26; os de `C:\CLAUDE\skills` e `scripts`, 03/10 10:20. O alheio é
`C:\DESOSP\docs\gpt\desktop.ini` (25/08, ASCII sem BOM, `[LocalizedFileNames]`). Não há desktop.ini nas
raízes dos projetos, em `fontes`, `.claude`, pastas de rodada nem em outra pasta de 1º nível de `C:\`
(varri até profundidade 3).

**1c. Gerador.** `icones_pastas.py` é Python puro (struct/zlib, sem Pillow); commit 4e47ff4 de 30/09 17:37,
mapa ampliado em c296e54 (03/10). Entradas: só flags (`--ver` mostra, `--remover` desfaz). Todo o resto é
fixo no código: `CATEGORIAS` (cor e dica) e `PASTAS` (25 caminhos absolutos desta máquina). Saídas: desenha
os 3 .ico (não copia de lugar nenhum) e grava o desktop.ini em cada pasta existente (`attrib +h +s` no
arquivo, `+r` na pasta), depois chama `SHChangeNotify`. É idempotente: regera os .ico e só reescreve ini
inexistente ou com a marca `; DESOSP icones_pastas` (a marca também limita o `--remover`); pula pasta com ini
alheio. Não tem teste automatizado. `C:\CLAUDE\scripts\ligar_claude.py` (`colorir()`) repete o formato para
`C:\CLAUDE\skills` e `scripts`, só se o ini não existir e `codigo.ico` já existir.

**1d. Legenda.** `C:\DESOSP_APP\docs\LEGENDA_CORES_PASTAS.md` (cor, desenho, significado, o que o usuário
faz, pasta por pasta, como mudar), indexada em `C:\DESOSP_APP\docs\LEIA-ME.md`. Há resumo em
`C:\CLAUDE\LEIA-ME.md`, a decisão em `HANDOFF_APP.md` linha 56 e as mensagens AK-009 (kernel) e AP-007
(planilha). Não há .docx/.html (`PALETAS_DESOSP.html` é paleta das telas, outro assunto).

**1e. Intenção reconstruída**
- **Pedido:** 30/09 ~10:05, projeto `c--DESOSP-APP`, sessão 15a63646. O usuário pediu cor/ícone diferente
  para as pastas "que o Claude mexe" e para as que ele mexe (padrão do Windows), inclusive dentro das pastas
  (código × ver arquivos/históricos × uploads), com o padrão enviado a kernel e planilha. O assistente propôs
  4 grupos e avisou o limite: o Windows não pinta pasta, só troca o ícone por um desktop.ini oculto, que
  precisa estar no .gitignore. Aprovado às 11:09 ("aprovo").
- **Feito:** 30/09 17:20–17:40, sessão cdda1cf7, mesmo projeto ("retome a paleta e execute"; o usuário também
  questionou por que existe DESOSP_APP_REAL). Em 03/10 10:20 (sessão dc503d77, projeto `C--DESOSP`, ao criar
  `C:\CLAUDE`) o `ligar_claude.py` pintou as duas pastas; a sessão 15241406 (app) as registrou no mapa.
- **Significados:** azul/`< >` = código, onde o Claude mexe (não precisa abrir); verde/linhas = para ler
  (abre e copia; não apaga nem renomeia); laranja/seta = entrada (o usuário deposita); amarela comum = pastas
  do usuário e a raiz de cada projeto (mistas).
- **Decisões e limites:** nunca só cor (desenho + dica); ini só no nível da pasta, nunca em pasta de rodada;
  .ico fora dos repositórios (sobrevivem a renomear). A raiz de DESOSP_APP_REAL ficou sem ícone (o assistente
  ofereceu vermelho com cadeado; não feito). O usuário escolheu juntar as 4 pastas sob
  `C:\DESOSP\{desosp-censo, desosp-app, desosp-hc, dados-app}` numa janela futura, depois do censo de 6ª;
  ainda não feito. Quando ocorrer, o mapa e a legenda precisam ser atualizados.

## 2. Inventário

**2a. `C:\Users\ettor\.claude\projects\`**

| subpasta | cwd real | existe | sessões | mais recente |
|---|---|---|---|---|
| C--DESOSP | c:\DESOSP | sim | 91 (+358 de subagentes) | 04/10 09:41 |
| c--DESOSP-APP | c:\DESOSP_APP | sim | 28 (+10) | 04/10 09:39 |
| c--planilha-hc | c:\planilha-hc | sim | 6 (+9) | 03/10 11:14 |
| C--Users-ettor-AppData-Local-Temp | C:\Users\ettor\AppData\Local\Temp | sim | 1 | 03/10 10:20 |
| ...Temp-claude-c--DESOSP-APP-9c62a77b-...-controle-recursos | scratchpad do app | sim | 2 | 04/10 01:17 |
| ...Temp-claude-c--DESOSP-a5574541-...-scratchpad | scratchpad do kernel | sim | 3 | 03/10 13:24 |

As três últimas parecem provas do `perguntas_controle.py`. Nunca abertos no Claude Code (sem pasta em
projects): `C:\CLAUDE`, `C:\DESOSP_APP_REAL`, `C:\conversation-core`.

**2b. Pastas de `C:\`** (só existe a unidade C:)

| pasta | CLAUDE.md | .claude | .git | o que é |
|---|---|---|---|---|
| CLAUDE | sim | não | não | skills, scripts e CLAUDE.md pessoais do Claude Code |
| DESOSP | sim | sim | sim | kernel: pipeline do censo de desospitalização |
| DESOSP_APP | sim | sim | sim | aplicativo sobre o kernel |
| DESOSP_APP_REAL | não | não | não | raiz de dado REAL do app (cópia do kernel, banco) |
| planilha-hc | sim | sim | sim | planilhas de home care + MASTER |
| conversation-core | sim | não | sim, sem remote | converte exports do WhatsApp em dataset |
| DESOSP ARQUIVO, ConVida, Ettore | não | não | não | arquivos pessoais e administrativos |
| Apps, dell, Drivers, e-logo, ESD, FisioterapiaSoft, inetpub, LDPlayer, Office, OneDriveTemp | não | não | não | terceiros/sistema (várias vazias) |

Remotes: github.com/HirugaX/desosp-censo, desosp-app, desosp-hc.

**2c. Settings**
- `~\.claude\settings.json`: nenhum hook e nenhum `additionalDirectories`. Tem só `permissions.allow`
  (12 regras: git add/commit/rm/mv, `python -m pytest -q`, `python -`, um Read da memória de c--DESOSP, um
  Copy-Item), model `opus[1m]` e effort `xhigh`. `settings.local.json` global não existe.
- `C:\DESOSP\.claude\` **não tem** `settings.json` nem `settings.local.json` (só `rules\` e
  `skills\rodada`). Logo: nenhum hook, nenhum additionalDirectories.
- Outros projetos: DESOSP_APP, SessionStart (sem matcher) → `$CLAUDE_PROJECT_DIR/.claude/hooks/session-start.sh`.
  planilha-hc, SessionStart → `python scripts/caixa_pendente.py`.

**2d. C:\CLAUDE.** Não é git (sem remote). Árvore: `CLAUDE.md` (hardlink com `~\.claude\CLAUDE.md`),
`LEIA-ME.md`, `fontes\claude-efficiency-report.md`, `scripts\` (desktop.ini, ligar_claude.py,
perguntas_controle.py), `skills\` (desktop.ini + 4 skills). `ligar_claude.py`:
1. Traz para `skills\` toda skill que caiu como pasta real em `~\.claude\skills` (a de mesmo nome vai para
   `_substituidas\`) e deixa uma junção `mklink /J`. Cria junção para as skills de `C:\CLAUDE\skills` ainda
   sem link e ignora `synced`.
2. Mantém o `CLAUDE.md` pessoal como hardlink; avisa se os dois diferirem.
3. Pinta as duas pastas de azul.

É idempotente; `--conferir` só informa. Skills: `grill-me`, `grilling`, `recursos-do-projeto`,
`uso-do-claude` (kebab-case; as próprias em português, as de terceiros em inglês). Nos projetos: `rodada`
(DESOSP) e `revisar-tela` (app).

## 3. Riscos

**3a. Git**

| repo | .gitignore cita desktop.ini | situação |
|---|---|---|
| C:\DESOSP | sim (linha 32) | todos ignorados (regra `desktop.ini` ou `entrada/ saida/ arquivo/ historico/`); nenhum rastreado |
| C:\DESOSP_APP | sim (linha 42) | idem |
| C:\planilha-hc | **não** | `docs\`, `scripts\`, `tests\` aparecem como `??`, e um `git add -A` os comita. entrada, saida, trabalho e historico saem por regras de pasta. AP-007 pede o ajuste e consta "enviado — 30/09", sem confirmação |

`core.excludesFile` global **não está definido** (nem `~/.config/git/ignore`, nem no system). O ini carrega
`C:\Users\ettor\...`. DESOSP_APP_REAL e CLAUDE não são git.

**3b. Varreduras em `C:\DESOSP\desosp\` (não há run_*.py na raiz).** Nenhuma lê, move ou acusa um
desktop.ini em `entrada\`, `saida\`, `arquivo\` ou `historico\`:
- Prefixo + extensão: CONFIG_DESOSP.py:76; loaders.py:124-126 e 196-197 (com `_e_lixo`, linhas 86-93, que já
  inclui desktop.ini; teste em tests\test_regressoes.py:9993); run_rodada.py:111-118; run_extracao.py:186,
  392, 838; run_merge.py:259, 308; run_build.py:92; sist_reuso.py:86; run_captacao_janela.py:46.
- Só subpastas de rodada (isdir + regex): CONFIG_DESOSP.py:94, 197; arquivo_rodada.py:109, 130, 223;
  espera.py:73; run_extracao.py:411; run_rodada.py:139; run_reprocessar.py:524.
- Pelo `_e_lixo`, que acusa o ini como lixo: arquivo_rodada.py:277, 303, 339 (regra nas linhas 77-79).
- espera.py:83 faz `glob('entrada\*')`, mas `rodada_do_nome` devolve None e o ini não é estacionado.

Pontos de atenção:
- `run_reprocessar.py:276-279` move todo arquivo de `WORKDIR` sem `_e_lixo`. Hoje `WORKDIR` é
  `saida\<rodada>`. No ramo "layout antigo" (CONFIG_DESOSP.py:304-314) seria `saida\`, e o ini iria para
  `_EXECUCAO_N`. Está inativo, porque não há `saida\_RODADA.json` na raiz.
- Um ini dentro de pasta de rodada impede `_remover_se_vazia` (arquivo_rodada.py:149) e `espera._limpar`. No
  app, entra no hash (`puxar.py:200`) e na datação da rodada (`ponte.py:152`).
- **ReadOnly:** `copytree` propaga o atributo e `rmtree` falha em `os.rmdir`. Aconteceu em 01/10 (sessão
  88629c23, `C:\DESOSP`): WinError 5 ao apagar uma cópia de `arquivo\`. As sobras em
  `...\Temp\claude\c--DESOSP\88629c23-…\scratchpad\ihdl\dados\` seguem ReadOnly. A sessão atribuiu à causa o
  desktop.ini; isso não está nos CLAUDE.md nem nas regras.
- App (`C:\DESOSP_APP\app`): ponte.py:223, 297, 330, 364, 434, 508; puxar.py:302, 314, 335, 539;
  comparador.py:112; envios.py:594, 1064; rotas.py:99. Todos filtram por `is_dir`+`e_sufixo`, prefixo ou
  `RE_MSG`, então não veem o ini.
- planilha-hc: `scripts\fechar_rodada.py:57-71, 105-130` trata todo arquivo de entrada, saida e trabalho
  (exceto LEIAME.txt) como da rodada. Ele arquiva o desktop.ini e depois o apaga, tirando o ícone dessas 3
  pastas a cada fechamento.

**3c.** Sim. `C:\DESOSP\entrada`, `saida`, `arquivo`, `historico` e `docs` (e também `desosp`, `scripts`,
`tests`) já têm desktop.ini do pacote. Em AK-009 o kernel igualou os dois `_e_lixo` (commit 8736b44, 01/10).

## Lacunas
- Não vi o Explorer; não confirmo que os ícones aparecem.
- Não rodei `icones_pastas.py --ver` nem `ligar_claude.py --conferir`.
- Conversas anteriores a 30/09 10:05 sobre o tema não estão nas transcrições locais (podem ter sido no
  claude.ai ou na nuvem).
- Não abri o conteúdo de `C:\Ettore`, `ConVida` e `DESOSP ARQUIVO`, só os nomes de pastas. Não li
  `.credentials.json` nem examinei hooks de plugins.
- A causa da falha de 01/10 (atributo ReadOnly) é inferência: o traceback mostra `os.rmdir` negado e as
  pastas copiadas seguem ReadOnly sem desktop.ini.

## Complemento — teste do atributo da pasta (04/10/2026, mesma janela)
Teste numa pasta temporária, com `shutil.copytree` e `shutil.rmtree` do Python 3.12:
- **Pasta com "somente leitura" (`attrib +r`), o que o pacote de 30/09 usa:** a cópia herda o atributo, e
  nem a cópia nem a original se apagam (`PermissionError: [WinError 5] Acesso negado`) — o mesmo erro de 01/10.
  A inferência da seção 3b fica confirmada.
- **Pasta com "sistema" (`attrib +s`):** a cópia não herda, e as duas se apagam. A Microsoft aceita qualquer
  dos dois atributos para o `desktop.ini` valer.
