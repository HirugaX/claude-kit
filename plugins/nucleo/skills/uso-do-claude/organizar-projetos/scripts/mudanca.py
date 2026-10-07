r"""A mudança das pastas (ORGANIZAR.md, fase 5), lendo o plano de um arquivo JSON (modelo: planos\).

    python mudanca.py retrato <plano.json> antes.json          (com os caminhos velhos)
    python mudanca.py tudo <plano.json>                         checar + mover + lápides (o que o usuário roda)
    python mudanca.py retrato <plano.json> depois.json --novo
    python mudanca.py comparar antes.json depois.json
    python mudanca.py memoria <plano.json>                      copia a memória do Claude para as chaves novas
    python mudanca.py voltar <plano.json>                       o caminho de volta: tira as lápides e desfaz

    (e cada passo sozinho: checar, mover, lapides)

O plano (planos\notebook_2026-10-05.json é o exemplo real):
  {"data": "AAAA-MM-DD", "mae": "C:/CLAUDE-PROJETOS",
   "movimentos": [{"nome": "app", "de": "C:/meu-app", "para": "C:/CLAUDE-PROJETOS/meu-app",
                   "repo": true, "insubstituiveis": ["dados"]}, ...],
   "lapides_extras": [{"de": "C:/KIT-VELHO", "para": "C:/CLAUDE-PROJETOS/claude-kit"}],
   "processos_extras": ["app\\.iniciar"], "portas": [8765]}

Regras que custaram caro em 04-05/10 e estão no código:
  - mover com os.rename (mesmo disco: atômico; se algo segura a pasta, falha e nada se move); um "Acesso negado"
    pode ser passageiro: tenta 5 vezes e, se não der, para sem mexer em nada; rodar de novo pula o que já mudou;
  - nunca reclonar; nunca seguir junção (o os.walk do Python 3.12 entra em junção e conta em dobro);
  - a lápide é um ARQUIVO com o nome da pasta velha: todo mkdir no caminho velho passa a dar erro; na raiz do
    disco ela precisa de administrador;
  - a memória se COPIA (a chave velha guarda o histórico e o caminho de volta);
  - o modo automático do Claude Code não deixa o Claude mover pasta de projeto nem apagar na raiz do C:: o
    comando "tudo" é do usuário, num PowerShell (de administrador, se houver lápide na raiz).
O retrato guarda só caminhos relativos, tamanhos, datas e hashes — nenhum conteúdo.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import regras as R  # noqa: E402

TEXTO_LAPIDE = 'Isto é uma lápide'


def ler_plano(caminho) -> dict:
    p = json.loads(Path(caminho).read_text(encoding='utf-8'))
    for m in p['movimentos']:
        m['de'], m['para'] = Path(m['de']), Path(m['para'])
    p['projects'] = Path(p.get('projects') or Path.home() / '.claude' / 'projects')
    return p


def lapides(plano: dict) -> list[tuple[Path, Path]]:
    out = [(m['de'], m['para']) for m in plano['movimentos']]
    out += [(Path(x['de']), Path(x['para'])) for x in plano.get('lapides_extras', [])]
    return out


def chave(p) -> str:
    """A chave da memória em ~\\.claude\\projects: todo caractere não alfanumérico vira '-'."""
    return ''.join(c if c.isalnum() and c.isascii() else '-' for c in str(Path(p)))


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for bloco in iter(lambda: f.read(1 << 20), b''):
            h.update(bloco)
    return h.hexdigest()


def git(repo: Path, *args) -> str:
    r = subprocess.run(['git', '--no-optional-locks', '-C', str(repo), *args], capture_output=True, text=True,
                       encoding='utf-8', errors='replace')
    return r.stdout.strip()


# ---------------------------------------------------------------- retrato e comparação

def andar_sem_links(raiz: Path):
    """(pasta, [subpastas], [arquivos], [junções]) sem nunca entrar em junção ou link."""
    pilha = [raiz]
    while pilha:
        d = pilha.pop()
        pastas, arqs, links = [], [], []
        try:
            for e in os.scandir(d):
                if R.e_link(e.path):
                    links.append(Path(e.path))
                elif e.is_dir(follow_symlinks=False):
                    pastas.append(Path(e.path))
                else:
                    arqs.append(Path(e.path))
        except OSError:
            pass
        yield d, pastas, arqs, links
        pilha.extend(pastas)


def retrato_de(raiz: Path, insubstituiveis=(), repo: bool = False) -> dict:
    lista, juncoes, inis, n, total = {}, {}, [], 0, 0
    for d, _, arqs, links in andar_sem_links(raiz):
        for p in arqs:
            rel = p.relative_to(raiz).as_posix()
            try:
                st = p.stat()
            except OSError as e:
                lista[rel] = f'ERRO {e}'
                continue
            lista[rel] = [st.st_size, st.st_mtime_ns]
            n += 1
            total += st.st_size
            if p.name.lower() == 'desktop.ini':
                inis.append(rel)
        for l in links:
            juncoes[l.relative_to(raiz).as_posix()] = os.path.realpath(l)
    hashes = {}
    for item in insubstituiveis:
        alvo = raiz / item
        if alvo.is_file():
            hashes[item] = sha(alvo)
        elif alvo.is_dir():
            for d, _, arqs, _ in andar_sem_links(alvo):
                for p in arqs:
                    hashes[p.relative_to(raiz).as_posix()] = sha(p)
    out = {'raiz': str(raiz), 'arquivos': n, 'bytes': total, 'lista': lista, 'hashes': hashes,
           'desktop_ini': sorted(inis), 'juncoes': juncoes}
    if repo:
        out['head'] = git(raiz, 'rev-parse', 'HEAD')
        out['status'] = git(raiz, 'status', '--porcelain')
    return out


def cmd_retrato(plano: dict, destino, novo: bool) -> int:
    r = {}
    for m in plano['movimentos']:
        raiz = m['para'] if novo else m['de']
        if not raiz.is_dir():
            print(f'PARO: {raiz} não existe')
            return 1
        r[m['nome']] = retrato_de(raiz, m.get('insubstituiveis', []), m.get('repo', False))
        x = r[m['nome']]
        print(f'{m["nome"]:10s} {raiz}: {x["arquivos"]} arquivos, {x["bytes"]:,} bytes, {len(x["hashes"])} hashes, '
              f'{len(x["desktop_ini"])} desktop.ini, {len(x["juncoes"])} junções (não seguidas)')
    Path(destino).write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding='utf-8')
    return 0


def comparar(A: dict, B: dict) -> tuple[int, list[str]]:
    linhas, erros = [], 0
    for nome, x in A.items():
        y = B.get(nome)
        if y is None:
            linhas.append(f'{nome}: AUSENTE no depois')
            erros += 1
            continue
        dif = [k for k in ('arquivos', 'bytes', 'hashes', 'desktop_ini', 'head', 'status') if x.get(k) != y.get(k)]
        if x.get('juncoes', {}).keys() != y.get('juncoes', {}).keys():
            dif.append('juncoes')
        if x['lista'] != y['lista']:
            so_a = set(x['lista']) - set(y['lista'])
            so_b = set(y['lista']) - set(x['lista'])
            mudou = [k for k in set(x['lista']) & set(y['lista']) if x['lista'][k] != y['lista'][k]]
            dif.append(f'lista (só antes {len(so_a)}, só depois {len(so_b)}, mudou {len(mudou)}: '
                       f'{sorted(so_a)[:3]} {sorted(so_b)[:3]} {sorted(mudou)[:3]})')
        linhas.append(f'{nome:10s} ' + ('IGUAL' if not dif else 'DIFERENTE: ' + '; '.join(dif)))
        erros += bool(dif)
    return (1 if erros else 0), linhas


def cmd_comparar(a, b) -> int:
    cod, linhas = comparar(json.loads(Path(a).read_text(encoding='utf-8')), json.loads(Path(b).read_text(encoding='utf-8')))
    print('\n'.join(linhas))
    return cod


# ---------------------------------------------------------------- checar

def padrao_processos(plano: dict) -> re.Pattern:
    partes = []
    for m in plano['movimentos']:
        s = str(m['de']).replace('/', '\\')
        partes.append(re.escape(s).replace(r'\\', r'[\\/]') + r'(?![\w-])')
    partes += plano.get('processos_extras', [])
    return re.compile('|'.join(partes), re.I)


def presos(linhas: list[str], rx: re.Pattern) -> list[str]:
    return [l for l in linhas if l.strip() and rx.search(l)]


def sessoes_abertas(plano: dict, minutos: int = 5) -> list[str]:
    """Sessões do Claude Code abertas DENTRO de uma pasta que vai mudar (registro escrito há < N min)."""
    chaves = {chave(m['de']).casefold() for m in plano['movimentos']}
    out, agora = [], time.time()
    if plano['projects'].is_dir():
        for d in plano['projects'].iterdir():
            if d.name.casefold() in chaves:
                for f in d.glob('*.jsonl'):
                    if agora - f.stat().st_mtime < minutos * 60:
                        out.append(f'{d.name}\\{f.name}')
    return out


def cmd_checar(plano: dict) -> int:
    ps = ("Get-CimInstance Win32_Process | Where-Object { $_.ProcessId -ne $PID } | "
          "ForEach-Object { '{0} {1} {2}' -f $_.ProcessId, $_.Name, $_.CommandLine }")
    r = subprocess.run(['powershell', '-NoProfile', '-Command', ps], capture_output=True, text=True,
                       encoding='utf-8', errors='replace')
    if r.returncode != 0:
        print('PARO: não consegui listar os processos:', r.stderr.strip()[:300])
        return 1
    achados = [l[:160] for l in presos(r.stdout.splitlines(), padrao_processos(plano))
               if 'mudanca.py' not in l]
    import socket
    portas = []
    for porta in plano.get('portas', []):
        s = socket.socket()
        s.settimeout(1)
        if s.connect_ex(('127.0.0.1', porta)) == 0:
            portas.append(porta)
        s.close()
    sess = sessoes_abertas(plano)
    if achados or portas or sess:
        print('PARO: feche antes:')
        for a in achados:
            print('  processo:', a)
        for p in portas:
            print(f'  algo escuta na porta {p} (o app ligado?)')
        for s in sess:
            print('  sessão do Claude aberta numa pasta que vai mudar:', s)
        return 1
    print('ok: nenhum processo segura as pastas, nenhuma porta do plano ocupada, nenhuma sessão dentro delas')
    return 0


# ---------------------------------------------------------------- mover, lápides, memória, voltar

def cmd_mover(plano: dict, tentativas: int = 5, espera: float = 3) -> int:
    for m in plano['movimentos']:
        velho, novo = m['de'], m['para']
        if not velho.exists() and novo.is_dir():
            print(f'já movida: {velho}  ->  {novo}')
            continue
        if velho.is_file() and novo.is_dir():
            print(f'já movida (e com lápide): {velho}  ->  {novo}')
            continue
        if not velho.is_dir() or R.e_link(velho):
            print(f'PARO: {velho} não é uma pasta comum')
            return 1
        if novo.exists():
            print(f'PARO: {novo} já existe')
            return 1
        novo.parent.mkdir(parents=True, exist_ok=True)
        for t in range(tentativas):
            try:
                os.rename(velho, novo)
                break
            except OSError as e:
                print(f'  {m["nome"]}: tentativa {t + 1} falhou ({e}); espero {espera:g} s')
                time.sleep(espera)
        else:
            print(f'PARO: não consegui mover {velho} (algo o segura); nada dele foi mexido')
            return 1
        if not novo.is_dir() or velho.exists():
            print(f'PARO: depois de mover {velho}, o estado não confere')
            return 1
        print(f'ok  {velho}  ->  {novo}   ({time.strftime("%H:%M:%S")})')
    return 0


def e_lapide(p: Path) -> bool:
    try:
        return p.is_file() and TEXTO_LAPIDE in p.read_text(encoding='utf-8', errors='replace')[:400]
    except OSError:
        return False


def cmd_lapides(plano: dict) -> int:
    """Um arquivo com o nome de cada pasta velha, somente leitura: o caminho esquecido dá erro na hora."""
    data = plano.get('data') or time.strftime('%Y-%m-%d')
    for velho, novo in lapides(plano):
        if e_lapide(velho):
            print(f'já é lápide: {velho}')
            continue
        if velho.exists():
            print(f'pulo {velho}: ainda existe (a lápide entra depois que a pasta sair)')
            continue
        try:
            velho.write_text(f'Esta pasta mudou para {novo} em {data}. {TEXTO_LAPIDE}: não apague.\r\n', encoding='utf-8')
        except PermissionError:
            print(f'PARO: sem permissão para criar {velho} (na raiz do disco, só como administrador)')
            return 1
        subprocess.run(['attrib', '+r', str(velho)], capture_output=True) if sys.platform == 'win32' else None
        print(f'lápide: {velho}  (mudou para {novo})')
    falhas = 0
    for velho, _ in lapides(plano):
        if not velho.exists():
            continue
        try:
            os.makedirs(velho / '_prova_da_lapide', exist_ok=True)
            print(f'FALHA: criar pasta dentro de {velho} ainda funciona')
            falhas += 1
        except OSError:
            pass
    print('ok: todo caminho velho dá erro ao criar pasta' if not falhas else '')
    return 1 if falhas else 0


def _achar(proj: Path, nome: str) -> Path | None:
    if not proj.is_dir():
        return None
    for d in proj.iterdir():
        if d.name.casefold() == nome.casefold():
            return d
    return None


def pares_memoria(plano: dict) -> list[tuple[str, str]]:
    if isinstance(plano.get('memoria'), list):
        return [(x['de'], x['para']) for x in plano['memoria']]
    return [(chave(m['de']), chave(m['para'])) for m in plano['movimentos']]


def cmd_memoria(plano: dict) -> int:
    proj = plano['projects']
    for velha, nova in pares_memoria(plano):
        orig_d = _achar(proj, velha)
        orig = orig_d / 'memory' if orig_d else None
        if not orig or not orig.is_dir():
            print(f'sem memória: {velha} (nada a copiar)')
            continue
        dest_d = _achar(proj, nova) or proj / nova
        dest = dest_d / 'memory'
        if dest.exists() and any(dest.iterdir()):
            print(f'PARO: {dest} já tem conteúdo')
            return 1
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists():
            dest.rmdir()
        shutil.copytree(orig, dest)
        a = {p.relative_to(orig).as_posix(): sha(p) for p in orig.rglob('*') if p.is_file()}
        b = {p.relative_to(dest).as_posix(): sha(p) for p in dest.rglob('*') if p.is_file()}
        print(f'{"ok " if a == b else "DIFERENTE"} {velha} -> {dest_d.name}: {len(b)} arquivos')
        if a != b:
            return 1
    return 0


def cmd_voltar(plano: dict) -> int:
    for velho, _ in lapides(plano):
        if e_lapide(velho):
            if sys.platform == 'win32':
                subprocess.run(['attrib', '-r', str(velho)], capture_output=True)
            velho.unlink()
            print(f'lápide tirada: {velho}')
    for m in reversed(plano['movimentos']):
        if m['para'].is_dir() and not m['para'].is_symlink() and not m['de'].exists():
            os.rename(m['para'], m['de'])
            print(f'voltou: {m["para"]} -> {m["de"]}')
    return 0


def precisa_admin(plano: dict) -> bool:
    return any(v.parent == Path(v.anchor) for v, _ in lapides(plano))


def _admin() -> bool:
    try:
        import ctypes
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def main(argv=None) -> int:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    a = list(sys.argv[1:] if argv is None else argv)
    if len(a) < 2:
        print(__doc__)
        return 2
    c = a[0]
    if c == 'comparar':
        return cmd_comparar(a[1], a[2])
    plano = ler_plano(a[1])
    if c == 'tudo':
        if precisa_admin(plano) and not _admin():
            print('PARO: há lápide na raiz do disco; abra o PowerShell como administrador e rode de novo')
            return 1
        for passo in (cmd_checar, cmd_mover, cmd_lapides):
            if passo(plano) != 0:
                print('PAREI aqui. Nada depois deste passo foi feito.')
                return 1
        print('\nPRONTO. Volte à janela do Claude e diga: "rodei a mudança".')
        return 0
    if c == 'retrato':
        return cmd_retrato(plano, a[2], '--novo' in a)
    acoes = {'checar': cmd_checar, 'mover': cmd_mover, 'lapides': cmd_lapides, 'memoria': cmd_memoria,
             'voltar': cmd_voltar}
    if c in acoes:
        return acoes[c](plano)
    print(__doc__)
    return 2


if __name__ == '__main__':
    sys.exit(main())
