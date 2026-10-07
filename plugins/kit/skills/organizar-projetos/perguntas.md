# Perguntas — a entrevista da fase 3

No formato do `grilling` (o `/grill-me`): em **rodadas**; cada rodada pergunta só o que já tem os pré-requisitos
respondidos; cada pergunta numerada, com a resposta recomendada. Fato do ambiente é trabalho do Claude (o inventário
e a fase 2 já trouxeram), nunca pergunta ao usuário. Termina quando não sobra decisão; o registro vai para
`claude-kit\decisoes\AAAA-MM-DD_<assunto>.md` e o usuário confirma antes do plano.

```
❓ **Q1** - **<título>**: <a pergunta, com as opções e o que o inventário mostrou>

➡️ <a recomendação, e por quê>
```

## Rodada 1 — o que não depende de nada

| # | pergunta | recomendação de partida | o que a resposta decide |
|---|---|---|---|
| 1 | **A pasta-mãe**: onde reunir os projetos do Claude? | `C:\CLAUDE-PROJETOS` (o mesmo nome nos dois PCs: o manual, as dicas das pastas e o `mapa.json` apontam para ela) | o `"mae"` do plano e do `local.json` |
| 2 | **Quais pastas são projetos do Claude**, e quais ficam fora (outro agente, pessoal, arquivo morto)? Uma linha por pasta que o inventário achou | fora: projeto de outro agente (Codex/GPT, como o `conversation-core` → `C:\GPT`), arquivo morto (fica onde está) | a lista de movimentos; o que fica fora das cores |
| 3 | **O nome novo de cada projeto** | nome curto, minúsculo, com hífen, que **não** coincida com o caminho velho (assim o caminho esquecido falha em vez de achar a pasta errada) | o `"para"` de cada movimento; as chaves novas da memória |
| 4 | **A raiz do disco é um repositório?** (se o inventário achou `.git` na raiz) | descobrir o que ele versiona antes de tudo; em geral, mover o projeto para a mãe e desfazer o repositório da raiz | se há uma fase extra antes da mudança |
| 5 | **Como o kit viaja** entre os PCs? | cópia manual com manifesto sha256 (o original é o do notebook) | a fase 1 e o retorno de mudanças |

## Rodada 2 — depende de quais são os projetos

| # | pergunta | recomendação de partida | o que a resposta decide |
|---|---|---|---|
| 6 | **Dado sensível**: em cada projeto, que pastas têm dado pessoal, de saúde ou financeiro? Pode sair da máquina? | nenhum dado sensível sai; a pasta de dados de um app fica **fora** do repositório, ao lado dele (`<app>-dados`), com regra `deny` no settings do Claude Code | a pasta de dados; a regra `deny`; o que o `antes_do_github.py` procura (o arquivo de termos, fora do repositório) |
| 7 | **O que vai ao GitHub**: cada projeto sem remote vai? | sim, **privado**, depois da varredura; o que não for código (dados, rodadas) fica no `.gitignore` | a fase 6 |
| 8 | **O que é do usuário e o que é da IA** em cada projeto (onde você deposita, onde lê, onde edita, onde não mexe) | levantar pelas pastas que o inventário viu e propor o verbo de cada uma | o mapa das cores daquele projeto (`/cores-das-pastas`) |
| 9 | **As pastas que o programa cria e apaga sozinho** (as passageiras) e as de rodada | ficam sem cor; quem lista é a janela de cada projeto, lendo o código | as entradas `sem-cor` do mapa |
| 10 | **O que roda agora** e o que não pode parar (app ligado, rodada em andamento, prazo próximo) | mudar fora dos dias de rodada, com o app desligado pelo próprio app | a data e as condições da fase 5 |

## Rodada 3 — depende do mapa e da ordem

| # | pergunta | recomendação de partida | o que a resposta decide |
|---|---|---|---|
| 11 | **O mapa completo de cada projeto**, aprovado de uma vez ("todas as situações desenhadas agora") | a tabela do mapa por projeto, com as exceções | o `mapa.json` |
| 12 | **As cores e os desenhos** (num PC que já tem o sistema, vale o que está no `mapa.json`) | os 9 ícones do pacote; a prévia antes de aplicar | `desenho.py previa`; o `mapa.json` |
| 13 | **A moldura de cada janela do VS Code** (Peacock) | uma cor por projeto, longe das cores dos verbos | `"peacock"` de cada projeto |
| 14 | **A ordem das janelas** e o que roda em paralelo | no máximo duas ao mesmo tempo; paralelo só o que não se cruza | os prompts ([prompts.md](prompts.md)) |
| 15 | **As lápides**: criar arquivo com o nome de cada caminho velho? | sim (precisa de administrador na raiz do disco); saem quando a varredura do projeto der zero | o `tudo` do `mudanca.py`; o `"lapides"` do `local.json` |
| 16 | **O velho**: quando apagar o que sobrou (kit antigo, pacote de ícones antigo, retratos)? | só na fase 9, conferido, para a Lixeira | a fase 9 |

## O que já está decidido (não se pergunta de novo)

- O sistema de cores: 5 verbos, 3 marcas, a regra da pasta nova, o gancho, o manual (`/cores-das-pastas`). Num PC
  novo, só se pergunta o **mapa** dos projetos dele.
- `+s` na pasta, nunca `+r`; o `.ico` gerado em cada PC; nenhum `CLAUDE.md` na raiz da mãe.
- O original do kit é o do notebook.
