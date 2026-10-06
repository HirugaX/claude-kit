# O espaço de pesquisa clínica com o Claude Code — ferramentas, OpenEvidence, memória e pasta (06/10/2026)

- **A pergunta:** como montar `C:\CLAUDE-PROJETOS\pesquisa\` para o Ettore (médico; hoje pesquisa no OpenEvidence)
  guardar a memória das pesquisas, acessar mais artigos, formular perguntas melhores e gastar poucos tokens — sem
  nenhum dado de paciente?
- **A data:** 06/10/2026 (GETs públicos medidos nesse dia: PubMed, Europe PMC, OpenAlex, Crossref, Unpaywall).
- **O projeto que pediu:** claude-kit → grill próprio do espaço de pesquisa (Q11 de `decisoes\2026-10-06_entrevista-fluxo.md`).
- **Conferir de novo depois de:** 05/12/2026 (K-Dense muda rápido); o resto em 06/01/2027.
- **Método:** clone do K-Dense lido (commit `92ace75`, 177 skills; nenhum código de terceiro rodado); termos do
  OpenEvidence lidos no texto da página. [A] = afirmação do autor sem medição; [I] = inferência.

## Conclusão em poucas linhas

1. **Do K-Dense, só 2 skills, e só dentro de `pesquisa\`:** `paper-lookup` (18 APIs abertas: PubMed, PMC, Europe
   PMC, OpenAlex, Crossref, Unpaywall, CORE…; Python stdlib + `curl`; grátis) e `scientific-critical-thinking`
   (GRADE por desfecho, RoB 2, ROBINS-I, AMSTAR 2; sem rede). As 177 juntas pesariam ~17 mil tokens de lista.
   Nenhuma faz meta-análise; GRADE é checklist, não cálculo.
2. **OpenEvidence não tem API pública**, e os termos proíbem automação, "inclusive assistentes de IA", para extrair
   conteúdo. Fluxo: o Ettore pergunta no site e cola a pergunta e as referências; o Claude confere cada referência no
   PubMed e guarda a nota. A prosa do OpenEvidence fica local e **fora do Git**.
3. **Memória mínima = Markdown:** uma nota por pergunta + `INDICE.md` + `REGISTRO.md` + `referencias.csv` (o padrão
   do gist de Karpathy: fontes brutas, wiki, esquema no CLAUDE.md; funciona até ~100 fontes sem embeddings [A]).
   Obsidian só como visualizador; Zotero depois; `claude-mem` não.
4. **Pergunta melhor:** o `grilling` (já instalado) é o motor; falta o conteúdo clínico — uma skill própria
   `pergunta-clinica` (~1 KB): tipo da pergunta → PICO(T) → desfechos críticos × importantes → FINER → "o que mudaria
   na conduta?" → conferir o `INDICE.md` → string de busca.

## K-Dense avaliado (tamanho do `SKILL.md`)

| skill | o que faz / APIs | dependências · chave · custo | veredito |
|---|---|---|---|
| `paper-lookup` (26 KB) | 18 APIs; paginação; texto completo (JATS) | stdlib + `curl`; chaves opcionais; Unpaywall exige e-mail real (422 sem) | **instalar** |
| `scientific-critical-thinking` (13 KB) | GRADE, RoB 2, ROBINS-I, AMSTAR 2 | nada (figuras via OpenRouter: ignorar) | **instalar** |
| `citation-management` (17 KB) | PubMed/OpenAlex/Crossref → BibTeX; valida DOI; raspa o Google Scholar (evitar) | `requests`; o scanner do próprio K-Dense marca CRITICAL | depois (BibTeX/Zotero) |
| `literature-review` (13 KB) | revisão sistemática/escopo, PRISMA | `requests`; PDF pede pandoc + XeLaTeX; `parallel-cli` e OpenRouter **pagos** (opcionais) | depois (revisão formal) |
| `hypothesis-generation` (17 KB) | PICO/PECO, FINER | offline | não: pesada; o exemplo dela atribui um artigo a autores errados (risco de citação) |
| `research-lookup` | pacote de referências via Parallel/Perplexity | **pagos**; manda a pergunta a terceiros | **não** |
| `pyzotero` | biblioteca Zotero local (Zotero 7+) | `pyzotero` | só se usar Zotero |
| `scientific-writing`, `peer-review`, `statistical-*`, `clinical-decision-support`, `clinical-reports` | manuscrito, parecer, estatística, artefatos clínicos | vários | não (sem manuscrito, sem dado) |

No Windows: usar `python` (o `python3` é o atalho da Loja) e rodar `curl` no Bash. Instalar só no projeto, a partir do
clone revisado: `npx skills add <clone> --skill paper-lookup --skill scientific-critical-thinking -a claude-code --copy -y`
(escopo padrão é o projeto, `.claude\skills`). Apagar o bloco "cite o nosso paper" de cada `SKILL.md`.

## Acesso a artigos

| fonte | caminho | grátis · chave · limite |
|---|---|---|
| PubMed | `paper-lookup` (E-utilities); conector oficial PubMed (`claude mcp add -s project --transport http pubmed https://pubmed.mcp.claude.com/mcp`, sem login) | 3 req/s; 10 com chave grátis |
| Europe PMC | `paper-lookup` | sem chave; texto completo aberto (num exemplo, 150 de 212 artigos) |
| OpenAlex | `paper-lookup`; `pyalex` | sem chave funciona; busca custa US$ 0,001 do orçamento grátis [A]; DOI grátis |
| Crossref | `paper-lookup` | sem chave; o `mailto` expõe o e-mail; traz retratação (`updated-by`) |
| Unpaywall | DOI → PDF aberto | e-mail real obrigatório |
| Semantic Scholar | dispensável | sem chave deu 429 |
| Zotero | só se já usar | leitura local sem chave; `zotero-mcp` (MIT) existe |

A skill basta; o conector só acrescenta busca por citação. Se usar o conector, escopo de projeto: ligado no claude.ai,
ele apareceria em todos os projetos. Artigo fechado: baixar pelo acesso institucional para `fontes\texto-completo\`.

## OpenEvidence (termos de 17/09/2026)

- Sem API pública (`/developer`, `/api`, `/docs` dão 404); integração só institucional (Epic) [A].
- Termos §3: licença "solely for your professional use"; pode baixar artigos individuais para ler. AUP §12: proíbe
  "automated software… (including AI assistants…) to scrape, extract, or aggregate content" e acesso por agente fora de
  navegador comum; AUP §7: conteúdo de terceiros só para cuidado clínico, pesquisa interna ou educação.
- [I] Nota pessoal de pesquisa interna cabe; arquivar respostas em massa, publicar (inclusive no GitHub) ou automatizar
  (Playwright, Claude in Chrome) não. Guardar: a pergunta, os identificadores das referências e a síntese própria.
- **Fluxo:** colar pergunta + referências em `fontes\openevidence\` → subagente `haiku`/`sonnet` casa cada referência
  (PMID, ou ECitMatch por revista|ano|volume|página|autor), confere retratação (`pubtype` no PubMed/Europe PMC;
  `updated-by` no Crossref), puxa o resumo e marca cada afirmação: sustentada, parcial, não sustentada, não
  verificável → o Opus avalia 2 a 3 estudos-chave e grava a nota.

## A nota de cada pergunta

PICO (Richardson 1995), data, bases e string da busca, tabela (PMID, desenho, N, efeito e IC, risco de viés, "lido:
resumo ou texto"), certeza GRADE por desfecho (Guyatt 2008), nível OCEBM só como etiqueta, "revisar depois de".
"Living review": guardar a string e a data e repetir com `mindate`, ou alerta do PubMed.

## A pasta proposta

```
pesquisa\
├─ CLAUDE.md       < 60 linhas: sem dado de paciente; ordem de trabalho; verificação; usar `python`
├─ INDICE.md       id | pergunta | status | certeza | revisar depois de
├─ REGISTRO.md     só acrescenta: ## [data] busca | verifiquei | revisei | id
├─ .mcp.json       opcional: conector PubMed, só aqui
├─ .claude\        settings.json (permissões, gancho) · skills\ (as 2 do K-Dense + pergunta-clinica)
├─ perguntas\      uma nota por pergunta
├─ referencias\    referencias.csv: pmid, doi, 1º autor, ano, tipo, retratado?, verificado em, lido
├─ fontes\         FORA DO GIT: openevidence\ · texto-completo\ · brutos\ (JSON, nunca no contexto)
└─ modelos\        pergunta.md: id, tipo, status, PICO, busca, certeza, revisar_depois_de
```

## Tokens (medido numa busca)

10 PMIDs: o JSON do `esummary` tem 24 KB (~6 mil tokens) e vira uma tabela de 7 campos de 2 KB (~0,5 mil); 10 resumos,
42 KB (~10 mil); um ECR em texto completo, ~10 mil tokens. Regras: `INDICE.md` antes de buscar; o bruto vai para
`fontes\brutos\` e só a tabela entra no contexto; resumo primeiro, texto completo só de estudo-chave e em subagente;
`/clear` por pergunta; conferência com `haiku`/`sonnet`, tabela com Sonnet `medium`, julgamento de evidência com Opus
`high`. O `paper-lookup` carrega ~6,5 mil tokens por uso: depois de 5 perguntas, olhar o `session-report`; se pesar,
trocar por uma skill própria de ~2 KB.

## Riscos

- **Citação errada:** nada vira achado sem PMID conferido e número lido na fonte; GRADE do Claude é proposta, não veredito.
- **Direitos:** só PDFs abertos ou do acesso institucional; nada do OpenEvidence em repositório (nem privado, por cautela [I]).
- **Dinheiro:** fora tudo o que pede chave paga (Parallel, OpenRouter, Exa, BGPT, Paperclip).
- **Privacidade:** as skills de busca não têm guarda contra dado de paciente; o e-mail vai à Unpaywall, ao Crossref e ao
  NCBI (usar um endereço de pesquisa). Um gancho `UserPromptSubmit` com saída 2 barra prompt com CPF, CNS ou telefone,
  mas não nome nem história clínica [I].
- **Nunca aqui:** o plugin `healthcare` inteiro (traz extração de nota clínica), `claude-mem`, nada com chave paga.

## Fontes

- https://github.com/K-Dense-AI/scientific-agent-skills (commit `92ace75`; `docs/security-report.md`, `docs/security-triage.md`)
- https://claude.com/connectors/pubmed · https://github.com/cyanheads/pubmed-mcp-server
- https://ncbiinsights.ncbi.nlm.nih.gov/2017/11/02/new-api-keys-for-the-e-utilities/ · https://www.ncbi.nlm.nih.gov/books/NBK25499/
- https://help.openalex.org/guides/authentication · https://github.com/J535D165/pyalex · https://github.com/sckott/habanero
- https://unpaywall.org/products/api · https://www.semanticscholar.org/product/api
- https://www.zotero.org/support/dev/web_api/v3/local_api · https://github.com/54yyyu/zotero-mcp
- https://www.openevidence.com/policies/terms · https://www.openevidence.com/policies/acceptable-use
- https://github.com/kepano/obsidian-skills · https://obsidian.md/blog/free-for-work/
- https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- PICO: https://pubmed.ncbi.nlm.nih.gov/7582737/ · GRADE: https://doi.org/10.1136/bmj.39489.470347.AD e https://gdt.gradepro.org/app/handbook/handbook.html
- OCEBM: https://www.cebm.ox.ac.uk/resources/levels-of-evidence/ocebm-levels-of-evidence · living review: https://doi.org/10.1371/journal.pmed.1001603
- FINER: https://pubmed.ncbi.nlm.nih.gov/37838572/ · limites do PICO: https://pubmed.ncbi.nlm.nih.gov/17238363/
- https://code.claude.com/docs/en/hooks · https://code.claude.com/docs/en/mcp · https://github.com/vercel-labs/skills
