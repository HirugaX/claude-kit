# PROMPT — configurar fila de pacientes/acolhimento

Configure meu Claude Code para o Google Apps Script de fila/acolhimento. Faça auditoria e proposta primeiro; mudanças de configuração somente no plano aprovado. Não altere pacientes, prioridades reais, triggers nem deployment durante o bootstrap.

Este repo não foi encontrado no conjunto GitHub acessível em 05/10/2026. Identifique path/repo pelo código. Não confunda este Apps Script com as filas existentes no app DESOSP.

## Mapeamento obrigatório

Identifique entrada → estados → prioridade → ordenação → atendimento → saída. Descubra timestamps e timezone, identificadores, critério de empate, cancelamento, reentrada e recuperação. Não invente critérios clínicos ou operacionais.

Inspecione operações simultâneas, duplicidade, idempotência, retries, `LockService`, `PropertiesService`, Sheets, triggers, quotas, autenticação/permissões e audit trail. Uma leitura seguida de escrita sem proteção pode perder atualização concorrente; verifique no código, não só pela presença de LockService.

Mapeie UI, se existir, e vínculo de cada tela com estado. Descubra `clasp` e testes atuais. Use dados sintéticos.

## Configuração

`CLAUDE.md` curto: finalidade, commands reais, limites de dados/ambiente e referências. Documento de domínio guarda máquina de estados/invariantes; regras por paths cobrem estado, concorrência, persistência, UI, testes e deployment. Paths devem existir. Projeto monolítico exige disclosure por tarefa, não globs fingindo granularidade.

Skills: workflow de alteração de estado/ordenação; diagnóstico de concorrência; recuperação delimitada, se recorrentes. Globais: requisitos/spec, pesquisa de docs, debug, review, handoff. Nenhuma seleção de prioridade deve depender de raciocínio improvisado da IA.

Agents: review separado para transições, concorrência e integridade. Exploração volumosa isolada; pequeno ajuste bem definido direto. Frontend reviewer apenas se houver UI e alteração relevante.

Hooks: checks pequenos de syntax/lint; suíte relevante no checkpoint/CI; sem mutação de Sheets num hook de abertura/fechamento. MCP/CLI Google apenas se necessário, com permissões e planilha de teste verificadas. Não enviar nomes/dados de pacientes para pesquisa web ou browser externo.

## Testes de conclusão

Prioridades válidas, empates determinísticos, clique repetido, duas chamadas simultâneas, estado inválido, evento fora de ordem, timeout, escrita parcial e retomada. Selecionar casos pertinentes à alteração. Testes locais não demonstram sozinhos o comportamento do runtime Google; registrar verificação de integração autorizada e limitações.

UI, se presente: estados vazios/erro/espera, retorno da ação, foco/teclado, contraste e atualização visível. Browser deve usar ambiente de teste, nunca a fila real para testar uma ação.

## Handoff/background

Siga `04_HANDOFF_PROTOCOL.md`. Estado mínimo: transição/invariante afetado, regra de prioridade vigente, funções, fixture, risco concorrente, testes e próximo passo. Referencie o documento de domínio.

Nome: `fila-debug-<id>` ou `fila-feature-<id>`. Worktree por escritor; Google Sheet de teste própria ou testes puros por worker. Revisão não escreve. Defina proprietário da integração final.

## Explícito

Mudança de critério de prioridade, reset/finalização em massa, recuperação que altera fila real, alteração de acesso/triggers e deployment. Bug especificado segue plano aprovado sem entrevista longa.

Entregue auditoria real, proposta/diff de arquivos, comandos reais, protocolo de continuidade, testes e health check. Não declarar `/fresh-session` funcionando sem o teste local do dispatcher.
