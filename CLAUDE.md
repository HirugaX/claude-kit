# Regras pessoais — valem em todo projeto desta máquina

- Ao recomendar modelo ou esforço, abrir ou fechar uma janela, escrever o prompt da próxima
  janela, planejar fases, delegar a subagentes ou começar trabalho longo sem supervisão: siga a
  skill `uso-do-claude` (o núcleo) e a peça do momento — `modelo-e-esforco`, `fechar-janela`,
  `orquestrar`. A regra do projeto vence quando as duas conflitarem.
- O prompt da próxima janela traz **o modelo e o comando `/effort <nível>` na primeira linha**, com o
  porquê em uma: o `/effort` confirmado fica gravado para as janelas seguintes, e o Sonnet 5.5 vai pelo
  ID `claude-sonnet-5-5` (o atalho `sonnet` abre o 5.5 desde a 2.1.291, mas atalho muda entre versões; o
  gancho do `nucleo` barra o Sonnet 5).
- `max`, `xhigh`, Fable e `ultracode` não são padrão: só com motivo escrito.
- Depois de um `/grill-me` de projeto novo ou de implementação nova, confirmado o entendimento:
  skill `recursos-do-projeto` antes do plano. No fim de todo grill e de todo plano, antes do "sim":
  a rodada de contingências (skill `uso-do-claude`, §7).
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
  quais, com o exemplo (skill `uso-do-claude`, §3). Havendo, o prompt da próxima janela sobe o
  degrau para aquele tipo de tarefa: esforço primeiro, Fable só depois de o Opus falhar.
- Tudo do Claude Code mora em `C:\CLAUDE-PROJETOS\claude-kit` (as skills em `plugins\<grupo>\skills\`,
  scripts, pesquisas, decisões, este arquivo, que o `~\.claude\CLAUDE.md` importa); os projetos, em
  `C:\CLAUDE-PROJETOS\`. Depois de `git pull` do kit: `python C:\CLAUDE-PROJETOS\claude-kit\scripts\instalar_kit.py
  --verificar` (sem o `--verificar`, conserta). Skill de terceiros nova ou atualizada: `scripts\atualizar_terceiros.py`,
  nunca `npx skills add` direto (ele grava em `~\.claude\skills` e repete o nome). Nunca um `CLAUDE.md` na raiz
  `C:\CLAUDE-PROJETOS\`: ele carregaria em todos os projetos.
- Antes de pesquisar (internet ou varredura grande), procure em
  `C:\CLAUDE-PROJETOS\claude-kit\pesquisas\INDICE.md`; depois de pesquisar, salve lá, no formato do
  índice (skill `pesquisa`). Nunca dado de paciente nem trecho de documento da operadora.
- Privacidade e isolamento: `C:\CLAUDE-PROJETOS\claude-kit\decisoes\adr\0001-privacidade.md` e
  `0002-isolamento.md`. Em resumo: o paciente aparece pelo pseudônimo (iniciais + 3 últimos dígitos do RA, ex.
  `FDSE-417`), só nos `desosp-`; nome completo só na conversa, quando o assunto é ele ou quando vem do conector do
  Drive, e nunca em arquivo, commit ou resumo; dado de paciente nunca no repositório de código, no kit, em
  `pesquisas\` nem fora dos `desosp-`; uma janela = um projeto; entre projetos, só pelos canais.
