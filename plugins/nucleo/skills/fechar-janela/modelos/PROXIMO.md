<Modelo> · /effort <nível> — <o porquê, em uma linha: o custo de descobrir tarde o erro desta fase>; suba para <x> se <o sinal>.

<!-- Modelo do docs\PROXIMO.md (skill fechar-janela): o prompt da próxima janela, conferido pela janela que fecha.
A 1ª linha é sempre modelo + o COMANDO /effort (o /effort digitado grava o padrão; o Sonnet 5.5 vai pelo ID
claude-sonnet-5-5: o atalho "sonnet" abre o 5.5 desde a 2.1.291, mas muda entre versões). Nada de nome de paciente
nem pseudônimo: este texto pode virar linha de comando do claude --bg. Apague este comentário. -->

Janela aberta em <pasta>. Antes: <pré-condições conferíveis: git pull --ff-only, git status limpo, o que deve existir>.

/goal <portão desta fase, demonstrável pela saída: "pytest -q passa com 0 falhas e docs\ESTADO.md foi reescrito"> — ou: tudo o que sobra depende de docs\PERGUNTAS.md, gravado com o ESTADO.md

## Contexto
- <o que ler, com caminho; só o necessário: docs\ESTADO.md, o ADR, a seção do plano>

## O que fazer
1. <passo, com o critério de pronto>
2. <...>

## Limites
- <o que não se mexe; pastas de outro projeto; o que é de outra fase>

## Escritas em dado real aprovadas
| comando ou rotina | pasta | limite |
|---|---|---|
| <ex.: python scripts\rodada.py --aplicar> | <C:\CLAUDE-PROJETOS\<projeto>-dados\saida> | <uma vez; só a rodada de DD/MM> |

<Nenhuma, se a fase não escreve em dado real. Fora desta tabela, escrita em dado real é ponto da Q10: nunca sem o "sim".>

## Decisões pré-aprovadas
<!-- Da rodada de contingências do plano (Q36), aprovada em lote: situação → o que fazer → limite. -->
| situação | o que fazer | limite |
|---|---|---|
| <ex.: um teste antigo falha por causa de data fixa> | <corrigir o teste, commit à parte> | <só testes; nada de código de produção> |

## Sempre me pergunte
- <o que nunca se decide sozinho nesta fase, além dos pontos da Q10>

## Ao fechar
Portão: <comandos e números>. docs\ESTADO.md reescrito; docs\PERGUNTAS.md com o que ficou; o PROXIMO.md da fase seguinte. Resumo com "Sinais de insuficiência do modelo".
