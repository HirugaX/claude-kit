r"""Prova por perguntas: cada pergunta numa sessão NOVA do Claude Code, do jeito certo.

    python C:\CLAUDE-PROJETOS\claude-kit\scripts\perguntas_controle.py PERGUNTAS.txt --projeto C:\CLAUDE-PROJETOS\desosp-censo
    python C:\CLAUDE-PROJETOS\claude-kit\scripts\perguntas_controle.py PERGUNTAS.txt --projeto C:\CLAUDE-PROJETOS\desosp-censo --so 2,15 --repetir 3

Serve para saber se uma regra CHEGA a uma sessão nova depois de mexer no CLAUDE.md, numa skill
ou em .claude/rules (skill uso-do-claude, §9b). PERGUNTAS.txt tem uma pergunta por linha; linha
vazia e linha que começa com # são ignoradas. Cada resposta vai para um arquivo próprio, numa
pasta NOVA: nada é sobrescrito nem apagado. O resumo diz, por sessão, o modelo que DE FATO rodou,
o custo (equivalente de API, que a assinatura não cobra assim) e o tempo. Comparar cada resposta
com o texto da regra continua sendo trabalho de quem lê.

Feito para não repetir os erros de 03/10 (KN42 do kernel DESOSP):
  1. a pergunta vai logo depois do -p, ANTES das opções: o --allowedTools aceita vários valores
     e engole o que vem depois dele;
  2. stdin fechado: o claude -p junta à pergunta tudo o que chegar pelo stdin;
  3. o modelo vai pelo ID completo e é conferido no modelUsage da saída JSON. O que um atalho abre
     muda entre versões (até a 2.1.234, `sonnet` abria o Sonnet 5); modelo diferente do pedido sai como ERRO;
  4. as respostas vão para uma pasta nova, nunca para o lugar das perguntas;
  5. sem shell: não há conversão de caminho do Git Bash (/doctor virava C:/Program Files/Git/doctor)
     nem aspas quebradas.

Só lê: as sessões abrem com Read, Grep, Glob e Skill, e mais nada.
"""
import argparse
import concurrent.futures as cf
import datetime as dt
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

SUFIXO = 'Responda em até 15 linhas e diga de qual arquivo tirou a resposta.'
FERRAMENTAS = 'Read,Grep,Glob,Skill'        # só leitura: a pergunta não pode mexer em nada
AUXILIAR = 'haiku'                           # o Claude Code usa um Haiku em tarefas internas


def achar_claude():
    c = shutil.which('claude')
    if c:
        return c
    for p in (Path.home() / '.local' / 'bin' / 'claude.exe', Path.home() / '.local' / 'bin' / 'claude'):
        if p.exists():
            return str(p)
    sys.exit('não achei o executável claude no PATH')


def ler_perguntas(arq):
    return [s.strip() for s in Path(arq).read_text(encoding='utf-8').splitlines()
            if s.strip() and not s.strip().startswith('#')]


def perguntar(claude, projeto, modelo, pergunta, sufixo, tempo_max):
    # 1. a pergunta logo depois do -p, antes de qualquer opção
    cmd = [claude, '-p', f'{pergunta} {sufixo}'.strip(),
           '--model', modelo, '--allowedTools', FERRAMENTAS, '--output-format', 'json']
    t0 = time.time()
    try:
        r = subprocess.run(cmd, cwd=projeto, stdin=subprocess.DEVNULL,   # 2. stdin fechado
                           capture_output=True, timeout=tempo_max)
    except subprocess.TimeoutExpired:
        return {'erro': f'passou de {tempo_max} s', 'segundos': round(time.time() - t0)}
    saida = r.stdout.decode('utf-8', 'replace')
    try:
        d = json.loads(saida)
    except ValueError:
        bruto = saida or r.stderr.decode('utf-8', 'replace')
        return {'erro': 'a saída não é JSON: ' + bruto.strip()[:300], 'segundos': round(time.time() - t0)}
    rodou = sorted(m for m in (d.get('modelUsage') or {}) if AUXILIAR not in m)
    res = {'texto': d.get('result') or '', 'modelos': rodou, 'custo': d.get('total_cost_usd'),
           'segundos': round((d.get('duration_ms') or 0) / 1000)}
    if d.get('is_error'):
        res['erro'] = f'o claude devolveu erro ({d.get("subtype")})'
    elif rodou != [modelo]:                                                # 3. o modelo que rodou
        res['erro'] = f'pedido {modelo}, rodou {", ".join(rodou) or "?"}'
    return res


def main():
    ap = argparse.ArgumentParser(description='Cada pergunta numa sessão nova do Claude Code.')
    ap.add_argument('perguntas', help='arquivo com uma pergunta por linha')
    ap.add_argument('--projeto', required=True,
                    help='a pasta onde a sessão abre: é o CLAUDE.md dela que se testa')
    ap.add_argument('--modelo', default='claude-sonnet-5-5',
                    help='ID completo (padrão claude-sonnet-5-5); atalho é recusado')
    ap.add_argument('--saida', help='pasta NOVA para as respostas (padrão: ao lado das perguntas)')
    ap.add_argument('--repetir', type=int, default=1, help='sessões por pergunta (padrão 1)')
    ap.add_argument('--so', help='só estas perguntas, pelo número: 2,4,15')
    ap.add_argument('--paralelo', type=int, default=5, help='sessões ao mesmo tempo (padrão 5)')
    ap.add_argument('--sufixo', default=SUFIXO, help='texto acrescentado ao fim de cada pergunta')
    ap.add_argument('--tempo-max', type=int, default=600, help='segundos por sessão (padrão 600)')
    a = ap.parse_args()

    if not a.modelo.startswith('claude-'):
        sys.exit(f'--modelo {a.modelo!r}: use o ID completo (ex.: claude-sonnet-5-5). O que um atalho '
                 'abre muda entre versões (até a 2.1.234, "sonnet" abria o Sonnet 5).')
    projeto = Path(a.projeto).resolve()
    if not projeto.is_dir():
        sys.exit(f'--projeto {projeto} não é uma pasta')
    qs = ler_perguntas(a.perguntas)
    if not qs:
        sys.exit('nenhuma pergunta no arquivo')
    escolha = list(range(1, len(qs) + 1))
    if a.so:
        escolha = [int(x) for x in a.so.split(',') if x.strip()]
        fora = [n for n in escolha if not 1 <= n <= len(qs)]
        if fora:
            sys.exit(f'--so fora da lista: {fora} (o arquivo tem {len(qs)} perguntas)')
    pasta = Path(a.saida) if a.saida else (
        Path(a.perguntas).resolve().parent / ('respostas_' + dt.datetime.now().strftime('%Y%m%d_%H%M%S')))
    if pasta.exists():                                                     # 4. nunca sobrescreve
        sys.exit(f'{pasta} já existe: escolha outra pasta (nada é sobrescrito)')
    pasta.mkdir(parents=True)

    claude = achar_claude()
    tarefas = [(n, k) for n in escolha for k in range(1, a.repetir + 1)]
    print(f'{len(tarefas)} sessão(ões) · {a.modelo} · abrindo em {projeto}\nrespostas em {pasta}\n')
    resultados = {}
    with cf.ThreadPoolExecutor(max_workers=max(1, a.paralelo)) as ex:
        futuros = {ex.submit(perguntar, claude, str(projeto), a.modelo, qs[n - 1], a.sufixo,
                             a.tempo_max): (n, k) for n, k in tarefas}
        for f in cf.as_completed(futuros):
            n, k = futuros[f]
            r = f.result()
            resultados[(n, k)] = r
            cab = [f'# Pergunta {n} · sessão {k}', '', qs[n - 1], '',
                   f'modelo: {", ".join(r.get("modelos") or ["?"])} · '
                   f'custo US$ {r.get("custo")} (equivalente de API) · {r.get("segundos")} s']
            if r.get('erro'):
                cab.append(f'ERRO: {r["erro"]}')
            (pasta / f'resposta_{n:02d}_{k}.md').write_text(
                '\n'.join(cab) + '\n\n---\n\n' + (r.get('texto') or '') + '\n', encoding='utf-8')
            print(f'  {n:2d}.{k}  ' + (f'ERRO: {r["erro"]}' if r.get('erro') else 'ok')
                  + f'  ({r.get("segundos")} s)')
    erros = [c for c, r in resultados.items() if r.get('erro')]
    custo = sum(r.get('custo') or 0 for r in resultados.values())
    print(f'\n{len(resultados) - len(erros)} ok · {len(erros)} com erro · '
          f'US$ {custo:.2f} (equivalente de API)')
    print(f'Agora compare cada resposta com o texto da regra: {pasta}')
    return 1 if erros else 0


if __name__ == '__main__':
    sys.exit(main())
