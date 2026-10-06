# organizar-projetos — o fluxo da reorganização vira módulo da uso-do-claude (05/10/2026)

- **Decisão do Ettore (05/10, chat da janela da reorganização):** o fluxo inteiro desta mudança — juntar os projetos e o
  kit do Claude numa pasta-mãe, o GitHub, o sistema de cores — vira um **módulo da skill `uso-do-claude`**, chamado
  **`organizar-projetos`**, e não uma skill separada. O sistema de cores (antes "o pacote das pastas", plano 4.1) mora
  dentro dele.
- **Exigência:** avisos para que, ao rodar num sistema novo, se **aproveite só o que for necessário** e se rode uma
  **checagem para não duplicar** o que já existe no PC (skills, ganchos, CLAUDE.md, ícones, scripts, pastas de projeto).
- **O primeiro uso:** o desktop. Lá os arquivos estão espalhados: skills copiadas em `C:\Users\<usuário>\.claude\skills`,
  um repositório direto na raiz do `C:`, arquivos de IA em pastas diferentes. Só o finance-app está no GitHub; faltam dois
  projetos. O objetivo é o mesmo daqui: reunir tudo numa pasta-mãe, **sem prejudicar o CLAUDE.md** pessoal, preservando a
  identidade de cada projeto (pasta, git, CLAUDE.md, memória), e pôr no GitHub os que faltam.
- **Junto:** a regra `deny` do Claude Code para `desosp-app-dados` (Read e Edit em
  `//c/CLAUDE-PROJETOS/desosp-app-dados/**`, no `settings.json` de usuário) foi gravada e testada em 05/10: o Glob não
  acha nada lá e o Read é recusado. Não afeta o app rodando, o código do app, os commits nem o GitHub.

## A forma proposta (a janela de construção decide os detalhes)

```
skills\uso-do-claude\
  SKILL.md                    a descrição ganha "organizar os projetos e as pastas de um PC"; uma seção curta aponta para o módulo
  organizar-projetos\
    ORGANIZAR.md              o fluxo em fases, cada uma com o seu "sim"; as regras que não se quebram; as lições de 04-05/10
    reaproveitar.md           a checagem do que já existe no PC, antes de instalar qualquer coisa (para não duplicar)
    perguntas.md              o setup de perguntas (no formato do grill-me) e o que cada resposta decide
    pastas.md                 o sistema de cores (verbos, marcas, a pasta nova, o gancho, a conferência, o manual)
    github.md                 publicar o que falta (sempre privado; varredura de segredo e de dado sensível antes do
                              primeiro envio) e re-registrar no GitHub Desktop o que mudou de pasta
    prompts.md                os modelos dos prompts das janelas de cada projeto
    scripts\                  mudanca.py (generalizado: lê o plano de um arquivo, em vez de caminhos fixos), varredura.py,
                              pastas.py, desenho.py, gancho.py, inventario.py; tests\
    icones\                   os quadros PNG do pacote do Ettore (o .ico se monta em cada PC)
```

## As fases (o mesmo fluxo de 04-05/10)

0. **Reaproveitar** — o que o PC já tem (skills, ganchos, CLAUDE.md, ícones, scripts, kit); o que serve, o que duplicaria.
1. **Preparar o PC** — trazer o kit; comparar as skills e o CLAUDE.md de lá com os do kit e juntar; ligar (junção e
   hardlink; nunca editar o CLAUDE.md pela ferramenta Edit).
2. **Inventário** (só leitura, subagente) — projetos, repositórios (e se há repositório na raiz do disco), arquivos de IA
   soltos, memórias, ganchos, OneDrive, junções, permissões de sandbox (Codex), o que está e o que não está no GitHub.
3. **Entrevista** (grill-me) — nome de cada projeto, o que é do usuário e o que é da IA, dado sensível, o que vai ao
   GitHub, a pasta de dados de cada app, a pasta-mãe.
4. **Plano** — o mapa de cada projeto, a ordem, os prompts.
5. **Mudança** — retrato antes, movimentos (mover, nunca reclonar), lápides, memória para as chaves novas, retrato depois,
   caminho de volta. O comando é do usuário quando o modo automático bloquear.
6. **GitHub** — publicar (privado) e registrar.
7. **Janelas de cada projeto** — corrigir os caminhos (prompt nomeado).
8. **Cores** — aplicar, gancho, manual, VS Code.
9. **Limpeza** — o velho só sai no fim, conferido.

## As lições de 04-05/10 que entram no módulo

- O modo automático não deixa o Claude mover pasta de projeto nem apagar na raiz do `C:`: entregar o comando, com
  conferência, ao usuário.
- `os.rename` no mesmo disco é atômico; um "Acesso negado" pode ser passageiro — o script tenta de novo e, se não
  der, para sem mexer em nada; rodar de novo pula o que já mudou.
- Lápide: arquivo com o nome da pasta velha (precisa de administrador na raiz do `C:`), para o caminho esquecido dar erro.
- A ferramenta Edit separa o hardlink do `CLAUDE.md`: gravar no próprio arquivo e conferir com `fsutil hardlink list`.
- O `.ignore` barra o Grep e não o Glob; a proteção de verdade é a regra `deny`.
- Junção com caminho absoluto (como um `node_modules` de teste) conta em dobro no retrato e quebra na mudança; o
  `os.walk` do Python 3.12 entra em junção.
- O sandbox do Codex deixa permissões próprias nas pastas em que trabalhou.
- A chave da memória é o caminho com todo caractere não alfanumérico trocado por `-`; copiar, não mover.

## Construído (05/10, noite — janela 4, Opus 5.5 · high)

- **O portão da paridade abriu:** a cópia do desktop (`_do_desktop\desktop_2026-10-05\`) tem os 10 hashes iguais aos de
  `base_notebook_2026-10-04\kit_antes.json`; lá não existe CLAUDE.md pessoal. Nada a juntar.
- **O módulo** está em `skills\uso-do-claude\organizar-projetos\` e a `uso-do-claude` aponta para ele (descrição e §13).
  Testes: `python -m pytest` na pasta do módulo (123 passam; a mutação "seguir junção" derruba os 7 testes de junção);
  `scripts\tests` do kit (13 do `ligar_claude.py`) seguem verdes.
- **Rodado só lendo, na árvore real:** `inventario.py` (achou 23 `desktop.ini` de 30/09 e um `effortLevel` de topo no
  settings de usuário); `pastas.py aplicar --ver` (248 pastas a pintar, 0 provisória); `conferir` (o pacote de 30/09 com
  `+r`, que o aplicar troca); `varredura.py` com `planos\notebook_2026-10-05.json`.
- **A prévia foi aprovada** (versão 4, 05/10 à noite: `2026-10-05_icones-escolha.md`, seção "A versão 4"): o pacote do
  Ettore e, das referências dele, o braço de robô, a mão com chip, o cadeado no circuito e o robô com "?"; o Projeto com
  IA na cor original. Os quadros do módulo são os da página aprovada, pixel a pixel. A amostra no Explorador:
  `prototipos-icones\amostra-referencias\`.
- **O `effortLevel: xhigh` de topo saiu do `settings.json` de usuário** (pedido do Ettore). Ficou aberto: o Opus 5.5 está
  gravado em `xhigh` dentro de `modelSettings` (apareceu em 05/10 à noite, provavelmente por um `/effort` de outra janela).
- **Pasta nova na mãe:** `desosp-app-backups` (o destino dos backups que a janela do app escolheu, já com regra `deny`).
  Precisa de linha no mapa antes de aplicar (a proposta: Dado real).
- **Para a janela 5:** `pastas.py instalar --lapide C:\DESOSP --lapide C:\DESOSP_APP --lapide C:\DESOSP_APP_REAL
  --lapide C:\planilha-hc --lapide C:\conversation-core --lapide C:\CLAUDE`; as passageiras do app (janela 3) entram no
  `mapa.json` antes de aplicar; `desosp-hc\rodada` (se existir) aparece como provisória.

## Aplicado (05/10, 23:30–00:00 — nesta janela 4, no lugar da janela 5)

O Ettore autorizou ("implemente então, tem minha autorização") e pediu trabalho sem interrupção. As condições do plano
estavam cumpridas: as janelas do kernel, da planilha e do app tinham terminado (commits até 22:28; a do app escreveu o
"Passo 8 — para o sistema de cores" no `HANDOFF_APP.md`), nenhuma outra sessão do Claude estava aberta, o módulo estava
testado e os ícones aprovados.

| passo | resultado | conferido por |
|---|---|---|
| decisões | Opus 5.5 de `xhigh` para `medium` em `modelSettings`; `desosp-app-backups` = Dado real; as passageiras do app no mapa (`_PUXANDO_*`, `_PUXADA_ANTERIOR_*`, `entrada/*` dos dados, e as mesmas na `workspace_dev`) | `puxar.py` (só as `_PUXANDO_` são apagadas; as `_PUXADA_ANTERIOR_` guardam rodadas) |
| antes de pintar | cópia dos 96 `desktop.ini` que existiam (23 de 30/09, 55 alheios, 18 das amostras) em `%LOCALAPPDATA%\claude-pastas\antes_da_aplicacao_2026-10-05\` (com a `lista.json`) | contagem |
| `instalar` | `local.json` (a mãe, o módulo, os ícones, as 6 lápides), os 9 `.ico` em `%LOCALAPPDATA%\claude-pastas\icones`, `desktop.ini` no ignore global do git (`%USERPROFILE%\.config\git\ignore`) | saída do comando |
| `aplicar` | **181 pastas** em 0,7 s (os 23 de 30/09 trocados, o `+r` tirado, o alheio de `docs\gpt` preservado); a 2ª rodada não escreve nada | `aplicar --ver` |
| `legenda` | `C:\CLAUDE-PROJETOS\LEGENDA DAS PASTAS.html` | arquivo |
| `vscode` | `.vscode\settings.json` nos 4 projetos (clones do Material + `peacock.color`), no `.git\info\exclude`; extensões `pkief.material-icon-theme` 5.39.0 e `johnpapa.vscode-peacock` 4.5.1; `workbench.iconTheme` no settings de usuário do VS Code | `code --list-extensions` |
| `conferir` | **0 problemas**; 2 avisos esperados (na planilha, `2026-09` e `placar` com verbos diferentes ficam sem cor no VS Code) | saída 0 |
| git | `desktop.ini` ignorado nos 3 repositórios; nenhum no `git status` | `git check-ignore -v` |
| gancho | testado antes numa sessão nova (`claude -p --settings`, Sonnet 5.5, US$ 0,35: o `additionalContext` chegou); ligado (`settings.json.antes-gancho-20261005_233738` é a cópia de antes); ao vivo nesta sessão: a pasta herdeira ganhou "Eu leio" calada e a da raiz gerou a pergunta (as pastas de teste foram tiradas) | o texto do gancho |
| tempo do gancho | processo novo, 20 chamadas por caso: mediana 46–50 ms, **p95 49–57 ms** (o limite era 150), sempre saída 0 e nada impresso | `medir_gancho.py` |
| varredura | nenhum caminho velho vivo em código ou configuração; o que sobra é histórico (comentário, documento da mudança, dado de teste que simula manifesto antigo, `docs\fontes` do app) | `varredura.py` com o plano do notebook |

| suítes com as cores | **kernel 614 passed** (48 s) · **planilha 99 passed** (12 s) · **app 736 passed, 1 skipped** (o de sempre, `test_catalogos.py:100`; 7 min 53 s, com `DESOSP_KERNEL` no lugar novo) | `pytest -q -rs` |
| depois das suítes | `conferir` = 0 de novo; **234** pastas certas: as 181 e mais 53 pastas das 24 skills novas que entraram no kit às 23:47 (pelo `npx skills` e o `ligar_claude.py`, já ligadas por junção), pintadas de "Não toco" pelo gancho, como manda o mapa | `aplicar --ver`; a hora de cada `desktop.ini` |
| comparação de skills | o `ligar_claude.py` e o `inventario.py` passam a ignorar `desktop.ini` e `Thumbs.db` (são de cada PC): sem isso, a cópia de uma skill no desktop pareceria diferente da do kit | os testes novos (14 do kit, 147 do módulo) |
| a cópia para o desktop | `Downloads\claude-kit-do-notebook_2026-10-06.zip`: o kit sem `_do_desktop`, sem `desktop.ini` e sem `.vscode`, com `manifesto.json` (sha256) e `LEIA-ME.txt`; conferido arquivo a arquivo | `zip_kit.py` |

**O caminho de volta** (nada se perde): `pastas.py remover` tira os nossos `desktop.ini` (o alheio fica); os de antes
estão na cópia acima (voltam com `attrib -h -s`, cópia e `attrib +h +s`); `pastas.py desligar-gancho` tira só o nosso
gancho; as extensões saem pelo VS Code.

## Encerramento desta janela (06/10, madrugada) — o que a próxima janela precisa saber

**Estado:** o módulo `organizar-projetos` está pronto e testado (147 testes no módulo, 14 nos scripts do kit), e o
sistema de cores está **aplicado e ligado no notebook** (seção "Aplicado" acima). Esta janela (a 4, que também fez o
trabalho da 5) está encerrada.

**Limpeza feita (06/10, com o "sim" do Ettore, tudo para a Lixeira):** `%LOCALAPPDATA%\DESOSP\icones_pastas` (o pacote
de 30/09), `%LOCALAPPDATA%\claude-mudanca-2026-10-05` (os retratos e o `mudanca.py` da mudança; o caminho de volta
agora é o `mudanca.py voltar` do módulo, com `planos\notebook_2026-10-05.json`) e, em
`C:\CLAUDE-PROJETOS\prototipos-icones`, os protótipos, as amostras, os candidatos e as prévias locais. **Ficaram de
propósito:** `prototipos-icones\amostra_gerada_ettore` (o pacote do Ettore, a fonte do `desenho.py quadros`) e
`prototipos-icones\referencia_icones` (as referências dele). A conferência continua em 0.

**O que espera data ou decisão:**

| item | quando | como |
|---|---|---|
| as 6 lápides de `C:\` (`C:\DESOSP`, `C:\DESOSP_APP`, `C:\DESOSP_APP_REAL`, `C:\planilha-hc`, `C:\conversation-core`, `C:\CLAUDE`) | **só depois das rodadas de 07, 08 e 09/10** (decisão do Ettore, 06/10); então para a Lixeira | arquivo na raiz do `C:` = PowerShell de administrador, comando entregue ao Ettore; depois, tirar a lista `lapides` do `%LOCALAPPDATA%\claude-pastas\local.json`, senão o `pastas.py conferir` acusa "lápide ausente" |
| a cópia dos `desktop.ini` de antes da aplicação (`%LOCALAPPDATA%\claude-pastas\antes_da_aplicacao_2026-10-05\`) | depois de o Ettore aprovar o Explorador e o VS Code | Lixeira |
| as cores do Material no VS Code | na primeira janela do VS Code aberta num projeto | se os clones não pegarem no `.vscode\settings.json` do projeto, levar para o settings de usuário |

**Com a outra janela (a que orquestra o kit e o desktop), não com esta:**
- **as skills**: as 24 que entraram no kit em 05/10 às 23:47 (pelo `npx skills` + `ligar_claude.py`) estão em
  pesquisa e definição lá ("deixe que a outra janela maneje", Ettore, 06/10). Daqui só se registrou: elas foram
  pintadas de "Não toco" pelo gancho, e o `ligar_claude.py` e o `inventario.py` passaram a ignorar `desktop.ini` e
  `Thumbs.db` na comparação de skills;
- **o desktop e o GitHub** (o prompt 7 de `2026-10-04_prompts-das-janelas.md`): também orquestrados lá. O kit para o
  desktop está em `C:\Users\ettor\Downloads\claude-kit-do-notebook_2026-10-06.zip` (com `manifesto.json`; o prompt 7
  já fala do zip e do `Unblock-File`). Se o kit mudar antes de ir, refazer o zip (sem `_do_desktop`, `desktop.ini` e
  `.vscode`).

**Onde está cada coisa:** o roteiro `skills\uso-do-claude\organizar-projetos\ORGANIZAR.md`; o sistema de cores
`pastas.md` e `mapa.json`; os ícones aprovados (versão 4) em `decisoes\2026-10-05_icones-escolha.md`; neste PC,
`%LOCALAPPDATA%\claude-pastas\` (o `local.json` e os `.ico`); a legenda em `C:\CLAUDE-PROJETOS\LEGENDA DAS PASTAS.html`.
Pasta nova fora do mapa ganha o "?" e o gancho pede ao Claude que pergunte a cor: responder com
`pastas.py marcar "<pasta>" <verbo>`.
