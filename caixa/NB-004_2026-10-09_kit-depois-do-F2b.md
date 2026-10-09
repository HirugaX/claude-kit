# NB-004 — do notebook para o desktop · 09/10/2026

> Série NB (notebook → desktop). Gerado uma vez, não é reescrito. Regras: `caixa\LEIA-ME.md`. Soma-se à NB-003: se o
> desktop ainda não a aplicou, faça a NB-003 inteira e, no passo 3 dela, o `instalar_kit.py` já faz o desta.

## Em uma linha

O F2b trouxe os ganchos do `nucleo` (abertura, modelo, portão, guarda de dado, fila), a statusline e a medição semanal
automática. Os ganchos chegam com o `git pull`; a statusline e o `showClearContextOnPlanAccept` moram no
`~\.claude\settings.json` de cada PC, e o `instalar_kit.py` os grava.

## O que o desktop faz, na ordem

1. **Feche as janelas do Claude Code** no desktop.
2. **Traga o kit:** `git -C C:\CLAUDE-PROJETOS\claude-kit pull --ff-only`.
3. **Instale:** `python C:\CLAUDE-PROJETOS\claude-kit\scripts\instalar_kit.py`. Ele grava no `~\.claude\settings.json`
   (com backup em `~\.claude\backups\`) a `statusLine` do nucleo e o `showClearContextOnPlanAccept: true`.
4. **O rótulo do PC:** num terminal, `echo %COMPUTERNAME%`; numa janela do kit, acrescente esse nome em
   `config\fluxo.json`, chave `"pcs"`, com o valor `"desktop"` (o notebook é `"NOTE_ETTORE": "notebook"`), e faça o
   commit (`git add config/fluxo.json`). Sem isso, a coluna `pc` da medição sai com o nome do computador.
5. **O guia:** `python C:\CLAUDE-PROJETOS\claude-kit\scripts\gerar_guia_skills.py`.

## Como saber que deu certo

- `instalar_kit.py --verificar` termina com "Verificação: 0 achados".
- `python C:\CLAUDE-PROJETOS\claude-kit\scripts\testar_ganchos.py` termina com "52 de 52 verdes".
- Num terminal, `claude` numa pasta qualquer: a linha de baixo mostra `Opus 5.5 · <esforço> · ctx N%` e, depois da 1ª
  resposta, `5h N% · sem N%`; o arquivo `%USERPROFILE%\.claude\kit-local\limites.jsonl` aparece.
- Na abertura seguinte, o gancho mede sozinho a última semana fechada deste PC (em segundo plano, sem imprimir): uma
  linha nova com `pc` = `desktop` em `metricas\uso-semanal.csv`, que vai no próximo commit do kit feito no desktop.

## O que NÃO fazer agora

- Não mexa nos projetos do desktop (DASH, Folha/RH, Acolhimento): eles entram no F8. Nenhum deles tem `docs\ESTADO.md`,
  então os ganchos da 2ª camada (portão, guarda, fila) não agem lá; os ganchos antigos deles continuam.

Depois, escreva no `INDICE.md` desta caixa, na linha da NB-004: `confirmado — DD/MM — <o que ficou>`. Se algo falhou,
uma DK com a saída do `--verificar` e do `testar_ganchos.py`.
