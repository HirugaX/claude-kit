# Auditoria inicial — Work e GitHub

Data: 05/10/2026. **Somente leitura dos repositórios; nenhuma instalação local, configuração ou commit aplicado.** Esta é uma auditoria do ambiente acessível e das configurações versionadas, não do estado completo dos dois computadores.

## Ambiente efetivamente acessível

Work executando em Linux, diretório `/workspace/scratch/34ba3b134143`. Git 2.51.1, Node 24.19.0, npm 11.9.0, Python 3.12.14. Claude Code e GitHub CLI não foram encontrados no PATH. Não há `~/.claude` nem repositório de projeto no diretório atual.

Consequência: instalar Claude/plugins aqui não configuraria seus dois computadores. Ainda faltam os inventários locais, SO/shell de A/B e acesso às configurações globais/pessoais. O pacote inclui prompt de execução local para obter isso sem você montar o inventário manualmente.

O GitHub está conectado e permitiu listar quatro repositórios privados e ler árvores/configurações/documentação selecionada em `main`. A busca indexada de código estava indisponível no metadado; leitura direta de arquivos funcionou. Metadados de tamanho do repositório não foram usados para inferir ausência de conteúdo: `app-finance` apareceu com size=0, mas continha código.

## Mapa real dos projetos

| Repo | Identificação obtida dos arquivos | Stack/automação observadas | Prompt |
|---|---|---|---|
| [HirugaX/app-finance](https://github.com/HirugaX/app-finance) | DASH financeiro local | Python/FastAPI/SQLite; React/TypeScript/Vite; handoff, 9 rules, 2 skills, hook SessionStart | `10_FINANCEIRO.md` |
| [HirugaX/desosp-app](https://github.com/HirugaX/desosp-app) | App que dirige o kernel do censo | FastAPI/Jinja2/SQLite; 1 rule de frontend, skill revisar-tela, hooks, Playwright/Edge e axe-core | `13_CENSO_HOSPITALAR_APP.md` |
| [HirugaX/desosp-censo](https://github.com/HirugaX/desosp-censo) | Kernel Python que gera censo Excel | 27 rules path-scoped, skill rodada, testes e handoff volumoso | `14_CENSO_EXCEL_KERNEL.md` |
| [HirugaX/desosp-hc](https://github.com/HirugaX/desosp-hc) | Projeto adicional de planilhas Home Care | Python, ExcelJS, recálculo LibreOffice documentado; 12 comandos, hook de caixa pendente | `16_HOME_CARE_EXCEL.md` |

Folha/RH e fila/acolhimento Apps Script não foram identificados neste conjunto acessível. Isso não prova que não existam no GitHub ou localmente. Seus prompts permanecem condicionados à descoberta do código correto.

## Achados e implicações

1. **Já existe infraestrutura para parte do problema de continuidade.** O financeiro carrega estado no arranque e atualiza handoff; HC avisa sobre uma caixa de comunicação entre projetos; o app tem abertura e revisão visual. Escolher um novo harness antes de avaliar essas peças seria prematuro.
2. **Frontend não tem a mesma stack nos dois apps.** DASH usa React/Vite; DESOSP usa Jinja2/JS/CSS. Não replicar pack React nos dois. As capturas e testes existentes merecem integração antes de instalar outra automação browser.
3. **Handoff atual é um alvo concreto de economia.** `docs/HANDOFF_APP.md`: 559.819 bytes; `docs/HANDOFF_SPRINT2.md`: 334.841 bytes; financeiro `dash/docs/HANDOFF.md`: 15.505 bytes. O app manda ler seu handoff sempre. A estrutura precisa ser separada em estado ativo e referências históricas; tamanho em bytes não é contagem de tokens nem prova de custo faturado.
4. **Router de projeto ainda contém bastante contexto.** CLAUDE financeiro: 198 linhas/18.150 bytes; app: 349/23.388; kernel: 422/32.364; HC: 223/19.493. O limite de linhas sozinho é insuficiente: medir conteúdo realmente injetado e leituras obrigatórias.
5. **Rules por caminho podem se acumular.** No kernel, `data_merge.py`, `run_merge.py`, `loaders.py` e `mensagens.py` aparecem em vários globs. Frontmatter foi examinado nos 37 arquivos de rules. Não medimos o carregamento no Claude local. A tabela ao fim mostra risco de overlap, não erro comprovado no mecanismo.
6. **Ruflo não deve ser reinstalado automaticamente.** Settings financeiros desabilitam quatro plugins. O código de `.claude/sessao_inicio.py` remove diretórios `.claude-flow` recursivamente na raiz, pulando Git/node_modules; há conflito operacional documentado no código. É um efeito de escrita/deleção, apesar de parte das descrições do hook enfatizar leitura. Não executar esse hook durante auditoria somente leitura.
7. **Dependência global ainda não auditada:** `uso-do-claude`, referida em `C:\CLAUDE`/`C:\CLAUDE\skills`. Não está nas árvores acessíveis. A skill revisar-tela referencia esse conteúdo, inclusive uma afirmação sobre cache/esforço que precisa de verificação atual; não adotá-la como fato pela autoridade do arquivo.
8. **Invocação manual ainda precisa ser calibrada.** As quatro skills de projeto examinadas têm name/description, sem marcador de bloqueio de invocação automática no frontmatter observado. Fechar-janela inclui commit; revisão adversarial termina chamando fechar-janela. Assim, a revisão pode alcançar efeitos de fechamento. Recomenda-se explicitar fronteiras e não tratar “review” como sempre somente leitura.
9. **Hook de app também é bootstrap condicionado.** `session-start.sh` instala dependências no ambiente de nuvem e procura kernel irmão. Isso não é necessário em cada sessão local; deve ser preservado/adaptado ao ambiente, sem virar hook global.
10. **Settings declarados não comprovam capacidade ativa.** Campos de modelo/esforço/compactação e permissões presentes devem ser confrontados com schema e versão local. Não foram testados no Work porque Claude não está instalado aqui.

## Inventário principal classificado

A=always-on; B=descoberta de skill sob demanda; C=workflow manual desejado; D=contexto isolado; E=hook por evento; F=ferramenta externa. Escopo de todos os componentes abaixo: projeto, distribuição por arquivos versionados do autor. Nenhuma entrada comprova instalação global.

| Componente | Tipo/classe | Invocação observada | Dependências/efeitos | Recomendação |
|---|---|---|---|---|
| Quatro `CLAUDE.md` | Instrução/A | Automática no escopo correto, a validar localmente | Leitura de handoffs e refs; orienta ações | Enxugar routers sem perder regras, separar estado/histórico |
| 37 rules | Rule/path-scoped | Gatilhos `paths`, sem comando explícito | Contexto de domínio; globs sobrepostos | Manter escopo, medir expansão e ajustar refs |
| DASH `fechar-janela` | Skill/B; candidato C | Frontmatter não restringe auto-invocação | Specs, testes, aferição, handoff, uso-do-claude; inclui commit sem push | Preservar política; explicitar efeito e invocação |
| DASH `revisao-adversarial` | Skill/B | Frontmatter não restringe auto-invocação | Spec/fixtures/dado local autorizado; termina em fechar-janela | Evitar duplicar reviewer e separar efeitos de fechamento |
| App `revisar-tela` | Skill/B | Model/user conforme default a validar | Kit/UX, navegador, screenshots, axe-core; refere uso-do-claude e subagent condicional | Integrar com pack UI; não substituir sem ganho |
| Kernel `rodada` | Skill/B; controle operacional a avaliar | Model/user conforme default a validar | Pipeline, entrada/saída/arquivo, contratos; pode escrever censo | Separar operacional de desenvolvimento; roteiro compacto + refs |
| DASH `sessao_inicio.py` | Hook/E | SessionStart no settings | SQLite leitura; Git/settings; remove .claude-flow; injeta resumo | Revisar conflito antes de novos harnesses |
| App `session-start.sh` + abertura.py | Hook/E | SessionStart no settings | Local: abertura; nuvem: venv/pip e kernel irmão | Revisar payload de abertura; não globalizar bootstrap |
| HC `caixa_pendente.py` | Hook/E | SessionStart no settings | Lê índice e injeta pendências; código lido | Manter aviso curto; rever limites/erro de I/O |
| HC 12 arquivos commands | Workflow explícito de interface/C proposto | Sintaxe publicada no README; flags de todos os corpos ainda não auditadas | Scripts/planilhas/relatórios; efeitos por comando | Preservar interfaces; auditar cada efeito antes de migrar formato |
| Agents/custom MCPs | D/F | Nenhum arquivo correspondente encontrado nas quatro árvores `main` | Globais/locais não acessíveis | Não declarar ausência global; inventariar no PC |

Lista HC: nova-rodada, rodada, consolidar, boletins, placar, mensagem, ler-pdfs, fechar-rodada, novo-hospital, nova-versao, informativo, verificar. README e árvore examinados; não é auditoria completa dos corpos de todos os comandos.

## Stack recomendado para a próxima etapa

Preservar workflows atuais; resolver dependência `uso-do-claude`; acrescentar requisitos/spec/pesquisa/debug gerais se ausentes, a partir da coleção selecionada; docs sob demanda; PDF/XLSX onde necessário; frontend por stack; review de segurança seletivo. Um dono de handoff/estado e um caminho browser por necessidade.

Adiar Ruflo/ECC/Superpowers e múltiplas soluções de memória até uma comparação isolada. `planning-with-files` também deve provar ganho sobre estado/hooks já existentes. K-Dense e n8n são packs de pesquisa/automação condicionais; não entram em cada sessão hospitalar por afinidade temática.

## Ainda falta para instalar de fato

- Rodar `07_AUDITORIA_LOCAL.md` em A e B, resolver caminhos e versões.
- Examinar conteúdo da skill pessoal e configurações globais/locais.
- Finalizar e aprovar seleção/diff arquitetural conforme o pedido editado.
- Executar `03_IMPLEMENTAR_STACK.md` em cada ambiente e registrar health/parity check.
- Testar background/fresh-session e só então anunciar a capacidade como pronta.

## Evidências e limites

Leituras diretas em `main`: árvores completas, quatro CLAUDE.md (estrutura/trechos), manifests Python/Node, READMEs, três settings de projeto, quatro skills, 37 frontmatters de rules, scripts financeiros e shell do app, código do hook HC. Conteúdo de todos os modules/hooks/commands e workbooks não foi auditado exaustivamente; nenhuma suite foi executada.

Snapshot por SHA da **árvore**, não do commit:

- app-finance: `aa32fbccc6222c31ddf315ca7720cd1655553d75`
- desosp-app: `547e32deb3ffe51fcb27e336793e207d67dc4804`
- desosp-censo: `271deeb6fd00184cc43d273312305cc4577ffdfa`
- desosp-hc: `c6bc80fe6ce09f4ed3e17460edcfea532958e897`

Árvores/arquivos foram lidos em chamadas distintas sobre main; confirmar commit local antes da implementação.

## Inventário por arquivo de rule (frontmatter inspecionado)

Todos são rules de projeto com ativação por paths, sem comando humano específico. Efeito direto: adicionar instruções ao contexto; efeitos de execução dependem da tarefa. Recomendação inicial: manter conhecimento no projeto, medir overlap e reduzir disclosure sem apagar regras. Impacto abaixo é tamanho de arquivo, não tokens medidos.

| Repo | Rule | Bytes | Paths/gatilhos declarados |
|---|---|---:|---|
| app-finance | classificacao.md | 7584 | - "dash/src/dash/classify/**"; "dash/manifest/TAXONOMY*"; "dash/src/dash/query/{pix,taxonomia_tela,tags}.py"; "dash/web/src/routes/{classificacao,transacoes,config,receitas-e-pix}.tsx"; "dash/scripts/decisoes_*.py" |
| app-finance | decisao-api.md | 3822 | - "dash/src/dash/api/**"; "dash/src/dash/query/decisions.py"; "dash/scripts/**"; "dash/web/src/api/**" |
| app-finance | dinheiro.md | 6328 | - "dash/src/dash/query/**"; "dash/src/dash/interpret/**"; "dash/web/src/routes/**" |
| app-finance | documento.md | 7069 | - "dash/src/dash/parsers/**"; "dash/src/dash/registry/**"; "dash/src/dash/extract/**"; "dash/src/dash/normalize/**"; "dash/src/dash/inbox.py"; "dash/src/dash/ops/importer.py"; "dash/src/dash/query/{horizonte,faltando,conferencia,quality}.py"; "dash/manifest/**"; "dash/web/src/routes/qualidade.tsx"; "dash/scripts/{mover_para_inbox,substituir_documento,reorganize_data}.py" |
| app-finance | fontes.md | 2156 | - "dash/src/dash/parsers/**"; "dash/tools/inspect/probe_*.py"; "dash/tests/fixtures/**" |
| app-finance | investimento.md | 3566 | - "dash/src/dash/invest/**"; "dash/src/dash/parsers/{b3_xlsx,itau_cdb,sofisa_pdf,xp_pdf,xp_xlsx}.py"; "dash/web/src/routes/investimentos*.tsx"; "dash/web/src/lib/invest.ts" |
| app-finance | tela.md | 7282 | - "dash/web/src/**"; "dash/tools/inspect/capturas.py" |
| app-finance | testes.md | 959 | - "dash/tests/**" |
| app-finance | viagem.md | 1593 | - "dash/src/dash/query/viagens.py"; "dash/src/dash/ops/export_viagem.py"; "dash/web/src/routes/orcamento.tsx"; "dash/web/src/**/*viag*" |
| desosp-app | front.md | 1431 | - "app/templates/**"; "app/static/**"; "app/web/**" |
| desosp-censo | adendo.md | 6070 | - "desosp/loaders.py"; "desosp/arquivo_rodada.py"; "desosp/run_rodada.py"; "desosp/run_merge.py"; "desosp/mensagens.py"; "entrada/*_ADENDO*" |
| desosp-censo | build-e-invariantes.md | 3802 | - "desosp/build_wb.py"; "desosp/run_build.py"; "saida/**/LOG_DO_BUILD.txt" |
| desosp-censo | correcao-manual.md | 8854 | - "desosp/loaders.py"; "desosp/data_merge.py"; "desosp/run_reprocessar.py"; "desosp/build_wb.py" |
| desosp-censo | cuidadosmil.md | 3042 | - "desosp/cuidadosmil.py"; "desosp/triage.py"; "desosp/ficha.py"; "fontes/Linha_cuidados_mil.md" |
| desosp-censo | datas-e-ancora.md | 10381 | - "desosp/loaders.py"; "desosp/data_merge.py"; "desosp/run_merge.py"; "desosp/run_extracao.py"; "saida/_extracao/**"; "entrada/EVOL_*" |
| desosp-censo | decisoes-clinicas.md | 3959 | - "desosp/mensagens.py"; "desosp/triage.py"; "desosp/data_merge.py"; "saida/**/MSG_*.txt"; "saida/**/RELATORIO_*.txt"; "saida/_extracao/**" |
| desosp-censo | discussao-e-pendencia.md | 12257 | - "desosp/data_merge.py"; "desosp/build_wb.py"; "desosp/run_merge.py"; "docs/CONTRATO_FONTE_*.md" |
| desosp-censo | docs-gpt.md | 3678 | - "docs/gpt/**"; "desosp/run_doc_gpt.py"; "docs/KNOWLEDGE_*.md"; "docs/CONTRATO_FONTE_*.md" |
| desosp-censo | exames.md | 4285 | - "desosp/exames.py"; "desosp/run_doc_exames.py"; "docs/KNOWLEDGE_03*.md" |
| desosp-censo | fase-e.md | 9463 | - "desosp/run_extracao.py"; "desosp/run_rodada.py"; "desosp/run_reprocessar.py"; "desosp/loaders.py"; "saida/_extracao/**"; "docs/CONTRATO_FONTE_*.md"; "entrada/BRUTO_*"; "entrada/EVOL_*" |
| desosp-censo | hd-carimbo.md | 2392 | - "desosp/hd_carimbo.py"; "desosp/run_merge.py"; "historico/HD_CARIMBO.json" |
| desosp-censo | hd.md | 18977 | - "desosp/data_merge.py"; "desosp/CONFIG_DESOSP.py"; "desosp/cuidadosmil.py"; "docs/CONTRATO_FONTE_*.md" |
| desosp-censo | home-care.md | 24058 | - "desosp/loaders.py"; "desosp/data_merge.py"; "desosp/run_merge.py"; "desosp/hc_evolucao.py"; "desosp/mensagens.py"; "desosp/triage.py"; "entrada/HC_*"; "historico/HC_EVOLUCAO.json"; "docs/templates/HOME_CARE.md" |
| desosp-censo | lp-plus-e-abas.md | 6579 | - "desosp/lp_plus.py"; "desosp/build_wb.py" |
| desosp-censo | marca-fonte.md | 6221 | - "desosp/data_merge.py"; "desosp/build_wb.py"; "desosp/mensagens.py"; "desosp/hc_evolucao.py"; "desosp/ficha.py"; "desosp/loaders.py" |
| desosp-censo | matricula.md | 4618 | - "desosp/loaders.py"; "desosp/build_wb.py"; "desosp/mensagens.py"; "desosp/lp_plus.py" |
| desosp-censo | mensagens.md | 8608 | - "desosp/mensagens.py"; "desosp/run_msg.py"; "desosp/run_captacao_janela.py"; "desosp/pdf_rounds.py"; "desosp/run_rodada.py"; "saida/**/MSG_*.txt"; "docs/templates/**" |
| desosp-censo | motivo.md | 3367 | - "desosp/motivo.py"; "desosp/mensagens.py"; "desosp/build_wb.py"; "docs/templates/FECHAMENTO.md" |
| desosp-censo | nomes-e-varredura.md | 4699 | - "tests/varredura_nomes.py"; "desosp/nomes_locais.py"; "desosp/local_nomes*.json"; "docs/para_o_app/**"; "docs/para_o_kernel/**"; "docs/para_a_planilha/**" |
| desosp-censo | pastas-e-arquivo.md | 3441 | - "desosp/arquivo_rodada.py"; "desosp/run_merge.py"; "desosp/run_build.py"; "desosp/espera.py"; "desosp/CONFIG_DESOSP.py"; "saida/**/_RODADA.json" |
| desosp-censo | pdf-uti.md | 1797 | - "desosp/pdf_uti.py"; "desosp/run_extracao.py"; "entrada/CENSO_UTIA_*" |
| desosp-censo | pipeline-ordem.md | 2572 | - "desosp/run_merge.py"; "desosp/data_merge.py"; "desosp/build_wb.py" |
| desosp-censo | quarentena.md | 677 | - "desosp/quarentena.py"; "desosp/quarentena.json" |
| desosp-censo | reprocessar.md | 13423 | - "desosp/run_reprocessar.py"; "desosp/espera.py"; "desosp/run_extracao.py"; "entrada/_ESPERA/**" |
| desosp-censo | rodadas-especiais.md | 16845 | - "desosp/run_rodada.py"; "desosp/run_merge.py"; "desosp/sist_reuso.py"; "desosp/periodo.py"; "desosp/mensagens.py"; "desosp/build_wb.py"; "desosp/arquivo_rodada.py"; "desosp/espera.py"; "scripts/prova_*.py"; "entrada/SIST_*" |
| desosp-censo | series-at-ak.md | 3430 | - "docs/para_o_app/**"; "docs/para_o_kernel/**"; "docs/para_a_planilha/**" |
| desosp-censo | testes.md | 2167 | - "tests/**" |
