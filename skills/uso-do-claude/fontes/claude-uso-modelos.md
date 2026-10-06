# Claude Code em outubro de 2026: base de evidências para qualidade, custo, velocidade e autonomia

**Data da pesquisa:** 3 de outubro de 2026, fuso America/São_Paulo.  
**Escopo temporal:** estado documentado dos produtos e modelos nessa data, preservando resultados históricos quando ajudam a explicar mudanças de comportamento.  
**Status desta entrega:** pesquisa e conclusões provisórias. **Não** é ainda o guia de operação, o `CLAUDE.md` nem uma configuração recomendada para seus repositórios.

A conclusão mais importante é que várias regras simples que circulam sobre Claude Code não sobrevivem à evidência atual. “Sonnet para fácil, Opus para difícil” é grosseiro demais; “max é sempre melhor” é demonstravelmente falso em pelo menos um benchmark de coding; “uma sessão nova sempre economiza tokens” confunde contexto, cache e reconstrução de estado; “mais agentes = mais capacidade” ignora duplicação, comunicação e conflitos; e **Fable 5.1 não deve ser interpretado como um Opus automaticamente melhor para coding**, apesar de ocupar o topo da taxonomia comercial da Anthropic para raciocínio e tarefas de longa duração. citeturn12view1turn9search3turn18view1turn16view1turn21search0

A evidência independente mais interessante encontrada vai ainda mais contra a heurística “modelo menor + esforço máximo”: numa bateria reproduzida a partir da Artificial Analysis, **Opus 5.5 em esforço menor frequentemente atingiu a mesma ou maior qualidade por tarefa que Sonnet 5.5 em esforço maior, por custo igual ou menor**. O caso mais extremo reportado foi Sonnet 5.5 `max`: índice 56 a US$ 7,60/tarefa versus Opus 5.5 `xhigh`: também 56 a US$ 3,46/tarefa. Isso é evidência de benchmark de modelo, não uma lei para Claude Code, mas é forte o bastante para derrubar a ideia de que “subir o esforço do modelo barato” seja sempre a estratégia econômica. citeturn21search16

Há também uma limitação concreta desta pesquisa: a ferramenta de busca impôs um limite de chamadas durante a execução. Consegui auditar extensivamente a documentação oficial, changelogs comportamentais, Terminal-Bench, anúncios técnicos e diversas fontes independentes, mas não consegui abrir diretamente algumas páginas que apareceram na indexação — em particular a página específica da Artificial Analysis por trás dos números reproduzidos pela BitsMinds e a matriz completa atual de invalidação de prompt cache. Por isso, esses resultados são classificados abaixo com a força de evidência correspondente, e campos não confirmados permanecem como **“não informado”**, em vez de serem preenchidos por inferência.

## Estado atual dos recursos e correções da hipótese anterior

### Modelos que realmente existem agora

A família que importa para seu uso corrente de Claude Code, em 3 de outubro de 2026, é **Fable 5.1, Opus 5.5, Sonnet 5.5 e Haiku 4.5**. A página atual da plataforma ainda lista Haiku 4.5 como o modelo Haiku vigente; no lançamento de Sonnet 5.5, a Anthropic anunciou Haiku 5.5 para “as próximas semanas”, portanto não deve ser tratado como já disponível nesta pesquisa. citeturn21search18turn21search7

| Modelo vigente | Papel documentado | Contexto / saída | Esforço disponível | Padrão relevante | API, US$/1M tokens | Observação crítica |
|---|---|---:|---|---|---:|---|
| **Fable 5.1** | raciocínio muito exigente, pesquisa e trabalho de longo horizonte | 1M / 128k | low, medium, high, xhigh, max | **High no Claude Code**; Medium no Cowork/Claude.ai segundo lançamento | **10 input / 50 output**; cache read US$0,25 | É o mais caro da linha geral e **não lidera automaticamente coding**. citeturn20search9turn11view3 |
| **Opus 5.5** | coding agentic, projetos complexos e knowledge work | 1M / 128k | low, medium, high, xhigh, max | **Medium** na documentação de effort | **4 / 20**; cache read US$0,20 | Adaptive thinking sempre ativo; é atualmente muito mais barato que Fable por token. citeturn12view0turn21search5turn21search0 |
| **Sonnet 5.5** | trabalho diário bem delimitado, bugs, documentos/design; equilíbrio velocidade/custo | 1M / 128k | low, medium, high, xhigh, max | **Medium no Claude Code/apps; High na API** | **2 / 10**; cache read US$0,20 | Lançado em 28/09/2026; portanto a evidência independente ainda é jovem. citeturn19search10turn19search22 |
| **Haiku 4.5** | alta velocidade, alto volume, tarefas auxiliares baratas | 200k / 64k | **não suporta `effort`** | não se aplica | **1 / 5**; cache read US$0,10 | Útil como trabalhador delimitado; não existe “Haiku high/max”. citeturn8search2turn21search18 |

Há uma tensão interessante na própria taxonomia da Anthropic. A página da plataforma chama Fable 5.1 de “Most capable” e o destina a tarefas muito exigentes ou de vários dias; ao mesmo tempo, o lançamento de **Opus 5.5 o coloca à frente de Fable 5.1 em Terminal-Bench 4.0, FrontierCode e CursorBench**. Portanto, “Fable > Opus > Sonnet” não é uma ordenação universal de capacidade. O eixo depende da tarefa, do harness e do esforço. citeturn21search18turn21search0

Isso tem uma consequência prática importante para você: **Fable deve ser tratado como uma especialização cara a ser justificada, e não como o botão “faça direito”**. Para desenvolvimento de aplicações, refatoração, bugs e trabalho agentic verificável, Opus 5.5 tem hoje evidência mais direta; Fable ganha plausibilidade quando o problema exige raciocínio excepcionalmente longo, pesquisa ou integração conceitual que já resistiu a Opus. A segunda frase é uma **inferência operacional**, não um resultado de benchmark abrangente. citeturn21search0turn20search9

### Esforço não é um orçamento e os nomes não são comparáveis entre modelos

A documentação atual define cinco níveis: `low`, `medium`, `high`, `xhigh` e `max`. O parâmetro controla o comportamento global de resposta — raciocínio, extensão da resposta e quantidade/tipo de chamadas de ferramentas — e **não** representa um número fixo de thinking tokens nem um teto de gasto. A própria Anthropic descreve `max` como a busca da capacidade máxima sem restrição de gasto de tokens; `xhigh` é orientado a tarefas especialmente longas; `high` a raciocínio/coding/agentic exigentes; `medium` ao equilíbrio; e `low` a tarefas simples ou muito sensíveis a eficiência. citeturn12view0turn12view2

Mais importante: **“high” em um modelo não equivale a “high” em outro, nem necessariamente à mesma coisa na versão seguinte**. A Anthropic diz explicitamente que os níveis de Sonnet 5.5 foram recalibrados em relação a Sonnet 5. Isso torna inválidas tabelas que tentam transformar esforço em multiplicadores universais do tipo “xhigh custa 2×” ou “max pensa N vezes mais”. citeturn12view1

Para Sonnet 5.5, a recomendação oficial é particularmente conservadora: começar em `medium` para trabalho agentic bem especificado, subir para `high` quando a tarefa se torna mais longa/difícil e usar `xhigh`/`max` **somente quando avaliações da sua tarefa mostrarem ganho**. Para Opus 4.8/4.7, a própria documentação já advertia que `max` podia custar significativamente mais com ganho pequeno e até “overthink” tarefas estruturadas. citeturn12view1

E agora existe evidência ainda mais direta de não monotonicidade: no lançamento de Sonnet 5.5, a Anthropic relata que **FrontierCode teve desempenho inferior em `max` comparado a `xhigh`**. Na investigação de dois casos feita com a Cognition, o maior esforço levou o modelo a acionar com mais frequência a skill de code review, causando timeout ou alterações adicionais fora do escopo. Isso é uma análise pequena — dois casos não provam causalidade geral — mas falsifica a premissa forte “mais esforço nunca piora”. citeturn9search3

### Max, `max`, Ultracode e o antigo `ultrathink` são coisas distintas

**Claude Max** é um plano de assinatura. A página de preços vigente oferece Max com **5–20× mais uso que Pro**, a partir de US$100/mês. Esses limites são de produto/assinatura e variam com a carga de trabalho. citeturn13search7turn15view5

**`max`** é um nível de esforço de determinados modelos. Você pode ter plano Max e usar `medium`; pode usar API pay-as-you-go e chamar `max`; e `max` **não constitui um teto financeiro**. citeturn12view0

**Ultracode**, na implementação atual, é principalmente um mecanismo de **orquestração automática de dynamic workflows**, e não um sexto nível de inteligência. O comando `/effort ultracode` liga a orquestração automática para tarefas substanciais no esforço em que a sessão estiver. Já iniciar com `claude --effort ultracode` ativa Ultracode e escolhe `xhigh` por padrão. A documentação marca esse comportamento para Claude Code **v2.1.203+**. citeturn6view0

O uso do texto `ultracode` no prompt humano pode solicitar um workflow apenas para aquela tarefa. A origem do pedido importa: a partir da mudança documentada em **v2.1.210**, esse gatilho é deliberadamente humano/interativo e não deve ser presumido para `-p`, tarefas agendadas, webhooks ou relays de PR; versões anteriores podiam se comportar de outra forma. Tutoriais anteriores a essa mudança estão, portanto, parcialmente obsoletos. citeturn6view0

**`ultrathink`**, por sua vez, é essencialmente um artefato histórico. Em abril de 2025, a inspeção do Claude Code relatada por Simon Willison mostrou que a string exata era reconhecida pelo cliente e associada a um orçamento de thinking de **31.999 tokens**. Esse era um comportamento específico do Claude Code antigo. Não encontrei `ultrathink` na documentação atual como nível de esforço suportado; o controle documentado em 2026 é `effort`/adaptive thinking, com Ultracode separado para orquestração. Portanto, reaplicar tutoriais de 2025 sobre `ultrathink` ao Claude Code atual é um erro. citeturn13search24turn12view0

### Superfícies, configurações e persistência

Claude Code atualmente existe em **terminal, IDE, desktop e browser**. Terminal, extensão do VS Code/JetBrains e Claude Code local no desktop leem a mesma família de arquivos de configuração local; sessões web rodam em outra máquina e apenas uma parte dessas configurações é aplicável. citeturn17search10turn15view3

A precedência atual inclui configurações gerenciadas pela organização, flags da linha de comando, `.claude/settings.local.json`, `.claude/settings.json` do projeto e `~/.claude/settings.json`. `/model` pode persistir a escolha de modelo para sessões futuras; o seletor também permite trocar apenas na sessão. `ANTHROPIC_MODEL` pode sobrescrever o modelo de arquivos de configuração. A documentação capturada inclui mudanças de comportamento em **v2.1.211**, **v2.1.242** e **v2.1.246**, mostrando que detalhes de configuração realmente mudam entre releases. citeturn15view3

Não consegui capturar, antes do limite da ferramenta de busca, uma tabela oficial atual completa que mapeie **todos os aliases informais** (`sonnet`, `opus`, etc.) para IDs versionados em cada plano/surface. Portanto, não vou fingir que um alias resolve eternamente para uma versão determinada. Para experimentos reprodutíveis, a escolha metodologicamente correta é registrar o **ID concreto**, por exemplo `claude-sonnet-5-5` ou `claude-opus-5-5`, além da versão do Claude Code. A própria documentação atual usa esses IDs concretos em exemplos. citeturn15view3turn19search22turn21search5

Também não obtive um único campo oficial dizendo “a última versão do Claude Code hoje é X”. A documentação capturada contém requisitos e mudanças até pelo menos **v2.1.281**, mas isso não prova que v2.1.281 seja o binário mais recente. Por isso, neste relatório as afirmações são marcadas como “documentação vigente em 03/10/2026” e, quando a Anthropic fornece um mínimo explícito, o número é registrado. citeturn16view5

**Correções que podem ser feitas com segurança em relação às hipóteses anteriores**, sem ter de supor o texto literal da resposta anterior:

| Hipótese | Auditoria |
|---|---|
| “Fable não existe / é codinome.” | **Errado em 2026. Fable 5.1 é modelo oficial atual.** citeturn20search9turn21search18 |
| “Fable é simplesmente melhor que Opus para coding.” | **Não sustentado.** Opus 5.5 supera Fable 5.1 em vários benchmarks de coding publicados pela própria Anthropic. citeturn21search0 |
| “`max` é o plano Max.” | **Errado.** Um é esforço; o outro é assinatura. citeturn12view0turn13search7 |
| “Ultracode é um esforço acima de max.” | **Errado/incompleto.** É orquestração de workflows; a forma CLI pode ligar xhigh como padrão. citeturn6view0 |
| “Ultracode = ultrathink.” | **Errado.** `ultrathink` é comportamento histórico; Ultracode atual é orquestração. citeturn13search24turn6view0 |
| “Mais esforço sempre melhora.” | **Refutado.** Há resultado FrontierCode em que `max` piorou versus `xhigh`. citeturn9search3 |
| “Os mesmos nomes de esforço significam o mesmo entre modelos.” | **Errado.** Os níveis são calibrados por modelo/versão. citeturn12view1 |
| “Haiku pode ser colocado em high/max.” | **Errado para Haiku 4.5.** Ele não suporta `effort`. citeturn8search2 |
| “Dividir sempre em janelas curtas economiza.” | **Não sustentado.** Há custo de histórico, mas também cache, reconstrução e perda de estado. citeturn18view0turn18view1 |
| “Mais agentes sempre aumentam qualidade.” | **Errado como regra.** Sessões paralelas multiplicam uso e podem conflitar. citeturn16view1 |
| “Uma instrução ‘não gaste mais que X’ impõe teto.” | **Errado.** Prompt é orientação; `effort` também não é teto financeiro. Controles precisam existir fora do texto. citeturn12view0turn14search21 |

## O que a evidência realmente mostra

A literatura atual sobre os modelos lançados nas últimas semanas é inevitavelmente desigual. Existe boa documentação de mecanismo e alguns benchmarks reprodutíveis, mas ainda há **pouca experimentação independente que altere simultaneamente modelo, esforço e Claude Code mantendo exatamente a mesma tarefa e harness**. Esse é o maior buraco da evidência.

Para não misturar coisas diferentes, usei quatro níveis:

**A — comparação controlada/reproduzível:** benchmark com tarefas, harness e resultados publicados.  
**B — teste prático observável:** procedimento e artefatos visíveis, mas sem controle suficiente.  
**C — relato de experiência:** prática real, porém sem contrafactual e repetição controlada.  
**D — alegação promocional/opinião:** fornecedor, launch partner ou autor sem demonstração adequada.

### Catálogo dos testes mais informativos

| Fonte e classe | Configuração conhecida | Tarefa / procedimento | Resultado principal | Tokens, custo e tempo | Não informado / limitação |
|---|---|---|---|---|---|
| **Terminal-Bench public leaderboard — A**; resultado Fable 5.1 em 01/09/2026 | **Fable 5.1 max**, harness **Claude Code** | tarefas reais executadas em terminal; leaderboard público | **57,9% ±3,8** | **2,7 bilhões de tokens; ~US$6,2 mil** no run listado | prompt individual, contexto médio e tempo total não expostos no resultado capturado. citeturn21search2 |
| **Terminal-Bench public leaderboard — A**; 24/07/2026 | **Opus 5 xhigh**, Claude Code | mesmo tipo de benchmark | **53,9% ±3,2** | **6,9 bilhões de tokens; ~US$6,1 mil** | é **Opus 5, não 5.5**; portanto não serve para declarar Fable 5.1 > Opus 5.5. citeturn21search2 |
| **Anthropic, Opus 5.5 launch — A/D híbrido** | Opus 5.5, **xhigh em Terminal-Bench 4.0**; outros benchmarks em max salvo nota | Terminal-Bench 4.0, FrontierCode 1.1, CursorBench 4.0 | TB4: **66,4% Opus 5.5 vs 55,8% Fable 5.1**; FrontierCode: **54,4 vs 50,3**; CursorBench: **57,8 vs 51,8** | custos dos runs não informados no trecho; API Opus 5.5 custa US$4/20 por MTok | fornecedor escolhe harness/settings; alguns benchmarks têm fallback de modelo por safeguards. Não é validação independente. citeturn21search0 |
| **Anthropic/Cognition, Sonnet 5.5 FrontierCode — B/D** | Sonnet 5.5, comparação `xhigh` × `max`, Claude Code/code-review skill envolvida | coding agentic | **max pior que xhigh**; em dois casos inspecionados, max acionou revisão adicional levando a timeout ou edição fora do escopo | não informado | só dois casos analisados causalmente; fornecedor. Ainda assim, é evidência contra monotonicidade. citeturn9search3 |
| **Artificial Analysis v4.3.2, números reproduzidos pela BitsMinds — A, porém extração secundária** | Sonnet 5.5 em **todos os cinco esforços**; comparação com Opus 5.5 | índice de inteligência com **10 avaliações**; avaliação de modelo/API, não Claude Code completo | Sonnet: **36/41/47/52/56** de low→max; Opus 5.5 chega a 58 | Sonnet: **US$0,41 / 0,59 / 1,08 / 2,74 / 7,60** por tarefa; tempo medido também | build pré-release de Sonnet teve bug de structured output; AA planejava rerun. Página direta do AA não foi aberta nesta pesquisa. citeturn21search16 |
| **Artificial Analysis via BitsMinds — comparação cruzada — A/secundária** | Opus low/high/xhigh versus Sonnet medium/xhigh/max | mesma bateria | Opus **low 42 / US$0,55** vs Sonnet **medium 41 / US$0,59**; Opus **high 54 / US$1,82** vs Sonnet **xhigh 52 / US$2,74**; Opus **xhigh 56 / US$3,46** vs Sonnet **max 56 / US$7,60** | Sonnet medium ~6 s; Opus low ~18,5 s segundo relatório; Sonnet é muito mais responsivo | é benchmark geral; custo e latência reais no Claude Code podem diferir fortemente pelo uso de ferramentas/contexto. citeturn21search16 |
| **Addy Osmani, 15/06/2026 — C/B** | Claude Code e Codex lado a lado | primeira passagem sobre PRs, triagem e risco | agentes úteis para **triagem e leitura inicial**; decisão de merge continua humana | não informado | relato prático, não benchmark controlado; modelos/settings não detalhados no trecho. citeturn17search32turn13search19 |
| **Relatos de Agent Teams — C** | Claude Code teams/subagents em produção | coordenação paralela | relatos descrevem comunicação extra, notificações no contexto do lead, custo e problemas de merge | não informado | evidência anedótica; útil para gerar hipóteses, não para quantificar benefício. citeturn7search6turn7search21 |
| **Simon Willison/Hacker News, abril/2025 — A para mecanismo histórico** | Claude Code antigo | inspeção/deobfuscation do cliente | string `ultrathink` mapeava para budget de thinking de 31.999 | não informado | descreve **2025**, não comportamento atual. citeturn13search24 |

Uma questão metodológica precisa ser destacada: **Artificial Analysis, Terminal-Bench e Claude Code não medem a mesma coisa**. Um teste de API mede essencialmente modelo + prompt/harness da avaliação. Um row de Terminal-Bench marcado “Claude Code” mede modelo **mais** o agente, ferramentas, system prompt e políticas do Claude Code. Trocar apenas o modelo não garante que o restante do harness tenha permanecido invariável. citeturn21search2turn18view1

Da mesma forma, um benchmark que reporta “custo por tarefa” não mede seu custo de conclusão verificada. Seu trabalho real inclui ler o repositório, executar testes, fazer nova tentativa, rever a diff, corrigir regressões e possivelmente gastar tempo humano. Um modelo que custa o dobro por token pode terminar numa tentativa; outro barato pode gerar três ciclos de correção. A evidência atual sustenta medir **custo até sucesso verificado**, não preço nominal por token isoladamente. citeturn21search16turn21search0

### O resultado mais relevante sobre modelo versus esforço

Os dados atribuídos à Artificial Analysis fornecem exatamente a comparação que geralmente falta:

| Comparação na mesma bateria | Índice | Custo/tarefa | Leitura correta |
|---|---:|---:|---|
| Sonnet 5.5 `medium` | 41 | US$0,59 | baseline barato/rápido |
| **Opus 5.5 `low`** | **42** | **US$0,55** | ligeiramente melhor e ligeiramente mais barato no benchmark, porém bem mais lento |
| Sonnet 5.5 `xhigh` | 52 | US$2,74 | grande salto sobre high |
| **Opus 5.5 `high`** | **54** | **US$1,82** | melhor resultado e menor custo nesta bateria |
| Sonnet 5.5 `max` | 56 | US$7,60 | esforço muito caro |
| **Opus 5.5 `xhigh`** | **56** | **US$3,46** | mesmo índice por menos da metade do custo |
| Opus 5.5 `max` | 58 | US$5,98 | topo da comparação reproduzida |

Esses números vêm de uma fonte secundária reproduzindo a Artificial Analysis e o Sonnet testado era pré-release, por isso **não devem virar uma política rígida**. Mas eles são fortes o bastante para justificar uma política de escalonamento na qual você testa **trocar de modelo antes de empurrar Sonnet de high até max**. citeturn21search16

Há ainda o fator velocidade. No mesmo relato, Sonnet 5.5 `medium` completava a resposta em cerca de seis segundos contra aproximadamente 18,5 s de Opus 5.5 `low`. Portanto, “melhor custo de tokens” e “melhor experiência interativa” podem apontar para modelos diferentes. citeturn21search16

Isso é particularmente relevante para seu aprendizado de Python: em sessões interativas nas quais você pergunta, executa, recebe erro, corrige e pergunta de novo, **latência é parte do custo cognitivo**. Um Opus teoricamente mais eficiente por score pode ser uma escolha pior para pequenos ciclos de aprendizado. Essa última conclusão é uma aplicação prática dos dados de latência, não um benchmark específico de ensino.

## Matriz provisória de tarefa, modelo e esforço

A matriz abaixo não deve ser transformada ainda em regras do `CLAUDE.md`. Ela é uma **hipótese de operação sustentada pelo conjunto de evidências**, com indicação explícita de quando aumentar esforço, trocar modelo ou melhorar a especificação.

| Cenário | Configuração inicial candidata | Primeiro sinal de insuficiência | Escalonamento racional | Multiagente | Verificação obrigatória | Confiança |
|---|---|---|---|---|---|---|
| **Alteração mecânica pequena** | Sonnet 5.5 `low`–`medium`; Haiku 4.5 para busca/classificação auxiliar | começa a alterar arquitetura, não entende dependência local, falha teste | primeiro melhorar escopo/prompt; depois Sonnet `high`; Opus raramente necessário | geralmente não | testes afetados + diff restrita | **Alta** para evitar xhigh/max; docs recomendam low/medium para tarefas simples. citeturn12view0turn12view1 |
| **Implementação com especificação detalhada** | Sonnet 5.5 `medium` | falhas em invariantes, múltiplos módulos ou testes após tentativa | Sonnet `high`; se persistir erro de integração/raciocínio, Opus 5.5 `medium/high` antes de Sonnet `max` | subagente apenas para pesquisa/testes independentes | acceptance tests da especificação | **Moderada–alta**; alinhada ao guidance oficial e ao sweep independente. citeturn12view1turn21search16 |
| **Feature com requisitos incompletos** | Opus 5.5 `medium` ou Sonnet `high` para exploração curta | modelo preenche lacunas silenciosamente ou inventa regra de negócio | parar implementação, transformar ambiguidades em decisões; Opus `high` para comparar opções | subagentes podem mapear alternativas, mas não decidir regra de negócio | lista explícita de suposições + testes de regra | **Moderada**; ambiguidade exige julgamento, mas não há benchmark específico. citeturn21search7turn21search0 |
| **Arquitetura / escolha entre alternativas** | Opus 5.5 `high` | plano superficial, não examina restrições ou trade-offs | Opus `xhigh`; Fable 5.1 `high` somente se o problema realmente permanecer frontier/long-horizon | 2–3 análises independentes podem ajudar se perspectivas forem distintas | ADR/decision record com critérios e contraexemplos | **Moderada**; Opus/Fable têm posicionamento oficial, mas poucas comparações independentes de arquitetura. citeturn21search0turn20search9 |
| **Bug local reproduzível** | Sonnet 5.5 `medium` | primeira hipótese falha; causa não é local | `high`; se o problema atravessa estado/tempo/módulos, Opus `high` | normalmente não; subagente para examinar logs pode poupar contexto | reproducer antes/depois + regression test | **Alta** para começar barato; Sonnet 5.5 é explicitamente direcionado a bugs. citeturn21search7 |
| **Bug distribuído/temporal** | Opus 5.5 `high` | investigação entra em ciclo, várias hipóteses sem eliminação | primeiro exigir árvore de hipóteses/evidências; depois `xhigh`; Fable só após falha real | investigação paralela de subsistemas pode ajudar; edições paralelas tendem a atrapalhar | reproducer, logs, invariantes temporais, teste regressivo | **Moderada**; recomendação é inferência a partir de capacidade agentic e isolamento de subagentes. citeturn21search0turn3view1 |
| **Refatoração/migração multi-módulo** | Sonnet `high` ou Opus `medium/high` conforme acoplamento | regressões e alterações fora de escopo | trocar para Opus antes de Sonnet max; workflow se a migração puder ser particionada | workflow/`/batch` quando arquivos são separáveis; worktrees | suite completa + lint/typecheck + invariantes de API | **Moderada–alta** para orquestração; dynamic workflows foram feitos explicitamente para grandes migrações. citeturn16view0turn16view1 |
| **Code review / performance / segurança** | Opus 5.5 `high`; Sonnet `high` para triagem | reviewer concorda automaticamente com implementação ou não reproduz risco | segunda revisão independente, ferramenta estática/testes; `xhigh` em casos realmente críticos | paralelo pode ampliar cobertura, mas revisores do mesmo modelo não são independentes | execução de testes/analisadores; decisão humana para riscos importantes | **Moderada**; agentes parecem úteis para triagem, não para terceirizar merge/trust. citeturn17search32 |
| **UI e conferência visual** | Sonnet 5.5 `medium/high` | código “parece correto” mas interface real não corresponde | melhorar especificação visual antes de subir modelo; Opus se problema for arquitetura/estado, não estética isolada | pouco benefício de teams | browser/Chrome, screenshots, console, testes de interação | **Moderada**; Anthropic posiciona Sonnet 5.5 fortemente para design, mas isso é vendor evidence. Chrome integration dá verificação real. citeturn21search7turn14search5 |
| **Importação XLS/XLSX/CSV/PDF e reconciliação** | Sonnet `high` com regras formais; Opus `high` se schemas/identidade forem ambíguos | perda de linhas, duplicatas ou interpretação inconsistente | **não** subir esforço antes de criar fixtures e invariantes; só depois trocar modelo | subagentes úteis para perfilar formatos diferentes; integração central única | contagens, hashes/IDs, totais, duplicações, fixtures e golden files | **Moderada-baixa** porque não encontrei benchmark específico deste domínio |
| **Trabalho autônomo prolongado** | Sonnet `medium/high` se especificação/testes fortes; Opus `high` se julgamento domina | loops de reparo, escopo crescendo, mesma falha reaparece | aumentar estrutura e checkpoints antes de esforço; xhigh somente se raciocínio é gargalo | workflow se paralelizável; sessão única se dependências forem fortes | critérios executáveis de conclusão | **Moderada**; duração em horas não justifica effort alto por si só. citeturn12view0turn16view0 |

### Aplicações propostas aos seus projetos

**Aplicação proposta — aplicativo hospitalar.** Pedido: “Paciente é identificado por RA fixo; cada internação é distinta; leito pode mudar; a partir do quarto dia de longa permanência deve existir ação diária. Implemente e teste transições de internação, alta, reinternação e troca de leito.” A dificuldade real não é escrever CRUD; é preservar **identidade versus episódio temporal** e impedir que estado de uma internação contamine outra. Minha candidata seria **Opus 5.5 `high`** se a lógica ainda precisa ser descoberta, ou **Sonnet 5.5 `medium/high`** se você já fornecer uma tabela formal de estados. O melhor investimento provavelmente é formalizar os invariantes antes de subir para `xhigh`. A verificação deveria incluir testes de reinternação com mesmo RA, mudança de leito, D+3/D+4, alta e reabertura.

**Aplicação proposta — dashboard financeiro.** Pedido: “Importe planilhas de fontes diferentes, evite duplicação e reconcilie o valor final com a fonte.” A dificuldade real é definir **identidade de transação e idempotência**, não produzir a tela. Começaria em Sonnet 5.5 `high` com fixtures contendo duplicatas deliberadas, arredondamento, estorno e linhas reimportadas. Se o modelo não consegue formular um algoritmo consistente de matching, trocaria para Opus 5.5 `high`; não usaria `max` para compensar ausência de regra de deduplicação.

**Aplicação proposta — filtros/chips/formulários.** Pedido: “Adicionar chips de filtro, preservar seleção durante atualização, limpar filtros com uma ação e não alterar os resultados de backend.” Isso é bem delimitado e visual. **Sonnet 5.5 `medium`** é a hipótese forte, com inspeção real pelo browser. Subir para Opus porque um chip ficou desalinhado seria usar inteligência como substituto de feedback visual — uma maneira cara de resolver o problema errado. A integração oficial de Claude Code com Chrome permite testar páginas, preencher formulários e inspecionar console, tornando verificação visual/funcional mais informativa que effort extra. citeturn14search5

**Aplicação proposta — bug que atravessa Apps Script, importação e UI.** Se um valor aparece duplicado depois de importações sucessivas, o pedido deveria ser de **investigação**, não “conserte a duplicação”. Opus 5.5 `high` com um plano explícito de rastrear identidade desde arquivo → parser → armazenamento → API → renderização tende a ser mais racional do que cinco agentes editando cada camada simultaneamente. Uma vez localizada a causa, Sonnet pode executar a correção mecânica.

A regra crítica emergente é:

> **Aumentar qualidade da especificação geralmente deve preceder aumentar effort quando o erro decorre de ambiguidade; aumentar modelo/effort é mais defensável quando a especificação está boa e ainda assim o raciocínio falha.**

Isso é inferência operacional, mas é consistente com o fato de que esforço maior acrescenta planejamento/tool calls, não informação ausente, e pode inclusive ampliar alterações fora de escopo. citeturn12view2turn9search3

## Orquestração, Ultracode e vários agentes

Claude Code tem hoje várias formas distintas de paralelismo, e misturá-las produz conselhos ruins. A própria documentação lista **subagentes, Agent View, agent teams, dynamic workflows e Projects** como mecanismos diferentes. citeturn16view0

| Mecanismo | Quem coordena | Contexto | Comunicação | Isolamento de edição | Melhor caso |
|---|---|---|---|---|---|
| **Sessão normal** | Claude + você | um contexto principal | não se aplica | working tree atual | tarefa fortemente acoplada |
| **Subagente** | Claude principal | fresh context; devolve resumo | retorno ao chamador | pode ter worktree | pesquisa/logs/leitura que poluiria contexto principal |
| **Agent View** | você | sessões independentes | resultado volta principalmente a você; messaging pode ligar sessões | sessões despachadas usam worktrees | várias tarefas independentes |
| **Agent Teams** | um lead Claude | sessões independentes | teammates podem conversar diretamente e compartilhar tasks | **não têm worktree isolation automático** | partes distintas que precisam se coordenar |
| **Dynamic workflow** | script gerado/definido | vários subagentes | coordenação programática | depende da configuração | migração grande, auditoria, fan-out + verificação |
| **Projects cloud** | você + Claude | múltiplos threads | coordenação via projeto | cloud/local conforme modo | trabalho por dias/semanas e execução mesmo com sua máquina desligada |

citeturn16view0turn16view1

### Subagentes: o melhor primeiro degrau de paralelismo

Subagentes recebem **contexto fresco e isolado**, system prompt, ferramentas/permissões próprias e devolvem o resultado ao chamador. Eles são particularmente valiosos quando uma investigação despejaria centenas de linhas de logs, resultados de busca ou arquivos no contexto principal. Também podem usar modelos mais baratos para trabalho auxiliar. citeturn3view1turn6view2

Esse isolamento tem custo: o subagente **não sabe automaticamente o que a sessão principal já leu ou raciocinou**. É necessário fornecer uma delegação suficientemente informativa; CLAUDE.md e estado do repositório podem ser carregados, mas isso não é equivalente a herdar toda a conversa. Forked subagents são a exceção que pode herdar contexto. citeturn6view2turn16view1

Na documentação atual, o limite padrão é **20 subagentes simultâneos** por sessão e a profundidade padrão de nesting passou a **três níveis abaixo do principal a partir de v2.1.219**; versões imediatamente anteriores tiveram limites diferentes. Esse detalhe é um ótimo exemplo de por que vídeos/tutoriais sem versão são perigosos. citeturn6view2

Minha interpretação: para seus projetos, **subagente deve ser o paralelismo padrão antes de Agent Teams**. “Investigue a regra de importação nos módulos A/B/C e me traga evidências, sem editar” é uma boa delegação. “Você implementa backend enquanto outro agente altera o mesmo schema e um terceiro mexe no frontend que depende desse schema” é um convite a sincronização e retrabalho.

### Agent Teams: comunicação é capacidade e também overhead

Agent Teams cria sessões Claude independentes, com um líder, lista compartilhada de tarefas e mensagens diretas entre teammates. O recurso é documentado como **experimental e desabilitado por padrão**. citeturn16view0turn7search0

O ponto mais importante para desenvolvimento real: **teammates não são automaticamente isolados em worktrees**. A documentação manda particionar o trabalho para que cada teammate possua conjuntos diferentes de arquivos. citeturn16view1

Isso torna Agent Teams atraente para:

- backend e frontend com contrato já congelado;
- investigações independentes de hipóteses;
- revisão de áreas distintas;
- pesquisa em fontes realmente separáveis.

Mas pouco atraente quando A depende da decisão que B ainda vai tomar. Nesse caso, a aparente paralelização cria esperas, mensagens, reinterpretações e merge.

Existem relatos de usuários em produção dizendo que comunicação entre agentes, mensagens ociosas e merges consumiram tokens sem benefício proporcional; um autor relatou ter abandonado teams em parte por custo e problemas de integração. Eles são úteis como **sinal de risco**, mas não devem ser tratados como ensaio controlado. citeturn7search6turn7search21

### Dynamic workflows e o que Ultracode realmente faz

Dynamic workflows são scripts de orquestração que podem lançar muitos subagentes, controlar estágios e cruzar resultados. A Anthropic os indica explicitamente para **auditorias de codebase, migrações grandes e pesquisa com cross-checking**. Estão disponíveis nos planos pagos, API e provedores cloud; usuários Pro precisam habilitá-los em `/config`. citeturn6view0

Existe ainda `/deep-research`, workflow empacotado que distribui buscas, cruza evidências e filtra afirmações não verificadas. Isso mostra a ideia arquitetural: workflow não é “um Claude mais inteligente”; é **decomposição + fan-out + agregação + verificação programada**. citeturn6view0

Com Ultracode ativo, **uma solicitação pode virar vários workflows**, consumir mais tokens e atingir limites da assinatura mais cedo. A documentação também diz que ele remove alguns freios: o aviso de workflow grande e certos passos de aprovação inicial são pulados, e o limite normal de subagentes concorrentes não é aplicado às execuções do Agent tool no contexto Ultracode. Isso torna particularmente errada a ideia “deixo Ultracode ligado porque é sempre melhor”. citeturn6view0

Outra restrição importante para autonomia: um workflow **não oferece diálogo humano normal no meio da execução**, exceto eventos como permissões/usage limits. Se você precisa aprovar “primeiro analise, depois me mostre o plano, só então migre”, são conceitualmente fases/workflows separados. citeturn6view0

### Por que mais revisores não produzem independência estatística

Dois agentes do mesmo modelo, com o mesmo repositório, as mesmas instruções e hipóteses semelhantes **podem produzir erros correlacionados**. Não encontrei um experimento Claude Code atual que quantifique essa correlação, então esta é uma inferência metodológica. O simples voto “três agentes concordaram” não transforma três amostras correlacionadas em verdade.

Para revisão robusta, diversidade de **método** é frequentemente mais importante que diversidade de agentes: teste unitário, type checker, linter, consulta SQL, propriedade/invariante, screenshot, parser independente ou segundo modelo. Addy Osmani chega a uma conclusão prática semelhante para code review: o agente é valioso para triagem, mas a decisão de merge não deve ser confundida com a primeira opinião gerada. citeturn17search32

Para seu hospital, por exemplo, pedir a três agentes “essa regra de longa permanência está correta?” é inferior a criar casos formais:

`mesmo RA + alta + nova internação`  
`D+3 sem ação obrigatória`  
`D+4 com ação obrigatória`  
`troca de leito sem reiniciar tempo`  
`nova internação reiniciando o contador`

e fazer qualquer agente provar seu código contra esses casos.

## Sessões longas, contexto, cache e handoff

Esta é provavelmente a parte em que o conselho do próprio Claude de “abrir janelas menores para economizar tokens” precisa de mais correção.

**Uma janela longa em horas não custa por ser longa em horas.** O que importa é quantas chamadas ao modelo ocorrem, quanto contexto cada chamada recebe, quanto foi cacheado, quanto o modelo gera/pensa, quantas ferramentas/agentes são acionados e quanto precisa ser reconstruído depois. citeturn18view1

### O que é reapresentado ao modelo

No modelo de conversação da API, uma nova chamada contém o histórico anterior aplicável mais a nova mensagem. System prompt, mensagens, tool results, imagens/documentos e definições de ferramentas contam para a janela. Assim, conforme a conversa cresce, o input lógico de cada turno também cresce. citeturn18view1

Com os modelos atuais principais, a janela é **1 milhão de tokens**; isso não significa que usar 900 mil seja uma boa ideia. A própria documentação alerta para degradação de precisão/recall à medida que o contexto cresce, o chamado “context rot”, e enfatiza que curadoria é tão importante quanto capacidade. citeturn18view1

No Claude Code, `/context` mostra o consumo atual por categoria e oferece sugestões de otimização. O cliente compacta automaticamente ao se aproximar do limite; você também pode executar `/compact` com foco e `/autocompact` com um limiar configurado. A documentação sugere explicitamente `/clear` quando se troca para um trabalho **não relacionado**, justamente porque a conversa antiga consome contexto e tokens em mensagens futuras. citeturn18view0

Isso sustenta **“limpe quando muda de assunto”**, mas não sustenta “abra uma janela nova a cada X mensagens”.

### Prompt cache muda radicalmente a interpretação do custo

Prompt caching não remove tokens da janela. Um prefixo cacheado **continua contando para o contexto**, mas a cobrança de leitura pode ser muito menor do que reprocessar input normal. A API separa `input_tokens`, `cache_read_input_tokens` e `cache_creation_input_tokens`. citeturn18view1

Na precificação atual, Sonnet 5.5 custa US$2/MTok de input e apenas **US$0,20/MTok de cache read**; Opus 5.5 custa US$4/MTok de input, mas também US$0,20/MTok de cache read. Sonnet tem cache write de 5 minutos a US$2,50/MTok e de 1 hora a US$4/MTok; Opus 5.5 tem 5-minute write a US$5/MTok e 1-hour write a US$8/MTok. citeturn19search22turn21search11

Exemplo estritamente de API: reaproveitar 100 mil tokens cacheados de Sonnet 5.5 custa aproximadamente **US$0,02 por leitura**, contra US$0,20 se fossem input normal; para Opus 5.5, os mesmos 100 mil cacheados custam aproximadamente US$0,02 contra US$0,40 de input normal. Isso não quer dizer que toda conversa longa obtenha hit perfeito nem que a assinatura Max contabilize exatamente esses dólares.

Há outro detalhe pouco conhecido: **mudar o `effort` top-level invalida o prompt cache**. Para Fable 5.1, Mythos 5.1, Opus 5.5, Opus 5 e Sonnet 5.5 existe um beta de effort por mensagem que pode preservar cache em certas conversas, mas isso não equivale ao comportamento genérico do Claude Code para todo usuário. citeturn12view2

A documentação atual possui uma matriz específica de ações que invalidam o prefixo cacheado, mas não consegui capturá-la integralmente antes do limite de buscas. Portanto, **não vou afirmar como fato que toda alteração de ferramenta, instrução ou modelo mantém/quebra cache de uma forma determinada**. A regra segura para avaliação é registrar cache hits reais em vez de supor.

### Pensamento também fica no histórico nos modelos novos

Nos atuais Opus, Sonnet ≥4.6 e Fable, blocos anteriores de thinking podem permanecer no contexto. Eles são cobrados como output quando produzidos e, quando preservados em turnos futuros, passam a fazer parte do input correspondente. Haiku e modelos antigos têm comportamento diferente, frequentemente removendo thinking anterior. citeturn18view1

Logo, `max` numa sessão muito longa pode ter dois efeitos: gastar mais no turno atual e produzir mais material que participa da conversa futura. Isso reforça por que “tenho 1M tokens, então deixarei max ligado” não é uma estratégia de eficiência. citeturn18view1turn12view0

### Compactação é diferente de sessão nova

Quando o contexto enche, Claude Code compacta e mantém a sessão andando. `/compact` permite orientar o resumo; `/rewind` pode resumir partes específicas. Os checkpoints permanecem associados à conversa e podem ser usados depois de retomar a sessão. citeturn18view0turn16view3

Compactar não equivale a preservar literalmente cada detalhe no contexto ativo. Há uma transformação de histórico em representação resumida; portanto, informação não considerada relevante pode ter menos saliência. A vantagem é manter a continuidade operacional e liberar espaço. Para longos debug sessions, a própria documentação recomenda resumo focado. citeturn16view3turn18view0

Uma sessão nova, por outro lado, começa com **novo contexto**. A persistência vem de arquivos como `CLAUDE.md`/`AGENTS.md`, auto memory e estado do próprio repositório. A auto memory é carregada entre sessões, com os primeiros **200 lines ou 25 KB** segundo a documentação atual. citeturn15view1

Essa diferença explica por que “nova janela economiza tokens” pode ser verdadeira e simultaneamente piorar o custo total: você eliminou 200 mil tokens de conversa irrelevante, mas talvez force Claude a reler dez arquivos, redescobrir uma hipótese de bug e repetir três testes que a sessão anterior já entendeu.

### Comparação das cinco estratégias solicitadas

Não encontrei um estudo controlado atual que execute **o mesmo projeto Claude Code** múltiplas vezes nas cinco estratégias abaixo. Portanto, a tabela distingue mecanismo comprovado de inferência prática.

| Estratégia | Vantagem | Custo/risco | Quando tende a ganhar | Confiança |
|---|---|---|---|---|
| **A. Sessão contínua** | estado de raciocínio e decisões continuam disponíveis; cache pode baratear prefixos | contexto cresce, logs/hipóteses antigas contaminam, compaction eventual | problema único e fortemente encadeado, especialmente debugging | **Moderada**. Mecânica é documentada; superioridade depende do projeto. citeturn18view1 |
| **B. Sessões por fase** | remove contexto irrelevante entre planejar/implementar/verificar; reduz contaminação | cada fase precisa reconstruir estado; handoff pode perder decisões | fases têm contratos claros e pouca dependência tácita | **Moderada-baixa**, por falta de A/B controlado |
| **C. Sessão contínua + compactação/checkpoints** | conserva continuidade e controla janela; permite rewind | resumo pode omitir detalhes; compaction não corrige suposições ruins | longa tarefa coerente com momentos naturais para resumir | **Moderada–alta** como mecanismo oficial. citeturn18view0turn16view3 |
| **D. Sessões novas + handoff persistido no repo** | estado auditável/reproduzível; excelente para retomada e mudança de modelo/agente | overhead de manter handoff; conhecimento que nunca foi escrito é perdido | trabalho de horas/dias, passagem de fase ou interrupção prevista | **Moderada**; Anthropic recomenda state artifacts para agents multi-session. citeturn18view2 |
| **E. Sessão principal + subagentes delimitados** | logs/pesquisa grande ficam fora do contexto principal | chamadas extras + bootstrap de contexto + potencial duplicação | investigações paralelizáveis e leituras volumosas | **Alta para isolamento, moderada para economia líquida**. citeturn3view1turn16view1 |

Minha conclusão provisória é que **C e E são melhores candidatas a “default sofisticado” do que abrir janelas arbitrariamente curtas**: sessão coerente, compactada em pontos semânticos, e subagentes para material volumoso. **D** torna-se superior quando a duração atravessa uma interrupção real, mudança de fase, mudança de responsável ou execução overnight que precisa sobreviver a perda de contexto.

### Critérios observáveis para decidir quando começar outra sessão

Não há base para “depois de 20 mensagens” ou “a cada duas horas”. Há, porém, sinais operacionais melhores:

**Continue** quando a tarefa depende fortemente de hipóteses que foram refinadas durante a investigação; `/context` ainda está saudável; o agente não repete perguntas/leituras; e a conversa contém decisões difíceis de reconstruir.

**Compacte** quando a investigação antiga está resolvida, muitos logs/tool outputs já perderam utilidade, mas o objetivo e as decisões continuam os mesmos. `/compact focus on...` existe exatamente para isso. citeturn18view0

**Use `/clear` ou sessão nova** quando mudou de tarefa, as hipóteses antigas passaram a induzir o agente ao erro, o repositório já contém estado suficiente para recomeçar ou o contexto está dominado por material sem utilidade atual. A Anthropic recomenda explicitamente clear entre trabalhos não relacionados. citeturn18view0

**Crie handoff** quando outro agente/sessão precisa saber “onde estamos” sem reconstruir tudo: objetivo, decisões, arquivos alterados, testes passados/falhos, hipóteses rejeitadas, próximo passo e condições de conclusão. Isso transforma estado tácito em estado do projeto.

Portanto, a afirmação do Claude de que “janelas curtas economizam tokens” é **condicionalmente verdadeira**. Ela é verdadeira quando remove histórico caro e irrelevante. Torna-se uma simplificação ruim quando o custo de reconstruir o estado excede o histórico economizado ou quando a nova sessão reincide em erros já eliminados.

## Autonomia por horas e durante a noite

Duração desejada e dificuldade são variáveis diferentes. **Não há razão técnica para escolher Fable/max simplesmente porque você quer que o trabalho dure oito horas.** Effort descreve quanto raciocínio e trabalho o modelo dedica às decisões; tempo de execução decorre do número de etapas, ferramentas, agentes, testes e dependências. citeturn12view0

Para trabalho overnight, a pergunta correta é: **o trabalho é serial ou paralelizável, e o critério de término é executável?**

Uma refatoração cujo passo 8 depende dos resultados arquiteturais do passo 7 favorece uma sessão principal/coordenador. Uma migração de 500 arquivos com transformação bem definida e testes automatizados favorece workflow/`/batch`. Cinco investigações independentes sobre módulos diferentes favorecem sessões/worktrees ou Agent View. citeturn16view0turn16view1

### O que realmente pode continuar rodando

O Claude Code web/Projects oferece trabalho em cloud e é explicitamente pensado para projetos com múltiplos threads que podem continuar enquanto sua máquina está desligada; Projects estava em beta pública para Pro e Max na documentação capturada. citeturn16view0

Uma sessão local no terminal/IDE depende, por definição, do processo local, rede, autenticação, energia e ausência de suspensão do computador. “Rodar durante a noite” no terminal e “rodar na nuvem enquanto o notebook dorme” não são a mesma coisa. A página do produto diferencia Claude Code local e tarefas longas/assíncronas disponíveis nas superfícies atuais. citeturn17search2turn17search10

Tarefas agendadas são ainda outra categoria. A documentação distingue uma **routine** que inicia sessão conforme um schedule na cloud de um comando shell em background — que é apenas um processo shell e **não** um agente — e das sessões agentes em background monitoradas por `claude agents`. citeturn16view1

### Para uma noite inteira, uma boa especificação vale mais que `max`

O pacote mínimo que torna a autonomia plausível é:

**Objetivo verificável:** não “melhore o dashboard”, mas “elimine duplicatas sob estes quatro casos; mantenha total reconciliado; todos os testes devem passar”.

**Escopo explícito:** arquivos/módulos permitidos e coisas que não devem ser redesenhadas.

**Invariantes:** por exemplo, no hospital, RA identifica paciente, `admission_id` identifica internação, troca de leito não cria internação, nova internação reinicia duração.

**Critérios de aceitação executáveis:** testes, lint, typecheck, fixtures, screenshots, comparação de totais.

**Política de falha:** após N tentativas distintas sobre o mesmo teste, registrar bloqueio e parar aquela linha de trabalho. Isso deve idealmente estar codificado no workflow/script, não depender apenas do modelo lembrar uma frase.

**Checkpoint:** commits/branch ou arquivo de status com o que foi feito e próximo passo.

**Prova de término:** comandos executados, resultado dos testes, diff final, itens deliberadamente não resolvidos.

Essas são aplicações práticas; não existe um benchmark demonstrando que exatamente essa receita maximiza Claude Code.

### Controle real versus pedido textual

Este ponto merece tratamento quase paranoico, porque é onde “autonomia” vira facilmente “eu disse para o Claude não fazer isso e ele fez”.

| Mecanismo | É controle real? | Comentário |
|---|---|---|
| `permissions.allow/ask/deny` | **Sim, software** | Claude Code aplica regras de ferramentas/ações. citeturn14search21turn15view3 |
| managed settings | **Sim** | configurações organizacionais podem ter precedência. citeturn15view3 |
| hook que rejeita determinada operação | **Sim, se implementado corretamente** | mais forte que “não faça X” no prompt |
| worktree/branch | **Sim para isolamento de arquivos** | evita que sessões paralelas editem o mesmo checkout; não garante código correto. citeturn15view4 |
| testes/CI obrigatórios | **Sim como gate de propriedades testadas** | não provam propriedades que o teste não cobre |
| limite padrão de 20 subagentes | **Sim normalmente** | **Ultracode é exceção** para Agent-tool subagents. citeturn6view2turn6view0 |
| limites de assinatura/rate limit | **Sim, externo ao modelo** | podem interromper/atrasar execução |
| “não gaste mais de US$10” em prompt | **Não é teto financeiro** | é instrução ao agente |
| “pare após três tentativas” em prompt | **Orientação, não garantia** | script/workflow com contador é mais forte |
| “não altere arquivos fora deste módulo” em prompt | **Orientação** | permission/hook/worktree é enforcement melhor |
| `effort=max` | **Não é limite; é o oposto** | permite maior gasto de tokens. citeturn12view0 |

Outro detalhe relevante: os checkpoints do Claude Code não são substituto completo de Git. Alterações feitas por comandos Bash e muitas edições de subagentes não são restauradas pelo mecanismo de rewind normal; a documentação recomenda usar Git para esses casos. citeturn16view4

### Sessão longa, workflow ou handoffs?

Minha síntese provisória:

| Trabalho | Melhor candidato | Por quê |
|---|---|---|
| bug complexo com hipótese que vai sendo refinada | **sessão principal longa + compaction** | conhecimento acumulado é ativo |
| auditoria de muitos módulos sem edição simultânea | **main + subagentes** | isola pesquisa volumosa |
| migração mecânica de centenas de arquivos | **dynamic workflow ou `/batch` + worktrees** | paralelização é real e verificação automatizável |
| feature com decisões arquiteturais no meio | **fases com handoffs/checkpoints** | você precisa de gate humano entre decisões |
| backlog de tarefas independentes | **Agent View/worktrees ou Projects** | supervisão por exceção |
| projeto de vários dias que deve sobreviver à máquina desligada | **Projects/cloud + estado persistido** | continuidade não depende do processo local |
| módulos fortemente dependentes editados simultaneamente | **evitar team grande** | custo de sincronização tende a destruir o paralelismo |

A confiança é **alta** na distinção mecânica entre esses modos, porque está documentada; é **moderada** em afirmar qual produz menor custo total, porque faltam A/B tests independentes representativos. citeturn16view0turn16view1

## Custo total, confiança e protocolo pessoal

### API: preço nominal atual

Para API, a diferença entre modelos é grande:

| Modelo | Input / MTok | Output / MTok | Cache read / MTok |
|---|---:|---:|---:|
| Haiku 4.5 | US$1 | US$5 | US$0,10 |
| Sonnet 5.5 | US$2 | US$10 | US$0,20 |
| Opus 5.5 | US$4 | US$20 | US$0,20 |
| Fable 5.1 | US$10 | US$50 | US$0,25 |

citeturn3view2turn19search22turn21search0turn11view3turn8search2

Batch API tem desconto de 50% em input/output nas condições documentadas. O **fast mode** de Opus 5.5 eleva preço para US$8/MTok input e US$40/MTok output, em troca de velocidade anunciada de aproximadamente 2,5×; no Claude Code ele está em research preview e pode aparecer em planos consumption-based ou via usage credits em assinaturas. citeturn3view2turn17search2

Esses preços dizem pouco sozinhos. Por exemplo, Fable custa 5× Sonnet no output nominal. Se Fable resolve uma tarefa que Sonnet repete seis vezes, ele pode ganhar. Se ambos acertam na primeira tentativa, Fable é simplesmente muito mais caro. A variável útil é:

**custo até resultado correto e verificado = exploração + implementação + tentativas falhas + testes + revisão + integração + retrabalho.**

Não encontrei suporte para converter isso numa única fórmula universal, e fazê-lo esconderia justamente os trade-offs que você quer entender.

### Assinatura: não converta API dollars em “quanto do Max gastei”

Em Pro/Max/Team/Enterprise, o comportamento de limites de uso não deve ser modelado simplesmente multiplicando tokens pelo preço da API. A página oficial descreve Max em termos de multiplicadores de uso relativos a Pro, não como uma carteira linear de dólares de API. citeturn13search7

Portanto, para você existem pelo menos dois cenários diferentes:

**Se você usa Claude Code dentro de Max:** o problema prático é chegar à conclusão antes de esgotar os limites da janela/período da assinatura. Ultracode, agent teams e esforços altos podem acelerar o consumo sem produzir uma fatura proporcional visível. citeturn6view0turn16view1

**Se você usa Console/API:** cada token/cache operation tem preço observável e é possível comparar runs economicamente com muito mais rigor. O Claude Code autenticado por Console consome tokens conforme o preço padrão da API. citeturn17search2

Não identifiquei seu plano atual e, como você pediu, não presumi um.

### Recomendações sustentadas e grau de confiança

| Conclusão provisória | Evidência | Condições | Confiança |
|---|---|---|---|
| **Sonnet 5.5 medium deve ser um baseline forte para coding bem especificado** | default do Claude Code + guidance oficial + sweep independente mostrando bom custo/velocidade | tarefas com regras/acceptance criteria claros | **Alta para eficiência; moderada para qualidade relativa**. citeturn19search10turn21search16 |
| **Antes de Sonnet xhigh/max, vale testar Opus em esforço menor** | AA reportada: Opus high supera Sonnet xhigh em score e custo; Opus xhigh iguala Sonnet max por menos da metade | resultados gerais podem não transferir para seu repo/harness | **Moderada**. Evidência controlada de modelo, mas não Claude Code específico. citeturn21search16 |
| **xhigh/max não devem ser default** | guidance oficial + FrontierCode max<xhigh + curva de custo AA | especialmente tarefas bem estruturadas | **Alta**. citeturn12view1turn9search3turn21search16 |
| **Fable 5.1 deve ser escalonamento excepcional, não default de coding** | preço muito maior + Opus 5.5 lidera Fable em benchmarks de coding do próprio fornecedor | tarefas de raciocínio/long-horizon podem ser diferentes | **Moderada**; evidência independente atual Fable×Opus5.5 ainda escassa. citeturn21search0turn20search9 |
| **Haiku é mais defensável como auxiliar delimitado do que coordenador de trabalho complexo** | preço/velocidade, ausência de effort e design de subagents | busca, classificação, leitura simples, checks | **Moderada–alta**. citeturn8search2turn3view1 |
| **Mais agentes devem ser introduzidos apenas quando existe paralelismo real** | docs confirmam multiplicação de uso, conflitos e necessidade de partitioning | módulos/hipóteses independentes | **Alta para mecanismo; moderada para tamanho ótimo do time**. citeturn16view1 |
| **Uma sessão não deve ser quebrada por contagem de mensagens/horas** | contexto depende de tokens/calls; cache/compaction alteram economia | medir `/context`, relevância e reconstrução | **Alta contra a regra arbitrária; moderada sobre estratégia ótima**. citeturn18view0turn18view1 |
| **Para overnight, estrutura/verification gates são mais importantes que effort max** | effort não é duração; workflows/cloud têm mecanismos próprios | tarefa precisa ser testável | **Moderada–alta**. citeturn12view0turn16view0 |
| **Review pelo mesmo modelo não basta para segurança de regras críticas** | relatos práticos + problema de erros correlacionados; falta benchmark quantitativo | regras médicas/financeiras/identidade | **Moderada**, sustentada mais por engenharia defensiva que por benchmark Claude específico. citeturn17search32 |

### Protocolo pessoal necessário para resolver a dúvida das sessões

Aqui há uma lacuna real da literatura, então vale um experimento seu. O desenho precisa separar **modelo**, **effort** e **estratégia de sessão**; testar tudo ao mesmo tempo produz uma sopa causal.

Escolheria duas tarefas reais, congeladas por commit:

**Tarefa curta/modular:** implementação de filtros/chips com testes e comportamento visual especificado.

**Tarefa longa/estado rico:** importação XLS/XLSX com deduplicação/reconciliação ou a regra hospitalar RA × internação × D+4, incluindo bugs deliberados.

Para cada tarefa, primeiro fixe **Sonnet 5.5 medium** e compare as estratégias A–E. Idealmente três execuções por condição; cinco seriam melhores se custo permitir. Depois, em uma segunda bateria, mantenha a melhor estratégia de sessão fixa e compare Sonnet `medium/high/xhigh` com Opus `low/medium/high`. Não misture as duas etapas.

Registre por run:

| Categoria | Métricas |
|---|---|
| **Correção** | acceptance tests pass/fail; bugs residuais cegos; invariantes violados |
| **Custo API**, quando aplicável | input, output, cache creation, cache read; custo monetário total |
| **Assinatura** | quota/usage antes e depois, sem tentar convertê-la artificialmente em API dollars |
| **Contexto** | `/context` inicial, pico, número de compactions |
| **Trabalho agentic** | tool calls, subagentes, agentes simultâneos, retries |
| **Tempo** | wall-clock até primeira implementação e até resultado verificado |
| **Humano** | minutos de revisão, número de intervenções, decisões requeridas |
| **Retrabalho** | tentativas falhas, linhas/arquivos revertidos, regressões |
| **Escopo** | arquivos alterados necessários versus não necessários |
| **Continuidade** | arquivos relidos, hipóteses redescobertas, perda de decisões após handoff |

Para cache, runs “cold” e “warm” não podem ser misturados. O API oferece caches de cinco minutos e uma hora com preços distintos; portanto, execute as repetições sob condição explicitamente controlada e registre `cache_read_input_tokens`/`cache_creation_input_tokens`, em vez de inferir hit. citeturn19search22turn18view1

O resultado útil não será “estratégia B gastou 17% menos”. Será algo como: **B economizou input, mas acrescentou 11 minutos humanos e duas redescobertas de contexto; C consumiu mais cache-read porém precisou de zero reconstruções e produziu menos erros**. Esse é o nível de granularidade de que um guia futuro realmente precisa.

## Conclusões contraditórias, lacunas e fontes

### O que já pode ser considerado bem estabelecido

**Não existe fundamento para usar `max` sistematicamente.** A documentação desaconselha esse padrão e já existe caso concreto de pior desempenho em `max`. citeturn12view1turn9search3

**Modelo e effort são dois eixos separados.** Em pelo menos uma bateria independente, um modelo mais capaz em esforço menor venceu ou igualou um modelo menor em esforço maior por custo menor. citeturn21search16

**Sonnet 5.5 `medium` merece ser levado muito mais a sério como default do que a heurística “Sonnet só para coisas simples”.** É literalmente o default do Claude Code atual, é muito rápido e, nos dados independentes iniciais, supera Sonnet 5 em configurações muito mais caras. citeturn19search10turn21search16

**Opus 5.5 parece ser o verdadeiro escalonamento de coding antes de Fable.** Ele lidera Fable 5.1 nos benchmarks agentic coding publicados pela Anthropic e custa menos da metade por token de output. Isso não prova que Opus vença Fable em todos os problemas difíceis, mas torna irracional tratar Fable como escalonamento automático. citeturn21search0turn20search9

**Ultracode não deve ser confundido com inteligência adicional.** É orquestração automática de workflows, pode aumentar muito o fan-out e inclusive relaxa alguns guardrails de concorrência/avisos do fluxo normal. citeturn6view0

**Context window, tokens cobrados e limite de assinatura são grandezas diferentes.** Cache reduz preço de processamento de um prefixo, não o espaço que ele ocupa; compaction reduz contexto ativo; uma sessão nova reseta conversa; assinatura impõe outra camada de limites. citeturn18view1turn18view0turn13search7

### Contradições que precisam permanecer abertas

Há um resultado particularmente instrutivo: Anthropic mostra **Sonnet 5.5 vencendo Opus 5.5 no Terminal-Bench 4.0** em seu lançamento, enquanto a Artificial Analysis reproduzida pela BitsMinds coloca **Opus 5.5 acima de Sonnet 5.5 em todos os níveis comparáveis do índice geral**. Isso não é necessariamente uma inconsistência. É evidência de que **ranking é dependente da tarefa e do harness**. citeturn21search16turn21search21

Fable é outro exemplo. O marketing/documentação o posiciona para o extremo de capacidade e multi-day work, mas Opus 5.5 vence nos benchmarks de coding destacados pela própria Anthropic. Pode ser que Fable seja melhor em um subconjunto diferente de raciocínio longo; pode ser que a nomenclatura comercial represente posicionamento mais amplo que coding. O conjunto atual não permite transformar isso em uma fronteira limpa. citeturn20search9turn21search0

O ganho de vários agentes continua mal quantificado. A mecânica de custo e coordenação é clara; o benefício líquido em software real não. Agent Teams possui exemplos e relatos, mas não encontrei uma bateria independente atual em que “1 agente versus 2 versus 4 versus workflow” execute centenas das mesmas tarefas com custo total e qualidade avaliados cegamente.

Também falta uma comparação pública confiável das estratégias **A–E de sessão** em Claude Code atual. A documentação permite explicar o mecanismo, mas qualquer número do tipo “sessões curtas economizam 30%” seria inventado sem experimento.

Para Apps Script, ingestão de PDF/XLSX, dashboards financeiros e lógica temporal hospitalar, não encontrei benchmarks específicos suficientes. As recomendações nesses domínios são **aplicações de princípios gerais**, não evidência direta.

Também não usei vídeos atuais como evidência central. A busca encontrou vários vídeos de lançamento e demos, mas os resultados acessíveis não forneceram transcrição/procedimento/timestamps suficientes para comprovar uma comparação controlada. Seguindo seu critério, **título entusiasmado de YouTube não foi convertido em dado**.

### Hierarquia provisória de decisão

A síntese que melhor sobrevive à pesquisa é esta:

**Primeiro, melhorar a especificação**, quando o problema é “Claude não sabe qual regra você quer”.

**Depois, elevar `medium → high`**, quando o modelo entende a tarefa mas não verifica/investiga suficientemente.

**Depois, considerar trocar Sonnet → Opus**, especialmente antes de pagar o custo de Sonnet `xhigh/max`, porque há evidência inicial de que o Opus menos esforçado pode ser simultaneamente melhor e mais barato por tarefa.

**Só então usar `xhigh/max`**, quando a tarefa realmente parece limitada por raciocínio e suas próprias avaliações mostram ganho.

**Fable 5.1 vem depois como escalonamento especializado**, não como rotina de coding.

**Adicionar agentes somente quando existe decomposição verdadeira**; não para compensar falta de especificação.

**Preservar uma sessão enquanto o contexto acumulado continua sendo informação útil; compactar quando virou peso; começar nova quando a tarefa mudou ou quando o estado importante já está explicitamente persistido.**

**Para overnight, o principal multiplicador de confiabilidade é tornar o sucesso verificável e o estado recuperável**, e não pedir ao modelo para “trabalhar muito, revisar infinitamente e só parar quando estiver perfeito”.

Essa hierarquia é uma **conclusão provisória**, com confiança moderada. A parte “não usar max por default” tem confiança alta; a ordenação fina entre Sonnet/Opus/Fable ainda precisa de avaliações nos seus próprios repositórios.

### Fontes principais auditadas

| Fonte direta | Autor / data | Papel nesta pesquisa |
|---|---|---|
| [Effort — Claude Platform Docs](https://platform.claude.com/docs/en/build-with-claude/effort) | Anthropic; documentação vigente consultada em 03/10/2026 | níveis, defaults, compatibilidade, cache e recomendações de effort. citeturn12view0turn12view1turn12view2 |
| [Claude Sonnet 5.5](https://www.anthropic.com/claude-sonnet-5-5) | Anthropic, **28/09/2026** | lançamento, preço, velocidade, defaults e benchmarks do fornecedor. citeturn19search10 |
| [Sonnet 5.5 model docs](https://platform.claude.com/docs/en/models/sonnet-5-5/overview) | Anthropic; consultado 03/10/2026 | contexto, output, cache e preços. citeturn19search22 |
| [Claude Opus 5.5](https://www.anthropic.com/claude-opus-5-5) | Anthropic, setembro/2026 | benchmarks, comparação com Fable, custo e fast mode. citeturn21search0 |
| [Opus 5.5 model docs](https://platform.claude.com/docs/en/models/opus-5-5/overview) | Anthropic; consultado 03/10/2026 | comportamento técnico e breaking changes. citeturn21search5 |
| [Claude Fable 5.1 and Mythos 5.1](https://www.anthropic.com/claude-fable-and-mythos-5-1) | Anthropic, setembro/2026 | posicionamento e configuração Fable. citeturn20search9 |
| [Terminal-Bench leaderboard](https://terminal-bench.com/) | Terminal-Bench maintainers; linhas atuais com datas por run | benchmark público de ambiente terminal/Claude Code. citeturn21search2 |
| [Sonnet 5.5 benchmarks: scores, real costs…](https://www.bitsminds.com/news/claude-sonnet-5-5-launch-price-benchmarks-2026) | BitsMinds, **29/09/2026** | fonte secundária dos resultados da Artificial Analysis e discussão de effort/custo; não confundida com o avaliador original. citeturn21search16 |
| [Explore the context window](https://code.claude.com/docs/en/context-window) | Anthropic; consultado 03/10/2026 | `/context`, compaction, `/clear`, 1M context e subagents. citeturn18view0 |
| [Context windows — Claude API](https://platform.claude.com/docs/en/build-with-claude/context-windows) | Anthropic; consultado 03/10/2026 | contabilidade de contexto, thinking e cache. citeturn18view1turn18view2 |
| [Memory / CLAUDE.md](https://code.claude.com/docs/en/memory) | Anthropic; consultado 03/10/2026 | persistência entre sessões. citeturn15view1 |
| [Checkpointing](https://code.claude.com/docs/en/checkpointing) | Anthropic; consultado 03/10/2026 | rewind, summaries e limitações do checkpoint. citeturn16view3turn16view4 |
| [Settings](https://code.claude.com/docs/en/settings) | Anthropic; consultado 03/10/2026 | precedência, persistência e diferenças entre superfícies. citeturn15view3 |
| [Run agents in parallel](https://code.claude.com/docs/en/agents) | Anthropic; consultado 03/10/2026 | subagents, Agent View, teams, workflows e Projects. citeturn16view0turn16view1 |
| [Worktrees](https://code.claude.com/docs/en/worktrees) | Anthropic; consultado 03/10/2026 | isolamento e requisitos de versões recentes. citeturn15view4turn16view5 |
| [Claude Code product page](https://claude.com/product/claude-code) | Anthropic; consultado 03/10/2026 | superfícies, assinatura/API e fast mode. citeturn17search2 |
| [Claude pricing](https://claude.com/pricing) | Anthropic; consultado 03/10/2026 | Max e planos de assinatura. citeturn13search7 |
| [Agentic Code Review](https://addyosmani.com/blog/agentic-code-review/) | Addy Osmani, **15/06/2026** | experiência prática de revisão assistida por agentes; não tratado como benchmark. citeturn17search32 |
| [“Ultrathink is a Claude Code magic word” — Hacker News](https://news.ycombinator.com/item?id=43739997) | discussão com Simon Willison, **abril/2025** | evidência histórica do antigo mecanismo `ultrathink`; explicitamente não generalizada para 2026. citeturn13search24 |

A base de evidências aponta, portanto, para uma filosofia menos espetacular e mais útil: **use o modelo/effort mínimo que fecha a tarefa com verificação, escale diante de sinais observáveis de insuficiência, mantenha estado onde ele tem valor e introduza paralelismo apenas quando a estrutura do problema realmente o permite**. O maior erro econômico não parece ser “usar Opus demais” ou “usar Sonnet demais” isoladamente; é **gastar tokens adicionais sem atacar o gargalo real — especificação, raciocínio, contexto, feedback, verificação ou decomposição**.