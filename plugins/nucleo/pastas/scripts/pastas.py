r"""O sistema de cores das pastas (skill cores-das-pastas, do plugin kit): aplicar, conferir, manter.

    python pastas.py instalar [--mae C:\CLAUDE-PROJETOS] [--lapide C:\VELHO ...]   (uma vez por PC; precisa de Pillow)
    python pastas.py aplicar [--ver] [projeto]      --ver: só conta, por projeto e por verbo; nada se escreve
    python pastas.py conferir                       sai 1 se achar algo (pastas.md, "A conferência")
    python pastas.py marcar <pasta> <verbo>         grava no mapa e pinta a pasta (e as filhas que herdam)
    python pastas.py legenda                        <mãe>\LEGENDA DAS PASTAS.html, do mesmo mapa
    python pastas.py vscode [--ver]                 Material Icon Theme + Peacock no .vscode\settings.json de cada projeto
    python pastas.py remover [pasta]                tira os nossos desktop.ini (o alheio fica)
    python pastas.py desligar-gancho [--settings ARQ]   tira do settings.json um gancho das cores antigo (o de antes do F1b)

O gancho das cores é do plugin nucleo (plugins\nucleo\hooks\hooks.json): liga onde o nucleo está ligado, sem gravar
nada em settings.json. O "ligar-gancho" ficou só para dizer isso.
O código e o mapa se acham pelo local.json (%LOCALAPPDATA%\claude-pastas\local.json), gravado pelo instalar e
consertado pelo instalar_kit.py do kit.
Nada aqui segue junção ou link.
"""
from __future__ import annotations

import argparse
import base64
import collections
import html
import json
import os
import subprocess
import sys
import time
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import regras as R  # noqa: E402

MODULO = AQUI.parent
MATCHER = 'Write|Edit|MultiEdit|NotebookEdit|Bash|PowerShell'
GANCHO_DO_PLUGIN = MODULO.parent / 'hooks' / 'hooks.json'     # plugins/nucleo/hooks/hooks.json


def e_gancho_nosso(comando: str) -> bool:
    """O gancho das cores, no caminho de antes do F2a (organizar-projetos) ou no de agora (nucleo/pastas)."""
    c = comando.replace('\\', '/')
    return 'gancho.py' in c and ('organizar-projetos/scripts/' in c or '/pastas/scripts/' in c)


# ---------------------------------------------------------------- contexto

class Contexto:
    def __init__(self, local: dict | None = None):
        local = local or R.ler_local()
        if not local:
            raise SystemExit('Este PC ainda não tem o sistema instalado: rode "pastas.py instalar" primeiro.')
        self.local = local
        self.mae = Path(local['mae'])
        self.modulo = Path(local.get('modulo') or MODULO)
        self.icones = Path(local['icones'])
        self.arq_mapa = self.modulo / 'mapa.json'
        self.dados = R.carregar_mapa(self.arq_mapa)
        self.mapa = R.Mapa(self.dados, self.mae)

    def ico(self, verbo: str) -> Path:
        return self.icones / f'{self.mapa.defs[verbo]["icone"]}.ico'


def _git_ignore_global() -> Path:
    r = subprocess.run(['git', 'config', '--global', 'core.excludesFile'], capture_output=True, text=True)
    if r.returncode == 0 and r.stdout.strip():
        return Path(os.path.expanduser(r.stdout.strip()))
    base = os.environ.get('XDG_CONFIG_HOME') or str(Path.home() / '.config')
    return Path(base) / 'git' / 'ignore'


def pôr_no_ignore(arquivo: Path, linha: str = 'desktop.ini') -> bool:
    texto = arquivo.read_text(encoding='utf-8') if arquivo.exists() else ''
    if linha in [l.strip() for l in texto.splitlines()]:
        return False
    arquivo.parent.mkdir(parents=True, exist_ok=True)
    arquivo.write_text(texto + ('' if not texto or texto.endswith('\n') else '\n') + linha + '\n', encoding='utf-8')
    return True


def cmd_instalar(mae: Path, lapides: list[str], ignore: Path | None = None, destino_local: Path | None = None) -> int:
    import desenho
    destino_local = destino_local or R.local_json()
    icones = destino_local.parent / 'icones'
    antigo = R.ler_local() if destino_local == R.local_json() else None
    local = {'mae': str(mae), 'modulo': str(MODULO), 'icones': str(icones),
             'lapides': sorted(set(lapides) | set((antigo or {}).get('lapides', [])))}
    if not mae.is_dir():
        raise SystemExit(f'a mãe {mae} não existe; crie a pasta antes')
    destino_local.parent.mkdir(parents=True, exist_ok=True)
    destino_local.write_text(json.dumps(local, ensure_ascii=False, indent=1), encoding='utf-8')
    feitos = desenho.montar(R.carregar_mapa(MODULO / 'mapa.json'), icones)
    print(f'local.json: {destino_local}\nícones: {len(feitos)} em {icones}')
    ign = ignore or _git_ignore_global()
    print(f'ignore global do git ({ign}): ' + ('desktop.ini acrescentado' if pôr_no_ignore(ign) else 'já tinha desktop.ini'))
    return 0


# ---------------------------------------------------------------- aplicar

def plano(ctx: Contexto, inicio=None):
    """Para cada pasta: (pasta, partes, verbo, ação) com ação em ok | escrever | tirar | nada."""
    for p, partes, v in ctx.mapa.andar(inicio):
        ini = p / 'desktop.ini'
        texto = R.ler_ini(ini)
        tipo, _ = R.marca_de(texto)
        if v == R.SEM_COR:
            yield p, partes, v, ('tirar' if tipo in ('nosso', '3009') else 'nada')
            continue
        desejado = R.montar_ini(ctx.ico(v), ctx.mapa.infotip(partes, v), v, texto)
        atual_ok = texto is not None and texto.replace('\r\n', '\n') == desejado.replace('\r\n', '\n')
        ro = sys.platform == 'win32' and bool(R.atributos(p) & 0x1)
        yield p, partes, v, ('ok' if atual_ok and not ro else 'escrever')


def _projeto(partes) -> str:
    return partes[0] if partes else '(a mãe)'


def cmd_aplicar(ctx: Contexto, ver: bool, projeto: str | None = None) -> int:
    inicio = ctx.mae / projeto if projeto else None
    faltam_icones = [v for v in ctx.mapa.defs if not ctx.ico(v).exists()]
    if faltam_icones and not ver:
        raise SystemExit(f'faltam ícones em {ctx.icones} ({faltam_icones}): rode "pastas.py instalar"')
    conta = collections.defaultdict(collections.Counter)
    acoes = collections.Counter()
    provisorias = []
    guarda = ctx.icones.parent / 'antes' / time.strftime('%Y%m%d_%H%M%S')
    guardados = 0
    for p, partes, v, acao in plano(ctx, inicio):
        conta[_projeto(partes)][v] += 1
        acoes[acao] += 1
        if v == R.PROVISORIA:
            provisorias.append(p)
        if ver or acao in ('ok', 'nada'):
            continue
        ini = p / 'desktop.ini'
        if ini.exists() and R.marca_de(R.ler_ini(ini))[0] in ('alheio', '3009'):
            # o desktop.ini de antes (alheio ou de 30/09) fica guardado: a volta é exata
            alvo = guarda / os.path.relpath(p, ctx.mae) / 'desktop.ini'
            alvo.parent.mkdir(parents=True, exist_ok=True)
            alvo.write_bytes(ini.read_bytes())
            guardados += 1
        if acao == 'tirar':
            R.tirar_ini(p)
        else:
            R.gravar_ini(p, R.montar_ini(ctx.ico(v), ctx.mapa.infotip(partes, v), v, R.ler_ini(p / 'desktop.ini')))
    for proj, c in sorted(conta.items()):
        print(f'{proj}: ' + ', '.join(f'{ctx.mapa.defs[v]["nome"] if v in ctx.mapa.defs else "sem cor"} {n}'
                                      for v, n in c.most_common()))
    verbo = 'a escrever' if ver else 'escritas'
    print(f'\npastas {verbo}: {acoes["escrever"]} · a tirar o ini: {acoes["tirar"]} · já certas: {acoes["ok"]}')
    if guardados:
        print(f'os {guardados} desktop.ini de antes (alheios ou de 30/09) foram guardados em {guarda}')
    if provisorias:
        print('provisórias (o Ettore escolhe a cor; depois "pastas.py marcar"):')
        for p in provisorias:
            print(f'  {p}')
    return 0


# ---------------------------------------------------------------- conferir

def _repos(ctx: Contexto) -> list[Path]:
    out = []
    try:
        filhas = list(os.scandir(ctx.mae))
    except OSError:
        return out
    for e in filhas:
        if e.is_dir(follow_symlinks=False) and not R.e_link(e.path) and (Path(e.path) / '.git').exists():
            out.append(Path(e.path))
    return out


def _aponta_para(texto: str) -> str:
    for l in (texto or '').splitlines():
        if l.lower().startswith('iconresource='):
            return l.split('=', 1)[1].rsplit(',', 1)[0]
    return ''


def _inis_abaixo(pasta: Path, mapa: R.Mapa, icones: Path | None = None):
    """Os desktop.ini de pasta pintada copiados para dentro de uma pasta sem cor (uma rodada que levou o ícone),
    sem seguir link: os do pacote de 30/09 e os nossos que apontam para os ícones instalados. Uma amostra que
    aponta para os próprios .ico (como as de prototipos-icones) não conta."""
    pilha = [pasta]
    instalados = os.path.normcase(str(icones)) if icones else None
    while pilha:
        d = pilha.pop()
        try:
            for e in os.scandir(d):
                if e.is_dir(follow_symlinks=False) and not R.e_link(e.path) and not mapa.nunca_cor(e.name):
                    pilha.append(Path(e.path))
                elif e.name.lower() == 'desktop.ini' and Path(d) != pasta:
                    texto = R.ler_ini(e.path)
                    tipo = R.marca_de(texto)[0]
                    if tipo == '3009' or (tipo == 'nosso' and (instalados is None or os.path.normcase(
                            _aponta_para(texto)).startswith(instalados))):
                        yield Path(d)
        except OSError:
            continue


def achados(ctx: Contexto) -> tuple[list[str], list[str]]:
    """(problemas, avisos). Problema faz o conferir sair 1."""
    prob, avisos = [], []
    nomes = collections.defaultdict(lambda: collections.defaultdict(set))
    for p, partes, v, acao in plano(ctx):
        ini = p / 'desktop.ini'
        texto = R.ler_ini(ini)
        tipo, verbo_ini = R.marca_de(texto)
        if v == R.SEM_COR:
            if tipo in ('nosso', '3009'):
                prob.append(f'ini em pasta sem cor (nunca-cor, rodada ou passageira): {p}')
            if partes and not ctx.mapa.nunca_cor(partes[-1]):
                prob += [f'ini dentro de pasta sem cor: {d}' for d in _inis_abaixo(p, ctx.mapa, ctx.icones)]
            continue
        if len(partes) >= 2:
            nomes[partes[0]][partes[-1]].add(v)
        if v == R.PROVISORIA:
            prob.append(f'provisória pendente (falta escolher a cor): {p}')
        if tipo is None or tipo == 'alheio':
            prob.append(f'pasta sem o nosso desktop.ini: {p} (deveria ser {v})')
        elif tipo == '3009':
            prob.append(f'ini do pacote de 30/09: {p}')
        elif verbo_ini != v:
            prob.append(f'verbo diferente do mapa: {p} ({verbo_ini}, o mapa diz {v})')
        elif acao == 'escrever':
            prob.append(f'ini desatualizado (dica, ícone ou +r): {p}')
        if tipo == 'nosso' and texto:
            for l in texto.splitlines():
                if l.lower().startswith('iconresource='):
                    ico = l.split('=', 1)[1].rsplit(',', 1)[0]
                    if not Path(ico).exists():
                        prob.append(f'ini aponta para .ico ausente: {p} -> {ico}')
                    if 'icones_pastas' in ico.lower():
                        prob.append(f'ini aponta para o pacote de 30/09: {p}')
        if sys.platform == 'win32' and R.atributos(p) & 0x1:
            prob.append(f'pasta com "somente leitura" (+r): {p}')
        if texto is not None and R.tem_marca_da_web(ini):
            prob.append(f'desktop.ini com marca da web (o Windows o ignora): {p}')
    for repo in _repos(ctx):
        r = subprocess.run(['git', '--no-optional-locks', '-C', str(repo), 'status', '--porcelain'],
                           capture_output=True, text=True, encoding='utf-8', errors='replace')
        vis = [l for l in r.stdout.splitlines() if 'desktop.ini' in l.lower()]
        if vis:
            prob.append(f'desktop.ini visível no git status de {repo.name}: {len(vis)} (ex.: {vis[0].strip()})')
    for lap in ctx.local.get('lapides', []):
        if not Path(lap).is_file():
            prob.append(f'lápide ausente: {lap} (deveria ser um arquivo)')
    plugin = json.loads(GANCHO_DO_PLUGIN.read_text(encoding='utf-8')) if GANCHO_DO_PLUGIN.is_file() else {}
    cmds = [h.get('command', '') for g in plugin.get('hooks', {}).get('PostToolUse', []) for h in g.get('hooks', [])]
    if not any(e_gancho_nosso(c) for c in cmds):
        prob.append(f'o gancho das cores não está no plugin nucleo ({GANCHO_DO_PLUGIN})')
    elif not any(Path(c.split('"')[1].replace('${CLAUDE_PLUGIN_ROOT}', str(MODULO.parent))).is_file()
                 for c in cmds if e_gancho_nosso(c) and c.count('"') >= 2):
        prob.append(f'o gancho do plugin nucleo aponta para um gancho.py que não existe ({GANCHO_DO_PLUGIN})')
    usuario = Path.home() / '.claude' / 'settings.json'
    if usuario.is_file():
        dados = json.loads(usuario.read_text(encoding='utf-8'))
        if any(e_gancho_nosso(h.get('command', '')) for g in dados.get('hooks', {}).get('PostToolUse', [])
               for h in g.get('hooks', [])):
            prob.append(f'o gancho das cores está também em {usuario} (dispara duas vezes): pastas.py desligar-gancho')
    for proj, por_nome in nomes.items():
        for nome, vs in por_nome.items():
            if len(vs) > 1:
                avisos.append(f'VS Code: em {proj}, as pastas "{nome}" têm verbos diferentes ({", ".join(sorted(vs))}); '
                              'o Material Icon Theme casa por nome e fica sem cor para elas')
    return prob, avisos


def cmd_conferir(ctx: Contexto) -> int:
    prob, avisos = achados(ctx)
    for a in avisos:
        print('aviso:', a)
    if not prob:
        print('conferência: 0 problemas')
        return 0
    for p in prob:
        print(p)
    print(f'\nconferência: {len(prob)} problema(s)')
    return 1


# ---------------------------------------------------------------- marcar e remover

def cmd_marcar(ctx: Contexto, pasta: Path, verbo: str) -> int:
    if verbo not in ctx.mapa.defs and verbo != R.SEM_COR:
        raise SystemExit(f'verbo desconhecido: {verbo}. Os que existem: {", ".join(ctx.mapa.defs)}, {R.SEM_COR}')
    partes = ctx.mapa.rel(pasta)
    if not partes:
        raise SystemExit(f'{pasta} não está dentro da mãe {ctx.mae}')
    nomes = Path(os.path.abspath(pasta)).parts[len(ctx.mae.parts):]
    projetos = {k.casefold(): k for k in ctx.dados.get('projetos', {})}
    if len(partes) == 1 and verbo in ('projeto-ia', 'dado-real'):
        # uma pasta da mãe que vira projeto: a marca é a raiz dele
        ctx.dados.setdefault('projetos', {}).setdefault(projetos.get(partes[0], nomes[0]), {'pastas': {}})['raiz'] = verbo
    elif partes[0] in projetos and len(partes) > 1:
        ctx.dados['projetos'][projetos[partes[0]]].setdefault('pastas', {})['/'.join(nomes[1:])] = verbo
    else:
        ctx.dados.setdefault('mae', {}).setdefault('pastas', {})['/'.join(nomes)] = verbo
    ctx.arq_mapa.write_text(json.dumps(ctx.dados, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(f'mapa: {"/".join(nomes)} = {verbo}')
    return _aplicar_em(Contexto(ctx.local), Path(pasta))


def _aplicar_em(ctx: Contexto, pasta: Path) -> int:
    n = 0
    for p, partes, v, acao in plano(ctx, pasta):
        if acao == 'escrever':
            R.gravar_ini(p, R.montar_ini(ctx.ico(v), ctx.mapa.infotip(partes, v), v, R.ler_ini(p / 'desktop.ini')))
            n += 1
        elif acao == 'tirar':
            R.tirar_ini(p)
            n += 1
    print(f'{n} pasta(s) atualizadas')
    return 0


def cmd_remover(ctx: Contexto, pasta: Path | None) -> int:
    n = 0
    inicio = Path(pasta) if pasta else ctx.mae
    pilha = [inicio]
    while pilha:
        d = pilha.pop()
        if R.tirar_ini(d):
            n += 1
        try:
            for e in os.scandir(d):
                if e.is_dir(follow_symlinks=False) and not R.e_link(e.path) and not ctx.mapa.nunca_cor(e.name):
                    pilha.append(Path(e.path))
        except OSError:
            pass
    print(f'{n} desktop.ini nossos tirados')
    return 0


# ---------------------------------------------------------------- legenda

def _png64(ctx: Contexto, verbo: str, px: int = 48) -> str:
    """O desenho embutido na legenda, dos quadros do módulo, na cor do mapa (não depende do .ico instalado)."""
    import desenho
    pasta = ctx.modulo / 'icones' if (ctx.modulo / 'icones' / 'quadros.json').exists() else desenho.QUADROS
    d = ctx.mapa.defs[verbo]
    return desenho._uri(desenho.quadros_na_cor(d['icone'], d['cor'], pasta)[px])


def _humano(chave: str) -> str:
    """O padrão do mapa em palavras: saida/[0-9][0-9][0-9][0-9]_* -> saida/DDMM_P (cada rodada)."""
    k = chave.replace('[0-9][0-9][0-9][0-9]_*', 'DDMM_P (cada rodada)')
    if k.endswith('/*'):
        k = k[:-2] + '/ (cada subpasta)'
    return k.replace('*', '…')


def legenda_html(ctx: Contexto) -> str:
    defs = ctx.mapa.defs
    e = html.escape
    verbos = ''.join(
        f'<tr><td><img src="{_png64(ctx, v)}" width="48" height="48" alt=""></td>'
        f'<td><b>{e(d["nome"])}</b><br>{e(d["dica"])}</td></tr>'
        for v, d in defs.items())
    projetos = ''
    for nome, conf in ctx.dados.get('projetos', {}).items():
        existe = (ctx.mae / nome).is_dir()
        linhas = ''.join(
            f'<li><code>{e(_humano(k))}</code> — {e(defs[v]["nome"] if v in defs else "sem cor (rodada ou passageira)")}</li>'
            for k, v in conf.get('pastas', {}).items())
        raiz = defs.get(conf.get('raiz'), {}).get('nome', '')
        projetos += (f'<h3>{e(nome)}{"" if existe else " (não existe neste PC)"}</h3>'
                     f'<p>A raiz: <b>{e(raiz)}</b>. As pastas sem linha aqui herdam a cor da pasta de cima.</p>'
                     f'<ul>{linhas}</ul>')
    lapides = ''.join(f'<li><code>{e(l)}</code></li>' for l in ctx.local.get('lapides', []))
    nunca = ', '.join(f'<code>{e(n)}</code>' for n in ctx.dados.get('nunca_cor', []))
    dados_reais = ''.join(
        f'<li><code>{e(nome)}</code> — {e((conf.get("dicas") or {}).get("", defs["dado-real"]["dica"]))}</li>'
        for nome, conf in ctx.dados.get('projetos', {}).items()
        if conf.get('raiz') == 'dado-real' and (ctx.mae / nome).is_dir())
    return f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Legenda das pastas</title>
<style>
:root {{ --fundo:#fafafa; --texto:#1b1b1b; --suave:#555; --linha:#ddd; }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --fundo:#161616; --texto:#eee; --suave:#aaa; --linha:#333; }} }}
:root[data-theme="dark"] {{ --fundo:#161616; --texto:#eee; --suave:#aaa; --linha:#333; }}
body {{ background:var(--fundo); color:var(--texto); font:15px/1.5 "Segoe UI", system-ui, sans-serif; margin:0; padding:16px; }}
main {{ max-width:900px; margin:auto; }} td {{ padding:6px 12px 6px 0; vertical-align:middle; border-bottom:1px solid var(--linha); }}
p, li {{ color:var(--suave); }} code {{ font-family:Consolas, monospace; }}
</style></head><body><main>
<h1>Legenda das pastas</h1>
<p>A cor de cada pasta diz <b>o que você faz com ela</b>. Gerada de <code>{e(str(ctx.arq_mapa))}</code> em
{time.strftime("%d/%m/%Y %H:%M")}; não edite à mão (rode <code>pastas.py legenda</code>).</p>
<table>{verbos}</table>
<h2>Regras</h2><ul>
<li>A pasta nova herda a cor da pasta de cima. Fora do mapa (na raiz de um projeto, ou na mãe), ela ganha o "?" e o Claude pergunta a cor.</li>
<li>Dentro de uma pasta vermelha (dado real), as filhas são "Não toco": o vermelho não passa adiante.</li>
<li>Nunca recebem cor: as pastas de rodada, as passageiras (o programa as cria e apaga) e {nunca}.</li>
<li>Fora do sistema: <code>C:\\GPT</code> e tudo fora de <code>{e(str(ctx.mae))}</code>.</li></ul>
<h2>As pastas de dado real</h2>
<p>Ficam ao lado do programa delas e fora de todo git; nunca vão ao GitHub. Só o programa mexe: não se move, não se
copia, não se abre por fora. O Claude não as lê (há uma regra <code>deny</code> no settings do Claude Code).</p>
<ul>{dados_reais or "<li>nenhuma neste PC</li>"}</ul>
<h2>O mapa de cada projeto</h2>{projetos}
<h2>As lápides</h2>
<p>Cada caminho velho virou um arquivo com o nome da pasta antiga. Programa que ainda use o caminho velho dá erro na
hora, em vez de recriar uma pasta vazia. Não apague: elas saem quando nenhum projeto citar mais o caminho velho.</p>
<ul>{lapides or "<li>nenhuma neste PC</li>"}</ul>
<h2>Aplicar num projeto ou num PC novo</h2>
<p>Projeto novo: o Claude propõe as linhas dele no <code>mapa.json</code>, você aprova, e ele roda
<code>pastas.py aplicar</code>. PC novo: o roteiro está na skill <code>/organizar-projetos</code> (plugin
<code>kit</code>, ligado no kit e na janela da raiz).</p>
</main></body></html>'''


def cmd_legenda(ctx: Contexto) -> int:
    destino = ctx.mae / R.LEGENDA
    destino.write_text(legenda_html(ctx), encoding='utf-8')
    print(destino)
    return 0


# ---------------------------------------------------------------- VS Code

def clones_do_projeto(ctx: Contexto, raiz: Path) -> tuple[list[dict], list[str]]:
    por_nome = collections.defaultdict(set)
    for p, partes, v in ctx.mapa.andar(raiz):
        if v in (R.SEM_COR, R.PROVISORIA) or len(partes) < 2:
            continue
        por_nome[p.name].add(v)
    conflitos = sorted(n for n, vs in por_nome.items() if len(vs) > 1)
    por_verbo = collections.defaultdict(list)
    for n, vs in por_nome.items():
        if len(vs) == 1:
            por_verbo[next(iter(vs))].append(n)
    clones = [{'name': f'claude-{v}', 'base': ctx.mapa.defs[v]['vscode_base'], 'color': ctx.mapa.defs[v]['cor'],
               'folderNames': sorted(ns, key=str.casefold)} for v, ns in sorted(por_verbo.items())]
    return clones, conflitos


def _rastreado(repo: Path, rel: str) -> bool:
    r = subprocess.run(['git', '-C', str(repo), 'ls-files', '--error-unmatch', rel], capture_output=True, text=True)
    return r.returncode == 0


def cmd_vscode(ctx: Contexto, ver: bool) -> int:
    status = 0
    for nome, conf in ctx.dados.get('projetos', {}).items():
        raiz = ctx.mae / nome
        if not raiz.is_dir() or not conf.get('peacock'):
            continue
        clones, conflitos = clones_do_projeto(ctx, raiz)
        arq = raiz / '.vscode' / 'settings.json'
        print(f'{nome}: {len(clones)} cores, {sum(len(c["folderNames"]) for c in clones)} nomes de pasta, '
              f'moldura {conf["peacock"]}' + (f'; sem cor no VS Code (conflito de nome): {conflitos}' if conflitos else ''))
        if ver:
            continue
        if (raiz / '.git').exists() and _rastreado(raiz, '.vscode/settings.json'):
            print(f'  PULO: {arq} é versionado no git; não mexo (decidir com o Ettore)')
            status = 1
            continue
        try:
            atual = json.loads(arq.read_text(encoding='utf-8')) if arq.exists() else {}
        except ValueError:
            print(f'  PULO: {arq} não é JSON puro (tem comentário?); não mexo')
            status = 1
            continue
        atual['material-icon-theme.folders.customClones'] = clones
        atual['peacock.color'] = conf['peacock']
        arq.parent.mkdir(exist_ok=True)
        arq.write_text(json.dumps(atual, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        if (raiz / '.git').is_dir():
            if pôr_no_ignore(raiz / '.git' / 'info' / 'exclude', '.vscode/settings.json'):
                print('  .vscode/settings.json no .git\\info\\exclude')
    return status


# ---------------------------------------------------------------- o gancho antigo no settings.json

def desligar_gancho(settings: Path) -> str:
    """Tira do settings.json o gancho das cores de antes do F1b; os outros ganchos ficam. Guarda cópia antes."""
    dados = json.loads(settings.read_text(encoding='utf-8')) if settings.exists() else {}
    ganchos = dados.get('hooks', {})
    lista = ganchos.get('PostToolUse', [])
    tinha = any(e_gancho_nosso(h.get('command', '')) for g in lista for h in g.get('hooks', []))
    if not tinha:
        return 'não havia gancho nosso'
    for g in lista:
        g['hooks'] = [h for h in g.get('hooks', []) if not e_gancho_nosso(h.get('command', ''))]
    lista[:] = [g for g in lista if g.get('hooks')]
    if not lista:
        del ganchos['PostToolUse']
    if not ganchos:
        del dados['hooks']
    if settings.exists():
        copia = settings.with_name(f'{settings.name}.antes-gancho-{time.strftime("%Y%m%d_%H%M%S")}')
        copia.write_bytes(settings.read_bytes())
    settings.parent.mkdir(parents=True, exist_ok=True)
    settings.write_text(json.dumps(dados, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return 'gancho desligado'


# ---------------------------------------------------------------- main

def main(argv=None) -> int:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest='cmd', required=True)
    s = sub.add_parser('instalar')
    s.add_argument('--mae', type=Path, default=Path(r'C:\CLAUDE-PROJETOS'))
    s.add_argument('--lapide', action='append', default=[])
    s = sub.add_parser('aplicar')
    s.add_argument('--ver', action='store_true')
    s.add_argument('projeto', nargs='?')
    sub.add_parser('conferir')
    s = sub.add_parser('marcar')
    s.add_argument('pasta', type=Path)
    s.add_argument('verbo')
    sub.add_parser('legenda')
    s = sub.add_parser('vscode')
    s.add_argument('--ver', action='store_true')
    s = sub.add_parser('remover')
    s.add_argument('pasta', type=Path, nargs='?')
    for nome in ('ligar-gancho', 'desligar-gancho'):
        s = sub.add_parser(nome)
        s.add_argument('--settings', type=Path, default=Path.home() / '.claude' / 'settings.json')
    a = ap.parse_args(argv)
    if a.cmd == 'instalar':
        return cmd_instalar(a.mae, a.lapide)
    if a.cmd == 'ligar-gancho':
        print(f'Nada a gravar: o gancho das cores é do plugin nucleo ({GANCHO_DO_PLUGIN}) e liga onde o nucleo '
              'está ligado. Para conferir: pastas.py conferir; numa janela nova, uma pasta nova num projeto ganha a cor.')
        return 0
    if a.cmd == 'desligar-gancho':
        print(desligar_gancho(a.settings))
        print('Abra uma janela nova do Claude Code: os ganchos são lidos ao abrir a sessão.')
        return 0
    ctx = Contexto()
    if a.cmd == 'aplicar':
        return cmd_aplicar(ctx, a.ver, a.projeto)
    if a.cmd == 'conferir':
        return cmd_conferir(ctx)
    if a.cmd == 'marcar':
        return cmd_marcar(ctx, a.pasta, a.verbo)
    if a.cmd == 'legenda':
        return cmd_legenda(ctx)
    if a.cmd == 'vscode':
        return cmd_vscode(ctx, a.ver)
    if a.cmd == 'remover':
        return cmd_remover(ctx, a.pasta)
    return 2


if __name__ == '__main__':
    sys.exit(main())
