# Registro da entrevista — cores de pasta, biblioteca de pesquisas e reorganização (04/10/2026)

- **O que é:** a especificação aprovada pelo Ettore no fim da entrevista (`/grill-me`) de 04/10/2026, feita
  numa janela aberta em `C:\DESOSP`, no notebook (Opus 5.5). Pergunta final (Q25): "sim". O que está decidido
  aqui não se rediscute; o que ficou aberto está na seção 9.
- **Fatos de apoio:** a biblioteca `C:\CLAUDE\pesquisas\` (seis arquivos de 04/10; comece pelo `INDICE.md`).
- **Regra que vale para tudo:** nenhuma alteração sem antes mostrar no chat o que foi verificado e o que muda,
  e esperar o "sim" (CLAUDE.md pessoal, linha de 04/10). Um plano aprovado é o "sim" dos passos dele.

## 1. Vocabulário (Ettore, 04/10)
- **notebook** = este computador: os projetos DESOSP e o kit do Claude. **desktop** = o outro computador, com
  o app financeiro (Claude Code 2.1.289, Python instalado, skills instaladas como pastas copiadas).
- Nomes novos das pastas (seção 6): `desosp-censo` (o kernel, hoje `C:\DESOSP`), `desosp-app`
  (`C:\DESOSP_APP`), `desosp-app-dados` (`C:\DESOSP_APP_REAL`), `desosp-hc` (a planilha, `C:\planilha-hc`).
- "Kit" é o que hoje está em `C:\CLAUDE`: skills, scripts, CLAUDE.md pessoal, `fontes`, `pesquisas`, `decisoes`.

## 2. O sistema de cores — a pasta diz "o que eu faço com ela"
Mantido o sentido da legenda de 30/09 (Q6), refinado pelo uso real (Q3, Q18):

| verbo | o que significa para o Ettore | exemplos (hoje) |
|---|---|---|
| **Eu alimento** | deposito os arquivos de cada rodada; o programa os consome e arquiva | `entrada` do kernel e da planilha |
| **Eu forneço fontes** | trago documento de referência; a IA consulta; ninguém altera | `fontes` do kernel; `docs\fontes` do app; `fontes` do kit |
| **Eu leio** | o programa ou o Claude produz para mim; abro e copio; posso apagar rodada velha | `arquivo` do kernel; `docs\gpt`; `saida` e `planilhas` da planilha; `pesquisas` do kit |
| **Trabalhamos juntos** | o programa escreve e eu também edito à mão | `saida` do kernel (Base Censo); `historico` do kernel |
| **Não toco** | é do Claude: código, testes, rascunhos, `docs` técnicos e o correio entre janelas (com envelope no desenho grande) | `desosp`, `app`, `scripts`, `tests`, `.claude`, `trabalho`, `workspace_dev`, `docs`, as caixas `para_*`, `skills` |

Marcas:
- **Projeto com IA** — na raiz de cada projeto: "aqui a IA trabalha; dentro, siga as cores".
- **Dado real / sem cópia** — a pasta inteira em vermelho (Q18 iii): `desosp-app-dados` (o banco do app),
  `historico` do kernel (sem backup), `privado` da planilha (senha). O vermelho não passa às filhas: dentro de
  uma pasta vermelha, as filhas recebem "Não toco".
- **Criada pela IA — falta classificar** — provisória, só para pasta nova fora dos escopos (seção 3).

Regras:
- "Eu forneço fontes" é separado de "Eu alimento" (Q18 i); o correio entre janelas fica em "Não toco" (Q18 ii).
- O `docs` passa a "Não toco"; o `docs\gpt` fica em "Eu leio" (Q18 iv).
- Os textos da legenda de 30/09 são corrigidos: o laranja deixa de citar os `EVOL_` (quem os cria é o Claude)
  e passa a citar o `BRUTO_` e o PDF da UTI; o verde deixa de dizer "não apague" onde o Ettore apaga ou edita.
- Nunca recebem cor: as pastas de rodada (`saida\DDMM_P` e as de `arquivo\`), `.git`, `__pycache__`,
  `.pytest_cache`, `node_modules`, `.venv`, pastas temporárias e tudo em `C:\GPT`.
- Ícones intuitivos: o Ettore pediu esse cuidado de forma explícita (Q18).

## 3. A regra da pasta nova (Q11, Q12)
- Cada projeto é marcado **uma vez, por inteiro**, quando entra no sistema. O **mapa completo** de cada projeto
  (toda pasta com o seu verbo, e as exceções) é proposto no plano e aprovado de uma vez: "todas as situações
  desenhadas agora, para não haver mais decisões" (Ettore).
- Depois disso, um **gancho** do Claude Code (no settings de usuário, nos dois PCs) **só age quando nasce uma
  pasta**: sem pasta nova, não faz nada e não gasta token. A pasta nova **herda o verbo da mãe**, salvo
  exceção escrita no mapa.
- **Pergunta só fora dos escopos** (pasta nova na raiz de um projeto, ou fora de projeto): a pasta ganha a
  marca provisória e o Claude pergunta a cor no chat.
- Um comando de **conferência** acha o que escapou: pasta criada pelo pipeline, vinda da nuvem ou feita à mão.

## 4. Onde mora, como se gera, como se vê
- **Pacote:** dentro da skill `uso-do-claude`, num arquivo próprio (por exemplo `pastas.md`) com uma subpasta
  de scripts; o `SKILL.md` dela ganha só uma linha apontando para ele (Q10 a). A implementação espera as duas
  cópias da `uso-do-claude` (notebook e desktop) ficarem iguais (seção 8).
- **Linguagem:** Python nos dois PCs (o desktop tem Python — Ettore, 04/10), com teste automático.
- **Ícones gerados em cada PC**, nunca levados prontos por zip ou download: desde a atualização de segurança de
  junho de 2026, o Windows ignora `desktop.ini` com marca da web.
- **Tamanhos:** 16, 20, 24, 32, 40, 48, 64 e 256 px. A tela do notebook está em 125%: o ícone pequeno sai com
  20 px, que o pacote de 30/09 não tem.
- **`desktop.ini`:** UTF-16 LE com BOM; **atributo "sistema" (`+s`) na pasta, não "somente leitura"** (o `+r`
  deixa cópias impossíveis de apagar — testado em 04/10). A dica (`InfoTip`) de toda pasta colorida termina
  com "Legenda: C:\CLAUDE-PROJETOS\LEGENDA DAS PASTAS.html".
- **Protótipos (Q13):** três estilos — (1) o desenho atual com 20/40 px; (2) pasta no estilo Windows 11 com
  emblema da fonte de ícones do próprio Windows; (3) o ícone de pasta do Windows recolorido, com emblema — em
  `C:\CLAUDE-PROJETOS\prototipos-icones\VER_PROTOTIPOS.html`. O Ettore escolhe vendo; nada é aplicado nesse
  passo.
- **Onde se vê (Q2):** no Explorador (ícone, dica do mouse, coluna "Comentários") e no VS Code: **Material Icon
  Theme** (as mesmas cores por nome de pasta, configurado por projeto) e **Peacock** (cor da moldura de cada
  janela, por projeto), nos dois PCs (Q23). No desktop, a instalação vai no prompt da janela de lá.
- **Manual (Q5, Q24):** `C:\CLAUDE-PROJETOS\LEGENDA DAS PASTAS.html`, gerado pelo script a partir da mesma
  tabela que pinta as pastas; sem atalho na Área de Trabalho. Conteúdo: os verbos, as cores e os desenhos; o
  mapa de cada projeto; a explicação da pasta de dados do app (o que é, por que existe, que não se mexe nela
  por fora do app); a pasta `C:\GPT`, fora do sistema; como aplicar num projeto ou PC novo.

## 5. A biblioteca de pesquisas (Q15, Q16)
- Hoje em `C:\CLAUDE\pesquisas\`; vai junto com o kit para o lugar novo. Um arquivo por pesquisa
  (`AAAA-MM-DD_assunto.md`) com o cabeçalho fixo, e o `INDICE.md`. Nunca dado de paciente nem trecho de
  documento da operadora.
- A regra "antes de pesquisar, procurar; depois, salvar" mora na `uso-do-claude`, com uma linha no CLAUDE.md
  pessoal — **as duas ainda não foram escritas** (entram no plano).
- A **colheita** das pesquisas antigas (documentos dos três projetos e transcrições das sessões) roda numa
  janela própria, logo. O prazo de 30 dias das transcrições **não** aumenta: elas têm dado de paciente.

## 6. A reorganização — hoje, 04/10
- **Objetivo (Ettore):** concentrar num lugar só todo o trabalho com o Claude, separado dos demais arquivos do PC.
- **Pasta-mãe: `C:\CLAUDE-PROJETOS\`** (Q19 b), para todo projeto do Claude, presente e futuro:
  `desosp-censo`, `desosp-app`, `desosp-app-dados`, `desosp-hc`.
- **`desosp-app-dados` ao lado de `desosp-app`, fora do repositório** (Q20 a): amarrada pelo nome e pelo
  lugar; nunca vai ao GitHub; nenhuma janela do Claude a abre como projeto; o app passa a achá-la como "a
  vizinha com o meu nome + `-dados`". O Ettore nunca abriu sessão nela e espera que tudo seja feito pelo
  `desosp-app`.
- **O kit sai de `C:\CLAUDE`.** O Ettore vai apagar o `C:\CLAUDE` ("deixa de ter utilidade", Q19). O conteúdo
  (skills, scripts, CLAUDE.md pessoal, `fontes`, `pesquisas`, `decisoes`) vai para dentro de
  `C:\CLAUDE-PROJETOS`; o nome da subpasta fica para o plano. 🛑 **O `C:\CLAUDE` só se apaga no fim**, depois
  de mover, religar e conferir: hoje as skills do notebook são junções para `C:\CLAUDE\skills`, e o CLAUDE.md
  pessoal é hardlink com `~\.claude\CLAUDE.md`. Apagar antes faz as skills sumirem do Claude Code. O
  `ligar_claude.py` e a linha do CLAUDE.md pessoal que diz "Tudo do Claude Code mora em `C:\CLAUDE`" mudam junto.
- **Nenhum `CLAUDE.md` na raiz de `C:\CLAUDE-PROJETOS`** sem decisão do Ettore: todos os projetos o
  carregariam (o Claude Code lê o CLAUDE.md das pastas acima do projeto).
- **`C:\conversation-core` → `C:\GPT\conversation-core`.** É um projeto do Codex com o GPT; fica fora dos
  processos do Claude e do sistema de cores.
- **`C:\DESOSP ARQUIVO` fica onde está** (Q21).
- **GitHub:** os repositórios já se chamam `desosp-censo`, `desosp-app` e `desosp-hc`; não há o que renomear lá.
- **Por que um nome novo para a mãe:** se ela se chamasse `C:\DESOSP`, todo caminho esquecido continuaria
  achando uma pasta — a errada — sem erro nenhum: o app trataria o dado real como do kernel, uma exportação
  criaria `entrada` na mãe, e uma janela aberta na mãe carregaria a memória do kernel. Com o nome novo, o
  esquecido falha na hora.
- **Antes de mover:** nenhuma janela do Claude ou do VS Code aberta dentro das pastas (inclusive a desta
  entrevista, em `C:\DESOSP`); o app desligado; PDFs fechados; nenhum processo Python segurando as pastas
  (havia um órfão, PID 21168); o kernel commitado e enviado; a janela da colheita de pesquisas (em
  `C:\CLAUDE`) terminada. No fim da entrevista o Ettore informou: nenhum projeto rodando no notebook nem no
  desktop.
- **Mover, nunca reclonar:** muita coisa só existe no disco (`entrada`, `saida`, `arquivo`, `historico` e
  `fontes` do kernel; os nomes locais, as caixas e `docs\fontes` do app; `planilhas`, `privado` e `historico`
  da planilha). A janela que move nunca fica dentro das pastas que move.
- **Depois de mover:**
  - levar a memória do Claude para as chaves novas (`~\.claude\projects\`: a do kernel tem 16 arquivos, a do
    app 6, a da planilha 3) e conferir o `~\.claude.json` (confiança e permissões por pasta);
  - recriar o `.venv` do app; registrar as pastas de novo no GitHub Desktop e no VS Code;
  - corrigir os caminhos dentro de cada projeto **pela janela daquele projeto** (prompt nomeado), preferindo
    caminho derivado da posição do código, para a próxima mudança não quebrar nada;
  - regerar o guia em Word do kernel; o guia em Word da planilha não tem gerador e cita `C:\planilha-hc`
    três vezes;
  - uma rodada de prova antes do próximo censo de verdade (07 ou 08/10);
  - só então aplicar as cores, uma vez, já na estrutura nova; e só então apagar o `C:\CLAUDE`.

## 7. Prompts que o plano entrega (cada um com o nome do projeto)
- **desosp-censo (kernel):** atualizar o `ESTRUTURA.md` (não cita `fontes`, `.claude`, as caixas `para_*`
  nem as pastas de rodada); corrigir os caminhos (`CONFIG_DESOSP.py`, o teste que fixa `C:\DESOSP`, as regras,
  o "rodar da raiz" do CLAUDE.md); regerar o guia em Word; avisar o app pelo protocolo dos dois projetos.
- **desosp-app:** amarrar a pasta de dados (`desosp-app-dados`, vizinha); tirar os backups do banco de dentro
  da pasta do banco (hoje ficam juntos: um problema na pasta leva os dois) e sinalizar isso no app; aposentar
  o `scripts\icones_pastas.py` e a `docs\LEGENDA_CORES_PASTAS.md` (apontar para o manual novo); corrigir os
  caminhos (`app\config.py`, o `.bat`, a página de ajuda, os testes); avisar o kernel pelo protocolo.
- **desosp-hc (planilha):** o `fechar_rodada.py` parar de arquivar e apagar o `desktop.ini`; pôr
  `desktop.ini` no `.gitignore`; confirmar a caixa (AP-007 e os demais não confirmados); corrigir os caminhos
  e o guia em Word.
- **desktop:** trazer o kit do notebook (o original); aplicar o sistema de cores lá, com o mapa do app
  financeiro; instalar o Material Icon Theme e o Peacock; conferir a linha nova do CLAUDE.md pessoal.
- **GPT:** nada além da mudança de pasta. O `conversation-core` tem trabalho sem commit desde 01/09 e nenhum
  remote; a decisão é do Ettore, no Codex.
- A **colheita de pesquisas** já tem prompt próprio (entregue no fechamento da entrevista).

## 8. Coordenação com o desktop
- **O original do kit é o do notebook** (Q22). A janela da `uso-do-claude` rodou no desktop (Partes 0 a 2: as
  skills nos dois PCs, a compactação programada, as janelas paralelas) sobre a cópia de lá; o que ela mudou
  volta para cá pelo caminho que a Parte 0 dela escolheu. Perguntar ao Ettore o que ela concluiu.
- A parte das pastas mora dentro da `uso-do-claude`: implementar só depois que as duas cópias estiverem iguais.
- A linha nova do CLAUDE.md pessoal (04/10) precisa chegar ao desktop.

## 9. O que ficou aberto (decide-se no plano, com o Ettore)
- O estilo visual e as cores exatas de "Eu forneço fontes", "Trabalhamos juntos" e das marcas — nos protótipos.
- O nome da subpasta do kit dentro de `C:\CLAUDE-PROJETOS`.
- O mapa completo de cada projeto, proposto a partir de `pesquisas\2026-10-04_mapa-das-pastas-e-fluxos.md`.
- Como o kit viaja entre os PCs (vem da Parte 0 da janela do desktop).
- O que roda em paralelo e o que roda em sequência (ver `pesquisas\2026-10-04_janelas-paralelas-e-tokens.md`).

## 10. Riscos encontrados em 04/10, com dono

| risco | dono |
|---|---|
| A planilha apaga os próprios ícones a cada fechamento, e o `desktop.ini` aparece como arquivo novo no git | janela da planilha |
| Pastas com "somente leitura": cópia que não se apaga (WinError 5 em 01/10, confirmado por teste em 04/10) | plano das pastas (trocar por "sistema") |
| Backups do banco do app na mesma pasta do banco | janela do app |
| Os dados do app quatro rodadas atrás do kernel (última puxada em 28/09) | o Ettore, pelo app |
| `ESTRUTURA.md` do kernel desatualizado | janela do kernel |
| Nenhum ignore global de `desktop.ini` no git: todo repositório novo o mostraria | plano das pastas |
| `conversation-core` sem commit desde 01/09 e sem remote | o Ettore, no Codex |
