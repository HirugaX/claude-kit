# Estudo para a residência e produtividade pessoal — recursos, evidência e desenho (06/10/2026)

- **A pergunta:** que recursos (skills, plugins, MCPs, conectores, métodos) servem a dois projetos pessoais do
  Ettore — (A) estudo para a residência médica (Anki, resumos com esquemas, mnemônicos, recursos interativos como o
  "aparato" de ECG que o Gemini montou, perguntas para memorizar, escrever o que estudou, o acervo de resumos do
  cursinho) e (B) produtividade (organização, hábitos, procrastinação, Notion) — e aprender código sendo vibe coder?
- **A data:** 06/10/2026.
- **O projeto que pediu:** claude-kit → grill dos projetos de estudo e de produtividade (`decisoes\2026-10-06_entrevista-fluxo.md` §12.5).
- **Conferir de novo depois de:** 06/11/2026.
- Marcas: [A] = afirmação do autor sem medição; [I] = inferência. "Fixo" = tokens por turno da descrição; skill só `/` custa 0.
  Nada foi instalado.

## Conclusão em poucas linhas

1. **Dois projetos.** A = Claude Code numa pasta (`estudo-residencia\`), com scripts e skills próprias. B = um Project
   do claude.ai com os conectores Notion e Google Calendar (anda no celular). Ferramentas, sensibilidade e ritmo
   diferentes; skill de projeto só carrega no projeto dela.
2. **Para o A não existe skill pronta de terceiros que preste:** seis skills próprias só `/` (fixo 0) — `/ingerir`,
   `/resumo`, `/quiz`, `/explica-de-novo`, `/flashcards`, `/simular` —, extração local de PDF e Word, e o conector
   PubMed. Regras copiadas de quem fez bem (`law-student` da Anthropic, `feynman` do paperthin, Exam Cram Coach).
3. **O que a evidência manda:** testar-se e espaçar têm utilidade ALTA; resumir, grifar, reler e mnemônico de
   palavra-chave, BAIXA (Dunlosky 2013). Então o resumo **termina em perguntas** e o produto final é quiz e cartão. IA
   ajuda quando exige esforço e atrapalha quando entrega a resposta (−17% na prova, Bastani 2025): o Claude pergunta
   antes de explicar.
4. **Anki: arquivo TSV, sem MCP.** O AnkiConnect original está arquivado e aceita apagar notas sem chave. Cartão
   gerado por LLM erra de modo medido (49% de falha de redação e 22% de erro factual numa série; 1% de erro grave nos
   aprovados em outra): revisão humana, lotes de 5-10, campo Fonte, nada importado sem "sim".
5. **O "aparato" do ECG = uma página HTML única**, local (nada sai do PC) ou como Artifact privado para ver no celular,
   com âncoras numéricas com fonte, autoteste e caixa de limitações.
6. **Alerta de isolamento:** os conectores do claude.ai (Notion, Google Calendar, Gmail…) valem em **todo** projeto do
   Claude Code quando se está logado. No projeto de estudo: `disableClaudeAiConnectors: true` no
   `.claude\settings.json` e o PubMed no `.mcp.json` do projeto.
7. **Aprender código:** os estilos `Learning` e `Explanatory` são nativos (`/output-style learning` grava em
   `.claude\settings.local.json`, só na pasta); os plugins oficiais de mesmo nome são redundantes. Opcional leve: a
   skill `learning-opportunities` (Dr. Cat Hicks).

## A — Anki

- **TSV com cabeçalhos** (`#separator:tab`, `#html:true`, `#notetype`, `#deck`, `#guid column`); reimportar com o mesmo
  GUID atualiza ([manual](https://docs.ankiweb.net/importing/text-files.html)). TSV não leva mídia nem Image
  Occlusion; para imagens em lote, [genanki](https://github.com/kerrickstaley/genanki) (fixar o GUID com `guid_for`).
- **AnkiConnect/MCP: nenhum agora.** [FooSoft/anki-connect](https://github.com/FooSoft/anki-connect) arquivado; escuta
  em 127.0.0.1:8765 sem chave e aceita `deleteNotes`. Se um dia: o add-on [ankimcp](https://github.com/ankimcp/anki-mcp-server-addon)
  (AGPL, `delete_notes` em `disabled_tools`); nunca o [nailuoGG](https://github.com/nailuoGG/anki-mcp-server) (apaga sem trava).
- **Image Occlusion:** o modelo erra coordenadas; o Claude lista os rótulos, o Ettore cria no editor nativo.
- **Regras da `/flashcards`:** uma informação por cartão; sem sim/não nem listas; cloze só na palavra-chave; cartão
  autônomo; campo Fonte (aula, página); só conteúdo da fonte; prévia de 5; nada importado sem "sim". Modelos para
  copiar regras: [anki-card-forge](https://github.com/FrostySL/anki-card-forge) (`grounding_check`), [loftiskg](https://github.com/loftiskg/anki-claude-code-skill).
- **Erro medido em cartão/questão gerada:** [Advances in Physiology Education](https://doi.org/10.1152/advan.00106.2024)
  (49% redação, 22% factual; 91% aproveitáveis com revisão); [npj Digital Medicine](https://doi.org/10.1038/s41746-026-02978-8) (1% de erro bloqueante nos aprovados, 1.284 cartões).

## A — Resumos visuais e interativos

| formato | VS Code | navegador | Anki |
|---|---|---|---|
| Mermaid (fluxograma) | preview nativo do Markdown | precisa de mermaid.js | só como PNG ([mermaid-cli](https://github.com/mermaid-js/mermaid-cli)) |
| mapa mental | lista Markdown (o `mindmap` do Mermaid é experimental) | `npx markmap-cli x.md` gera HTML | PNG |

- O chat da extensão do Claude Code **não** renderiza Mermaid ([issue 20529](https://github.com/anthropics/claude-code/issues/20529),
  "not planned"): pedir um `.md` e abrir o preview.
- **Não instalar:** excalidraw-mcp, drawio-mcp, `canvas-design`, `theme-factory` (Excalidraw ≈ 3,7 mil tokens por
  diagrama × Mermaid de 7 nós ≈ 73 [I]).
- **Interativo:** HTML único sem CDN (offline) ou [Artifacts](https://support.claude.com/en/articles/17153992-what-are-artifacts-and-how-do-i-use-them).
  O `playground` oficial não simula fisiologia. Modelo de rigor: [tareko/ventilator-sim](https://github.com/tareko/ventilator-sim)
  (sem rede, 77 testes). Pedir: âncoras numéricas com fonte antes de codificar (P50 ≈ 26-27 mmHg; PR 120-200 ms;
  ECG a 25 mm/s), autoteste em `node`, caixa "Limitações". Erros típicos: kPa × mmHg; o sentido do desvio da curva da
  hemoglobina. Custo ≈ 1,5-4,5 mil tokens por simulação [I].

## A — Do Google ao Claude; aula gravada

| Google | o equivalente no Claude |
|---|---|
| [Guided Learning](https://blog.google/products-and-platforms/products/education/guided-learning/) (Gemini: tutor que pergunta, divide em passos, aplica quiz) | o estilo `Learning` do claude.ai (para todos desde 14/08/2025 [A]) + `/quiz` e `/explica-de-novo` |
| [Gemini Notebook](https://blog.google/innovation-and-ai/products/gemini-notebook/notebooklm-gemini-notebook/) (ex-NotebookLM: chat com citação nas fontes, áudio, mapas, quiz) | o acervo local + `/ingerir`, ou um Project do claude.ai (RAG nos planos pagos) |
| o "aparato" do ECG | HTML único (acima) |

- **Ligar o Claude ao Gemini Notebook: não** (sem API para conta pessoal; os conectores usam cookies e rotas não
  documentadas; o `notebooklm-skill` está arquivado desde 10/09/2026; o `open-notebook` exige Docker e chave de API).
- **Aula gravada → texto:** `pip install faster-whisper` (CPU int8, sem ffmpeg). No i5-1345U, 1 h de aula ≈ 20 min no
  modelo `small`, ≈ 1 h no `medium` [I]. Termo médico erra (WER 0,37 do large-v3 em anamneses pt-BR,
  [SBBD](https://sol.sbc.org.br/index.php/sbbd/article/download/30715/30518)): usar `initial_prompt` com os termos e
  deixar o Claude corrigir. O Claude não recebe áudio: transcrever antes, `.txt` com `[hh:mm:ss]`.

## A — O acervo do cursinho

- **Padrão:** [gist de Karpathy](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) — fontes imutáveis →
  nota por tema → índice, com página.
- **Cadeia no Windows:** `pip install pymupdf pymupdf4llm` (texto, imagens, páginas); `winget install oschwartz10612.Poppler`
  (sem o `pdftoppm`, a ferramenta Read do Claude não lê PDF de mais de 10 páginas — falta neste PC); `winget install
  JohnMacFarlane.Pandoc` (Word); Tesseract só para escaneado.
- **Imagem custa** ≈ ⌈largura/28⌉ × ⌈altura/28⌉ tokens ([Vision](https://platform.claude.com/docs/en/build-with-claude/vision)):
  ler o fluxograma UMA vez e gravá-lo como Mermaid na nota.
- **Índice:** nota por tema com frontmatter (tema, especialidade, fonte, páginas, imagens, siglas) + `MAPA-<especialidade>.md`
  + `INDEX.md`; busca por `rg`. Um tema ≈ 5-15 mil tokens contra 1-2 milhões para reler 750 páginas [I]. Embeddings só
  se um teste de 20 perguntas falhar.
- **Contra responder "de memória":** regra no CLAUDE.md — resposta em "No acervo (nota, página)" ou "Fora do acervo
  (conferir)". Modelo de código: [Exam Cram Coach](https://github.com/ZeKaiNie/universal-examprep-skill) (MIT; extrai
  texto e figuras com `[arquivo p.N]`; sem rede).
- **Direitos:** [Lei 9.610](https://www.planalto.gov.br/ccivil_03/leis/l9610.htm), art. 46 — uso privado de pequenos
  trechos e apanhado de lições, vedada a publicação; ler o contrato do cursinho; nunca publicar.
- **Dados enviados ao Claude:** com a opção de uso para melhorar os modelos ligada, há treino e retenção de 5 anos;
  desligada, 30 dias ([doc](https://code.claude.com/docs/en/data-usage)); ajuste em claude.ai/settings/data-privacy-controls.

## A — Educação no Claude e o que a literatura sustenta

- **Tutoria pronta para residência: nenhuma séria.** Copiar regras (não instalar) de
  [`law-student`](https://github.com/anthropics/claude-for-legal) (Anthropic: `socratic-drill` não dá a resposta antes
  da tentativa; `flashcards` em caixas de Leitner +1/+3/+7/+21 dias, `[VERIFY]` em carta sem fonte) e do
  [`feynman` do paperthin](https://github.com/LilMGenius/paperthin) (você explica antes; um furo por vez).
- **Não:** [anthropics/healthcare](https://github.com/anthropics/healthcare) (FHIR/CID-10 americano);
  [Open Medical Skills](https://github.com/Open-Medica/open-medical-skills) (uma referência dela aponta para
  [outro artigo](https://pubmed.ncbi.nlm.nih.gov/25693988/)). Referência inventada por LLM é medida
  ([Cureus 2023](https://doi.org/10.7759/cureus.39238); [Sci Rep 2023](https://doi.org/10.1038/s41598-023-41032-5)): só PMID conferido.

| achado | fonte | consequência no desenho |
|---|---|---|
| teste e espaçamento: ALTA; autoexplicação, intercalação: média; resumir, grifar, reler, mnemônico de palavra-chave: BAIXA | [Dunlosky 2013](https://doi.org/10.1177/1529100612453266) | `/resumo` termina em perguntas; o produto final é cartão ou quiz |
| ECR com 40 residentes: teste 39% × estudo 26% aos 6 meses (d = 0,91) | [Larsen 2009](https://pubmed.ncbi.nlm.nih.gov/19930508/); [Rowland 2014](https://pubmed.ncbi.nlm.nih.gov/25150680/); [Adesope 2017](https://doi.org/10.3102/0034654316689306) | `/quiz` pede a resposta antes de mostrar |
| espaçar funciona, inclusive com estudantes de medicina | [Cepeda 2006](https://pubmed.ncbi.nlm.nih.gov/16719566/); [Kerfoot 2007](https://pubmed.ncbi.nlm.nih.gov/17209889/) | o Anki agenda; `erros.md` com revisão +1/+3/+7/+21 |
| intercalar ajuda (g = 0,42), mas vocabulário vai melhor em blocos (g = −0,39) | [Brunmair 2019](https://pubmed.ncbi.nlm.nih.gov/31556629/) | `/quiz` mistura diagnósticos parecidos; siglas em bloco |
| Anki: só dado observacional | [Deng 2015](https://pubmed.ncbi.nlm.nih.gov/26498443/) | revisão diária, sem promessa causal |
| regras de Wozniak e Matuschak: opinião de autor [A] | [Wozniak](https://www.supermemo.com/en/blog/twenty-rules-of-formulating-knowledge) | boa prática, não evidência |
| IA ajuda quando exige esforço; atrapalha quando entrega a resposta | [Kestin 2025](https://pubmed.ncbi.nlm.nih.gov/40537565/); [Bastani 2025](https://pubmed.ncbi.nlm.nih.gov/40560616/) | o Claude pergunta antes de explicar |
| "estilos de aprendizagem" sem base | [Pashler 2008](https://doi.org/10.1111/j.1539-6053.2009.01038.x) | visual × texto pelo conteúdo |

## A — As seis skills próprias (todas só `/`) e a pasta

| skill | faz |
|---|---|
| `/ingerir` | script local extrai texto e imagens para `acervo\texto\<tema>.md`, com páginas, e atualiza o MAPA; o modelo não lê o PDF inteiro |
| `/resumo <tema>` | lê o MAPA e 1-3 notas; resumo, fluxograma Mermaid, mapa em lista; cada afirmação com nota e página; "fora do acervo" marcado; fecha com 3 perguntas |
| `/quiz <tema>` | uma pergunta por vez, sem dica; você responde antes; corrige só com trecho (arquivo:página) ou PMID conferido, senão `[VERIFICAR]`; erro vai a `quiz\erros.md`; abre pelos vencidos; intercala 2-3 temas |
| `/explica-de-novo` | outro ângulo e analogia; você escreve de volta; o Claude aponta o maior furo sem dar a resposta |
| `/flashcards <tema>` | prévia de 5; TSV com Fonte em `anki\rascunho\`; nada importado sem "sim" |
| `/simular <tema>` | HTML único com âncoras numéricas e `FONTES.md` |

```
C:\CLAUDE-PROJETOS\estudo-residencia\
  CLAUDE.md     < 80 linhas: responder do acervo, citar nota + página, nunca dado de paciente
  .mcp.json     só o PubMed
  .claude\      settings.json (disableClaudeAiConnectors: true) · rules\{cartoes,resumos}.md · skills\{as 6}\
  acervo\       originais\ (só leitura) · texto\ · img\ · MAPA-<especialidade>.md · INDEX.md
  notas\  resumos\  simulacoes\<tema>\{index.html,FONTES.md}  anki\{rascunho,aprovado}\  transcricoes\  quiz\erros.md
  docs\         ESTADO.md · adr\        .gitignore: acervo\ e transcricoes\
```

## B — Produtividade

- **Conectores, não plugin.** Notion: o conector do claude.ai (o Claude Code logado o herda); o
  [plugin oficial](https://github.com/makenotion/claude-code-notion-plugin) traz o mesmo servidor + 4 skills de equipe:
  não precisa. O MCP do Notion "age com todas as suas permissões" ([ajuda](https://www.notion.com/help/notion-mcp)):
  usar um workspace separado. Agenda: [conector Google Calendar](https://claude.com/connectors/google-calendar) (cria e
  apaga), sem Google Cloud. Todoist só se já usa.
- **Skill pronta que sirva: nenhuma.** Escrever a própria, com 9 regras: uma lista (Notion) e uma agenda; nada criado
  ou alterado sem confirmação; tarefa = próxima ação de 15/30/60 min com gatilho "se-então"; até 3 prioridades por
  dia; bloquear só prioridade, com 30% de folga e título genérico; revisão semanal de 30 min, registrada; adiada 3
  vezes = dividir, delegar, fazer em 2 min ou descartar; um hábito por vez, na versão de 2 minutos; nunca dado de paciente.
- **Evidência das regras:** intenção de implementação "se-então", d = 0,65 ([Gollwitzer & Sheeran 2006](https://doi.org/10.1016/S0065-2601(06)38002-1));
  monitorar o progresso, d = 0,40 ([Harkin 2016](https://pubmed.ncbi.nlm.nih.gov/26479070/)); formação de hábito, 18 a
  254 dias, faltar uma vez não atrapalha ([Lally 2010](https://doi.org/10.1002/ejsp.674)); MCII/WOOP, g = 0,34
  ([meta-análise](https://pubmed.ncbi.nlm.nih.gov/34054628/)); procrastinação: aversão à tarefa, atraso, baixa
  autoeficácia, impulsividade ([Steel 2007](https://pubmed.ncbi.nlm.nih.gov/17201571/)). "Habit stacking" e
  time-blocking: sem ensaio controlado achado [A]. Não citar Ariely & Wertenbroch 2002 (o relatório o dá como
  [retratado em 09/2026](https://pubmed.ncbi.nlm.nih.gov/42684323/) — conferir).
- **Avisos:** o Claude só responde; para lembrar, [rotinas](https://code.claude.com/docs/en/routines) (nuvem; mínimo
  1 h; consomem cota; conector incluído escreve sem perguntar) ou [tarefas agendadas do Cowork](https://support.claude.com/en/articles/13854387-schedule-recurring-tasks-in-claude-cowork).
  Truque a testar: a tarefa cria um bloco na agenda e o celular avisa.

## Transversal — aprender código sendo vibe coder

- Estilos nativos ([doc](https://code.claude.com/docs/en/output-styles)): `/output-style learning` (pede que você
  escreva trechos nos pontos de decisão) e `explanatory`; gravam em `.claude\settings.local.json` (só na pasta). Custam
  instrução em toda requisição (o cache reduz) e respostas mais longas; trocar de estilo não invalida o cache.
- [learning-opportunities](https://github.com/DrCatHicks/learning-opportunities) (CC-BY-4.0; fixo ≈ 96 tokens): depois
  de trabalho de arquitetura, oferece um exercício de 10-15 min (prever, explicar de volta); só a skill, não a versão
  com gancho. `teach` (já instalada) monta um curso numa pasta própria.
- **Por quê:** no [ECR da Anthropic](https://www.anthropic.com/research/AI-assistance-coding-skills) (52 programadores),
  quem usou IA tirou 50% contra 67% num teste de habilidade (d = 0,74), sem ganho de tempo significativo; quem pediu
  explicação ou só fez perguntas conceituais foi melhor.

## Fontes

As citadas ao longo do texto (links em cada linha), mais: https://code.claude.com/docs/en/settings-reference
(`disableClaudeAiConnectors`), https://code.claude.com/docs/en/skills, https://code.claude.com/docs/en/tools-reference,
https://code.claude.com/docs/en/prompt-caching, https://support.claude.com/en/articles/9517075-what-are-projects,
https://github.com/anthropics/knowledge-work-plugins/tree/main/productivity, https://github.com/alirezarezvani/claude-skills,
https://github.com/SYSTRAN/faster-whisper, https://docs.ankiweb.net/templates/styling.html, https://code.visualstudio.com/docs/languages/markdown.
