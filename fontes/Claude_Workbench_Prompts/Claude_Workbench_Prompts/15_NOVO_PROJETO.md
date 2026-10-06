# PROMPT — bootstrap de projeto novo

Audite este projeto e proponha o menor pack Claude que permita trabalho autônomo, verificação e continuidade. Leia manifesto/health check global e `04_HANDOFF_PROTOCOL.md`. Não copie os prompts, manuais e regras dos meus outros projetos como contexto permanente.

## Descobrir

Identifique finalidade pelo código e docs; stack, entrypoints, dependências, banco/dados, UI, testes, commands, deployment e riscos. Veja CLAUDE/settings/rules/skills/agents/hooks/MCPs existentes, ignorados e locais. Se não houver código, obtenha somente os requisitos que mudam a escolha arquitetural; não invente stack por conveniência.

## Propor

1. `CLAUDE.md` pequeno: propósito, comandos, limites e roteamento.
2. Rules por paths reais; referências para domínio e contratos.
3. Skills para procedimentos recorrentes ausentes, com descriptions específicas e dependências claras.
4. Poucos agents, apenas quando isolamento/review justificar custo.
5. Hooks determinísticos pequenos, com timeout e escopo; suites no checkpoint/CI.
6. MCPs somente para estado externo necessário; preferir CLI/API suficiente já disponível.
7. Estado ativo/handoff e dispatcher testado; sem copiar transcript.
8. Workflow UI com execução, screenshot, acessibilidade, testes e review se houver frontend.
9. Lista de comandos reais versus propostas. Não inventar aliases silenciosamente.

Apresente arquivos a mudar, diff, benefícios, dependências, permissões e limites antes de aplicar. Depois de aprovado, implemente e faça health check sem pedir autorização para cada microdecisão reversível dentro do plano.

## Políticas

Rotina clara: direto. Ambiguidade com consequência: esclarecer; grilling só quando houver decisões interdependentes. Pesquisa volumosa: contexto isolado. Feature definida: spec e execução verificável. Longo/independente: background validado, limite de custo/tempo e critério de pronto. Destruição/migration/deploy: autorização explícita no escopo. Sem captura automática de dados privados para memória externa.

Se criar worktree, prever transferência de uncommitted changes e isolamento de banco/dados; worktree não isola serviço externo. Reviewer não deve modificar o resultado para depois revisar sua própria alteração sem registrar isso.

## Pronto quando

Claude reconhece o projeto e seus commands, descobre os procedimentos certos, não executa workflow manual sem intenção humana, passa checks pertinentes e recupera tarefa sintética pelo handoff. Estado de cada componente: aprovado/instalado/habilitado/testado ou bloqueado com causa. Entregue guia de uma página; o uso diário começa com “implemente X”, não com memorização de catálogo.
