# PROMPT — configurar folha/RH em Google Apps Script

Configure o ambiente Claude deste projeto, preservando regras de folha e dados. Primeiro audite e proponha; aplique mudanças de configuração após aprovação do plano. Não altere cálculo, planilha real, trigger ou deployment como efeito do bootstrap.

Este projeto foi informado pelo usuário, mas **não apareceu entre os quatro repositórios acessíveis na auditoria de 05/10/2026**. Não associe `desosp-hc` a RH: é um sistema de Home Care. Descubra repo/path reais e o código antes de escolher ferramentas.

## Auditar

- Estrutura `.gs`/JS/TS, `appsscript.json`, Sheets, esquema de abas/tabelas e entradas/saídas.
- Se há `clasp`, bundler, controle de versões ou edição somente no editor Google.
- Funções de cálculo, arredondamento, datas/competência, fechamento e correções retroativas; decisões vigentes em specs.
- Triggers simples/instaláveis, quotas, execução repetida, concorrência, `LockService`, `PropertiesService` e identidade de quem executa.
- Permissões OAuth, dados sensíveis e integração externa, sem imprimir valores privados.
- Testes atuais, mocks do runtime e fronteira de lógica pura versus integração.

## Arquitetura do pack

`CLAUDE.md` curto: finalidade, paths, rotina de desenvolvimento/teste, limites de escrita e referência para regras vigentes. Não despejar manual completo de folha no arranque.

Regras por caminhos reais: cálculo, schema/leitura-escrita de Sheets, triggers/concorrência, testes e deployment. Se tudo estiver num arquivo, não finja que path scoping isola funções: use referências/skills por tarefa ou planeje modularização separadamente.

Skills específicas: alterar/regredir regra de folha; mapear schema; depurar trigger. Criar somente procedimentos recorrentes ausentes no stack existente. Globais mantidas disponíveis: requisitos/spec, docs/pesquisa, debug, review e handoff.

Agents: reviewer de regra de negócio com spec e casos extremos; debugger de execução/concorrência. Não exigir vários agents para mudança pequena. Review deve conferir resultados esperados calculados por método independente, não copiar a mesma fórmula.

Hooks: lint/syntax e verificação pequena se já houver comandos; suíte no checkpoint/CI. Nunca fazer deploy, rodar fechamento ou escrever planilha real num SessionStart/Stop. Caso `clasp` exista, separar baixar/exportar, testes, push de código e deploy; não pressupor que um comando de sincronismo é somente leitura.

MCPs: não instalar um Google Sheets MCP genérico sem avaliar origem, OAuth e escopo. Preferir APIs/CLI existentes quando suficientes. MCP só quando houver ganho claro de acesso necessário. Context7 não substitui documentação oficial de Apps Script quando ela já é suficiente.

## Continuidade

Leia `04_HANDOFF_PROTOCOL.md`. Use estado mínimo com regra alterada, funções, schema, período/competência, fixture sintética, comandos de teste, decisão vigente e critério de pronto. Substitua o copiar/colar pela leitura desse estado em sessão nova.

Workers longos: `rh-regra-<id>` ou `rh-tests-<id>`, sobre código isolado e planilha de teste dedicada. Git worktree não isola o documento Google. Sem credenciais/propriedades copiadas para versionamento. Bloqueio por quota/permissão deve ser reportado, sem tentativas ilimitadas.

## Workflows explícitos

Mudança de regra ambígua, alteração de triggers/OAuth, escrita de valores reais, fechamento de folha, exclusão/migração de colunas e deployment. Rotina de código especificada pode seguir automaticamente o plano aprovado.

## Entregáveis

Diagnóstico com paths e stack reais; catálogo classificado; proposta de `CLAUDE.md`/rules/skills/agents/hooks/MCPs com diff; comandos reais; handoff mínimo; plano de testes sintéticos; health check local; guia de uso. Não impor biblioteca científica, React, n8n ou banco SQL sem necessidade demonstrada.
