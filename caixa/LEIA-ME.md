# caixa — mensagens entre o notebook e o desktop (Q12, 06/10/2026)

O kit é o mesmo repositório nos dois PCs (`github.com/HirugaX/claude-kit`, privado). O que um PC precisa contar ao
outro sobre o kit, ou sobre o trabalho que atravessa os dois PCs, vem para cá, no formato das caixas dos projetos
(`docs\para_*`, ADR-0002).

## As regras

- **Duas séries:** **NB** (o notebook escreve para o desktop) e **DK** (o desktop escreve para o notebook).
- **Um arquivo por mensagem:** `NB-NNN_AAAA-MM-DD_assunto.md` (ou `DK-…`). É gerado uma vez e nunca reescrito; uma
  correção é uma mensagem nova.
- **O índice:** `INDICE.md`, uma tabela por série. Quem escreve acrescenta a linha; quem lê preenche o status.
- **Status:**
  - `enviado`: commit e push feitos por quem escreveu;
  - `confirmado — DD/MM — <o que ficou>`: o outro PC leu, depois do `git pull`, e anotou o que fez;
  - `nada a fazer`: o outro PC só tomou ciência.
- **Ao abrir uma janela no kit:** `git pull --ff-only` (o gancho de abertura fará isso no F2), ler o `INDICE.md` e
  apresentar ao Ettore o que estiver `enviado` para este PC. Sem nada: "caixa vazia".
- **O que nunca vem para cá:** dado de paciente (nem o pseudônimo, ADR-0001), credencial e retrato com nomes de
  arquivo dos projetos. O `pre-commit` do kit (`scripts\checa_kit.py`) recusa o commit se achar.
- **Cada mensagem diz:** em uma linha, o que mudou; o que o outro PC faz, na ordem, com o comando; e como saber que
  deu certo.
