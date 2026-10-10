# Prompts — os modelos das janelas

Tirados dos prompts reais de 05/10, atualizados em 07/10 (plugins, import) (`claude-kit\decisoes\2026-10-04_prompts-das-janelas.md`). Troque o que está entre
`<>`. Todo prompt leva: **o modelo e o comando `/effort` na 1ª linha**, com o porquê; a pasta em que a janela abre; o que
ler; o que fazer, numerado; os limites; e o que o resumo de fechamento traz (com a linha "Sinais de insuficiência do
modelo"). Nenhum nome de paciente, de funcionário ou de operadora em prompt nenhum.

## A ordem

```
fase 5 (a mudança)       [janela na mãe] — o usuário roda o "mudanca.py tudo"
fase 7, em paralelo      [projeto A] ║ [projeto B]      (no máximo duas ao mesmo tempo; só o que não se cruza)
                         [projeto C] depois de A, se C lê algo de A
fase 8                   [kit · aplicar as cores] depois do "pronto" de todos
outro PC                 [outro PC · enviar a cópia] cedo; [outro PC · organizar-projetos] por último
```

## 1 · projeto · corrigir os caminhos depois da mudança

```
Opus 5.5 · /effort high — a raiz de dados errada escreve no lugar errado sem dar erro; descobrir na próxima rodada real custa caro.

Janela aberta em <mãe>\<projeto> (até <data> era <caminho velho>). Antes de tudo, confira: esta pasta existe e <caminho velho> é um ARQUIVO (a lápide), não uma pasta. Se não for, pare e avise.

## Contexto
- Em <data> as pastas foram movidas (não reclonadas) para <mãe>. Cada caminho velho virou uma lápide: programa que ainda use o caminho antigo dá erro na hora.
- Leia: <kit>\decisoes\<registro da entrevista> e, em <kit>\decisoes\<varredura>, a seção <projeto> (arquivo:linha de cada caminho velho).
- A memória do Claude foi copiada para a chave nova: confira que carregou e corrija os caminhos velhos dela.
- Antes da mudança, a suíte deu <N passed, M skipped>. Depois das correções, o mesmo.

## O que fazer
1. Aceite a confiança da pasta; leia a caixa de entrada e o handoff.
2. Código e testes, com o caminho derivado da posição do código (o projeto vem de __file__; o vizinho é <mãe>\<outro>; os overrides por variável de ambiente continuam): <lista da varredura>.
3. Documentos vivos: <lista>. Os históricos (handoff, mensagens, índices, caixas) não se reescrevem.
4. Para o sistema de cores (a janela do kit aplica; você não aplica): escreva no handoff e no resumo (a) as pastas que o programa cria e apaga sozinho (as passageiras: ficarão sem cor, porque pasta com desktop.ini nunca fica vazia) e (b) todo os.listdir/iterdir/glob('*') sobre pastas que terão desktop.ini, com a confirmação de que ele ali não atrapalha.
5. Suíte completa com -rs: o mesmo número de passados e pulados, cada pulado explicado. Depois, uma rodada de prova que não escreve em dado real: proponha o modo ao usuário antes de rodar.
6. Avise os projetos que dependem deste, pelo protocolo de caixas de vocês.
7. Commit por caminho explícito e push (git log origin/main.. antes, para ver o que vai junto).

## Limites
- Não aplique cores nem mexa em desktop.ini.
- Não abra nem varra a pasta de dados de outro projeto (a regra deny do settings já barra).
- Nome de paciente, de funcionário e da operadora nunca entram no repositório de código nem no resumo; o pseudônimo
  do paciente segue o ADR-0001 (`claude-kit\decisoes\adr\0001-privacidade.md`).

## Ao fechar
Resumo curto: o que mudou, a suíte (números), a rodada de prova, as listas do passo 4, o que ficou pendente (como pergunta, com a recomendação) e a linha "Sinais de insuficiência do modelo: nenhum" (ou quais, com o exemplo). Diga "<projeto> pronto".
```

## 2 · kit · aplicar as cores (depois do "pronto" de todos os projetos)

```
Opus 5.5 · /effort high — aplica o sistema em todas as pastas dos projetos e liga o gancho de toda sessão; erro em pasta de rodada ou no gancho aparece tarde.

Janela aberta em <mãe>\claude-kit. Só abra depois que as janelas de projeto disseram "pronto" e a prévia dos ícones foi aprovada.

## Contexto
- O roteiro: /cores-das-pastas. O módulo: plugins\nucleo\pastas\ (o mapa: mapa.json; confira as passageiras que as janelas listaram; o que faltar entra antes de aplicar).
- As suítes antes das cores: <números de cada projeto>.

## O que fazer
1. Peça ao usuário para fechar as outras janelas do Claude (as suítes paradas: a guarda do app fotografa as pastas de dado).
2. python plugins\nucleo\pastas\scripts\pastas.py instalar --lapide <cada caminho velho>.
3. pastas.py aplicar --ver; mostre o resumo (pastas por verbo em cada projeto, as provisórias) e, com o "sim", aplique.
4. pastas.py vscode; com o "sim", instale o Material Icon Theme e o Peacock e ponha o workbench.iconTheme.
5. pastas.py legenda.
6. O gancho é do plugin nucleo (já liga com ele). Numa janela nova: uma pasta nova dentro de um projeto ganha o verbo sem nada impresso; uma na raiz de um projeto gera a pergunta.
7. pastas.py conferir = 0; git check-ignore -v desktop.ini em cada repositório; as suítes de novo, já com as cores; o usuário olha o Explorador (ícone, dica, coluna Comentários) e o VS Code.
8. Limpeza (fase 9), com o "sim": o pacote de ícones velho (quando a conferência não achar ini apontando para ele), os protótipos, os retratos da mudança. As lápides saem quando a varredura de cada projeto der zero (arquivo de administrador: entregue o comando).

## Limites
- Nunca desktop.ini em pasta de rodada nem em pasta passageira; nunca seguir junção.
- Nome de paciente, de funcionário e da operadora nunca entram em arquivo do kit nem no resumo.

## Ao fechar
Resumo curto: o que foi aplicado (números por projeto), a conferência, as suítes, o que ficou pendente (como pergunta, com a recomendação) e a linha "Sinais de insuficiência do modelo: nenhum" (ou quais).
```

## 3 · outro PC · enviar a cópia (cedo; não muda nada lá) — só para PC sem git; com git, o kit viaja por `git clone`/`git pull`

```
Sonnet 5.5 (claude-sonnet-5-5) · /effort medium — é cópia de arquivos com conferência por hash; o erro aparece na hora.

Janela no <outro PC>, aberta em qualquer pasta que não seja de projeto. Não muda nada neste PC.

## O que fazer
1. Pergunte ao usuário e anote, em uma linha cada: o que mudou aqui nas skills, no CLAUDE.md pessoal e no settings.json desde a última cópia.
2. Copie, numa pasta claude-kit-do-<pc>_AAAA-MM-DD: de %USERPROFILE%\.claude\skills\ as pastas que não são a synced, o %USERPROFILE%\.claude\CLAUDE.md (se existir) e qualquer pasta de kit deste PC. Sem __pycache__.
3. Na mesma pasta: manifesto.json (caminho relativo → sha256 de cada arquivo) e LEIA-ME.txt com as respostas do passo 1.
4. Confira que todo arquivo copiado bate com o manifesto.

## Ao fechar
Resumo curto e a linha "Sinais de insuficiência do modelo: nenhum" (ou quais). Peça ao usuário para pôr a pasta em <mãe>\claude-kit\_do_<pc>\ no PC do kit original.
```

## 4 · outro PC · organizar-projetos (por último)

```
Opus 5.5 · /effort high — vai mover projetos com dados de verdade e publicar código no GitHub pela primeira vez; erro silencioso (pasta errada, dado sensível enviado) custa caro e é difícil de desfazer.

Janela no <outro PC>, aberta em <mãe> (crie a pasta antes, vazia, se não existir). Nunca trabalhe de dentro de uma pasta que vai mudar de lugar. O kit chega por git clone do repositório privado HirugaX/claude-kit em <mãe>\claude-kit.

## Contexto
- O roteiro é a skill /organizar-projetos (plugin kit; plugins\kit\skills\organizar-projetos\SKILL.md). Siga as fases, cada uma com o "sim" do usuário, e os avisos de aproveitar só o necessário (reaproveitar.md).
- <o que já se sabe deste PC: projetos, o que está no GitHub, repositório na raiz, ganchos próprios>

## O que fazer
1. git clone do kit em <mãe>\claude-kit; git log -1 igual ao do PC original.
2. Fase 0: python <kit>\plugins\nucleo\pastas\scripts\inventario.py. Mostre o que serve, o que duplicaria e o que fica de fora, antes de instalar qualquer coisa.
3. Fase 1: python <kit>\scripts\instalar_kit.py (sem o claude no PATH, ele lista os comandos /plugin para colar); as linhas do CLAUDE.md pessoal que só existirem neste PC vão ao do kit com o "sim", depois --claude-md-kit-vence; instalar_kit.py --verificar com 0 achados.
4. As fases 2 a 9 do /organizar-projetos: inventário (subagente, só leitura), entrevista (perguntas.md), plano (planos\<pc>_<data>.json e o mapa no mapa.json), mudança (o comando é do usuário se o modo automático bloquear), GitHub (github.md; sempre privado, depois do antes_do_github.py), os prompts das janelas de cada projeto, as cores (/cores-das-pastas), a limpeza. Pillow e git instalados com o "sim".
5. Se a raiz do C: for um repositório (git -C C:\ status), traga ao usuário como pergunta antes de qualquer outra coisa.

## Limites
- O kit é um só, no GitHub: mudança feita aqui vai por commit e push (git pull --ff-only antes).
- Nunca CLAUDE.md na raiz de <mãe>. Nunca reclonar: mover.
- Dado sensível nunca vai ao GitHub nem a prompt.

## Ao fechar
Resumo curto: o que mudou, o que foi ao GitHub (privado), as pendências (como pergunta, com a recomendação), os prompts entregues e a linha "Sinais de insuficiência do modelo: nenhum" (ou quais).
```
