---
name: fechar-janela
description: "Fechar janela ou fase: ESTADO.md, PROXIMO.md (o prompt da próxima), fila de perguntas, push, resumo, aviso."
---

# Fechar a janela

Uma janela fecha pelo que vier primeiro: **fim da fase, ~150 mil tokens ou troca de modelo** (nenhuma fase troca de
modelo no meio). Fechar é deixar no disco tudo o que a próxima janela precisa para recomeçar **só com o
`ESTADO.md`, o `PROXIMO.md` e o `git log`**: regra que ficou só no chat não existe para ela. Os modelos estão em
[modelos/](modelos/) (`ESTADO.md`, `PROXIMO.md`, `PERGUNTAS.md`, `ADR.md`, `GLOSSARY.md`). Projeto ainda sem
`docs\ESTADO.md` (não migrado): o lugar do estado é o que o `CLAUDE.md` dele manda, até a fase de migração dele.

## Os passos, nesta ordem

1. **O portão da fase.** Rode as verificações que o prompt pediu (testes, conferências, números). O que falhou entra no
   estado e no resumo como falhou, com a saída; nada se dá como pronto sem a prova.
2. **`docs\ESTADO.md` reescrito** ([modelos/ESTADO.md](modelos/ESTADO.md)): até uma página, **reescrito, não
   acrescentado** — o histórico fica no `git log` e nos ADRs. Decisão difícil de desfazer, surpreendente sem contexto e
   fruto de escolha real vira ADR (`docs\adr\`; no kit, `decisoes\adr\`; [modelos/ADR.md](modelos/ADR.md)); termo do
   domínio resolvido vai ao `GLOSSARY.md`. Pronto quando uma sessão nova saberia, só com ele, o que foi feito, o que
   falta e o critério de pronto da próxima fase.
3. **`docs\PERGUNTAS.md`** ([modelos/PERGUNTAS.md](modelos/PERGUNTAS.md)): cada dúvida que só o usuário decide, com o
   problema, as opções, a recomendação e o que depende dela. As respondidas descem para "Respondidas" com o destino
   (commit, ADR).
4. **`docs\PROXIMO.md`** ([modelos/PROXIMO.md](modelos/PROXIMO.md)): o prompt da próxima janela, **conferido** contra o
   plano e o estado (a janela que fecha é quem confere). A 1ª linha traz o modelo e o **comando** `/effort <nível>`
   com o porquê (skill `modelo-e-esforco`); se houve sinal de insuficiência, ela sobe o degrau para aquele tipo de
   tarefa (esforço primeiro; Fable só depois de o Opus falhar). Leva a linha `/goal` "portão ou fila", as "Escritas em
   dado real aprovadas", as "Decisões pré-aprovadas" e o "Sempre me pergunte" (da rodada de contingências do plano).
5. **A caixa**, se outro projeto ou o outro PC precisa saber: uma mensagem no canal (`docs\para_<projeto>\` entre os
   `desosp-`; `claude-kit\caixa\` entre os PCs) e a linha no índice. Ao copiar um índice, a coluna de status do
   destinatário fica como está (ela já foi apagada duas vezes assim).
6. **Commit e push.** Commit por assunto e por caminho explícito, nunca `git add -A`. O `git push` (Q10) é livre no fim
   da fase com o portão verde, depois de `git log origin/main..`: o push leva **todos** os commits locais do ramo,
   inclusive os de outra janela — diga no resumo o que foi junto.
7. **O resumo**, no chat: o que mudou; as verificações com os números; o que ficou na fila (como pergunta, com a
   recomendação); a linha **`Sinais de insuficiência do modelo: nenhum`** — ou quais, com o exemplo (skill
   `uso-do-claude`, §3); e o `PROXIMO.md` para copiar.
8. **Lançar a próxima** só se `C:\CLAUDE-PROJETOS\claude-kit\config\fluxo.json` disser `"lancar_bg": true` (fica
   `false` até o F3c ligar): `claude --bg --name <fase> --model <ID completo> --effort <nível> "Leia docs/PROXIMO.md e
   siga"`. O texto do comando vira linha de processo: nada de nome nem pseudônimo nele. Com `false`, o usuário cola o
   `PROXIMO.md` numa janela nova (ou, no painel, `/clear` e "siga", quando o gancho do F2b injetar o `PROXIMO.md`).

## Fechar porque tudo depende da fila

Na execução largada (skill `orquestrar`), a fase não para na primeira dúvida: ela vai para `docs\PERGUNTAS.md` e o
trabalho segue com o que não depende dela. Quando **tudo** o que sobra depende da fila, fecha-se pelos passos acima
com o portão parcial dito como parcial, e o `PROXIMO.md` começa por "responder `docs\PERGUNTAS.md`".

## O aviso no celular (ADR-0001 D8; Q43, Q48)

`PushNotification` só em três casos: **(1)** a fase parou porque tudo o que sobra depende da fila; **(2)** a cadeia de
fases terminou; **(3)** uma falha que só o usuário resolve (limite de uso, login, erro de ambiente). O texto aparece na
tela bloqueada, por isso é só `projeto · fase · N perguntas` (ex.: `desosp-app · F5b parada · 3 perguntas`) — nunca
nome nem pseudônimo, nunca conteúdo. O aviso serve porque ele responde pelo app via Remote Control: sessão sem Remote
Control não avisa. Fora desses três casos, nenhum aviso (nem "terminei uma tarefa").
