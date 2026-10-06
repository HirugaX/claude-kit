# A escolha dos ícones de pasta (05/10/2026)

- **O que é:** a decisão do Ettore sobre o desenho e as cores do sistema de pastas, depois dos protótipos de 04/10
  (`C:\CLAUDE-PROJETOS\prototipos-icones\VER_PROTOTIPOS.html`, três estilos). Respostas dadas no chat da janela da
  reorganização (aberta em `C:\CLAUDE-PROJETOS`, notebook), em 05/10.
- **Para quem:** a janela **claude-kit · construir o pacote das pastas** (e a de aplicar).

## A base: o pacote que o Ettore fez

`C:\CLAUDE-PROJETOS\prototipos-icones\amostra_gerada_ettore\` ("Ícones de pastas — versão 3", com a prévia
`PREVIA_ICONES.html`). Sete `.ico`, cada um com 16, 20, 24, 32, 40, 48, 64, 128 e 256 px em RGBA; de 16 a 24 px
um símbolo simplificado, de 32 a 256 o principal; o correio ganha o envelope a partir de 48 px. Estilo: pasta
lisa (o fundo e a aba num tom mais escuro), emblema branco. Conferido em 05/10: os tamanhos estão todos lá.

| verbo ou marca | desenho | cor | de onde vem |
|---|---|---|---|
| Eu alimento | seta para baixo | `#D97722` | `eu-alimento.ico` |
| Eu forneço fontes | mão entregando um chip/robô | `#7B5CD6` | `eu-forneco-fontes.ico` |
| Eu leio | livro aberto com brilho | `#25824D` | `eu-leio.ico` |
| Trabalhamos juntos | cabeça com circuitos | **ciano `#0F9BA8`** (no arquivo está `#105C40`, verde-escuro perto demais do verde de Eu leio em 16-20 px: recolorir) | `trabalhamos-juntos-cabeca.ico` |
| Não toco | `< >` | `#2F6FD6` | `nao-toco.ico` |
| Não toco (correio) | `< >` + envelope a partir de 48 px | `#2F6FD6` | `nao-toco-correio.ico` |
| **Projeto com IA** (marca da raiz) | **engrenagem com "AI"** | cor própria, a confirmar na prévia (proposta: dourado `#D4A21A`, a candidata A dos protótipos) | `trabalhamos-juntos-engrenagem.ico`, recolorido |
| **Dado real / sem cópia** | cadeado | vermelho `#D23B3B` (registro, seção 2) | **desenhar** no mesmo estilo |
| **Criada pela IA — falta classificar** | "?" | cinza `#8C8C8C` | **desenhar** no mesmo estilo |

- Quem desenha as duas que faltam: a janela do kit, no estilo do Ettore (a mesma pasta, o mesmo emblema branco, o
  mesmo símbolo simplificado em 16-24 px), com prévia antes de aplicar.
- O `.ico` final é **montado em cada PC** a partir dos quadros PNG (extraídos dos `.ico` do Ettore e guardados no
  pacote como fonte do desenho), nunca levado pronto: desde junho de 2026 o Windows ignora `desktop.ini` com marca
  da web, e a regra do registro (seção 4) é gerar em cada PC.
- O brilho fica só no "Eu leio" (foi por isso que a marca Projeto com IA não usa o brilho dos protótipos).
- Moldura do VS Code (Peacock): as propostas dos protótipos (censo `#2E7D32`, app `#1565C0`, hc `#EF6C00`, kit
  `#6A1B9A`) seguem como proposta; mostrar na prévia.

## O mapa (os dois pontos que estavam abertos)

- A pasta-mãe `C:\CLAUDE-PROJETOS` recebe a marca **Projeto com IA**.
- `desosp-hc\docs\premiacoes` (as artes do placar) fica em **Eu forneço fontes**.
- O resto do mapa é o do plano aprovado (`2026-10-04_plano-aprovado.md`, seção 4.9), mais as pastas passageiras
  que as janelas do kernel, da planilha e do app listarem (ficam sem cor).

## A versão 4 — aprovada (05/10, noite)

Na janela do kit (organizar-projetos), o Ettore apontou que faltavam dois desenhos das referências que ele tinha dado ao
ChatGPT (o braço de robô e a mão com chip) e pôs as referências em `C:\CLAUDE-PROJETOS\prototipos-icones\referencia_icones`
(8 imagens; a 1 e a 7 são a mesma grade de 16 ícones de IA). Pediu também a engrenagem do Projeto com IA na cor original.
Viu a prévia (página "Ícones de pasta v4") e respondeu: **"gostei muito! aprovo tudo"**.

| ícone | o desenho | de onde vem |
|---|---|---|
| Eu alimento | seta para baixo | o desenho dele, sem mudança |
| Eu forneço fontes | **mão com chip** | a mão dele (`eu-forneco-fontes.ico`), com um chip no lugar do robozinho (de 32 px para cima; de 16 a 24 px o desenho dele já é um quadradinho sobre a mão) |
| Eu leio | livro aberto com brilho | o desenho dele, sem mudança |
| Trabalhamos juntos | cabeça com circuitos | o desenho dele, em ciano `#0F9BA8` |
| Não toco | **braço de robô** | novo, da grade de referências, na pasta azul dele |
| Não toco (correio) | **braço de robô + envelope** | o braço, com o selo de envelope dele (a partir de 48 px) |
| Projeto com IA | engrenagem com "AI" | o desenho dele, **na cor original `#105C40`** (perto do verde do Eu leio em 16-20 px; aceito) |
| Dado real / sem cópia | **cadeado no circuito** | novo, da grade de referências (o cadeado sozinho em 16-24 px) |
| Criada pela IA — falta classificar | **robô com "?" no rosto** | novo, do robô da grade (o "?" sozinho em 16-24 px) |

- Os desenhos novos são próprios, **inspirados** nas referências, sem decalque: a grade é uma prévia de banco de imagens
  com marca d'água, e algumas das outras são imagens "premium".
- Onde estão: os quadros em `claude-kit\skills\uso-do-claude\organizar-projetos\icones\` (a origem de cada um no
  `quadros.json`); a receita é a `ORIGEM` do `desenho.py`. A amostra para o Explorador está em
  `prototipos-icones\amostra-referencias\`. A `amostra-final` e a `amostra-explorador` são de versões anteriores.
- As molduras do VS Code ficaram como propostas: censo `#2E7D32`, app `#1565C0`, hc `#EF6C00`, kit `#6A1B9A`.
