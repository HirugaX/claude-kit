r"""O núcleo do sistema de cores das pastas: o mapa, a regra de cada pasta e o desktop.ini.

Só biblioteca padrão: o gancho (gancho.py) importa este arquivo a cada ferramenta do Claude e não pode
depender de Pillow.

Três cuidados que valem para tudo aqui:
  - caminho se compara por PARTES e sem diferenciar maiúscula (NTFS), nunca por startswith: "desosp-app"
    é prefixo de "desosp-app-dados";
  - nunca se segue junção nem link simbólico (o os.walk do Python 3.12 entra em junção; havia junções velhas
    apontando para lápide): andar() e verbo_de() pulam todo ponto de nova análise;
  - o desktop.ini se grava em UTF-16 LE com BOM e CRLF, oculto e de sistema; a pasta fica com +s e SEM +r
    (o +r deixa cópia impossível de apagar: WinError 5, 01/10).

A regra de cada pasta (plano 4.2), nesta ordem:
  1. nome na lista nunca_cor -> sem cor, e não desce;
  2. entrada explícita no mapa (exata, depois padrão com * ? [ ]) -> vale ela;
  3. senão herda da mãe, pelo campo "filhas" do verbo (dado real -> Não toco; Projeto com IA -> provisória;
     provisória -> sem cor);
  4. "sem-cor" é a pasta de rodada ou passageira: nenhum desktop.ini e não desce.
"""
from __future__ import annotations

import fnmatch
import json
import os
import stat
import sys
from pathlib import Path

MARCA = '; claude-pastas v1'          # 1ª linha do nosso desktop.ini, seguida do verbo
MARCA_3009 = '; DESOSP icones_pastas'  # o pacote de 30/09, que este substitui
SEM_COR = 'sem-cor'
PROVISORIA = 'provisoria'
LEGENDA = 'LEGENDA DAS PASTAS.html'
NOSSAS_CHAVES = {'iconresource', 'iconfile', 'iconindex', 'infotip', 'confirmfileop'}

_REPARSE = 0x400      # FILE_ATTRIBUTE_REPARSE_POINT: junção, link simbólico (e marcador de nuvem)
_READONLY, _HIDDEN, _SYSTEM, _NORMAL = 0x1, 0x2, 0x4, 0x80


# ---------------------------------------------------------------- onde mora cada coisa neste PC

def local_json() -> Path:
    """%LOCALAPPDATA%\\claude-pastas\\local.json: a mãe, o módulo, os ícones e as lápides DESTE PC."""
    if os.environ.get('CLAUDE_PASTAS_LOCAL'):
        return Path(os.environ['CLAUDE_PASTAS_LOCAL'])
    base = os.environ.get('LOCALAPPDATA') or str(Path.home() / 'AppData' / 'Local')
    return Path(base) / 'claude-pastas' / 'local.json'


def ler_local() -> dict | None:
    try:
        return json.loads(local_json().read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return None


def carregar_mapa(caminho) -> dict:
    return json.loads(Path(caminho).read_text(encoding='utf-8'))


# ---------------------------------------------------------------- junções e atributos

def e_link(p) -> bool:
    """Junção, link simbólico ou outro ponto de nova análise: nunca se entra."""
    try:
        st = os.lstat(p)
    except OSError:
        return False
    return stat.S_ISLNK(st.st_mode) or bool(getattr(st, 'st_file_attributes', 0) & _REPARSE)


def _entrada_e_link(e: os.DirEntry) -> bool:
    if e.is_symlink():
        return True
    return bool(getattr(e.stat(follow_symlinks=False), 'st_file_attributes', 0) & _REPARSE)


def atributos(p) -> int:
    return getattr(os.stat(p, follow_symlinks=False), 'st_file_attributes', 0)


def por_atributos(p, valor: int) -> None:
    if sys.platform == 'win32':
        import ctypes
        if not ctypes.windll.kernel32.SetFileAttributesW(str(p), valor):
            raise OSError(f'SetFileAttributes falhou em {p}')


def avisar_explorador(pasta) -> None:
    """Pede ao Explorador que releia a pasta (SHCNE_UPDATEITEM, SHCNF_PATHW)."""
    if sys.platform == 'win32':
        import ctypes
        try:
            ctypes.windll.shell32.SHChangeNotify(0x00002000, 0x0005, str(pasta), None)
        except Exception:
            pass


# ---------------------------------------------------------------- o mapa e a regra

def _partes_chave(k: str) -> tuple[str, ...]:
    return tuple(x.casefold() for x in k.replace('\\', '/').strip('/').split('/') if x)


def _preparar(conf: dict) -> dict:
    exatas, padroes, dicas = {}, [], {}
    for k, v in (conf.get('pastas') or {}).items():
        partes = _partes_chave(k)
        if any(c in k for c in '*?['):
            padroes.append((partes, v))
        else:
            exatas[partes] = v
    for k, t in (conf.get('dicas') or {}).items():
        dicas[_partes_chave(k)] = t
    return {'raiz': conf.get('raiz') or conf.get('marca'), 'exatas': exatas, 'padroes': padroes, 'dicas': dicas}


class Mapa:
    """O mapa (mapa.json) aplicado a uma pasta-mãe."""

    def __init__(self, dados: dict, mae):
        self.dados = dados
        self.mae = Path(os.path.abspath(mae))
        self.defs = {**dados.get('verbos', {}), **dados.get('marcas', {})}
        self.nunca = [n.casefold() for n in dados.get('nunca_cor', [])]
        self.projetos = {k.casefold(): _preparar(v) for k, v in (dados.get('projetos') or {}).items()}
        self.conf_mae = _preparar(dados.get('mae') or {})
        validos = set(self.defs) | {SEM_COR}
        ruins = [(k, v) for c in [self.conf_mae, *self.projetos.values()]
                 for k, v in [*c['exatas'].items(), *c['padroes']] if v not in validos]
        ruins += [(p, c['raiz']) for p, c in self.projetos.items() if c['raiz'] and c['raiz'] not in validos]
        if ruins:
            raise ValueError(f'verbo desconhecido no mapa: {ruins[:5]}')

    # -- caminhos
    def rel(self, pasta) -> tuple[str, ...] | None:
        """As partes de `pasta` abaixo da mãe (minúsculas), ou None se estiver fora dela."""
        a = Path(os.path.normcase(os.path.abspath(pasta))).parts
        b = Path(os.path.normcase(str(self.mae))).parts
        if tuple(x.casefold() for x in a[:len(b)]) != tuple(x.casefold() for x in b):
            return None
        return tuple(x.casefold() for x in a[len(b):])

    def nunca_cor(self, nome: str) -> bool:
        n = nome.casefold()
        return any(fnmatch.fnmatchcase(n, p) for p in self.nunca)

    @staticmethod
    def _entrada(conf: dict, partes: tuple[str, ...]):
        v = conf['exatas'].get(partes)
        if v:
            return v
        for padrao, valor in conf['padroes']:
            if len(padrao) == len(partes) and all(fnmatch.fnmatchcase(a, b) for a, b in zip(partes, padrao)):
                return valor
        return None

    def verbo(self, partes: tuple[str, ...], verbo_mae: str | None) -> str:
        """O verbo de uma pasta, dado o verbo da pasta de cima (a regra 4.2)."""
        if not partes:
            return self.conf_mae['raiz'] or SEM_COR
        if self.nunca_cor(partes[-1]):
            return SEM_COR
        v = self._entrada(self.conf_mae, partes)
        if v:
            return v
        proj = self.projetos.get(partes[0])
        if proj is not None:
            if len(partes) == 1 and proj['raiz']:
                return proj['raiz']
            v = self._entrada(proj, partes[1:]) if len(partes) > 1 else None
            if v:
                return v
        if verbo_mae in (None, SEM_COR):
            return SEM_COR
        return self.defs.get(verbo_mae, {}).get('filhas', verbo_mae)

    def verbo_de(self, pasta) -> str | None:
        """O verbo de qualquer pasta, descendo da mãe (None se estiver fora dela)."""
        partes = self.rel(pasta)
        if partes is None:
            return None
        nomes = Path(os.path.abspath(pasta)).parts[len(self.mae.parts):]
        atual, v = self.mae, self.verbo((), None)
        if e_link(atual):
            return SEM_COR
        for i, nome in enumerate(nomes):
            atual = atual / nome
            if v == SEM_COR or e_link(atual):
                return SEM_COR
            v = self.verbo(partes[:i + 1], v)
        return v

    def andar(self, inicio=None, max_nivel: int | None = None):
        """(pasta, partes, verbo) de cada pasta a partir de `inicio`, sem seguir junção nem link e sem
        descer em pasta sem cor."""
        inicio = Path(os.path.abspath(inicio or self.mae))
        partes = self.rel(inicio)
        v = self.verbo_de(inicio)
        if partes is None or v is None or not inicio.is_dir():
            return
        pilha = [(inicio, partes, v, 0)]
        while pilha:
            p, partes, v, n = pilha.pop()
            yield p, partes, v
            if v == SEM_COR or (max_nivel is not None and n >= max_nivel):
                continue
            try:
                entradas = sorted(os.scandir(p), key=lambda e: e.name.casefold(), reverse=True)
            except OSError:
                continue
            for e in entradas:
                try:
                    if not e.is_dir(follow_symlinks=False) or _entrada_e_link(e):
                        continue
                except OSError:
                    continue
                filhas = partes + (e.name.casefold(),)
                pilha.append((Path(e.path), filhas, self.verbo(filhas, v), n + 1))

    def dica(self, partes: tuple[str, ...], verbo: str) -> str:
        d = self.conf_mae['dicas'].get(partes)
        if not d and partes and partes[0] in self.projetos:
            d = self.projetos[partes[0]]['dicas'].get(partes[1:])
        return d or self.defs.get(verbo, {}).get('dica', '')

    def infotip(self, partes: tuple[str, ...], verbo: str) -> str:
        nome = self.defs[verbo]['nome']
        return f'{nome} — {self.dica(partes, verbo)} Legenda: {self.mae / LEGENDA}'


# ---------------------------------------------------------------- o desktop.ini

def ler_ini(ini) -> str | None:
    try:
        b = Path(ini).read_bytes()
    except OSError:
        return None
    if b.startswith(b'\xff\xfe'):
        return b[2:].decode('utf-16-le', errors='replace')
    if b.startswith(b'\xfe\xff'):
        return b[2:].decode('utf-16-be', errors='replace')
    for cod in ('utf-8-sig', 'mbcs' if sys.platform == 'win32' else 'latin-1'):
        try:
            return b.decode(cod)
        except (UnicodeDecodeError, LookupError):
            continue
    return b.decode('latin-1')


def marca_de(texto: str | None) -> tuple[str | None, str | None]:
    """('nosso', verbo) | ('3009', None) | ('alheio', None) | (None, None) quando não há ini."""
    if texto is None:
        return None, None
    for linha in texto.splitlines():
        s = linha.strip()
        if s.startswith(MARCA):
            resto = s[len(MARCA):].split()
            return 'nosso', (resto[0] if resto else None)
    if MARCA_3009 in texto:
        return '3009', None
    return 'alheio', None


def _secoes(texto: str) -> tuple[list[str], list[tuple[str, list[str]]]]:
    """Linhas antes da 1ª seção e a lista (cabeçalho, linhas) de cada seção, sem as nossas marcas."""
    antes, secoes = [], []
    for linha in texto.splitlines():
        s = linha.strip()
        if s.startswith(MARCA) or s.startswith(MARCA_3009):
            continue
        if s.startswith('[') and s.endswith(']'):
            secoes.append((s, []))
        elif secoes:
            secoes[-1][1].append(linha)
        elif s:
            antes.append(linha)
    return antes, secoes


def _sem_nossas_chaves(cab: str, linhas: list[str]) -> list[str]:
    if cab.casefold() != '[.shellclassinfo]':
        return linhas
    return [l for l in linhas if l.split('=', 1)[0].strip().casefold() not in NOSSAS_CHAVES]


def montar_ini(icone, infotip: str, verbo: str, existente: str | None = None) -> str:
    """O texto do desktop.ini. Do ini alheio (ex.: [LocalizedFileNames]) ficam as seções e as chaves que não
    são nossas; o de 30/09 se troca inteiro. Nunca ConfirmFileOp."""
    nossas = [f'IconResource={icone},0', f'InfoTip={infotip}']
    antes, secoes = ([], [])
    if existente and marca_de(existente)[0] != '3009':
        antes, secoes = _secoes(existente)
    saida = [f'{MARCA} {verbo}', *antes, '[.ShellClassInfo]', *nossas]
    for cab, linhas in secoes:
        if cab.casefold() == '[.shellclassinfo]':
            saida += [l for l in _sem_nossas_chaves(cab, linhas) if l.strip()]
    for cab, linhas in secoes:
        if cab.casefold() != '[.shellclassinfo]':
            saida += [cab, *[l for l in linhas if l.strip()]]
    return '\r\n'.join(saida) + '\r\n'


def sem_o_nosso(texto: str) -> str | None:
    """O ini alheio sem as nossas linhas, ou None se não sobrar nada dele."""
    antes, secoes = _secoes(texto)
    resto = []
    for cab, linhas in secoes:
        ls = [l for l in _sem_nossas_chaves(cab, linhas) if l.strip()]
        if ls:
            resto += [cab, *ls]
    if not resto and not [a for a in antes if a.strip()]:
        return None
    return '\r\n'.join([*antes, *resto]) + '\r\n'


def _bytes_ini(texto: str) -> bytes:
    return b'\xff\xfe' + texto.replace('\r\n', '\n').replace('\n', '\r\n').encode('utf-16-le')


def gravar_ini(pasta, texto: str) -> bool:
    """Grava o desktop.ini (só se mudou) e acerta os atributos: ini oculto e de sistema; pasta +s e -r.
    Devolve True se escreveu ou mudou atributo."""
    pasta = Path(pasta)
    ini = pasta / 'desktop.ini'
    dados = _bytes_ini(texto)
    mudou = False
    try:
        atual = ini.read_bytes()
    except OSError:
        atual = None
    if atual != dados:
        if atual is not None:
            por_atributos(ini, _NORMAL)          # o open('wb') recusa arquivo oculto e de sistema
        with open(ini, 'wb') as f:
            f.write(dados)
        mudou = True
    if sys.platform == 'win32':
        a = atributos(ini)
        if (a & (_HIDDEN | _SYSTEM)) != (_HIDDEN | _SYSTEM):
            por_atributos(ini, (a | _HIDDEN | _SYSTEM) & ~_NORMAL)
            mudou = True
        a = atributos(pasta)
        novo = (a | _SYSTEM) & ~_READONLY
        if novo != a:
            por_atributos(pasta, novo)
            mudou = True
    if mudou:
        avisar_explorador(pasta)
    return mudou


def tirar_ini(pasta) -> bool:
    """Tira o nosso desktop.ini. O ini alheio fica, sem as nossas linhas. Devolve True se mexeu."""
    pasta = Path(pasta)
    ini = pasta / 'desktop.ini'
    texto = ler_ini(ini)
    if marca_de(texto)[0] not in ('nosso', '3009'):
        return False
    resto = sem_o_nosso(texto) if marca_de(texto)[0] == 'nosso' else None
    por_atributos(ini, _NORMAL)
    if resto is None:
        ini.unlink()
        if sys.platform == 'win32':
            por_atributos(pasta, atributos(pasta) & ~(_SYSTEM | _READONLY) or _NORMAL)
    else:
        ini.write_bytes(_bytes_ini(resto))
        por_atributos(ini, _HIDDEN | _SYSTEM)
    avisar_explorador(pasta)
    return True


def tem_marca_da_web(ini) -> bool:
    """O Windows ignora desktop.ini baixado da internet (Zone.Identifier), desde junho de 2026."""
    return sys.platform == 'win32' and os.path.exists(f'{ini}:Zone.Identifier')
