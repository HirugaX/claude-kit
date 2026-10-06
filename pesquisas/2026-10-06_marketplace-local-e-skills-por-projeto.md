# Marketplace local, skills por projeto, ultracode e celular — o que a documentação confirma (06/10/2026)

- **A pergunta:** o kit pode virar um marketplace local de plugins, com grupos de skills ligados por projeto? Como se
  desliga, por projeto, skill de usuário, skill sincronizada do claude.ai e conector? O que muda com o "Ultracode
  keyword trigger" desligado? Uma sessão do Remote Control consegue lançar `claude --bg` e receber resposta?
- **A data:** 06/10/2026 (Claude Code 2.1.290 no PATH; extensão do VS Code 2.1.289).
- **O projeto que pediu:** claude-kit (rodada 3 do fluxo; `decisoes\2026-10-06_plano-fluxo.md`, Q17 e F1b).
- **Conferir de novo depois de:** 06/11/2026 (plugins, agent view e mensagens entre sessões mudam a cada versão).
- **Método:** documentação oficial lida por subagente, complementando `2026-10-05_sessoes-memoria-plugins-claude-code.md`
  e `2026-10-04_verificacao-recursos-claude-code.md`; conferência local do `~\.claude\settings.json` e dos transcritos
  da sessão. [não achado] = a documentação não diz.

## Conclusão em poucas linhas

1. **Uma pasta local serve de marketplace:** `claude plugin marketplace add C:\CLAUDE-PROJETOS\claude-kit` (também
   `/plugin marketplace add`; formas `.\`, `..\` e `C:\` valem no Windows). Plugin com caminho relativo nesse
   marketplace **carrega no lugar**: a edição vale na sessão seguinte ou com `/reload-plugins`, sem subir versão. Outras
   fontes são copiadas para `~\.claude\plugins\cache\<marketplace>\<plugin>\<versão>\` e só mudam com versão nova +
   `plugin update` (`marketplace update` sozinho não atualiza o instalado). `--plugin-dir <pasta>` carrega um plugin só
   naquela sessão, sem instalar.
2. **Skill de plugin** atende por `/plugin:skill` e pelo nome curto quando não há outra com o mesmo nome. Nome e
   descrição de cada skill entram em toda sessão onde o plugin está ligado (descrições cortadas pelo orçamento de 1%).
3. **`enabledPlugins`** (`"<plugin>@<marketplace>"`): vale a fonte de maior precedência (usuário < projeto < local), nos
   dois sentidos. Plugin de caminho relativo ligado no projeto dispensa registro de instalação.
4. **Skill de usuário** (`~\.claude\skills`) se desliga por projeto com `skillOverrides` (`on`, `name-only`,
   `user-invocable-only`, `off`; o `/skills` grava em `.claude\settings.local.json`) — não vale para skill de plugin.
   `permissions.deny` com `Skill(nome)` existe; se a descrição continua na lista com ele: [não achado].
5. **Claude.ai:** `syncClaudeAiSkills: false` (por máquina) para a sincronização e manda as já sincronizadas para
   `~\.claude\skills\.trash\` (`pdf` e `xlsx` sempre vêm); uma a uma, `deny` com `Skill(anthropic-skills:<nome>)`.
   `disableClaudeAiConnectors: true` em qualquer settings desliga os conectores (o projeto desliga, não religa); `/mcp`
   liga e desliga cada um; não fala de skills.
6. **Ultracode:** a chave é `workflowKeywordTriggerEnabled` (gravada pelo `/config` em `~\.claude\settings.json:74`;
   vale no terminal e na extensão, que leem o mesmo arquivo). Em `false`, só a palavra deixa de disparar; continuam
   `/effort ultracode`, `claude --effort ultracode`, `/deep-research`, workflows salvos e o pedido explícito. Tudo some
   só com `disableWorkflows` ou `CLAUDE_CODE_DISABLE_WORKFLOWS=1`.
7. **O atalho `sonnet` no subagente abre o Sonnet 5.5:** os 4 subagentes desta sessão, chamados com `model: sonnet`,
   rodaram em `claude-sonnet-5-5` (transcritos em `~\.claude\projects\c--CLAUDE-PROJETOS\db454f8f-…\subagents\`). A
   armadilha do Sonnet 5 é `/model sonnet` e `--model sonnet` na sessão principal.
8. **Celular:** `claude --bg` é comando de shell (prévia; sem terminal e em pasta não confiada sai com "Workspace not
   trusted"). Rodá-lo de dentro de uma sessão do Remote Control: [não achado]. Sessões `--bg` aparecem no `/list-agents`
   quando abrem caixa de entrada; mensagens entre sessões no Windows vão por named pipe (2.1.234+), nunca pelos
   servidores; mensagem de outra sessão não aprova nada; em sessão do VS Code ou do Desktop, a mensagem que pede diálogo
   expira (5 min). `/reload-plugins` não roda pelo Remote Control.

## Fontes (lidas em 06/10/2026)

- https://code.claude.com/docs/en/plugins/install (#add-a-marketplace, #update-plugins-now)
- https://code.claude.com/docs/en/plugins/loading (#in-place-and-copied-plugins, #find-where-a-plugin-is-enabled,
  #enabled-in-project-settings-but-not-installed)
- https://code.claude.com/docs/en/plugins/cli-reference (#plugin-marketplace-add, #reload-plugins,
  #flags-that-load-a-plugin-for-one-session)
- https://code.claude.com/docs/en/plugins/create-marketplace · https://code.claude.com/docs/en/plugins/host-marketplace
  (#keep-users-up-to-date) · https://code.claude.com/docs/en/plugins/measure
- https://code.claude.com/docs/en/skills (#override-skill-visibility-from-settings) · https://code.claude.com/docs/en/permissions
- https://code.claude.com/docs/en/settings-reference · https://code.claude.com/docs/en/settings (#use-the-config-menu)
- https://code.claude.com/docs/en/mcp (#disable-claude-ai-connectors)
- https://code.claude.com/docs/en/workflows (#dismiss-or-turn-off-the-keyword, #turn-workflows-off, #where-the-keyword-works)
- https://code.claude.com/docs/en/agent-view (#from-your-shell) · https://code.claude.com/docs/en/remote-control ·
  https://code.claude.com/docs/en/cross-session-messaging
- https://code.claude.com/docs/en/changelog (2.1.289: `plugin list/eval/update` mostrava cópia velha de plugin de
  marketplace em pasta local)
