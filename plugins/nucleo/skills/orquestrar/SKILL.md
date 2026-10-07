---
name: orquestrar
description: "Delegar e paralelizar: subagentes com modelo e esforço por papel, SDD, Workflow, várias janelas, execução largada com fila."
---

# Orquestrar

Paralelismo só paga com **decomposição real** (partes independentes, arquivos separados) ou com **material volumoso**
que não deve entrar no contexto principal. Em tarefa pequena, espalhar entre 2 a 5 agentes gastou 2,6× a 5,9× mais
entrada sem ganhar tempo (teste reproduzível). Se B depende da decisão de A, é sequência.

## 1. O roteamento (Q13, Q18)

| o trabalho | como |
|---|---|
| menos de 4 tarefas; ler, buscar, varrer, pesquisar | a própria sessão + subagentes comuns (§2) |
| um plano de 4 ou mais tarefas no mesmo código | SDD (§6), onde o plugin `sdd` está ligado |
| 4+ itens do mesmo formato, independentes, cada um conferido por comando, sem decisão do usuário no meio e sem dado de paciente | Workflow (§7) |

Nunca por Workflow: julgamento clínico, dado real, decisão do usuário. **Teto: 10 agentes** sem perguntar; acima
disso, mostre a estimativa (agentes, tokens, tempo, o pedaço-piloto) e espere o "sim". `ultracode` só com motivo
escrito e o "sim" (ele desliga o aviso de execução grande e o limite de simultâneos).

## 2. Os três papéis — modelo e esforço fixados em cada despacho

O subagente não viu a conversa: a delegação é completa (objetivo, arquivos, o que já se sabe, o formato da resposta, o
critério de pronto, o que ele não pode mexer). E **todo despacho leva `model` e `effort`**: esta skill pede o esforço
explicitamente, porque a documentação não diz se o subagente herda o da janela, e na semana de 29/09 1.197 chamadas do
Sonnet 5.5 rodaram em `max`, quase todas em subagentes. Num subagente próprio (`.claude/agents` ou de plugin), o campo
`effort` da definição faz o mesmo.

| papel | para quê | `model` | `effort` |
|---|---|---|---|
| **explorador** | material ruidoso: ler, buscar, varrer, documentação, logs; devolve só a conclusão | `haiku` (localizar) ou `sonnet` (resumir, extrair) | `low` (haiku não tem esforço) a `medium` |
| **especialista** | um ponto difícil que pede modelo maior que o da janela | `opus` | `high` |
| **revisor isolado** | segunda opinião genuína, sem o contexto de quem fez | `opus` | `high` |
| implementador (SDD) | tarefa mecânica bem especificada / integração entre arquivos | `sonnet` / `opus` | `medium` |
| revisor final (SDD) | a revisão do ramo inteiro | `opus` | `high` |

Mais papéis que esses, só com partes independentes em paralelo, ou com modelo ou permissão diferentes. Revisores do
mesmo modelo erram juntos: para regra crítica, varie o **método** (teste, invariante, script independente), não o número
de agentes. O Explore e o Plan não carregam o `CLAUDE.md` (o jeito barato de ler muito); os demais o carregam inteiro,
cada um. `model: sonnet` num subagente roda no Sonnet 5.5 (armadilhas: skill `uso-do-claude`).

**Cache e retomada:** o cache do subagente dura **5 minutos**, mesmo na assinatura (`subagentPromptCacheTtl: "1h"` só
se a medição semanal mostrar cache gravado alto nos subagentes). Pergunta relacionada vai ao mesmo subagente pelo
`SendMessage`, que mantém o histórico dele, em vez de abrir outro.

## 3. Os pontos que nunca andam sem o "sim" (Q10)

Escrita em dado real fora das "Escritas em dado real aprovadas" do `PROXIMO.md`; rodada real ou reprocesso não
aprovados; migração de banco ou de esquema; regra clínica nova; leitura de fonte nova; subir para Fable, `xhigh`, `max`
ou ultracode (descer, mantida a qualidade, não pede); o mesmo erro depois de 2 tentativas diferentes; decisão que não
está no `ESTADO.md`, num ADR nem nas "Decisões pré-aprovadas". Merge, push fora do fim de fase, publicar: idem.

## 4. A execução largada e a fila (Q35, Q36, Q44)

Numa fase que roda sem o usuário olhando:

1. Começa com a linha `/goal` do `PROXIMO.md`: "o portão passou, **ou** tudo o que sobra depende de
   `docs\PERGUNTAS.md`, gravado com o `ESTADO.md`" — o avaliador impede parar antes da hora.
2. Situação prevista nas "Decisões pré-aprovadas": faz o que está lá, dentro do limite, e anota no `ESTADO.md`.
   Decisão técnica de rotina: decide e anota numa linha.
3. **Dúvida que é do usuário, ou um ponto da §3: vai para a fila** (`docs\PERGUNTAS.md`, com o problema, as opções, a
   recomendação e o que depende dela) e **a fase segue com o que não depende dela**. Nunca se escolhe por ele e nunca se
   executa o ponto da §3: só se adia.
4. O mesmo erro depois de 2 tentativas diferentes estaciona **só aquela linha de trabalho** (vai para a fila com a
   saída); o resto segue.
5. **Para só quando tudo o que sobra depende da fila**: fecha pela `fechar-janela` e avisa (três casos, texto sem nome:
   `fechar-janela`, "O aviso no celular").

A fila vale onde há `docs\ESTADO.md` e os ganchos do `nucleo` que a garantem (F2b: o `PreToolUse` em `AskUserQuestion`
grava a pergunta e responde "adiada"; o `PermissionRequest` nega e enfileira; o `Stop` aceita fechar com a fila
gravada). Sem eles — projeto ainda não migrado, ou fase supervisionada —, a dúvida vai ao chat, como sempre.

## 5. Várias janelas e a sonda (Q37, Q45)

- **Tantas janelas quanto houver trabalho independente**, desde que o total de tokens fique igual ou menor que em série
  e a qualidade a mesma. Um escritor por projeto, ou por worktree (até 3 no mesmo projeto). Uma janela = um projeto.
- Antes de abrir outra janela, olhe o **% do limite de 5 h** (statusline ou `/usage`): a cota é o tanque; o paralelo só
  o esvazia antes. No limite, só uma janela retoma sozinha, e a `--bg` nem espera.
- Commit por caminho explícito; antes do push, `git log origin/main..` (o push leva o commit da outra janela).
- **A sonda**: pesquisa que serve a duas janelas roda uma vez, num subagente ou sessão própria, e **grava em arquivo**
  (`pesquisas\` ou a pasta do projeto); as janelas leem o arquivo. Mensagem entre sessões chega como turno novo e custa
  o contexto inteiro de quem recebe: o aviso de "pronto" por `SendMessage` só dentro do mesmo domínio (ADR-0002) e só
  se o F3a mostrar ganho de tempo ou de tokens; até lá, o arquivo basta.
- Acima de 3 ou 4 janelas ao mesmo tempo: uma janela coordenadora pequena, que só lança e repassa.

## 6. SDD — plano de várias tarefas no mesmo código

As 4 skills do Superpowers no plugin `sdd` (terceiros; `subagent-driven-development`, `requesting-code-review`,
`using-git-worktrees`, `finishing-a-development-branch`): um implementador novo por tarefa, em série, com revisão de
especificação e de qualidade por tarefa e uma revisão final do ramo. Ao usar:

- o plano tem um cabeçalho por tarefa, `## Task 1`, `## Task 2`… (o `task-brief` procura `Task N`);
- **modelo e esforço fixados em cada despacho**, pela tabela da §2 (sem eles, herda os da sessão);
- onde o texto dela diz `superpowers:<skill>`, aqui é `sdd:<skill>`;
- o **`docs\ESTADO.md` continua o dono do estado**; o livro-razão em `.superpowers\sdd\` é descartável (fora do git) e
  some no fim do plano;
- as paradas dela (destrutivo, segurança, efeito fora do worktree, plano quebrado) somam-se às da §3; merge e push
  seguem a Q10 (fim de fase, portão verde).

## 7. Workflow

O script que o Claude escreve (carregue a skill `workflow-authoring` antes): agentes em segundo plano, aprovação ao
lançar e **nenhuma entrada no meio**. Sem opção, cada agente herda o modelo **e o esforço** da sessão: fixe os dois em
cada `agent(prompt, {model, effort})` pela tabela da §2 (etapa mecânica em `effort: 'low'`; só a etapa de julgar ou
conferir mais alto). Rode antes um pedaço-piloto pequeno. Respeite o teto da §1.
