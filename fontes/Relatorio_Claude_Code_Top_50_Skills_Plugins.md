# Claude Code em 2026: Skills, Plugins, Subagents, Hooks, MCPs e os cinquenta projetos mais relevantes no GitHub

**Escopo da pesquisa:** GitHub exclusivamente, com fotografia em **5 de outubro de 2026**. Foram considerados Agent Skills, Claude Code plugins, subagents, hooks, MCP servers, frameworks/harnesses de agentes, memória/context engineering e projetos auxiliares relevantes aos seus objetivos.

A principal conclusão é que você estava certo em olhar para `grill-me`, mas a categoria mental estava incompleta: **`grill-me` não é equivalente a um plugin, e uma skill não é simplesmente um “plugin pequeno”**. O ecossistema atual tem várias camadas que se combinam.

A forma mais útil de pensar nisso é:

> **Skill = procedimento especializado**  
> **Plugin = pacote que distribui componentes**  
> **Subagent = especialista com contexto próprio**  
> **Command = entrada explícita do usuário**  
> **Hook = automação acionada por eventos**  
> **MCP = conexão com ferramentas/dados externos**  
> **Harness/framework = arquitetura que coordena várias dessas peças**

Essa distinção é central porque os projetos mais interessantes de 2026 — `Superpowers`, `ECC`, `gstack`, `planning-with-files`, `Compound Engineering`, `ruflo` — **não são simplesmente coleções de prompts**. Eles estão cada vez mais próximos de sistemas operacionais para agentes.

## O mapa do ecossistema

A especificação aberta de Agent Skills define uma skill como uma pasta contendo obrigatoriamente um `SKILL.md`, com metadados e instruções, e opcionalmente scripts, referências, templates e outros recursos. A descoberta é progressiva: inicialmente o agente conhece apenas nome e descrição; o conteúdo completo entra no contexto quando a skill é ativada. | Componente | O que realmente é | Analogia útil | Quando faz sentido |
|---|---|---|---|
| **Skill** | Conhecimento + procedimento reutilizável em `SKILL.md`, podendo carregar scripts/referências | SOP/playbook | “Como revisar código”, “como pesquisar”, “como me entrevistar” |
| **Plugin** | Unidade de distribuição que pode conter skills, agents, hooks, MCP config e comandos | Aplicativo/pacote | Instalar um sistema inteiro |
| **Subagent** | Agente especializado executado com papel/contexto próprio | Especialista da equipe | Pesquisa, review, testes, implementação paralela |
| **Command** | Ação explicitamente chamada pelo usuário | Botão/comando | `/grill-me`, `/review`, `/plan` |
| **Hook** | Código/automação disparado automaticamente por eventos | Reflexo automático | Verificar antes de executar, reinjetar contexto, bloquear comando perigoso |
| **MCP server** | Interface que oferece ferramentas/dados externos ao modelo | Adaptador/USB-C | GitHub, browser, docs, bancos de dados, APIs |
| **Harness/framework** | Sistema coordenando skills, memória, agentes, hooks e workflow | Sistema operacional do agente | Desenvolvimento autônomo de longa duração |

A distinção plugin/skill é particularmente clara no próprio repositório oficial da Anthropic: o exemplo de plugin pode conter `.claude-plugin/plugin.json`, `.mcp.json`, `skills/`, agentes e outros componentes. A Anthropic passou a preferir **skills tanto para comportamentos chamados pelo modelo quanto para comportamentos explicitamente invocados pelo usuário**; o antigo diretório `commands/*.md` continua suportado, mas é considerado o formato legado para novos plugins. Portanto:

**uma skill pode existir sozinha; um plugin pode conter várias skills.**

Isso explica por que algo como `mattpocock/skills` pode ser instalado como um **Claude Code plugin**, embora o conteúdo conceitual central do projeto seja um conjunto de **skills**. O próprio repositório oferece as duas modalidades: plugin gerenciado no Claude Code ou cópias editáveis das skills para outros agentes. ### O caso `grill-me`

`grill-me` é um excelente exemplo porque ele é muito menor do que parece.

Matt Pocock divide suas skills em dois tipos:

**User-invoked:** você chama explicitamente, por exemplo `/grill-me`.

**Model-invoked:** Claude pode decidir carregá-las automaticamente quando uma tarefa combina com sua descrição. `/grill-me` é essencialmente o **ponto de entrada/orquestrador**. O mecanismo reutilizável por baixo é a skill `grilling`, que conduz uma entrevista agressiva sobre uma decisão, design ou plano até resolver as ramificações importantes. Matt descreve `grilling` como o primitive reutilizado também por `grill-with-docs`, `triage`, `wayfinder` e `improve-codebase-architecture`. Isso é uma ideia arquitetural importante:

> **Boas skills não precisam ser grandes. Elas podem compor primitivas menores.**

`grill-with-docs` é particularmente interessante para você. Ele faz o grilling, mas também transforma as decisões em memória persistente do projeto, trabalhando o vocabulário do domínio, `GLOSSARY.md` e ADRs. Matt argumenta que isso melhora a comunicação subsequente entre humano e agente e reduz ambiguidade conceitual. Já `to-spec` pega uma conversa que amadureceu e a transforma em especificação; `to-tickets` decompõe um plano em unidades executáveis; `implement-spec` executa essas unidades usando subagents quando há tarefas independentes; e `code-review` separa revisão de padrões e fidelidade à especificação em subagents paralelos, evitando que um eixo contamine o outro. Ou seja, há praticamente uma cadeia:

**ideia → `/grill-me` → `/grill-with-docs` → `/to-spec` → `/to-tickets` → `/implement-spec` → `/code-review` → `/retro`**

Isso é muito mais interessante do que instalar “um prompt bom”.

## Como a seleção foi construída

Há uma limitação importante na expressão “melhores avaliações no GitHub”: **GitHub não possui um sistema de reviews ou estrelas de 1–5 para repositórios**. Uma star é um sinal de interesse/adoção, não uma avaliação de qualidade.

Por isso, tratei “melhor avaliado” como uma combinação de sinais.

O pool inicial foi deliberadamente amplo. Um dos índices usados para descoberta foi `subinium/awesome-claude-code`, que impõe como regra listar apenas projetos com pelo menos **1.000 GitHub stars**; depois disso, os projetos mais promissores foram confrontados com seus próprios repositórios, documentação, issues e estrutura técnica. O **score global de 0–100** abaixo é meu score composto, com aproximadamente:

| Critério | Peso |
|---|---:|
| Adoção: stars, forks, comunidade | 25% |
| Qualidade técnica/arquitetural | 20% |
| Utilidade prática | 20% |
| Credibilidade do autor/organização | 15% |
| Composição/interoperabilidade | 10% |
| Documentação, testes, evals, exemplos | 10% |

**Recência foi usada como informação e desempate, não como penalidade automática.** Isso respeita sua decisão: um projeto excelente não perde a posição simplesmente porque está estável ou arquivado.

Segurança também **não removeu projetos do ranking**. Ela aparece apenas como superfície de risco:

**L** = predominantemente instruções, pouca execução externa.  
**M** = scripts, filesystem, hooks ou rede.  
**H** = browser, credenciais, escrita em serviços externos ou autonomia ampla.

Isso significa **superfície de privilégio**, não “o projeto é inseguro”.

Também atribuí um **Score Ettore**, reponderando o ranking conforme as prioridades que você forneceu: programação, pesquisa profunda, agentes autônomos, documentos, dados, produtividade, memória, APIs, segurança, frontend e backend, nessa ordem.

Finalmente, “recomendado por nomes respeitados” precisou de uma interpretação rigorosa. Como você restringiu a investigação ao **GitHub**, eu considerei principalmente autoria/manutenção e referências verificáveis dentro do GitHub, não tweets, podcasts ou newsletters. Entre os repositórios de alto sinal apareceram projetos de **Anthropic, GitHub, Microsoft, Vercel Labs, Trail of Bits, Supabase, Every Inc.**, além de builders como **Matt Pocock, Addy Osmani, Garry Tan, Anthony Fu e Kepano**. Uma ressalva importante: quando um README diz que segue “as regras de Karpathy”, por exemplo, isso **não equivale a um endosso de Andrej Karpathy ao projeto**. O README do `gstack` faz essa referência, mas inferir endorsement seria metodologicamente errado. Diferenças de dois ou três pontos nos scores abaixo devem ser entendidas como **mesma faixa**, não como uma verdade matemática do tipo “89 é objetivamente melhor que 87”.

## Ranking global dos cinquenta projetos

O topo atual do ecossistema é surpreendentemente competitivo. Há repositórios específicos de Agent Skills com centenas de milhares de stars: `mattpocock/skills` estava em **276,9 mil**, `anthropics/skills` em **179,8 mil** e `affaan-m/ECC` em **273,3 mil** no snapshot pesquisado. `obra/superpowers` aparecia com aproximadamente **291 mil stars**. | # | Projeto | Tipo | Global | Ettore | Melhor uso | Risco |
|---:|---|---|---:|---:|---|:---:|
| 1 | **obra/superpowers** | Plugin/harness | **97** | 94 | Processo disciplinado de desenvolvimento, planning, TDD e subagents | M |
| 2 | **mattpocock/skills** | Skills/plugin | **97** | **99** | Pensamento, especificação, TDD, research, review | L–M |
| 3 | **anthropics/skills** | Skills oficiais | **96** | 96 | Referência canônica + documentos + exemplos | L–M |
| 4 | **affaan-m/ECC** | Harness | **95** | 95 | Sistema completo: skills, memória, research, segurança | H |
| 5 | **garrytan/gstack** | Plugin/workflow | **94** | 91 | Desenvolvimento com papéis de CEO, design, engineering, release | M |
| 6 | **addyosmani/agent-skills** | Skills | **93** | 92 | Engenharia orientada a define→plan→build→verify→review→ship | M |
| 7 | **nextlevelbuilder/ui-ux-pro-max-skill** | Skill/plugin | **93** | 90 | Design systems e frontend | M |
| 8 | **thedotmack/claude-mem** | Plugin/memória | **92** | 94 | Memória automática cross-session | H |
| 9 | **K-Dense-AI/scientific-agent-skills** | Skills | **91** | **97** | Pesquisa científica, medicina, dados | M |
| 10 | **ruvnet/ruflo** | Multi-agent harness | **91** | 95 | Swarms, memória, agentes autônomos | H |
| 11 | **upstash/context7** | MCP | **91** | **96** | Documentação atual de bibliotecas durante coding | M |
| 12 | **anthropics/claude-plugins-official** | Plugins oficiais | **90** | 93 | Referência e plugins Claude Code | M |
| 13 | **vercel-labs/agent-skills** | Skills oficiais | **90** | 91 | React, Next.js, web design, performance | M |
| 14 | **kepano/obsidian-skills** | Skills | **89** | 94 | Knowledge management/Obsidian | M |
| 15 | **github/github-mcp-server** | MCP oficial | **89** | **95** | Repos, issues, PRs, Actions e code security | H |
| 16 | **microsoft/playwright-mcp** | MCP oficial | **89** | 92 | Browser automation e UI testing | H |
| 17 | **EveryInc/compound-engineering-plugin** | Plugin/harness | **88** | 91 | Engineering workflow + subagents | M |
| 18 | **OthmanAdi/planning-with-files** | Skill/plugin/hooks | **88** | **98** | Long-running agents, planejamento e recuperação de contexto | M |
| 19 | **wshobson/agents** | Plugin marketplace | **87** | 91 | Catálogo enorme de especialistas/subagents | M–H |
| 20 | **agentskills/agentskills** | Especificação | **87** | 89 | Standard aberto de skills | L |
| 21 | **VoltAgent/awesome-agent-skills** | Biblioteca/index | **86** | 85 | Descoberta de skills | L |
| 22 | **sickn33/antigravity-awesome-skills** | Biblioteca | **86** | 84 | Grande catálogo de skills | M |
| 23 | **gastownhall/beads** | Memória/tasks | **86** | **96** | Memória estruturada e trabalho persistente | M |
| 24 | **SuperClaude-Org/SuperClaude_Framework** | Framework | **85** | 87 | Workflow Claude Code completo | H |
| 25 | **gsd-build/get-shit-done** | Harness/context | **85** | 93 | Spec/context engineering | M |
| 26 | **Yeachan-Heo/oh-my-claudecode** | Orquestração | **85** | 93 | Coordenação de workflows/agentes | H |
| 27 | **trailofbits/skills** | Security skills/plugins | **85** | 93 | Code/security audit | M–H |
| 28 | **supabase/agent-skills** | Skills oficiais | **84** | 88 | Backend, PostgreSQL, Supabase | M |
| 29 | **czlonkowski/n8n-skills** | Skills/plugin/hooks | **84** | **95** | Construção de automações n8n | H |
| 30 | **czlonkowski/n8n-mcp** | MCP | **84** | **96** | Executar/inspecionar n8n através do agente | H |
| 31 | **jarrodwatts/claude-hud** | Observabilidade | **83** | 92 | Tornar estado/contexto do Claude visível | L–M |
| 32 | **VoltAgent/awesome-claude-code-subagents** | Subagents/index | **83** | 90 | Biblioteca de especialistas | L |
| 33 | **humanlayer/humanlayer** | Agent framework | **83** | 89 | Human-in-the-loop para agentes | H |
| 34 | **smtg-ai/claude-squad** | Multi-agent | **82** | 88 | Sessões/agentes paralelos | H |
| 35 | **davila7/claude-code-templates** | Templates/plugins | **82** | 84 | Descoberta e instalação de configurações | M |
| 36 | **muratcankoylan/Agent-Skills-for-Context-Engineering** | Skills | **82** | 92 | Context engineering | L–M |
| 37 | **antfu/skills** | Skills | **81** | 86 | Engineering workflows curados | L–M |
| 38 | **lackeyjb/playwright-skill** | Skill | **81** | 89 | Browser/UI testing via skill | M–H |
| 39 | **SawyerHood/dev-browser** | Browser tooling | **81** | 89 | Browser de desenvolvimento para agentes | H |
| 40 | **firecrawl/firecrawl-mcp-server** | MCP | **81** | **94** | Web search, scraping, crawling e research | H |
| 41 | **PleasePrompto/notebooklm-skill** | Skill | **80** | 91 | Pesquisa grounded sobre seus documentos | H |
| 42 | **Orchestra-Research/AI-Research-SKILLs** | Research skills | **80** | 93 | Pesquisa e workflows acadêmicos | M |
| 43 | **snyk/agent-scan** | Segurança | **80** | 91 | Inspeção de agentes/configurações | M |
| 44 | **nizos/tdd-guard** | Hooks/guardrail | **79** | 90 | Forçar disciplina TDD | M |
| 45 | **kenryu42/claude-code-safety-net** | Hooks/guardrail | **79** | 89 | Prevenir comandos destrutivos | M |
| 46 | **pchalasani/claude-code-tools** | Ferramentas/plugin | **79** | 89 | Utilitários para Claude Code | M |
| 47 | **aidenybai/react-grab** | Frontend tool | **78** | 86 | Dar contexto visual/componentes React ao agente | M |
| 48 | **supermemoryai/claude-supermemory** | Memória | **78** | 94 | Memória persistente externa | H |
| 49 | **CodeGraphContext/CodeGraphContext** | Code graph/context | **78** | 91 | Representação estrutural de codebase | M |
| 50 | **u14app/deep-research** | Research agent | **77** | 94 | Pesquisa profunda autônoma | H |

Os primeiros colocados não são simplesmente populares. Por exemplo, `Superpowers` formaliza brainstorming, especificação, implementação, TDD e desenvolvimento com subagents; `ECC` se descreve como um sistema de otimização do “agent harness”, integrando skills, memória, segurança e research-first development; e `ruflo`, antigo Claude Flow, já se apresenta como um harness multi-agent com swarms, adaptive memory e integração com vários agentes. `gstack`, de Garry Tan, é outra abordagem interessante: em vez de ser uma coleção genérica, organiza mais de vinte ferramentas em torno de papéis como CEO, designer, engineering manager, release manager, documentation engineer e QA. Seu repositório estava acima de **133 mil stars** no snapshot pesquisado. `addyosmani/agent-skills` é particularmente forte em qualidade de engenharia. O repositório, com cerca de **95 mil stars**, explicita que skills devem ser específicas, verificáveis, testadas e mínimas; releases recentes também destacam validação, evals, CI e portabilidade entre agentes. `UI UX Pro Max` merece atenção especial para frontend: sua estrutura já incorpora `.claude-plugin`, `.claude/skills`, CLI e outros componentes, e um issue de julho de 2026 já mencionava mais de **101 mil stars**; portanto, não é mais uma pequena skill de nicho. Na área de memória, `claude-mem` atingiu aproximadamente **92 mil stars**; porém, justamente por interferir bastante no ciclo de vida do Claude, sua superfície operacional é maior do que a de uma skill simples. Há issues envolvendo hooks e lifecycle/subagents, o que não prova insegurança, mas mostra que memória automática traz complexidade operacional real. Para ciência, `K-Dense-AI/scientific-agent-skills` é provavelmente o achado que mais muda o ranking personalizado para você: o repositório tinha **47,7 mil stars**, 4,3 mil forks e 177 skills voltadas a ciência, biologia, química, medicina, análise de dados e workflows de evidência clínica. Entre MCPs, `Context7` tinha **62,7 mil stars**, `Playwright MCP` **37,8 mil**, o servidor oficial do GitHub **33,3 mil** e Firecrawl MCP **7,6 mil**. A biblioteca `planning-with-files`, embora menor que os gigantes, merece posição muito acima do que stars isoladamente sugeririam: tinha **27,3 mil stars** e implementa persistent planning, recuperação após `/clear`/compaction, hooks de reinjeção e gates de conclusão. `Beads`, hoje em `gastownhall/beads`, tinha aproximadamente **27,6 mil stars** e se define como uma “memory upgrade” para coding agents, sendo particularmente interessante para estruturar trabalho persistente em vez de apenas tentar lembrar semanticamente conversas anteriores. O restante do top 50 foi filtrado a partir do universo GitHub de skills, plugins, subagents, orchestration e MCPs — incluindo SuperClaude, GSD, Oh My ClaudeCode, HumanLayer, Claude Squad, Playwright Skill, React Grab, Safety Net, TDD Guard e CodeGraphContext. ## As skills individuais que mais valem instalar

Aqui aparece uma diferença importante entre **“qual repositório é excelente?”** e **“qual comportamento eu realmente quero adicionar ao Claude?”**.

Para o seu uso, eu daria mais atenção às skills concretas abaixo do que à caça indiscriminada a bibliotecas com milhares de skills.

| Skill/componente | Origem | Por que considero importante para você |
|---|---|---|
| **grill-me** | Matt Pocock | Obriga você a esclarecer uma ideia antes de agir |
| **grilling** | Matt Pocock | Primitive reutilizável de entrevista crítica |
| **grill-with-docs** | Matt Pocock | Grilling + conhecimento persistente do projeto |
| **to-spec** | Matt Pocock | Converte pensamento amadurecido em especificação |
| **to-tickets** | Matt Pocock | Decompõe spec em unidades executáveis |
| **implement** | Matt Pocock | Implementação disciplinada com TDD/review |
| **implement-spec** | Matt Pocock | Executa uma spec usando task graph e subagents |
| **research** | Matt Pocock | Pesquisa fontes primárias e cria Markdown citado |
| **diagnosing-bugs** | Matt Pocock | Loop disciplinado de diagnóstico |
| **tdd** | Matt Pocock | Red-green-refactor |
| **code-review** | Matt Pocock | Reviews paralelos de standards e spec |
| **domain-modeling** | Matt Pocock | Vocabulário e modelo conceitual do projeto |
| **handoff** | Matt Pocock | Entrega contexto compacto para outro agente/sessão |
| **teach** | Matt Pocock | Workspace de aprendizado persistente |
| **writing-for-agents** | Matt Pocock | Escrever documentação otimizada para agentes |
| **react-best-practices** | Vercel | Performance React/Next |
| **web-design-guidelines** | Vercel | Auditoria de UX, acessibilidade e performance |
| **writing-guidelines** | Vercel | Documentação/prosa técnica |
| **differential-review** | Trail of Bits | Review de segurança baseado em diff/history |
| **static-analysis** | Trail of Bits | CodeQL/Semgrep/SARIF |
| **supply-chain-risk-auditor** | Trail of Bits | Dependências e supply-chain |
| **second-opinion** | Trail of Bits | Review independente com outro agente |
| **modern-python** | Trail of Bits | Práticas modernas de Python |
| **post-patch-validation** | Trail of Bits | Verificação rigorosa depois de correções |

As descrições das skills de Matt vêm diretamente de seu catálogo atual. Ele identifica `grill-me` e `grill-with-docs` como suas skills mais populares e descreve todo o fluxo de engineering, incluindo `research`, `TDD`, `diagnosing-bugs`, `code-review`, `implement-spec`, `handoff` e `writing-for-agents`. ### O que eu instalaria antes de `grill-me`

Tecnicamente nada: `grill-me` é útil imediatamente.

Mas conceitualmente, eu instalaria **o repositório inteiro de Matt**, não apenas aquela skill, porque o valor real está nas composições.

Para você, particularmente:

**`grill-me` → `to-spec`** é uma máquina de transformar ideias meio difusas em projetos implementáveis.

**`grill-with-docs` → `domain-modeling`** é extremamente interessante para a clínica, agentes, sistemas internos e qualquer projeto em que as palavras tenham significados específicos.

**`research` → `to-spec`** é útil para programação orientada por pesquisa.

**`implement-spec` → `code-review` → `retro`** aproxima Claude de um engenheiro trabalhando com processo, em vez de um autocomplete hipervitaminado. ### Anthropic para documentos

Você também não deveria ignorar as próprias skills da Anthropic. O repositório oficial inclui as implementações de referência usadas para **DOCX, PDF, PPTX e XLSX**, inclusive versões source-available das skills que sustentam capacidades de documentos do Claude. O repositório tinha aproximadamente **179,8 mil stars e 21,2 mil forks** no momento da pesquisa. Isso alinha diretamente com sua prioridade de criação/manipulação de documentos.

### Vercel para frontend

O `vercel-labs/agent-skills` tinha aproximadamente **31,9 mil stars** e inclui `react-best-practices`, com mais de quarenta regras de React/Next.js; `web-design-guidelines`, com mais de cem verificações relacionadas a acessibilidade, UX e performance; além de writing, React Native, composition patterns e otimização de projetos Vercel. Para frontend, eu confiaria mais nessa combinação:

**Vercel Agent Skills + UI UX Pro Max + Playwright**

do que em uma skill genérica chamada “frontend-expert”.

### Trail of Bits para segurança e debugging

`trailofbits/skills`, com aproximadamente **7,4 mil stars**, é um exemplo de situação em que reputação e especialização técnica importam mais do que alcançar cem mil stars. O marketplace cobre differential review, static analysis, supply-chain risk, C/C++/Rust review, fuzzing, Semgrep, post-patch validation e outros workflows de segurança. Para você, eu destacaria também `modern-python`: é uma fonte mais interessante para ensinar boas práticas ao seu agente Python do que simplesmente escrever “use best practices”.

### Pesquisa científica e medicina

Aqui eu mudaria significativamente sua stack.

`K-Dense-AI/scientific-agent-skills` não é uma única skill médica; é uma biblioteca de **177 workflows científicos**, cobrindo explicitamente pesquisa clínica/evidência, bioinformática, genômica, drug discovery, healthcare AI, scientific computing, dados e comunicação científica. O README diferencia ainda pesquisa/avaliação retrospectiva de decisões clínicas sobre pacientes, uma distinção metodológica importante. Para um médico que está simultaneamente aprendendo programação e construindo agentes, eu classificaria isso como **muito mais relevante para você do que a maior parte dos top-100 genéricos de Claude Skills**.

## MCP, subagents, hooks e memória: o que realmente muda o jogo

Uma skill diz ao Claude **como fazer**.

Um MCP dá ao Claude **algo com que fazer**.

Essa é a diferença fundamental.

`Context7`, por exemplo, fornece documentação atual de bibliotecas para LLMs e editores; estava em **62,7 mil stars**. Para programação, isso ataca diretamente um problema frequente de agentes: usar APIs de versões erradas ou inferir documentação antiga. O servidor MCP oficial do GitHub permite ao agente navegar código, commits, issues e PRs, trabalhar com Actions e consultar informações de segurança. Também oferece seleção fina de toolsets, **read-only mode** e um **lockdown mode** destinado a reduzir exposição a prompt injection proveniente de conteúdo não confiável em issues, comentários e PRs. Minha shortlist de MCPs para o seu caso seria:

| MCP | Prioridade Ettore | Função |
|---|---:|---|
| **Context7** | **10/10** | Documentação atual para programação |
| **GitHub MCP** | **10/10** | Repos, issues, PRs, CI, agentes |
| **Firecrawl MCP** | **9,5/10** | Pesquisa/web crawling |
| **Playwright MCP** | **9/10** | Browser, testes, UI |
| **n8n MCP** | **9/10** | Automação de workflows |
| **MCP reference servers** | 8/10 | Aprender padrões MCP |

O repositório `modelcontextprotocol/servers` hoje se concentra em servidores de referência; vários servidores históricos — GitHub, Git, Google Drive, Slack, PostgreSQL, Puppeteer, Redis, SQLite etc. — foram movidos/arquivados conforme o ecossistema amadureceu. O GitHub MCP, por exemplo, migrou para o repositório oficial `github/github-mcp-server`. **Não instale MCPs indiscriminadamente.** Cada tool exposta aumenta o espaço de decisão do agente e, dependendo do MCP, também aumenta permissões e superfície de credenciais.

O próprio GitHub MCP reconhece isso ao permitir habilitar apenas toolsets específicos e operar em read-only. ### Playwright: um detalhe interessante

Há uma evolução recente particularmente reveladora: o próprio repositório do Playwright MCP informa que, **para coding agents, o usuário pode se beneficiar mais de CLI + Skills do que MCP**. Isso mostra que “MCP sempre é melhor” já está se tornando uma premissa errada.

Para algumas tarefas:

**skill + CLI = menos contexto + comportamento mais previsível**

pode vencer:

**MCP expondo dezenas de tools ao modelo**.

Essa distinção merece ser testada no seu ambiente.

### Firecrawl

Firecrawl MCP adiciona search, scraping e crawling ao agente e tinha cerca de **7,6 mil stars**. A versão pesquisada também inclui ferramentas voltadas a pesquisa em papers/repositórios. Aqui eu colocaria um ⚠️ operacional: issues recentes do próprio GitHub relatam problemas relacionados a descrições de ferramentas, discrepâncias de `readOnlyHint` e uma alegação de leitura arbitrária de arquivos locais através de uma ferramenta. Issues não equivalem a vulnerabilidades confirmadas e podem já ter correções em andamento, mas são suficientemente relevantes para justificar execução com privilégios mínimos. ### Subagents

Subagents são úteis quando você quer **separar raciocínios ou contextos**, e não simplesmente “mais inteligência”.

Os melhores casos são:

**Researcher →** pesquisa sem poluir o contexto principal.

**Reviewer →** revisa algo que o agente principal implementou.

**Tester →** tenta quebrar a solução.

**Security reviewer →** procura uma categoria específica de falhas.

**Implementers paralelos →** trabalham em partes independentes de um task graph.

Matt Pocock usa exatamente esse padrão no `code-review`: Standards e Spec são avaliados por subagents diferentes para reduzir contaminação entre os critérios. `implement-spec` pode lançar implementadores paralelos sobre tarefas independentes. Plugins oficiais da Anthropic também usam arquiteturas multi-agent em workflows de development e review. O erro seria pensar:

> “se um agente é bom, sete agentes serão sete vezes melhores.”

Não serão. Você ganha paralelismo e independência, mas paga em tokens, integração, duplicação de trabalho e coordenação.

### Hooks

Hooks são provavelmente o componente mais subestimado.

Eles permitem fazer algo acontecer **mesmo quando Claude “esquece” de seguir uma regra**.

Exemplo extremamente bom: `planning-with-files`.

Ele registra no Claude Code hooks para `SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `PreCompact` e `Stop`. Com isso, o plano pode ser reinjetado, o progresso lembrado e uma sessão recuperada mesmo após compactação. Isso é fundamentalmente diferente de escrever no `CLAUDE.md`:

> “lembre-se de sempre atualizar o plano”.

Uma é uma sugestão ao modelo.

A outra é infraestrutura.

Esse é um dos motivos pelos quais atribuí **98/100 de adequação ao seu caso** a `planning-with-files`.

O projeto inclusive reduziu descrições de skills carregadas desnecessariamente pelo plugin porque o scanner do Claude registrava várias variantes no system prompt. É uma demonstração prática de que instalar tudo indiscriminadamente tem custo de contexto. ### Commands versus skills

Outro detalhe que pode evitar confusão: muitos posts antigos falam em “slash commands” como uma categoria totalmente separada.

A arquitetura oficial evoluiu. O exemplo atual da Anthropic recomenda skills para novos comportamentos user-invoked/model-invoked; `commands/*.md` permanece como formato legado. Portanto, `/grill-me` **parece um command na interface**, mas arquiteturalmente é uma **user-invoked skill**.

### Memória: não instale três soluções imediatamente

Aqui sou mais conservador do que os rankings de GitHub.

`claude-mem`, `Beads`, `planning-with-files` e `Supermemory` resolvem problemas relacionados, mas diferentes.

| Ferramenta | Tipo de memória |
|---|---|
| **planning-with-files** | Estado explícito do plano e progresso |
| **Beads** | Trabalho/tasks estruturados persistentes |
| **claude-mem** | Captura automática de contexto entre sessões |
| **Supermemory** | Memória externa/semântica |

Minha ordem para você seria:

**planning-with-files primeiro → Beads depois, se necessário → claude-mem somente se a memória conversacional ainda for um problema.**

Isso é deliberadamente o inverso do impulso “92k stars, instala já”.

Memória automática parece mágica, mas é também uma nova fonte de estado oculto. Para alguém construindo agentes autônomos, é melhor aprender primeiro a manter **estado explícito, auditável e versionável**.

`NotebookLM Skill` é um caso diferente: tinha **7,8 mil stars** e permite Claude Code consultar seus próprios notebooks/documentos para respostas grounded. Entretanto, foi **arquivado em 10 de setembro de 2026**, e o próprio mantenedor alerta que não haverá updates ou suporte e que mudanças upstream podem quebrá-lo. Como você pediu, não o excluí por abandono. Ele continua conceitualmente excelente — e provavelmente vale um fork ou procurar seu sucessor — mas eu não o colocaria no núcleo da infraestrutura.

## A stack ideal para Ettore

Seu ranking pessoal muda bastante em relação ao ranking global porque seu problema não é “fazer Claude gerar código mais rápido”.

Você quer progressivamente transformar Claude em:

**parceiro crítico → pesquisador → arquiteto → programador → conjunto de agentes especializados → sistema autônomo.**

Por isso, meu **Top pessoal para você** ficaria assim:

| Ordem | Projeto | Ettore Score | Papel na sua stack |
|---:|---|---:|---|
| 1 | **mattpocock/skills** | **99** | Pensamento, especificação, engineering |
| 2 | **planning-with-files** | **98** | Persistência e tarefas longas |
| 3 | **K-Dense scientific-agent-skills** | **97** | Medicina, ciência, pesquisa, dados |
| 4 | **Context7** | **96** | Coding com documentação atual |
| 5 | **n8n MCP** | **96** | Automação/agentes conectados |
| 6 | **Beads** | **96** | Estado/task memory |
| 7 | **Anthropic Skills** | **96** | Docs + referência canônica |
| 8 | **ECC** | **95** | Harness avançado |
| 9 | **GitHub MCP** | **95** | Desenvolvimento autônomo real |
| 10 | **n8n Skills** | **95** | Construção de automações |
| 11 | **ruflo** | **95** | Experimentos multi-agent |
| 12 | **Superpowers** | **94** | Disciplina de engenharia |
| 13 | **Firecrawl MCP** | **94** | Deep research/web |
| 14 | **Obsidian Skills** | **94** | Knowledge management |
| 15 | **claude-mem / Supermemory** | **94** | Memória de longo prazo |

Mas **não recomendo instalar esses quinze simultaneamente**.

Esse seria justamente o tipo de decisão que `/grill-me` deveria impedir.

Há sobreposição forte entre:

**Superpowers ↔ ECC ↔ gstack ↔ Compound Engineering ↔ GSD ↔ Oh My ClaudeCode.**

Todos tentam, em alguma medida, decidir **como o agente trabalha**. Instalar vários sistemas com opiniões fortes simultaneamente pode gerar instruções redundantes ou contraditórias, além de aumentar a superfície de contexto e execução. Isso é uma inferência arquitetural a partir das funções declaradas pelos projetos, não uma alegação de incompatibilidade formal. Eu montaria sua arquitetura em camadas.

**Núcleo cognitivo**

`mattpocock/skills`

Começaria por `grill-me`, `grill-with-docs`, `to-spec`, `research`, `diagnosing-bugs`, `tdd`, `code-review`, `handoff` e `writing-for-agents`. É a melhor combinação que encontrei entre simplicidade, composição e valor cognitivo. O repo tinha **276,9 mil stars e 23,2 mil forks** no snapshot. **Persistência**

`planning-with-files`

Para você isso resolve um problema mais fundamental que “memória”: permite ao agente manter uma tarefa longa estruturada, sobreviver a compaction e recuperar objetivo/progresso. O plugin integra skill, commands e hooks; o projeto tinha **27,3 mil stars e 2,3 mil forks**. **Pesquisa científica**

`K-Dense-AI/scientific-agent-skills`

É a adição mais óbvia dada sua profissão. Com 177 skills, **47,7 mil stars** e workflows explicitamente relacionados a pesquisa clínica, evidência, dados e healthcare AI, ele oferece conhecimento procedimental muito mais especializado do que uma collection genérica. **Conhecimento de programação**

`Context7`

Para um médico aprendendo Python e agentes, há uma diferença enorme entre Claude “lembrar como uma library costuma funcionar” e consultar documentação atual. Context7 é exatamente a camada que eu colocaria cedo. **GitHub**

`github/github-mcp-server`, inicialmente em **read-only** e apenas com os toolsets necessários.

Depois você pode liberar issues/PRs/write de forma progressiva. O servidor oficial oferece controles explícitos para isso. **Documentos**

`anthropics/skills`, sobretudo PDF, DOCX, PPTX e XLSX.

Isso cobre diretamente seu uso empresarial, pesquisa e documentos da clínica sem precisar confiar primeiro em uma coleção obscura de terceiros. **Automação**

`n8n-skills + n8n-mcp`.

Essa combinação é especialmente interessante porque demonstra a complementaridade:

> **Skill ensina Claude como construir bons workflows n8n. MCP permite Claude interagir com n8n.**

O `n8n-skills` atual contém 14 skills complementares, um router, hooks e integração com `n8n-mcp`; tinha aproximadamente **6,4 mil stars e 1,1 mil forks**. **Browser**

Eu testaria **Playwright CLI + Skills primeiro** e Playwright MCP depois, precisamente porque a própria equipe Microsoft agora sugere que coding agents podem se beneficiar da abordagem CLI+skills. O MCP permanece excelente quando você realmente precisa de interface de ferramenta persistente. **Frontend**

`vercel-labs/agent-skills + UI UX Pro Max`.

A primeira fornece standards de engenharia/web; a segunda oferece uma camada muito mais rica de design intelligence. **Segurança**

`Trail of Bits Skills + Safety Net`.

Trail of Bits para *saber o que procurar*; Safety Net/hooks para impedir determinadas classes de operação indesejada automaticamente. **Harness avançado**

Somente depois eu faria um experimento controlado:

**Superpowers vs ECC**, usando o mesmo projeto pequeno.

`Superpowers` é mais fortemente orientado a um processo disciplinado de desenvolvimento e subagent-driven engineering; `ECC` é mais amplo, tentando integrar skills, instincts, memory, security e research-first development. Ambos têm adoção enorme. Eu **não escolheria pelo número de stars**. Escolheria pelo que introduz menos comportamento inesperado no seu workflow.

**Multi-agent**

Só depois dessa base partiria para `ruflo`, Claude Squad ou sistemas de swarm. `ruflo` estava em aproximadamente **73,9 mil stars** e oferece uma superfície muito maior — swarms, workflows autônomos, memória e integração com múltiplos runtimes. Isso o torna poderoso, mas também péssimo como primeiro passo para aprender arquitetura de agentes: abstrairia justamente as peças que você ainda precisa entender. A arquitetura que eu efetivamente montaria para você hoje seria:

```text
                       E T T O R E
                           │
                           ▼
                 mattpocock/skills
             grill → research → spec
                           │
             ┌─────────────┴──────────────┐
             ▼                            ▼
    planning-with-files              K-Dense
    plano + persistência        ciência + medicina
             │                            │
             └─────────────┬──────────────┘
                           ▼
                     CLAUDE CODE
                           │
       ┌───────────────────┼──────────────────┐
       ▼                   ▼                  ▼
   Context7             GitHub MCP        Firecrawl
   docs/APIs            code/PRs          research/web
       │                   │                  │
       └───────────────────┼──────────────────┘
                           ▼
                  implementação/agentes
                           │
             ┌─────────────┼──────────────┐
             ▼             ▼              ▼
          n8n          Playwright       Vercel
       automação         browser        frontend
                           │
                           ▼
                 review / segurança
                   Trail of Bits
```

E há uma conclusão mais importante que o próprio ranking:

**eu não acho que seu próximo passo seja procurar “mais skills”.**

Os repositórios gigantes já oferecem centenas ou milhares delas. O ganho marginal de instalar a skill número 73 provavelmente será pequeno.

O salto real é aprender a combinar corretamente quatro padrões:

**Skill para procedimento.**  
**Hook para garantia/invariante.**  
**MCP para capacidade externa.**  
**Subagent para isolamento ou paralelismo.**

A partir daí, um plugin é principalmente a unidade conveniente para distribuir tudo isso.

E `grill-me` é um ótimo ponto de partida justamente porque exemplifica o princípio oposto ao hype atual: **uma skill de sete linhas pode ser mais útil do que um framework com cem agentes, desde que esteja posicionada no ponto certo do processo**. A própria coleção de Matt estrutura `grill-me` como uma interface pequena sobre um primitive `grilling` reutilizável e, em seguida, compõe esse primitive com specs, documentação, arquitetura e implementação. Para o seu perfil, a combinação de maior alavancagem não é “Claude com o maior número de ferramentas”. É:

**Claude que primeiro o interroga (`grill-me`), depois pesquisa (`research` + K-Dense + Firecrawl), formaliza (`to-spec`), mantém estado (`planning-with-files`), busca documentação real (`Context7`), age sobre o mundo (`MCPs`), delega tarefas independentes (`subagents`) e é impedido por infraestrutura de ignorar invariantes importantes (`hooks`).**

Isso já deixa de ser “usar Claude Code melhor” e começa a se aproximar da arquitetura dos agentes autônomos que você quer aprender a construir.
