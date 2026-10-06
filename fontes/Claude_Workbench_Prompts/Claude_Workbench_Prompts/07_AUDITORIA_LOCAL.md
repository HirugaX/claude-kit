# PROMPT — execute uma vez em cada computador

Leia os arquivos deste pacote. Você está no Claude Code local: audite este computador e a configuração existente em somente leitura antes de instalar/configurar.

Não dependa do usuário para listar skills ou reconstruir o contexto. Identifique SO/shell/Windows nativo ou WSL, versão/método de instalação Claude, Git, gh, Python, Node e ferramentas pertinentes. Encontre diretórios de configuração efetivos e os projetos acessíveis, respeitando o escopo das pastas autorizadas; evite varredura indiscriminada de todo o disco.

Leia `~/.claude/CLAUDE.md`, rules, skills, agents, plugins, hooks, MCPs, settings/overrides e imports. Inspecione também `C:\CLAUDE` ou equivalente se existir: procure `uso-do-claude` e entenda seu registro/sincronismo. Não execute hooks para auditar; alguns existentes têm efeitos de deleção/instalação.

Para cada skill leia frontmatter e corpo necessário para dependências/efeitos. Diferencie global, projeto e plugin; always-on, model-invoked, user-invoked, agents, hooks e MCPs. Registre nomes/paths/versões/metadados; nunca valores de secrets, contas privadas, dados clínicos, salários ou transações reais.

Leia `06_AUDITORIA_WORK_GITHUB.md` e compare com cópias locais. Não assuma que main está sincronizado. Registre branch/commit/status por projeto, sem apagar ou stash automático de mudanças.

Produza inventário sanitizado e arquitetura/diff conforme `01_MASTER_WORK.md`. Após aprovação do plano, continue autonomamente com `03_IMPLEMENTAR_STACK.md`: instalar o stack selecionado, registrar descoberta/gatilhos, testar e fornecer os arquivos de bootstrap/health-check. O pedido de instalar o necessário não autoriza alterar regras de negócio ou implantar projetos como efeito colateral.

Meu objetivo é executar este prompt uma vez em A e uma vez em B; depois obter configuração equivalente. Se um computador não estiver acessível, conclua o que é local e deixe o outro explicitamente pendente.
