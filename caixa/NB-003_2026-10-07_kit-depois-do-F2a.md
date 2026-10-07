# NB-003 — do notebook para o desktop · 07/10/2026

> Série NB (notebook → desktop). Gerado uma vez, não é reescrito. Regras: `caixa\LEIA-ME.md`. Substitui a NB-002
> (que o desktop ainda não confirmou): os passos são os mesmos, com o F2a por cima.

## Em uma linha

O F2a quebrou as skills: o `nucleo` tem agora 6 (`uso-do-claude` virou núcleo + `modelo-e-esforco`, `fechar-janela`,
`pesquisa`, `orquestrar`, `recursos-do-projeto`); nasceram os plugins `kit` (organizar projetos, cores e ícones, só
por `/`) e `sdd` (terceiros, por projeto de código). No desktop: `git pull` e o `instalar_kit.py`, uma vez.

## O que o desktop faz, na ordem

1. **Feche as janelas do Claude Code** no desktop.
2. **Traga o kit:**
   - nunca clonou: `git clone https://github.com/HirugaX/claude-kit.git C:\CLAUDE-PROJETOS\claude-kit` (um kit de zip
     nessa pasta: renomeie antes para `claude-kit-zip-velho`);
   - já clonou: `git -C C:\CLAUDE-PROJETOS\claude-kit pull --ff-only`.
3. **Instale:** `python C:\CLAUDE-PROJETOS\claude-kit\scripts\instalar_kit.py`. Além do que a NB-002 dizia (marketplace,
   `nucleo` e `planejamento` no escopo de usuário, ganchos do git, junções antigas, o import do `CLAUDE.md` pessoal), ele
   agora:
   - liga o plugin `kit` na janela da raiz (`C:\CLAUDE-PROJETOS\.claude\settings.json`, que não vaza para os projetos);
   - se o sistema de cores já estiver instalado aí (`%LOCALAPPDATA%\claude-pastas\local.json`), aponta o `"modulo"` para
     `plugins\nucleo\pastas`.
4. **Sem o `claude` no PATH**, ele lista comandos `/plugin` para colar numa janela do Claude Code; cole um a um e rode o
   passo 3 de novo. **`CLAUDE.md` pessoal diferente do kit:** as linhas que só o desktop tem vêm numa DK; depois, o
   passo 3 com `--claude-md-kit-vence`.
5. **A política do safety-net:** rode num terminal o comando que o script imprime no fim e confirme (é sua).
6. **O guia:** `python C:\CLAUDE-PROJETOS\claude-kit\scripts\gerar_guia_skills.py` (fora do git; cada PC gera o seu).

## Como saber que deu certo

- `python C:\CLAUDE-PROJETOS\claude-kit\scripts\instalar_kit.py --verificar` termina com "Verificação: 0 achados" e lista
  `nucleo (6); kit (3); planejamento (12); engenharia (14); sdd (4)`.
- Numa janela nova aberta em `C:\CLAUDE-PROJETOS`, `/organizar-projetos` aparece no menu `/`; numa pasta qualquer fora
  dali, não.
- `git -C C:\CLAUDE-PROJETOS\claude-kit status` está limpo.

## O que NÃO fazer agora

- Não mexa nos projetos do desktop (DASH, Folha/RH, Acolhimento): eles entram no F8, que usa o `/organizar-projetos`.
- Nada de `npx skills add`: skill de terceiros entra pelo `scripts\atualizar_terceiros.py`, no notebook.

Depois, escreva no `INDICE.md` desta caixa, na linha da NB-003 (e da NB-002): `confirmado — DD/MM — <o que ficou>`. Se
algo falhou, uma DK com a saída do `--verificar`.
