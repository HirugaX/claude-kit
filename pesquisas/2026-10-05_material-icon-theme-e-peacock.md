# Material Icon Theme (customClones) e Peacock — o formato e o comportamento

- **Pergunta:** como o `material-icon-theme.folders.customClones` se escreve (campos, cor hexadecimal ou nome),
  quais ícones de pasta existem como `base`, se vale no settings do projeto, e se o Peacock aplica o `peacock.color`
  sozinho?
- **Data:** 05/10/2026
- **Projeto que pediu:** claude-kit, módulo `organizar-projetos` (o `pastas.py vscode`).
- **Fontes:**
  - https://github.com/material-extensions/vscode-material-icon-theme (README, seção "Custom Folder Icon Clones")
  - https://raw.githubusercontent.com/material-extensions/vscode-material-icon-theme/main/src/core/icons/folderIcons.ts
  - https://raw.githubusercontent.com/material-extensions/vscode-material-icon-theme/main/package.json
  - https://github.com/johnpapa/vscode-peacock (`src/extension.ts`) e a issue #459
  - Lidas por um subagente (Sonnet) com WebFetch, que resume a página: as frases não são literais conferidas.
- **Conclusão:**
  - Formato: `[{"name", "base", "color", "lightColor"?, "folderNames": [...], "rootFolderNames"?: [...]}]`. O README
    aceita qualquer `#RRGGBB` em `color` (recomenda os nomes da paleta Material, por consistência).
  - Existem como `base`: download, resource, docs, shared, src, mail, robot, secure, temp, review, include, lib,
    private, archive, input, import, log, other (o ícone `folder-X` ↔ `base: "X"`).
  - O `customClones` não declara `scope` no `package.json`; no VS Code isso quer dizer `window`, então **deve** valer
    no `.vscode/settings.json` do projeto. Inferência: conferir na primeira janela.
  - O Peacock, ao ativar, lê o `peacock.color` do workspace e escreve o `workbench.colorCustomizations` sozinho (pelo
    código, não pelo README). Em ambiente remoto já houve caso de a cor não voltar (issue #459); local, sem problema
    conhecido.
- **Conferir de novo depois de:** 05/01/2027, ou antes de mudar o `pastas.py vscode`.
