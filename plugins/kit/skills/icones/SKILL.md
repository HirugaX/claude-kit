---
name: icones
description: Os ícones das pastas — os desenhos, a montagem do .ico em cada PC, a prévia, e os pedidos de ícone novo, que se juntam e se desenham em lote. Só por /icones.
disable-model-invocation: true
---

# Os ícones das pastas

Os desenhos são a **versão 4**, aprovada pelo Ettore em 05/10/2026
(`C:\CLAUDE-PROJETOS\claude-kit\decisoes\2026-10-05_icones-escolha.md`): o pacote dele (versão 3) e, das referências
dele, o braço de robô, o chip, o cadeado no circuito e o robô com `?`, redesenhados no mesmo estilo (pasta lisa, aba
mais escura, emblema branco; de 16 a 24 px um símbolo simplificado; o correio ganha o envelope a partir de 48 px). O que
cada verbo e cada marca significa: `/cores-das-pastas`.

## Onde está cada coisa

| o quê | onde |
|---|---|
| os quadros PNG de cada ícone (16, 20, 24, 32, 40, 48, 64, 128, 256 px) — **a fonte do desenho** | `C:\CLAUDE-PROJETOS\claude-kit\plugins\nucleo\pastas\icones\<id>\<px>.png` |
| a origem de cada ícone (do pacote dele, recolorido, ou redesenhado) | `...\pastas\icones\quadros.json` |
| a cor de cada ícone | o `mapa.json` do módulo (`...\pastas\mapa.json`); o `.ico` se recolore na montagem |
| o programa | `...\pastas\scripts\desenho.py` |
| o pacote do Ettore (v3), as referências dele e as prévias antigas | `C:\CLAUDE-PROJETOS\prototipos-icones\` (`amostra_gerada_ettore\`, `referencia_icones\`) |
| os `.ico` montados neste PC | `%LOCALAPPDATA%\claude-pastas\icones\` (gravados pelo `pastas.py instalar`) |

O `.ico` nunca viaja pronto: monta-se em cada PC a partir dos quadros. Desde junho de 2026 o Windows ignora
`desktop.ini` com marca da web, e um `.ico` baixado pode vir marcado.

## Os comandos (`python <módulo>\scripts\desenho.py ...`)

| comando | o que faz |
|---|---|
| `montar <pasta>` | os `.ico` de todos os verbos e marcas, nas cores do mapa (o `pastas.py instalar` chama este) |
| `previa <arquivo.html>` | a prévia: 16, 20, 32, 48 e 256 px, em fundo claro e escuro |
| `amostra <pasta>` | pastas de amostra com `desktop.ini`, para ver no Explorador |
| `quadros <pasta_do_pacote_ettore>` | refaz os quadros a partir dos `.ico` do Ettore, pela receita `ORIGEM` do `desenho.py` (enquanto o pacote existir em `prototipos-icones\amostra_gerada_ettore`) |

## Ícone novo: junta-se o pedido, desenha-se em lote

Um verbo ou marca novo, ou um desenho trocado, não se desenha na hora em que aparece:

1. **Anote o pedido** numa linha de `C:\CLAUDE-PROJETOS\prototipos-icones\PEDIDOS.md` (crie se não existir): a data, o
   projeto, o que a pasta representa, a sugestão de desenho e de cor. Enquanto espera, a pasta usa o verbo mais
   próximo, ou fica provisória.
2. **Desenhe em lote**, numa janela da raiz (`C:\CLAUDE-PROJETOS`), quando o Ettore pedir ou os pedidos somarem
   alguns: os quadros novos em `icones\<id>\` no mesmo estilo, a origem em `quadros.json`, a cor e o verbo no
   `mapa.json`; `desenho.py previa` para o Ettore aprovar **antes** de aplicar (um endereço só para a prévia, para ele
   não abrir uma antiga).
3. Aprovado: os testes do módulo (`python -m pytest` em `...\pastas`, inclusive o `test_desenho.py`, que confere os
   desenhos que não mudaram pixel a pixel), `pastas.py instalar` e `aplicar` em cada PC, e os pedidos atendidos saem do
   `PEDIDOS.md`.
