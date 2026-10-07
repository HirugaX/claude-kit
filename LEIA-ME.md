# claude-kit — tudo o que é do Claude Code, num lugar só

Criado em 03/10/2026; mora em `C:\CLAUDE-PROJETOS\claude-kit`, ao lado dos projetos. Vale para todos os projetos
dos dois PCs. Repositório privado: `github.com/HirugaX/claude-kit` (ramo `main`); o notebook escreve, o desktop
recebe por `git pull` (e escreve na `caixa\`).

## As skills: onde moram e onde ligam

O kit é um **marketplace local** de plugins. Cada plugin é um grupo de skills; o Claude Code carrega os plugins
direto desta pasta (a edição vale na sessão seguinte, ou com `/reload-plugins`). Quem liga cada grupo, e onde, é o
`config\plugins.json`.

| grupo | de quem | onde mora | onde liga |
|---|---|---|---|
| `nucleo` | nossas | `plugins\nucleo\skills\` | todo projeto (escopo de usuário) |
| `planejamento` | terceiros | `plugins\planejamento\skills\` | todo projeto (escopo de usuário) |
| `engenharia` | terceiros | `plugins\engenharia\skills\` | só nos projetos de código, cada um na sua fase (`<projeto>\.claude\settings.json`); hoje, no kit |
| `kit` (a partir do F2a) | nossas | `plugins\kit\skills\` | no kit e na janela da raiz `C:\CLAUDE-PROJETOS` |

- **O que cada skill faz e quando usar:** o `GUIA_DAS_SKILLS.docx` (abaixo), com a tabela de qual projeto liga qual
  grupo.
- **De onde veio cada skill de terceiros:** o `origem.json` de cada plugin (repositório, caminho, commit, data).
- **O gancho das cores das pastas** é do plugin `nucleo` (`plugins\nucleo\hooks\hooks.json`): roda em todo projeto.

## Instalar ou conferir (os dois PCs)

```
git clone https://github.com/HirugaX/claude-kit C:\CLAUDE-PROJETOS\claude-kit     (só na 1ª vez)
git -C C:\CLAUDE-PROJETOS\claude-kit pull --ff-only                               (nas outras)
python C:\CLAUDE-PROJETOS\claude-kit\scripts\instalar_kit.py
```

O `instalar_kit.py`:
- registra o marketplace do kit e os de fora;
- liga os grupos e plugins de escopo de usuário;
- liga os ganchos do git (`core.hooksPath .githooks`: o pre-commit de privacidade);
- tira as junções antigas de `~\.claude\skills`;
- grava o `~\.claude\CLAUDE.md` com só a linha `@C:/CLAUDE-PROJETOS/claude-kit/CLAUDE.md` (o import);
- no fim, imprime o comando da política do safety-net, que é seu.

`--verificar` só confere: sai com achado se sobrar junção, se um nome se repetir, se um grupo faltar ou estiver no
escopo errado, se o gancho das cores estiver em dobro, se houver `CLAUDE.md` na raiz `C:\CLAUDE-PROJETOS\` (ele
carregaria em todos os projetos) ou se o CLAUDE.md pessoal não for o import. `--trecho codigo` (ou `pesquisa-estudo`,
`pessoal`, `kit`, `raiz`, `teste`) imprime o `enabledPlugins` para o `.claude\settings.json` de um projeto.

**Skill de terceiros nova ou atualizada:** `python scripts\atualizar_terceiros.py --todas` confere;
`... <skill> --aplicar` traz a versão nova para o plugin e atualiza o `origem.json`. Nunca `npx skills add` direto: ele
grava em `~\.claude\skills` e repete o nome.

## O que mora aqui

| pasta ou arquivo | o que é |
|---|---|
| `plugins\` e `.claude-plugin\marketplace.json` | as skills, por grupo (acima) |
| `config\plugins.json` | os marketplaces, os grupos, os plugins de fora e o escopo de cada um |
| `CLAUDE.md` | as suas regras pessoais, importadas pelo `~\.claude\CLAUDE.md` em toda janela de todo projeto |
| `COMO_OPERAR.md` | como você opera, até o F3 |
| `docs\ESTADO.md` | onde o kit está e o que vem a seguir (reescrito a cada fase) |
| `decisoes\` | as entrevistas, os planos e os ADRs (`decisoes\adr\0001-privacidade.md`, `0002-isolamento.md`) |
| `pesquisas\` | a biblioteca: antes de pesquisar, procure no `INDICE.md`; depois, salve lá |
| `metricas\` | a medição semanal (só números) |
| `caixa\` | as mensagens entre os PCs (NB: do notebook; DK: do desktop) |
| `fontes\` | os materiais que viraram skill |
| `scripts\` | `instalar_kit.py`, `atualizar_terceiros.py`, `gerar_guia_skills.py`, `checa_kit.py` (a varredura de privacidade do pre-commit), `medir_semana.py`, `perguntas_controle.py`, `md_para_docx.py`; os testes em `scripts\tests\` |
| `.githooks\` | o pre-commit (`checa_kit.py --staged`) e o pre-push (só o remoto do kit) |
| `_do_desktop\` | o material que veio do desktop (fora do git) |

## O guia em Word

`python scripts\gerar_guia_skills.py` gera o `GUIA_DAS_SKILLS.docx` na raiz do kit (fora do git: cada PC gera o seu).
A 1ª parte é como você opera; depois, cada grupo com o que cada skill faz, quando usar e um exemplo de pedido; e a
tabela de qual projeto liga qual grupo. Toda fase que muda skill, plugin ou o uso por projeto termina regenerando o
guia.

## O que NÃO mora aqui

| o quê | por que fica onde está |
|---|---|
| `~\.claude\settings.json`, o login, o histórico e as memórias de cada projeto | são do próprio Claude Code, que os escreve o tempo todo |
| `~\.claude\skills\synced` | as skills que o claude.ai sincroniza sozinho; não mexer |
| os projetos | moram ao lado, em `C:\CLAUDE-PROJETOS\` |
| dado de paciente | nunca no kit (ADR-0001); o pre-commit barra |

Os caminhos velhos (`C:\DESOSP`, `C:\DESOSP_APP`, `C:\DESOSP_APP_REAL`, `C:\planilha-hc`, `C:\conversation-core`,
`C:\CLAUDE`) viraram **lápides**: um arquivo vazio com o nome da pasta velha, para que o programa que ainda use o
caminho antigo dê erro na hora, em vez de recriar uma pasta vazia.
