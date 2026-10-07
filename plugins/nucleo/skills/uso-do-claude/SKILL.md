---
name: uso-do-claude
description: "Núcleo do uso do Claude Code: escada de modelo e esforço, sinais de insuficiência, armadilhas, contexto, janela por fase, planejar. Use ao abrir janela, planejar ou explicar o custo."
---

# Uso do Claude — o núcleo

Fatos conferidos de 03 a 07/10/2026; as fontes, as medições e o que as pesquisas erraram estão em
[reference.md](reference.md) (consulta). Com esta data a mais de 60 dias, confira `code.claude.com/docs/en/model-config`
antes de afirmar um fato daqui como atual. A regra do projeto vence esta quando as duas conflitarem.

As peças, cada uma no seu momento: **`modelo-e-esforco`** (recomendar modelo e `/effort`), **`fechar-janela`**
(estado, próximo prompt, resumo, push), **`pesquisa`** (biblioteca → subagente → salvar), **`orquestrar`** (subagentes,
SDD, Workflow, várias janelas, execução largada), **`recursos-do-projeto`** (o que um projeto usa). Só por `/`, no kit
e na janela da raiz: `/organizar-projetos`, `/cores-das-pastas`, `/icones`.

## 1. O princípio

Use o **menor modelo e esforço que fecham a tarefa COM verificação**; suba só diante de um **sinal observável** de
insuficiência; e ataque o gargalo certo: especificação, raciocínio, contexto, verificação ou decomposição. O esforço
acompanha **o custo de descobrir tarde** o erro daquela fase, não o tamanho dela: erro silencioso e diferido (dado vivo,
identidade, poda, modelo de dados herdado) pede mais; erro que aparece na tela na hora pede menos. A medida é o **custo
por tarefa concluída corretamente**: tokens + espera + retrabalho + (chance × custo do erro). É a verificação por
comando que deixa descer: com um teste que pega o erro, Sonnet 5.5 `medium` fecha o que pediria Opus `high`.

## 2. A escada — nesta ordem

1. **Especificação.** Erro de regra ambígua: escrever a regra, o caso de teste, ou entrevistar (`/grill-me`).
2. **Esforço `medium → high`.** O modelo entende a tarefa mas não verifica o bastante.
3. **Sonnet → Opus**, antes de empurrar o Sonnet a `xhigh`/`max`.
4. **`xhigh`**, com o motivo escrito (casos de borda escondidos; o raciocínio é o gargalo).
5. **Fable 5.1**, só depois de o Opus falhar de verdade num raciocínio longo: o Opus 5.5 o supera em código, custa ~3×
   menos por chamada, e o Fable gasta a cota semanal mais rápido.
6. **Mais agentes**, só com decomposição real (partes independentes, arquivos separados): `orquestrar`.

`max` nunca é padrão (propenso a *overthinking*; medido pior que `xhigh`). `max`, `xhigh`, Fable e ultracode só com
motivo escrito, e subir pede o "sim"; descer, mantida a qualidade, não pede.

## 3. Sinais de insuficiência do modelo

Quem vê primeiro é o próprio Claude. **Todo resumo de fim de janela traz a linha `Sinais de insuficiência do modelo:
nenhum`** — ou quais, cada um com o exemplo. Contam:

1. o mesmo erro voltou depois de corrigido, ou o mesmo teste falhou em duas tentativas diferentes;
2. o usuário corrigiu o raciocínio, não um detalhe (regra ao contrário, casos misturados, resposta a outra pergunta);
3. contradisse uma decisão já escrita (CLAUDE.md, `ESTADO.md`, ADR, memória) na mesma janela;
4. disse que conferiu e não tinha conferido (teste ou conferência independente desmentiu);
5. gira em círculo: relê os mesmos arquivos, repete hipóteses sem eliminar nenhuma;
6. plano raso: ignora uma restrição que o usuário citou.

Não contam: faltar regra escrita (é especificação), o programa parar numa verificação (é a proteção), erro que dependia
de informação que ninguém deu. **O que fazer:** 1 sinal → a próxima janela sobe o esforço naquele tipo de tarefa; o
sinal volta já em `xhigh`, ou 2 sinais na mesma janela → o prompt da próxima recomenda Fable 5.1 · `high` para aquele
tipo de tarefa, citando os sinais; o Fable também falhou → o gargalo é especificação ou decomposição: `/grill-me`.

## 4. As armadilhas

- **O atalho `sonnet` abre o Sonnet 5**, não o 5.5, em `/model sonnet` e `--model sonnet` (medido em 03/10: a FF-P3c do
  app rodou 188 chamadas no Sonnet 5 com o prompt dizendo 5.5). O Sonnet 5.5 se escolhe **na lista** do `/model` ou
  pelo ID `claude-sonnet-5-5`. **Subagente com `model: sonnet` roda no 5.5** (conferido em 06/10): ali o atalho resolve
  pela tabela da documentação — a não ser que a janela já esteja num Sonnet, cujo modelo exato o subagente herda.
- **O `/effort` grava**: confirmado com `Enter`, ou digitado (`/effort xhigh`), vira o padrão daquele modelo para todas
  as janelas seguintes, de todos os projetos. `s` no seletor vale só para a sessão; `max` nunca grava. Por isso todo
  prompt traz o **comando** `/effort <nível>` na 1ª linha.
- **Rebaixamento silencioso**: pedido que o classificador marca como biologia (texto clínico pode cair nisso) é refeito
  no **Opus 5**, e a janela continua nele até alguém digitar `/model`. Viu o aviso de troca de modelo: `/model`.
- **`/model` quebra o cache** (a chamada seguinte relê tudo sem cache); **mudar o esforço não quebra** (Opus 5.5,
  Sonnet 5.5, Fable 5.1). Ajuste o esforço por etapa; troque de modelo em janela nova.
- **O esforço do subagente**: a documentação não diz se ele herda o da janela; na semana de 29/09, 1.197 chamadas do
  Sonnet 5.5 rodaram em `max`, quase todas em subagentes. Fixe o esforço por papel: `orquestrar`.
- **A palavra `ultracode`** escrita numa mensagem dispara um workflow (`Alt+W` cancela).

## 5. Contexto — o custo que mais pesa

Cada chamada reenvia a conversa inteira: uma pergunta de uma linha numa janela de 400 mil tokens custa 400 mil.

- **Continuar** enquanto o histórico é informação útil; **`/compact <o que preservar>`** num ponto natural, quando o
  passado virou peso mas o objetivo é o mesmo; **`/clear` ou janela nova** quando o assunto mudou ou o estado já está
  no disco (`/clear` não custa nada). Dividir por fase e assunto, nunca por número de mensagens.
- **Estado em arquivo, não na conversa** (`docs\ESTADO.md`, `docs\PROXIMO.md`, ADR: `fechar-janela`). Nada de estado
  no `CLAUDE.md`: ele é custo fixo de toda chamada (alvo < 200 linhas) e envelhece sem ninguém ver. Regra que ficou só
  no chat não existe para a próxima janela.
- Material volumoso (logs, varreduras, páginas, documentação) → subagente, que devolve só a conclusão (`orquestrar`).
- Plugins e MCPs que o projeto não usa pesam em toda sessão (a descrição de cada skill entra em toda chamada): cada
  projeto liga só os grupos dele (`enabledPlugins`).
- Micro-otimização não paga: encurtar frase de `CLAUDE.md` não se compara a um log de 20 mil linhas no contexto.

## 6. Uma janela

- **Uma janela = um projeto** (aberta na pasta dele) **e uma fase**. Duas janelas nunca editam os mesmos arquivos.
- **Abrir:** o ritual fixo (git, caixa, estado, modelo e esforço) é trabalho de gancho `SessionStart`, não de texto.
- **Fechar** pelo que vier primeiro: fim da fase, ~150 mil tokens ou troca de modelo. Como: `fechar-janela`.
- Duas etapas na mesma janela (julgar e depois executar): na virada, **baixe o esforço** (grátis); não troque de modelo.
- **Plano na mesma janela da entrevista** — o contexto construído é o valor. **Exceção (Q15):** acima de ~200 mil
  tokens, o registro escrito da entrevista e o plano vão para uma janela nova (começa com ~60-80 mil em vez de ~550 mil).

## 7. Planejar

1. `/grill-me` (skill `grilling`) com o melhor modelo e o **modo plano desligado** (ele empurra a produzir plano cedo).
   Participar é discordar, dizer "não sei", cortar escopo; pergunta que só se responde vendo pede protótipo.
2. Projeto novo ou implementação nova, entendimento confirmado: **`recursos-do-projeto`** antes do plano.
3. O plano.
4. **A rodada de contingências** (Q36), no fim de **todo** grill e de **todo** plano, antes do "sim": liste as situações
   prováveis da execução — dúvida de escopo, teste que falha, dado ou arquivo inesperado, alternativa técnica, limite de
   uso, escrita em dado real — e, para cada uma, *situação → o que fazer → limite*. O usuário aprova em lote. O aprovado
   vira "Decisões pré-aprovadas" do `PROXIMO.md`; o que não se pré-aprova vira "Sempre me pergunte" (`fechar-janela`).

## 8. Pontos de checagem de recursos (Q14)

Quando a tarefa parece fugir do que o projeto tem (linguagem, integração ou tipo de arquivo novo, procedimento que vai
se repetir 3 vezes, verificação que só se faz de olho), **pare e procure antes de improvisar**: a biblioteca
(`pesquisa`), a `find-skills`, a `recursos-do-projeto` (com a descoberta opcional pelo `claude-code-setup`). "Recurso"
= plugin, skill, repositório, MCP, CLI. Instalar é com o "sim"; o que é de terceiros entra no kit pelo
`scripts\atualizar_terceiros.py`. O CLAUDE.md de cada projeto tem a seção "Skills deste projeto" (≤ 10 linhas) e o
`.claude\settings.json` liga os grupos dele; a `engenharia` (código) liga por projeto, nunca no escopo de usuário
(`python C:\CLAUDE-PROJETOS\claude-kit\scripts\instalar_kit.py --trecho codigo`).

## 9. Controle real × pedido em texto

Permissão, gancho, teste e worktree são controle; "não gaste mais que X", "pare após 3 tentativas" no prompt são só
orientação, e `effort` não é teto de gasto. O que um comando responde (teste, lint, navegador, acessibilidade,
varredura) não se confere de cabeça; para o que é determinístico, CLI antes de MCP. Para saber se uma regra **chega**
a uma sessão nova: [testar-instrucao.md](testar-instrucao.md).
