# NB-002 — do notebook para o desktop · 07/10/2026

> Série NB (notebook → desktop). Gerado uma vez, não é reescrito. Regras: `caixa\LEIA-ME.md`. Substitui os passos 3 e
> 4 da NB-001: o `ligar_claude.py` saiu.

## Em uma linha

As skills do kit viraram plugins (grupos `nucleo`, `planejamento` e `engenharia`, em `plugins\`). No desktop, um
único script instala tudo: `scripts\instalar_kit.py`. Os projetos do desktop continuam como estão até o F8.

## O que o desktop faz, na ordem

1. **Feche as janelas do Claude Code** no desktop.
2. **Traga o kit:**
   - nunca clonou: `git clone https://github.com/HirugaX/claude-kit.git C:\CLAUDE-PROJETOS\claude-kit`. Se o kit do zip
     estiver nessa pasta, renomeie-o antes para `claude-kit-zip-velho`;
   - já clonou (NB-001): `git -C C:\CLAUDE-PROJETOS\claude-kit pull --ff-only`.
3. **Instale:** `python C:\CLAUDE-PROJETOS\claude-kit\scripts\instalar_kit.py`. Ele:
   - registra o marketplace do kit e liga `nucleo`, `planejamento` e os plugins de fora;
   - liga os ganchos do git;
   - tira as junções antigas de `~\.claude\skills`;
   - põe no `~\.claude\CLAUDE.md` a linha de import do CLAUDE.md do kit.
4. **Se ele listar comandos `/plugin` para colar**, é porque o `claude` não está no PATH (a extensão do VS Code usa o
   dela). Abra uma janela do Claude Code, cole os comandos um a um e rode o passo 3 de novo.
5. **Se ele avisar que o `CLAUDE.md` pessoal do desktop difere do kit**, é porque ele tem linhas que o do kit não tem.
   Elas vêm para o kit pelo notebook, numa mensagem DK. Depois, rode o passo 3 com `--claude-md-kit-vence` (ele guarda
   uma cópia em `~\.claude\backups`).
6. **A política do safety-net:** rode num terminal o comando que o script imprime no fim e confirme. É sua; o Claude
   não pode aplicá-la.
7. **O guia:** `python C:\CLAUDE-PROJETOS\claude-kit\scripts\gerar_guia_skills.py`. Ele fica fora do git e cada PC gera
   o seu.

## Como saber que deu certo

- `python scripts\instalar_kit.py --verificar` termina com "Verificação: 0 achados".
- Numa janela nova do Claude Code, `/grill-me` abre a entrevista.
- `git -C C:\CLAUDE-PROJETOS\claude-kit status` está limpo.

## O que NÃO fazer agora

- Não mexa nos projetos do desktop (DASH, Folha/RH, Acolhimento): eles entram no F8.
- Não use o `organizar-projetos` antes do F2a: ele ainda cita o `ligar_claude.py`.
- Nada de `npx skills add`: skill nova de terceiros entra pelo `scripts\atualizar_terceiros.py`, no notebook.

Depois, escreva no `INDICE.md` desta caixa: `confirmado — DD/MM — <o que ficou>`. Se algo falhou, escreva uma DK com
a saída do `--verificar`.
