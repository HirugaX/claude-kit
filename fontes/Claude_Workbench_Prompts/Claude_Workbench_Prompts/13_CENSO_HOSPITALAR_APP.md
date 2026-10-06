# PROMPT — configurar DESOSP app

Configure Claude Code para o aplicativo hospitalar, com isolamento de dados, workflow visual e continuidade automática. Primeiro audite e apresente a arquitetura/diff; aplique configuração aprovada. Não reimplemente regras do kernel ou altere dados clínicos como parte desta tarefa.

## Contexto GitHub confirmado em 05/10/2026

Repo `HirugaX/desosp-app`: Python >=3.12, FastAPI, Jinja2, SQLite/SQLAlchemy/Alembic; UI em templates/CSS/JavaScript, **não React**. Não instalar React/Next skills como base deste front.

Este app dirige o kernel `HirugaX/desosp-censo`, localmente referido como `C:\DESOSP`. O kernel é o escritor do censo; integração via arquivos/execução. `DESOSP_KERNEL` é código; `DESOSP_RAIZ` é dado e tem padrão de desenvolvimento. Não inferir que os paths do GitHub correspondem aos paths atuais do notebook.

Já há `.claude/rules/front.md`, `.claude/skills/revisar-tela/SKILL.md`, hook `session-start.sh`/`abertura.py`, suíte pytest, ruff e testes Playwright que dirigem o Edge instalado. Capturas em `scripts/fotografar_telas.py`; axe-core vendorizado nos testes. A configuração atual restringe instalação de browsers: confirmar exceções antes de baixar navegador genérico.

## Auditar

Ler `CLAUDE.md`, `docs/HANDOFF_APP.md` e contratos relevantes; separar estado ativo do enorme histórico. O arquivo remoto de handoff tem aproximadamente 560 KB: não exigir leitura integral desse histórico como “contexto mínimo” sem avaliar suas seções.

Mapear identidade paciente/internação/presença, estados de alta/pendência, timestamps, filtros e ações de escrita. Verificar fronteira `APP_`, imports via `app/kernel/puros.py`, banco, migrações e isolamento real de testes em `app/config.py`/conftest. Não rodar testes sobre censo real.

Inspecionar hooks antes de executar. `session-start.sh` faz bootstrap de dependências na nuvem e procura kernel em diretório irmão; não copiar esse comportamento para todo projeto. Ler `abertura.py` e o que injeta. Resolver dependência pessoal `uso-do-claude` fora do repo.

## Arquitetura

Enxugar router de projeto com limites essenciais e índice; extrair histórico e procedimentos especializados para refs/skills. Preservar cada regra e suas referências: reduzir contexto não autoriza apagar decisão vigente.

Rules path-scoped: templates/static/web já têm regra; propor integração/kernel, persistência/schema, privacidade e testes somente quando faltar cobertura. Regras do pipeline vivem no kernel e são referenciadas; não duplicar cada regra clínica no app.

Skills: manter `revisar-tela` e kit/identidade existentes; escolher design genérico apenas como complemento útil. Debug/review/spec/pesquisa globais sob demanda. Skills PDF/XLSX somente na tarefa pertinente.

Agents: UI reviewer com evidências e contratos; reviewer de integração/identidade para mudança de risco; explorador para volume. Não copiar o catálogo inteiro de agentes. Verificar se a política da skill “mais de três telas → subagent” continua adequada em testes comparáveis.

Hooks: arranque curto e verificável; checks determinísticos pequenos; suites no checkpoint/CI. Browser/Playwright existente antes de outro MCP. Documentação e GitHub sob demanda; sem MCP de banco real para testes, sem n8n/Ruflo por padrão.

## Loop visual a automatizar

Requisito → `PROJETO_FRONT_DESOSP`/UX/kit → implementação → execução sobre raiz sintética → screenshots → inspeção humana do agente → correção → teclado/foco/contraste/axe-core → testes → `revisar-tela` e review.

Confirmar comandos atuais: laço rápido `pytest -m "not lento"`, navegador `pytest -m navegador`, ruff e capturas. Resultados condicionais/kernel ausente ficam declarados, sem inventar suite verde. Não rodar simultaneamente suites do app/kernel se as restrições do projeto ainda proibirem.

## Continuidade

Siga `04_HANDOFF_PROTOCOL.md`. Reorganize `HANDOFF_APP.md` em presente curto + arquivo histórico com referências preservadas; não criar segundo mestre concorrente. Registrar dependências do kernel, spec, telas, evidências e bloqueios. A nova sessão não precisa copiar transcript nem todo o handoff histórico.

Workers: `censo-ui-<id>`, `censo-feature-<id>`, `censo-review-<id>`. Um escritor por worktree, raiz/banco de teste separados; kernel compartilhado não deve ser mutado por workers. Comunicação de alteração de contrato precisa gerar item nomeado para o outro repo e acompanhar conclusão, conforme protocolo existente.

## Explícito e entrega

Opt-in de dado real, migration, alteração assistencial ambígua e deploy permanecem deliberados. Entregar diagnóstico, inventário, proposta/diff, comandos reais, estado ativo compacto, dispatcher testado, workflow visual e health check sem dados reais. Não chamar instalação no Work de instalação nos notebooks.
