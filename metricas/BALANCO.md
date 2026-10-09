Opus 5.5 · /effort medium — o balanço compara números com metas e propõe ajustes; o erro aqui só atrasa um ajuste (a decisão é do Ettore, pela fila); suba para high se os números não fecharem entre o CSV e a planilha.

<!-- O prompt fixo do balanço quinzenal das métricas (Q42; plano, Ficha item 8). O gancho de abertura do nucleo avisa
quando ele vence (15 dias desde o último metricas\balancos\AAAA-MM-DD.md). Roda na janela da raiz, C:\CLAUDE-PROJETOS
(decisão de 07/10); lançá-lo sozinho é do F3c. Só números: nada de texto de conversa, nome nem pseudônimo. -->

Janela aberta em C:\CLAUDE-PROJETOS (a janela da raiz). Antes: git -C claude-kit pull --ff-only; git -C claude-kit status sem arquivo de outra janela (a linha semanal nova que o gancho gravou em metricas\ é esperada).

/goal metricas\balancos\<hoje>.md gravado com a tabela da régua e as propostas, cada proposta na fila do kit (claude-kit\docs\PERGUNTAS.md), e o commit feito — ou: tudo o que sobra depende de claude-kit\docs\PERGUNTAS.md

## Contexto
- claude-kit\metricas\uso-semanal.csv (uma linha por semana e por PC; só números) e claude-kit\metricas\ctx0-por-projeto.csv.
- claude-kit\metricas\metas.json: a régua, a base (semana de 29/09) e a meta de cada métrica — a única fonte das metas.
- O último balanço em claude-kit\metricas\balancos\ (se houver): as propostas dele e o que o Ettore respondeu na fila.
- O porquê das métricas: claude-kit\decisoes\2026-10-06_R1-objetivo-medicao-recursos.md (Q34, Q39, Q42) e a "Verificação de ponta a ponta" do claude-kit\decisoes\2026-10-06_plano-fluxo.md.

## O que fazer
1. Semanas que faltam: python claude-kit\plugins\nucleo\ganchos\semana.py --pendentes; se listar alguma, rode python claude-kit\plugins\nucleo\ganchos\semana.py (mede e refaz a planilha). Nunca leia as transcrições direto: só os números que o medir_semana.py imprime.
2. A tabela da régua, por PC: métrica · base · as semanas desde o último balanço · meta · tendência (melhora, piora, parada) · na meta? Some também o ctx0 por projeto e o "fora_da_planilha" do metas.json onde houver número.
3. As propostas: para cada métrica longe da meta ou piorando duas semanas seguidas, um ajuste concreto no kit (gancho, skill, configuração, modelo ou esforço por papel), com a evidência em números. Até 5, da maior para a menor folga. Sem proposta onde a régua está na meta.
4. Cada proposta vai para a fila do kit, claude-kit\docs\PERGUNTAS.md, no formato do modelo (claude-kit\plugins\nucleo\skills\fechar-janela\modelos\PERGUNTAS.md): o problema com o número, a pergunta, as opções, a recomendação e o que depende dela. Crie o arquivo pelo modelo se não existir.
5. Grave claude-kit\metricas\balancos\<AAAA-MM-DD>.md: a tabela, as propostas (com o número de cada uma na fila) e uma linha "Sinais de insuficiência do modelo".

## Limites
- Não mude skill, gancho nem configuração: só propõe. Quem decide é o Ettore, pela fila; quem aplica é uma janela do kit.
- Nada de texto das conversas, nome nem pseudônimo; só números, datas e nomes de projeto.
- Nenhum projeto aberto (desosp-*, pesquisa-*, estudo-*, pessoal-*).

## Ao fechar
Commit no kit por caminho explícito: metricas\balancos\<data>.md, docs\PERGUNTAS.md e, se o passo 1 gravou, metricas\uso-semanal.csv e metricas\ctx0-por-projeto.csv (a planilha fica fora do git). Push depois de git -C claude-kit log origin/main.. (o push leva todo commit local). Resumo no chat: a régua em 5 linhas, as propostas com o número na fila e "Sinais de insuficiência do modelo".
