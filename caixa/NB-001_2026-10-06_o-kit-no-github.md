# NB-001 — do notebook para o desktop · 06/10/2026

> Série NB (notebook → desktop). Gerado uma vez, não é reescrito. Regras: `caixa\LEIA-ME.md`.

## Em uma linha

O kit agora é o repositório privado `github.com/HirugaX/claude-kit`. O desktop **clona** o kit em vez de usar o zip
`claude-kit-do-notebook_2026-10-06.zip`, que ficou velho na hora em que o git nasceu.

## O que o desktop faz, na ordem

1. Se o kit do zip já foi aberto em `C:\CLAUDE-PROJETOS\claude-kit`, renomeie a pasta para `claude-kit-zip-velho`
   (nada se apaga antes de o clone funcionar).
2. `git clone https://github.com/HirugaX/claude-kit.git C:\CLAUDE-PROJETOS\claude-kit`
3. `cd C:\CLAUDE-PROJETOS\claude-kit`, depois `git config core.hooksPath .githooks` (liga a varredura de privacidade
   antes de cada commit e a trava de envio só para o `HirugaX/claude-kit`). O `instalar_kit.py` do F1b fará isso
   sozinho.
4. `python scripts\ligar_claude.py`, que liga as skills e o CLAUDE.md pessoal até o F1b o trocar pelo
   `instalar_kit.py`.
5. `python scripts\gerar_guia_skills.py`, porque o guia em Word fica fora do git e cada PC o gera.
6. Leia `decisoes\adr\0001-privacidade.md` e `0002-isolamento.md`: as regras novas de privacidade e de isolamento
   valem nos dois PCs.

## Como saber que deu certo

- `git -C C:\CLAUDE-PROJETOS\claude-kit status` diz "nothing to commit, working tree clean".
- `fsutil hardlink list C:\Users\<usuário>\.claude\CLAUDE.md` lista também o `claude-kit\CLAUDE.md`.
- `python scripts\checa_kit.py --tudo` termina com "0 achado(s)". No desktop ele avisa "sem o checador do HC": é
  esperado, porque o dicionário de nomes só existe no notebook.

Depois, escreva no `INDICE.md` desta caixa: `confirmado — DD/MM — <o que ficou>`.
