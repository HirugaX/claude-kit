# Os prompts das janelas da reorganização (05/10/2026)

Cada prompt vai inteiro na janela nova, aberta na pasta indicada na linha "Janela aberta em". Nenhum nome de
paciente, de funcionário ou da operadora aqui (regra do registro).

## A ordem

```
antes de tudo            FEITO em 05/10, 15:14: C:\CLAUDE apagado, as cinco pastas mudadas, as lápides criadas,
                         a memória copiada, o retrato conferido, a regra deny da pasta de dados gravada
                         (2026-10-04_execucao-reorganizacao.md)
onda 1, em paralelo      [1 desosp-censo]  ║  [2 desosp-hc]  ║  no desktop: [6 desktop · enviar a cópia]      FEITAS
onda 2, em paralelo      [3 desosp-app] (depois do "kernel pronto")  ║  [4 uso-do-claude · construir o organizar-projetos]
                         FEITAS em 05/10 (a 4 até a madrugada de 06/10)
onda 3                   [5 claude-kit · aplicar as cores no notebook] FEITA em 05/10, 23:30–00:00, pela própria janela 4
                         (2026-10-05_organizar-projetos.md, seção "Aplicado")
onda 4                   [7 desktop · organizar-projetos] (no desktop) — A PRÓXIMA
GPT                      nenhuma janela: só a mudança de pasta; o commit e o remote do conversation-core são seus, no Codex
```

- No máximo duas janelas trabalhando ao mesmo tempo no notebook (pesquisa das janelas paralelas). Em paralelo só o
  que não se cruza: repositórios diferentes, e o correio entre eles pelas caixas de sempre.
- O app espera o kernel porque lê a AT dele e testa a puxada no lugar novo. As cores esperam as três janelas porque
  pasta passageira pintada nunca se esvazia e o `fechar_rodada` da planilha apagaria os ícones.
- Próximo censo real: 07 ou 08/10. As ondas 1 e 2 vêm antes dele; as cores podem vir antes ou depois.
- O esforço gravado do Opus 5.5 estava em `xhigh` em 05/10: digite a 1ª linha de cada prompt (`/effort ...`) sempre.

---

## 1 · desosp-censo

```
Opus 5.5 · /effort high — a raiz de dados do kernel errada escreve a rodada no lugar errado sem dar erro; descobrir no censo real (07 ou 08/10) custa caro.

Janela aberta em C:\CLAUDE-PROJETOS\desosp-censo (o kernel; até 05/10 era C:\DESOSP), no notebook. Antes de tudo, confira que a mudança foi feita: esta pasta existe e C:\DESOSP é um ARQUIVO (a lápide), não uma pasta. Se não for, pare e avise o Ettore.

## Contexto
- Em 05/10 as pastas foram movidas (não reclonadas) para C:\CLAUDE-PROJETOS: desosp-censo (este), desosp-app, desosp-app-dados (os dados reais do app, antes C:\DESOSP_APP_REAL), desosp-hc (antes C:\planilha-hc) e o kit do Claude, claude-kit (antes C:\CLAUDE); o conversation-core foi para C:\GPT. Cada caminho velho virou uma lápide: programa que ainda use o caminho antigo dá erro na hora.
- Leia: C:\CLAUDE-PROJETOS\claude-kit\decisoes\2026-10-04_pastas-e-reorganizacao.md (seções 6, 7 e 10) e, em 2026-10-04_varredura-caminhos.md, a seção desosp-censo (arquivo:linha de cada caminho velho).
- A memória do Claude foi copiada para a chave nova. Confira que carregou e corrija os caminhos velhos dela (8 arquivos; lista no fim da varredura).
- Antes da mudança, a suíte deu 589 passed, 0 skipped. Depois das correções, o mesmo.

## O que fazer
1. Aceite a confiança da pasta; leia a caixa (docs\para_o_kernel) e o handoff.
2. Código e testes, com o caminho derivado da posição do código (o projeto vem de __file__; o app é o vizinho desosp-app; o override DESOSP_RAIZ continua): desosp\CONFIG_DESOSP.py, docs\guia\gerar_guia_rodada.py, docs\scripts\REF_medir_relevancia_hd.py, scripts\prova_multicenso.py, tests\test_regressoes.py (o teste das linhas 5265-5277, que fixa RAIZ == 'C:\\DESOSP', passa a conferir a derivação) e o .gitignore:14.
3. Documentos vivos: CLAUDE.md (o "rodar da raiz" e as demais linhas da varredura), .claude\rules\series-at-ak.md, .claude\skills\rodada\SKILL.md:137 (C:\CLAUDE → C:\CLAUDE-PROJETOS\claude-kit), docs\MEDICAO_RELEVANCIA_HD.md. Os históricos (HANDOFF, AT/AK/KP, INDICE, caixas) não se reescrevem.
4. ESTRUTURA.md: o caminho novo; fontes, .claude, as caixas para_* e as pastas de rodada (saida\DDMM_P), que ele não cita; a legenda das cores em C:\CLAUDE-PROJETOS\LEGENDA DAS PASTAS.html (a janela do kit vai gerar).
5. Regerar o guia em Word (docs\GUIA_DA_RODADA.docx e entrada\_GUIA_DA_RODADA.docx) e conferir que não cita C:\DESOSP.
6. Para o sistema de cores (a janela do kit aplica depois; você não aplica), escreva no handoff e no resumo: (a) as pastas que o pipeline cria e apaga sozinho (as "passageiras", como entrada\_ESPERA): elas ficarão sem cor, porque pasta com desktop.ini nunca fica vazia (arquivo_rodada.py:149); (b) todo os.listdir/iterdir/glob('*') sobre fontes, docs\para_*, saida\_extracao, saida\_revisao_02out e a raiz, com a confirmação de que um desktop.ini ali não atrapalha.
7. Suíte completa com -rs: 589 passed, 0 skipped. Depois, uma rodada de prova que não escreve em historico\ nem na rodada corrente: proponha o modo ao Ettore antes de rodar.
8. Avise o app pelo protocolo (AT nova em ..\desosp-app\docs\para_o_app\): o kernel mudou de lugar, a raiz vem da posição, nada muda no formato.
9. Commit por caminho explícito e push (git log origin/main.. antes, para ver o que vai junto).

## Limites
- Não aplique cores nem mexa em desktop.ini (é da janela claude-kit).
- Não abra nem varra C:\CLAUDE-PROJETOS\desosp-app-dados (a regra deny do settings já barra a leitura e a edição).
- Nome de paciente, de funcionário e da operadora nunca entram em arquivo versionado nem no resumo.

## Ao fechar
Resumo curto: o que mudou, a suíte (números), a rodada de prova (comando e resultado), as listas do passo 6, o que ficou pendente (como pergunta, com a recomendação) e a linha "Sinais de insuficiência do modelo: nenhum" (ou quais, com o exemplo). Diga "kernel pronto": é o sinal para a janela do app.
```

## 2 · desosp-hc

```
Opus 5.5 · /effort high — o fechar_rodada arquiva e apaga arquivos; um erro de poda só aparece na rodada seguinte.

Janela aberta em C:\CLAUDE-PROJETOS\desosp-hc (a planilha de HC; até 05/10 era C:\planilha-hc), no notebook. Antes de tudo, confira: esta pasta existe e C:\planilha-hc é um ARQUIVO (a lápide). Se não for, pare e avise o Ettore.

## Contexto
- Em 05/10 as pastas foram movidas (não reclonadas) para C:\CLAUDE-PROJETOS: desosp-censo, desosp-app, desosp-app-dados, desosp-hc (este) e o kit do Claude, claude-kit (antes C:\CLAUDE). Cada caminho velho virou uma lápide: programa que ainda use o caminho antigo dá erro na hora.
- Leia: C:\CLAUDE-PROJETOS\claude-kit\decisoes\2026-10-04_pastas-e-reorganizacao.md (seções 2, 6, 7 e 10) e, em 2026-10-04_varredura-caminhos.md, a seção desosp-hc.
- A memória do Claude foi copiada para a chave nova; confira que carregou.
- Antes da mudança: 95 passed. Depois, o mesmo, mais os testes novos.
- O sistema de cores vai pôr desktop.ini em quase todas as pastas daqui. Hoje o scripts\fechar_rodada.py (linhas 57-71 e 105-130) trata todo arquivo de entrada, saida e trabalho (menos LEIAME.txt) como da rodada: arquiva o desktop.ini e depois o apaga, e o ícone some a cada fechamento.

## O que fazer
1. Aceite a confiança da pasta. A caixa (docs\para_a_planilha): confirmar AP-007, AP-008, KP-001, KP-002 e o INDICE, que estão sem confirmação.
2. fechar_rodada.py: deixar de arquivar e de apagar o desktop.ini (e os outros arquivos ocultos de sistema do Windows, como Thumbs.db), com teste que prova que um desktop.ini em entrada, saida e trabalho sobrevive ao fechamento e não vai para o arquivo.
3. .gitignore: desktop.ini (hoje docs\, scripts\ e tests\ o mostram como não rastreado).
4. Caminhos: CLAUDE.md, docs\09_AMBIENTE.md, docs\14_MODELO_E_ESFORCO.md (C:\CLAUDE → C:\CLAUDE-PROJETOS\claude-kit) e modelos\checklists\CHECKLIST_NOVA_VERSAO.md (linhas na varredura). O GUIA_DE_TRABALHO_COM_O_CLAUDE.docx cita C:\planilha-hc três vezes e não tem gerador: proponha ao Ettore como editar (python-docx no lugar exato, conferido no Word) antes de mexer.
5. Para o sistema de cores, escreva no resumo: as pastas que os scripts criam e apagam sozinhos (as "passageiras", que ficarão sem cor) e as varreduras com glob('*')/iterdir sobre pastas que terão desktop.ini.
6. Memória: corrigir caminhos velhos, se houver. E duas junções do teste A/B de 29/09, trabalho\testes_antes_depois\2026-09-29_08h57m05\antes\node_modules e ...\depois\node_modules, apontam para C:\planilha-hc\node_modules, que hoje é lápide (o node_modules de verdade está inteiro em desosp-hc\node_modules). Proponha ao Ettore re-apontar para o lugar novo ou apagar só as junções (cmd /c rmdir, nunca rmtree, que entraria no alvo).
7. Suíte: 95 passed + os testes novos. Commit por caminho explícito e push.

## Limites
- Não aplique cores nem mexa em desktop.ini fora do fechar_rodada e do .gitignore.
- Nome de paciente, de funcionário e da operadora nunca entram em arquivo versionado nem no resumo.

## Ao fechar
Resumo curto: o que mudou, a suíte, as listas do passo 5, o que ficou pendente (como pergunta, com a recomendação) e a linha "Sinais de insuficiência do modelo: nenhum" (ou quais). Diga "planilha pronta".
```

## 3 · desosp-app (depois do "kernel pronto")

```
Opus 5.5 · /effort high — mexe em onde o app acha o dado real e nos backups do banco; um caminho errado cria um banco vazio sem dar erro.

Janela aberta em C:\CLAUDE-PROJETOS\desosp-app (o app; até 05/10 era C:\DESOSP_APP), no notebook. Só comece depois de a janela do kernel dizer "kernel pronto" (a AT dela chega em docs\para_o_app). Antes de tudo, confira: esta pasta existe, e C:\DESOSP_APP e C:\DESOSP_APP_REAL são ARQUIVOS (lápides). Se não forem, pare e avise o Ettore.

🛑 Não abra o app (nem pelos .bat) antes do passo 3: o iniciar_app_real.bat ainda aponta para o caminho velho.

## Contexto
- Em 05/10 as pastas foram movidas (não reclonadas) para C:\CLAUDE-PROJETOS: desosp-censo, desosp-app (este), desosp-app-dados, desosp-hc e o kit do Claude, claude-kit. Cada caminho velho virou uma lápide.
- Os dados reais do app agora moram em C:\CLAUDE-PROJETOS\desosp-app-dados: vizinha deste repositório, fora de todo git, nunca no GitHub. O app a acha como "a vizinha com o meu nome + -dados". O Ettore nunca abre sessão nela; tudo se faz por aqui. O Claude não lê nem edita arquivos lá: há uma regra deny no settings do Claude Code (Read e Edit em //c/CLAUDE-PROJETOS/desosp-app-dados/**), gravada em 05/10. Ela não afeta o app rodando, o código, os commits nem o GitHub. Para listar, use PowerShell (Get-ChildItem), sem abrir conteúdo de paciente; se precisar mesmo ler algo de lá, peça ao Ettore.
- Leia: C:\CLAUDE-PROJETOS\claude-kit\decisoes\2026-10-04_pastas-e-reorganizacao.md (seções 6, 7 e 10) e, em 2026-10-04_varredura-caminhos.md, a seção desosp-app.
- A memória do Claude foi copiada para a chave nova; confira que carregou.
- Antes da mudança, a suíte deu 718 passed, 1 failed, 1 skipped. O pulado é tests\test_catalogos.py:99 (molde de HC não versionado). A falha é anterior à mudança: tests\test_varredura.py:140, a varredura de nome de paciente em arquivo versionado, achou 72 ocorrências no nível D (A, B e C deram 0), todas em tests\ (_fabrica.py, test_deteccao.py, test_diff_relatorios_painel.py, test_altas_confirmar.py).

## O que fazer
1. PRIMEIRO, antes de qualquer push: a falha da varredura. Confira cada achado do nível D sem copiar nome nenhum para o chat. É nome fictício da fábrica que coincide com trecho de nome real (como em 29/09, FG-B)? Troque por palavra inventada que o universo não tem. É nome de paciente de verdade num arquivo versionado? Pare e avise o Ettore: o repositório está no GitHub.
2. Recriar o .venv (o velho embute C:\DESOSP_APP\.venv) e conferir que a suíte roda com ele.
3. A pasta de dados: app\config.py (PADRAO_KERNEL = o vizinho desosp-censo; PADRAO_REAL = o vizinho <nome>-dados; os dois derivados da posição do código; os overrides DESOSP_KERNEL, DESOSP_RAIZ e TERMINAL continuam); _areas_de_teste, _e_do_kernel, _e_dado_real e estado_da_raiz comparando por partes do caminho, nunca startswith ("desosp-app" é prefixo de "desosp-app-dados"); iniciar_app_real.bat sem caminho fixo; iniciar.py, puxar.py, exportar.py, comparador.py, anotacoes.py, db\models.py, web\rotas.py, templates\ajuda.html, scripts\paletas_escolhas.py; e os testes da varredura (test_config, test_exportar, test_puxar, test_raiz_real, test_iniciar, test_revisao_f2, test_rodada_ponta_a_ponta, _fabrica.py, varredura_nomes.py). Um teste com exatamente os nomes desosp-app e desosp-app-dados.
4. Os backups do banco moram dentro da pasta do banco (desosp-app-dados\_backups): um problema na pasta leva os dois. Proponha ao Ettore um destino fora dela (nunca no GitHub nem no OneDrive) e, aprovado, mude o código e mostre no app onde estão os backups e quando foi o último. Avise a janela do kit do destino (ele entra no mapa das cores e, se for fora da pasta de dados, talvez na regra deny).
5. Aposentar scripts\icones_pastas.py e docs\LEGENDA_CORES_PASTAS.md: os dois passam a apontar para o manual novo, C:\CLAUDE-PROJETOS\LEGENDA DAS PASTAS.html (a janela do kit gera). Não rode o --remover: a janela do kit troca os ícones.
6. Documentos vivos com caminho velho (lista na varredura): corrigir. Os históricos, não.
7. O banco tem caminhos absolutos gravados (insumo.caminho, mensagem.caminho, execucao.pasta e censo_xlsx, puxada.origem e destino; e o _RAIZ_REAL.json diz origem C:\DESOSP). Diga ao Ettore o que eles fazem (parecem só auditoria); não reescreva dado sem ele.
8. Para o sistema de cores, escreva no resumo: as pastas passageiras (ficarão sem cor) e as varreduras com glob('*')/iterdir sobre pastas que terão desktop.ini (o puxar.py:200 entra no hash da rodada: confirme que só pastas de rodada são lidas assim; elas nunca terão ícone).
9. Suíte com -rs: 719 passed e 1 skipped (o pulado de sempre), com DESOSP_KERNEL no lugar novo (o test_rodada_ponta_a_ponta não pode pular por "não há censo real"). A puxada testada em workspace_dev, sem tocar no dado real. Depois, abrir o app pelo .bat com o Ettore olhando.
10. AK ao kernel pelo protocolo. Commit por caminho explícito e push, só depois do passo 1.

## Limites
- Não aplique cores nem mexa em desktop.ini.
- Os dados do app estão quatro rodadas atrás do kernel (última puxada em 28/09): a puxada de verdade é do Ettore, pelo app, depois desta janela.
- Nome de paciente, de funcionário e da operadora nunca entram em arquivo versionado nem no resumo.

## Ao fechar
Resumo curto: o que mudou, o resultado do passo 1, a suíte, o destino dos backups, as listas do passo 8, o que ficou pendente (como pergunta, com a recomendação) e a linha "Sinais de insuficiência do modelo: nenhum" (ou quais). Diga "app pronto".
```

## 4 · uso-do-claude · construir o organizar-projetos (onda 2)

```
Opus 5.5 · /effort high — o módulo vai mover projetos e publicar código em outros PCs, e o gancho dele roda em toda sessão; erro aqui se repete em cada máquina.

Janela aberta em C:\CLAUDE-PROJETOS\claude-kit (o kit do Claude), no notebook. Pode rodar ao mesmo tempo que a janela do app (não se cruzam). Nesta janela nada se aplica nos projetos e o gancho não se liga.

## Contexto
- A decisão: decisoes\2026-10-05_organizar-projetos.md. O fluxo inteiro da reorganização de 04-05/10 vira o módulo organizar-projetos DENTRO da skill uso-do-claude (pasta skills\uso-do-claude\organizar-projetos\), com o sistema de cores dentro dele, e com avisos para, num PC novo, aproveitar só o necessário e checar antes o que já existe (para não duplicar).
- A especificação do que já foi desenhado: decisoes\2026-10-04_plano-aprovado.md (passos 2 a 6; o "pacote das pastas" do passo 4 agora mora no módulo), decisoes\2026-10-04_pastas-e-reorganizacao.md (seções 2 a 4), decisoes\2026-10-05_icones-escolha.md e decisoes\2026-10-04_execucao-reorganizacao.md (o que aconteceu, com as lições).
- Os scripts testados na mudança de 05/10, para generalizar: %LOCALAPPDATA%\claude-mudanca-2026-10-05\ (mudanca.py: retrato, checar, mover, lápides, voltar, memória; varredura.py) e claude-kit\scripts\ligar_claude.py (com os testes em scripts\tests).
- O CLAUDE.md pessoal é hardlink (~\.claude\CLAUDE.md = claude-kit\CLAUDE.md): nunca o edite pela ferramenta Edit, que separa o hardlink (visto em 05/10). Grave no próprio arquivo e confira com fsutil hardlink list.

## O que fazer
1. O portão da paridade (o registro, seção 8: o que mora na uso-do-claude espera as duas cópias ficarem iguais). A cópia do desktop chegou em _do_desktop\ (janela 6)? Compare com _do_desktop\base_notebook_2026-10-04\kit_antes.json e junte o que for do desktop (base = base_notebook_2026-10-04) com o "sim" do Ettore. Se ainda não chegou, construa tudo em claude-kit\_obra\organizar-projetos\ e só mova para dentro da uso-do-claude depois do portão.
2. O módulo (forma proposta na decisão; você decide os detalhes): ORGANIZAR.md (as fases com portões e as lições), reaproveitar.md + scripts\inventario.py (o que o PC já tem: skills por nome e hash, ganchos no settings de usuário e de projeto, linhas do CLAUDE.md, ícones e desktop.ini com marca, scripts, pastas de projeto, kit; diz o que serve e o que duplicaria), perguntas.md (o setup de perguntas no formato do grill-me), pastas.md + scripts\pastas.py, desenho.py e gancho.py (o plano 4.1 a 4.8, com o mapa do notebook em mapa.json: o plano 4.9, as respostas de 05/10 e as pastas passageiras que as janelas do kernel, da planilha e do app listarem), github.md (publicar sempre privado, com varredura de segredo e de dado sensível antes do primeiro envio; re-registrar no GitHub Desktop com "Locate"), prompts.md (os modelos das janelas de projeto, a partir deste arquivo), scripts\mudanca.py e varredura.py generalizados (lendo o plano de um arquivo, sem caminho fixo), icones\ (os quadros PNG do pacote do Ettore; o .ico se monta em cada PC). Testes para tudo (python -m pytest -q).
3. A uso-do-claude: a descrição ganha "organizar os projetos e as pastas de um PC" e uma seção curta aponta para o módulo. Só depois do portão.
4. A prévia para o Ettore: os 9 ícones finais em 16, 20, 32, 48 e 256 px, em fundo claro e escuro, e as cores da moldura do VS Code. Ele aprova antes de qualquer aplicação.
5. Não aplique nada nos projetos e não ligue o gancho: isso é da janela 5.

## Limites
- Nunca CLAUDE.md na raiz de C:\CLAUDE-PROJETOS.
- O aplicador, a conferência, o inventário e o gancho nunca seguem junção nem link (há junções velhas em desosp-hc\trabalho apontando para lápide; o os.walk do Python 3.12 entra em junção): pule toda pasta com os.path.isjunction ou islink, com teste.
- Nome de paciente, de funcionário e da operadora nunca entram em arquivo do kit nem no resumo.

## Ao fechar
Resumo curto: o módulo (arquivos, testes), o portão (fechado ou aberto), a prévia aprovada ou não, as pendências (como pergunta, com a recomendação) e a linha "Sinais de insuficiência do modelo: nenhum" (ou quais).
```

## 5 · claude-kit · aplicar as cores no notebook (depois do "pronto" de 1, 2, 3 e 4)

```
Opus 5.5 · /effort high — aplica o sistema em todas as pastas dos projetos e liga o gancho de toda sessão; erro em pasta de rodada ou no gancho aparece tarde.

Janela aberta em C:\CLAUDE-PROJETOS\claude-kit, no notebook. Só abra depois que as janelas do kernel, da planilha e do app disseram "pronto" e o módulo organizar-projetos foi construído, testado e teve a prévia aprovada.

## Contexto
- O módulo: skills\uso-do-claude\organizar-projetos\ (ORGANIZAR.md, pastas.md). A especificação: decisoes\2026-10-04_plano-aprovado.md (passos 4 e 6) e o resumo da janela 4.
- As suítes antes das cores: kernel 589, planilha 95 + os testes novos, app 719 + 1 pulado (confira os números finais nos resumos das janelas).

## O que fazer
1. Peça ao Ettore para fechar as outras janelas do Claude (o gancho é lido ao abrir a sessão, e o settings.json é gravado pelo Claude Code).
2. pastas.py instalar (os ícones em %LOCALAPPDATA%\claude-pastas\icones e o ignore global do git com desktop.ini).
3. pastas.py aplicar --ver; mostre ao Ettore o resumo (quantas pastas por verbo, em cada projeto) e aplique. Isso inclui trocar o pacote de 30/09 (na pasta, -r e +s) e preservar o desktop.ini alheio de desosp-censo\docs\gpt.
4. pastas.py vscode; instalar o Material Icon Theme e o Peacock (code --install-extension) e o workbench.iconTheme; .vscode/settings.json no .git\info\exclude de cada repositório.
5. pastas.py legenda → C:\CLAUDE-PROJETOS\LEGENDA DAS PASTAS.html.
6. pastas.py ligar-gancho. Teste numa sessão nova (claude -p): uma pasta nova dentro de um projeto ganha o verbo sem nada impresso; uma na raiz de um projeto gera a pergunta. Meça o p95 (< 150 ms).
7. pastas.py conferir = 0; git check-ignore -v desktop.ini nos três repositórios; as três suítes de novo, já com as cores; o Ettore olha o Explorador (ícone, dica, coluna Comentários) e o VS Code.
8. Limpeza, com o "sim" do Ettore: %LOCALAPPDATA%\DESOSP\icones_pastas (quando a conferência não achar nenhum desktop.ini apontando para lá), a pasta prototipos-icones e %LOCALAPPDATA%\claude-mudanca-2026-10-05 (depois que as janelas de projeto terminaram; ali estão os retratos com nomes de arquivo).
9. As lápides de C:\ saem quando a varredura de cada projeto der zero (é um arquivo de administrador: entregue o comando ao Ettore).

## Limites
- Nunca desktop.ini em pasta de rodada nem em pasta passageira; nunca seguir junção.
- Nome de paciente, de funcionário e da operadora nunca entram em arquivo do kit nem no resumo.

## Ao fechar
Resumo curto: o que foi aplicado (números por projeto), a conferência, as suítes, o que ficou pendente (como pergunta, com a recomendação) e a linha "Sinais de insuficiência do modelo: nenhum" (ou quais).
```

## 6 · desktop · enviar a cópia (no desktop, já na onda 1)

```
Sonnet 5.5 (escolha-o na lista do /model; o atalho "sonnet" abre o Sonnet 5) · /effort medium — é cópia de arquivos com conferência por hash; o erro aparece na hora.

Janela no DESKTOP (o PC do app financeiro), aberta em qualquer pasta que não seja de projeto. Não muda nada no desktop: só copia para o pendrive.

## O que fazer
1. Pergunte ao Ettore e anote, em uma linha cada: o que a janela da uso-do-claude concluiu aqui (Partes 0 a 2: as skills nos dois PCs, a compactação programada, as janelas paralelas) e se ela mudou arquivos das skills ou do CLAUDE.md pessoal deste PC.
2. Copie para o pendrive, numa pasta claude-kit-do-desktop_AAAA-MM-DD: de %USERPROFILE%\.claude\skills\ as skills do kit (uso-do-claude, recursos-do-projeto, grill-me, grilling; não a synced), o %USERPROFILE%\.claude\CLAUDE.md e qualquer pasta de kit que a Parte 0 tenha criado (pergunte onde). Sem __pycache__.
3. Na mesma pasta: manifesto.json (caminho relativo → sha256 de cada arquivo) e LEIA-ME.txt com as respostas do passo 1.
4. Confira que todo arquivo copiado bate com o manifesto.

## Limites
- Não mude nada no desktop. Nome de paciente, de funcionário e da operadora não entram em nada.

## Ao fechar
Resumo curto e a linha "Sinais de insuficiência do modelo: nenhum" (ou quais). Peça ao Ettore para pôr a pasta do pendrive em C:\CLAUDE-PROJETOS\claude-kit\_do_desktop\ no notebook.
```

## 7 · desktop · organizar-projetos (no desktop, por último)

```
Opus 5.5 · /effort high — vai mover projetos com dados de verdade e publicar código no GitHub pela primeira vez; erro silencioso (pasta errada, dado sensível enviado) custa caro e é difícil de desfazer.

Janela no DESKTOP, aberta em C:\CLAUDE-PROJETOS (crie a pasta antes, vazia, se não existir). Nunca trabalhe de dentro de uma pasta que vai mudar de lugar. Só depois de o notebook terminar a onda 3. O Ettore traz (pelo Google Drive, ou pendrive) o zip claude-kit-do-notebook_AAAA-MM-DD.zip, feito no notebook: o claude-kit (o original do kit) sem a subpasta _do_desktop e sem os desktop.ini e .vscode, que são de cada PC, com o manifesto.json (caminho relativo → sha256) e um LEIA-ME.txt.

## Contexto
- Os arquivos do Claude estão espalhados aqui: skills copiadas em %USERPROFILE%\.claude\skills, um repositório direto na raiz do C:, arquivos de IA em pastas diferentes. Só o finance-app está no GitHub; faltam dois projetos. O objetivo é o mesmo do notebook em 04-05/10: reunir tudo em C:\CLAUDE-PROJETOS (os projetos e o kit), sem prejudicar o CLAUDE.md pessoal, preservando a identidade de cada projeto (pasta, git, CLAUDE.md, memória), pôr no GitHub os que faltam e aplicar as cores.
- O roteiro é o módulo organizar-projetos da skill uso-do-claude (skills\uso-do-claude\organizar-projetos\ORGANIZAR.md, no kit que veio do notebook). Siga as fases dele, cada uma com o "sim" do Ettore, e os avisos de aproveitar só o necessário.

## O que fazer
1. Extrair o zip para C:\CLAUDE-PROJETOS\claude-kit e conferir arquivo a arquivo com o manifesto.json do zip (sha256). Extraído de um zip baixado, todo arquivo vem com a marca da web: rode Unblock-File no claude-kit inteiro (o Python não liga, mas o Windows ignora desktop.ini e .ico marcados; os .ico se montam no PC, então não devem vir marcados de qualquer jeito).
2. Fase "reaproveitar" (inventario.py): o que este PC já tem — skills (as quatro do kit em versão de cópia, e outras), ganchos, CLAUDE.md, ícones, scripts. Mostre ao Ettore o que serve, o que duplicaria e o que fica de fora, antes de instalar qualquer coisa.
3. Ligar as skills: tire as cópias velhas de %USERPROFILE%\.claude\skills (as do kit) e rode python C:\CLAUDE-PROJETOS\claude-kit\scripts\ligar_claude.py --kit-vence. Se o Ettore usa aqui o app Claude Desktop e as skills somem do menu / com junção (problema conhecido do app), volte ao modo cópia e anote no LEIA-ME do kit. O CLAUDE.md pessoal: o do kit é o novo; junte as linhas que só existirem no deste PC (com o "sim") e ligue como hardlink; confira com fsutil hardlink list.
4. As fases seguintes do módulo: inventário (só leitura, subagente), entrevista (as perguntas do módulo, no formato do grill-me), plano (com o mapa de cada projeto e o nome novo de cada pasta), mudança (retrato, movimentos, lápides, memória; o comando é do Ettore se o modo automático bloquear), GitHub (os dois projetos que faltam, sempre privados, depois da varredura de segredo e de dado sensível; o finance-app re-registrado no GitHub Desktop com "Locate"), os prompts das janelas de cada projeto para corrigir caminhos, e as cores (pastas.py instalar, aplicar, legenda, vscode, ligar-gancho, conferir = 0), com Pillow e git instalados com o "sim" do Ettore.
5. Atenção ao repositório na raiz do C:: confira o que ele é (git -C C:\ status mostra se a raiz do disco virou repositório) antes de qualquer outra coisa, e traga ao Ettore como pergunta.

## Ajustes de 06/10 (decididos no notebook; o porquê está em decisoes\2026-10-06_entrevista-fluxo.md)
- Isolamento entre projetos (§12.4 do registro): cada projeto do desktop pertence a um domínio (financeiro, RH, acolhimento); a pasta de dado de cada um fica fora do repositório e ganha regra deny no settings.json de usuário (como desosp-app-dados no notebook); nenhum trabalho de projeto numa janela da pasta-mãe; nada pessoal em projeto de trabalho, nem o contrário.
- Folha/RH tem dado de funcionário e Acolhimento tem dado de paciente: a varredura de segredo e de dado sensível antes do primeiro envio ao GitHub não é opcional.
- Nomes de pasta: proponha na entrevista um prefixo por domínio (ex.: financeiro-, rh-, acolhimento-); o padrão final sai da rodada 3 no notebook — se ainda não saiu, pergunte ao Ettore.
- Só a consolidação, as cores e o GitHub dos dois projetos. O fluxo novo de janelas (estado curto, sessões em segundo plano, skills por projeto) e os plugins vêm depois do teste no notebook (fase F8 do plano).
- O DASH: o .claude\sessao_inicio.py apaga pastas .claude-flow e os settings desligam plugins Ruflo; leia antes de mexer (não rode) e traga ao Ettore.
- O kit ainda vai virar repositório privado no GitHub (Q6): esta é a última cópia manual. Não edite o kit aqui; anote no LEIA-ME.txt do zip, ao lado, o que mudaria, para o notebook aplicar.

## Limites
- O original do kit é o do notebook: mudança feita aqui volta para lá pela cópia, sempre comparada.
- Nunca CLAUDE.md na raiz de C:\CLAUDE-PROJETOS. Nunca reclonar: mover.
- Dado sensível nunca vai ao GitHub nem a prompt.

## Ao fechar
Resumo curto: o que mudou, o que foi ao GitHub (privado), as pendências (como pergunta, com a recomendação), os prompts entregues e a linha "Sinais de insuficiência do modelo: nenhum" (ou quais).
```
