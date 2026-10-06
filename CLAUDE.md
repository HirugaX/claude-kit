# Regras pessoais — valem em todo projeto desta máquina

- Ao recomendar modelo ou esforço, abrir ou fechar uma janela, escrever o prompt da próxima
  janela, planejar fases, delegar a subagentes ou começar trabalho longo sem supervisão: siga a
  skill `uso-do-claude`. A regra do projeto vence quando as duas conflitarem.
- O prompt da próxima janela traz **o modelo e o comando `/effort <nível>` na primeira linha**, com o
  porquê em uma: o `/effort` confirmado fica gravado para as janelas seguintes, e o Sonnet 5.5 se
  escolhe na lista do `/model` (o atalho `sonnet` abriu o Sonnet 5).
- `max`, `xhigh`, Fable e `ultracode` não são padrão: só com motivo escrito.
- Depois de um `/grill-me` de projeto novo ou de implementação nova, confirmado o entendimento:
  skill `recursos-do-projeto` antes do plano.
- O contexto é o custo que mais pesa: `/clear` ao mudar de assunto, `/compact <o que preservar>`
  num ponto natural, material volumoso (logs, varreduras, páginas) para subagente.
- Pergunta que é decisão do usuário vai no chat, elaborada: o problema, a pergunta escrita como
  pergunta, as opções com a recomendação e o que muda com cada resposta. Decisão técnica de
  rotina se resolve sem perguntar.
- Nenhuma alteração — código, skill, configuração, documento, pasta — sem antes mostrar no chat o
  que foi verificado (arquivos, medições, documentação, internet), o que se achou, com a fonte
  (arquivo:linha, link ou comando), as opções com a recomendação e exatamente o que vai mudar; e
  esperar o "sim". Um pedido explícito ("rode a manhã", "corrija X") e um plano aprovado já são o
  "sim" do que pedem; o *como* continua com o Claude.
- Todo resumo de fim de janela traz a linha "Sinais de insuficiência do modelo: nenhum" — ou
  quais, com o exemplo (skill `uso-do-claude` §2b). Havendo, o prompt da próxima janela sobe o
  degrau para aquele tipo de tarefa: esforço primeiro, Fable só depois de o Opus falhar.
- Tudo do Claude Code mora em `C:\CLAUDE-PROJETOS\claude-kit` (skills, scripts, pesquisas, decisões,
  este arquivo); os projetos, em `C:\CLAUDE-PROJETOS\`. Skill nova instalada ou atualizada com
  `npx skills`: rodar `python C:\CLAUDE-PROJETOS\claude-kit\scripts\ligar_claude.py` (se avisar que a
  pasta difere da do kit: `--pasta-vence` para atualização do npx, `--kit-vence` para cópia velha).
- Antes de pesquisar (internet ou varredura grande), procure em
  `C:\CLAUDE-PROJETOS\claude-kit\pesquisas\INDICE.md`; depois de pesquisar, salve lá, no formato do
  índice (skill `uso-do-claude` §5). Nunca dado de paciente nem trecho de documento da operadora.
- Privacidade e isolamento: `C:\CLAUDE-PROJETOS\claude-kit\decisoes\adr\0001-privacidade.md` e
  `0002-isolamento.md`. Em resumo: o paciente aparece pelo pseudônimo (iniciais + 3 últimos dígitos do RA, ex.
  `FDSE-417`), só nos `desosp-`; nome completo só na conversa, quando o assunto é ele ou quando vem do conector do
  Drive, e nunca em arquivo, commit ou resumo; dado de paciente nunca no repositório de código, no kit, em
  `pesquisas\` nem fora dos `desosp-`; uma janela = um projeto; entre projetos, só pelos canais.
