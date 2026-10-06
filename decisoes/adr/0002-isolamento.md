---
status: accepted
data: 2026-10-06
decidido_por: Ettore (Q16 da rodada 3, plano aprovado em 06/10; conectores ajustados pela Q4 do ADR-0001)
---

# Isolamento: um domínio por prefixo, e a informação só cruza pelos canais

Os projetos agora são de domínios diferentes: trabalho hospitalar com dado de paciente, pesquisa clínica, estudo e
vida pessoal (e, no desktop, financeiro, RH e acolhimento). O Ettore pediu "uma operação e divisão muito clara para
que os projetos não comecem a se misturar". Em 06/10 se viu o vazamento real: uma janela aberta na pasta-mãe leu um
arquivo do censo, e a skill daquele projeto entrou na lista dela. Decidiu-se:
- cada projeto pertence a um domínio, marcado pelo prefixo da pasta;
- o dado mora numa pasta irmã fechada;
- uma janela trabalha num projeto só;
- informação passa de um projeto a outro só pelos canais.

## Domínios e prefixos

| prefixo | o que é | dado de paciente |
|---|---|---|
| `desosp-` | trabalho da desospitalização: `desosp-app`, `desosp-censo`, `desosp-hc`, `desosp-comunicacao` | sim, pelo [ADR-0001](0001-privacidade.md) (pseudônimo) |
| `pesquisa-` | literatura clínica: `pesquisa-clinica` | nunca; só a pergunta |
| `estudo-` | residência: `estudo-residencia` | nunca; caso desidentificado |
| `pessoal-` | `pessoal-organizacao`, `pessoal-produtividade` | nunca; nada do trabalho |
| (sem prefixo) | `claude-kit`: skills, scripts, decisões, pesquisas | nunca |

Os projetos do desktop (DASH, Folha/RH, Acolhimento) ganham prefixo no F8.

## As cinco camadas

| camada | o que mora ali | regra |
|---|---|---|
| 1. global (todo projeto) | `~\.claude\CLAUDE.md`, as skills que servem a qualquer projeto, safety-net, o gancho de abertura | Nada de domínio. Antes de pôr algo aqui, perguntar: "serve a todos os projetos?" |
| 2. projeto | o `CLAUDE.md` do projeto, `.claude\rules`, `.claude\skills` do domínio, `enabledPlugins` do projeto | Skill e plugin de domínio moram no projeto, nunca em `~\.claude\skills` (F1b: plugins por grupo). |
| 3. dados | `<projeto>-dados\`, pasta irmã fora do repositório de código, com `deny` (Read, Edit), `deny_paths` do safety-net e linha no `C:\CLAUDE-PROJETOS\.ignore` | A sessão de um projeto não lê o dado de outro. Pode ter repositório privado próprio (ADR-0001 D2). Censo e HC só mudam o dado de lugar na fase deles (F6, F7); até lá, valem os `deny` internos da D6 do ADR-0001. |
| 4. canais | as caixas `docs\para_*` entre os `desosp-`; a `caixa\` do kit entre os PCs; a biblioteca `claude-kit\pesquisas\` | A informação cruza só por eles, como arquivo com índice. |
| 5. janelas | uma janela = um projeto | A pasta-mãe e o kit não fazem trabalho de projeto. A janela que orquestra guarda só estado e resumo, nunca dado, e delega a sessões abertas na pasta de cada projeto. |

## O que cruza, e como

- **Pesquisa:** recebe do trabalho a **pergunta clínica**, nunca o paciente (nem o pseudônimo).
- **Pessoal:** não recebe nada do trabalho. O trabalho não recebe nada do pessoal.
- **Comunicação:** lê o app só pela **porta de leitura** (`desosp-app\app\ia\`, F5c), que devolve o pseudônimo e os
  campos mínimos.
- **Estudo:** recebe caso desidentificado, escrito pelo Ettore ou tirado de uma pergunta da pesquisa.
- **Pseudônimo:** não sai dos `desosp-`.
- **Leituras declaradas** (um projeto lê arquivo de outro de propósito): ficam escritas no `CLAUDE.md` de quem lê, com
  o caminho e "só leitura". Ex.: o app lê a lei do kernel; o app e o kernel leem o HC no GitHub
  (`HirugaX/desosp-hc`); o `claude-kit\scripts\checa_kit.py` usa as funções e o dicionário de hashes do
  `desosp-hc\scripts\checa_privacidade.py` (só hashes, nunca nomes) para achar nome de paciente antes do commit do
  kit.
- **Leitura não declarada:** não se faz, porque tocar em arquivo de outro projeto puxa as skills dele para a sessão.

## Os canais

- **Caixas entre `desosp-`** (`docs\para_o_app\`, `docs\para_o_kernel\`, `docs\para_a_planilha\`). Formato em uso desde
  28/09:
  - uma série por remetente (AP, KP, PA, PK…);
  - um arquivo por envio, `XX-NNN_AAAA-MM-DD_assunto.md`, gerado uma vez e nunca reescrito;
  - um índice por série;
  - status `gerado → enviado → confirmado — DD/MM → alinhado`;
  - o pre-commit de privacidade roda sobre a caixa.

  Desenho: `desosp-app\docs\PROJETO_FLUXOS_DESOSP.md` §2.
- **`claude-kit\caixa\`:** mensagens entre o notebook e o desktop, pelo git do kit (`caixa\LEIA-ME.md`).
- **`claude-kit\pesquisas\`:** só conhecimento (fontes, verificações), com o `INDICE.md`. Nunca dado de paciente nem
  trecho de documento da operadora.

## Conectores do claude.ai

Ligados no claude.ai, eles valem em todo projeto do Claude Code. Por isso cada projeto declara o seu (ADR-0001 D4):
- `desosp-`: todos negados pelo nome, menos o Google Drive;
- `pesquisa-` e `estudo-`: `disableClaudeAiConnectors: true`, mais o que estiver no `.mcp.json` do projeto;
- `pessoal-`: ligados, com cautela.

A chave vai no `.claude\settings.json` versionado de cada projeto. O projeto pode desligar, mas não religar o que o
nível de usuário desligou.

## Aplicado em 06/10 (F1a)

- `C:\CLAUDE-PROJETOS\.ignore`: `desosp-app-dados/` e `desosp-app-backups/` (a busca do Claude não entra nelas a
  partir da pasta-mãe).
- Ponteiro deste ADR no `~\.claude\CLAUDE.md`.

## Tarefas por fase

| fase | o quê |
|---|---|
| F1b | Plugins por grupo e `enabledPlugins` por tipo de projeto (camada 2). |
| F2 | O gancho de abertura avisa: janela aberta na pasta-mãe, conector do claude.ai fora da lista do projeto, `git pull` do kit divergente. |
| F5a, F6, F7 | `.claude\settings.json` de cada `desosp-` com o `deny` interno e os conectores (ADR-0001); as leituras declaradas escritas no `CLAUDE.md`. |
| F6, F7 | Decidir se o dado do censo e do HC muda para `<projeto>-dados\`. |
| F8 | Prefixos e pastas de dado dos projetos do desktop. |
| N1-N5 | Cada projeto novo nasce com prefixo, `<projeto>-dados\` (se tiver dado), settings e `CLAUDE.md` por este ADR. |
