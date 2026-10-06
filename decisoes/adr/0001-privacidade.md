---
status: accepted
data: 2026-10-06
decidido_por: Ettore (minientrevista em duas rodadas na janela do F1a)
substitui: as regras "nome de paciente nunca em arquivo versionado" e "console sem linha de paciente" no que conflitarem
---

# Privacidade: o paciente aparece por pseudônimo, só nos projetos `desosp-`

O Ettore é médico e tem direito de acesso aos dados. Ele não quer ser privado de recurso por cautela, quer decidir
informado: o risco é dito uma vez, com um contorno. As regras antigas proibiam qualquer nome de paciente fora da
planilha, o que travava conferências simples. Decidiu-se: nos projetos `desosp-`, o paciente aparece por um
**pseudônimo** feito por script, como se faz em discussão de caso entre profissionais. O nome completo só entra na
conversa quando o assunto é ele e nunca sai dela. Fora dos `desosp-`, nada de paciente.

## Decisões

**D1 · O que o Claude vê, por domínio** (domínios no [ADR-0002](0002-isolamento.md))

| domínio | identificador direto | pseudônimo | conteúdo clínico |
|---|---|---|---|
| `desosp-` | Só na conversa e só quando o assunto é ele: grafia, cruzar o mesmo paciente entre duas fontes, telefone errado. Exceção: o que o conector do Drive trouxer (D4). | Em todo veículo do domínio: conversa, `ESTADO.md`, resumo, caixa, relatório, commit. | Sim, junto do pseudônimo. |
| `pesquisa-` | nunca | nunca | Só a pergunta clínica, sem paciente. |
| `estudo-` | nunca | nunca | Caso desidentificado (idade, sexo, quadro). |
| `pessoal-` e `claude-kit` | nunca | nunca | nunca |

- **Identificador direto:** nome completo; RA, matrícula, CPF, CNS, Marca Ótica e telefone inteiros.
- **Pseudônimo:** as iniciais de todas as palavras do nome, inclusive "da", "de", "dos", em maiúsculas e sem acento,
  mais hífen e os 3 últimos dígitos de um número fixo do paciente.
  - Exemplo com nome fictício: Fulana de Souza Exemplo, RA terminado em 417 → `FDSE-417`.
  - O número é o RA no app e no censo. No HC, o F7 escolhe (o RA, se existir; senão, a Marca Ótica), e o ideal é o
    mesmo pseudônimo nos três projetos.
  - Se dois pacientes do mesmo conjunto caírem no mesmo pseudônimo, o script usa 4 dígitos para os dois e avisa.
  - Só iniciais repetiriam quase sempre num censo de ~200; com 3 dígitos a repetição fica por volta de 1%
    (estimativa, não medição).
- **Quem faz o pseudônimo é o script, nunca o modelo.** A função fica em cada projeto, com teste. O custo em token é
  zero: a sigla é mais curta que o nome, e o nome nem chega à conversa.
- **Padrão ao inspecionar dado:** contagem, cabeçalho, tipo. Quando a tarefa é sobre um registro, a linha vem com o
  pseudônimo no lugar do nome e dos números.
- **Regra de saída:** identificador direto nunca vai para arquivo fora das pastas de dado, commit, `ESTADO.md`,
  `PROXIMO.md`, resumo, prompt de `claude --bg` ou caixa. Mensagem para fora (e-mail, WhatsApp) segue a D7.

**D2 · Repositório**
- **Código:** identificador direto nunca entra no repositório de código. O pre-commit de nomes, no modelo do
  `desosp-hc\scripts\checa_privacidade.py` (dicionário de hashes; mostra só `arquivo:linha:tipo`), chega ao app e ao
  censo.
- **Dado:** pode ter repositório privado próprio (`HirugaX/<projeto>-dados`), separado do de código. Ele é criado só
  quando for preciso sincronizar o dado entre os PCs.
- **Contornos:**
  - verificação em duas etapas no GitHub;
  - `pre-push` que aceita só o próprio remoto;
  - nunca público, sem fork, sem colaborador.

**D3 · claude-mem e Headroom**
- **claude-mem:** nunca habilitado nos `desosp-` enquanto o banco for global (`~/.claude-mem/`, o mesmo para todo
  projeto). Senão, um paciente visto no censo ficaria pesquisável numa sessão `pessoal-`. O F3b confere que, com o
  plugin ligado só no estudo, uma sessão `desosp-` não grava nada.
- **Headroom:** permitido nos `desosp-` se passar no F3b, só no terminal, com `HEADROOM_BEACON=off`,
  `--code-memory none` e `--no-subscription-tracking`.

**D4 · Conectores do claude.ai**
- **`desosp-`:** todos negados, menos o **Google Drive**, que vale para tudo, inclusive planilha com paciente.
  - O que se aceitou: o conteúdo trazido pelo conector entra cru na conversa, com o nome completo. É exceção consciente
    à D1, decidida pelo Ettore com essa consequência à vista.
  - Contornos:
    - o que vier do Drive segue a regra de saída da D1;
    - arquivo com paciente que for processado por script passa antes pela pasta de dados, e o script entrega o
      pseudônimo.
  - Como se faz: `disableClaudeAiConnectors` é tudo ou nada, então os outros conectores são negados pelo nome no
    `.claude\settings.json` do projeto (`mcp__claude_ai_<Nome>`, inclusive o Claude Docs). Os nomes exatos se leem no
    `/mcp` na fase.
  - Em 06/10 o Drive não aparecia no Claude Code: conectá-lo no claude.ai quando for usar.
  - Conector novo que surgir depois fica ligado até ser negado; o gancho de abertura (F2) avisa.
- **`pesquisa-` e `estudo-`:** `disableClaudeAiConnectors: true`; só o que estiver declarado no `.mcp.json` do projeto
  (ex.: PubMed na pesquisa).
- **`pessoal-`:** conectores ligados, nunca com dado do trabalho.

**D5 · Drive pessoal.** Arquivo do trabalho, inclusive com paciente, pode ficar em `G:\Meu Drive\IA\desosp-*\`.
- A pasta `IA` fica "Restrito" (confirmado em 06/10).
- Nunca "qualquer pessoa com o link".
- Verificação em duas etapas na conta Google.

**D6 · `deny` de dentro dos projetos**
- **Princípio:** o bruto e as cópias ficam fechados para Read, Edit, Grep e Glob, com o `deny_paths` do safety-net e o
  `.ignore`. A pasta de trabalho da rodada fica aberta. Os scripts continuam lendo tudo.
- **Lista inicial** (a fase confere no lugar antes de aplicar):
  - app (F5a): `workspace_dev\`, `docs\para_o_app\`, `local_nomes.json`, `docs\fontes\PLANILHA_HC\`;
  - censo (F6): `entrada\`, `historico\`, `arquivo\`, `_envios\`, `desosp_app.db`, `desosp\local_nomes.json`;
  - HC (F7): `planilhas\`, `historico\`, `privado\`, `entrada\`.
- **Ficam abertas:** a `saida\` do censo e as pastas `rodada\`, `trabalho\` e `saida\` do HC.
- A política do safety-net é do Ettore: a fase imprime o comando para ele rodar.

**D7 · Comunicação (Q22)**
- O Claude escreve com `{{nome}}`, `{{matricula}}` e `{{telefone}}`, e um script local preenche. O texto final fica num
  arquivo local ou na área de transferência.
- O acervo de mensagens antigas só é lido em cópia com marcadores, feita por script.
- O Claude nunca envia: só redige.

## O que não depende do Ettore (dito uma vez, em 06/10)

- O controlador do dado é o hospital ou a operadora. A política deles pode proibir o envio a terceiros (Anthropic,
  GitHub, Google), e o Claude não tem como conferi-la.
- LGPD art. 11: dado de saúde é sensível; a base do trabalho dele é a tutela da saúde (II, f).
- LGPD art. 33: Anthropic, GitHub e Google guardam fora do Brasil, o que é transferência internacional.
- A opção de treino com as conversas está **desligada** (conferido por ele em 06/10). Ela vale também para o Claude
  Code na mesma conta. A retenção é de 30 dias, mas conversa marcada com 👍/👎 pode ser usada.

**A posição do Ettore, registrada:** "todos os repositórios e drives serão sempre privados; as próprias empresas
garantem a segurança dos dados. Se eu parar de confiar nelas, a regra precisa ser coerente e eu teria que parar de
confiar em você." O conselho de medicina permite discutir caso clínico em grupo fechado só de profissionais de saúde,
identificando o paciente pelas iniciais; o fluxo aqui é o mesmo.

## O que não muda

- Nome de funcionário e da operadora seguem as regras de cada projeto.
- Documento interno da operadora não entra em `pesquisas\`.
- Credencial nunca vai a repositório.
- Nada de paciente no `claude-kit`.

## Opções consideradas

| decisão | a que ficou de fora e por quê |
|---|---|
| D1 | "Como antes" (nenhum nome, nunca): travava conferências. "Linha inteira sempre que a tarefa é do registro": põe o nome na conversa sem necessidade. "Iniciais + leito": o leito muda e a sigla passa a apontar para outra pessoa. |
| D2 | Dado no próprio repositório de código: o histórico é permanente e vai junto em todo clone. "Nunca em repositório": tira a sincronização entre PCs. |
| D3 | claude-mem nos `desosp-`: o banco global quebra o isolamento (ADR-0002). |
| D4 | Pasta sincronizada para planilha com paciente e conector só sem paciente (era a recomendação): o Ettore preferiu o conector para tudo. |

## Tarefas por fase (as regras dos projetos não mudam antes da fase deles)

| fase | onde | o quê |
|---|---|---|
| F1a (feito) | `~\.claude\CLAUDE.md` (hardlink com `claude-kit\CLAUDE.md`) | Item "Privacidade e isolamento" apontando este ADR e o 0002. |
| F1a (feito) | `organizar-projetos\ORGANIZAR.md` (regra 7), `prompts.md` (prompt da arrumação) | "Nem ao GitHub" e "arquivo versionado" passam a "repositório de código". |
| F1a (feito) | memória `recursos-antes-de-recusa` | Aponta este ADR. |
| F5a | `desosp-app\CLAUDE.md:163` e `:264` | "Nenhum nome de paciente" passa a "nenhum identificador direto; pseudônimo pode (D1)". |
| F5a | `desosp-app` | Pre-commit de nomes (D2); `.claude\settings.json` com o `deny` da D6 e os conectores da D4. |
| F5c | `desosp-app\app\ia\` | A porta de leitura devolve o pseudônimo e os campos mínimos. |
| F6 | `desosp-censo\CLAUDE.md:181-192`, `:229-232`, `:384` | A mesma troca da D1; "dado clínico vira arquivo" ganha a exceção da D1. |
| F6 | `desosp-censo` | Pre-commit de nomes; settings (D4, D6); pseudônimo nas saídas que o Claude lê. |
| F7 | `desosp-hc\CLAUDE.md:143` e `:161` | A troca da D1 (o pre-commit atual continua: ele procura nome, não pseudônimo). |
| F7 | memória `console-sem-linha-de-paciente` (do HC) | "Nunca uma linha" passa a "por padrão contagem; a linha, com pseudônimo, quando a tarefa é sobre o registro". |
| F7 | `desosp-hc` | Settings (D4, D6); pseudônimo nas saídas; a escolha do número do pseudônimo. |
| F3b | `teste-ferramentas` | Claude-mem e Headroom só com dado sintético; a conferência da D3. |
| N2 | `desosp-comunicacao` | D7, com a porta de leitura do F5c. |

## Quando rever

- O hospital ou a operadora publicar política sobre IA ou nuvem.
- O claude-mem passar a ter banco por projeto.
- Aparecer um modo de ligar só um conector do claude.ai por projeto.
- Um pseudônimo repetido causar erro real.
