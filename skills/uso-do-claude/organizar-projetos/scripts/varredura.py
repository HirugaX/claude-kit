r"""Varredura dos caminhos velhos (ORGANIZAR.md, fases 4 e 7). Só lê; mostra arquivo:linha e o caminho achado.

    python varredura.py <plano.json> <saida.json>

Lê do plano (o mesmo do mudanca.py):
  - os caminhos velhos: o "de" de cada movimento e das lapides_extras, mais as chaves de memória velhas;
  - "nao_casar": caminhos que começam igual mas são outra coisa (ex.: "C:/PROJ ARQUIVO" não é "C:/PROJ");
  - "varrer": [{"nome": "kernel", "raiz": "C:/CLAUDE-PROJETOS/desosp-censo", "pular": ["entrada", "saida"]}, ...]
    (as pastas de dado não se varrem nem se corrigem; "pular" aceita subpasta, "a/b"); sem "varrer", varre o
    "para" de cada movimento com repo.
Acha as formas C:\X, C:/X, C:\\X (dentro de string), /c/X e //c/X, sem diferenciar maiúscula, e só com fronteira
no fim ("C:\KIT" não casa com "C:\KIT-NOVO"). Não segue junção nem link. Separa o resultado em código,
teste, config, doc vivo e histórico (o histórico não se reescreve).
"""
from __future__ import annotations

import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import regras as R  # noqa: E402

PULAR_DIR = {'.git', '.venv', 'venv', 'node_modules', '__pycache__', '.pytest_cache', '.mypy_cache', '.ruff_cache'}
TEXTO = {'.py', '.md', '.txt', '.json', '.toml', '.ini', '.cfg', '.bat', '.cmd', '.ps1', '.sh', '.html', '.js', '.ts',
         '.css', '.yml', '.yaml', '.gitignore', '.gitattributes', '.ignore', ''}
HIST = re.compile(r'(?i)(HANDOFF|^A[TKP]-\d|^PA-\d|^KP-\d|^PK-\d|INDICE|para_o_|para_a_|historico|ARQUIVO|_RELATO|decisoes)')


def _forma(caminho: str) -> str:
    """Regex de um caminho absoluto em todas as formas (C:\\, C:/, /c/, //c/, barras dobradas)."""
    p = caminho.replace('\\', '/').rstrip('/')
    m = re.match(r'^([A-Za-z]):/(.*)$', p)
    if not m:
        return re.escape(p)
    letra, resto = m.group(1), m.group(2)
    corpo = r'[\\/]+'.join(re.escape(x) for x in resto.split('/'))
    return rf'(?:{letra}:|/{letra}|//{letra})[\\/]+{corpo}'


def montar_regex(velhos: list[str], chaves: list[str]) -> re.Pattern:
    partes = [rf'(?<![\w.]){_forma(v)}(?![\w-])' for v in sorted(set(velhos), key=len, reverse=True)]
    partes += [rf'\b{re.escape(c)}(?![\w-])' for c in sorted(set(chaves), key=len, reverse=True)]
    return re.compile('|'.join(partes), re.I)


def _normal(s: str) -> str:
    s = re.sub(r'[\\/]+', '/', s).casefold()
    return re.sub(r'^//?([a-z])/', r'\1:/', s)


def regex_do_plano(plano: dict) -> tuple[re.Pattern, list[str]]:
    velhos = [m['de'] for m in plano['movimentos']] + [x['de'] for x in plano.get('lapides_extras', [])]
    chave = lambda p: ''.join(c if c.isalnum() and c.isascii() else '-' for c in str(Path(p)))
    chaves = [chave(v) for v in velhos] + plano.get('chaves_velhas', [])
    return montar_regex([str(v) for v in velhos], chaves), [_normal(x) for x in plano.get('nao_casar', [])]


def classe(rel: Path) -> str:
    s = rel.as_posix()
    if any(HIST.search(p) for p in rel.parts):
        return 'histórico'
    if s.startswith('tests/') or '/tests/' in s or rel.name.startswith('test_'):
        return 'teste'
    if rel.suffix in {'.py', '.bat', '.cmd', '.ps1', '.sh', '.js', '.ts', '.html'}:
        return 'código'
    if rel.suffix in {'.json', '.toml', '.ini', '.cfg', '.yml', '.yaml'} or rel.name.startswith('.git') or '.git' in rel.parts:
        return 'config'
    return 'doc vivo'


def arquivos(raiz: Path, pular: set[tuple[str, ...]]):
    pilha = [raiz]
    while pilha:
        d = pilha.pop()
        try:
            entradas = list(os.scandir(d))
        except OSError:
            continue
        for e in entradas:
            p = Path(e.path)
            if R.e_link(p):
                continue
            rel = p.relative_to(raiz)
            if e.is_dir(follow_symlinks=False):
                if e.name == '.git':
                    if (p / 'config').is_file():
                        yield p / 'config', rel / 'config'
                    continue
                if e.name in PULAR_DIR or any(rel.parts[:len(x)] == x for x in pular):
                    continue
                pilha.append(p)
            elif (p.suffix.lower() in TEXTO) and e.stat().st_size < 5_000_000:
                yield p, rel


def varrer(raiz: Path, rx: re.Pattern, nao_casar: list[str], pular=()) -> dict:
    achados = defaultdict(list)
    pular = {tuple(x.replace('\\', '/').strip('/').split('/')) for x in pular}
    for p, rel in arquivos(raiz, pular):
        try:
            linhas = p.read_text(encoding='utf-8', errors='replace').splitlines()
        except OSError:
            continue
        for i, l in enumerate(linhas, 1):
            for m in rx.finditer(l):
                resto = _normal(l[m.start():])
                if any(resto.startswith(n) for n in nao_casar):
                    continue
                achados[rel.as_posix()].append((i, m.group(0)))
    out = defaultdict(dict)
    for rel, lst in sorted(achados.items()):
        out[classe(Path(rel))][rel] = lst
    return dict(out)


def main(argv=None) -> int:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    a = list(sys.argv[1:] if argv is None else argv)
    if len(a) != 2:
        print(__doc__)
        return 2
    plano = json.loads(Path(a[0]).read_text(encoding='utf-8'))
    rx, nao = regex_do_plano(plano)
    alvos = plano.get('varrer') or [{'nome': m['nome'], 'raiz': m['para']} for m in plano['movimentos'] if m.get('repo')]
    tudo = {}
    for alvo in alvos:
        raiz = Path(alvo['raiz'])
        if not raiz.is_dir():
            print(f'== {alvo["nome"]}: {raiz} não existe')
            continue
        r = varrer(raiz, rx, nao, alvo.get('pular', []))
        tudo[alvo['nome']] = r
        tot = {c: (len(v), sum(len(x) for x in v.values())) for c, v in r.items()}
        print(f'== {alvo["nome"]} ({raiz}): ' + (', '.join(f'{c} {n} arq/{o} ocorr.' for c, (n, o) in sorted(tot.items())) or 'nada'))
    Path(a[1]).write_text(json.dumps(tudo, ensure_ascii=False, indent=1), encoding='utf-8')
    return 0


if __name__ == '__main__':
    sys.exit(main())
