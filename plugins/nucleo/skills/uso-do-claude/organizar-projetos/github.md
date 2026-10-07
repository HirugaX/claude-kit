# GitHub — publicar o que falta, re-registrar o que mudou de pasta

A fase 6 do [ORGANIZAR.md](ORGANIZAR.md). Publicar é ação para fora: o que vai ao GitHub pode ser copiado ou indexado
mesmo depois de apagado. Por isso: **sempre privado, sempre com a varredura antes, sempre com o "sim" do usuário.**

## Antes do primeiro envio de um repositório

1. **O arquivo de termos sensíveis**, fora do repositório e fora do kit (ex.: `%LOCALAPPDATA%\claude-termos\<projeto>.txt`),
   um termo por linha: nomes do domínio que não podem ir (de paciente, de funcionário, de cliente), identificadores. O
   usuário escreve ou aprova; o Claude nunca o copia para o chat nem para o resumo.
2. **O `.gitignore`** cobre os dados, as rodadas, o `.env`, os bancos, o `desktop.ini` e o `.vscode/settings.json` (gerado em
   cada PC). Pasta de dados de app fica **fora** do repositório (a vizinha `<app>-dados`), não só no `.gitignore`.
3. **A conferência**:
   ```
   python scripts\antes_do_github.py <repositório> --termos <arquivo de termos>
   ```
   Confere o que iria (versionados, novos que um `git add -A` pegaria e **todo o histórico**, porque o primeiro push leva
   todos os commits): segredos conhecidos, chave privada, `.env`, senha ou token com valor; os termos (mostra só
   arquivo:linha e o número do termo, nunca o texto); arquivo acima de 100 MB (o GitHub recusa) ou de 50 MB; extensões de
   dado (`.db`, `.xlsx`, `.csv`, `.pdf`...) como aviso; o remote, se já existir, tem de ser privado. Roda o `gitleaks`
   também, se estiver instalado. Sai 1 se achar problema.
4. **Achou no histórico**: não envie. Reescrever o histórico (`git filter-repo`) é decisão do usuário, com cópia de
   segurança antes; a alternativa é começar um repositório novo a partir do estado limpo.
5. **Sem problema**: o script imprime o comando, sempre `--private`:
   ```
   gh repo create <nome> --private --source "<repositório>" --remote origin --push
   ```
   Precisa do `gh` autenticado (`gh auth status`). Sem o `gh`: o usuário cria o repositório **privado** no site ou no
   GitHub Desktop ("Publish repository", com "Keep this code private" marcado) e o Claude faz o `git remote add` e o
   `git push -u origin main`.
6. **Depois**: `gh repo view <nome> --json visibility` diz `PRIVATE`; `git log origin/main..` vazio.

## Repositório que mudou de pasta

O git não guarda a pasta: mover não muda nada nele. Quem se perde são os programas que lembram o caminho:

- **GitHub Desktop**: o repositório aparece como "não encontrado". Clique nele → **Locate...** → escolha a pasta nova.
  **Nunca "Clone again"**: reclonaria um repositório vazio de tudo o que não vai ao GitHub (dados, rodadas, nomes locais),
  e com a lápide no caminho velho o clone falha de qualquer jeito.
- **VS Code**: abra a pasta nova (Arquivo → Abrir Pasta) e aceite a confiança; os recentes antigos dão erro.
- **Claude Code**: a janela nova na pasta nova pede a confiança uma vez; a memória já foi copiada para a chave nova
  (fase 5). As sessões antigas continuam listadas pela pasta velha.
- `git -C <pasta nova> status` e `git log origin/main..` conferem que nada se perdeu.

## O que nunca

- Repositório público, nem por um minuto.
- Enviar sem a conferência, ou com problema "para corrigir depois".
- Pôr o arquivo de termos dentro do repositório ou do kit.
- `git add -A` às cegas: commit por caminho explícito.
- Reclonar para "consertar" uma pasta que mudou de lugar.
