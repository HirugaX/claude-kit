# PROMPT — configurar DASH financeiro

Configure meu Claude Code para o projeto financeiro com foco em autonomia, correção e economia de contexto. Leia este prompt uma vez na configuração; não o transforme integralmente em always-on. Primeiro audite e apresente diff/arquitetura; aplique somente mudanças de configuração já aprovadas. Não desenvolva uma feature nem altere meus dados como parte deste bootstrap.

## Contexto obtido do GitHub em 05/10/2026

Repo: `HirugaX/app-finance`. Código em `dash/`; Python >=3.12, FastAPI, SQLite, pdfplumber/openpyxl/xlrd. Front existente em `dash/web/`: React 19, TypeScript, Vite, Tailwind, TanStack, Radix, ECharts; testes Vitest. **O frontend já existe**: trate a demanda como evolução, não criação arbitrária de stack nova.

Entradas de conhecimento: `CLAUDE.md`, `.claude/rules/`, `dash/docs/HANDOFF.md`, specs `dash/docs/fase-N.md`, relatório de arquitetura e identidade visual em `dash/docs/projeto/`. Leia os arquivos atuais locais, que podem diferir da fotografia remota.

Já existem `.claude/skills/fechar-janela`, `.claude/skills/revisao-adversarial` e hook `.claude/sessao_inicio.py`. Settings desabilitam quatro componentes Ruflo. Skill pessoal `uso-do-claude` é dependência externa a resolver no inventário local.

## Auditar antes de configurar

- Mapear CLI `dashfin`, registry → parser → extract → normalize → interpret → classify → query → API → UI; contratos e idempotência.
- Conferir `DASH_DATA_DIR`, separação código/dados, schema e mutações. Os testes sintéticos não substituem verificação sobre dados reais quando esta for autorizada e necessária.
- Ler frontmatter das nove regras, duas skills e overrides. Confirmar mecanismo de registro e descoberta.
- Inspecionar fechamento atual: handoff, aferição e commit. Preservar política de commit sem push existente até decisão explícita de mudança.
- Inspecionar hook sem executar: ele consulta banco em leitura, mas também remove pastas `.claude-flow`. Não é um hook inteiramente somente leitura. Entender a origem do conflito antes de instalar novos harnesses.

## Configuração desejada

`CLAUDE.md`: finalidade, paths, comandos básicos, limites de dados, dono das decisões, ponte para handoff e índice de regras. Regras financeiras/UX detalhadas permanecem por caminho ou em referências. Evitar importar todas as specs no arranque.

Manter/adaptar regras existentes para `dash/src/dash/parsers/**`, normalização/interpretação, classificações, banco/API, `dash/web/src/**` e testes; use os paths reais. Para discussão de domínio sem leitura de código, carregar explicitamente a referência correta — regra por caminho não lê a mente.

Skills: aproveitar revisão adversarial/fechar-janela, requisitos/spec/pesquisa/debug/review globais selecionados, frontend-design ou alternativa escolhida, Vercel se útil em React, PDF/XLSX sob demanda. Escolher apenas uma camada de design principal.

Agents: pesquisa/inspeção e review isolados quando gerarem volume; review financeiro precisa método de conferência numérica diferente, não só mais revisores. Frontend reviewer apenas em mudanças relevantes de UI. Não manter agentes executando sem tarefa.

Hooks: estado curto no SessionStart; formatter/verificação pequena onde determinístico; testes completos no checkpoint de tarefa/CI. Não usar cada edição para disparar toda a suíte. Revalidar schema de settings e suporte de modelo/esforço; configuração escrita não prova que a versão instalada aplica o valor.

MCPs: docs sob demanda; GitHub somente se Git/gh não bastarem; browser escolhido quando necessário. Não habilitar n8n/Supabase só porque existem no catálogo. Proibir envio de documentos/transações reais para serviços externos não autorizados.

## Frontend

Requisito → identidade visual vigente → implementação nas primitivas existentes → execução com dados sintéticos → capturas → correções → teclado/acessibilidade → testes → review. Preservar `dash/tools/inspect/capturas.py` e travas de estilo já adotadas.

`package.json` oferece `build`, `test` e `typecheck`; confirme os comandos reais e diretório antes de usar. Backend tem pytest. A captura deve medir estados relevantes e inspecionar imagens; compilação verde não demonstra qualidade visual.

## Handoff e background

Siga `04_HANDOFF_PROTOCOL.md`, adaptando ao `dash/docs/HANDOFF.md` existente. A skill de fechamento deve produzir um handoff ativo compacto e apontar para fase/ADR/evidências. Não exigir que eu copie o “prompt da próxima janela” se o dispatcher pode ler o arquivo.

Nome sugerido: `financeiro-ui-<id>` ou `financeiro-parser-<id>`. Worktree e banco sintético por worker; não compartilhar banco real para desenvolvimento paralelo. Alterações não commitadas precisam de plano de transferência. Resultado deve voltar com diff, testes/capturas e pendências de decisão.

## Entrega

Inventário local + gaps; mapa de contexto atual; proposta/diff por arquivo; stack habilitado e comandos reais; handoff adaptado; health check; guia curto de uso. Não recriar skills existentes com nomes genéricos duplicados. Não declarar integração de nova sessão funcionando antes do teste local.
