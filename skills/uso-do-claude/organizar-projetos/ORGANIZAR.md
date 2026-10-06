# organizar-projetos — reunir os projetos e o kit do Claude numa pasta-mãe, pôr no GitHub, pintar as pastas

Módulo da skill `uso-do-claude`. Nasceu da reorganização do notebook em 04-05/10/2026 (os registros estão em
`claude-kit\decisoes\`: `2026-10-04_pastas-e-reorganizacao.md`, `2026-10-04_plano-aprovado.md`,
`2026-10-04_execucao-reorganizacao.md`, `2026-10-05_icones-escolha.md`, `2026-10-05_organizar-projetos.md`).
Use num PC novo, ou quando os projetos e os arquivos do Claude estiverem espalhados.

| arquivo | o quê |
|---|---|
| `ORGANIZAR.md` | este roteiro: as fases, cada uma com o seu portão, as regras que não se quebram, as lições |
| [reaproveitar.md](reaproveitar.md) | a fase 0: o que o PC já tem, para não duplicar (`scripts\inventario.py`) |
| [perguntas.md](perguntas.md) | a fase 3: a entrevista, no formato do `grill-me`, e o que cada resposta decide |
| [pastas.md](pastas.md) | o sistema de cores: verbos, marcas, a regra, o gancho, a conferência, o VS Code |
| [github.md](github.md) | publicar o que falta (sempre privado, com varredura antes) e re-registrar no GitHub Desktop |
| [prompts.md](prompts.md) | os modelos dos prompts das janelas de cada projeto |
| `mapa.json` | a tabela única das cores: verbos, marcas e o mapa de cada projeto (dos dois PCs) |
| `planos\` | o plano da mudança em JSON (`notebook_2026-10-05.json` é o real, executado) |
| `scripts\` | `inventario.py`, `mudanca.py`, `varredura.py`, `antes_do_github.py`, `pastas.py`, `desenho.py`, `gancho.py`, `regras.py`; testes em `scripts\tests` (`python -m pytest` nesta pasta) |
| `icones\` | os quadros PNG de cada ícone (a fonte do desenho); o `.ico` se monta em cada PC |

## As regras que não se quebram

1. **Mostrar antes, esperar o "sim"** (CLAUDE.md pessoal). Cada fase abaixo termina num portão: o que foi visto,
   com a fonte, e o que vai mudar. Um plano aprovado é o "sim" dos passos dele; o *como* continua com o Claude.
2. **Aproveitar só o necessário.** Antes de instalar qualquer coisa, a fase 0 diz o que já existe. Nada se instala
   em dobro: skill, gancho, linha de CLAUDE.md, pasta de ícones, script.
3. **Mover, nunca reclonar.** Muita coisa só existe no disco (entrada, saída, histórico, nomes locais, caixas).
4. **Nunca seguir junção nem link** (o `os.walk` do Python 3.12 entra em junção; junção com caminho absoluto conta
   em dobro no retrato e quebra na mudança). Todo script daqui pula ponto de nova análise, com teste.
5. **Nunca `CLAUDE.md` na raiz da mãe**: todo projeto o carregaria (o Claude Code lê o `CLAUDE.md` das pastas acima).
6. **O `CLAUDE.md` pessoal é um hardlink**: nunca editar pela ferramenta Edit (ela grava um arquivo novo e separa o
   hardlink). Grave no próprio arquivo e confira com `fsutil hardlink list`.
7. **Dado sensível segue o ADR-0001** (`claude-kit\decisoes\adr\0001-privacidade.md`): nunca no repositório de
   código, em prompt nem em resumo. Nome de paciente, de funcionário ou de operadora nunca entra em arquivo do kit.
8. **O comando que o modo automático bloqueia é do usuário**: mover pasta de projeto e apagar na raiz do `C:`. Entregue
   o comando pronto, com a conferência embutida, e espere o "rodei".
9. **O velho só sai no fim**, conferido (a fase 9).

## As fases

Uma janela aberta na **mãe** (ou numa pasta que não muda), nunca dentro de uma pasta que vai mudar. Modelo e
esforço: Opus 5.5 · `/effort high` para as fases 2 a 6 (o erro é silencioso: pasta no lugar errado, dado enviado);
a fase 8 aplica um pacote testado e pode ir em `/effort medium`.

| fase | o que se faz | portão (o que se mostra antes de seguir) |
|---|---|---|
| **0. Reaproveitar** | `python scripts\inventario.py` (só lê) — [reaproveitar.md](reaproveitar.md) | a lista SERVE / DUPLICARIA / FALTA / ATENÇÃO; o que entra e o que fica de fora |
| **1. Preparar o PC** | trazer o kit (cópia com manifesto sha256, conferida); comparar as skills e o CLAUDE.md de lá com os do kit e juntar; ligar: `python <kit>\scripts\ligar_claude.py --conferir`, depois sem `--conferir` (com `--kit-vence` se houver cópia velha) | a comparação arquivo a arquivo; as linhas do CLAUDE.md que só existem no PC (juntar com o "sim"); depois, `fsutil hardlink list` e o menu `/` com as skills |
| **2. Inventário dos projetos** | subagente (Explore com `model: sonnet`), só leitura: projetos, repositórios (e se a raiz do disco virou repositório: `git -C C:\ status`), arquivos de IA soltos, memórias (`~\.claude\projects\<chave>\memory`), ganchos, OneDrive, junções, permissões de sandbox (Codex), o que está e o que não está no GitHub, processos que seguram pastas | o quadro por projeto, sem conteúdo de dado |
| **3. Entrevista** | [perguntas.md](perguntas.md), no formato do `grill-me` | as respostas registradas em `claude-kit\decisoes\AAAA-MM-DD_<assunto>.md` e o "sim" |
| **4. Plano** | o plano em JSON (`planos\<pc>_<data>.json`, modelo: `notebook_2026-10-05.json`); o mapa das cores de cada projeto no `mapa.json`; a varredura de caminhos (`python scripts\varredura.py <plano> <saída>`); a ordem das janelas e os prompts ([prompts.md](prompts.md)) | o plano inteiro de uma vez: movimentos, lápides, memória, mapa, ordem |
| **5. Mudança** | ver abaixo | o retrato depois igual ao de antes; as lápides recusam `mkdir`; a memória copiada com hash igual |
| **6. GitHub** | [github.md](github.md): `antes_do_github.py` em cada repositório novo; publicar privado; re-registrar no GitHub Desktop | a conferência sem problema; o comando do envio |
| **7. Janelas de cada projeto** | cada projeto corrige os próprios caminhos, na janela dele (prompt nomeado); a raiz derivada da posição do código | cada janela diz "pronto", com a suíte igual à de antes e a varredura do repositório sem caminho velho vivo |
| **8. Cores** | [pastas.md](pastas.md): `pastas.py instalar`, `aplicar --ver` → `aplicar`, `legenda`, `vscode`, `ligar-gancho`, `conferir` | a prévia dos ícones aprovada; o resumo por projeto antes de aplicar; `conferir` = 0; o usuário olha o Explorador e o VS Code |
| **9. Limpeza** | o velho sai: pasta antiga do kit (`os.unlink` do `CLAUDE.md` de lá ANTES, senão o hardlink vai junto), pacote de ícones velho, retratos, protótipos; as lápides saem quando a varredura de cada projeto der zero | a lista do que sai, com a prova de que nada depende dele; sempre para a Lixeira |

### A fase 5 — a mudança

Antes, as condições (o script confere as que dá): as janelas do Claude e do VS Code abertas dentro das pastas,
fechadas; o app desligado **pelo próprio app**; PDFs fechados; nenhum processo com caminho velho; cada repositório
commitado e enviado (`git log origin/main..` vazio).

```
python scripts\mudanca.py retrato <plano> antes.json         (retratos fora do kit: listam nomes de arquivo)
python scripts\mudanca.py tudo <plano>                        <- o USUÁRIO roda (PowerShell de administrador se
                                                                 houver lápide na raiz do disco)
python scripts\mudanca.py memoria <plano>
python scripts\mudanca.py retrato <plano> depois.json --novo
python scripts\mudanca.py comparar antes.json depois.json
```

O caminho de volta: `mudanca.py voltar <plano>` tira as lápides e renomeia tudo para os lugares velhos; a memória
velha continua nas chaves velhas (a das novas é cópia).

Depois: o usuário abre cada pasta nova no VS Code (aceita a confiança) e re-registra no GitHub Desktop
("Locate"). O `~\.claude.json` não se edita: cada projeto pede a confiança uma vez.

## As lições de 04-05/10

| o que aconteceu | o que fazer |
|---|---|
| O modo automático não deixou o Claude mover as pastas dos projetos ("destruição local irreversível") nem apagar na raiz do `C:` | entregar o comando ao usuário, com a conferência embutida (`mudanca.py tudo`) |
| `C:\DESOSP` deu "Acesso negado" 5 vezes sem nada visível segurando; uma hora e meia depois, moveu | `os.rename` é atômico: falha sem mexer; o script tenta 5 vezes, para limpo, e na 2ª rodada pula o que já mudou. Pista não confirmada: permissões do sandbox do Codex (`CodexSandboxUsers`) nas pastas em que ele trabalhou |
| Usuário comum só cria **pasta** na raiz do `C:`, não arquivo | a lápide na raiz precisa de administrador |
| A ferramenta Edit separou o hardlink do `CLAUDE.md` | gravar no próprio arquivo; conferir com `fsutil hardlink list` |
| O `.ignore` barrou o Grep, mas **não o Glob** (o Glob achou um arquivo da pasta de dados) | a proteção de verdade é a regra `deny` do settings (Read e Edit em `//c/<mãe>/<dados>/**`), testada com Glob e Read |
| Duas junções de teste (`node_modules`) com caminho absoluto contaram 4.374 arquivos a mais no retrato e passaram a apontar para a lápide | retrato e scripts não seguem junção e a registram à parte; a janela do projeto decide re-apontar ou apagar só a junção (`cmd /c rmdir`, nunca `rmtree`) |
| A chave da memória é o caminho com todo caractere não alfanumérico trocado por `-` (`C:\DESOSP_APP` → `C--DESOSP-APP`), e o NTFS não distingue maiúscula | `mudanca.py memoria` acha a chave sem diferenciar maiúscula e **copia** |
| O Claude Code lista as sessões antigas pela pasta: depois da mudança, as janelas velhas não abrem mais pela pasta nova | avisar o usuário; as sessões continuam na chave velha |
| `desktop.ini` com "somente leitura" na pasta deixou cópia impossível de apagar (WinError 5) | a pasta leva `+s`, nunca `+r` |
| A planilha arquivava e apagava o `desktop.ini` a cada fechamento | cada projeto confere, na janela dele, o que os scripts fazem com arquivo de sistema (ver [pastas.md](pastas.md), "Pastas passageiras") |
| O pacote de ícones do Ettore veio baixado do ChatGPT: todo arquivo com a marca da web (`Zone.Identifier`, ZoneId=3) | o `.ico` se monta em cada PC a partir dos quadros PNG; nada pronto viaja; kit extraído de zip baixado: `Unblock-File` no kit inteiro |
| A prévia nova ficou na mesma pasta que a de 04/10, e o Ettore abriu a antiga ("cadê os meus ícones?") | mandar a prévia por um endereço só (uma página privada) e tirar a antiga na limpeza |
| O gancho foi testado numa sessão nova antes de valer para todas: `claude -p "<pedido>" --settings <arquivo só com o gancho>` (só aquela sessão o vê), com uma pasta nova na raiz de um projeto | ligar no settings de usuário só depois de o `additionalContext` chegar |
| O Claude Code regravou o `settings.json` durante a janela (a ordem das chaves, o apelido do modelo) | ler de novo antes de mexer; o `ligar-gancho` guarda uma cópia (`settings.json.antes-gancho-*`) |
| A guarda do app fotografa as pastas de dado durante a suíte: `desktop.ini` criado no meio dela a faz falhar | pintar com as suítes paradas; com uma suíte rodando, ficar com o diretório fora dos projetos (o gancho varre o projeto do `cwd`) |
