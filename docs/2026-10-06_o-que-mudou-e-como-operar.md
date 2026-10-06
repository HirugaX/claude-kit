# O que mudou com as pesquisas sobre o uso do Claude — e como deixar de ser "office boy de prompt"

*06/10/2026 · escrito na janela do F1a para o Ettore · fonte deste texto:
`claude-kit\docs\2026-10-06_o-que-mudou-e-como-operar.md`. Os parênteses no fim das frases dizem de onde veio cada
afirmação (arquivo:linha): servem para conferir, não precisam ser lidos.*

Você trouxe quatro pesquisas (a de stack veio em duas cópias idênticas: Pesquisa_Stack_Profissional_Claude_Code.md:1, claude-efficiency-report.md:1). As conferências de 03 a 06/10 alimentaram o plano aprovado em 06/10 (2026-10-06_plano-fluxo.md:3-5).

## Parte 1 — As pesquisas que você trouxe

### 1.1 Relatório de stack

**O que dizia.** A melhor stack deixa o mínimo fixo no contexto (a conversa que o Claude relê a cada resposta) e confere por comando. Pedia CLAUDE.md (as regras que o Claude lê ao abrir o projeto) abaixo de 200 linhas, três papéis de subagente (ajudante com conversa própria) e Sonnet como modelo principal (Pesquisa_Stack_Profissional_Claude_Code.md:10, :12, :122, :334).

**Conferido.** De 11 afirmações checadas em 04/10, 9 se confirmaram e 2 só em parte: o Explore (subagente que só pesquisa) herda o modelo da sessão (não é Haiku) e o padrão no plano Max é o Opus 5.5 (2026-10-04_verificacao-recursos-claude-code.md:14-26, :35-55).

**Mudou.** Vão na mesma direção do relatório: skills por momento de uso (Q4), ganchos que barram (Q21) e os mesmos três papéis de subagente (Q13, Q18) (2026-10-06_entrevista-fluxo.md:122, :131, :180; 2026-10-06_plano-fluxo.md §Decisões da rodada).

**Recusado.** Sonnet como principal: a Q5 ficou com o Opus 5.5, na linha da evidência do relatório de uso e modelos
(1.4) (2026-10-06_entrevista-fluxo.md:123). Context7, GitHub MCP (conexão com ferramenta externa) e Playwright MCP, recusados em 04/10 (motivo escrito no app), voltam por projeto (2026-10-05_skills-e-plugins-avaliados.md:54; 2026-10-06_entrevista-fluxo.md:391).

### 1.2 Top 50 de skills e plugins

**O que dizia.** O passo seguinte não é instalar mais skills, e sim combinar skill (procedimento), gancho (programa que o Claude Code roda sozinho num evento), MCP e subagente (Relatorio_Claude_Code_Top_50_Skills_Plugins.md:443-452). Recomenda o repositório do Matt Pocock inteiro, o `planning-with-files` e o K-Dense, mas não instalar os 15 juntos nem vários harnesses (sistemas que coordenam agentes) (Relatorio_Claude_Code_Top_50_Skills_Plugins.md:176, :358, :362, :342-350).

**Conferido.** Candidatos lidos na fonte, com custo medido; estrelas não contaram (2026-10-05_skills-e-plugins-avaliados.md:9-10).

**Mudou.** Do Superpowers entrou só o `subagent-driven-development` (Q18); do K-Dense, 2 skills, só no espaço de pesquisa (Q11). O que o `planning-with-files` faz (devolver o plano ao Claude e travar o fim da tarefa) o plano refaz com `ESTADO.md` e ganchos próprios (Q3) (Relatorio_Claude_Code_Top_50_Skills_Plugins.md:275; 2026-10-06_espaco-de-pesquisa-clinica.md:14-17; 2026-10-06_plano-fluxo.md §Ficha, AGORA 3-4).

**Recusado.** O plugin (pacote de skills e ganchos) `planning-with-files`, segundo dono do estado, e os harnesses, que conflitam com o método do kit (2026-10-05_skills-e-plugins-avaliados.md:45, :51).

### 1.3 Pasta Claude_Workbench_Prompts

**O que dizia.** Quinze arquivos feitos no ChatGPT Work (00_INICIO.md:3, :9): o mesmo ambiente nos dois PCs (01_MASTER_WORK.md:3); estado num arquivo de ~1.000 palavras; sessão nova testada em pasta sintética (com dados de mentira) antes de automatizar (04_HANDOFF_PROTOCOL.md:21, :61-82).

**Conferido.** O `claude --bg` (abre sessão em segundo plano) existe, mas é prévia de pesquisa; bifurcar ou retomar uma conversa copia o contexto, não limpa; que o Claude o lance sozinho não está documentado (2026-10-05_sessoes-memoria-plugins-claude-code.md:19-22, :63-64).

**Mudou.** Um só dono do estado (Q3), fase seguinte por `claude --bg` depois de teste sintético (Q9), kit privado no GitHub para os dois PCs (Q6). O teste virou o F3a (o laço, as fases se lançando sozinhas; F3b: ferramentas; F3c: ajustes) (2026-10-06_entrevista-fluxo.md:121, :124, :127; 2026-10-06_plano-fluxo.md §A cadeia).

**Recusado.** Os prompts por projeto só viraram checklist: os de 10 a 12, no F8 (2026-10-06_plano-fluxo.md §F8).

### 1.4 Relatório de uso e modelos

**O que dizia.** "Sonnet para o fácil, Opus para o difícil", "`max` é sempre melhor" e "janela nova sempre economiza" não resistem à evidência (claude-uso-modelos.md:7). Em teste independente, o Opus 5.5 em esforço menor (o quanto o Claude pensa antes de responder) em geral igualou ou superou o Sonnet 5.5 em esforço maior, por custo igual ou menor (claude-uso-modelos.md:9).

**Conferido.** Em 03/10: índices e preços batem; `max` pior que `xhigh` é dado do fabricante; trocar o esforço no meio da sessão mantém o cache (releitura barata), trocar de modelo não (2026-10-03_modelo-e-esforco-claude-code.md:20-31).

**Mudou.** A ordem do relatório (melhorar a especificação, subir `medium` para `high`, trocar para Opus, só então `xhigh` ou `max`) virou a peça `modelo-e-esforco` (Q4); Opus 5.5 `medium` na janela, `high` em plano e regra clínica (Q5); fecha-se por fase, ~150 mil tokens (pedaços de texto) ou troca de modelo (Q9) (claude-uso-modelos.md:487-495; 2026-10-06_entrevista-fluxo.md:123, :127, :161-163).

**Recusado.** `max`, `xhigh`, Fable e ultracode (workflows com vários agentes) como padrão (`max` rendeu menos que `xhigh` em teste do fabricante) (2026-10-06_plano-fluxo.md §Como você opera; 2026-10-03_modelo-e-esforco-claude-code.md:25).

### Recomendação → virou o quê

| Recomendação | Virou |
| --- | --- |
| CLAUDE.md curto, skills sob demanda, ganchos | Adotado (Q4, Q21; meta de menos de 200 linhas: 2026-10-06_plano-fluxo.md §Verificação) |
| Estado em arquivo | Adotado com ajuste: sem plugin (Q3) |
| Sonnet como principal; ordem para subir de modelo | Adotado com ajuste: Opus 5.5 na janela, Sonnet 5.5 nos ajudantes (Q5); a ordem, em peça própria (Q4, Q10) |
| Matt Pocock, K-Dense, Superpowers | Adotado com ajuste: 20 skills do Matt, 2 do K-Dense, 4 avulsas do Superpowers (2026-10-05_skills-e-plugins-avaliados.md:27-28; Q18) |
| `claude-mem`, oh-my-claudecode, Headroom, `claude-code-setup` | Testar no F3b, a seu pedido; a conferência de 06/10 dizia "não instalar" (oh-my-claudecode: só em pasta de teste) (2026-10-06_ferramentas-pedidas-e-orquestradores.md:15-17; 2026-10-06_entrevista-fluxo.md:385; Q19) |
| `planning-with-files`, GSD, times de agentes | Recusado: segundo dono do estado; ~7 vezes o custo (2026-10-06_plano-fluxo.md §Ficha, NÃO) |
| Context7, GitHub MCP, Playwright MCP | Recusado em 04/10; volta por projeto (2026-10-06_plano-fluxo.md §Ficha, QUANDO) |

## Parte 2 — Como deixar de ser "office boy de prompt"

### (a) O diagnóstico em números

O custo grande é a conversa, não as skills: desde 28/09 a mediana de contexto por chamada ficou em 199 a 317 mil tokens (2026-10-06_entrevista-fluxo.md:99-101). Cada janela exige ~7 passos manuais, 4 só de transporte: abrir, copiar, colar e digitar o `/effort` (2026-10-06_entrevista-fluxo.md:107). Os handoffs (arquivos de passagem entre janelas) chegam a 575 KB e 376 KB (2026-10-06_entrevista-fluxo.md:105).

### (b) O desenho novo

- **`docs\ESTADO.md`**: a página de "onde estamos", reescrita a cada fechamento; os handoffs antigos ficam congelados, lidos só por busca (2026-10-06_entrevista-fluxo.md:121).
- **`docs\PROXIMO.md`**: o prompt da próxima fase, escrito pela janela que fecha, com modelo e `/effort` na primeira linha (2026-10-06_plano-fluxo.md §Ficha, AGORA 3; §F2).
- **`claude --bg`**: a janela que termina lança a próxima, que lê o `PROXIMO.md` e segue. Desligado até o F3c (2026-10-06_plano-fluxo.md §Ficha, AGORA 5).
- **Ganchos**: barram o atalho `sonnet` (que abre o Sonnet 5 por engano), avisam modelo e esforço errados, impedem fechar a fase sem o `ESTADO.md` e barram gravação em pasta de dado fora da lista aprovada. Custam quase zero token (2026-10-06_plano-fluxo.md §Ficha, AGORA 4).
- **Pontos de parada (Q10)**: o Claude para e pergunta antes de gravar em dado real, rodar rodada real ou reprocesso sem aprovação prévia, mexer em banco ou esquema, criar regra clínica, ler fonte nova, subir para Fable, `xhigh`, `max` ou ultracode, repetir o erro após duas tentativas diferentes ou decidir algo fora do `ESTADO.md` e dos ADRs (registros de decisão). Descer para modelo mais barato, mantendo a qualidade, não pergunta (2026-10-06_entrevista-fluxo.md:128).
- **Statusline e `claude agents`**: a statusline é a linha do terminal com modelo, esforço e % do contexto. `claude agents` lista o que roda; `attach <nome>` entra; `logs <nome>` mostra sem entrar; "Needs input" avisa que a fase precisa de você (2026-10-06_plano-fluxo.md §Como você opera).

### (c) O que vale quando

**Até o F3 terminar, como hoje, pela última vez** (2026-10-06_plano-fluxo.md §Como você opera):

1. Abra a janela na pasta que o prompt indica e digite o `/effort` da primeira linha; se pedir Sonnet 5.5, escolha na lista do `/model`, nunca digite `sonnet`.
2. Cole o prompt e responda nos pontos de parada com a letra e a nuance ("a, mas sem X").
3. Ao fechar, copie o prompt da próxima e abra outra janela; duas juntas só onde o plano diz.

**Depois do F3c, se o teste do laço passar** (2026-10-06_plano-fluxo.md §Como você opera):

1. A janela que termina grava `ESTADO.md` e `PROXIMO.md` e lança a seguinte: `claude --bg --name <fase> --model <modelo> --effort <nível> "Leia docs/PROXIMO.md e siga"`.
2. Você acompanha no terminal com `claude agents`, `attach` e `logs`.
3. Você entra só nos pontos de parada e para aprovar plano novo, com "Yes, clear context and…" (limpa o planejamento da conversa; o F3a ainda testa isso no painel do VS Code) (2026-10-06_continuar-em-contexto-limpo-sem-copiar-prompt.md:68-69).
4. Reserva, e único caminho se o laço não passar: `/clear` e "siga"; um gancho injeta o `PROXIMO.md`; ficam dois gestos seus (2026-10-06_continuar-em-contexto-limpo-sem-copiar-prompt.md:14-16; 2026-10-06_plano-fluxo.md §F3c).
5. Celular: só se o experimento do F3a passar, e com uma janela pequena.

### (d) O que continua sendo seu (2026-10-06_plano-fluxo.md §Como você opera, §Decisões que ficaram)

- O `/effort`; `max`, `xhigh`, Fable e ultracode só com motivo escrito.
- Nunca rodar `/omc-setup`, que sobrescreve seu CLAUDE.md pessoal.
- Mover ou apagar pasta de projeto e mexer na raiz do `C:`.
- Aplicar a política do safety-net (plugin que barra comandos destrutivos) quando nascer pasta de dado nova.
- O "sim" antes de qualquer mudança e as decisões que o plano deixou para as fases.

### (e) As metas medidas (2026-10-06_plano-fluxo.md §Verificação)

| Medida | Antes (05/10) | Meta |
| --- | --- | --- |
| Passos manuais por janela | ~7, 4 de transporte | no máximo 2 gestos seus por fase, depois do F3c (§Ficha, AGORA 5) |
| Contexto mediano por chamada | 199 a 317 mil tokens | até 120 mil |
| Custo de abrir (ctx0): app, kernel, planilha | 58, 66 e 55 mil | até 40, 50 e 45 mil |
| Linhas do CLAUDE.md: app, kernel, planilha | 354, 430 e 226 | menos de 200 |
| Chamadas no Sonnet 5 por engano | 188 (03/10) | 0 |

### (f) Onde olhar e quando algo dá errado (2026-10-06_plano-fluxo.md §Como você opera)

- **Onde olhar:**
  - o estado de cada projeto, em `docs\ESTADO.md` (uma página);
  - o que vem, em `docs\PROXIMO.md`;
  - o porquê, em `docs\adr\` (no kit, `decisoes\adr\`);
  - no terminal, a statusline;
  - o custo, com `medir_uso.py --sessoes`;
  - as skills de cada projeto, na seção "Skills deste projeto" do CLAUDE.md e no `GUIA_DAS_SKILLS.docx`.
- **A fase falhou no mesmo ponto duas vezes:** ela anota no `ESTADO.md` e para. Você escolhe repetir com esforço
  maior ou voltar ao `/grill-me`.
- **Aviso de troca para o Opus 5 no meio da conversa:** `/model` e escolher o Opus 5.5.
- **Duas janelas no mesmo projeto:** feche uma e rode `git status`.
- **Arquivo solto no Drive:** vai para `IA\00-entrada`.

## Parte 3 — Privacidade em uma página (ADR-0001 e ADR-0002, 06/10)

O que você decidiu em 06/10, numa minientrevista de duas rodadas. As regras completas estão em
`claude-kit\decisoes\adr\0001-privacidade.md` (privacidade) e `0002-isolamento.md` (isolamento entre projetos).

**O paciente aparece por pseudônimo.**
- Formato: as iniciais de todos os nomes, mais hífen e os 3 últimos dígitos do RA. Exemplo, com nome inventado:
  Fulana de Souza Exemplo → `FDSE-417`.
- Quem faz a troca é o script que lê a planilha, não o Claude. Por isso não gasta token: a sigla é até mais curta que
  o nome.
- O pseudônimo pode aparecer em tudo dos projetos `desosp-` (conversa, `ESTADO.md`, resumo, caixa, relatório,
  commit). Fora deles, nunca.
- Com só as iniciais, duas pessoas repetiriam a sigla quase sempre num censo de ~200; com os 3 dígitos, cerca de 1%.
  Quando repetir, o script usa 4 dígitos.

**O nome completo** (e os números inteiros: RA, telefone, CPF, CNS, Marca Ótica):
- entra na conversa só quando o assunto é ele: grafia, o mesmo paciente em duas fontes, telefone errado;
- também entra o que o conector do Google Drive trouxer — essa foi a sua escolha, com a consequência à vista;
- nunca vai para arquivo fora das pastas de dado, commit, `ESTADO.md`, resumo ou caixa.

**Onde o dado pode morar.**

| lugar | dado de paciente |
|---|---|
| repositório de código (GitHub) | nunca. O pre-commit de nomes vai para o app e o censo, como já existe no HC |
| repositório privado só de dado (`<projeto>-dados`) | pode, quando precisar sincronizar entre os PCs. Nunca público, sem fork, verificação em duas etapas |
| Google Drive pessoal, `IA\desosp-*` (Restrito) | pode. Nunca "qualquer pessoa com o link" |
| conectores do claude.ai nos `desosp-` | só o Google Drive. Os outros ficam negados e valem só nos projetos pessoais |
| claude-mem | fora dos `desosp-`, enquanto o banco dele for um só para todos os projetos |
| Headroom | pode nos `desosp-`, se passar no teste do F3b, só no terminal, com o envio de uso desligado |
| `pesquisa-`, `estudo-`, `pessoal-`, o kit | nunca: a pesquisa recebe só a pergunta; o estudo, o caso desidentificado |

**Dentro dos projetos:** o Claude fica sem acesso ao dado bruto (entrada, histórico, cópias, `privado\`). A pasta de
trabalho da rodada fica aberta. Os scripts continuam lendo tudo.

**Mensagem para fora (e-mail, WhatsApp):** o Claude escreve com `{{nome}}`, `{{matricula}}` e `{{telefone}}`; um
script no PC preenche; quem envia é você.

**O que não depende de você (dito uma vez):**
- o dono do dado é o hospital ou a operadora, e a política deles pode proibir o envio a terceiros;
- a LGPD trata dado de saúde como sensível (art. 11) e o envio para servidor fora do Brasil como transferência
  internacional (art. 33);
- o treino com as suas conversas está desligado, e isso vale também para o Claude Code. A Anthropic guarda as
  conversas por 30 dias; conversa marcada com 👍/👎 pode ser usada.

**Quando passa a valer:**
- já vale no kit e no seu CLAUDE.md pessoal;
- em cada projeto, na fase dele: app no F5a, censo no F6, planilha no F7. Até lá, valem as regras antigas de cada
  projeto.
