# Claude Workbench — comece aqui

Preparado para Ettore em 05/10/2026. Este pacote contém prompts de execução e propostas; não é evidência de instalação, auditoria local ou configuração concluída.

**Já estamos no Work e o GitHub foi verificado.** Leia `06_AUDITORIA_WORK_GITHUB.md` para os achados reais e use `07_AUDITORIA_LOCAL.md` no Claude Code de cada computador. Não precisa reiniciar a pesquisa no Work nem reexplicar os projetos. Aqui não há Claude Code nem acesso às configurações locais de A/B; por isso nenhuma instalação nesses computadores foi concluída.

## Ordem de uso

1. Abra um trabalho de arquitetura no ChatGPT Work, disponibilize esta pasta e o relatório de pesquisa indicado abaixo. Inicie com `01_MASTER_WORK.md`.
2. O primeiro resultado será inventário, seleção e arquitetura. Aprove o plano antes da instalação/configuração. `02_STACK_CANDIDATO.md` é uma lista de avaliação, não uma lista para instalar cegamente.
3. Após aprovar, use `03_IMPLEMENTAR_STACK.md`. Execute a parte local em Claude Code ou em outro ambiente com acesso real às pastas dos computadores A e B. O Work não ganha acesso ao seu notebook só porque conhece um caminho Windows.
4. Concluído o health check dos dois computadores, use somente o prompt do projeto que será configurado: arquivos `10` a `14`. Disponibilize o repositório/workbook correspondente.
5. Consulte `05_COMMAND_PLAYBOOK.md` para o uso diário. Para projetos novos, use `15_NOVO_PROJETO.md`.

Há também `16_HOME_CARE_EXCEL.md`, porque o GitHub revelou esse quarto repositório com código, distinto do censo/kernel. Folha/RH e fila Apps Script ainda precisam de repo/path.

## Pedido pronto para usar no Claude Code local

Salve a pasta extraída em um diretório acessível ao Claude Code e diga:

> Leia `Claude_Workbench_Prompts/07_AUDITORIA_LOCAL.md` e os arquivos a que ele se refere. Audite este computador e os projetos acessíveis, apresente o plano de instalação/configuração necessário e, após a aprovação arquitetural, execute-o e faça o health check. Use os achados do GitHub já registrados; não me peça para remontar o inventário à mão.

Use o path real se a pasta tiver outro nome/local. Depois do stack global, em cada repo diga apenas “Leia o prompt de configuração deste projeto” apontando para o arquivo `10`, `11`, `12`, `13`, `14` ou `16` pertinente. Não é necessário colar todos eles numa sessão.

Os prompts por projeto solicitam auditoria e proposta antes de aplicar mudanças. Não precisa aprovar microdecisões reversíveis depois de aprovar o plano.

## Fontes de entrada

Relatório localizado e lido durante a preparação deste pacote:

**“Claude Code em 2026: Skills, Plugins, Subagents, Hooks, MCPs e os cinquenta projetos mais relevantes no GitHub”**, de 05/10/2026.

Ele serve para descobrir candidatos. Scores, stars e recomendações do relatório não substituem leitura do código, documentação atual e teste local. Sua recomendação de não instalar vários harnesses simultaneamente foi preservada.

Contexto de projetos informado pelo usuário:

| Projeto | Contexto confirmado | Ainda precisa ser inspecionado |
|---|---|---|
| Financeiro | PDFs de extratos, normalização, análises; precisa de frontend | Stack, parser, banco, arquitetura e testes |
| Folha/RH | Google Apps Script | Fórmulas/regras, Sheets, triggers, implantação |
| Fila/acolhimento | Google Apps Script | Estados, prioridades, concorrência, Sheets |
| Censo e pendências | Aplicativo hospitalar | Código, stack, regras efetivamente implementadas |
| Censo Excel | Workbook hospitalar | Arquivo atual, fórmulas, queries, macros, dependências |

## Como reduzir as intervenções humanas

O fluxo pretendido é: você explica o objetivo; Claude detecta projeto e ferramentas, executa a rotina aprovada, registra estado e prepara continuidade. Comandos explícitos ficam para mudar o modo de trabalho ou autorizar efeitos relevantes.

Equivalência entre computadores significa mesma configuração declarativa e capacidades compatíveis, não sincronização de caches, credenciais, transcripts e paths absolutos.

Instalar o stack selecionado nos dois computadores não significa habilitar todos os MCPs/hooks em todos os projetos. O catálogo pode estar disponível; componentes devem ser ativados conforme necessidade e compatibilidade.

## O que disponibilizar uma vez

- SO e shell de cada computador, indicando Windows nativo versus WSL quando aplicável.
- Acesso à configuração Claude de A/B ou inventários locais sanitizados.
- Repositórios ou paths dos cinco projetos; workbook Excel vigente.
- Relatório da pesquisa. Se não puder ser acessado, o arquiteto deve declarar a lacuna.
- Método de autenticação/provedor do Claude, sem enviar chaves ou senhas.

Não envie a pasta de configuração completa sem revisar: ela pode conter credenciais e dados privados. O inventário deve extrair metadados relevantes localmente e ocultar valores sensíveis.

## Limites e escolha de ambiente/modelo

Work é adequado para manter e revisar estes arquivos e sintetizar a arquitetura. A instalação e os testes dos computadores exigem acesso ao ambiente correspondente. Use um modelo com boa capacidade de raciocínio para seleção, conflitos e decisões de arquitetura; auditorias mecânicas e bootstrap não precisam automaticamente do modelo mais caro.

Não há garantia de que abrir sessões novas ou usar subagents reduza a cobrança: eles também repetem instruções e consomem tokens. Meça o custo e o tempo de tarefas comparáveis; diferencie janela de contexto, cache, faturamento de API e limites da assinatura.

## Documentação a revalidar durante a execução

- [Skills](https://code.claude.com/docs/en/skills)
- [Subagents](https://code.claude.com/docs/en/sub-agents)
- [Memória e regras](https://code.claude.com/docs/en/memory)
- [Agent View e background](https://code.claude.com/docs/en/agent-view)
- [Cross-session messaging](https://code.claude.com/docs/en/cross-session-messaging)
- [Hooks](https://code.claude.com/docs/en/hooks)
- [Plugins oficiais](https://github.com/anthropics/claude-plugins-official)

Recursos documentados podem exigir versões, plataformas e provedores específicos. A documentação consultada confirma a distinção entre nova sessão background e retomada de conversa; suporte no seu computador só será confirmado pelos testes locais.
