r"""Atualiza as skills de terceiros dos plugins do kit (F1b, 07/10/2026).

    python <kit>\scripts\atualizar_terceiros.py --todas                 # confere todas; não muda nada
    python <kit>\scripts\atualizar_terceiros.py tdd wait-what           # confere estas
    python <kit>\scripts\atualizar_terceiros.py tdd --aplicar           # traz a versão nova para o plugin
    python <kit>\scripts\atualizar_terceiros.py nova --repo dono/repo --grupo engenharia --aplicar
                                                                        # skill nova num grupo

Como: o `npx skills add` baixa cada skill numa pasta de preparo (fora do kit e fora de ~\.claude), o
script compara com a cópia do plugin (plugins\<grupo>\skills\<skill>) e, com --aplicar, troca a pasta
e atualiza o origem.json do grupo (repositório, caminho, commit do repositório no dia, data). Nada
vai para ~\.claude\skills: as skills só existem nos plugins. Depois de aplicar, confira o diff no git
e faça o commit; a edição vale na sessão seguinte (ou com /reload-plugins).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

KIT = Path(__file__).resolve().parents[1]
DE_CADA_PC = {'desktop.ini', 'thumbs.db'}


def origens(kit: Path = KIT) -> dict[str, tuple[str, dict]]:
    """skill -> (grupo, registro do origem.json)."""
    out = {}
    for o in sorted(kit.glob('plugins/*/origem.json')):
        for s, reg in json.loads(o.read_text(encoding='utf-8')).get('skills', {}).items():
            out[s] = (o.parent.name, reg)
    return out


def impressao(pasta: Path) -> dict[str, str]:
    return {f.relative_to(pasta).as_posix(): hashlib.sha256(f.read_bytes()).hexdigest()
            for f in sorted(pasta.rglob('*'))
            if f.is_file() and f.name.lower() not in DE_CADA_PC and '__pycache__' not in f.parts}


def diferencas(velha: Path, nova: Path) -> list[str]:
    a, b = impressao(velha) if velha.is_dir() else {}, impressao(nova)
    return ([f'+ {k}' for k in sorted(b.keys() - a.keys())] + [f'- {k}' for k in sorted(a.keys() - b.keys())]
            + [f'~ {k}' for k in sorted(a.keys() & b.keys()) if a[k] != b[k]])


def _npx() -> str:
    return shutil.which('npx') or shutil.which('npx.cmd') or 'npx'


def baixar(repo: str, skill: str, preparo: Path) -> Path:
    """Instala a skill só na pasta de preparo (escopo de projeto, cópia) e devolve a pasta dela."""
    preparo.mkdir(parents=True, exist_ok=True)
    r = subprocess.run([_npx(), '-y', 'skills', 'add', repo, '--skill', skill, '--agent', 'claude-code',
                        '--copy', '--yes'], cwd=preparo, capture_output=True, text=True, encoding='utf-8',
                       errors='replace')
    pasta = preparo / '.claude' / 'skills' / skill
    if not (pasta / 'SKILL.md').is_file():
        raise SystemExit(f'{skill}: o npx skills não entregou a skill em {pasta}\n{(r.stdout + r.stderr)[-800:]}')
    return pasta


def commit_do_repo(url: str) -> str | None:
    r = subprocess.run(['git', 'ls-remote', url, 'HEAD'], capture_output=True, text=True)
    return r.stdout.split()[0] if r.returncode == 0 and r.stdout.strip() else None


def hash_no_preparo(preparo: Path, skill: str) -> str | None:
    lock = preparo / 'skills-lock.json'
    if not lock.is_file():
        return None
    d = json.loads(lock.read_text(encoding='utf-8'))
    reg = d.get('skills', d).get(skill, {})
    return next((v for k, v in reg.items() if 'hash' in k.lower() and isinstance(v, str)), None)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('skills', nargs='*')
    ap.add_argument('--todas', action='store_true', help='todas as skills dos origem.json')
    ap.add_argument('--aplicar', action='store_true', help='troca a pasta no plugin e atualiza o origem.json')
    ap.add_argument('--repo', help='skill nova: o repositório (dono/repo)')
    ap.add_argument('--grupo', help='skill nova: o grupo (plugin) que a recebe')
    a = ap.parse_args(argv)
    reg = origens()
    nomes = sorted(reg) if a.todas else a.skills
    if not nomes:
        ap.error('diga as skills ou --todas')
    preparo = Path(tempfile.mkdtemp(prefix='claude-kit-preparo-'))
    mudou = 0
    try:
        for s in nomes:
            if s in reg:
                grupo, r = reg[s]
                repo, url = r['repositorio'], r.get('url') or f'https://github.com/{r["repositorio"]}.git'
            elif a.repo and a.grupo:
                grupo, r, repo, url = a.grupo, {}, a.repo, f'https://github.com/{a.repo}.git'
            else:
                print(f'{s}: não está em nenhum origem.json; para skill nova use --repo e --grupo')
                continue
            nova = baixar(repo, s, preparo / s)
            destino = KIT / 'plugins' / grupo / 'skills' / s
            dif = diferencas(destino, nova)
            print(f'{s} ({grupo}, {repo}): ' + ('igual' if not dif else f'{len(dif)} diferença(s)'))
            for linha in dif[:20]:
                print('   ', linha)
            if not dif or not a.aplicar:
                continue
            if destino.exists():
                shutil.rmtree(destino)
            shutil.copytree(nova, destino, ignore=shutil.ignore_patterns('desktop.ini', '__pycache__'))
            o_path = KIT / 'plugins' / grupo / 'origem.json'
            o = json.loads(o_path.read_text(encoding='utf-8')) if o_path.is_file() else {'skills': {}}
            hoje = time.strftime('%Y-%m-%d')
            o['skills'][s] = {
                'repositorio': repo, 'url': url,
                'caminho': r.get('caminho', ''),
                'hash_da_pasta': hash_no_preparo(preparo / s, s) or r.get('hash_da_pasta'),
                'commit': commit_do_repo(url),
                'instalada_em': r.get('instalada_em', hoje),
                'atualizada_em': hoje,
            }
            o_path.write_text(json.dumps(o, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
            mudou += 1
            print(f'    aplicada em {destino}; origem.json atualizado')
    finally:
        shutil.rmtree(preparo, ignore_errors=True)
    if mudou:
        print(f'\n{mudou} skill(s) trocadas. Confira o git diff, rode o instalar_kit.py --verificar e faça o commit.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
