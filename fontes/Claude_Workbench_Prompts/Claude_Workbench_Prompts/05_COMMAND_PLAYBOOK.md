# Guia de uso — poucos comandos, nomes reais

Você deve conseguir explicar o trabalho em linguagem natural. O router escolhe procedimentos pertinentes; comando explícito serve para mudar o modo de trabalho ou delimitar efeitos importantes. Não existe obrigação de chamar uma skill a cada tarefa.

Este guia distingue nomes encontrados no GitHub de interfaces desejadas ainda não instaladas. Registro no GitHub não prova que o Claude da sua máquina descobriu o comando. O health check local deve produzir `COMMANDS_RESOLVED.md` com os namespaces e sintaxes exatos.

## Como pedir no dia a dia

| Intenção | Pedido simples | Quando usar |
|---|---|---|
| Executar rotina | “Corrija X conforme a regra Y e verifique.” | Bug/mudança bem delimitados |
| Esclarecer | “Questione os requisitos antes de implementar.” | Ambiguidade com impacto; não para typo |
| Desenvolver | “Implemente a feature da spec X.” | Objetivo e critérios de pronto definidos |
| Revisar | “Revise esse diff contra o contrato e procure casos extremos.” | Mudança relevante ou erro silencioso |
| UI | “Faça a alteração e confira no navegador e nas capturas.” | Mudança visual/fluxo; cumprir regras existentes |
| Limpar contexto | “Continue essa tarefa em uma sessão limpa.” | Fase nova ou exploração contaminando implementação |
| Trabalho longo | “Execute a tarefa X em background dentro desses limites.” | Independente, verificável, sem decisão iminente |
| Commit | “Prepare/registre esse conjunto de mudanças.” | Conforme política específica do projeto |
| Deploy/migration | “Prepare o deploy/migration para eu revisar.” | Mudança com efeito externo; execução só autorizada |

`/grill`, `/feature`, `/review`, `/frontend`, `/fresh-session`, `/background` como wrapper próprio e `/bootstrap-project` são interfaces propostas. Não apresente todas como comandos instalados. A versão local pode ter `/background` nativo; não o sobrescreva com uma skill de mesmo nome.

## Comandos/skills encontrados nos seus repositórios

| Projeto | Nome observado | Uso e dependências |
|---|---|---|
| DASH financeiro | `/fechar-janela` | Encerrar fase: resultados, aferição, handoff e git; corpo atual inclui commit sem push e depende de `uso-do-claude` |
| DASH financeiro | `/revisao-adversarial` | Revisão contra spec, números e cenários; chama `fechar-janela` ao terminar |
| DESOSP app | `/revisar-tela` | Evidência visual, estados, teclado, contraste, impressão, testes e capturas |
| DESOSP kernel/Excel | `/rodada` | Procedimento de extração/processamento e reporte; distinguir operação real de desenvolvimento |
| HC Excel, projeto adicional | `/nova-rodada`, `/rodada`, `/consolidar`, `/boletins`, `/placar`, `/mensagem`, `/ler-pdfs`, `/fechar-rodada`, `/novo-hospital`, `/nova-versao`, `/informativo`, `/verificar` | Comandos legados presentes; preservar interfaces úteis e validar efeitos antes de migrar formato |

Não há evidência local ainda da instalação de `/grill-me` ou de uma skill própria de sessão limpa. Não declarar ausência global: o Work não acessou seu `~/.claude` pessoal.

## Qual modo usar por projeto

| Projeto | Esclarecimento antes de alterar | Review necessário | Interface visual | O que exige intenção explícita |
|---|---|---|---|---|
| Financeiro | Competência, reconciliação, classificação e UX ambíguas | Parser, cálculo, schema e decisões persistidas | React/Vite; capturas e testes | Migração, reprocesso de dados, push/deploy conforme política |
| Folha/RH | Base de cálculo, período, exceções, fechamento | Regra de cálculo, acessos, concorrência | Sheets/dialogs somente se existirem | Escrita real, triggers, implantação, fechamento |
| Fila/acolhimento | Prioridade, estados e empates | Estado, concorrência, idempotência | UI da fila se existir | Reset/finalização em massa, triggers e deploy |
| Censo app | Regra assistencial/operacional nova | Identidade, escrita via `APP_`, integração | `/revisar-tela` e suite do navegador | Dado real, schema e efeitos operacionais relevantes |
| Censo kernel/Excel | Fonte, âncora e insumo ambíguos | Pipeline e preservação de dados | Workbook e exportações | Reprocesso, correção real e mudanças estruturais |
| HC adicional | Correções/versão ainda indefinidas | Fórmulas, consolidação e privacidade | Excel/PDF recalculados e inspecionados | Entrega/subida/fechamento, hospital e versão novos |

Uma correção pequena não exige workflow completo. Review independente é útil quando há risco e superfície definida; vários revisores do mesmo modelo não garantem independência das falhas.

## Ao abrir um projeto existente

Abra o Claude na raiz correta. Depois de configurado, `CLAUDE.md` deve ser lido automaticamente e apontar para estado mínimo e regras sob demanda. Não cole este pacote inteiro em todas as sessões.

Na configuração inicial, use o prompt do projeto uma vez: “Leia `10_FINANCEIRO.md` e faça a auditoria/configuração indicada.” Cada prompt registra o que ainda exige acesso local e mantém o código de negócio fora do escopo da configuração.

## Ao começar projeto novo

Use `15_NOVO_PROJETO.md` uma vez. Após auditar, gere somente as referências e automações úteis. Não copie todas as regras de outro projeto. Se vier a existir `/bootstrap-project`, a implantação deve explicar de onde vem e validar seu resultado.

## Sessões longas

Para manter conversa e apenas sair do terminal, use o background nativo validado. Para trocar contexto, use o handoff e uma nova sessão. `--resume`, `--continue` e fork não são substitutos de contexto limpo. Agent View, attach/logs/stop e notificações entram no guia final apenas conforme suporte local comprovado.
