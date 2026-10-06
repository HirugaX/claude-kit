# Protocolo comum — continuidade sem copiar conversas

Proposta a adaptar e testar no Claude Code local. Não existe uma skill `/fresh-session` instalada por este pacote.

## Escolher o mecanismo certo

| Mecanismo | Objetivo | O que verificar |
|---|---|---|
| Mesma conversa em background | Deixar trabalho atual continuar fora do terminal | Não fornece contexto limpo |
| Nova sessão | Continuar a partir do estado mínimo persistido | Não usar resume/continue/fork do transcript antigo |
| Subagent | Exploração/review delimitado e retorno compacto | Prompt, ferramentas e contexto efetivamente recebido |
| Fork de conversa | Explorar alternativa preservando histórico | Cópia herda contexto; não equivale a sessão limpa |
| Agent Team | Coordenação entre vários participantes | Só se dependências/paralelismo justificarem custo |

A documentação atual descreve `claude --bg` para iniciar sessão background e opções de retomada da conversa. Esses recursos, naming e mensagens entre sessões devem ser testados na versão, no SO e no provedor local. Mensagens transportam texto; não transportam automaticamente arquivos ou worktrees.

## Um arquivo ativo por tarefa

Reutilize o handoff existente em cada projeto; não crie um segundo arquivo mestre competindo com ele. Um handoff de tarefa independente pode ficar em `docs/handoffs/<task-id>.md` ou path já adotado, com dono explícito.

Orçamento inicial: aproximadamente 1.000 palavras no handoff ativo, ajustável por complexidade. Se exigir muito mais, extraia specs/contratos/decisões para arquivos de referência. Não perca regras essenciais para cumprir o orçamento. Arquivo de histórico permanece acessível, mas não é leitura de arranque obrigatória.

### Template de conteúdo

```markdown
# Objective
Objetivo verificável, task-id e data da última validação.

# Current State
Concluído, em andamento e bloqueado; dono de cada parte. Sem narrativa histórica.

# Decisions
Decisões vigentes e links para spec/ADR/contrato. Não repetir conteúdo integral.

# Constraints
Limites de autonomia, dados/ambientes permitidos, compatibilidade e efeitos externos autorizados.

# Relevant Files
Paths relativos ao repo; seção/símbolo útil; motivo para cada referência.

# Branch/Commit
Repo, branch, commit-base observado, worktree; mudanças não commitadas e como serão transferidas.

# Tests
Comando, resultado, data, ambiente; distinguir executado, não executado e dependente de dado local.

# Known Problems
Repro mínima, risco, bloqueio e dono. Separar falha de dúvida de produto.

# Next Action
Uma ação inicial concreta; id da sessão de origem se necessário para retorno.

# Definition of Done
Critérios objetivos de conclusão, evidências e destino do resultado.
```

Não incluir pacientes, salários, transações reais, credenciais ou transcript. Referenciar dados locais por identificador/path permitido, sem copiar seu conteúdo para um repo remoto.

## Workflow desejado

Quando eu disser “continue em contexto limpo”:

1. Inspecionar `git status`, branch e alterações pendentes. Reescrever o estado ativo, sem acumular fechamento após fechamento.
2. Validar que referências existem. Registrar o que está medido e o que foi apenas alegado no documento antigo.
3. Separar execução de relato: principal entrega objetivo, paths e critérios; nova sessão lê apenas os conteúdos indispensáveis, carregando domínio sob demanda.
4. Se a nova sessão usar worktree, disponibilizar a alteração vigente por mecanismo explicitamente acordado. Um worktree novo não contém automaticamente mudanças não commitadas de outro.
5. Iniciar uma nova sessão nomeada pelo caminho nativo verificado. Não herdar transcript antigo nem limpar variáveis de proteção para contornar restrições de sessão aninhada.
6. Guardar task-id/session-id e estado no projeto. Worker atualiza status, testes e resultado compactos, sem outro worker editar o mesmo estado simultaneamente.
7. Avisar a origem por mecanismo de mensagens confirmado. Se origem morreu ou mensagens estão indisponíveis, deixar resultado persistido e recuperável; retorno automático não é garantia.

## Teste de capacidade antes de automatizar

Fase aprovada, repo de teste sintético:

- Registrar `claude --version`, ajuda local e documentação relevante.
- Uma nova sessão identifica um arquivo fictício e entrega um resultado simples. Não executar tarefa de produto.
- Confirmar id novo, histórico não herdado, diretório correto, instruções carregadas, nome no Agent View, estado e logs.
- Confirmar como permissões e notificações funcionam; teste negativo deve permanecer bloqueado, sem bypass.
- Testar um retorno compacto à origem, recuperação e encerramento do job de teste.
- Comparar Windows nativo, WSL e outro SO somente se esses forem os ambientes realmente usados. Não assumir comunicação entre eles.

Se spawning por dentro de Claude não for suportado, entregue alternativa nativa de dispatch ou launcher externo com uma ação humana. Arquivo handoff preenchido automaticamente permanece o principal ganho; não me devolva a tarefa de reconstruir contexto.

## Autonomia e limites

Um writer por worktree; banco/Sheets/arquivos operacionais exigem isolamento próprio. Inicialmente uma continuação por tarefa, sem continuação recursiva. Workflows longos precisam de escopo, critério de pronto e limite de custo/tempo/iterações acordado; parar por bloqueio sem repetir tentativas indefinidamente.

Nome sugerido: `<projeto>-<tarefa>-<task-id>`. Estados: planejada, executando, precisa-decisão, bloqueada, concluída, falhou. Notificar em transição relevante, não gerar polling caro para escrever “ainda trabalhando”.

Registre pedido de permissão e forma de retomada. Não transforme “autonomia” em acesso irrestrito. Não faça pergunta de produto se a decisão já estiver no contrato/ADR; dúvida nova que altera comportamento merece decisão humana.

## Economia que pode ser verificada

Compare tarefas equivalentes e registre: tamanho das instruções/descrições, conteúdos adicionados por hooks, handoff carregado, uso de subagents, cache quando observável, tokens/limites de assinatura quando disponíveis, tempo e defeitos. Começar conversa nova pode perder cache; reduzir transcript não assegura reduzir cobrança.

Fontes: [Agent View](https://code.claude.com/docs/en/agent-view), [Cross-session messaging](https://code.claude.com/docs/en/cross-session-messaging), [Subagents](https://code.claude.com/docs/en/sub-agents), [Skills](https://code.claude.com/docs/en/skills).
