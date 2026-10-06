# Pastas de dado, proteções e o Google Drive — inventário do notebook (foto de 06/10/2026)

- **A pergunta:** onde mora o dado de paciente de cada projeto (dentro ou fora do repositório) e o que o protege hoje?
  Quem está pondo arquivos soltos na raiz do Google Drive?
- **A data:** 06/10/2026.
- **O projeto que pediu:** claude-kit (rodada 3 do fluxo; perguntas 4 e 5 do Ettore; Q16 e Q25 do
  `decisoes\2026-10-06_plano-fluxo.md`).
- **Conferir de novo depois de:** qualquer mudança de pasta de dado, de `.gitignore` ou de `deny` (é foto de 06/10).
- **Método:** subagente só de leitura — nomes de pasta, `.gitignore`, settings e `Test-Path`; nenhuma pasta de dado
  aberta; nos transcritos, só nomes de ferramenta. Nenhum dado de paciente neste arquivo.

## Conclusão em poucas linhas

1. **Só o app tem o dado fora do repositório:** `desosp-app-dados` e `desosp-app-backups`, pastas irmãs dentro de
   `C:\CLAUDE-PROJETOS`, fora de todo git, com `deny` de Read e Edit (`~\.claude\settings.json:18-21`) e `deny_paths`
   na política do safety-net (aplicada em 06/10, `~\.cc-safety-net\policy.json`).
2. **Censo e planilha HC guardam dado de paciente dentro do repositório,** protegido só pelo `.gitignore` — o git não
   sobe, mas a sessão do projeto enxerga. Nenhum projeto tem `deny` próprio, nem política própria do safety-net.
3. **No app, dentro e ignorados:** `workspace_dev\` (cópia do dado) e `docs\para_o_app\` (a caixa do kernel, com nomes
   reais).
4. **O `.ignore` da pasta-mãe** (que faz o Grep e o Glob pularem) lista só `desosp-app-dados/`; falta
   `desosp-app-backups/`.
5. **Google Drive:** deste notebook nada escreve no Drive — não há Google Drive para computador (só a unidade `C:`),
   nenhum código em `C:\CLAUDE-PROJETOS` grava lá, nenhuma ferramenta do Google foi chamada pelo Claude Code em 552
   transcritos, e o `export` do Claude Docs só devolve o arquivo (pdf, docx, html, texto, markdown, notion). Suspeitos,
   fora daqui: o claude.ai com o conector do Google (a skill sincronizada `google-workspace`, desligada em 06/10, "cria e
   edita arquivos do Google no seu Drive"); o desktop, onde `G:` é o Drive e por onde iam os zips do kit; as ferramentas
   do Google (Gemini exporta para Docs na raiz). Decisão do Ettore: tudo em `IA\<projeto>`, arrumado numa janela no
   desktop (fase Fd do plano).

## O detalhe

| projeto | o que o `.gitignore` exclui (dado, saída, documento) | pastas de dado que existem dentro |
|---|---|---|
| `desosp-app` | `workspace_dev/` (:11), `*.db*`, `*.sqlite*` (:15-20), `*.xlsx`, `*.xls`, `*.pkl` (:23-25), `docs/para_o_app/` (:67), `local_nomes.json` (:75), `docs/fontes/PLANILHA_HC/` (:82) | `workspace_dev`, `docs\para_o_app`, `docs\fontes\PLANILHA_HC` |
| `desosp-censo` | `*.xlsx`, `*.xls`, `*.xlsm`, `*.csv`, `*.pkl`, `*.pdf` (:2-7), `entrada/`, `saida/`, `arquivo/` (:8-10), `historico/` (:12), `desosp_app.db*`, `_envios/` (:18-20), `desosp/local_nomes.json` (:39), duas fontes (:43-44) | `entrada`, `saida`, `arquivo`, `historico`, `fontes`, `docs\para_o_app` |
| `desosp-hc` | `entrada/*`, `saida/*`, `trabalho/*` (:3-8), `planilhas/`, `historico/`, `privado/`, `rodada/`, `fontes/` (:9-13), `*.xlsx` menos os moldes (:14-15), `*.pdf`, `*.pkl` (:16-17) | `entrada`, `saida`, `trabalho`, `planilhas`, `historico`, `privado` |

- Sem `.gitignore`: `claude-kit`, `pesquisa-clinica`, `prototipos-icones` (sem git).
- Settings: `desosp-app\.claude\settings.json` e `desosp-hc\.claude\settings.json` só com ganchos e env; o censo sem
  settings; nenhum `settings.local.json`. Os `allow` do usuário citam caminhos antigos (`c--DESOSP`, `C:\DESOSP`).
- MCP: `mcpServers` vazio em `~\.claude.json`; o único conector do claude.ai já usado é o Claude Docs.
- Cores: o `organizar-projetos\mapa.json` já marca `historico` (censo) e `privado` (HC) como dado real.

## Fontes

- `C:\CLAUDE-PROJETOS\desosp-app\.gitignore`, `desosp-censo\.gitignore`, `desosp-hc\.gitignore` (linhas acima)
- `~\.claude\settings.json:18-21` (deny), `:32` (gancho das cores), `:74` (gatilho do ultracode); `~\.claude.json`
- `~\.cc-safety-net\policy.json`; `C:\CLAUDE-PROJETOS\.ignore:2`
- `claude-kit\scripts\gerar_guia_skills.py:389`; `claude-kit\_do_desktop\desktop_2026-10-05\LEIA-ME.txt:34-35`;
  `claude-kit\decisoes\2026-10-04_prompts-das-janelas.md:215`
- `~\.claude\skills\.trash\` (as 5 skills desligadas em 06/10 09:29)
