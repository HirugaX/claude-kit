# Mermaid nos documentos que o Claude lê — reduz tokens? melhora o acerto? (06/10/2026)

- **A pergunta:** escrever processos e decisões como diagrama Mermaid (em vez de prosa, lista numerada ou tabela) no
  CLAUDE.md, no `ESTADO.md`, nas skills e nas regras reduz tokens e melhora o acerto do Claude?
- **A data:** 06/10/2026.
- **O projeto que pediu:** claude-kit (pedido do Ettore na janela do plano: "se tiver e for significativo, aplique;
  apenas nesse cenário").
- **Conferir de novo depois de:** 06/04/2027, ou quando sair estudo com modelos Claude comparando Mermaid e prosa.
- **Método:** artigos com medição, documentação da Anthropic e uma medição de tamanho numa regra real do kit. [A] =
  afirmação de autor sem medição independente; [I] = inferência; [não achado] = não encontrado.

## Conclusão em poucas linhas

1. **Tokens: não reduz.** Na regra real de roteamento (Q18 do plano), em caracteres: prosa 335 (≈ 84 tokens), lista
   347, tabela 390, Mermaid 445 a 542 (+33% a +62%). Os símbolos são 4,8% dos caracteres na prosa e 13,5% no Mermaid. Os
   "3 a 6 vezes menos tokens" que circulam não foram medidos [A], e os exemplos de quem afirma dão mais tokens.
2. **Acerto: sem evidência para o Claude.** FlowBench (EMNLP 2024 Findings; GPT-4o, GPT-4-Turbo, GPT-3.5-Turbo):
   fluxograma ganha +4 a +11 pontos no acerto do passo seguinte, mas o sucesso da sessão inteira fica entre −2,1 e +2,6
   pontos da prosa ("comparable"); os três formatos juntos foram melhores (só no GPT-4-Turbo). O formato muda o
   resultado em até 40% sem vencedor fixo (He et al. 2024; GraphOmni).
3. **Anthropic:** recomenda títulos e marcadores, lista numerada para passos em ordem e XML para conteúdo misto;
   orientação sobre diagramas [não achado]; 0 de 7 skills oficiais conferidas usam Mermaid.
4. **Pode ajudar [I]:** máquina de estados com laço e retomada, junto com uma linha de prosa por decisão. **Atrapalha:**
   regra plana, condições em "E" (cada uma vira um losango), passos lineares e grafo grande (Mermaid é lista de arestas;
   em "Talk like a Graph" a lista de pares deu 19,8% contra 53,8% do agrupado por nó, no PaLM).
5. **Para gente:** renderiza no GitHub e na prévia do VS Code; no chat da extensão do Claude Code aparece como código cru
   (issue 20529, "not planned"). Evidência em humanos antiga e mista.
6. **Decisão (plano de 06/10):** não aplicar no que o Claude lê; diagrama só para gente (estudo, guia). Reabrir se surgir
   máquina de estados com laço que lista e tabela não deem conta.

## Fontes (lidas em 06/10/2026)

- FlowBench: https://arxiv.org/abs/2406.14884
- TextFlow (Claude 3.5 Sonnet lendo Mermaid 80,0% × Graphviz 82,2% × PlantUML 70,2%; sem braço de prosa):
  https://arxiv.org/abs/2412.16420
- He et al. 2024, formato do prompt: https://arxiv.org/abs/2411.10541 · GraphOmni: https://arxiv.org/abs/2504.12764 ·
  Talk like a Graph: https://arxiv.org/abs/2310.04560 · especificações de algoritmo (2026): https://arxiv.org/abs/2607.03158
- PMo (Mermaid × BPMN, sem prosa): https://arxiv.org/abs/2507.11356 · arquivos de contexto em agentes (+20% de custo):
  https://arxiv.org/abs/2602.11988
- Anthropic: https://code.claude.com/docs/en/memory#write-effective-instructions ·
  https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices ·
  https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices ·
  https://code.claude.com/docs/en/output-styles
- Skills oficiais: https://github.com/anthropics/skills (docx, webapp-testing…)
- Praticantes [A]: https://dev.to/cleverhoods/claudemd-best-practices-mermaid-for-workflows-khb ·
  https://www.mindstudio.ai/blog/mermaid-diagrams-claude-code-skills-context-compression/ ·
  https://github.com/obra/superpowers/blob/main/skills/writing-skills/SKILL.md
- Renderização: https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams ·
  https://code.visualstudio.com/docs/languages/markdown · https://github.com/anthropics/claude-code/issues/20529
- Humanos: https://doi.org/10.1145/359605.359610 · https://doi.org/10.1109/52.35587 ·
  https://research.wu.ac.at/de/publications/making-sense-of-business-process-descriptions-an-experimental-com-3/
