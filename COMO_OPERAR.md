# Como você opera — até o F3

Vale da F1b até o F3c terminar. A parte "depois do F3" (sem carregar prompt: a fase seguinte se lança sozinha, a fila
de perguntas, o aviso no celular) entra aqui no F3c, se o laço do F3a passar. O desenho completo e o porquê estão no
plano, `decisoes\2026-10-06_plano-fluxo.md`, seção "Como você opera daqui em diante".

## Uma janela, passo a passo

1. **Abra a janela na pasta que o prompt indica.** No painel do VS Code, abra a pasta; no terminal, `cd <pasta>` e
   `claude`. Uma janela é um projeto só.
2. **Digite o `/effort` da 1ª linha do prompt.** Se o prompt pedir Sonnet 5.5, digite `/model sonnet` ou escolha-o na
   lista do `/model` (o atalho abre o 5.5 desde a 2.1.291; a troca para o Sonnet 5 é barrada pelo gancho). O
   `/effort` digitado vira o padrão das próximas janelas, o que não atrapalha, porque todo prompt traz o seu. Para valer só nesta sessão, use o seletor do `/effort` e a tecla `s`.
3. **Cole o prompt.** O Claude trabalha e para só nos pontos da Q10:
   - escrita em dado real não aprovada antes;
   - rodada real ou reprocesso não aprovados;
   - migração de banco ou de esquema;
   - regra clínica nova;
   - leitura de fonte nova;
   - subir para Fable, `xhigh`, `max` ou ultracode (para descer, quando a qualidade se mantém, ele não pergunta);
   - o mesmo erro depois de duas tentativas diferentes;
   - decisão que não está no `ESTADO.md` nem num ADR.

   Com o Remote Control ligado sozinho, dá para responder pelo app do celular; num ponto de parada chega o aviso
   "projeto · fase · precisa de você".
4. **Responda no chat** com a letra e a nuance ("a, mas sem X").
5. **Ao fechar, a janela entrega o resumo e o prompt da próxima, já conferido.** O resumo traz "Sinais de insuficiência
   do modelo". Copie o prompt, feche a janela e abra a próxima.

## A ordem até o app

F2a → F2b → F3a ∥ F3b (em paralelo, cada uma na sua pasta de teste) → F3c → F5a (o app volta).
- A R0, a revisão do front do app, roda em paralelo quando você quiser, porque não toca no kit.
- Depois do F5b vêm F6 ∥ F7 ∥ N1.
- O desktop instala o kit logo depois do F1b (`caixa\NB-002`) e espera o F8 para os projetos de lá.

## Onde olhar

| o quê | onde |
|---|---|
| onde cada projeto está | `docs\ESTADO.md` do projeto (uma página) |
| o porquê das decisões | `docs\adr\` do projeto; no kit, `decisoes\` |
| que skills existem, para que servem, quem liga | `claude-kit\GUIA_DAS_SKILLS.docx` (gere com `python scripts\gerar_guia_skills.py`); as skills moram em `claude-kit\plugins\<grupo>\skills\` |
| se o kit está bem instalado | `python C:\CLAUDE-PROJETOS\claude-kit\scripts\instalar_kit.py --verificar` (rode depois de todo `git pull` do kit) |
| o custo de abrir uma janela | `python C:\CLAUDE-PROJETOS\claude-kit\scripts\medir_uso.py --sessoes` |
| a semana em números | `claude-kit\metricas\uso-semanal.csv` (uma linha por semana e por PC); a planilha com os gráficos da régua e as metas em `claude-kit\metricas\uso.xlsx` (fora do git; cada PC a refaz) |
| modelo, esforço, contexto e limites, ao vivo | a statusline, no terminal (o painel do VS Code não a mostra): `Opus 5.5 · medium · ctx 34% · 5h 12% · sem 40%` |

**Manutenção:** a janela aberta na raiz `C:\CLAUDE-PROJETOS` cuida das cores e dos ícones das pastas e do balanço das
métricas. Os ícones novos ficam para depois, todos juntos.

## O que os ganchos fazem sozinhos (desde o F2b)

- **Ao abrir qualquer janela:** avisam modelo errado (Sonnet 5, Opus 5) e esforço `xhigh` ou `max`; atualizam o kit
  (`git pull`, no máximo uma vez por hora) e avisam se ele divergiu; medem a semana fechada em segundo plano; e, a cada
  15 dias, avisam numa linha que o balanço das métricas venceu — aí abra a janela da raiz e peça "rode o
  `claude-kit\metricas\BALANCO.md`" (as propostas vão para a fila do kit, `claude-kit\docs\PERGUNTAS.md`).
- **`/model` para o Sonnet 5 é barrado** (o Sonnet 5.5 passa).
- **Nos projetos já migrados (com `docs\ESTADO.md`):** a abertura traz o estado curto, a fila, a caixa e o git; depois
  de um `/clear`, o `docs\PROXIMO.md`. A janela não fecha a fase sem reescrever o `ESTADO.md`, e escrita em pasta de
  dado fora das "Escritas em dado real aprovadas" do `PROXIMO.md` é barrada.

## O que continua sendo seu

- o `/effort` como comando; `max`, `xhigh`, Fable e ultracode só com motivo escrito; nunca `/omc-setup`;
- mover ou apagar pasta de projeto e mexer na raiz do `C:` (o modo automático bloqueia: o Claude entrega o comando);
- aplicar a política do safety-net quando nascer pasta de dado nova (o `instalar_kit.py` imprime o comando);
- o "sim" antes de qualquer mudança (o plano aprovado já é o "sim" do que ele pede).

## Quando algo dá errado

- **A fase falhou no mesmo ponto duas vezes:** ela anota no `ESTADO.md` e para. Você escolhe entre repetir com esforço
  maior e voltar ao `/grill-me`.
- **Aviso de troca para o Opus 5 no meio da conversa:** `/model` e escolha o Opus 5.5.
- **Duas janelas no mesmo projeto:** feche uma e rode `git status`.
- **Uma skill sumiu ou apareceu repetida:** `instalar_kit.py --verificar`, e sem o `--verificar` ele conserta.

## Leitura de apoio

A Parte 2 de `docs\2026-10-06_o-que-mudou-e-como-operar.md` explica o diagnóstico em números (a), o desenho novo (b),
o que vale quando (c) e o que continua sendo seu (d). As metas da parte (e) foram trocadas na R1: as que valem estão em
`decisoes\2026-10-06_R1-objetivo-medicao-recursos.md` §2 (atenção concentrada: perguntas de uma vez, execução longa sem
você, várias janelas).
