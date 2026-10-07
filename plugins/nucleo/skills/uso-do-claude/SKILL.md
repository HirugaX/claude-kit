---
name: uso-do-claude
description: Como escolher modelo e esforço e como organizar o trabalho no Claude Code — janelas, contexto, sessões longas sem interrupção, várias janelas em paralelo, subagentes, handoff — para a melhor qualidade pelo menor uso de tokens; e organizar os projetos e as pastas de um PC (reunir projetos e kit numa pasta-mãe, GitHub, cores das pastas). Use ao recomendar modelo ou esforço, ao abrir ou fechar uma janela, ao escrever o prompt da próxima janela, ao planejar fases, ao delegar a subagentes ou workflows, antes de um trabalho longo sem supervisão, ao organizar os projetos e as pastas de um PC, e quando o usuário perguntar como usar o Claude Code, quanto algo custa ou por que o uso está alto.
---

# Uso do Claude — modelo, esforço e método de trabalho

Fatos verificados em **03/10/2026** e **04/10/2026**; fontes, medições e o que as pesquisas erraram estão em
[reference.md](reference.md). Modelo e preço mudam: se esta data tiver mais de 60 dias, confira
`code.claude.com/docs/en/model-config` antes de afirmar um fato daqui como atual.

## 1. O princípio

Use o **menor modelo e esforço que fecham a tarefa COM verificação**; suba só diante de um
**sinal observável** de insuficiência; e ataque o gargalo certo — especificação, raciocínio,
contexto, verificação ou decomposição. Gastar mais sem atacar o gargalo é o erro mais caro.

O esforço acompanha **o custo de descobrir tarde** o erro daquela fase, não o tamanho dela:
erro silencioso e diferido (escreve em dado vivo, decide identidade, poda, arquiva, define
modelo de dados herdado) pede mais; erro que aparece na tela na hora pede menos.

A medida é o **custo por tarefa concluída corretamente**: tokens + espera + retrabalho + (chance × custo
do erro). E é a **verificação por comando** que deixa descer: com um teste que pega o erro, o Sonnet 5.5
`medium` fecha o que, sem ele, pediria Opus `high` e o olho do usuário. Que recursos um projeto usa
(testes, navegador, ganchos, MCPs, stack): skill `recursos-do-projeto`.

## 2. A escada — nesta ordem

1. **Especificação.** O erro vem de regra ambígua? Escrever a regra, o caso de teste, ou
   entrevistar (`/grill-me`). Esforço não traz a informação que falta.
2. **Esforço `medium → high`.** O modelo entende a tarefa mas não verifica o bastante.
3. **Sonnet → Opus**, antes de empurrar o Sonnet a `xhigh`/`max`.
4. **`xhigh`**, com o motivo escrito (casos de borda escondidos, raciocínio é o gargalo).
5. **Fable 5.1**, só depois de o Opus falhar de verdade num problema de raciocínio longo.
   Não é "o botão faça direito": o Opus 5.5 o supera nos testes de código (do fornecedor e
   independentes), custa ~3× menos por chamada no uso medido, e o Fable gasta a cota semanal mais
   rápido (no Max, até metade dela).
6. **Mais agentes** só com decomposição real (partes independentes, arquivos separados).

`max` nunca é padrão: a documentação o diz propenso a *overthinking* e há medição de `max` pior
que `xhigh`. Vale só para a sessão em que é digitado.

## 2b. Como reconhecer que o modelo não deu conta

Quem vê primeiro é o próprio Claude: ele sabe quantas vezes foi corrigido e quantas tentativas
falharam. Por isso **todo resumo de fim de janela traz a linha
`Sinais de insuficiência do modelo: nenhum`** — ou quais, cada um com o exemplo concreto.

Sinais (qualquer um conta):

1. **O mesmo erro voltou** depois de corrigido, ou o mesmo teste falhou em duas tentativas diferentes.
2. **O usuário corrigiu o raciocínio, não um detalhe**: regra entendida ao contrário, dois casos
   misturados, resposta a outra pergunta.
3. **Contradisse uma decisão já escrita** (CLAUDE.md, handoff, memória) na mesma janela.
4. **Disse que conferiu e não tinha conferido**: teste, invariante ou conferência independente desmentiu.
5. **Gira em círculo**: relê os mesmos arquivos, repete hipóteses sem eliminar nenhuma.
6. **Plano raso**: ignora uma restrição que o usuário citou.

Não são sinais de modelo: faltar regra escrita (é especificação — escrever a regra); o programa
parar numa verificação (é a proteção funcionando); erro que dependia de informação que ninguém deu.

O que fazer:

- 1 sinal: registrar no resumo; naquele tipo de tarefa, a próxima janela sobe o esforço
  (`high → xhigh`).
- O sinal volta no mesmo tipo de tarefa já em `xhigh`, ou 2 sinais na mesma janela: o prompt da
  próxima janela recomenda **Fable 5.1 · `high`** para aquele tipo de tarefa, citando os sinais.
- O Fable também falhou: o gargalo é especificação ou decomposição, não modelo — voltar ao `/grill-me`.

## 3. Ponto de partida por tipo de tarefa

| Tarefa | Começa em | Sinal para subir | Próximo degrau | Verificação |
|---|---|---|---|---|
| rodar comandos e relatar, mudança mecânica, renomear, doc | Sonnet 5.5 `medium` (ou Opus 5.5 `low`) | mexe no que não devia | escopo mais claro → `high` | diff restrito + testes afetados |
| implementar o especificado, com verificação que pega o erro (testes, navegador) | Sonnet 5.5 `medium`, escolhido na lista | falha teste, integra mal | Opus 5.5 `medium` | testes de aceitação; navegador nas telas |
| implementar o especificado sem essa verificação, ou com erro silencioso | Opus 5.5 `medium` | falha invariante, integra mal | `high` | testes de aceitação da especificação |
| bug local reproduzível | Opus 5.5 `medium` | 1ª hipótese falha | `high` | reprodução antes/depois + teste de regressão |
| regra com erro silencioso (dado vivo, identidade, poda, arquivo) | Opus 5.5 `high` | casos de borda escapam | `xhigh` com motivo | invariantes + casos formais |
| bug distribuído, temporal ou de dado | Opus 5.5 `high` | gira sem eliminar hipótese | árvore de hipóteses → `xhigh` | reprodução, logs, invariantes |
| julgar texto (clínico, contrato, especificação) | Opus 5.5 `high` | erra o sentido, não o detalhe | Fable 5.1 `high` | gabarito ou conferência por outro método |
| planejar, arquitetura, entrevista `/grill-me` | Opus 5.5 `high` (o melhor disponível) | plano raso, ignora restrição | `xhigh`; Fable se o Opus já falhou nisso | registro de decisão com critérios |
| tela, conferência visual | Sonnet 5.5 `medium` | "parece certo" e a tela não bate | especificação visual melhor, não modelo | testes no navegador (layout, foco, impressão), axe; a captura só apoia |
| importar XLS/CSV/PDF, reconciliar | Opus 5.5 `high` | perde linha, duplica | fixtures e invariantes ANTES de subir | contagens, totais, hashes, golden files |
| buscar, varrer, ler muito | subagente Explore **com** `model: haiku`/`sonnet` (sem ele, herda o da janela) | perde nuance | `sonnet` → `opus` | o principal confere a conclusão |
| revisar código / segurança | Opus 5.5 `high` | concorda com tudo | outro MÉTODO (teste, análise estática) | testes; decisão humana |

## 4. Fatos que mudam a prática

- **O esforço é calibrado por modelo.** O Opus 5.5 em `medium` iguala ou supera o Opus 5 em
  `high` (documentação oficial): ao trocar de geração, desça um nível; não carregue o antigo.
- Padrão de fábrica: Opus 5.5 e Sonnet 5.5 em `medium`; os demais em `high`. Haiku 4.5 não
  tem esforço e tem só 200k de contexto.
- **Mudar o esforço no meio da janela NÃO quebra o cache** (Opus 5.5, Sonnet 5.5, Fable 5.1,
  na assinatura). Então ajuste por etapa: implementar em `medium`, verificar em `high`.
- **Mudar de modelo (`/model`) quebra o cache**: a chamada seguinte relê tudo sem cache. Com
  contexto grande, troque de modelo em janela nova, com handoff.
- **Ler o histórico custa igual no Opus 5.5 e no Sonnet 5.5** (US$ 0,20/MTok em cache). Em
  janela de contexto grande, o tamanho do contexto e o esforço pesam mais que o modelo.
- `ultrathink` no prompt pede raciocínio extra **só naquele turno**, sem mudar o esforço.
- `ultracode` não é nível: liga orquestração de workflows (muitos agentes, avisos pulados).
  Só com pedido explícito. `opusplan` = Opus no modo plano, Sonnet na execução — cada troca de
  modo é troca de modelo (cache recomeça).
- Agent teams gastam ~7× (documentação oficial) e são experimentais.
- Cache dura **1 hora** na assinatura: voltar depois de pausa maior relê tudo sem cache.
- **Rebaixamento silencioso.** Pedido que o classificador de segurança marca como biologia
  (texto clínico pode cair nisso) é refeito no **Opus 5**, e **a janela continua no Opus 5** até
  alguém digitar `/model`. Viu o aviso de troca de modelo no meio da conversa: volte com `/model`.
  No Sonnet 5.5 o mesmo pedido é recusado.
- **O atalho `sonnet` abre o Sonnet 5, não o 5.5** (visto nos registros em 03/10, Claude Code
  2.1.234), tanto em `--model sonnet` quanto em `/model sonnet`. Para o Sonnet 5.5, escolha-o
  **na lista** do `/model` ou use o ID completo `claude-sonnet-5-5`. Para conferir o modelo que
  rodou: `medir_uso.py --sessoes`, ou o `modelUsage` da saída `--output-format json`.
  **Aconteceu de novo em 03/10 à noite**: a FF-P3c do app rodou as 188 chamadas no Sonnet 5 com o prompt
  dizendo 5.5, e ninguém percebeu. Regra em skill não chega ao momento de escolher o modelo; chega a 1ª
  linha do prompt e o aviso de um gancho de abertura (o `SessionStart` recebe o modelo da sessão).
- **O `/effort` grava.** Confirmado com `Enter`, ou digitado como `/effort xhigh`, o nível vira o padrão
  daquele modelo (`modelSettings` do `settings.json` do usuário) para **todas as janelas seguintes, de todos
  os projetos**; o seletor de modelo do VS Code grava igual. `s` no seletor do `/effort` vale só para a
  sessão (v2.1.257+); `max` e o `/effort` de um `-p` nunca gravam. Visto em 04/10: `xhigh` gravado no Opus
  5.5, contra a régua. Por isso o prompt traz o **comando** `/effort <nível>` na 1ª linha, sempre.
- Um `settings.json` **do projeto** vence o do usuário, modelo a modelo (`modelSettings`): dá para fixar o
  esforço padrão de um projeto. Não testado: se isso atrapalha um `/effort` no meio da janela.
- A palavra `ultracode` escrita em qualquer mensagem dispara um workflow; `Alt+W` cancela.
- Em tarefa bem delimitada, Sonnet 5.5 `medium` e Opus 5.5 `medium` acertam igual e o Sonnet
  custa metade (teste reproduzível). Em extração factual, o Sonnet erra mais (Artificial
  Analysis: 54% contra 66% do Opus 5.5 e 67% do Fable 5.1). Em julgamento de texto, o Opus 5.5
  e o Fable 5.1 não se distinguiram num teste cego, com o Opus pela metade do custo.

## 5. Contexto — o custo que mais pesa

Cada chamada reenvia a conversa inteira. Uma pergunta de uma linha numa janela de 400 mil
tokens custa 400 mil. Por isso:

- **Continuar** enquanto o histórico é informação útil (hipótese refinada, decisão difícil de
  reconstruir).
- **`/compact <o que preservar>`** num ponto natural, quando o passado virou peso mas o objetivo
  é o mesmo (compactar contexto grande é, ele mesmo, uma chamada grande).
- **`/clear` ou janela nova** quando o assunto mudou ou o estado já está no disco. `/clear` não
  custa nada.
- Dividir por **fase e assunto**, nunca por número de mensagens ou horas.
- Heurística (não é medição): passou de ~250 mil, no próximo ponto natural, compactar ou
  fechar com handoff.
- A compactação automática dos modelos de 1M só acontece **perto do limite** (~1 milhão). Para
  ela agir antes, `/autocompact 400k` (por modelo) ou `"autoCompactWindow"` no `settings.json`.
  Para trabalho longo, a própria Anthropic achou que compactar não basta: o que funciona é estado
  escrito em arquivo e contexto novo — o handoff.
- Instrução que mora em comentário HTML (`<!-- … -->`) no `CLAUDE.md` não custa token.
  `/doctor prompt-audit` aponta instrução velha, contraditória ou que cita arquivo inexistente.
  Só funciona numa janela interativa e com o Claude Code **2.1.283 ou mais novo**
  (`claude update`). Em versão anterior, ou no `-p`, não imprime nada.
- `CLAUDE.md` é custo fixo de toda chamada: alvo oficial **< 200 linhas**. O resto vai para
  `.claude/rules/*.md` com `paths:` (carrega só ao mexer nos arquivos), para skills ou para
  documentos lidos sob demanda.
- **Estado mutável fora do que carrega sempre.** `CLAUDE.md`: comandos, invariantes, nunca/sempre. O
  estado (onde estamos, o próximo) num handoff **curto**; o histórico num arquivo à parte, lido por busca.
  Estado no `CLAUDE.md` envelhece e contradiz o handoff; handoff que só cresce faz o "leia o alto" virar um
  parágrafo velho de 40 linhas (o do app tinha 538 KB em 04/10).
- Plugins e MCPs que o projeto não usa pesam em toda sessão: a descrição de cada skill entra em toda
  chamada, e a lista (~1% da janela), quando estoura, tem descrições **cortadas** — as suas inclusive. Os
  esquemas de ferramenta MCP ficam adiados (só nome e instrução); o que pesa do MCP é o resultado.
- Micro-otimização não paga: encurtar frase de `CLAUDE.md` não se compara a um log de 20 mil linhas, uma
  árvore de acessibilidade ou quatro agentes repetindo a mesma busca.
- Material volumoso (logs, varredura, páginas da web, documentação) → subagente, que devolve
  só a conclusão.
- **Antes de pesquisar, procurar; depois, salvar.** A biblioteca é
  `C:\CLAUDE-PROJETOS\claude-kit\pesquisas\`: comece pelo `INDICE.md`; pesquisa que já está lá não se
  refaz (só se o "conferir de novo depois de" venceu). Pesquisa nova vira um arquivo
  `AAAA-MM-DD_assunto.md` com o cabeçalho fixo (a pergunta, a data, o projeto que pediu, as fontes com
  link, a conclusão em poucas linhas, "conferir de novo depois de") e uma linha no índice. O subagente
  devolve; quem salva é a janela principal. Nunca dado de paciente nem trecho de documento da operadora.

## 6. Uma janela — abrir, trabalhar, fechar

- Uma janela = um projeto (aberta na pasta dele) e uma fase.
- Ao abrir: o ritual fixo (atualizar o repositório, ler a caixa de entrada, ler o handoff) é
  trabalho de **hook `SessionStart`**, não de instrução em texto. O gancho imprime só o resumo — o git
  e o arquivo que outra janela deixou sem commit, os itens pendentes da caixa, a seção do handoff, o
  esforço gravado, o modelo — e o texto entra no contexto. Modelo pronto:
  `C:\CLAUDE-PROJETOS\desosp-app\.claude\hooks\abertura.py`.
- Duas fases na mesma janela (ex.: julgar e depois executar): na virada, **baixe o esforço**
  (`/effort medium`), que é grátis; trocar de modelo relê o contexto inteiro. Plano aprovado:
  seguir na mesma janela é o certo; o que não se faz é `/clear` ou `/model` no meio.
- Ao fechar: (1) registrar o estado **no repositório** — objetivo, decisões, arquivos
  alterados, testes, hipóteses descartadas, próximo passo, condição de término; (2) entregar o
  prompt da próxima janela com **o modelo e o comando `/effort <nível>` na 1ª linha** (§4: o nível
  gravado é o da última janela que confirmou um); (3) parar quando o modelo muda.
- Regra que ficou só no chat não existe para a próxima janela.

## 7. Várias janelas em paralelo

- Cada janela na pasta do seu projeto; nunca duas janelas editando os mesmos arquivos (se
  precisar, `worktree`). Commit por caminho explícito, nunca `git add -A`.
- O `git push` leva **todos** os commits locais do ramo, os de outra janela também (visto em
  04/10: o push de uma janela levou o commit que a FF-T acabara de fazer). Antes de empurrar,
  `git log origin/main..` diz o que vai junto; commit alheio pronto pode ir, mas diga no resumo.
- Mensagem entre sessões chega como turno novo e custa o contexto inteiro de quem recebe:
  prefira caixa de entrada em arquivo, lida ao abrir.
- Só é paralelo o que é independente. Se B depende da decisão de A, é sequência.

## 8. Trabalho longo sem interrupção

Duração não pede esforço maior; pede **estrutura**:

- objetivo verificável; escopo (o que pode e o que não pode mexer); invariantes; critério de
  aceitação executável; política de falha (N tentativas diferentes no mesmo erro → registrar o
  bloqueio e parar aquela linha); checkpoint por commit; prova de término (comandos, resultado,
  diff, o que ficou de fora).
- **`/goal <condição>`**: um avaliador confere a condição a cada turno e mantém a sessão
  andando. A condição tem de ser demonstrável pela saída do Claude ("`pytest -q` passa com 0
  falhas e o relatório X foi gravado"), porque o avaliador não roda nada sozinho.
- O que interrompe é pedido de permissão: modo auto + lista de permissões
  (`/fewer-permission-prompts`). O que precisa ser proibido vai em permissão ou hook.
- Sessão local precisa da máquina acordada; com a máquina desligada, só sessão na nuvem.

## 9. Subagentes

- Primeiro degrau de paralelismo: ler, buscar, varrer — sem editar.
- A delegação tem de ser completa: o subagente não viu a conversa.
- Modelo pelo trabalho (parâmetro `model`): `haiku` busca mecânica, `sonnet` extração
  delimitada, `opus` julgamento. Sem parâmetro, herda o da janela — **o Explore e o Plan também**
  (a pesquisa de 04/10 errou nisso); para o Explore ter Haiku por padrão, um subagente próprio chamado
  `Explore` com `model: haiku`. O Explore e o Plan não carregam o `CLAUDE.md` — é o jeito barato
  de ler muito; os demais subagentes carregam o `CLAUDE.md` inteiro cada um (agente próprio pode pular com `omitClaudeMd: true`).
- Subagente custa: em tarefa pequena, espalhar entre 2 a 5 agentes gastou 2,6× a 5,9× mais
  entrada sem ganhar tempo (teste reproduzível). Vale para material volumoso ou modelo menor.
- **Retomar** um subagente geral ou próprio pelo `SendMessage` mantém o histórico dele — melhor que
  abrir outro para pergunta relacionada. O cache do subagente dura **5 minutos**, mesmo na assinatura.
- Três papéis bastam: o **explorador** (material ruidoso), o **especialista** (modelo maior num ponto
  difícil), o **revisor isolado** (segunda opinião genuína). Mais que isso, só com partes independentes
  em paralelo, ou com modelo ou permissão diferentes.
- Revisores do mesmo modelo erram juntos: para regra crítica, varie o **método** (teste,
  invariante, script independente), não o número de agentes.

## 9b. Testar instrução numa sessão nova (`claude -p`)

Para saber se uma regra **chega** a uma sessão nova (depois de mexer no `CLAUDE.md`, numa skill
ou em `.claude/rules`), faça a pergunta numa sessão nova, uma pergunta por sessão, e compare a
resposta com o texto da regra. Use o script, que já evita os erros de 03/10:

    python C:\CLAUDE-PROJETOS\claude-kit\scripts\perguntas_controle.py perguntas.txt --projeto C:\CLAUDE-PROJETOS\desosp-censo

Se for fazer à mão, siga as quatro regras abaixo. Cada uma custou uma tentativa perdida em 03/10
(KN42):

1. **A pergunta vem logo depois do `-p`, antes das opções.** O `--allowedTools` aceita vários
   valores e engole a pergunta que vem depois dele.
2. **Feche o stdin**: `< /dev/null` no shell, `stdin=DEVNULL` no Python. O `-p` junta à
   pergunta tudo o que chega pelo stdin. Num laço `while read`, cada sessão recebeu o resto do
   arquivo de perguntas.
3. **Modelo pelo ID completo** (`claude-sonnet-5-5`), nunca pelo atalho (§4). Confira o modelo
   que rodou no `modelUsage` da saída `--output-format json`.
4. **Respostas numa pasta nova, com nome que não casa com o do arquivo de perguntas.** Um
   `rm q*.txt` feito para limpar as respostas apagou também o `qs.txt`, que era a lista de
   perguntas.

No Git Bash, um texto que começa com `/` vira caminho do Windows (`/doctor` virou
`C:/Program Files/Git/doctor`). Use `MSYS_NO_PATHCONV=1`, ou rode pelo script.

**O custo fixo de abrir uma sessão se mede do mesmo jeito.** Cada `claude -p` aparece como uma
sessão no `medir_uso.py --sessoes`, com o seu `ctx0`. Para comparar duas versões de um arquivo
de instrução, troque o arquivo, rode, e devolva o original no mesmo comando, conferindo o hash.

## 10. Planejar com `/grill-me`

- `/grill-me` (usa a skill `grilling`) entrevista em rodadas até esgotar as decisões. Use no
  começo da janela de planejamento, com o melhor modelo.
- **Modo plano desligado** durante a entrevista (ele empurra a produzir plano cedo). Terminada,
  modo plano ou especificação **na mesma janela** — o contexto construído é o valor.
- Participar: discordar, dizer "não sei", cortar escopo. Pergunta que só se responde vendo algo
  pede protótipo, não mais perguntas.
- Terminada a entrevista de **projeto novo ou implementação nova**, e confirmado o entendimento: skill
  **`recursos-do-projeto`** antes do plano. Ela liga cada recurso (testes, navegador, ganchos, MCPs,
  stack) a uma resposta da entrevista e diz o que fica de fora.

## 11. Controle real × pedido em texto

Permissão, hook, teste e worktree são controle. "Não gaste mais que X", "pare após 3
tentativas", "não mexa fora do módulo" no prompt são só orientação. `effort` não é teto de gasto.

**Verificar por comando; ferramenta por CLI.** O que um comando responde (teste, lint, navegador,
acessibilidade, varredura) não se confere de cabeça: "linha 43 viola X" custa menos e erra menos que
provar a ausência de erro raciocinando. Para o que é determinístico, CLI antes de MCP; MCP para estado
externo ou introspecção interativa.

## 12. Ao recomendar modelo e esforço

Diga modelo + esforço + o porquê em uma linha (o custo de descobrir tarde o erro daquela fase)
+ o sinal que mandaria subir ou descer. O esforço vai como **comando** (`/effort high`), e o Sonnet
como "Sonnet 5.5, escolhido na lista do `/model`" (§4). Regra do projeto vence esta quando conflitar.

## 13. Organizar os projetos e as pastas de um PC

Só por `/`, no kit e na janela da raiz (plugin `kit`): `/organizar-projetos`, `/cores-das-pastas`, `/icones`.
