# Ícones e cores de pasta no Windows 11 — o que existe, o que funciona, o que é bonito

- **Pergunta:** existe recurso melhor, mais bonito ou mais fácil que o `desktop.ini` com ícone próprio para
  distinguir pastas no Windows 11 (e no VS Code e no terminal)? O que funciona hoje no 25H2?
- **Data:** 04/10/2026
- **Projeto que pediu:** entrevista das cores de pasta (notebook).
- **Fontes (principais; as demais no corpo):**
  - https://learn.microsoft.com/en-us/windows/win32/shell/how-to-customize-folders-with-desktop-ini
  - https://support.microsoft.com/en-us/topic/custom-folder-icons-or-localized-folder-names-might-not-appear-after-installing-the-june-2026-windows-security-update-f105e47a-3bfb-4e64-b757-767cfcdce07a
  - https://learn.microsoft.com/en-us/windows/win32/api/shlobj_core/nf-shlobj_core-shgetsetfoldercustomsettings
  - https://github.com/material-extensions/vscode-material-icon-theme
  - https://github.com/johnpapa/vscode-peacock
  - https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#ico
- **Conclusão:** o Windows 11 não tem cor de pasta nativa; o `desktop.ini` continua sendo o único jeito de o
  Explorador mostrar a diferença. Desde a atualização de segurança de junho de 2026, o Windows ignora o
  `desktop.ini` "não confiável" (baixado, de zip baixado, de rede): os ícones têm de ser gerados em cada PC.
  A dica (InfoTip) aparece no mouse e na coluna "Comentários" do modo Detalhes. Dá para ficar mais bonito:
  versões de 20/40 px, estilo Windows 11 com emblema da fonte de ícones do sistema, ou o ícone de pasta do
  Windows recolorido. O VS Code não lê o `desktop.ini`: espelhar com Material Icon Theme (por nome de pasta)
  e Peacock (cor por janela).
- **Conferir de novo depois de:** 04/12/2026 (o Windows mudou o tratamento do `desktop.ini` duas vezes em 2026).
- **Como foi feita:** subagente Explore (Sonnet), 220 chamadas de ferramenta. O texto abaixo é o relatório
  dele, sem mudança de conteúdo. **Atenção:** a recomendação final do relatório supõe verde = minhas,
  azul = IA, laranja = ambas, porque o pedido foi escrito antes de se conhecer a legenda real — essa parte
  não vale.

---

Legenda: [V] = [VERIFICADO EM FONTE]; [I] = [INCERTO]. Data-base: 04/10/2026. Nada foi gravado em disco.

## Alerta que muda o plano portátil
Desde 09/06/2026 (KB5094126, builds 26200.8655/26100.8655, ou seja, o 25H2) o Windows 11 ignora desktop.ini
"não confiável": com Mark of the Web (baixado, ou extraído de zip baixado), vindo de WebDAV/HTTP, ou de rede
fora de Intranet/Sites Confiáveis. A pasta volta ao ícone/nome padrão. Saídas oficiais: Sites Confiáveis;
política "Allow the use of remote paths in file shortcut icons" (reduz segurança; o Home não tem editor de
política [I]); Unblock-File (`Get-ChildItem <pasta> -Recurse -Filter desktop.ini -Force | Unblock-File`).
Arquivo criado localmente não tem MotW. A MS não diz se MotW no .ico também bloqueia (a equipe de suporte MS
mandou desbloquear o .ico) [I]. Não achei reversão até set/2026. [V]
- https://support.microsoft.com/en-us/topic/custom-folder-icons-or-localized-folder-names-might-not-appear-after-installing-the-june-2026-windows-security-update-f105e47a-3bfb-4e64-b757-767cfcdce07a
- https://learn.microsoft.com/en-nz/answers/questions/5919444/the-folder-icon-is-not-changing-in-windows-11

## 1. desktop.ini no Windows 11
- Doc oficial (atualizada 03/2025): ConfirmFileOp (=0 evita o aviso "excluindo pasta do sistema"),
  IconFile+IconIndex, InfoTip; NoSharing não vale desde o Vista. Pasta precisa ser system (`attrib +s`) ou
  somente leitura; desktop.ini oculto+sistema; arquivo "em Unicode". [V]
  https://learn.microsoft.com/en-us/windows/win32/shell/how-to-customize-folders-with-desktop-ini
- IconResource não está nessa página, mas é a chave das pastas do sistema e dos guias de 2026, inclusive
  relativa (`IconResource=icone.ico,0`, .ico dentro da pasta). Absoluto quebra em cópia/backup; relativo +
  .ico na pasta resolve. [V]
  https://learn.microsoft.com/en-us/answers/questions/4173234/desktop-ini-in-download-folder ;
  https://mariacherry.tumblr.com/post/815953208571789312/guide-the-magic-of-the-desktopini-file ;
  https://learn.microsoft.com/en-us/answers/questions/ed95a6f3-ca05-4937-a0de-eccc9b00cba9/is-there-an-easy-way-to-change-ini-files-which?forum=windows-all .
  Variáveis de ambiente expandem (fonte de 2018) [I hoje]:
  https://insert-script.blogspot.com/2018/08/leaking-environment-variables-in_20.html
- Texto descritivo: InfoTip aparece na coluna "Comentários" do modo Detalhes no Win11 (testes nov/2023;
  ativar a coluna por pasta e reiniciar o Explorer). [V]
  https://www.howtogeek.com/add-comments-to-folders-windows-11/ ;
  https://www.makeuseof.com/folder-comments-windows-11-file-explorer/ .
  Tooltip ao passar o mouse: documentado pela MS, depende de "Mostrar descrição pop-up...", sem teste de
  terceiros em 25H2 [I].
- Seção [{F29F85E0-4FF9-1068-AB91-08002B27B3D9}] (Prop2=Título, Prop5=Tags, Prop6=Comentários, formato
  `31,texto`): documentada, mas nenhuma fonte confirma no Win11, e a aba Detalhes não existe para pastas. [I]
  https://learn.microsoft.com/en-us/answers/questions/4099995/add-comments-to-a-folder-in-windows-11 ;
  https://www.voidtools.com/support/everything/properties/
- LocalizedResourceName (texto simples) parou com a KB5074109 (13/01/2026) e voltou com a KB5074105 (29/01). [V]
  https://learn.microsoft.com/en-us/answers/questions/5708363/kb5074109-breaks-localizedresourcename-parsing-in
- Codificação: MS exige Unicode; o seguro é UTF-16 LE com BOM. Windows PowerShell 5.1: `-Encoding Unicode` =
  UTF-16LE com BOM; `Set-Content` padrão = ANSI e `New-Item -Value` = UTF-8 sem BOM (acento pode estragar);
  .ps1 com acento deve ser UTF-8 com BOM. [V]
  https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_character_encoding?view=powershell-7.6 ;
  https://gist.github.com/hyrious/aa87fe5c4161da438b50af84288ee873 . Um guia de 2026 diz que cirílico só
  funcionou em ANSI [I].
- Atualizar: F5; reiniciar Explorer; `ie4uinit.exe -show` (fev/2026)
  https://woshub.com/how-to-rebuild-corrupted-icon-cache-in-windows/ ; SHChangeNotify: SHCNE_UPDATEDIR
  (conteúdo da pasta mudou), SHCNE_ASSOCCHANGED (invalida cache de ícones/miniaturas)
  https://learn.microsoft.com/en-us/windows/win32/api/shlobj_core/nf-shlobj_core-shchangenotify . A API
  oficial SHGetSetFolderCustomSettings (FCSM_ICONFILE/FCSM_INFOTIP) grava o desktop.ini sozinha ("pode ser
  alterada ou indisponível"); chamável por PowerShell Add-Type, sem instalar nada. [V]
  https://learn.microsoft.com/en-us/windows/win32/api/shlobj_core/nf-shlobj_core-shgetsetfoldercustomsettings
- Efeitos: OneDrive não sincroniza desktop.ini, então o ícone não viaja por OneDrive [V]
  https://support.microsoft.com/en-us/office/restrictions-and-limitations-in-onedrive-and-sharepoint-64883a5d-228e-48f5-b3d2-eb39e07630fa .
  Git: aparece como não rastreado; usar .git/info/exclude ou core.excludesFile global [V]
  https://git-scm.com/docs/gitignore . Zip: "Enviar para zip" estraga o efeito (guia mai/2026); o Explorer
  propaga MotW ao extrair zip baixado, 7-Zip só se ativado [V]
  https://www.bleepingcomputer.com/news/microsoft/7-zip-now-supports-windows-mark-of-the-web-security-feature/ .
  Copiar/mover preservando os atributos da pasta: sem fonte [I].

## 2. Cor nativa de pasta: não existe para pastas locais
- MS Q&A (set/2025): não há recurso nativo de cor. [V]
  https://learn.microsoft.com/en-us/answers/questions/5551665/color-coding-files-in-windows-11
- PowerToys: pedidos #40932 (ago/2025), #45718 (fev/2026), #48501 (jun/2026) fechados como duplicado ou
  "abra no Feedback Hub". [V] https://github.com/microsoft/PowerToys/issues/45718 . Builds Insider de
  set-out/2026 (26220.9568, 28020.3142): a busca não mostrou recurso de cor [I, ausência de evidência].
- Única exceção: OneDrive > "Folder color" (menu de contexto), só para pastas dentro do OneDrive; lançado
  set/2024 para contas corporativas; contas pessoais com relatos conflitantes e a opção sumindo em 2026. [I]
  https://www.windowslatest.com/2024/09/19/upcoming-onedrives-colored-folders-in-windows-11-file-explorer-for-microsoft-365-business/ ;
  https://learn.microsoft.com/en-gb/answers/questions/5906536/one-drive-stopped-allowing-color-changes-to-folder

## 3. Ferramentas prontas
Quase todas gravam desktop.ini, então o resultado sobrevive sem o programa; só Rainbow Folders e Folcolor
declaram isso [I para as demais].
- Folder Marker (ArcticLine): Free (só uso doméstico, 23 ícones, 10 próprios, altera data da pasta, sem CLI)
  e Pro US$34,95 (148 ícones, CLI/script). Sem adware relatado (Softpedia/UpdateStar). Visual clássico [I].
  https://foldermarker.com/en/11-differences-in-free-and-pro/ ; https://foldermarker.com/en/folder-marker-pro/ [V]
- FolderPainter (Sordum): freeware portátil (v1.3, jan/2021), CLI existe (sintaxe não documentada na
  página), 21 pacotes/294 ícones, opção "Copy icon while in folder" para levar entre PCs; winget
  `sordum.FolderPainter`. [V] https://www.sordum.org/10124/folder-painter-v1-3/ ;
  https://www.wingetly.io/apps/sordum/folder-painter
- CustomFolder (GDZ): grátis, proprietário, portátil, .NET 8, v4.0.3, Win10/11; 16,7 mi de cores + até 9
  emblemas por ícone (único pronto com cor+símbolo); CLI não documentado [I]. https://gdzsoft.com/ [V]
- Folder Colorizer 2 (Softorino): pago (teste de 24 h, assinatura Universal License); queixas de
  licenciamento, sem adware achado; não diz se as cores persistem após expirar [I].
  https://softorino.com/store/foldercolorizer2
- Rainbow Folders: freeware v2.05 de 2008, usa desktop.ini, visual antigo, sem CLI; evitar.
  https://www.snapfiles.com/get/rainbowfolders.html . Folcolor: MIT, exe único <1 MB, 14 cores Material,
  desktop.ini, sem CLI, não Fluent. https://github.com/kweatherman/Folcolor [V]
- GitHub com CLI: weiwei84530/folder-color (MIT, Python+Pillow+NumPy, `apply/reset/list`, 16 cores, preserva
  o gradiente Fluent do ícone do Windows, usa SHGetSetFolderCustomSettings+SHChangeNotify, caminho absoluto;
  0 estrelas/4 commits = imaturo) https://github.com/weiwei84530/folder-color ; FolderIkon (MIT,
  `folderikon -i img -d pasta`, só 256 px) https://github.com/demberto/FolderIkon . No winget só achei o
  Sordum; Folder Marker Free está no Chocolatey (v4.4, 2020). [V]

## 4. Ícones Fluent e geração por script
- Folder11 (+2.000 estrelas; SVG com variantes para 16/20/24/32): licença "só uso pessoal" (não é livre,
  serve ao uso pessoal). https://github.com/icon11-community/Folder11 . Nico0302/windows-11-folder-icons:
  template Affinity, PNGs em 16/20/24/32/40/48/64/256 e comando ImageMagick para ICO; sem licença declarada.
  https://github.com/Nico0302/windows-11-folder-icons [V]
- MIT: Fluent UI System Icons (a pasta só tem filled/regular, monocromática; serve de emblema) e Fluent Emoji
  "File folder" (Color/Flat/3D). https://github.com/microsoft/fluentui-emoji [V]. A fonte Segoe Fluent Icons
  já vem no Win11 (glifo Robot E99A; tamanhos 16/20/24/32/40/48/64): dá para desenhar o emblema no Pillow sem
  baixar nada; licença de redistribuir o resultado [I].
  https://learn.microsoft.com/en-us/windows/apps/design/style/segoe-fluent-icons-font
- Pillow grava ICO multi-tamanho (`sizes=`; `append_images=` desde 8.1.0 para versões desenhadas por tamanho;
  `bitmap_format` desde 8.3.0). O padrão NÃO inclui 20 nem 40, e tamanhos maiores que a imagem-base são
  descartados: desenhe em 256 e passe a lista completa. [V]
  https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#ico . ICO aceita frames PNG desde o
  Vista. [V] https://en.wikipedia.org/wiki/ICO_(file_format)
- Projeto que desenhe a pasta Win11 do zero com emblema: não achei. Mais próximos: folder-color (hue-shift do
  ícone Fluent, 7 tamanhos sem 20/40, sem emblema) e winlabeler (ImageMagick, protótipo, MIT)
  https://github.com/moxwel/winlabeler . Sem Python: System.Drawing do PowerShell + escrever o contêiner ICO
  (inferência, sem fonte) [I]. Testar a abertura no Explorer (houve bug antigo de .ico do Pillow sem
  miniatura no Win10, fechado) https://github.com/python-pillow/Pillow/issues/3773

## 5. Alternativas ao ícone
- Files (files-community): tags em arquivos e pastas, guardadas em fluxos alternativos NTFS (só NTFS; nem
  toda nuvem); tags personalizadas têm cor; a doc não diz que o Explorer as exiba [I]. MIT+MPL; Store paga,
  instalador clássico grátis. É outro gerenciador de arquivos (muda o hábito).
  https://files.community/docs/features/tags ; https://github.com/files-community/files [V]
- Directory Opus: rótulos (Azul, Verde, Laranja, Roxo, Vermelho) guardados em NTFS e acompanham o item;
  regras por curinga/regex/caminho completo (cor automática por nome); só aparecem no Opus; pago (~US$68,
  fonte de revendedor [I]). https://docs.dopus.com/doku.php?id=file_operations%3Alabels ;
  https://docs.dopus.com/doku.php?id=preferences%3Apreferences_categories%3Alabels%3Alabel_assignments [V]
- Emoji/prefixo no nome: NTFS aceita Unicode (https://learn.microsoft.com/en-us/windows/win32/fileio/naming-a-file)
  [V], mas o caminho muda para sempre; git cita caminhos não-ASCII (core.quotePath=false desfaz)
  https://git-scm.com/docs/git-config [V]; .bat sem `chcp 65001`, .ps1 sem BOM e ferramentas antigas podem
  errar [I].
- Acesso rápido/Início: o item fixado mostra o ícone da pasta de destino (não aceita ícone próprio) [V]
  https://learn.microsoft.com/en-us/answers/questions/3901460/how-to-change-icons-for-shortcuts-pinned-to-quick ;
  não oferece cor.

## 6. VS Code
- Material Icon Theme v5.39.0 (28/09/2026). customClones surgiu na v5.2.0 (9/maio/2024, PR #2305). [V]
  https://github.com/material-extensions/vscode-material-icon-theme/releases/tag/v5.2.0 ;
  https://marketplace.visualstudio.com/items?itemName=PKief.material-icon-theme

```json
"material-icon-theme.folders.associations": { "minhaPasta": "src" },
"material-icon-theme.folders.color": "#ef5350",
"material-icon-theme.folders.customClones": [ { "name": "users-admin", "base": "admin", "color": "light-green-500", "lightColor": "light-green-700", "folderNames": ["users"], "rootFolderNames": ["users"] } ]
```

  (README oficial: https://github.com/material-extensions/vscode-material-icon-theme [V]). associations =
  nome da pasta -> ícone existente; folders.color = um único tom para as pastas padrão; customClones.color
  aceita #RRGGBB ou alias da paleta; casa por NOME da pasta, não por caminho. Bug aberto #3169 (v5.26.0)
  deixava ícones de pasta em branco com customClones (pode estar corrigido) [I]. O manifesto não define
  "scope", logo vale em Usuário e Workspace (.vscode/settings.json) [I]; só SVG personalizado exige Usuário
  [V]. A v5.26.0 já trouxe ícones do Claude Code (changelog) [V].
- Peacock: grava `peacock.color` e `workbench.colorCustomizations` em .vscode/settings.json (cor por
  projeto); favoritas em `peacock.favoriteColors`. [V]
  https://github.com/johnpapa/vscode-peacock/blob/main/docs/guide/README.md
- Mostrar o ícone do desktop.ini no VS Code: não; os ícones vêm só do tema (folderNames, sem curingas). [V]
  https://code.visualstudio.com/api/extension-guides/file-icon-theme (não achei pedido de recurso [I])

## 7. Terminal
- Windows Terminal: `"tabColor": "#rrggbb"` no perfil. [V]
  https://learn.microsoft.com/en-us/windows/terminal/customize-settings/profile-appearance
- oh-my-posh: segmento `text` com `{{ if glob "CLAUDE.md" }}[IA]{{ end }}` (função glob documentada)
  https://ohmyposh.dev/docs/configuration/templates ; há segmento oficial do Claude Code
  (`"statusLine": {"type":"command","command":"oh-my-posh claude"}`)
  https://ohmyposh.dev/blog/oh-my-posh-claude-code-integration [V]
- Starship: `[custom.ia] detect_files=["CLAUDE.md"] detect_folders=[".claude"] symbol="[IA] " style="bold blue"`;
  mostra se detectar, mesmo sem comando (código-fonte). [V]
  https://raw.githubusercontent.com/starship/starship/master/src/modules/custom.rs

## O que o subagente recomendaria e por quê
(Lembrete: o sentido das cores abaixo NÃO é a legenda real.) Manter o desktop.ini (não há nada nativo
melhor: Windows 11 não tem cor de pasta), mas gerado por UM script PowerShell rodado em cada computador,
nunca por ícones baixados ou levados por zip/OneDrive. O script cria (ou copia de uma pasta central e faz
Unblock-File) três .ico multi-tamanho (verde = minhas, azul = IA, laranja = ambas, cada um com
emblema/letra para não depender só de cor), coloca o .ico dentro da pasta, grava o desktop.ini em UTF-16 LE
com BOM com IconResource relativo + InfoTip com a legenda ("AZUL = IA usa/cria aqui"), aplica attrib (+r na
pasta; +s +h nos arquivos), avisa o shell (SHChangeNotify) e inclui desktop.ini e o .ico no
.git/info/exclude. Motivos: a MS endureceu em jun/2026 exatamente o caso baixado/zip/rede; OneDrive e zip
não levam o desktop.ini; e criar localmente é o caminho que a MS trata como confiável. A coluna Comentários
permite ordenar por categoria sem depender de cor. Detecção automática: pasta com CLAUDE.md ou .claude vira
azul; "ambas" é manual. Para ficar bonito: Folder11 (uso pessoal) ou hue-shift do ícone Fluent
(folder-color) mais emblema da fonte Segoe Fluent Icons. Se quiser interface gráfica sem instalar:
CustomFolder (portátil, emblemas) ou FolderPainter (portátil, winget). Evitar Rainbow Folders (2008) e Folder
Colorizer (assinatura). Espelhar a mesma legenda no VS Code (customClones + Peacock) e no Windows Terminal
(tabColor + segmento CLAUDE.md), porque eles não leem desktop.ini.

## Complemento — fatos do notebook (04/10/2026, mesma janela)
- Escala da tela: 125% (`AppliedDPI = 120`; tela lógica 1536×864). Os ícones pequenos (painel lateral, modo
  Detalhes) saem com 20 px — e o pacote de 30/09 não tem a versão de 20.
- A opção "Mostrar descrição pop-up" está ligada (`ShowInfoTip = 1`), e o Ettore confirmou que a dica aparece
  ao passar o mouse.
- O Python global tem Pillow. O VS Code tem 19 extensões, nenhuma de tema de ícones nem o Peacock.
- O teste do atributo da pasta ("somente leitura" × "sistema") está em
  [2026-10-04_pacote-icones-pastas-30-09.md](2026-10-04_pacote-icones-pastas-30-09.md), no complemento: use
  "sistema" (`attrib +s`), não "somente leitura" — a recomendação acima de `+r` na pasta não vale.
