---
name: recursos-do-projeto
description: Depois do /grill-me (ou de qualquer entrevista de planejamento) de um projeto NOVO ou de uma implementação nova num projeto que já existe, escolhe quais recursos entram, quando entram e quais ficam de fora — contexto (CLAUDE.md, .claude/rules, skills, ganchos, handoff), verificação determinística (testes, lint, navegador, acessibilidade, varredura de segredos e de dado sensível), MCPs e CLIs, interface, banco e dados, observabilidade — cada escolha ligada a uma resposta da entrevista, e escreve as regras do projeto. Use também quando perguntarem que ferramentas, MCPs, bibliotecas ou stack usar, o que instalar, ou como montar um projeto no Claude Code.
---

# Recursos do projeto — o que entra, quando, e o que fica de fora

Base: a pesquisa de 04/10/2026 (`C:\CLAUDE-PROJETOS\claude-kit\fontes\claude-efficiency-report.md`), conferida na documentação
oficial no mesmo dia (`C:\CLAUDE-PROJETOS\claude-kit\skills\uso-do-claude\reference.md` §2b). Os cartões de cada recurso estão em
[catalogo.md](catalogo.md). Modelo e esforço **não** se decidem aqui: são da skill `uso-do-claude`. Se a data
acima tiver mais de 60 dias, reconfira os fatos marcados como "da documentação" antes de afirmá-los.

## 1. O princípio

O melhor conjunto de recursos **não é o que instala mais**. É o que põe **o mínimo de informação permanente no
contexto**, torna **o máximo de verificações determinísticas** (um comando que responde sim ou não) e deixa as
ferramentas externas **sob demanda**. A medida certa não é token economizado, é:

> custo por tarefa **concluída corretamente** = tokens + espera + retrabalho + (chance × custo do erro)

Cortar 20% do contexto e provocar um erro que custa três janelas não é economia. E o erro mais provável depois
de ler uma pesquisa de ferramentas é instalar todas.

## 2. Quando usar

- **Projeto novo**, depois da entrevista (`/grill-me`) e antes do plano.
- **Implementação nova num projeto existente** que traz algo que o projeto não tinha: interface nova, fonte de
  dado nova, integração externa, outra linguagem, ou trabalho que vai rodar sem supervisão.
- Não use para mudança pequena dentro do que o projeto já sabe fazer: ela herda os recursos que existem.
- Chamada antes da entrevista, devolva só as perguntas da §4 que a entrevista ainda não cobriu, para entrarem
  na árvore de decisões dela.

## 3. O passo a passo

1. **Releia a entrevista.** Liste as decisões já tomadas que mudam a escolha de recursos (§4).
2. **Inventário — projeto existente.** Fato do ambiente é trabalho seu, nunca pergunta ao usuário: tamanho do
   `CLAUDE.md` (linhas), `.claude/rules`, skills e ganchos do projeto, quantos testes e quanto demoram,
   marcadores, lint, teste de navegador, plugins e MCPs ligados, tamanho do handoff e dos documentos lidos
   ao abrir, e o custo de abrir a janela (`python C:\CLAUDE-PROJETOS\claude-kit\skills\uso-do-claude\medir_uso.py --sessoes`,
   coluna `ctx0`). Repositório grande: subagente Explore (`model: haiku` para localizar, `sonnet` para
   resumir) — ele não carrega o `CLAUDE.md`.
3. **As perguntas que faltam.** Só as da §4 que mudam a escolha e que nem a entrevista nem o inventário
   responderam — numa rodada só, no formato do `grilling` (numeradas, com a resposta recomendada).
4. **O núcleo** (catálogo §1): vale para todo projeto. Em projeto existente, marque o que já existe e o que falta.
5. **Os condicionais** (catálogo §2): percorra a tabela de gatilhos; entra só o que uma resposta dispara.
6. **Os "não"** (catálogo §4): confira que nenhum entrou pela porta dos fundos.
7. **A ficha** (§5): no máximo **7 itens em AGORA**; o resto vai para QUANDO (com o gatilho) ou NÃO (com o motivo).
8. **As regras para escrever** (§6) e o modelo e esforço de cada fase (skill `uso-do-claude` §3 e §12).
9. **Mostre a ficha ao usuário antes de instalar ou escrever.** Instalar ferramenta e mudar a lei do projeto
   são ações dele aprovar; decisão técnica de rotina (qual regra de lint, qual pasta) é sua, em uma linha.

## 4. As perguntas que mudam a escolha

| # | Pergunta | O que a resposta liga ou desliga |
|---|---|---|
| 1 | Projeto novo ou implementação num existente? Que parte do sistema ela toca? | o inventário; reaproveitar antes de acrescentar |
| 2 | Tem interface? Web, desktop, terminal? Tela densa de trabalho? Vai para o papel? | navegador, acessibilidade, catálogo de componentes, revisão de tela |
| 3 | Onde roda: só na máquina, rede interna, internet? A máquina de uso tem internet? | CDN e fontes externas; observabilidade em nuvem; o que vendorizar |
| 4 | Um usuário ou vários escrevendo ao mesmo tempo? | SQLite × PostgreSQL |
| 5 | Que dado: relacional e transacional? Planilha como interface? Arquivos para analisar (CSV, XLSX, Parquet)? Quanto? | a árvore de dados (catálogo §3) |
| 6 | Dado pessoal ou de saúde? Pode sair da máquina? Há segredo (chave, token)? | varredura própria; Gitleaks; nenhum SaaS nem MCP de terceiro com o dado |
| 7 | O erro aparece na hora (na tela) ou fica escondido e é descoberto depois (dado gravado, identidade, número oficial)? | quanto de verificação determinística; o esforço (skill `uso-do-claude`) |
| 8 | Que linguagem e framework? O front tem build (React, Node) ou o servidor renderiza (Jinja2, Django)? | lint e tipos; a cadeia de interface |
| 9 | O Claude precisa ler algo de fora: PRs e issues, um design no Figma, uma API que muda depressa, erros de produção? | os MCPs e CLIs (catálogo §2.6) |
| 10 | Protótipo, uso interno diário ou produção com usuário de fora? Quem fica sabendo quando quebra? | observabilidade; segurança no CI |
| 11 | Como se trabalha: uma janela por fase, janelas em paralelo, sessão longa sem supervisão, outro agente (Codex, Cursor) no mesmo repositório? | ganchos, handoff, caixa de entrada, `AGENTS.md` |
| 12 | Que procedimento vai se repetir três vezes ou mais (abrir e fechar janela, rodar o pipeline, importar, criar migração, revisar tela)? | as skills do projeto |

## 5. A ficha — a saída

```
FICHA DE RECURSOS — <projeto ou implementação> — <data>
Base: a entrevista de <data> · o inventário (projeto existente)

AGORA (no máximo 7)
| recurso | por quê: a resposta que o pede | como saber que funcionou | custo |
QUANDO
| recurso | o gatilho que o faz entrar |
NÃO
| recurso | por quê não, neste projeto |
REGRAS PARA ESCREVER
- CLAUDE.md: <as linhas>
- .claude/rules/<domínio>.md (paths: …): <as regras>
- skills do projeto: <nome — quando roda>
- ganchos: <evento — o que faz>
MODELO E ESFORÇO POR FASE (skill uso-do-claude)
| fase | modelo · esforço | por quê | o sinal para subir |
DECISÕES DO USUÁRIO QUE FICARAM — cada uma escrita como pergunta, com a recomendação e o que muda
```

**Conferência da própria ficha, antes de mostrar:**

- cada AGORA aponta para uma resposta da entrevista ou um problema medido no inventário — gosto não conta;
- cada AGORA tem um "como saber que funcionou" que é um comando ou algo que se vê, nunca "melhora a qualidade";
- nada contraria a lei do projeto (sem internet → nada de CDN nem de SaaS; dado sensível → nada sai da máquina);
- não há duas ferramentas para o mesmo papel (dois frameworks de teste, dois bancos, dois sistemas de CSS);
- afirmação do fornecedor está marcada como tal (classe D no catálogo); número de estrelas não é qualidade.

## 6. Onde cada regra mora

| Informação | Onde |
|---|---|
| comandos (testar, rodar, lint), invariantes, "nunca X" e "sempre Y" | `CLAUDE.md`, **menos de 200 linhas** |
| regra que só vale ao mexer num tipo de arquivo (tela, migração, testes) | `.claude/rules/<domínio>.md` com `paths:` |
| procedimento de vários passos que se repete | skill do projeto (`.claude/skills/<nome>/SKILL.md`) |
| ritual que não pode ser esquecido (abrir janela, bloquear escrita em dado real) | gancho (`SessionStart`, `PreToolUse`) — controle, não lembrete |
| onde estamos, o que falta, o próximo prompt | handoff **curto**; o histórico em arquivo à parte, lido sob demanda |
| decisão com alternativas reais e consequência longa | registro de decisão curto (`docs/adr/`); nunca para detalhe de tela |
| preferência e correção recorrente do usuário | memória automática |
| explicação para gente | `README` |

🛑 **Estado mutável nunca no `CLAUDE.md`**: ele é lido em toda chamada e envelhece sem ninguém ver (no app DESOSP,
o parágrafo de estado dizia por dias uma "próxima fase" que já não era). E **uma regra mora num lugar só**:
duas cópias divergem no dia em que uma delas muda.

## 7. Exemplo aplicado

O app DESOSP (FastAPI + Jinja2, notebook sem internet, dado de saúde, um usuário) passou por esta skill em
04/10: `C:\CLAUDE-PROJETOS\desosp-app\docs\RECURSOS_CLAUDE_DESOSP.md`. Ali estão o inventário com os números, o que entrou
(o gancho de abertura, a revisão de tela, a regra por caminho, o navegador de verdade na suíte, o handoff
curto), e o que ficou de fora e por quê (Sentry, Figma, shadcn, GitHub MCP, Context7, Postgres, DuckDB).
