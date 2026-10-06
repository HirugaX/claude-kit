# PROMPT — arquitetura mestre e auditoria dos dois computadores

Atue como arquiteto do meu Claude Workbench. Meu objetivo é ter um ambiente Claude Code modular, reproduzível em dois computadores, autônomo dentro de limites claros e econômico em contexto/tokens. “Skills” no meu vocabulário abrange plugins, skills, subagents, hooks, MCPs e workflows.

Leia primeiro `00_INICIO.md`, `02_STACK_CANDIDATO.md` e `04_HANDOFF_PROTOCOL.md`, disponíveis junto deste prompt. Use a versão editada do meu pedido como referência: **na primeira fase, não instale nada nem altere configurações/repositórios; audite e proponha a arquitetura.** Você pode produzir os relatórios e manifests de proposta solicitados. Aplicação de mudanças depende da minha aprovação do plano.

## 1. Determine o acesso real

- Identifique seu ambiente atual: SO, shell, diretório de trabalho e ferramentas acessíveis.
- Separe esse ambiente dos computadores A/B. Não trate o container do Work como meu computador pessoal.
- Descubra quais repositórios estão realmente disponíveis, pelo código. Não assuma que está no financeiro.
- Se houver acesso local, faça auditoria somente leitura. Se não houver, prepare um coletor de inventário sanitizado para eu executar uma vez em cada computador. Produzir o coletor não equivale a executá-lo ou instalar componentes.
- Solicite em uma única mensagem os acessos/paths ainda indispensáveis. Continue a arquitetura conceitual enquanto isso.

## 2. Use as entradas certas

Leia o relatório “Claude Code em 2026: Skills, Plugins, Subagents, Hooks, MCPs e os cinquenta projetos mais relevantes no GitHub”, de 05/10/2026. Se estiver inacessível, declare isso; não reconstrua o Top 50 da memória. O arquivo `02_STACK_CANDIDATO.md` já fornece os candidatos mais úteis para avaliar.

Valide componentes em documentação oficial e repositórios originais. Registre URL, data consultada e commit/release quando relevante. Distingua recomendação do relatório, comportamento observado e proposta sua. Popularidade não comprova utilidade nem economia de tokens.

## 3. Audite A e B

Verifique versão real de Claude Code, método de instalação/atualização, provedor/autenticação por categoria, SO/shell e Windows nativo/WSL. Verifique Git, GitHub CLI, Node/npm/npx, Python, ferramentas de teste/browser e as dependências exigidas pelo stack selecionado.

Inspecione os locais efetivos da versão instalada, inclusive:

- `~/.claude/CLAUDE.md`, `~/.claude/rules/`, `~/.claude/settings.json` e overrides relacionados;
- skills pessoais, sincronizadas e distribuídas por plugins;
- plugins instalados/ativados e marketplaces;
- agents, hooks, MCPs e configurações/permissões que os habilitam;
- configuração de projeto `.claude/`, `CLAUDE.md`, `.mcp.json` e arquivos relacionados;
- instruções de organização/managed settings, se presentes e acessíveis;
- memória automática e arquivos importados por instruções, quando afetarem o contexto.

Não execute scripts de terceiros, hooks ou MCPs apenas para descobrir o que fazem. Leia configuração/código primeiro. Não imprima valores de secrets. Relate somente nomes de variáveis, existência de credenciais e necessidade de autenticação local.

Leia frontmatter e conteúdo necessário dos `SKILL.md`. Identifique dependências reais, skills que delegam para outras e comandos com namespace de plugin. Se Matt Pocock estiver instalado, examine especificamente a relação `grill-me`/`grilling` e as outras composições; não deduza a política de invocação pelo nome.

## 4. Inventário classificado

Produza tabela ou CSV de metadados com, para cada componente:

`nome | origem/repo/versão | tipo | escopo atual | classe de carregamento | model/user/both invoked | comando explícito? | gatilho | impacto de contexto | efeitos colaterais | dependências | risco | projetos úteis | manter/mover/modificar/remover/manual`.

Use classes distintas:

- A: instruções always-on realmente carregadas;
- B: skills descobertas globalmente e carregadas sob demanda;
- C: workflows deliberadamente manuais;
- D: subagents/contextos separados;
- E: hooks acionados por evento;
- F: MCPs que oferecem ferramentas externas.

Plugin é unidade de distribuição: desagregue seus componentes. Skill instalada globalmente não significa corpo permanentemente carregado; descrições e metadados também podem consumir contexto. Verifique quais conteúdos ficam retidos após invocação. Não rotule custo como medido se for apenas estimativa.

## 5. Selecione o stack canônico

Quero instalar nos dois computadores **todos os componentes aprovados como relevantes**, com disponibilidade/ativação apropriada ao projeto. Transforme candidatos em decisões: selecionar, condicionar, adiar, substituir, referência. Explique o que resolve e por que não duplica outro componente.

Use dois eixos separados:

1. Localização: global, projeto ou referência.
2. Invocação: modelo, usuário ou ambos.

Não misture esses eixos em uma única categoria. Adicione estado: proposto, aprovado, instalado, habilitado, testado, bloqueado. Um catálogo existente no disco não deve ser anunciado ao Claude como utilizável se não estiver registrado/habilitado.

Prefira composição enxuta: um método de requisitos/specs, um método de estado persistente e um caminho de browser. Harnesses amplos concorrentes precisam de comparação isolada antes de entrar no núcleo. Não instale bibliotecas inteiras quando só poucos componentes forem úteis, exceto quando suas dependências/distribuição justificarem o pacote completo.

## 6. Router global

Proponha `~/.claude/CLAUDE.md` curto, com meta de aproximadamente 60 linhas úteis; esse número é uma meta de projeto, não limite do produto. Use regras claras:

- Rotina especificada: execute diretamente.
- Ambiguidade que muda escopo, dados, custo ou comportamento: esclareça o ponto; use grilling quando houver várias decisões interdependentes.
- Bug conhecido/mudança mecânica: não transforme em entrevista.
- Pesquisa extensa: contexto isolado com retorno compacto e fontes.
- Feature grande definida: spec e unidades verificáveis; paralelismo apenas para partes independentes.
- Mudança relevante/arriscada: review separado e com evidência.
- Frontend: carregar workflow visual apenas nessa tarefa.
- Contexto poluído/transição de fase: oferecer handoff; executar quando autorizado pelo usuário ou política aprovada.
- Trabalho longo independente: mecanismo background confirmado na versão local.
- Hook: comportamento determinístico ligado a evento; MCP: estado externo necessário que não esteja melhor servido por CLI/API já disponível.
- Deploy, migration, destruição ou ampliação relevante de permissões: autorização humana explícita no escopo da ação.

Não inclua domínio financeiro, RH ou hospitalar no global. Não injete este prompt inteiro no `CLAUDE.md`.

## 7. Contexto limpo e autonomia

Siga `04_HANDOFF_PROTOCOL.md`. Verifique na versão de A/B: subagents, `context: fork`, background, Agent View, `/background` e aliases, `claude --bg`, naming, resume/continue, fork, worktrees, auto-compaction, dynamic workflows e Agent Teams. Registre disponível/documentado/testado/ausente, incluindo SO e provedor.

Não confunda background da mesma conversa, nova sessão, subagent, fork e equipe. Não prometa iniciar uma sessão Claude dentro de outra sem verificar a arquitetura suportada. Testes de execução fazem parte da fase aprovada, com tarefa sintética, custo limitado e sem alteração dos projetos reais.

Inclua notificações, limites de permissão, monitoramento, retomada e conflitos. Sessões paralelas editando código precisam de isolamento. Worktrees não isolam bancos/Sheets/APIs nem sincronizam automaticamente código entre computadores.

## 8. Reprodutibilidade

Proponha repositório privado de configuração declarativa. Credenciais, paths locais, caches, logs, transcripts e estado de jobs ficam fora do sincronismo. Não crie/publicize repositório remoto sem autorização específica.

Planeje bootstrap idempotente, dry-run/diff, backup seletivo, rollback, merge preservando configurações locais e pinning de versões. Não copie cegamente o `settings.json` de A sobre B. O arquivo local de configuração também pode conter secrets.

## 9. Entregáveis da auditoria

Produza:

1. Diagnóstico e inventário de A/B, com lacunas explícitas.
2. Redundâncias, conflitos e dependências.
3. `01_STACK_MANIFEST.md` e `stack-manifest.yaml`, inicialmente propostas sem falso status de instalação.
4. `02_TWO_COMPUTERS.md`, com estratégia de bootstrap e parity check.
5. Router global proposto e árvore final.
6. Arquitetura por projeto; não preencha detalhes não inspecionados.
7. Workflow de frontend e review.
8. Plano handoff/background e matriz de compatibilidade.
9. `COMMANDS_RESOLVED.md`: comandos reais ou propostas identificadas, namespaces e fallback em linguagem natural.
10. Arquivos/settings que pretende criar/alterar, riscos e plano em fases.

Manifesto: nome, tipo, fonte, repo, versão/commit, licença quando relevante, método de instalação, escopo, invocação, dependências, variáveis exigidas sem valores, OS, projetos, permissões, gatilho, motivo, status e evidência de teste.

Pare antes da instalação/configuração e apresente uma decisão arquitetural concreta para aprovação. Depois de aprovada, a implementação usará `03_IMPLEMENTAR_STACK.md`.
