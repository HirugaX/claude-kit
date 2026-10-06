# Estado do claude-kit — 06/10/2026, fim do F1a

## Onde estamos

- **Feito:** F1a (privacidade, isolamento, o kit no git).
- **Próxima:** F1b, o kit como marketplace. O prompt está em `decisoes\2026-10-06_plano-fluxo.md`, bloco "### F1b".
- **Em paralelo:** a R0 (revisão de front) pode estar aberta no `desosp-app`; nada do kit mexe lá.

## O que existe agora

- **Repositório privado `github.com/HirugaX/claude-kit`** (ramo `main`).
  - `.githooks\pre-commit` roda `scripts\checa_kit.py --staged`.
  - `.githooks\pre-push` só aceita esse remoto.
  - `core.hooksPath` está ligado neste PC; no desktop, o NB-001 manda ligar.
  - Fora do git: `_do_desktop\`, zips, o `GUIA_DAS_SKILLS.docx` gerado, `desktop.ini`, `.vscode\` e caches.
- **ADRs:** `decisoes\adr\0001-privacidade.md` (pseudônimo `iniciais-3 dígitos` nos `desosp-`, repositório só de
  dado, Drive Restrito, conectores, `deny` interno, marcadores) e `0002-isolamento.md` (domínios, cinco camadas,
  canais).
- **`caixa\`:** séries NB e DK. A NB-001 (o desktop clona o kit em vez de usar o zip) está `enviado`.
- **O documento do Ettore:** `docs\2026-10-06_o-que-mudou-e-como-operar.docx`, com a fonte `.md` ao lado.
- **CLAUDE.md pessoal:** tem o item "Privacidade e isolamento". O hardlink foi conferido com `fsutil` em 06/10.
- **Cores:** `pesquisa-clinica` (projeto-ia; `fontes` = eu-forneco-fontes); `claude-kit\.githooks` (nao-toco),
  `caixa` (correio), `docs` (nao-toco). `pastas.py conferir` sai com 0 problemas.

## Riscos e pendências

- **Hardlink × git:** checkout, reset, pull e stash que reescrevem o `CLAUDE.md` separam o hardlink. Conferir com
  `fsutil hardlink list C:\Users\ettor\.claude\CLAUDE.md`. O F1b testa trocá-lo por um import (`@...`).
- **Lixeira:** há um 3º link do `CLAUDE.md` lá, sobra da limpeza de 06/10. Some quando ela for esvaziada; não faz
  nada.
- **O que os ADRs mandam aos projetos:** ainda não foi aplicado. Fica com o F5a, F5c, F6, F7, F3b e N2 (tabelas
  "Tarefas por fase" dos ADRs). Até lá, valem as regras antigas de cada projeto.
- **Conector do Google Drive:** ainda não está ligado no claude.ai (ADR-0001 D4). O Ettore liga quando for usar.
- **As 6 lápides do `C:`:** só depois das rodadas de 07, 08 e 09/10 (`decisoes\2026-10-05_organizar-projetos.md`).
- **O `gh`:** não está instalado. Com ele, criar repositório e PR sai pelo terminal; sem ele, pelo site.

## Como retomar

1. `git pull --ff-only` e ler este arquivo e o `caixa\INDICE.md`.
2. Abrir o F1b com o prompt do plano.
3. Antes de commit: `python scripts\checa_kit.py --tudo` (o gancho roda o `--staged`).
