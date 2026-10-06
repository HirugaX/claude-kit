# PROMPT adicional — Home Care Excel encontrado no GitHub

Configure Claude Code para `HirugaX/desosp-hc`, projeto adicional aos cinco inicialmente descritos. Não confundir com folha/RH nem com kernel do censo. Primeiro audite e proponha; mudanças de configuração conforme plano aprovado. Não operar rodada, alterar dados reais ou distribuir planilhas como teste de configuração.

## Contexto confirmado

Sistema de planilhas das unidades e master Home Care, com scripts Python, ExcelJS 4.4.0, dependências PDF/Word/XLSX e recálculo LibreOffice documentado. Versionamento de código/docs separado das pastas clínicas e da senha local. Leia os arquivos atuais: `README.md`, `CLAUDE.md`, `docs/00_INDICE.md`, ambiente/validação, caixa `docs/para_a_planilha/INDICE.md` e `scripts/config.py`.

12 comandos existem em `.claude/commands/`; `SessionStart` chama `scripts/caixa_pendente.py`. Esse hook injeta pendências da caixa para não depender de pedido manual. Preservar esse padrão de comunicação, sem reinjetar documentos inteiros.

## Auditar

Mapear template/unidades/master, schema, fórmulas, tables/named ranges, proteção/validação, correções, consolidação e PDFs. Confirmar versão vigente pelo código, não por número copiado de um README. Verificar funções puras versus gravação, isolamento dos testes, backups e diferença entre cópia recalculada e arquivo de entrega.

Auditar Git hooks de privacidade/destino e scripts associados antes de executar. Não mover senha, pacientes, rodadas e relatórios reais para configuração compartilhada. Registre variáveis/paths sem valores privados.

Leia todos os corpos dos comandos: o Work examinou árvore/README, mas não todos os efeitos. Migrar commands para skills somente se houver ganho claro e preservando nomes, política de intenção e referências.

## Configuração

Router curto: finalidade, limites, caixa de entrada, comandos básicos e índice. Conhecimento detalhado do workbook/rodada/placar/versão em refs. Skills oficiais XLSX/PDF/DOCX sob demanda, mais debug/review/spec globais conforme necessidade. Não incluir biblioteca React ou pesquisa clínica como núcleo deste projeto.

Agents: review de fórmulas/consolidação e privacidade para alterações relevantes, contexto delimitado. Hook de caixa permanece curto e não dispara rodada. Checks de ambiente/privacidade automatizados com boundaries claras; não instalar múltiplos guardrails sem medir redundância.

MCPs somente para acesso necessário e autorizado; bibliotecas locais e scripts já existentes são o caminho principal. Arquivo Excel binário precisa política de writer único; Git não faz merge seguro de workbook.

## Continuidade

Siga `04_HANDOFF_PROTOCOL.md`. Separar desenvolvimento de operação da rodada. Handoff de código referencia spec, branch, testes, dependências e próxima ação. Estado de rodada referencia arquivos locais e decisões autorizadas, sem copiar dados clínicos para arquivo versionado.

Background para implementação/teste com fixtures e cópias isoladas. Um worker não pode atualizar template/versionamento enquanto outro monta entrega na mesma pasta. Nome `hc-validacao-<id>` ou `hc-versao-<id>`, com bloqueios/notificações recuperáveis.

## Explícito

Fechar/entregar/subir rodada, hospital/versão novos, alteração de fórmulas/proteção e correção real seguem intenção e protocolo vigente. Mensagens podem ser preparadas; envio externo não está autorizado pela configuração deste projeto.

## Entregar

Diagnóstico e catálogo real dos 12 comandos, proposta/diff sem perder a caixa de comunicação, estado mínimo, health check e guia. Validar ambiente por mecanismo atual em `scripts/verifica_ambiente.py`; testes de recalculação em cópia e inspeção do resultado, sem declarar verificação visual se não abriu/renderizou o artefato.
