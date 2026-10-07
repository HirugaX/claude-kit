---
name: pesquisa
description: "Antes de pesquisar ou varrer muito: biblioteca do kit, subagente, salvar."
---

# Pesquisa — biblioteca → subagente → salvar

A biblioteca é `C:\CLAUDE-PROJETOS\claude-kit\pesquisas\`, com o índice em `pesquisas\INDICE.md`. Ela existe para
nenhuma janela pagar duas vezes pela mesma pergunta. Vale para toda pesquisa na internet, leitura de documentação e
varredura grande (muitos arquivos, logs, transcrições).

## 1. Procurar

Leia o `INDICE.md` (só ele, não as pesquisas inteiras) e ache as linhas que respondem à pergunta. Achou e o "conferir
de novo depois de" não venceu: leia a conclusão daquele arquivo e use, citando o arquivo. Venceu, ou cobre só parte:
a pesquisa nova parte dela e confere só o que pode ter mudado. Pronto quando você sabe o que a biblioteca já responde e
o que falta.

## 2. Pesquisar o que falta, por subagente

O material bruto (páginas, documentação, repositórios, varreduras) fica no contexto do subagente; volta só a
conclusão. A delegação é completa, porque ele não viu a conversa: a pergunta exata; o que a biblioteca já respondeu (para
não refazer); o formato da resposta (fato → fonte com link → frase literal que o sustenta; "a documentação não diz"
quando não diz); e as marcas [A] afirmação do autor sem medição e [I] inferência. Modelo e esforço por papel (skill
`orquestrar`): leitura e extração em `sonnet`, julgamento em `opus`. Pergunta de literatura sem dado de paciente e de
tamanho pequeno pode usar o `/deep-research`, conferindo as fontes.

Fato que vai virar regra (de skill, de `CLAUDE.md`, de ADR) se relê na fonte pela janela principal, não só pelo resumo
do subagente: resumidor também erra (em 07/10 um resumidor afirmou uma frase que a página não tinha).

## 3. Salvar

Quem salva é a janela principal, não o subagente. Um arquivo `pesquisas\AAAA-MM-DD_assunto.md` com o cabeçalho fixo:

```
# <Assunto> (<DD/MM/AAAA>)

- **A pergunta:** <...>
- **A data:** <DD/MM/AAAA>
- **O projeto que pediu:** <projeto ou skill>
- **Conferir de novo depois de:** <data — fato de modelo, preço ou Windows envelhece em semanas>

## Conclusão em poucas linhas
## <o corpo: tabelas, por item>
## Fontes (lidas em <data>)
```

E uma linha no `INDICE.md`, no formato da tabela de lá (data, arquivo, pergunta, projeto, conferir de novo depois de).
Numa fase que pede para não mexer no índice (F3a, F3b), grave só o arquivo; a linha entra depois.

**Nunca** na biblioteca: dado de paciente, nem trecho dos documentos da operadora (ADR-0001). A biblioteca é um dos
canais entre projetos (ADR-0002): o que vai para ela tem de servir a qualquer projeto sem expor o de origem.
