# Candidatos de stack — seleção pendente de auditoria

Este é o ponto de partida extraído da pesquisa e da conversa. As linhas abaixo não atestam instalação, compatibilidade ou leitura do código de cada repo. Valide conteúdo, origem, licença, dependências e versão antes de selecionar. Mudanças nos repositórios podem alterar nomes de skills.

## Núcleo e extensões por necessidade

| Família / fonte | Papel a avaliar | Localização/ativação proposta | Decisão inicial |
|---|---|---|---|
| [mattpocock/skills](https://github.com/mattpocock/skills) | Requisitos, specs, pesquisa, debugging, review, handoff | Procedimentos gerais disponíveis; workflows deliberados manuais | Prioritário; mapear primitivas e dependências |
| [OthmanAdi/planning-with-files](https://github.com/OthmanAdi/planning-with-files) | Plano/progresso persistentes | Ativar em tarefas longas; revisar hooks | Comparar com handoff/estado nativos, escolher um dono do estado |
| [anthropics/skills](https://github.com/anthropics/skills) | PDF, DOCX, PPTX, XLSX e padrões de skills | Documentos sob demanda; XLSX/PDF nos projetos pertinentes | Prioritário por componentes e licença, não pacote cego |
| [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) | Setup, desenvolvimento de plugins, feature, design, review e segurança | Avaliar frontend-design, plugin-dev, feature-dev, pr-review-toolkit, security-guidance e commit workflows | Confirmar nomes e selecionar sem duplicar Matt/review |
| [upstash/context7](https://github.com/upstash/context7) | Documentação de bibliotecas | Sob demanda; acesso externo sanitizado | Útil se não houver alternativa suficiente |
| [github/github-mcp-server](https://github.com/github/github-mcp-server) | Repos, issues, PRs, CI | Repos relevantes; ferramentas mínimas; começar leitura | Preferir Git/gh quando suficientes; escrita só no escopo autorizado |
| [microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp) | Browser e verificação de UI | Projetos com UI | Comparar CLI+skill com MCP; escolher um caminho principal |
| [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | Engenharia React/web, padrões e acessibilidade | Somente stack web compatível | Selecionar componentes correspondentes ao código |
| [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | Design/UI | Financeiro e censo app se pertinente | Alternativa/complemento específico ao frontend-design; justificar ambos se escolhidos |
| [trailofbits/skills](https://github.com/trailofbits/skills) | Review de segurança, análise estática e Python | Somente linguagens/superfícies presentes | Seleção pequena; não rodar auditoria ampla por padrão |
| [kenryu42/claude-code-safety-net](https://github.com/kenryu42/claude-code-safety-net) | Guardrails de comandos | Hook apenas depois de revisão e teste | Comparar com permissões nativas; evitar sensação de garantia total |
| [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | Pesquisa científica e análise de dados | Pack separado de pesquisa; não globalizar biblioteca inteira | Medicina não torna todo workflow hospitalar pesquisa científica |
| [firecrawl/firecrawl-mcp-server](https://github.com/firecrawl/firecrawl-mcp-server) | Pesquisa web/crawling | Pack pesquisa, com quotas e destino conhecidos | Condicional; não duplicar busca já disponível |
| [czlonkowski/n8n-skills](https://github.com/czlonkowski/n8n-skills) + [n8n-mcp](https://github.com/czlonkowski/n8n-mcp) | Automações n8n | Somente projeto n8n real | Fora do núcleo dos cinco projetos até demonstrar necessidade |
| [jarrodwatts/claude-hud](https://github.com/jarrodwatts/claude-hud) | Visibilidade de contexto/status | Ferramenta local opcional | Comparar com indicadores nativos, medir benefício |

Matt: inspecionar, se ainda existirem, `grill-me`, `grilling`, `grill-with-docs`, `research`, `to-spec`, `to-tickets`, `implement`/`implement-spec`, `diagnosing-bugs`, `tdd`, `code-review`, `domain-modeling`, `handoff` e `writing-for-agents`. Validar invocação e dependências no frontmatter/corpo. Uma interface pequena pode exigir outra skill; instalar só a interface pode quebrar o workflow.

Não criar `/grill`, `/feature` ou `/review` se já existir interface adequada com outro nome. Documentar o nome real. Wrapper próprio só depois de justificar a vantagem e registrar de que componente depende.

## Alternativas e referências que exigem comparação isolada

| Grupo | Candidatos | Política proposta |
|---|---|---|
| Harnesses amplos | [Superpowers](https://github.com/obra/superpowers), [ECC](https://github.com/affaan-m/ECC), [gstack](https://github.com/garrytan/gstack), [Compound Engineering](https://github.com/EveryInc/compound-engineering-plugin), [GSD](https://github.com/gsd-build/get-shit-done), [Oh My ClaudeCode](https://github.com/Yeachan-Heo/oh-my-claudecode) | Não habilitar vários roteadores/opiniões de processo simultaneamente; experimento delimitado se a base enxuta não bastar |
| Estado/memória adicional | [Beads](https://github.com/gastownhall/beads), [claude-mem](https://github.com/thedotmack/claude-mem), [Supermemory](https://github.com/supermemoryai/claude-supermemory) | Primeiro testar estado explícito e handoff; evitar múltiplos donos da mesma memória e captura automática de dados privados |
| Orquestração/swarm | [ruflo](https://github.com/ruvnet/ruflo), [Claude Squad](https://github.com/smtg-ai/claude-squad) | Experimento posterior; recursos nativos e poucos workers antes de framework |
| Catálogos de agentes | [wshobson/agents](https://github.com/wshobson/agents), [VoltAgent](https://github.com/VoltAgent/awesome-claude-code-subagents) | Referência para selecionar/escrever poucos agentes; não importar o catálogo inteiro |
| Context engineering | [Agent-Skills-for-Context-Engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering) | Estudar padrões; adotar somente procedimento que reduza um problema medido |

## Critérios de aceitação de um componente

Necessidade recorrente identificada; pouca sobreposição; fonte verificada; permissões conhecidas; dependências disponíveis; compatibilidade com A/B; instalação reproduzível; teste de ativação e desativação; comando/gatilho documentado; manutenção e licença aceitáveis. Registre bloqueios individualmente, sem interromper toda a implantação.

Não use o ranking como fila de instalação. O produto final deve responder “como esse componente melhora meus projetos?” e “o que deixamos de carregar por causa dele?”.
