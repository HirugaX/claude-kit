"""Mede o uso real do Claude Code a partir dos registros locais das sessoes.

Le SO numeros (modelo, data, tokens, custo equivalente de API). Nunca le nem imprime
o texto das conversas: os projetos podem ter dado sensivel.

    python medir_uso.py                  # todos os projetos, desde sempre
    python medir_uso.py --desde 2026-09-23
    python medir_uso.py --sessoes        # uma linha por sessao

Leitura dos numeros:
  ctx0     contexto da 1a chamada da sessao = custo fixo (instrucoes + CLAUDE.md + memoria)
  ctx_med  contexto mediano por chamada; ctx_max o pico
  %fixo    quanto do contexto lido vem do custo fixo (o resto e conversa acumulada)
  US$      custo equivalente de API (a assinatura nao cobra assim; serve para comparar)
"""
import argparse, collections, glob, json, os

BASE = os.path.join(os.path.expanduser('~'), '.claude', 'projects')
FAMILIAS = ('fable-5-1', 'fable-5', 'opus-5-5', 'opus-5', 'sonnet-5-5', 'sonnet-5', 'haiku-4-5')


def familia(m):
    m = m or '?'
    for k in FAMILIAS:
        if k in m:
            return k
    return m[-14:]


def ler(caminho):
    """Uma sessao: chamadas unicas (por id de mensagem), compactacoes e o ultimo custo."""
    chamadas, comp, custo, t0 = {}, 0, None, None
    for linha in open(caminho, encoding='utf-8', errors='replace'):
        try:
            d = json.loads(linha)
        except Exception:
            continue
        t = d.get('type')
        t0 = t0 or d.get('timestamp')
        if d.get('isCompactSummary') or (t == 'system' and d.get('subtype') == 'compact_boundary'):
            comp += 1
        if t == 'cost-state':
            custo = d.get('totalCostUSD')
        if t == 'assistant':
            m = d.get('message', {})
            if not m.get('model') or m.get('model') == '<synthetic>':
                continue
            u = m.get('usage') or {}
            ctx = sum((u.get(k) or 0) for k in ('input_tokens', 'cache_read_input_tokens', 'cache_creation_input_tokens'))
            chamadas[m.get('id')] = (familia(m.get('model')), ctx, u.get('output_tokens') or 0, d.get('timestamp') or '')
    v = sorted(chamadas.values(), key=lambda x: x[3])
    return v, comp, custo, (t0 or '')[:16]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--desde', default='')
    ap.add_argument('--sessoes', action='store_true')
    a = ap.parse_args()
    for pasta in sorted(glob.glob(os.path.join(BASE, '*'))):
        if not os.path.isdir(pasta):
            continue
        tot = fixo = n = usd = 0
        faixas, modelos, linhas = collections.Counter(), collections.Counter(), []
        for f in glob.glob(os.path.join(pasta, '*.jsonl')):
            v, comp, custo, t0 = ler(f)
            if not v or t0 < a.desde:
                continue
            ctx = [c for _, c, _, _ in v]
            tot += sum(ctx); fixo += ctx[0] * len(ctx); n += len(ctx); usd += custo or 0
            modelos.update(m for m, *_ in v)
            for c in ctx:
                faixas['<100k' if c < 1e5 else '100-200k' if c < 2e5 else '200-400k' if c < 4e5 else '400-700k' if c < 7e5 else '>=700k'] += 1
            linhas.append((t0, len(ctx), ctx[0], sorted(ctx)[len(ctx) // 2], max(ctx), comp, custo or 0, dict(collections.Counter(m for m, *_ in v))))
        if not n:
            continue
        print(f"\n== {os.path.basename(pasta)}: {n} chamadas, contexto medio {tot / n / 1e3:.0f}k, "
              f"%fixo {100 * fixo / tot:.0f}%, US$ {usd:.0f}")
        print('   faixas:', {k: f"{100 * faixas[k] / n:.0f}%" for k in ('<100k', '100-200k', '200-400k', '400-700k', '>=700k')})
        print('   modelos:', dict(modelos))
        if a.sessoes:
            print(f"   {'inicio':16} {'cham':>5} {'ctx0':>5} {'ctx_med':>7} {'ctx_max':>7} {'comp':>4} {'US$':>6}  modelos")
            for t0, c, c0, cm, cx, comp, custo, mods in sorted(linhas):
                print(f"   {t0:16} {c:5} {c0 / 1e3:4.0f}k {cm / 1e3:6.0f}k {cx / 1e3:6.0f}k {comp:4} {custo:6.0f}  {mods}")


if __name__ == '__main__':
    main()
