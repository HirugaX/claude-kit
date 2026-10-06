# -*- coding: utf-8 -*-
"""
checa_kit.py: procura o que não pode ir para o git do kit (ADR-0001).

O que acusa:
  segredo        token do GitHub, chave da Anthropic, AWS ou Google, chave privada, senha atribuída no texto
  cpf            CPF com dígito verificador válido (com ou sem pontuação)
  cns            Cartão Nacional de Saúde (15 dígitos, soma válida)
  telefone       telefone brasileiro com DDD e separador
  caminho_dado   caminho que entra numa pasta de dado e termina num arquivo de dado
  arquivo_dado   planilha, PDF, banco ou pickle versionado
  nome           nome de paciente (pelo dicionário de hashes do desosp-hc, quando existe neste PC)
Mostra só arquivo:linha:tipo, nunca o trecho encontrado.

Leitura declarada (ADR-0002): para "nome", importa as funções carrega() e varre_texto() de
C:\\CLAUDE-PROJETOS\\desosp-hc\\scripts\\checa_privacidade.py, que leem só o dicionário de hashes do HC. Sem ele
(outro PC, ou dicionário ausente), avisa e segue com o resto.

Uso:
  python scripts/checa_kit.py --tudo        varre tudo o que o git versiona (ou versionaria)
  python scripts/checa_kit.py --staged      varre só o próximo commit (gancho pre-commit)
  python scripts/checa_kit.py ARQ1 ARQ2     varre arquivos avulsos (caminho relativo à raiz do kit)
Exceções conferidas, com o motivo num comentário: scripts/checa_kit_ignorar.txt, uma por linha (arquivo:linha,
arquivo:* ou arquivo:*:tipo). Código de saída: 0 limpo, 1 achou algo.
"""
import argparse
import importlib.util
import io
import os
import re
import subprocess
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

RAIZ = Path(__file__).resolve().parent.parent
IGNORAR = RAIZ / 'scripts' / 'checa_kit_ignorar.txt'
CHECADOR_HC = Path(os.environ.get('CHECADOR_HC', r'C:\CLAUDE-PROJETOS\desosp-hc\scripts\checa_privacidade.py'))

IMAGEM = {'.png', '.ico', '.jpg', '.jpeg', '.gif', '.webp'}
DADO = {'.xlsx', '.xlsm', '.xls', '.csv', '.pdf', '.db', '.sqlite', '.sqlite3', '.pkl', '.parquet'}

SEGREDOS = [re.compile(p) for p in (
    r'ghp_[A-Za-z0-9]{36}', r'github_pat_[A-Za-z0-9_]{22,}', r'gh[ousr]_[A-Za-z0-9]{36}',
    r'sk-ant-[A-Za-z0-9_-]{20,}', r'AKIA[0-9A-Z]{16}', r'AIza[0-9A-Za-z_-]{35}', r'xox[baprs]-[A-Za-z0-9-]{10,}',
    r'-----BEGIN [A-Z ]*PRIVATE KEY-----',
    r'(?i)\b(?:senha|password|passwd|secret|token|api[_-]?key)\b\s*[:=]\s*["\'][^"\'\s]{8,}["\']',
)]
CPF = re.compile(r'(?<![\d.])(\d{3}\.\d{3}\.\d{3}-\d{2}|\d{11})(?![\d-])')
CNS = re.compile(r'(?<!\d)([1-9]\d{2}[ .]?\d{4}[ .]?\d{4}[ .]?\d{4})(?!\d)')
TELEFONE = re.compile(r'(?<![\d/.-])(?:\+?55[\s-]?)?\(?[1-9]{2}\)?[\s-]?9?\d{4}[\s-]\d{4}(?![\d/-])')
PASTAS_DADO = r'(?:desosp-app-dados|desosp-app-backups|workspace_dev|para_o_app|historico|entrada|planilhas|privado|_envios|PLANILHA_HC)'
CAMINHO_DADO = re.compile(PASTAS_DADO + r'[\\/]+[^\s`\'"|)\]]*\.(?:' + '|'.join(e[1:] for e in sorted(DADO)) + r'|docx|msg|eml)\b',
                          re.IGNORECASE)


def cpf_valido(d):
    if len(d) != 11 or d == d[0] * 11:
        return False
    for n in (9, 10):
        dv = sum(int(d[i]) * (n + 1 - i) for i in range(n)) * 10 % 11 % 10
        if dv != int(d[n]):
            return False
    return True


def cns_valido(d):
    return len(d) == 15 and d[0] in '12789' and sum(int(d[i]) * (15 - i) for i in range(15)) % 11 == 0


def varre_linha(linha):
    """Os tipos achados numa linha (sem repetir tipo)."""
    tipos = []
    if any(p.search(linha) for p in SEGREDOS):
        tipos.append('segredo')
    if any(cpf_valido(re.sub(r'\D', '', m)) for m in CPF.findall(linha)):
        tipos.append('cpf')
    if any(cns_valido(re.sub(r'\D', '', m)) for m in CNS.findall(linha)):
        tipos.append('cns')
    if TELEFONE.search(linha):
        tipos.append('telefone')
    if CAMINHO_DADO.search(linha):
        tipos.append('caminho_dado')
    return tipos


def texto_docx(dados):
    w = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    linhas = []
    with zipfile.ZipFile(io.BytesIO(dados)) as z:
        for n in z.namelist():
            if re.fullmatch(r'word/(document|header\d*|footer\d*|footnotes|endnotes|comments)\.xml', n):
                for par in ET.fromstring(z.read(n)).iter(f'{w}p'):
                    linhas.append(''.join(t.text or '' for t in par.iter(f'{w}t')))
    return '\n'.join(linhas).encode('utf-8')


def _git(*args):
    r = subprocess.run(['git', '-C', str(RAIZ), *args], capture_output=True)
    if r.returncode:
        sys.exit(f'git {args[0]} falhou: {r.stderr.decode("utf-8", "replace").strip()}')
    return r.stdout


def arquivos(tudo, staged, avulsos):
    if staged:
        return _git('diff', '--cached', '--name-only', '--diff-filter=ACMR', '-z').decode('utf-8').split('\0')[:-1]
    if tudo:
        return _git('ls-files', '--cached', '--others', '--exclude-standard', '-z').decode('utf-8').split('\0')[:-1]
    return [Path(a).as_posix() for a in avulsos]


def conteudo(rel, staged):
    return _git('show', f':{rel}') if staged else (RAIZ / rel).read_bytes()


def checador_de_nomes():
    """As funções do checador do HC e o dicionário dele, ou None (com o motivo)."""
    if not CHECADOR_HC.exists():
        return None, f'sem o checador do HC ({CHECADOR_HC})'
    spec = importlib.util.spec_from_file_location('checa_privacidade_hc', CHECADOR_HC)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    try:
        nomes, mos, senha = mod.carrega()
    except SystemExit:
        return None, 'o HC está sem dicionário de nomes'
    return (lambda rel, dados: mod.varre_texto(rel, dados, nomes, mos, senha)), 'com o dicionário do HC'


def ignorados():
    if not IGNORAR.exists():
        return set()
    return {l.strip() for l in IGNORAR.read_text(encoding='utf-8').splitlines() if l.strip() and not l.startswith('#')}


def varre(lista, staged=False):
    nomes, como = checador_de_nomes()
    achados = []
    for rel in lista:
        ext = Path(rel).suffix.lower()
        if ext in DADO:
            achados.append((rel, 0, 'arquivo_dado'))
            continue
        if ext in IMAGEM:
            continue
        dados = conteudo(rel, staged)
        if ext == '.docx':
            dados = texto_docx(dados)
        elif b'\0' in dados[:4096]:
            achados.append((rel, 0, 'binario'))
            continue
        for i, linha in enumerate(dados.decode('utf-8', errors='replace').splitlines(), 1):
            achados += [(rel, i, t) for t in varre_linha(linha)]
        if nomes:
            achados += nomes(rel, dados)
    fora = ignorados()
    achados = [a for a in achados if f'{a[0]}:{a[1]}' not in fora and f'{a[0]}:*' not in fora
               and f'{a[0]}:*:{a[2]}' not in fora]
    return achados, como


def main():
    ap = argparse.ArgumentParser(description='segredo, CPF, CNS, telefone, caminho de dado e nome fora do git do kit')
    ap.add_argument('arquivos', nargs='*')
    ap.add_argument('--tudo', action='store_true')
    ap.add_argument('--staged', action='store_true')
    a = ap.parse_args()
    if not (a.tudo or a.staged or a.arquivos):
        ap.error('diga --tudo, --staged ou os arquivos')
    lista = arquivos(a.tudo, a.staged, a.arquivos)
    achados, como = varre(lista, a.staged)
    for rel, linha, tipo in sorted(set(achados)):
        print(f'{rel}:{linha}:{tipo}')
    print(f'{len(lista)} arquivo(s), {len(set(achados))} achado(s); nomes: {como}', file=sys.stderr)
    sys.exit(1 if achados else 0)


if __name__ == '__main__':
    main()
