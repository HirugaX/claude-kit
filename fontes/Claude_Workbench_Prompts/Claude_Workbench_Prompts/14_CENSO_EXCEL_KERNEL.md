# PROMPT — configurar censo Excel e kernel DESOSP

Configure Claude Code para o censo hospitalar Excel. Primeiro audite e proponha; aplique configuração aprovada. Distingua desenvolvimento do pipeline de operação clínica da rodada. Não execute uma rodada real nem reprocesso como teste de instalação.

## Contexto GitHub confirmado em 05/10/2026

Repo `HirugaX/desosp-censo`: pipeline Python (`desosp/`) que gera censo/workbooks/mensagens, não apenas um Excel isolado. Tem `CLAUDE.md`, 27 rules em `.claude/rules/` e skill `rodada`; requisitos incluem bibliotecas de processamento documental. O workbook atual com pacientes fica fora do GitHub e ainda precisa ser inspecionado localmente.

`docs/HANDOFF_SPRINT2.md` remoto tem aproximadamente 335 KB. A skill `rodada` tem aproximadamente 18 KB e inclui procedimentos operacionais. Não tornar ambos leitura integral de toda tarefa mecânica se apenas uma referência específica for necessária.

## Auditar

- Versão/code paths, `CONFIG_DESOSP`, entrada/saída/arquivo/histórico e comandos reais.
- Ordem do pipeline, âncora temporal, `_ADENDO`, períodos M/Ihdl/I/T, reset/rebate, fontes e invariantes; buscar contratos no código e documentos atuais.
- Workbooks atuais: abas, tabelas, fórmulas, named ranges, validações, formatting, referências, queries/macros e dependências externas se existirem.
- Preservação de dados, origem de cada campo e escritor autorizado. Não promover hipótese clínica a fato nem escolher fontes ambíguas por improviso.
- Isolamento dos testes e risco de escrita no dado real; sem rodar suíte por hábito antes de verificar guardas.
- Frontmatter das 27 rules, dependências da skill `rodada`, referências à skill pessoal `uso-do-claude` em `C:\CLAUDE` e como ela é registrada.

Não leia workbook real por API externa sem autorização. Inventários/versionamento do schema devem ser sanitizados.

## Pack proposto

Router de projeto curto: propósito, limite de dado real, fonte/ordem fundamentais, ponte para workflow de rodada e índice de regras. Regra do domínio permanece neste kernel, referenciada pelo app. Nunca copiar para o global.

Preservar/adaptar rules de datas, identidade, HC, exames, LP, mensagens, build e testes. Medir overlap: módulos como `data_merge.py` aparecem em múltiplos globs e podem carregar vários documentos grandes simultaneamente. Não assumir economia apenas porque há `paths:`.

Skill `rodada`: manter interface, avaliar separar roteiro pequeno de refs operacionais. Preservar dependências/contratos. Skills de XLSX/PDF sob demanda; revisão/debug/spec globais para desenvolvimento. Verificar se a invocação operacional deve ser manual, model-invoked ou híbrida à luz da autorização da rodada.

Agents: review de invariantes/datas/identidade e inspeção de documentos quando necessária. O próprio processamento determinístico do pipeline não exige agentes múltiplos. Reviewer leitura; implementador trabalha em cópia isolada.

Hooks: checks de ambiente pequenos e sem censo nominal no contexto; gates determinísticos de invariantes/privacidade quando apropriados ao workflow. Não iniciar rodada, arquivar entrada, podar HC ou recalcular workbook real em SessionStart/Stop.

MCP: GitHub/docs quando necessário; Excel/arquivos via bibliotecas locais existentes. Não adicionar banco ou integração clínica remota sem objetivo específico.

## Handoff e trabalho longo

Siga `04_HANDOFF_PROTOCOL.md`. Separar handoff de desenvolvimento de registro operacional de rodada; cada um tem dono e finalidade. Novo contexto recebe objetivo, período/âncora declarados quando pertinentes, paths de código/contrato, branch e testes. Insumos clínicos não entram no arquivo versionado.

Para operação real, manter manifesto/status idempotente do pipeline; não iniciar dois workers escrevendo a mesma rodada. Worktree não isola `entrada/saida/historico` externos. Para desenvolvimento, fixtures e raízes sintéticas próprias; evidência de preservação do workbook antes/depois quando houver mudança estrutural.

## Explícito

Reprocesso ou correção real, mudança de âncora, poda/cancelamento, migração de schema/workbook e entrega clínica. Uma rodada já autorizada deve seguir seu protocolo sem pedir confirmação a cada etapa, mas bloquear fonte ambígua/invariante inválido conforme as regras vigentes.

## Entrega

Diagnóstico local/código e workbook, inventário, proposta/diff, plano de preservação, workflow operacional versus desenvolvimento, comandos reais, handoff compacto com histórico acessível e health check. Reportar resultado de invariantes pelo checkpoint efetivamente executado; não copiar contagem de documento antigo.
