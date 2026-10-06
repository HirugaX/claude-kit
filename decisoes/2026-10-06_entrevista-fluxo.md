# Entrevista de 05-06/10/2026 — o fluxo de trabalho com o Claude Code (registro para a janela do plano)

- **O que é:** o registro da janela que leu as pesquisas, instalou as skills e fez o `/grill-me` do fluxo de
  trabalho (aberta em `C:\CLAUDE-PROJETOS`, notebook, Opus 5.5, esforço `max` digitado pelo Ettore). Ela fechou com
  ~550 mil tokens de contexto; por decisão do Ettore (Q15), **o plano roda numa janela nova que lê só este registro e
  as pesquisas**. Sem dado de paciente.
- **Estado do grill:** rodadas 1 e 2 respondidas (Q1-Q15). A **rodada 3** (o que depende de duas verificações que
  terminaram depois) abre a janela do plano — seção 7.
- **Quem confere:** o Ettore lê as seções 1, 2 e 5 antes de abrir a janela do plano; se algo estiver errado, corrige
  aqui ou diz na janela do plano.

## 0. Como a janela do plano usa este registro

1. Ler este arquivo inteiro. Depois, só o que a seção 10 manda ler (as pesquisas e as duas skills atuais).
2. Fazer a rodada 3 do grill (seção 7) com o Ettore, no formato da skill `grilling` (numeradas, com recomendação),
   e as perguntas no formato do CLAUDE.md pessoal (o problema, a pergunta, as opções, o que muda).
3. Aplicar o espírito da `recursos-do-projeto` (a ficha: AGORA ≤ 7 / QUANDO / NÃO) ao fluxo novo, já pesando o
   `claude-code-setup` como possível substituto dela (seção 6.2).
4. Escrever o plano em `decisoes\2026-10-06_plano-fluxo.md`: fases, portões, testes, o modelo e o esforço de cada fase,
   e o prompt de cada janela (modelo e `/effort` na 1ª linha). Mostrar ao Ettore e esperar o "sim".
5. Fechar com o resumo (com a linha "Sinais de insuficiência do modelo") e o prompt da 1ª janela de execução.

## 1. O objetivo, nas palavras do Ettore (sintetizado)

> A melhor tarefa feita, com a maior qualidade possível, pelo menor uso de tokens — "sempre foi esse o objetivo
> principal". Eficiência, qualidade, economia de tokens, sofisticação, profissionalismo em programação, engenharia
> de software e design.

E três dores concretas:
- **"Office boy de prompts":** copiar o prompt de uma janela, abrir outra, colar, escolher modelo e esforço — em
  janelas "infinitas". A divisão em janelas "melhorou muito a eficiência de tokens, sem dúvida"; ele quer manter a
  economia "de modo mais inteligente e que necessitasse menos intervenção minha".
- **Contexto desnecessário:** "não quero levar contexto desnecessário". Montou as skills "por não entender como
  funciona, sou vibe coder"; pede ajuda nas decisões e que só se acione "o que precisa em cada parte".
- **Memória entre sessões e tomada de decisões** fracas.

Sobre o que construímos: ele entendia que a `uso-do-claude` era o que tínhamos de único — orientar a escolha de
modelo e a sessão entre janelas (copiando o prompt) para economizar tokens. Quer que as skills que "criou" sejam
**repensadas, quebradas, ou nem usadas** se as de terceiros fizerem melhor. Skill nova, se precisar, "precisa ser
inteligente e bem orquestrada, incluir uso de agentes e manter eficiência de tokens com o melhor possível da tarefa".

Vocabulário dele: "skill" cobre skills, plugins, repositórios, MCPs e outros recursos.

## 2. O que o Ettore pediu, mensagem a mensagem (síntese fiel)

1. **Abertura (05/10):** refinar o fluxo; pensar skills e fluxos novos integrando `recursos-do-projeto` e
   `uso-do-claude`; as pesquisas em `claude-kit\fontes` (efficiency report, Top 50; o `Claude_Workbench_Prompts` como
   sugestão de fluxo dele); o `/grill-me` "ajudou muito" — pôr no fluxo normal o resto do repositório do Matt Pocock,
   as de UX e design, as de memória; não ser office boy; o Claude pode abrir janelas no VS Code? se não, agentes
   para tarefas menores?; memória entre sessões e decisões; ler tudo criticamente ("não aceite cegamente"); analisar
   à luz dos projetos e do que se sabe dele; analisar o fluxo atual; instalar o aplicável; refinar o fluxo; um fluxo
   por projeto; skills novas e meio de migrar para o desktop e aplicar personalizado aos projetos de lá; depois do
   grill, parar e começar o planejamento.
2. **Autorização (05/10):** "você tem autorização para instalar e configurar os plugins e skills que achar
   relevantes"; depois atualizar o guia com as skills, o uso e quais se chamam por `/`; incluir memória, controles
   do que o Claude não pode fazer, as outras do criador do grill-me, UX e design, as da Anthropic para Excel e
   documentos, o discutido no Workbench e o que eu achar relevante.
3. **Mais pedidos (05/10):** análise de dados, mapeamento, o "mem-claude" (é o `claude-mem`); "tome cuidado com as
   redundantes"; manter um conjunto de skills que funcione como o grill-me; ensinar o uso nos guias; banco de dados?
   UX? ícones? o que for relevante.
4. **Pesquisa (05/10):** "alguém já deve ter pensado nisso": pesquisar no GitHub e em nomes reconhecidos da IA como
   montar o fluxo com menos intervenção, mantendo a economia.
5. **Rodada 1 (06/10):** respostas na seção 5. Junto: a fase de planejamento roda aqui, mas ele precisa do prompt
   para a fase seguinte em outra janela; quer "uso mais claro de quando usar o ultracode"; quer incluir e
   contextualizar por projeto: **Cartographer, Claude Code Setup, Claude mem, Headroom e "Ominiclaude"** (quer muito
   usar este último de modo eficaz, sem comprometer qualidade); o `claude-code-setup` "pode ser extremamente útil
   inclusive para esse trabalho de agora".
6. **A fase de plano (06/10):** roda aqui ou em outra janela, sem perder contexto e economizando? (→ Q15).
7. **Rodada 2 (06/10):** respostas na seção 5. Junto: **separar no kit, em pastas, o que é skill, plugin e outro
   recurso, e o que nós criamos**; não achou a `uso-do-claude`; repensar as skills dele (seção 1); celular (Q9).

## 3. O que já foi feito na janela de 05-06/10 (fatos)

- **Instalado** (pesquisa `pesquisas\2026-10-05_skills-e-plugins-avaliados.md`):
  - 20 skills do Matt Pocock (commit `4588b32`), 1 da Vercel (`web-design-guidelines`), 3 da Trail of Bits
    (`property-based-testing`, `spec-to-code-compliance`, `goal-prompt`), por `npx skills add … -g -a claude-code
    --copy` + `ligar_claude.py`: 28 skills pessoais no kit, todas com junção conferida.
  - 4 plugins, escopo de usuário: `cc-safety-net@cc-marketplace` (gancho PreToolUse; Bash e PowerShell),
    `claude-md-management`, `session-report`, `frontend-design` (oficiais). Custo fixo medido por
    `claude plugin details`: 79, 177, 72 e 80 tokens.
  - O `claude` do PATH: 2.1.234 → 2.1.290 (`claude update`). A extensão do VS Code é 2.1.289 e embute o próprio CLI.
- **Proposta de política do safety-net** em `scripts\safety-net-politica.json` (protege `desosp-app-dados` e
  `desosp-app-backups` também no terminal); validada com `policy check`. **Quem aplica é o Ettore** (o plugin não
  deixa o Claude mudar a própria política).
- **Guia atualizado** (Claude Docs, https://claude.ai/code/artifact/954e4c88-eb09-4a18-b4e5-f95f27004488): catálogo
  das 33 skills (sozinha × só `/`), o fluxo do grill em 6 passos, controles, o que ficou de fora, skills do claude.ai
  a desligar, caminhos `C:\CLAUDE` corrigidos para o kit.
- **Pesquisas salvas** (com linha no `INDICE.md`): `2026-10-05_sessoes-memoria-plugins-claude-code.md`,
  `2026-10-05_skills-e-plugins-avaliados.md`, `2026-10-05_fluxo-atual-dos-projetos.md`,
  `2026-10-06_continuar-em-contexto-limpo-sem-copiar-prompt.md` — e as duas da seção 7, quando chegarem.
- **Backup** do `settings.json` de usuário antes dos plugins: `~\.claude\backups\settings.json.2026-10-05_antes-dos-plugins`.
- **Achados laterais:** outra janela (organizar-projetos, na mãe) grava o `~\.claude\settings.json` enquanto se
  trabalha: pôs o gancho PostToolUse das cores e devolveu o esforço do Opus 5.5 a `medium` (estava `xhigh`, contra a
  régua). O gancho das cores custa ~40 ms por comando e **zero token** (medido em 06/10). No Windows, `python3` é o
  atalho da Microsoft Store (falha); a ferramenta Bash daqui engole `\\` em heredoc e em JSON inline (usar arquivo).

## 4. O diagnóstico (números)

- **O custo dominante é o tamanho da conversa, não as skills.** Desde 28/09: ~6.400 chamadas, 88% Opus 5.5, 0,6%
  Sonnet 5.5. Mediana de contexto por chamada nas sessões de trabalho: 199 a 317 mil tokens; picos de 865 mil; custo
  fixo só 14-26%. A janela desta entrevista chegou a ~550 mil.
- **Custo fixo de abrir:** app ~58 mil, kernel ~66 mil (era 128-140 mil antes de 03/10), planilha ~55 mil. CLAUDE.md
  de 354 / 430 / 226 linhas (alvo < 200). `MEMORY.md` do censo: 12 KB, uma linha de 7,4 mil caracteres repetindo o
  status do handoff. No kernel, tocar o `data_merge.py` carrega 8 regras de uma vez (87 KB, ~25 mil tokens).
- **Estado que só cresce:** `HANDOFF_APP.md` 6.708 linhas / 575 KB; `HANDOFF_SPRINT2.md` 4.147 / 376 KB; estado velho
  em `desosp-app\CLAUDE.md:53` e no `HANDOFF_APP.md:11`. Nenhum projeto tem `docs\adr`.
- **Trabalho manual:** ~7 passos fixos por janela, 4 de transporte puro (abrir, copiar, colar, `/effort`); o app teve
  ~18 janelas em 29/09-05/10, ~7 de implementação.
- **Três implementações do mesmo método:** gancho de abertura (app completo, planilha só a caixa, kernel nenhum),
  lugar do estado e formato do prompt diferentes; a regra comum copiada em 4 a 9 lugares.
- **A `uso-do-claude`:** 22 KB de `SKILL.md` (~6 mil tokens) carregados a cada disparo — e ela dispara em quase toda
  janela (abrir, fechar, modelo, esforço). Em toda sessão vão só a descrição (~200 tokens) e o CLAUDE.md pessoal.
- Detalhes e fontes: `pesquisas\2026-10-05_fluxo-atual-dos-projetos.md`.

## 5. As decisões (rodadas 1 e 2)

| # | decisão | o porquê e as nuances do Ettore |
|---|---|---|
| Q1 | **(b)** painel da extensão para o trabalho com conversa; **terminal** para o que roda sozinho; testar antes numa pasta/tarefa sintética | "podemos predominar com trabalho no terminal, só preciso aprender o fluxo" → o guia ensina o fluxo do terminal (`claude --bg`, `claude agents`, `attach`, statusline) |
| Q2 | **(b)** o Claude encadeia as fases sozinho enquanto o critério de pronto passar; para só em decisão ou falha | escolheu (b) e não o (c) recomendado: os pontos de parada da Q10 são o freio |
| Q3 | **(a)** por projeto, `docs\ESTADO.md` curto (≤ ~1 página), **reescrito** a cada fechamento; o handoff atual congelado como histórico (lido por busca); decisões em `docs\adr\` + `GLOSSARY.md` (`domain-modeling`); memória automática só com preferência e correção; nada de estado no CLAUDE.md | "preciso embasar na pesquisa de como especialistas têm trabalhado": o desenho segue o arquivo de progresso + `git log` (harness da Anthropic), o ExecPlan da OpenAI (Progress, Surprises, Decision Log, Outcomes; "possível recomeçar só com ele"), o `STATE.md` do GSD, ADR + glossário do Matt Pocock — o plano cita cada um |
| Q4 | **(c)** quebrar por momento de uso: núcleo curto + peças que só carregam quando aquele momento chega | inclusive tirar as cores (`organizar-projetos`) para uma skill só `/`; "vamos quebrar e acionar só o que precisa em cada parte"; e repensar tudo à luz de terceiros (seção 6.2) |
| Q5 | **(a)** Opus 5.5 na janela principal (`medium` padrão; `high` em plano e regra clínica); trabalho mecânico em subagentes com `model: sonnet`/`haiku`, sem passo dele | "precisamos de uma skill para orquestrar os agentes de modo eficiente, parecem existir boas opções" → rodada 3 |
| Q6 | **(a)** o `claude-kit` vira repositório **privado** no GitHub; no desktop `git clone` + `ligar_claude.py` + script de plugins | "muito mais fácil"; e "damos comando para o desktop usar, sincronizar e trocar informações para ficar alinhado" |
| Q7 | **(a)** espaço próprio de pesquisa clínica | hoje pesquisa pelo OpenEvidence; quer guardar a memória das pesquisas anteriores, acessar mais artigos, ter perguntas melhores e usar o Claude com eficiência nisso |
| Q8 | a ordem: kit → piloto no app → kernel → planilha → desktop | Folha/RH e Acolhimento (Apps Script) **estão no desktop**; antes de subir ao GitHub, ele quer fazer lá o mesmo processo daqui: juntar tudo numa pasta `CLAUDE-PROJETOS`, trocar os ícones (módulo `organizar-projetos`) — **incluir esse passo na cadeia** |
| Q9 | **(a)** principal: a janela que fecha lança a fase seguinte com `claude --bg --name … --model … --effort … "Leia docs/PROXIMO.md e siga"`, depois de passar no teste sintético; **(b)** reserva no painel: `/clear` + gancho que injeta o `PROXIMO.md`; **(c)** link `vscode://` fora | a janela fecha pelo que vier primeiro: fim da fase, ~150 mil tokens ou troca de modelo. **Celular:** hoje o Remote Control só pega uma janela, e ele gasta muitos tokens nela ou para até voltar para casa; "se possível, incluir partes do processo pelo Claude Code do celular" (seção 6.3) |
| Q10 | parar sempre em: escrita em dado real **não aprovada antes**; rodada real e reprocesso não aprovados; migração de banco ou de esquema; regra clínica nova; leitura de fonte nova; subir para Fable, `xhigh`, `max` ou ultracode; o mesmo erro após 2 tentativas diferentes; decisão que não está no `ESTADO.md` nem num ADR | nuances dele: "ler fonte nova geralmente eu entreguei antes ou me exige entregar, aí é justo parar"; "escrita de dado real, se tiver isso aprovada de algum modo antes, pode ocorrer"; regra clínica e leitura "têm que me perguntar"; **subir de modelo pergunta; descer para modelo mais barato, se mantém a qualidade, não precisa perguntar**. `git push` **(i)**: livre no fim de cada fase com testes verdes, depois de `git log origin/main..` |
| Q11 | **(a)** o espaço de pesquisa tem grill próprio, numa janela própria, logo depois das peças do kit, em paralelo ao piloto do app | "podemos definir regras e já deixar essa parte orientada"; ele cria uma pasta nova, põe os artigos que já tem, e compartilha entre desktop e notebook pelo GitHub. Regra fixa: **nunca dado de paciente** ali |
| Q12 | **(a)** pasta `caixa\` no kit para mensagens entre os PCs (formato das caixas dos projetos); o gancho de abertura faz `git pull --ff-only` do kit e avisa se divergiu; ao fechar, commit e push do que mudou no kit | fora do git: dado de paciente, credenciais, retratos com nomes de arquivos dos projetos |
| Q13 | subagente comum é o padrão para ler/buscar/tarefa independente; **ultracode (Workflow)** só com 4+ partes independentes, cada uma conferida por comando; nunca para julgamento clínico, dado real ou decisão dele; **teto de 10 agentes** sem perguntar, acima disso estimativa + "sim" | exemplos da cadeia: auditar as 27 regras do kernel; migrar os 12 comandos da planilha; enxugar os três CLAUDE.md conferindo por script; pesquisa ampla |
| Q14 | **(a)** seção curta "Skills deste projeto" (≤ 10 linhas) no CLAUDE.md de cada projeto + `enabledPlugins` no settings do projeto desligando o que não serve ali | e repensar as skills de cada projeto quando preciso; **pontos de checagem para buscar recursos novos** quando algo parece fugir do escopo, usando skills de busca (`find-skills`, `claude-code-setup`, a nossa `pesquisa`) — "skill" = plugins, skills, repositórios, MCPs |
| Q15 | **(a)** este registro + o plano numa janela nova (começa com ~60-80 mil tokens em vez de ~550 mil) | "procure resumir e sintetizar tudo que escrevi para a próxima janela não perder o contexto". A regra da `uso-do-claude` §10 ("plano na mesma janela do grill") ganha exceção: acima de ~200 mil tokens, registro escrito + janela nova |

## 6. Diretrizes novas que o plano tem de cobrir

### 6.1 O kit separado por tipo e por origem
O Ettore pediu pastas diferentes para skill, plugin e outros recursos, e para o que nós criamos. Restrição técnica: o
Claude Code só acha skill pessoal em `~\.claude\skills\<nome>\SKILL.md` (um nível só). Então: o kit organiza as
**fontes** em subpastas e o `ligar_claude.py` cria as junções **planas** em `~\.claude\skills`. Proposta a validar:

```
claude-kit\
  CLAUDE.md  LEIA-ME.md
  skills\nossas\        uso-do-claude (quebrada), recursos-do-projeto, organizar-projetos, as novas
  skills\terceiros\     mattpocock\  vercel\  trailofbits\  (cópias fixadas por commit + origem.json)
  plugins\              plugins.json (marketplaces, plugins, escopo por projeto) + instalar_plugins.py
  ganchos\              abertura, fechamento, cores (hoje dentro da skill), statusline
  config\               safety-net-politica.json, trechos de settings
  scripts\              ligar_claude.py (fontes aninhadas → junções planas), perguntas_controle.py, medir_uso.py
  pesquisas\  decisoes\  fontes\  caixa\  _do_desktop\
```

O `npx skills update` grava em `~\.claude\skills`; o `ligar_claude.py --pasta-vence` precisa saber para qual
`terceiros\<origem>\` devolver (um `origem.json` com skill → repositório → commit). A outra janela (cores) mexe em
`skills\uso-do-claude\organizar-projetos\`: combinar antes de mover.

### 6.2 Repensar as skills "criadas" — manter só o que é único
Critério do Ettore: o que terceiros fazem melhor, sai; o que fica é inteligente, orquestrado, com agentes, e não leva
contexto desnecessário. Hipóteses a confirmar com as verificações da seção 7:
- **Único da `uso-do-claude`** (nenhum terceiro cobre): a escada de modelo e esforço da família Claude 5 com as
  medições dele; os sinais de insuficiência; as armadilhas (atalho `sonnet` → Sonnet 5; `/effort` que grava; cache
  e troca de modelo); a política de contexto e de janela; a biblioteca de pesquisas; o `medir_uso.py`.
- **Quebra proposta (Q4):** núcleo curto (≤ 150 linhas) + `fechar-janela` (estado, próximo passo, caixa, resumo com
  "Sinais de insuficiência"; o DASH já tem uma `fechar-janela` — unificar o nome) + `modelo-e-esforco` + `pesquisa`
  (biblioteca → subagente → salvar; substitui a `research` do Matt) + `orquestrar` (seção 6.4) + `organizar-projetos`
  (só `/`). A abertura vira **gancho único** para todos os projetos.
- **`recursos-do-projeto` × `claude-code-setup`:** o oficial varre o código e recomenda 1-2 automações por categoria;
  a nossa liga cada recurso a uma resposta da entrevista e escreve os "não". Decidir: substituir, ou virar uma camada
  fina que roda o oficial e aplica as restrições daqui (dado de saúde, Windows, custo, lista de recusados).

### 6.3 Celular
Desejo: trabalhar fora de casa sem pagar uma janela gigante. Desenho a testar na pasta sintética: **uma janela
orquestradora pequena** ligada ao Remote Control (o celular fala só com ela); ela lança as fases em sessões novas
(`claude --bg`) ou subagentes, que trabalham com contexto limpo no PC; a volta vem por `SendMessage` (mensagem entre
sessões vivas) ou pelo `ESTADO.md`. Conferir antes: o Remote Control aceita isso? O `--bg` roda a partir dela? A
mensagem de volta chega? (pesquisas `2026-09-28_claude-code-na-nuvem.md` e `2026-10-05_sessoes-memoria-plugins-claude-code.md`).

### 6.4 A skill orquestradora (Q5) e o ultracode (Q13)
Uma `orquestrar` própria, fina, que junte: os 3 papéis (explorador, especialista, revisor isolado) da `uso-do-claude`
§9; modelo por papel; os pontos de parada da Q10; a regra do ultracode e o teto de 10; o cache do subagente
(5 min; `subagentPromptCacheTtl: "1h"` existe). A rodada 3 decide se ela se apoia em algo de terceiros (OMC,
`subagent-driven-development` do Superpowers, GSD, `chief-of-staff`/`implement-spec` do Matt, Workflow nativo).

### 6.5 Peças técnicas candidatas (verificadas na documentação, a testar)
- Gancho `SessionStart` único (fontes `startup|resume|clear|compact`): estado curto, caixa, git, modelo e esforço
  errados; no `clear`, injeta o `PROXIMO.md` (até 10 mil caracteres).
- Gancho `Stop` como portão: só deixa a janela fechar com o `ESTADO.md` gravado (até 8 bloqueios seguidos).
- `PreModelSwitch` para barrar o Sonnet 5 (o atalho `sonnet`); statusline no terminal com modelo, esforço e % de
  contexto; `showClearContextOnPlanAccept: true` (aprovar o plano limpando o contexto; conferir na extensão).
- `claude --bg` (prévia de pesquisa): para em "Needs input" se pedir permissão; o resumo vira linha de comando — sem
  dado pessoal; cada sessão ganha worktree antes de editar.
- Não existe `/clear` programático (issues #20267, #24257, #35150). Laço `claude -p` fica fora do núcleo: sem
  sandbox no Windows nativo e com risco de política de cobrança.

## 7. Em aberto — rodada 3 (na janela do plano)

Cada item com a pesquisa que o alimenta (as duas últimas chegaram depois desta entrevista; se o arquivo não existir
ao abrir a janela do plano, parar e avisar o Ettore):
1. **As ferramentas pedidas pelo nome** — Cartographer, `claude-code-setup`, `claude-mem` (talvez só no espaço de
   pesquisa, sem dado de paciente), Headroom, "Ominiclaude" (provavelmente oh-my-claudecode): instalar onde e como
   usar sem perder qualidade. → `pesquisas\2026-10-06_ferramentas-pedidas-e-orquestradores.md`.
2. **A skill orquestradora** (6.4): a própria fina, ou apoiada em terceiros. → o mesmo arquivo.
3. **`recursos-do-projeto` × `claude-code-setup`** (6.2). → o mesmo arquivo.
4. **O desenho do espaço de pesquisa clínica** (skills do K-Dense, acesso a PubMed/Europe PMC/OpenAlex, OpenEvidence,
   a memória de pesquisa, PDFs no git ou não) — vai para o grill próprio do espaço (Q11), não para o plano geral.
   → `pesquisas\2026-10-06_espaco-de-pesquisa-clinica.md`.
5. **Como aprovar antes a escrita em dado real** (nuance da Q10): por fase, no `PROXIMO.md` que o Ettore aprova junto
   com o plano, e por rotina fixa (a rodada do kernel, que já tem protocolo)? Recomendação: as duas.
6. **O caminho do celular** (6.3): entra no teste sintético como experimento.
7. **Privacidade do projeto de comunicação** (seção 12.1) — decisão do Ettore: (a) o Claude nunca vê nome,
   matrícula nem telefone: escreve com marcadores (`{{nome}}`, `{{matricula}}`) e um script local preenche;
   recomendado, porque é a regra que já existe (`desosp-censo\CLAUDE.md:226`; memória da planilha
   `console-sem-linha-de-paciente`); (b) o Claude vê os dados reais — muda essa regra para este projeto.
8. **Ordem dos projetos novos** (seção 12.3): a organização pessoal (sem dado de paciente) como primeiro projeto
   real no fluxo novo, antes do piloto no app?
9. **Isolamento entre projetos** (seção 12.4): confirmar as cinco camadas, os domínios, o que pode cruzar entre
   eles e o prefixo dos nomes de pasta; e avaliar o kit como marketplace local de plugins (ligar por projeto).
10. **Estudo e produtividade: um projeto ou dois?** (seção 12.5) A pesquisa `2026-10-06_estudo-anki-e-produtividade.md`
    recomenda **dois**: o estudo como pasta do Claude Code (`estudo-residencia\`: acervo do cursinho, seis skills
    próprias só `/` — `/ingerir`, `/resumo`, `/quiz`, `/explica-de-novo`, `/flashcards`, `/simular` —, Anki por TSV,
    PubMed, sem os conectores do claude.ai); a produtividade como **Project do claude.ai** com os conectores Notion e
    Google Calendar (anda no celular; o conector, não o plugin do Notion; workspace do Notion separado). Confirmar com
    ele, e o nome com prefixo de domínio.

## 8. A cadeia de ações (rascunho para o plano refinar)

| fase | o quê | onde |
|---|---|---|
| F0 | o Ettore aplica a política do safety-net e desliga as skills do claude.ai (seção 11) | ele |
| F1 | kit reorganizado (6.1), `ligar_claude.py` para fontes aninhadas, `git init` + varredura + repositório privado, `caixa\` | kit |
| F2 | a quebra da `uso-do-claude` e a decisão sobre a `recursos-do-projeto` (6.2); `fechar-janela`, `orquestrar`, `pesquisa`, `modelo-e-esforco`; ganchos de abertura e de portão; statusline; `PreModelSwitch` | kit |
| F3 | pasta sintética: o laço inteiro (plano → fases encadeadas por `claude --bg` → portão → `ESTADO.md`), a reserva `/clear` + gancho no painel, o experimento do celular; medir tokens contra a linha de base | pasta de teste |
| F4 | espaço de pesquisa clínica: grill próprio → recursos → montagem → GitHub (em paralelo a F5) | `pesquisa\` |
| F5 | piloto no app: `ESTADO.md` a partir do `HANDOFF_APP.md` (histórico congelado), CLAUDE.md < 200 linhas, "Skills deste projeto", `enabledPlugins`, ADR + glossário; uma fase FF real no fluxo novo | `desosp-app` |
| F6 | kernel: o mesmo + desenvolvimento separado da operação da rodada; as 8 regras sobre `data_merge.py` (ultracode candidato); `MEMORY.md` sem status | `desosp-censo` |
| F7 | planilha HC: o mesmo + decidir se os 12 comandos viram skills | `desosp-hc` |
| F8 | desktop: `organizar-projetos` lá (pasta-mãe `CLAUDE-PROJETOS`, ícones) → GitHub de Folha/RH e Acolhimento → kit por `git clone` + plugins → fluxo do DASH, Folha/RH e Acolhimento (prompts 10-12 do Workbench como checklist) | desktop |
| F9 | guia atualizado (ensinar o fluxo do terminal) + `/retro` | kit |
| F4b | organização pessoal: grill próprio → recursos → migrar do claude.ai → Notion → GitHub (seção 12.2) | `organizacao-pessoal\` |
| F5b | comunicação (e-mail e WhatsApp): grill próprio → recursos → modelos e skills `/email` e `/whatsapp`; o preenchimento automático depois da porta de dados do app (F5) | `desosp-comunicacao\` |

## 9. O que não muda (leis já escritas)

- Nunca dado de paciente em pesquisa, kit, prompt, resumo de `claude --bg` ou repositório; as regras `deny` e o
  safety-net protegem `desosp-app-dados` e `desosp-app-backups`.
- Nenhuma alteração sem mostrar o que foi verificado e esperar o "sim"; um plano aprovado é o "sim" do que ele pede.
- O prompt de cada janela traz o modelo e o `/effort <nível>` na 1ª linha; `max`, `xhigh`, Fable e ultracode só com
  motivo escrito; o Sonnet 5.5 se escolhe na lista do `/model` (o atalho abre o Sonnet 5).
- Todo resumo de fim de janela traz "Sinais de insuficiência do modelo".
- Antes de pesquisar, o `pesquisas\INDICE.md`; depois, salvar lá.
- O modo automático bloqueia mover pasta de projeto e apagar na raiz do `C:`: o comando é do Ettore.
- O `CLAUDE.md` pessoal é hardlink: gravar no próprio arquivo e conferir com `fsutil hardlink list` (a ferramenta Edit
  separa o hardlink).
- Commit por caminho explícito, nunca `git add -A`; duas janelas nunca editam os mesmos arquivos.

## 10. O que a janela do plano lê (e só isso)

- Este registro.
- `pesquisas\2026-10-06_continuar-em-contexto-limpo-sem-copiar-prompt.md` (como especialistas fazem; base da Q3 e da Q9).
- `pesquisas\2026-10-05_sessoes-memoria-plugins-claude-code.md` (o que o Claude Code oferece; base da Q9 e da 6.5).
- `pesquisas\2026-10-05_skills-e-plugins-avaliados.md` (o que entrou e o que ficou de fora).
- `pesquisas\2026-10-05_fluxo-atual-dos-projetos.md` (o fluxo e o inventário; base das fases F5-F7).
- `pesquisas\2026-10-06_ferramentas-pedidas-e-orquestradores.md` e `pesquisas\2026-10-06_espaco-de-pesquisa-clinica.md`.
- `skills\uso-do-claude\SKILL.md` e `skills\recursos-do-projeto\SKILL.md` (o que será quebrado).
- Sob demanda, por subagente: `fontes\Claude_Workbench_Prompts\` (checklists por projeto), `reference.md` da
  `uso-do-claude`, os CLAUDE.md dos projetos.

## 11. Pendências do Ettore

1. Num terminal: `npx -y cc-safety-net@2.6.0 policy apply C:\CLAUDE-PROJETOS\claude-kit\scripts\safety-net-politica.json --global` (e confirmar).
2. No claude.ai, desligar as skills sincronizadas `task-observer`, `management-consultant`, `google-workspace`,
   `import-memory`, `web-artifacts-builder` (decidir sobre `llm-council`, `prompt-master`, `find-skills`).
3. Criar a pasta do espaço de pesquisa e pôr os artigos que já tem (quando quiser; o grill próprio decide a estrutura).
4. Em `/config`, desligar o "Ultracode keyword trigger": a palavra escrita num prompt dispara um workflow, e este
   registro e as pesquisas a citam muitas vezes (colar um trecho deles bastaria). Fonte:
   `pesquisas\2026-10-06_ferramentas-pedidas-e-orquestradores.md`.
5. Nunca rodar `/omc-setup` (o instalador do oh-my-claudecode): ele sobrescreve o `~\.claude\CLAUDE.md` pessoal.

## 12. Projetos novos pedidos em 06/10 (depois da rodada 2)

Os dois entram no escopo de criação de projetos; cada um tem grill próprio e `recursos-do-projeto`, como o espaço de
pesquisa (Q11). Nenhum começa antes do plano aprovado.

### 12.1 Comunicação da desospitalização (e-mail e WhatsApp)

- **O pedido:** uma pasta para escrever os e-mails da desospitalização, que às vezes são necessários, com acesso aos
  e-mails já escritos e ao contexto dos pacientes em questão (do censo e do app) para retomar nome completo,
  matrícula e contexto clínico mínimo; e, no mesmo projeto, um módulo de mensagens rápidas de WhatsApp com acesso às
  comunicações anteriores, adaptando ao que ele precisa. "Talvez tenha skills para facilitar essa parte."
- **Onde (decisão delegada ao Claude): projeto próprio, `C:\CLAUDE-PROJETOS\desosp-comunicacao\`,** com janela
  própria, CLAUDE.md pequeno e repositório privado só com modelos, skills e scripts. Por quê: (1) aberto como
  subpasta do app, ele carregaria o CLAUDE.md de 354 linhas e as regras do app numa sessão de escrita; (2) o kernel
  vai ser aposentado quando o app estiver pronto; (3) a planilha HC é outro domínio (o `/mensagem` dela, de WhatsApp
  das rodadas HC, continua lá); (4) escrever comunicação tem outra cadência que desenvolver o app.
- **De onde vem o contexto do paciente:** de uma **porta de leitura no app**, que é o dono do modelo de dados e
  sobrevive à aposentadoria do kernel: um comando só de leitura que devolve só os campos mínimos. O lugar natural é
  `desosp-app\app\ia\`, a pasta deixada vazia de propósito como "ponto de extensão da PROPOSTA §7" até o Ettore
  decidir o que a IA faz dentro do app (`app\ia\LEIA-ME.md`). Construída no piloto do app (F5).
- **A regra que já existe e pesa aqui:** dado clínico vira arquivo, nunca passa pelo terminal
  (`desosp-censo\CLAUDE.md:226`); nunca imprimir linha de dado inteira, porque a saída fica no histórico da janela e
  pode ir para um resumo (memória da planilha). Por isso a recomendação da pergunta 7 da seção 7: o Claude escreve
  com marcadores e um script local preenche nome, matrícula e telefone; o texto final fica num arquivo local (ou na
  área de transferência). O contexto clínico mínimo que o Claude precisar para adaptar o texto chega sem
  identificador.
- **O acervo de e-mails e conversas anteriores:** local, fora do git (pasta irmã com `deny`, como a
  `desosp-app-dados`); o Claude lê só cópias com os identificadores trocados por marcadores, feitas por script.
- **Nunca envia:** o Claude só redige; quem envia é o Ettore (ponto de parada da Q10).
- **Os modelos de e-mail já enviados estão no PC do trabalho** (uma terceira máquina); o Ettore vai buscá-los quando
  tiver tempo. Antes de chegarem: criar a pasta de dados protegida (`deny` + safety-net) — eles têm nome de paciente.
  Conferir se a política do hospital permite tirar esses e-mails do PC do trabalho e por qual meio.
- **Skills a avaliar no grill do projeto:** `internal-comms` (Anthropic, formatos de comunicação), `stop-slop` (já
  sincronizada: tira o "jeito de IA" do texto), e duas próprias, `/email` e `/whatsapp`, com os modelos, o tom e o
  fluxo dos marcadores. MCP de Gmail ou Outlook só se ele quiser rascunho direto na caixa — e com o cuidado da
  privacidade. WhatsApp pessoal não tem integração oficial confiável: o texto final é copiado.
- **Relação com o que já existe:** o kernel gera mensagens da rodada (`desosp\mensagens.py`, `run_msg.py`, regra
  `mensagens.md`, `docs\templates\`); a planilha tem `/mensagem`. O projeto novo é para comunicação avulsa; os
  modelos que se repetirem podem virar, depois, função do próprio app (determinística, sem IA).

### 12.2 Organização pessoal

- **O pedido:** um projeto de organização pessoal, que ele começou no Claude chat (claude.ai): migrar, trazer
  ferramentas de produtividade pessoal e conectar o repositório ao Notion. É **o agente que ele começou a desenhar
  para produtividade pessoal e controle de procrastinação**; em 06/10 ele começou a extrair o material do chat.
  Enquanto o plano não sai, o material bruto vai para uma pasta só de fontes (12.4), sem janela do Claude Code nela.
- **O que já existe:** o plugin oficial do Notion no marketplace (`notion`, da própria Notion:
  https://github.com/makenotion/claude-code-notion-plugin) — ligar **só nesse projeto** (`enabledPlugins` do
  projeto); a pesquisa `pesquisas\2026-10-04_notion-filtros-e-visoes.md` (como o Notion filtra e organiza).
- **A migrar:** as instruções, os arquivos e as conversas-chave do projeto do claude.ai (exportação de dados do
  claude.ai ou cópia das instruções); o grill decide o que vira arquivo do repositório.
- **Regras:** nunca dado de paciente; repositório privado no GitHub, compartilhado entre os PCs.

### 12.5 Estudo para a residência e produtividade pessoal (pedido de 06/10)

- **O pedido:** skills de produtividade, ganho de tempo, organização e formação de hábitos; skills para um vibe coder
  aprender código; skills para organizar resumo de estudo e flashcards. Ele usa o **Anki** e estuda para a
  **residência médica**; quer resumos com organogramas, fluxos e esquemas; hoje faz resumos de aula e mnemônicos no
  modo de aprendizagem do Google. "Se houver algo que alguém já criou, pesquisar e gravar" para usar depois numa
  pasta (projeto) de estudo para a residência e produtividade pessoal.
- **Pesquisa em curso** (para o grill desses projetos, não para o plano geral):
  `pesquisas\2026-10-06_estudo-anki-e-produtividade.md` — Anki com o Claude (AnkiConnect, `genanki`, boas práticas
  de cartão), resumos visuais (Mermaid, mapas mentais, Excalidraw), o equivalente do modo de aprendizagem do Google,
  NotebookLM e sucessores, transcrição de aula, produtividade e hábitos com evidência, e os estilos de saída
  "learning"/"explanatory" para aprender código.
- **Regras:** domínio pessoal; nunca dado de paciente (caso clínico de estudo só anonimizado); skills de estudo e de
  produtividade moram nos projetos delas, nunca no global (12.4).
- **Mais detalhes do pedido (06/10):** ele já tem **muitos resumos escritos do cursinho** e materiais de resumo com
  imagens e fluxos. O Gemini criava recursos de estudo em tempo real — estudando ECG, montou um "aparato" que movia as
  ondas para ele entender. Quer um módulo de **aprendizagem e dúvidas** no Claude com mnemônicos, fluxogramas, mapas
  mentais, infográficos e recursos interativos iguais ou melhores; um projeto para **tirar dúvidas e fazer resumos**;
  e algo que **pergunte o que foi estudado** (para memorizar) ou **exija que ele escreva** o que estudou. Acha que
  recursos de educação existem mas ficam fora da divulgação, centrada em programação.
- **Fato útil já sabido:** o Claude gera páginas interativas (Artifacts: HTML/JS com controles, publicadas privadas
  pela ferramenta Artifact desta máquina) — uma simulação de ECG com controles é viável; o plugin oficial
  `playground` traz modelos de mapa de conceitos e explorador. A pesquisa em curso foi ampliada com isso (simulações,
  modo de aprendizagem, recuperação ativa, técnica de Feynman, o acervo do cursinho como base consultável).

### 12.6 O guia das skills em Word (pedido de 06/10)

O Ettore reforçou: quer **um arquivo em Word** dizendo o que cada skill faz, quando usar, e se ele a chama por `/`,
se o Claude a chama sozinho, ou se ela vem programada no projeto (CLAUDE.md, regras e documentos sob demanda). Padrão
da casa (memória de 25/09: orientação para ele = Word, gerado por script): `scripts\gerar_guia_skills.py` lê as
skills realmente instaladas e gera `claude-kit\GUIA_DAS_SKILLS.docx`; skill nova sem descrição aparece numa seção
"sem descrição curada". **Regra para o plano:** toda fase que mudar skill, plugin ou o uso por projeto termina
regenerando o guia (o Claude Docs do guia antigo fica como histórico ou é retirado — decidir).

**Feito em 06/10:** `scripts\gerar_guia_skills.py` + `GUIA_DAS_SKILLS.docx` (17 páginas, 41 tabelas; 72 itens
conferidos contra o disco: 28 do kit, 5 de plugin, 15 do claude.ai, 14 de projeto, 10 do Claude Code; "a conta de
hoje": 31 skills chamáveis sozinhas ≈ 3,6 mil tokens por conversa, 1,2 mil delas das skills do claude.ai a desligar).
**Para o plano:** (1) o guia saiu com os vereditos de antes da §12.7 — regenerar depois do plano; (2) o `LEIA-ME.md`
do kit não cita o guia nem o gerador; (3) na fase da planilha, marcar `/fechar-rodada`, `/consolidar` e
`/nova-versao` como só `/` (`disable-model-invocation: true`; hoje nenhum dos 12 comandos tem). Ocorrência: o
subagente do guia rodou um `find` que listou nomes e datas de arquivos nas árvores dos projetos, inclusive em pastas
de dados (sem abrir conteúdo) e o interrompeu; registrado para transparência.

### 12.7 Posições do Ettore depois das verificações (06/10) — mudam vereditos

- **"Não me prive de recursos importantes só por risco de vazamento para a nuvem ou o GitHub; vamos fazer
  workaround quando possível; o GitHub privado é seguro."** Ele é médico, tem direito de acesso aos dados e aceita
  `claude-mem` gravando dado de paciente e repositório privado com dado. → O plano trata privacidade como **decisão
  consciente e escrita**: propor a revisão das regras de privacidade dele (CLAUDE.md pessoal, CLAUDE.md dos projetos,
  memórias "console sem linha de paciente" e "nome de paciente nunca em arquivo versionado") num ADR, com o que muda,
  e apontar uma vez os pontos que não dependem dele (política do hospital/operadora, LGPD art. 11, a opção de treino
  com as conversas no claude.ai). Workaround antes de recusa.
- **Testar na pasta sintética (F3):** Claude Code Setup (quer entender a recusa de Context7, Playwright MCP e GitHub
  MCP), oh-my-claudecode ("OmniClaude"), Headroom no terminal (fora do VS Code), `claude-mem` (começando por um
  projeto sem dado clínico: pesquisa ou estudo).
- **Cartographer:** "não me importo de jogar arquivo de dado no mapa" → permitido, com a ressalva de custo (dado não é
  código; o mapa incha e entra no contexto) e sem o passo que edita o CLAUDE.md; candidato ao kernel (F6), comparado
  com a `improve-codebase-architecture`.
- **Recursos recusados em 04/10, reconsiderados por projeto:** Context7 no DASH (React 19, Vite, Tailwind, TanStack:
  bibliotecas que mudam rápido); Playwright MCP só numa janela de depuração; GitHub MCP (ou `gh`) se ele passar a usar
  issues, PRs ou a nuvem.
- **Pesquisa:** conector oficial do PubMed "seria excelente" e outros indexadores também (Europe PMC, OpenAlex,
  Crossref, Unpaywall pela `paper-lookup`; outros que a pesquisa achar).
- **A pasta-mãe `CLAUDE-PROJETOS`:** ele pergunta se reunir tudo nela é inteligente ou se mistura projetos e injeta
  token onde não deve. Resposta dada no chat (06/10): a pasta em si não injeta nada; injeta o que a sessão carrega
  (CLAUDE.md da pasta aberta e dos ancestrais, o nível de usuário, skills de projeto tocado). Valem as regras da 12.4;
  a janela de orquestração mora no `claude-kit\`, não na raiz.
- Ele começou a configurar o desktop com o `CLAUDE-PROJETOS` em 06/10 (prompt 7 + zip das 07:32).

### 12.3 Sugestão de ordem para a rodada 3

A organização pessoal não tem dado de paciente: é um bom primeiro projeto real no fluxo novo (depois do teste
sintético, F3), antes do piloto no app — o erro ali custa pouco. A comunicação depende da porta de dados do app (F5)
para o preenchimento automático, mas os modelos e as skills podem vir antes, só com marcadores.

### 12.4 Isolamento entre projetos — "que o contexto de um não espirre no outro"

O pedido (06/10): "desenhar uma operação e divisão muito clara para que os projetos não comecem a se misturar",
com ajuda do Claude "desde já". Os projetos agora são de domínios diferentes: trabalho hospitalar com dado de
paciente (app, kernel, planilha HC, comunicação), pesquisa clínica (literatura), pessoal (produtividade), e no
desktop financeiro, RH e acolhimento.

**Por onde o contexto vaza hoje (fatos):**
- tudo o que está no nível de usuário entra em **todo** projeto: o `~\.claude\CLAUDE.md`, a descrição de cada skill
  de `~\.claude\skills` (as 28 do kit), os plugins de escopo de usuário, os ganchos de usuário;
- uma janela aberta na pasta-mãe (`C:\CLAUDE-PROJETOS`) enxerga todos os projetos pelo Glob e pelo Grep;
- a sessão de um projeto pode ler arquivo de outro (às vezes de propósito: o app lê a lei do kernel);
- **tocar em arquivo de outro projeto puxa as skills daquele projeto para a sessão**: visto em 06/10 — esta janela,
  na mãe, leu arquivos do `desosp-censo` e a descrição da skill `rodada` entrou na lista dela ("applies when working
  on files under desosp-censo/");
- **os conectores ligados no claude.ai** (Notion, Google Calendar, Gmail…) **valem em todo projeto do Claude Code**
  quando se está logado; um projeto se protege com `disableClaudeAiConnectors: true` no `.claude\settings.json` e
  declara só os seus no `.mcp.json` (pesquisa `2026-10-06_estudo-anki-e-produtividade.md`);
- a memória automática já é separada por projeto (chave = pasta do repositório): esta camada não vaza.

**O modelo proposto (para o plano confirmar), em cinco camadas:**

| camada | o que mora ali | regra |
|---|---|---|
| 1. global (todo projeto) | o CLAUDE.md pessoal com regras universais; as skills que servem a qualquer projeto (núcleo da `uso-do-claude`, fechamento, orquestração, a família do grill, quase todas só `/`); safety-net; o gancho de abertura único | nada de domínio aqui; cada coisa nova pergunta "serve a todos os projetos?" |
| 2. projeto | o CLAUDE.md do projeto, `.claude\rules`, `.claude\skills` do domínio (ex.: `/email` e `/whatsapp` só na comunicação; as do K-Dense só na pesquisa), `enabledPlugins` do projeto (ex.: Notion só no pessoal; `frontend-design` só onde há tela) | skill e plugin de domínio moram no projeto, nunca em `~\.claude\skills` |
| 3. dados | pastas de dado fora dos repositórios, cada uma com `deny` e `deny_paths` do safety-net | a sessão de um projeto não lê o dado de outro; dado de paciente só entra por porta de leitura com campos mínimos |
| 4. canais | as caixas `docs\para_*\` entre projetos; a `caixa\` do kit entre os PCs; a biblioteca `pesquisas\` (só conhecimento, nunca dado) | informação passa de um projeto a outro **só** por esses canais, como arquivo com índice |
| 5. janelas | uma janela = um projeto; a mãe e o kit não fazem trabalho de projeto; a janela orquestradora (celular) guarda só estado e resumo, nunca dado, e delega a sessões abertas na pasta de cada projeto | a orquestração cruza projetos, o contexto não |

**Uma consequência técnica a avaliar no plano:** skill em `~\.claude\skills` vale para todos os projetos e não se
desliga por projeto; plugin se liga e desliga por projeto (`enabledPlugins`). Empacotar os grupos de skills do kit
como **plugins de um marketplace local** (a própria pasta do kit, clonada nos dois PCs; a conferir:
`claude plugin marketplace add <pasta local>`) deixaria cada projeto ligar só os grupos dele — e combina com a
separação por tipo pedida na 6.1 e com o repositório privado da Q6.

**Desde já, até o plano sair:**
- o material extraído do chat para o agente pessoal vai para uma pasta só de fontes (sugestão de nome:
  `C:\CLAUDE-PROJETOS\pessoal-produtividade\fontes\`), sem janela do Claude Code nela;
- os e-mails do PC do trabalho só chegam depois que a pasta protegida da comunicação existir (12.1);
- nenhuma janela de trabalho de projeto na pasta-mãe;
- nenhum material pessoal num projeto de trabalho, nem o contrário.

**Pergunta para a rodada 3:** confirmar os domínios e o que pode cruzar entre eles (ex.: a pesquisa recebe a
pergunta clínica do trabalho, mas nunca o paciente; o pessoal nunca recebe dado do trabalho; a comunicação lê o app
só pela porta de leitura) e o prefixo dos nomes de pasta por domínio (ex.: `desosp-`, `pesquisa-`, `pessoal-`).

## 13. Sinais de insuficiência do modelo (janela de 05-06/10)

Nenhum. Tropeços de ambiente, não de modelo: a ferramenta Bash engoliu `\\` em heredoc e em JSON (resolvido gravando
em arquivo); uma edição do guia foi recusada por busca ambígua (a busca do conector não diferencia maiúsculas;
resolvido com `nth`).
