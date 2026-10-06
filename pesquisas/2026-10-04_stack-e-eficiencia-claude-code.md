# Stack e eficiência para desenvolver com o Claude Code

- **Pergunta:** qual stack usar para desenvolver aplicações com o Claude Code — Skills, MCPs, bibliotecas,
  ferramentas, UI/UX, bancos, planilhas, testes, observabilidade e segurança — com a melhor qualidade pelo
  menor uso de tokens?
- **Data:** 04/10/2026 (corte declarado no texto)
- **Projeto que pediu:** geral (`C:\CLAUDE`); alimentou a escolha de recursos do DESOSP_APP.
- **O documento:** `C:\CLAUDE\fontes\claude-efficiency-report.md` (548 linhas). Seções: resumo executivo;
  arquitetura de contexto e modelos; subagents; fichas das ferramentas; UI, browser (CLI × MCP), banco e
  planilhas; economia de tokens; stack enxuta e roadmap; ranking final.
- **Fontes:** o documento **não tem URLs** — só marcadores de busca de outra ferramenta (`citeturn…`), que
  não se conferem à mão. A conferência das afirmações dele está em
  `2026-10-04_verificacao-recursos-claude-code.md` e no `reference.md` §2b da skill `uso-do-claude`.
- **Conclusão:** "A melhor stack para Claude Code não é a que instala mais MCPs. É a que coloca o mínimo
  possível de informação permanente no contexto, torna o máximo possível de verificações determinísticas e
  oferece ferramentas externas sob demanda." Atenção: ele diz que o Explore usa Haiku e põe o Sonnet como
  padrão — a verificação de 04/10 mostrou que o Explore herda o modelo da sessão e que o padrão no Max é o
  Opus 5.5.
- **Conferir de novo depois de:** 04/12/2026 (versões, métricas de GitHub, modelos e preços; a parte
  "pouco contexto, muita verificação" é estável).
- **Como foi feita:** pesquisa profunda feita fora do Claude Code e salva em `C:\CLAUDE\fontes\`. A
  biblioteca guarda só este cabeçalho; o texto fica no documento.
