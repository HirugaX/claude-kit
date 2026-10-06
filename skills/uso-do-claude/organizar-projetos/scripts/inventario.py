r"""O que este PC já tem, antes de instalar qualquer coisa (reaproveitar.md). Só lê; nunca escreve.

    python inventario.py [--kit C:\CLAUDE-PROJETOS\claude-kit] [--mae C:\CLAUDE-PROJETOS] [--raiz D:\ ...] [--json ARQ]

Olha: as skills de ~\.claude\skills (por nome e hash, comparadas com as do kit); os ganchos e a statusline dos
settings de usuário e de cada projeto; o CLAUDE.md pessoal (linhas, hardlink, as linhas que só ele tem); os
desktop.ini com marca (nosso, o de 30/09, alheio) e as pastas de ícones; os scripts do kit; as pastas de projeto
(git, remote, CLAUDE.md, memória) nas raízes de costume, inclusive a raiz do disco virando repositório; o kit.

Para cada item diz: SERVE (reaproveitar), DUPLICARIA (já existe; não instalar de novo), FALTA, ou ATENÇÃO.
Lê só metadados, settings e os CLAUDE.md (para contar e comparar linhas): nunca conteúdo de projeto. Não segue
junção nem link.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import regras as R  # noqa: E402

KIT_PADRAO = AQUI.parents[3]          # organizar-projetos -> uso-do-claude -> skills -> claude-kit
CASA = Path.home() / '.claude'
PULAR = {'node_modules', '.venv', 'venv', '__pycache__', '.git', 'AppData', 'Windows', 'Program Files',
         'Program Files (x86)', 'ProgramData', '$Recycle.Bin', 'System Volume Information'}


def impressao(pasta: Path) -> dict[str, str]:
    """Caminho relativo -> sha256 (sem __pycache__ e .pytest_cache, e sem desktop.ini e Thumbs.db, que são de cada
    PC), sem seguir link."""
    out = {}
    pilha = [pasta]
    while pilha:
        d = pilha.pop()
        try:
            for e in os.scandir(d):
                if e.is_dir(follow_symlinks=False):
                    if not R.e_link(e.path) and e.name not in ('__pycache__', '.pytest_cache'):
                        pilha.append(Path(e.path))
                elif e.is_file(follow_symlinks=False) and e.name.lower() not in ('desktop.ini', 'thumbs.db'):
                    out[Path(e.path).relative_to(pasta).as_posix()] = hashlib.sha256(Path(e.path).read_bytes()).hexdigest()
        except OSError:
            continue
    return out


def skills(casa: Path, kit: Path) -> list[dict]:
    out = []
    pasta = casa / 'skills'
    kit_sk = kit / 'skills'
    nomes = set()
    if pasta.is_dir():
        for e in sorted(os.scandir(pasta), key=lambda e: e.name):
            if not e.is_dir():
                continue
            p = Path(e.path)
            nomes.add(e.name)
            no_kit = kit_sk / e.name
            item = {'nome': e.name}
            if R.e_link(p):
                alvo = Path(os.path.realpath(p))
                item['tipo'] = f'junção -> {alvo}'
                if not alvo.exists():
                    item['veredito'] = 'ATENÇÃO: junção sem alvo (o ligar_claude.py re-aponta)'
                elif no_kit.exists() and alvo == no_kit.resolve():
                    item['veredito'] = 'SERVE: já ligada ao kit'
                else:
                    item['veredito'] = 'ATENÇÃO: junção para outro lugar'
            else:
                item['tipo'] = 'pasta de verdade (cópia)'
                if e.name == 'synced':
                    item['veredito'] = 'SERVE: sincronizada pelo claude.ai; não se mexe'
                elif not no_kit.is_dir():
                    item['veredito'] = 'SERVE: não existe no kit (o ligar_claude.py a traz para o kit)'
                elif impressao(p) == impressao(no_kit):
                    item['veredito'] = 'DUPLICARIA: igual à do kit; vira junção (ligar_claude.py)'
                else:
                    item['veredito'] = 'ATENÇÃO: difere da do kit; comparar antes (--kit-vence ou --pasta-vence)'
            out.append(item)
    if kit_sk.is_dir():
        for d in sorted(kit_sk.iterdir()):
            if d.is_dir() and not d.name.startswith(('_', '.')) and d.name not in nomes:
                out.append({'nome': d.name, 'tipo': 'só no kit', 'veredito': 'FALTA: ligar (ligar_claude.py)'})
    return out


def _ganchos(dados: dict) -> list[str]:
    out = []
    for evento, grupos in (dados.get('hooks') or {}).items():
        for g in grupos or []:
            for h in g.get('hooks', []):
                out.append(f'{evento} [{g.get("matcher", "*")}] {h.get("command", h.get("type", "?"))}')
    return out


def settings(casa: Path, projetos: list[Path]) -> list[dict]:
    arquivos = [casa / 'settings.json', casa / 'settings.local.json']
    for p in projetos:
        arquivos += [p / '.claude' / 'settings.json', p / '.claude' / 'settings.local.json']
    out = []
    for a in arquivos:
        if not a.is_file():
            continue
        try:
            d = json.loads(a.read_text(encoding='utf-8'))
        except ValueError:
            out.append({'arquivo': str(a), 'veredito': 'ATENÇÃO: não é JSON válido'})
            continue
        g = _ganchos(d)
        nosso = [x for x in g if 'organizar-projetos/scripts/gancho.py' in x.replace('\\', '/')]
        item = {'arquivo': str(a), 'ganchos': g, 'statusline': bool(d.get('statusLine')),
                'deny': (d.get('permissions') or {}).get('deny', []),
                'modelSettings': d.get('modelSettings'), 'effortLevel': d.get('effortLevel')}
        if nosso:
            item['veredito'] = 'DUPLICARIA: o gancho das cores já está ligado aqui; não ligar de novo'
        elif g:
            item['veredito'] = 'SERVE: há outros ganchos; o ligar-gancho ACRESCENTA, nunca substitui'
        else:
            item['veredito'] = 'SERVE'
        if d.get('effortLevel'):
            item['veredito'] += ' · ATENÇÃO: effortLevel de topo (não vale para o Opus 5.5; ver uso-do-claude §4)'
        out.append(item)
    return out


def claude_md(casa: Path, kit: Path) -> dict:
    casa_md, kit_md = casa / 'CLAUDE.md', kit / 'CLAUDE.md'
    out = {'pessoal': str(casa_md), 'existe': casa_md.is_file()}
    if casa_md.is_file():
        linhas = casa_md.read_text(encoding='utf-8', errors='replace').splitlines()
        out['linhas'] = len(linhas)
        out['nomes_do_arquivo'] = os.stat(casa_md).st_nlink
        if kit_md.is_file():
            if os.path.samefile(casa_md, kit_md):
                out['veredito'] = 'SERVE: já é o mesmo arquivo do kit (hardlink)'
            else:
                do_kit = set(l.strip() for l in kit_md.read_text(encoding='utf-8', errors='replace').splitlines())
                so_aqui = [l for l in linhas if l.strip() and l.strip() not in do_kit]
                out['so_neste_pc'] = so_aqui
                out['veredito'] = (f'ATENÇÃO: difere do do kit; {len(so_aqui)} linha(s) só deste PC — juntar com o '
                                   '"sim" e ligar como hardlink (nunca pela ferramenta Edit)') if so_aqui else \
                    'DUPLICARIA: o do kit já tem todas as linhas deste; ligar o do kit (hardlink)'
        else:
            out['veredito'] = 'SERVE: ainda sem kit neste PC'
    else:
        out['veredito'] = 'FALTA: ligar o do kit (ligar_claude.py)' if kit_md.is_file() else 'FALTA'
    return out


def inis(raizes: list[Path], limite: int = 20000) -> dict:
    """Os desktop.ini das raízes, por marca. Não desce em pasta pesada nem em link."""
    conta = {'nosso': 0, '3009': 0, 'alheio': 0}
    exemplos = {'nosso': [], '3009': [], 'alheio': []}
    vistos = 0
    for raiz in raizes:
        pilha = [raiz] if raiz.is_dir() else []
        while pilha and vistos < limite:
            d = pilha.pop()
            vistos += 1
            try:
                for e in os.scandir(d):
                    if e.is_dir(follow_symlinks=False):
                        if not R.e_link(e.path) and e.name not in PULAR:
                            pilha.append(Path(e.path))
                    elif e.name.lower() == 'desktop.ini':
                        tipo = R.marca_de(R.ler_ini(e.path))[0] or 'alheio'
                        conta[tipo] += 1
                        if len(exemplos[tipo]) < 3:
                            exemplos[tipo].append(d.as_posix() if isinstance(d, Path) else str(d))
            except OSError:
                continue
    local = Path(os.environ.get('LOCALAPPDATA', '')) if os.environ.get('LOCALAPPDATA') else None
    pastas_icones = {}
    if local:
        for nome in ('claude-pastas', r'DESOSP\icones_pastas'):
            pastas_icones[str(local / nome)] = (local / nome).is_dir()
    vered = []
    if conta['3009']:
        vered.append(f'ATENÇÃO: {conta["3009"]} do pacote de 30/09 — o aplicar os troca')
    if conta['nosso']:
        vered.append(f'SERVE: {conta["nosso"]} já no sistema novo')
    return {'contagem': conta, 'exemplos': exemplos, 'pastas_de_icones': pastas_icones,
            'veredito': '; '.join(vered) or 'nada a reaproveitar', 'pastas_vistas': vistos}


def _git(p: Path, *args) -> str:
    r = subprocess.run(['git', '--no-optional-locks', '-C', str(p), *args], capture_output=True, text=True,
                       encoding='utf-8', errors='replace')
    return r.stdout.strip() if r.returncode == 0 else ''


def chave_memoria(p: Path) -> str:
    """A chave de ~\\.claude\\projects: o caminho com todo caractere não alfanumérico trocado por '-'."""
    return ''.join(c if c.isalnum() and c.isascii() else '-' for c in str(p))


def _memoria(casa: Path, p: Path) -> int | None:
    proj = casa / 'projects'
    alvo = chave_memoria(p).casefold()
    if proj.is_dir():
        for d in proj.iterdir():
            if d.name.casefold() == alvo:
                mem = d / 'memory'
                return len(list(mem.glob('*.md'))) if mem.is_dir() else 0
    return None


def projetos(raizes: list[Path], casa: Path) -> list[dict]:
    """Pastas de primeiro e segundo nível das raízes que têm .git, CLAUDE.md ou .claude."""
    candidatos = []
    for raiz in raizes:
        if not raiz.is_dir():
            continue
        if (raiz / '.git').exists():
            candidatos.append(raiz)
        try:
            nivel1 = [Path(e.path) for e in os.scandir(raiz) if e.is_dir(follow_symlinks=False)
                      and not R.e_link(e.path) and e.name not in PULAR and not e.name.startswith('$')]
        except OSError:
            continue
        for p in nivel1:
            if any((p / m).exists() for m in ('.git', 'CLAUDE.md', '.claude', 'AGENTS.md')):
                candidatos.append(p)
    out = []
    for p in dict.fromkeys(candidatos):
        if p == casa:                      # a própria ~\.claude tem CLAUDE.md, mas não é projeto
            continue
        tem_git = (p / '.git').exists()
        remoto = _git(p, 'remote', 'get-url', 'origin') if tem_git else ''
        item = {'pasta': str(p), 'git': tem_git, 'remote': remoto, 'CLAUDE.md': (p / 'CLAUDE.md').is_file(),
                'AGENTS.md': (p / 'AGENTS.md').is_file(), 'memoria_arquivos': _memoria(casa, p),
                'onedrive': 'onedrive' in str(p).casefold()}
        if tem_git:
            item['sem_commit'] = len(_git(p, 'status', '--porcelain').splitlines())
            item['a_enviar'] = len(_git(p, 'log', '--oneline', '@{u}..').splitlines()) if remoto else None
        v = []
        if p == Path(p.anchor):
            v.append('ATENÇÃO: a raiz do disco é um repositório git — perguntar ao usuário antes de tudo')
        if tem_git and not remoto:
            v.append('FALTA: não está no GitHub (github.md)')
        if item['onedrive']:
            v.append('ATENÇÃO: dentro do OneDrive (o Claude Code deve evitar)')
        item['veredito'] = '; '.join(v) or 'SERVE'
        out.append(item)
    return out


def kit(kit_: Path, mae: Path) -> dict:
    out = {'kit': str(kit_), 'existe': kit_.is_dir(), 'mae': str(mae), 'mae_existe': mae.is_dir(),
           'claude_md_na_raiz_da_mae': (mae / 'CLAUDE.md').exists()}
    out['scripts'] = {n: (kit_ / 'scripts' / n).is_file() for n in ('ligar_claude.py', 'perguntas_controle.py')}
    local = R.ler_local()
    out['sistema_de_cores'] = local or 'não instalado neste PC'
    v = []
    if out['claude_md_na_raiz_da_mae']:
        v.append('ATENÇÃO: há CLAUDE.md na raiz da mãe — todo projeto o carregaria')
    if not out['existe']:
        v.append('FALTA: trazer o kit')
    out['veredito'] = '; '.join(v) or 'SERVE'
    return out


def inventario(kit_: Path, mae: Path, raizes_extra: list[Path], casa: Path = CASA) -> dict:
    home = Path.home()
    raizes = [Path(Path.home().anchor), home, home / 'Documents', home / 'Documentos', home / 'Desktop',
              home / 'OneDrive' / 'Documentos' / 'GitHub', home / 'Documents' / 'GitHub', mae, *raizes_extra]
    raizes = [r for r in dict.fromkeys(raizes) if r.is_dir()]
    projs = projetos(raizes, casa)
    return {
        'skills': skills(casa, kit_),
        'settings': settings(casa, [Path(p['pasta']) for p in projs]),
        'claude_md': claude_md(casa, kit_),
        'desktop_ini': inis([mae, *raizes_extra]),
        'projetos': projs,
        'kit': kit(kit_, mae),
    }


def imprimir(inv: dict) -> None:
    print('== skills (~\\.claude\\skills)')
    for s in inv['skills']:
        print(f'  {s["nome"]:24s} {s["tipo"]:40s} {s["veredito"]}')
    print('== settings')
    for s in inv['settings']:
        print(f'  {s["arquivo"]}: {s["veredito"]}')
        for g in s.get('ganchos', []):
            print(f'      gancho: {g}')
        if s.get('statusline'):
            print('      statusline: sim')
    c = inv['claude_md']
    print(f'== CLAUDE.md pessoal: {c.get("linhas", 0)} linhas, {c.get("nomes_do_arquivo", 0)} nome(s) — {c["veredito"]}')
    for l in c.get('so_neste_pc', [])[:20]:
        print(f'      só neste PC: {l}')
    d = inv['desktop_ini']
    print(f'== desktop.ini: {d["contagem"]} ({d["pastas_vistas"]} pastas vistas) — {d["veredito"]}')
    for k, v in d['pastas_de_icones'].items():
        print(f'      {k}: {"existe" if v else "não existe"}')
    print('== pastas de projeto')
    for p in inv['projetos']:
        extra = f'git, remote={p["remote"] or "—"}, sem commit {p.get("sem_commit")}' if p['git'] else 'sem git'
        print(f'  {p["pasta"]}: {extra}, CLAUDE.md={"sim" if p["CLAUDE.md"] else "não"}, '
              f'memória={p["memoria_arquivos"]} — {p["veredito"]}')
    k = inv['kit']
    print(f'== kit: {k["kit"]} ({"existe" if k["existe"] else "não existe"}); mãe {k["mae"]} '
          f'({"existe" if k["mae_existe"] else "não existe"}) — {k["veredito"]}')


def main(argv=None) -> int:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--kit', type=Path, default=KIT_PADRAO)
    ap.add_argument('--mae', type=Path, default=Path(r'C:\CLAUDE-PROJETOS'))
    ap.add_argument('--raiz', type=Path, action='append', default=[])
    ap.add_argument('--json', type=Path)
    a = ap.parse_args(argv)
    inv = inventario(a.kit, a.mae, a.raiz)
    imprimir(inv)
    if a.json:
        a.json.write_text(json.dumps(inv, ensure_ascii=False, indent=1), encoding='utf-8')
    return 0


if __name__ == '__main__':
    sys.exit(main())
