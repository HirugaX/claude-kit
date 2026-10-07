---
name: modelo-e-esforco
description: "Recomendar modelo e /effort por tarefa ou fase, e a 1ª linha do prompt."
---

# Modelo e esforço

O princípio, a escada, os sinais de insuficiência e as armadilhas (o atalho `sonnet`, o `/effort` que grava, o
rebaixamento para o Opus 5) estão no núcleo, a skill `uso-do-claude`; as fontes, no `reference.md` dela. A regra do
projeto vence esta quando as duas conflitarem.

## Ao recomendar

Diga **modelo + esforço + o porquê em uma linha** (o custo de descobrir tarde o erro daquela fase) **+ o sinal** que
mandaria subir ou descer. O esforço vai como **comando** (`/effort high`): o `/effort` digitado grava o padrão, e a
1ª linha do prompt é o que chega ao momento de escolher. O Sonnet vai como "Sonnet 5.5 (escolha-o na lista do
`/model`)" ou pelo ID `claude-sonnet-5-5`, nunca `sonnet`.

A 1ª linha de todo prompt de janela:

    Opus 5.5 · /effort high — <o porquê, em uma linha>; suba para <x> se <o sinal>.

Subir para Fable, `xhigh`, `max` ou ultracode é decisão do usuário, com o motivo escrito; descer, mantida a qualidade,
não pede. Nenhuma fase troca de modelo no meio (quebra o cache); trocar o esforço no meio pode.

## Ponto de partida por tipo de tarefa

| tarefa | começa em | sinal para subir | próximo degrau | verificação |
|---|---|---|---|---|
| rodar comandos e relatar, mudança mecânica, renomear, doc | Sonnet 5.5 `medium` (ou Opus 5.5 `low`) | mexe no que não devia | escopo mais claro → `high` | diff restrito + testes afetados |
| implementar o especificado, com verificação que pega o erro | Sonnet 5.5 `medium`, da lista | falha teste, integra mal | Opus 5.5 `medium` | testes de aceitação; navegador nas telas |
| implementar o especificado sem essa verificação, ou com erro silencioso | Opus 5.5 `medium` | falha invariante, integra mal | `high` | testes de aceitação da especificação |
| bug local reproduzível | Opus 5.5 `medium` | 1ª hipótese falha | `high` | reprodução antes/depois + teste de regressão |
| regra com erro silencioso (dado vivo, identidade, poda, arquivo) | Opus 5.5 `high` | casos de borda escapam | `xhigh` com motivo | invariantes + casos formais |
| bug distribuído, temporal ou de dado | Opus 5.5 `high` | gira sem eliminar hipótese | árvore de hipóteses → `xhigh` | reprodução, logs, invariantes |
| julgar texto (clínico, contrato, especificação) | Opus 5.5 `high` | erra o sentido, não o detalhe | Fable 5.1 `high` | gabarito ou conferência por outro método |
| planejar, arquitetura, `/grill-me` | Opus 5.5 `high` | plano raso, ignora restrição | `xhigh`; Fable se o Opus já falhou nisso | registro de decisão com critérios |
| tela, conferência visual | Sonnet 5.5 `medium` | "parece certo" e a tela não bate | especificação visual melhor, não modelo | testes no navegador, axe; a captura só apoia |
| importar XLS/CSV/PDF, reconciliar | Opus 5.5 `high` | perde linha, duplica | fixtures e invariantes ANTES de subir | contagens, totais, hashes, golden files |
| buscar, varrer, ler muito | subagente com `model: haiku`/`sonnet` e esforço fixado (`orquestrar`) | perde nuance | `sonnet` → `opus` | o principal confere a conclusão |
| revisar código ou segurança | Opus 5.5 `high` | concorda com tudo | outro MÉTODO (teste, análise estática) | testes; decisão humana |

Janela principal: Opus 5.5, `medium` por padrão, `high` em plano e regra clínica (Q5); o mecânico vai a subagentes.

## Fatos que mudam a escolha

- **O esforço é calibrado por modelo.** O Opus 5.5 em `medium` iguala ou supera o Opus 5 em `high`: ao trocar de
  geração, desça um nível. Padrão de fábrica: Opus 5.5 e Sonnet 5.5 em `medium`; os demais em `high`. Haiku 4.5 não tem
  esforço e tem só 200 mil de contexto.
- **Ler o histórico custa igual no Opus 5.5 e no Sonnet 5.5** (US$ 0,20/MTok em cache): em janela grande, o tamanho do
  contexto e o esforço pesam mais que o modelo. No uso medido, o maior custo é o contexto acumulado; depois, o esforço;
  por último, o modelo.
- Em tarefa bem delimitada, Sonnet 5.5 `medium` e Opus 5.5 `medium` acertam igual e o Sonnet custa metade (teste
  reproduzível). Em extração factual o Sonnet erra mais (54% contra 66% do Opus 5.5 e 67% do Fable 5.1). Em julgamento
  de texto, Opus 5.5 e Fable 5.1 não se distinguiram num teste cego, com o Opus pela metade do custo.
- `ultrathink` no prompt pede raciocínio extra **só naquele turno**, sem mudar o esforço. `opusplan` = Opus no modo
  plano, Sonnet na execução: cada troca de modo é troca de modelo (o cache recomeça). `ultracode` não é nível: liga a
  orquestração de workflows (muitos agentes, avisos pulados); só com motivo escrito.
- Os campos `model` e `effort` no cabeçalho de uma skill valem enquanto ela está ativa, e o `effort` na definição de um
  subagente vence o da sessão (não a variável `CLAUDE_CODE_EFFORT_LEVEL`).
- Um `settings.json` do projeto vence o do usuário, modelo a modelo (`modelSettings`): dá para fixar o esforço padrão
  de um projeto.
- Para conferir o modelo que rodou de fato: `python C:\CLAUDE-PROJETOS\claude-kit\scripts\medir_uso.py --sessoes`, o
  `modelUsage` do `--output-format json`, ou a semana em `claude-kit\metricas\uso-semanal.csv`
  (`scripts\medir_semana.py`).
