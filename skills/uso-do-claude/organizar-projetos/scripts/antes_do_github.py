r"""A conferência antes do PRIMEIRO envio de um repositório ao GitHub (github.md). Só lê; não envia nada.

    python antes_do_github.py <repositório> [--termos ARQ] [--sem-historia]

Confere o que iria ao GitHub: os arquivos versionados, os novos que um "git add -A" pegaria e (salvo
--sem-historia) todo o histórico, porque o primeiro push leva todos os commits:
  - segredo: chaves e tokens conhecidos (GitHub, Anthropic/OpenAI, AWS, Google, Slack), chave privada, .env,
    atribuição de senha/token com valor;
  - dado sensível: os termos do arquivo --termos (um por linha: nomes do domínio, identificadores). O arquivo
    fica FORA do repositório e do kit; a saída mostra só arquivo:linha e o número do termo, nunca o texto;
  - arquivo grande (o GitHub recusa acima de 100 MB e avisa acima de 50 MB);
  - extensões de dado (.db, .xlsx, .csv, .pdf...): aviso, para conferir à mão;
  - o remote: se já existe e é do GitHub, tem de ser PRIVADO (gh repo view).
Se o gitleaks estiver instalado, roda também. Sai 1 se achar problema. No fim, imprime o comando do envio
(sempre --private) para o usuário rodar.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

SEGREDOS = [
    ('token do GitHub', re.compile(r'\b(?:gh[pousr]_[A-Za-z0-9]{36,}|github_pat_[A-Za-z0-9_]{60,})')),
    ('chave Anthropic/OpenAI', re.compile(r'\bsk-(?:ant-|proj-)?[A-Za-z0-9_\-]{20,}')),
    ('chave AWS', re.compile(r'\bAKIA[0-9A-Z]{16}\b')),
    ('chave Google', re.compile(r'\bAIza[0-9A-Za-z_\-]{35}\b')),
    ('token Slack', re.compile(r'\bxox[baprs]-[A-Za-z0-9-]{10,}')),
    ('chave privada', re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----')),
    ('senha ou token com valor', re.compile(
        r'(?i)\b(?:password|passwd|senha|secret|token|api[_-]?key)\b\s*[:=]\s*["\'][^"\'\s]{8,}["\']')),
]
EXT_DADO = {'.db', '.sqlite', '.sqlite3', '.xlsx', '.xlsm', '.xls', '.csv', '.pdf', '.docx', '.doc', '.parquet', '.zip'}
GRANDE, AVISO_GRANDE = 100 * 2**20, 50 * 2**20


def git(repo: Path, *args) -> subprocess.CompletedProcess:
    return subprocess.run(['git', '--no-optional-locks', '-C', str(repo), *args], capture_output=True, text=True,
                          encoding='utf-8', errors='replace')


def ler_termos(arq: Path | None) -> list[re.Pattern]:
    if not arq:
        return []
    termos = [l.strip() for l in arq.read_text(encoding='utf-8').splitlines() if l.strip() and not l.startswith('#')]
    return [re.compile(rf'(?<!\w){re.escape(t)}(?!\w)', re.I) for t in termos]


def arquivos_a_enviar(repo: Path) -> list[str]:
    a = git(repo, 'ls-files', '-z').stdout.split('\0')
    b = git(repo, 'ls-files', '-z', '--others', '--exclude-standard').stdout.split('\0')
    return sorted({x for x in a + b if x})


def examinar_texto(texto: str, termos: list[re.Pattern]) -> tuple[list[tuple[int, str]], list[tuple[int, int]]]:
    seg, sens = [], []
    for i, linha in enumerate(texto.splitlines(), 1):
        for nome, rx in SEGREDOS:
            if rx.search(linha):
                seg.append((i, nome))
        for n, rx in enumerate(termos, 1):
            if rx.search(linha):
                sens.append((i, n))
    return seg, sens


def conferir(repo: Path, termos: list[re.Pattern], historia: bool = True) -> tuple[list[str], list[str]]:
    prob, avisos = [], []
    if git(repo, 'rev-parse', '--is-inside-work-tree').stdout.strip() != 'true':
        return [f'{repo} não é um repositório git'], []
    if git(repo, 'rev-parse', '--show-toplevel').stdout.strip().replace('\\', '/').casefold() == \
            str(Path(repo.anchor)).replace('\\', '/').rstrip('/').casefold():
        prob.append('a raiz do disco é o repositório: não envie; pergunte ao usuário o que ele é')
    ext = {}
    for rel in arquivos_a_enviar(repo):
        p = repo / rel
        if not p.is_file():
            continue
        tam = p.stat().st_size
        if tam > GRANDE:
            prob.append(f'arquivo maior que 100 MB (o GitHub recusa): {rel}')
        elif tam > AVISO_GRANDE:
            avisos.append(f'arquivo maior que 50 MB: {rel}')
        if p.name == '.env' or p.name.startswith('.env.') and not p.name.endswith(('.example', '.exemplo', '.sample')):
            prob.append(f'arquivo .env iria junto: {rel}')
        if p.suffix.lower() in EXT_DADO:
            ext.setdefault(p.suffix.lower(), []).append(rel)
        if tam > 5 * 2**20:
            continue
        try:
            texto = p.read_text(encoding='utf-8')
        except (UnicodeDecodeError, OSError):
            continue
        seg, sens = examinar_texto(texto, termos)
        prob += [f'segredo ({nome}): {rel}:{i}' for i, nome in seg]
        prob += [f'termo sensível nº {n}: {rel}:{i}' for i, n in sens]
    for e, lst in sorted(ext.items()):
        avisos.append(f'{len(lst)} arquivo(s) {e} iriam junto (dado?): {", ".join(lst[:3])}{" ..." if len(lst) > 3 else ""}')
    if historia and git(repo, 'rev-parse', '--verify', 'HEAD').returncode == 0:
        r = subprocess.Popen(['git', '-C', str(repo), 'log', '--all', '-p', '--no-color', '--format=@@commit %h'],
                             stdout=subprocess.PIPE, text=True, encoding='utf-8', errors='replace')
        commit, arq, vistos = '?', '?', set()
        for linha in r.stdout:
            if linha.startswith('@@commit '):
                commit = linha.split()[1]
            elif linha.startswith('+++ b/'):
                arq = linha[6:].strip()
            elif linha.startswith('+') and not linha.startswith('+++'):
                seg, sens = examinar_texto(linha[1:], termos)
                for _, nome in seg:
                    k = ('s', commit, arq, nome)
                    if k not in vistos:
                        vistos.add(k)
                        prob.append(f'segredo no histórico ({nome}): commit {commit}, {arq}')
                for _, n in sens:
                    k = ('t', commit, arq, n)
                    if k not in vistos:
                        vistos.add(k)
                        prob.append(f'termo sensível nº {n} no histórico: commit {commit}, {arq}')
        r.wait()
    remoto = git(repo, 'remote', 'get-url', 'origin').stdout.strip()
    if remoto and 'github.com' in remoto and shutil.which('gh'):
        v = subprocess.run(['gh', 'repo', 'view', remoto, '--json', 'visibility'], capture_output=True, text=True)
        try:
            vis = json.loads(v.stdout)['visibility']
            if vis.upper() != 'PRIVATE':
                prob.append(f'o repositório do GitHub está {vis}: tem de ser PRIVATE')
        except (ValueError, KeyError):
            avisos.append(f'não consegui ler a visibilidade de {remoto} (gh auth status?)')
    elif remoto:
        avisos.append(f'já há remote: {remoto} (confira que é privado)')
    if shutil.which('gitleaks'):
        g = subprocess.run(['gitleaks', 'detect', '--source', str(repo), '--no-banner', '--redact'],
                           capture_output=True, text=True)
        if g.returncode not in (0,):
            prob.append('o gitleaks achou vazamento (rode "gitleaks detect --redact -v" no repositório)')
    else:
        avisos.append('gitleaks não está instalado: só a varredura própria rodou')
    return prob, avisos


def main(argv=None) -> int:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('repo', type=Path)
    ap.add_argument('--termos', type=Path)
    ap.add_argument('--sem-historia', action='store_true')
    a = ap.parse_args(argv)
    prob, avisos = conferir(a.repo.resolve(), ler_termos(a.termos), not a.sem_historia)
    for x in avisos:
        print('aviso:', x)
    for x in prob:
        print(x)
    if prob:
        print(f'\n{len(prob)} problema(s): NÃO envie. Corrija (e, se for no histórico, decida com o usuário) e rode de novo.')
        return 1
    nome = a.repo.resolve().name
    print('\nnenhum problema. O envio (o usuário roda, ou autoriza):')
    print(f'  gh repo create {nome} --private --source "{a.repo.resolve()}" --remote origin --push')
    return 0


if __name__ == '__main__':
    sys.exit(main())
