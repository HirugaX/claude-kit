---
name: organizar-projetos
description: Reunir os projetos e o kit numa pasta-mãe, pôr no GitHub o que falta (privado), reaproveitar o que o PC já tem e criar projeto novo. Só por /organizar-projetos.
disable-model-invocation: true
---

# organizar-projetos — pasta-mãe, GitHub, reaproveitar, projeto novo

Nasceu da reorganização do notebook em 04-05/10/2026 (registros em `C:\CLAUDE-PROJETOS\claude-kit\decisoes\`:
`2026-10-04_pastas-e-reorganizacao.md`, `2026-10-04_plano-aprovado.md`, `2026-10-04_execucao-reorganizacao.md`,
`2026-10-05_organizar-projetos.md`). Use num PC novo, quando os projetos e os arquivos do Claude estiverem espalhados, ou
para criar um projeto novo. As cores das pastas: `/cores-das-pastas`; os ícones: `/icones`.

Os scripts moram no plugin `nucleo`, junto com o gancho das cores, porque ele roda em todo projeto:
`C:\CLAUDE-PROJETOS\claude-kit\plugins\nucleo\pastas\` (chamado aqui de **módulo**): `scripts\inventario.py`,
`mudanca.py`, `varredura.py`, `antes_do_github.py`, `pastas.py`, `desenho.py`, `gancho.py`, `regras.py`; o
`mapa.json`; os planos em `planos\`; testes em `scripts\tests` (`python -m pytest` na pasta do módulo).

| arquivo desta skill | o quê |
|---|---|
| [reaproveitar.md](reaproveitar.md) | a fase 0: o que o PC já tem, para não duplicar (`inventario.py`) |
| [perguntas.md](perguntas.md) | a fase 3: a entrevista, no formato do `grilling`, e o que cada resposta decide |
| [github.md](github.md) | publicar o que falta (sempre privado, com varredura antes) e re-registrar no GitHub Desktop |
| [prompts.md](prompts.md) | os modelos dos prompts das janelas de cada projeto |

## As regras que não se quebram

1. **Mostrar antes, esperar o "sim"** (CLAUDE.md pessoal). Cada fase termina num portão: o que foi visto, com a fonte, e
   o que vai mudar. Um plano aprovado é o "sim" dos passos dele; o *como* continua com o Claude.
2. **Aproveitar só o necessário.** A fase 0 diz o que já existe. Nada se instala em dobro: skill, gancho, linha de
   CLAUDE.md, pasta de ícones, script.
3. **Mover, nunca reclonar.** Muita coisa só existe no disco (entrada, saída, histórico, nomes locais, caixas).
4. **Nunca seguir junção nem link** (o `os.walk` do Python 3.12 entra em junção; junção com caminho absoluto conta em
   dobro no retrato e quebra na mudança). Todo script do módulo pula ponto de nova análise, com teste.
5. **Nunca `CLAUDE.md` na raiz da mãe**: todo projeto o carregaria (o Claude Code lê o `CLAUDE.md` das pastas acima).
6. **O `CLAUDE.md` pessoal é um import**: o `~\.claude\CLAUDE.md` tem só a linha
   `@C:/CLAUDE-PROJETOS/claude-kit/CLAUDE.md`. Edita-se o do kit; o `instalar_kit.py` confere e conserta.
7. **Dado sensível segue o ADR-0001** (`claude-kit\decisoes\adr\0001-privacidade.md`): nunca no repositório de código,
   em prompt nem em resumo. Nome de paciente, de funcionário ou de operadora nunca entra em arquivo do kit.
8. **O comando que o modo automático bloqueia é do usuário**: mover pasta de projeto e apagar na raiz do `C:`. Entregue
   o comando pronto, com a conferência embutida, e espere o "rodei".
9. **O velho só sai no fim**, conferido (a fase 9).

## As fases

Uma janela aberta na **mãe** (a janela da raiz, `C:\CLAUDE-PROJETOS`, que liga este plugin) ou no kit, nunca dentro de
uma pasta que vai mudar. Modelo e esforço: Opus 5.5 · `/effort high` nas fases 2 a 6 (o erro é silencioso: pasta no
lugar errado, dado enviado); a fase 8 aplica um pacote testado e pode ir em `/effort medium`.

| fase | o que se faz | portão (o que se mostra antes de seguir) |
|---|---|---|
| **0. Reaproveitar** | `python <módulo>\scripts\inventario.py` (só lê) — [reaproveitar.md](reaproveitar.md) | a lista SERVE / DUPLICARIA / FALTA / ATENÇÃO; o que entra e o que fica de fora |
| **1. Preparar o PC** | `git clone` do kit (privado, `HirugaX/claude-kit`) em `<mãe>\claude-kit`; `python <kit>\scripts\instalar_kit.py` (marketplace, grupos, import do CLAUDE.md pessoal, `local.json` das cores) e `--verificar` | as linhas do CLAUDE.md pessoal que só existem no PC (levar ao do kit com o "sim", depois `--claude-md-kit-vence`); `--verificar` com 0 achados; o menu `/` com as skills |
| **2. Inventário dos projetos** | subagente (Explore com `model: sonnet`), só leitura: projetos, repositórios (e se a raiz do disco virou repositório: `git -C C:\ status`), arquivos de IA soltos, memórias (`~\.claude\projects\<chave>\memory`), ganchos, OneDrive, junções, permissões de sandbox (Codex), o que está e o que não está no GitHub, processos que seguram pastas | o quadro por projeto, sem conteúdo de dado |
| **3. Entrevista** | [perguntas.md](perguntas.md), no formato do `grilling` | as respostas em `claude-kit\decisoes\AAAA-MM-DD_<assunto>.md` e o "sim" |
| **4. Plano** | o plano em JSON (`<módulo>\planos\<pc>_<data>.json`; modelo: `notebook_2026-10-05.json`); o mapa das cores de cada projeto no `mapa.json`; a varredura de caminhos (`python <módulo>\scripts\varredura.py <plano> <saída>`); a ordem das janelas e os prompts ([prompts.md](prompts.md)) | o plano inteiro de uma vez: movimentos, lápides, memória, mapa, ordem |
| **5. Mudança** | ver abaixo | o retrato depois igual ao de antes; as lápides recusam `mkdir`; a memória copiada com hash igual |
| **6. GitHub** | [github.md](github.md): `antes_do_github.py` em cada repositório novo; publicar privado; re-registrar no GitHub Desktop | a conferência sem problema; o comando do envio |
| **7. Janelas de cada projeto** | cada projeto corrige os próprios caminhos, na janela dele (prompt nomeado); a raiz derivada da posição do código | cada janela diz "pronto", com a suíte igual à de antes e a varredura do repositório sem caminho velho vivo |
| **8. Cores** | `/cores-das-pastas` | a prévia dos ícones aprovada; o resumo por projeto antes de aplicar; `pastas.py conferir` = 0; o usuário olha o Explorador e o VS Code |
| **9. Limpeza** | o velho sai: pasta antiga do kit, pacote de ícones velho, retratos, protótipos; as lápides saem quando a varredura de cada projeto der zero | a lista do que sai, com a prova de que nada depende dele; sempre para a Lixeira |

### A fase 5 — a mudança

Antes, as condições (o script confere as que dá): as janelas do Claude e do VS Code abertas dentro das pastas,
fechadas; o app desligado **pelo próprio app**; PDFs fechados; nenhum processo com caminho velho; cada repositório
commitado e enviado (`git log origin/main..` vazio).

```
python <módulo>\scripts\mudanca.py retrato <plano> antes.json      (retratos fora do kit: listam nomes de arquivo)
python <módulo>\scripts\mudanca.py tudo <plano>                     <- o USUÁRIO roda (PowerShell de administrador
                                                                       se houver lápide na raiz do disco)
python <módulo>\scripts\mudanca.py memoria <plano>
python <módulo>\scripts\mudanca.py retrato <plano> depois.json --novo
python <módulo>\scripts\mudanca.py comparar antes.json depois.json
```

O caminho de volta: `mudanca.py voltar <plano>` tira as lápides e renomeia tudo para os lugares velhos; a memória
velha continua nas chaves velhas (a das novas é cópia).

Depois: o usuário abre cada pasta nova no VS Code (aceita a confiança) e re-registra no GitHub Desktop ("Locate"). O
`~\.claude.json` não se edita: cada projeto pede a confiança uma vez.

## Projeto novo

A pasta nasce **na janela da raiz** (`C:\CLAUDE-PROJETOS`), nunca dentro de outro projeto: uma janela = um projeto
(ADR-0002).

1. O nome, com o prefixo do domínio (`desosp-`, `pesquisa-`, `estudo-`, `pessoal-`; ADR-0002) e, se houver dado,
   a pasta irmã `<projeto>-dados\`, fora do git, com `deny` no settings e na política do safety-net (ADR-0001 D6).
2. `mkdir`, `git init`; o `.claude\settings.json` versionado com o `enabledPlugins` do tipo
   (`python <kit>\scripts\instalar_kit.py --trecho codigo|pesquisa-estudo|pessoal`) e os conectores da ADR-0001 D4.
3. As cores: o gancho pinta a raiz como provisória e pergunta; as linhas do projeto no `mapa.json` (`/cores-das-pastas`,
   "Projeto novo").
4. O resto é da janela do próprio projeto: `/grill-me` → skill `recursos-do-projeto` → plano; o GitHub privado pela
   [github.md](github.md).

## As lições de 04-05/10

| o que aconteceu | o que fazer |
|---|---|
| O modo automático não deixou o Claude mover as pastas dos projetos ("destruição local irreversível") nem apagar na raiz do `C:` | entregar o comando ao usuário, com a conferência embutida (`mudanca.py tudo`) |
| `C:\DESOSP` deu "Acesso negado" 5 vezes sem nada visível segurando; uma hora e meia depois, moveu | `os.rename` é atômico: falha sem mexer; o script tenta 5 vezes, para limpo, e na 2ª rodada pula o que já mudou. Pista não confirmada: permissões do sandbox do Codex (`CodexSandboxUsers`). Visto também em 07/10: a pasta com o diretório de trabalho de um shell dentro não se move |
| Usuário comum só cria **pasta** na raiz do `C:`, não arquivo | a lápide na raiz precisa de administrador |
| O `.ignore` barrou o Grep, mas **não o Glob** (o Glob achou um arquivo da pasta de dados) | a proteção de verdade é a regra `deny` do settings (Read e Edit em `//c/<mãe>/<dados>/**`), testada com Glob e Read |
| Duas junções de teste (`node_modules`) com caminho absoluto contaram 4.374 arquivos a mais no retrato e passaram a apontar para a lápide | retrato e scripts não seguem junção e a registram à parte; a janela do projeto decide re-apontar ou apagar só a junção (`cmd /c rmdir`, nunca `rmtree`) |
| A chave da memória é o caminho com todo caractere não alfanumérico trocado por `-` (`C:\DESOSP_APP` → `C--DESOSP-APP`), e o NTFS não distingue maiúscula | `mudanca.py memoria` acha a chave sem diferenciar maiúscula e **copia** |
| O Claude Code lista as sessões antigas pela pasta: depois da mudança, as janelas velhas não abrem mais pela pasta nova | avisar o usuário; as sessões continuam na chave velha |
| `desktop.ini` com "somente leitura" na pasta deixou cópia impossível de apagar (WinError 5) | a pasta leva `+s`, nunca `+r` |
| O pacote de ícones do Ettore veio baixado do ChatGPT: todo arquivo com a marca da web (`Zone.Identifier`, ZoneId=3) | o `.ico` se monta em cada PC a partir dos quadros PNG; nada pronto viaja; kit extraído de zip baixado: `Unblock-File` no kit inteiro |
| O Claude Code regravou o `settings.json` durante a janela (a ordem das chaves, o apelido do modelo) | ler de novo antes de mexer; guardar cópia antes (o `instalar_kit.py` e o `pastas.py` guardam) |
