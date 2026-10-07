# Testar instrução numa sessão nova (`claude -p`)

Para saber se uma regra **chega** a uma sessão nova (depois de mexer no `CLAUDE.md`, numa skill ou em `.claude/rules`),
faça a pergunta numa sessão nova, uma pergunta por sessão, e compare a resposta com o texto da regra. Use o script, que
já evita os erros de 03/10:

    python C:\CLAUDE-PROJETOS\claude-kit\scripts\perguntas_controle.py perguntas.txt --projeto C:\CLAUDE-PROJETOS\<projeto>

As perguntas do núcleo do kit (as regras da `uso-do-claude` e das peças dela) estão em
`C:\CLAUDE-PROJETOS\claude-kit\scripts\perguntas_nucleo.txt`, cada uma com a resposta esperada num comentário: rode-as
depois de mudar qualquer skill do `nucleo` ou o `CLAUDE.md` pessoal.

À mão, as quatro regras abaixo; cada uma custou uma tentativa perdida em 03/10 (KN42):

1. **A pergunta vem logo depois do `-p`, antes das opções.** O `--allowedTools` aceita vários valores e engole a
   pergunta que vem depois dele.
2. **Feche o stdin**: `< /dev/null` no shell, `stdin=DEVNULL` no Python. O `-p` junta à pergunta tudo o que chega pelo
   stdin; num laço `while read`, cada sessão recebeu o resto do arquivo de perguntas.
3. **Modelo pelo ID completo** (`claude-sonnet-5-5`), nunca pelo atalho. Confira o modelo que rodou no `modelUsage` da
   saída `--output-format json`.
4. **Respostas numa pasta nova, com nome que não casa com o do arquivo de perguntas.** Um `rm q*.txt` feito para limpar
   as respostas apagou também o `qs.txt`, que era a lista de perguntas.

No Git Bash, um texto que começa com `/` vira caminho do Windows (`/doctor` virou `C:/Program Files/Git/doctor`): use
`MSYS_NO_PATHCONV=1`, ou rode pelo script.

**O que a sessão enxerga:** a 1ª linha do `--output-format stream-json --verbose` lista os plugins, as skills e os
comandos `/` daquela pasta — é o jeito de conferir que uma skill só `/` aparece onde deve (07/10).

**O custo fixo de abrir uma sessão** se mede do mesmo jeito: `claude -p "/context"` imprime a tabela (o total, as
skills, a memória); cada `claude -p` aparece também como uma sessão no
`python C:\CLAUDE-PROJETOS\claude-kit\scripts\medir_uso.py --sessoes`, com o seu `ctx0`. Para comparar duas versões de
um arquivo de instrução, troque o arquivo, rode, e devolva o original no mesmo comando, conferindo o hash.
