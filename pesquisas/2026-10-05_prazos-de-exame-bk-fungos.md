# Prazos de exame de BK e fungos: nomes, dias úteis × corridos, e como cada projeto conta

- **Pergunta:** a pergunta tem três partes.
  - Qual nome separa a pesquisa de BAAR (o "escarro de BAAR") da cultura de BK.
  - Quanto tempo levam a pesquisa, a cultura e a hemocultura para BK e para fungos, e se o prazo se conta
    em dias úteis ou corridos.
  - Como a planilha HC, o kernel, o app e a planilha de SLA do laboratório contam esses prazos.
- **Data:** 05/10/2026
- **Projeto que pediu:** planilha HC (`desosp-hc`), decisão D3 da janela de 05/10 (prazos de cultura da 3.16).
- **Fontes:**
  - **Levantamento local**, sem internet e sem dado de paciente:
    - `desosp-censo\desosp\exames.py`: o catálogo de 30 exames, o `identificar()`, o `avaliar()` e as
      regras [1] a [3];
    - `CONFIG_DESOSP.py:427-460`: os feriados;
    - as mensagens KP-001, KP-002, AK-005, AT-028 e AT-029;
    - `desosp-app\app\templates\_ficha.html:83` e `catalogos.py:108-113`;
    - a planilha de SLA do laboratório, só as abas de parâmetros e feriados;
    - a `LISTAS` do `MOLDE_v315.xlsx` e o `MUDANCAS_V314.md`.
  - **Internet**, lida por um subagente nas páginas e nos PDFs, não em resumos de busca:
    - Ministério da Saúde (2022, 2019 e 2008), ANVISA (2004 e o módulo 8), SBPC/ML (2015);
    - J Infect Control (2012), o FDA 510(k) do frasco BD Myco/F Lytic, LACEN-DF e FUNED/LACEN-MG;
    - os catálogos de Fleury, DASA (Lavoisier e Sérgio Franco), Diagnósticos do Brasil e Hermes Pardini.

    Os links estão no fim.
- **Conclusão:**
  - **Os nomes.** O esfregaço é a **baciloscopia (pesquisa de BAAR)**. A cultura é a **cultura para
    micobactérias (cultura de BK)**. No sangue é a **hemocultura para micobactérias**.
    - O que separa um exame do outro é a palavra "cultura" ou "hemocultura", contra "pesquisa",
      "baciloscopia" ou "exame direto".
    - BK e BAAR sozinhos não separam, porque aparecem nos dois nomes (por exemplo, "Cultura de BAAR").
    - "Bacterioscopia" sozinha é o Gram, outro exame.
  - **Úteis ou corridos: não há convenção.**
    - MS, ANVISA, BD e SBPC/ML dão tempo de incubação, em dias, semanas ou horas, nunca em dias úteis.
    - Os laboratórios diferem: o Fleury publica as culturas em dias corridos; a DASA e o Diagnósticos do
      Brasil publicam em dias úteis, inclusive as culturas.
    - O par "fungos em corridos, BK em úteis" não é a convenção de nenhum catálogo lido. Vale o contrato
      com o laboratório, sempre com a unidade ao lado do número.
  - **Os tempos técnicos.**
    - **Baciloscopia:** até 24 horas (MS); os catálogos publicam de 1 a 3 dias úteis.
    - **Cultura para micobactérias:** 42 dias em meio líquido (MGIT) e 56 em meio sólido (8 semanas). A meta
      de entrega do MS é de 62 dias no sólido e 44 no automatizado; a ANVISA (2004) dava 60.
    - **Hemocultura para micobactérias:** 42 dias de incubação; os catálogos publicam de 43 a 61 dias.
    - **Hemocultura para fungos:** até 30 dias (pelo protocolo BD: leveduras 7, filamentosos 30, dimórficos 42).
    - **Cultura para fungos:** até 4 semanas (dimórficos até 8).
    - **60 dias úteis dão cerca de 84 corridos,** acima da meta do MS (62) e dos 61 corridos do Fleury.
  - **Resultado parcial.** Nenhuma fonte fixa um "negativo parcial" com data para BK ou fungos. O que existe:
    - o positivo é comunicado cedo (o MS pede até 48 h depois de detectado);
    - na hemocultura, o parcial é o Gram do frasco positivo.
  - **Nos projetos**, com os mesmos 30 feriados de 2026 e 2027 nos três:
    - **Fungos:** a planilha HC e o kernel contam 32 dias corridos, iguais nos 365 dias de coleta
      conferidos; a planilha de SLA ainda diz úteis.
    - **BK:** o kernel e a planilha de SLA contam 60 dias úteis na hemocultura e na cultura; a planilha HC
      conta a hemocultura em 60 corridos, desde a v3.10 e sem justificativa escrita.
    - **O porquê do "útil" no BK:** é só a coluna de contrato da planilha de SLA. Ela diz úteis também
      para os fungos.
    - **Pesquisa de BK:** 2 dias úteis, só no kernel.
    - **Início da contagem:** o kernel desloca a coleta de cultura feita em fim de semana ou feriado, e a
      planilha HC não. São 117 de 365 dias de coleta com 1 dia útil de diferença.
    - **Fragmentos:** tecido (7) e ósseo (10) só existem na planilha HC; o kernel conta 5.
  - **Nomes que o kernel já reconhece:** "Pesquisa de BK", "Pesquisa de BAAR", "Escarro de BAAR" e
    "Baciloscopia de escarro" vão para a pesquisa; "Cultura para BK" vai para a cultura.
  - **Nomes que o kernel classifica errado:**
    - "Hemocultura de fungos", o próprio nome curto do kernel, cai na hemocultura comum;
    - "Hemocultura para micobactérias" também cai na hemocultura comum;
    - "Cultura para micobactérias" cai na cultura de secreção.
  - **O que o autor decidiu em 05/10:**
    - a planilha é a referência, e o kernel se alinha a ela (PK-001);
    - entram na 3.16 a pesquisa de BK (2 dias úteis) e a cultura para BK (60 dias úteis);
    - os fungos ficam em 32 dias corridos;
    - à tarde, depois desta pesquisa, o autor decidiu os exames de BK de 60 dias em **dias úteis, em tudo**: a
      hemocultura para BK passa de 60 corridos a 60 úteis na 3.16, como o contrato e o kernel (PK-002, PA-003).
- **Conferir de novo depois de:** 05/04/2027 para os prazos dos catálogos, que mudam sem aviso; MS e SBPC/ML
  são estáveis. A parte dos projetos vale até a próxima mudança no `exames.py` ou na `LISTAS` da planilha HC
  (é uma foto de 05/10/2026).

## Prazos publicados pelos laboratórios (lidos em 05/10/2026)

Prazo de entrega, com a unidade que a página escreve. O prazo de entrega não é o tempo de incubação.

| Exame | Fleury | DASA (Lavoisier / Sérgio Franco) | Diagnósticos do Brasil | Hermes Pardini |
|---|---|---|---|---|
| Pesquisa de BAAR | 1 dia útil | 3 / 2 dias úteis | 1 dia útil | 1 dia útil |
| Cultura para micobactérias | 61 corridos | 60 úteis / sem prazo | 45 úteis (Löwenstein-Jensen) | não achado |
| Hemocultura para micobactérias | 45 corridos | 43 / 61 úteis | 45 (sem unidade) | não achado |
| Hemocultura para fungos | 30 corridos | 30 / 33 úteis | 30 úteis | não achado |
| Cultura para fungos | 30 corridos | 30 / 32 úteis | 28 úteis | 15 úteis |
| TRM-TB (PCR para *M. tuberculosis* e rifampicina) | não conferido | 6 / 5 úteis | 2 úteis | não conferido |

- **O TRM-TB (GeneXpert) é outro exame,** molecular: não é baciloscopia nem cultura.
- **Não deu para ler:** Einstein, Sabin e Delboni bloquearam a leitura automática, e o Sírio-Libanês não
  tem catálogo com esses itens.

## Como refazer a conferência entre os projetos

Ela é feita em três passos, só lendo o kernel:

1. Importar o kernel sem gravar cache: `PYTHONDONTWRITEBYTECODE=1`, com
   `sys.path.insert(0, r'C:\CLAUDE-PROJETOS\desosp-censo\desosp')`.
2. Passar cada nome da coluna AB da `LISTAS` pelo `exames.identificar()`.
3. Para cada dia de coleta de um ano inteiro, comparar a data da planilha com a do kernel:
   - **a da planilha:** `WORKDAY(coleta, N, feriados)` nos exames em dias úteis, e `coleta + N` nos
     corridos;
   - **a do kernel:** `exames.limite(inicio, sla, contagem)`, em que `inicio` é `proximo_util(coleta)`
     quando o exame desloca a coleta.

## Fontes (links)

**Técnicas:**
- MS 2022, Manual de Recomendações para o Diagnóstico Laboratorial de TB e MNT:
  https://www.gov.br/saude/pt-br/centrais-de-conteudo/publicacoes/svsa/tuberculose/manual-de-recomendacoes-e-para-diagnostico-laboratorial-de-tuberculose-e-micobacterias-nao-tuberculosas-de-interesse-em-saude-publica-no-brasil.pdf
  (p. 97, 137, 174, 192, 200, 213, 393, 433, 441 e 442)
- MS 2019, Manual de Recomendações para o Controle da TB no Brasil, 2ª ed.:
  https://bvsms.saude.gov.br/bvs/publicacoes/manual_recomendacoes_controle_tuberculose_brasil_2_ed.pdf
  (p. 54, 55, 61 e 290)
- MS 2008, Manual Nacional de Vigilância Laboratorial da TB:
  https://bvsms.saude.gov.br/bvs/publicacoes/manual_vigilancia_laboratorial_tuberculose.pdf (p. 27, 210 e 225)
- ANVISA 2004, Manual de Microbiologia Clínica:
  https://bvsms.saude.gov.br/bvs/publicacoes/manual_microbiologia_completo.pdf (pdf p. 22, 184 e 339)
- ANVISA, módulo 8 (fungos), cópia da SES-GO:
  https://goias.gov.br/saude/wp-content/uploads/sites/34/2017/02/modulo-8-deteccao-e-identificacao-de-fungos-de-importancia-medica-b22.pdf
  (p. 21 e 22)
- SBPC/ML, Boas Práticas em Microbiologia Clínica (2015):
  https://bibliotecasbpc.org.br/pags/view.arcType.pdf.php?Arq=microbiologia_clinica.pdf (p. 68, 95, 107, 109, 116 e 118)
- Araujo MRE, J Infect Control 2012;1(1):08-19 (hemocultura): https://jic-abih.com.br/index.php/jic/article/download/12/11
- FDA 510(k) K222559, BD BACTEC Myco/F Lytic: https://www.accessdata.fda.gov/cdrh_docs/pdf22/K222559.pdf
- FUNED/LACEN-MG 2020, micobactérias não tuberculosas:
  https://www.funed.mg.gov.br/wp-content/uploads/2020/10/RECOMENDACOES-DIAGNOSTICO-MICOBACTERIAS-MNT.pdf
- LACEN-DF, cultura para BAAR: https://www.lacendf.saude.df.gov.br/cultura-para-baar-tuberculose/ ; cultura
  para fungos: https://www.lacendf.saude.df.gov.br/fungos_cultura

**Catálogos:**
- **Fleury:** `https://www.fleury.com.br/exames/` seguido de `bk-pesquisa-varios-materiais`,
  `cultura-para-micobacterias-varios-materiais`, `hemocultura-para-micobacterias-automatizada-varios-materiais`,
  `hemocultura-para-fungos-varios-materiais`, `cultura-para-fungos-varios-materiais` e `bacterioscopico-escarro`
  (este é o Gram).
- **DASA:** `https://lavoisier.com.br/exames/SLUG/` e `https://sergiofranco.com.br/exames/SLUG/`, em que SLUG
  é `baar-pesquisa`, `cultura-para-micobacteria-baar`, `hemocultura-para-micobacterias`,
  `hemocultura-para-fungos`, `cultura-de-fungos` ou
  `mycobacterium-tuberculosis-e-resistencia-a-rifampicina-diversos-pcr-qualitativo`.
- **Diagnósticos do Brasil:**
  `https://gde.diagnosticosdobrasil.com.br/GDE_Home/DetalheDoExame.aspx?ExameId=COD`, em que COD é `BAARP`,
  `CUBAR`, `HMCBK`, `HFUN`, `CULFU` ou `MTRIF`.
- **Hermes Pardini:** https://www.hermespardini.com.br/exame/01424 (pesquisa de BAAR) e
  https://www.hermespardini.com.br/exame/01356 (cultura para fungos).
