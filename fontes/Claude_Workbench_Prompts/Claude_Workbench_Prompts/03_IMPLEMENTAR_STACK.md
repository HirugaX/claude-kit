# PROMPT — implantação local do stack aprovado

Leia o manifesto e a arquitetura produzidos por `01_MASTER_WORK.md`, além de `06_AUDITORIA_WORK_GITHUB.md`. Execute este prompt no Claude Code com acesso ao computador que será configurado. Meu pedido é instalar/configurar o necessário; decisões arquiteturais ainda não aprovadas devem ser apresentadas antes de aplicar.

## Preflight

Identifique computador A ou B, SO, shell, versão de Claude e paths reais. Audite `~/.claude` e os paths de configuração desta versão. Registre o estado antes de mudar. Não use os resultados do container Work como inventário do meu PC. Se não tiver manifesto aprovado, termine a seleção/proposta primeiro; não instale o Top 50 inteiro.

Examine `C:\CLAUDE` ou o path local equivalente se existir: os repositórios atuais dependem da skill pessoal `uso-do-claude`, que ainda não foi auditada pelo Work. Descubra como essa pasta é registrada, importada ou sincronizada. Não crie cópia concorrente dela.

## Aplicação

1. Calcule o diff de componentes presentes versus selecionados. Preserve versões válidas, configurações locais e overrides.
2. Apresente e registre o diff das mudanças relevantes. Faça backup seletivo antes de substituir; backups com credenciais permanecem locais e protegidos.
3. Instale primeiro o menor núcleo que cobre requisitos/spec, pesquisa, debugging e review, preservando workflows de projeto já existentes.
4. Configure um dono do estado/handoff. Se o mecanismo existente for suficiente, não adicione memória automática redundante.
5. Registre componentes por mecanismo nativo validado: nome, namespace, escopo, invocação, dependências. Não diga que uma pasta de skills virou disponível automaticamente.
6. Habilite hooks e MCPs somente no escopo escolhido, depois de ler seu código/configuração. Credenciais localmente; sem `skip permissions` amplo como solução para background.
7. Instale extensões de frontend, documentos e segurança conforme o manifesto; bibliotecas por linguagem apenas nos projetos compatíveis.
8. Compare browser CLI/skill com MCP em tarefa sintética. Preserve o Edge/Playwright já adotado pelo DESOSP e a sonda de capturas do DASH até demonstrar necessidade de mudança.
9. Faça health check e registre instalado/habilitado/testado separadamente.
10. Repita em B por bootstrap idempotente. Paridade lógica, com diferenças locais justificadas.

A configuração financeira desabilita plugins Ruflo e contém limpeza de `.claude-flow` no SessionStart. Investigue esse conflito antes de instalar/reativar qualquer harness dessa família.

## Health check mínimo

- Claude abre e reconhece projeto, skills e comandos reais.
- Skills escolhidas resolvem suas dependências; workflow manual não é acionado automaticamente.
- Skill contextual adequada é descoberta em tarefa compatível e não contamina tarefa sem relação.
- Hook recebe payload esperado, termina com timeout, gera saída pequena e não lê dados reais sem necessidade.
- MCP conecta com permissões mínimas; falha de credencial fica identificada como bloqueio, não como sucesso.
- Tarefa sintética passa pelo handoff e retorna estado recuperável.
- Reexecutar bootstrap não duplica plugins, agentes, regras ou hooks nem altera estado válido.
- Rollback/desativação funciona; A/B têm versões e capacidades comparadas.

Teste nova sessão/background apenas com protocolo `04_HANDOFF_PROTOCOL.md`. Uma sessão de teste, sem spawn recursivo, sem banco real, sem alteração de planilhas clínicas/RH e sem efeitos externos.

## Entrega

Atualize manifesto com versões/commits reais e evidência. Entregue scripts de bootstrap/dry-run/health-check apropriados aos SOs detectados, documentação dos paths e `COMMANDS_RESOLVED.md`. Não invente um instalador universal baseado num SO que não foi detectado.

Não considere concluído até os dois computadores serem testados. Se só A estiver acessível, conclua A e deixe B explicitamente pendente. Depois configure os projetos individualmente com os prompts `10`–`14`; o repo HC tem o prompt adicional `16`.
