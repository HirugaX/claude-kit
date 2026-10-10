---
name: recursos-do-projeto
description: "Depois do /grill-me de projeto ou implementação nova, ou ao perguntarem que ferramenta usar: escolhe testes, navegador, ganchos, MCPs e stack, e o que fica de fora."
---

# Recursos do projeto — o que entra, quando, e o que fica de fora

Base: a pesquisa de 04/10/2026 (`C:\CLAUDE-PROJETOS\claude-kit\fontes\claude-efficiency-report.md`), conferida na
documentação no mesmo dia (`reference.md` da `uso-do-claude`, §2b). Os cartões de cada recurso, com a evidência, estão
no [catalogo.md](catalogo.md): leia a seção que o passo pede, não o arquivo inteiro. Modelo e esforço não se decidem
aqui (`modelo-e-esforco`). Com esta data a mais de 60 dias, reconfira os fatos "da documentação" antes de afirmá-los.

## O princípio

O melhor conjunto **não é o que instala mais**: é o que põe **o mínimo de informação permanente no contexto**, torna **o
máximo de verificações determinísticas** (um comando que responde sim ou não) e deixa as ferramentas externas **sob
demanda**. A medida é o custo por tarefa **concluída corretamente** (tokens + espera + retrabalho + chance × custo do
erro). O erro mais provável depois de ler uma pesquisa de ferramentas é instalar todas.

**Quando:** projeto novo, depois da entrevista e antes do plano; implementação nova que traz o que o projeto não tinha
(interface, fonte de dado, integração externa, outra linguagem, trabalho sem supervisão). Mudança pequena dentro do que
o projeto já sabe fazer herda os recursos que existem. Chamada antes da entrevista: devolva só as perguntas da tabela
abaixo que a entrevista ainda não cobriu.

## O passo a passo

1. **Releia a entrevista.** Liste as decisões já tomadas que mudam a escolha de recursos.
2. **Inventário (projeto existente).** Fato do ambiente é trabalho seu, nunca pergunta: linhas do `CLAUDE.md`,
   `.claude/rules`, skills, ganchos e `enabledPlugins` do projeto, testes (quantos, quanto demoram), lint, navegador,
   MCPs ligados, tamanho do estado e dos documentos lidos ao abrir, e o custo de abrir a janela
   (`python C:\CLAUDE-PROJETOS\claude-kit\scripts\medir_uso.py --sessoes`, coluna `ctx0`). Repositório grande:
   subagente explorador (skill `orquestrar`).
3. **Descoberta (opcional).** Para uma segunda opinião sobre o que o código pede, o `claude-code-setup` oficial
   **sem instalar**: `claude --plugin-dir <clone do claude-plugins-official>\plugins\claude-code-setup`, só leitura.
   No F3b (10/10) custou US$ 0,12 e não mexeu em arquivo. Ele pende para web/JS e pode sugerir Context7, Playwright
   MCP e GitHub MCP, recusados com motivo em 04/10: o que ele sugerir passa pelos passos 5 a 7 como qualquer outro
   candidato.
4. **As perguntas que faltam:** só as da tabela que mudam a escolha e que nem a entrevista nem o inventário
   responderam, numa rodada só, no formato do `grilling` (numeradas, com a resposta recomendada).
5. **O núcleo** (catálogo §1): vale para todo projeto; em projeto existente, marque o que já existe e o que falta.
6. **Os condicionais** (catálogo §2, a tabela de gatilhos): entra só o que uma resposta dispara. **Os "não"**
   (catálogo §4): confira que nenhum entrou pela porta dos fundos.
7. **A ficha** (abaixo): no máximo **7 itens em AGORA**; o resto vai para QUANDO (com o gatilho) ou NÃO (com o motivo).
8. **Mostre a ficha antes de instalar ou escrever.** Instalar ferramenta e mudar a lei do projeto são do usuário
   aprovar; decisão técnica de rotina (qual regra de lint, qual pasta) é sua, em uma linha.

| # | A pergunta que muda a escolha | O que a resposta liga ou desliga |
|---|---|---|
| 1 | Projeto novo ou implementação num existente? Que parte do sistema ela toca? | o inventário; reaproveitar antes de acrescentar |
| 2 | Tem interface? Web, desktop, terminal? Tela densa? Vai para o papel? | navegador, acessibilidade, revisão de tela |
| 3 | Onde roda: só na máquina, rede interna, internet? A máquina tem internet? | CDN e fontes externas; o que vendorizar |
| 4 | Um usuário ou vários escrevendo ao mesmo tempo? | SQLite × PostgreSQL |
| 5 | Que dado: relacional? planilha como interface? arquivos para analisar? quanto? | a árvore de dados (catálogo §3) |
| 6 | Dado pessoal ou de saúde? Pode sair da máquina? Há segredo? | varredura própria; Gitleaks; nenhum SaaS nem MCP de terceiro com o dado (ADR-0001) |
| 7 | O erro aparece na hora ou fica escondido e é descoberto depois? | quanto de verificação determinística; o esforço |
| 8 | Que linguagem e framework? O front tem build ou o servidor renderiza? | lint e tipos; a cadeia de interface |
| 9 | O Claude precisa ler algo de fora (PRs, Figma, API que muda depressa, erros de produção)? | os MCPs e CLIs (catálogo §2.6) |
| 10 | Protótipo, uso interno diário ou produção com usuário de fora? | observabilidade; segurança no CI |
| 11 | Como se trabalha: janelas por fase, em paralelo, sessão longa sem supervisão? | ganchos, `ESTADO.md`, fila, caixa (`orquestrar`) |
| 12 | Que procedimento vai se repetir 3 vezes ou mais? | as skills do projeto |

## A ficha — a saída

```
FICHA DE RECURSOS — <projeto ou implementação> — <data>
Base: a entrevista de <data> · o inventário (projeto existente)
AGORA (no máximo 7)  | recurso | por quê: a resposta que o pede | como saber que funcionou | custo |
QUANDO               | recurso | o gatilho que o faz entrar |
NÃO                  | recurso | por quê não, neste projeto |
REGRAS PARA ESCREVER — CLAUDE.md (com "Skills deste projeto", ≤ 10 linhas); .claude/rules/<domínio>.md (paths:);
  .claude/settings.json (enabledPlugins: instalar_kit.py --trecho <tipo>; deny das pastas de dado); skills; ganchos
MODELO E ESFORÇO POR FASE | fase | modelo · esforço | por quê | o sinal para subir |
DECISÕES DO USUÁRIO QUE FICARAM — cada uma como pergunta, com a recomendação e o que muda
```

Antes de mostrar, confira: cada AGORA aponta para uma resposta da entrevista ou um problema medido — gosto não conta;
cada AGORA tem um "como saber" que é um comando ou algo que se vê; nada contraria a lei do projeto (sem internet → nada
de CDN nem SaaS; dado sensível → nada sai da máquina); não há duas ferramentas para o mesmo papel; afirmação de
fornecedor vem marcada (classe D no catálogo).

## Onde cada regra mora

| informação | onde |
|---|---|
| comandos, invariantes, "nunca X" e "sempre Y" | `CLAUDE.md`, menos de 200 linhas, sem estado |
| regra que só vale ao mexer num tipo de arquivo | `.claude/rules/<domínio>.md` com `paths:` |
| procedimento de vários passos que se repete | skill do projeto (`.claude/skills/<nome>/SKILL.md`) |
| ritual que não pode ser esquecido; bloquear escrita em dado real | gancho — controle, não lembrete |
| onde estamos, o próximo prompt, as perguntas | `docs\ESTADO.md`, `docs\PROXIMO.md`, `docs\PERGUNTAS.md` (`fechar-janela`) |
| decisão difícil de desfazer, com alternativa real | `docs\adr\` |
| preferência e correção recorrente do usuário | memória automática |

Uma regra mora num lugar só: duas cópias divergem no dia em que uma delas muda. Exemplo aplicado: o app DESOSP passou
por esta skill em 04/10 (`C:\CLAUDE-PROJETOS\desosp-app\docs\RECURSOS_CLAUDE_DESOSP.md`): o que entrou e o que ficou de
fora (Sentry, Figma, shadcn, GitHub MCP, Context7, Postgres, DuckDB), e por quê.
