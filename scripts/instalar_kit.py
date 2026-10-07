r"""Instala e confere o kit do Claude neste PC (substitui o ligar_claude.py; F1b, 07/10/2026).

    python <kit>\scripts\instalar_kit.py                 # instala; o que já está certo fica como está
    python <kit>\scripts\instalar_kit.py --verificar     # só confere; sai com 1 se houver achado
    python <kit>\scripts\instalar_kit.py --trecho TIPO   # o enabledPlugins de um tipo de projeto
                                                         # (codigo, pesquisa-estudo, pessoal, kit, raiz, teste)

As skills moram no kit, em plugins\<grupo>\skills\<skill>; o kit é um marketplace local e os plugins
carregam da própria pasta (a edição vale na sessão seguinte). Quem liga cada grupo, e onde, é o
config\plugins.json. O que a instalação faz:
  1. registra o marketplace do kit e os de fora;
  2. liga no ~\.claude\settings.json os grupos e plugins de escopo de usuário (os de projeto, cada
     projeto liga na sua fase: veja --trecho);
  3. git config core.hooksPath .githooks no kit;
  4. tira de ~\.claude\skills as junções antigas que apontam para o kit (a lista vai para ~\.claude\backups);
  5. o CLAUDE.md pessoal: ~\.claude\CLAUDE.md com só a linha de import do CLAUDE.md do kit (o import
     sobrevive ao git pull; o hardlink de antes se separava);
  6. o local.json das cores (%LOCALAPPDATA%\claude-pastas), se existir: o "modulo" aponta para o kit;
  7. a janela da raiz: o grupo kit no .claude\settings.json da pasta-mãe, quando o plugin kit existir.
No fim imprime o comando da política do safety-net, que é do Ettore (o plugin não deixa o Claude
mudar a própria política).
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

KIT = Path(__file__).resolve().parents[1]
MKT = 'claude-kit'
NAO_MEXER = {'synced'}          # skills sincronizadas pelo claude.ai: quem cuida é o próprio Claude


@dataclass
class Ambiente:
    kit: Path = KIT
    casa: Path = Path.home() / '.claude'
    local_json: Path | None = (Path(os.environ['LOCALAPPDATA']) / 'claude-pastas' / 'local.json'
                               if os.environ.get('LOCALAPPDATA') else None)
    claude: Callable[[list[str]], subprocess.CompletedProcess] | None = None   # roda `claude ...` (troca nos testes)
    feito: list[str] = field(default_factory=list)
    no_painel: list[str] = field(default_factory=list)     # sem o CLI: os comandos para colar no Claude Code

    @property
    def mae(self) -> Path:
        return self.kit.parent

    def rodar_claude(self, args: list[str]) -> subprocess.CompletedProcess:
        """Roda `claude ...`; sem o CLI no PATH (a extensão do VS Code não o põe lá), devolve o código 127."""
        if self.claude:
            return self.claude(args)
        exe = shutil.which('claude')
        if not exe:
            return subprocess.CompletedProcess(args, 127, '', 'o comando claude não está no PATH')
        return subprocess.run([exe, *args], capture_output=True, text=True, encoding='utf-8', errors='replace')


# ---------------------------------------------------------------- leitura

def _json(p: Path) -> dict:
    try:
        return json.loads(p.read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return {}


def _gravar_json(p: Path, d: dict, backup_dir: Path | None = None) -> None:
    if backup_dir and p.exists():
        backup_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, backup_dir / f'{p.name}.{time.strftime("%Y-%m-%d_%H%M%S")}_instalar_kit')
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def config(a: Ambiente) -> dict:
    return _json(a.kit / 'config' / 'plugins.json')


def plugins_do_kit(a: Ambiente) -> dict[str, list[str]]:
    """Grupo -> skills, pelo marketplace.json (só os que existem de fato na pasta)."""
    mkt = _json(a.kit / '.claude-plugin' / 'marketplace.json')
    out = {}
    for p in mkt.get('plugins', []):
        pasta = (a.kit / p['source']).resolve()
        sk = pasta / 'skills'
        out[p['name']] = sorted(d.name for d in sk.iterdir() if (d / 'SKILL.md').is_file()) if sk.is_dir() else []
    return out


def ligados_usuario(a: Ambiente) -> dict[str, bool]:
    return _json(a.casa / 'settings.json').get('enabledPlugins', {})


def _alvo_juncao(p: Path) -> str:
    try:
        return os.readlink(p)
    except OSError:
        return ''


def _e_juncao(p: Path) -> bool:
    return os.path.isjunction(p) if hasattr(os.path, 'isjunction') else p.is_symlink()


def juncoes_do_kit(a: Ambiente) -> list[Path]:
    """Junções em ~\\.claude\\skills que apontam para dentro do kit (inclusive as que perderam o alvo)."""
    pasta = a.casa / 'skills'
    if not pasta.is_dir():
        return []
    kit = str(a.kit.resolve()).lower().replace('\\\\?\\', '')
    out = []
    for p in sorted(pasta.iterdir()):
        if p.name in NAO_MEXER or not _e_juncao(p):
            continue
        alvo = _alvo_juncao(p).lower().replace('\\\\?\\', '')
        if alvo.startswith(kit) or os.sep + 'claude-kit' + os.sep in alvo:
            out.append(p)
    return out


def skills_de_usuario(a: Ambiente) -> list[str]:
    pasta = a.casa / 'skills'
    if not pasta.is_dir():
        return []
    return sorted(p.name for p in pasta.iterdir()
                  if p.name not in NAO_MEXER and not p.name.startswith('.') and (p / 'SKILL.md').is_file())


def linha_import(a: Ambiente) -> str:
    return '@' + (a.kit / 'CLAUDE.md').as_posix()


# ---------------------------------------------------------------- conferência

def verificar(a: Ambiente) -> list[str]:
    """Cada achado é uma linha; lista vazia = tudo certo."""
    ach: list[str] = []
    cfg = config(a)
    if not cfg:
        return [f'config\\plugins.json ausente ou inválido em {a.kit}']
    grupos = plugins_do_kit(a)
    usuario = ligados_usuario(a)

    conhecidos = _json(a.casa / 'plugins' / 'known_marketplaces.json')
    reg = conhecidos.get(MKT, {})
    lugar = reg.get('installLocation') or reg.get('source', {}).get('path', '')
    if not reg:
        ach.append(f'o marketplace {MKT} não está registrado neste PC')
    elif lugar and Path(lugar).resolve() != a.kit.resolve():
        ach.append(f'o marketplace {MKT} aponta para {lugar}, não para {a.kit}')
    if (a.casa / 'plugins' / 'cache' / MKT).exists():
        ach.append(f'há cópia do kit em {a.casa / "plugins" / "cache" / MKT}: o plugin devia carregar da pasta')

    for j in juncoes_do_kit(a):
        ach.append(f'junção antiga sobrando: {j} -> {_alvo_juncao(j)}')
    todas = {s: g for g, ss in grupos.items() for s in ss}
    for s in skills_de_usuario(a):
        if s in todas:
            ach.append(f'nome repetido: {s} existe em {a.casa / "skills"} e no plugin {todas[s]}')

    pastas_plugin = {d.name for d in (a.kit / 'plugins').iterdir() if d.is_dir()} if (a.kit / 'plugins').is_dir() else set()
    for g in sorted(pastas_plugin - set(grupos)):
        if (a.kit / 'plugins' / g / '.claude-plugin' / 'plugin.json').is_file():
            ach.append(f'o plugin {g} existe em plugins\\ mas falta no .claude-plugin\\marketplace.json')
    for g, c in cfg.get('grupos', {}).items():
        pid = f'{g}@{MKT}'
        if g not in grupos:
            if not c.get('desde'):
                ach.append(f'grupo faltando: {g} está no config mas não no marketplace')
            continue
        if c.get('escopo') == 'usuario' and usuario.get(pid) is not True:
            ach.append(f'grupo {g} não está ligado no escopo de usuário')
        if c.get('escopo') == 'projeto' and usuario.get(pid) is True:
            ach.append(f'grupo {g} está ligado no escopo de usuário; devia ser só por projeto')
    for pid, c in cfg.get('de_fora', {}).items():
        if c.get('escopo') == 'usuario' and usuario.get(pid) is not True:
            ach.append(f'{pid} não está ligado no escopo de usuário')
        if c.get('escopo') == 'projeto' and usuario.get(pid) is True:
            ach.append(f'{pid} está ligado no escopo de usuário; devia ser só nos projetos ({c.get("ligado_em") or c.get("ligado_em_prefixo")})')

    settings = _json(a.casa / 'settings.json')
    for h in settings.get('hooks', {}).get('PostToolUse', []):
        for x in h.get('hooks', []):
            if 'gancho.py' in x.get('command', ''):
                ach.append('o gancho das cores está no ~\\.claude\\settings.json e também no plugin nucleo: dispara duas vezes')

    if (a.mae / 'CLAUDE.md').exists():
        ach.append(f'existe {a.mae / "CLAUDE.md"}: ele carregaria em TODOS os projetos (o CLAUDE.md sobe as pastas)')
    casa_md = a.casa / 'CLAUDE.md'
    if not casa_md.is_file():
        ach.append(f'{casa_md} não existe: as regras pessoais não carregam')
    else:
        texto = casa_md.read_text(encoding='utf-8-sig').strip()
        if texto != linha_import(a):
            ach.append(f'{casa_md} não é só a linha de import "{linha_import(a)}"')

    if 'kit' in grupos:
        raiz = _json(a.mae / '.claude' / 'settings.json').get('enabledPlugins', {})
        if raiz.get(f'kit@{MKT}') is not True:
            ach.append(f'a janela da raiz não liga o grupo kit ({a.mae / ".claude" / "settings.json"})')

    if a.local_json and a.local_json.is_file():
        mod = _json(a.local_json).get('modulo', '')
        if not mod or not Path(mod).is_dir():
            ach.append(f'o local.json das cores aponta para um módulo que não existe: {mod}')

    r = subprocess.run(['git', '-C', str(a.kit), 'config', 'core.hooksPath'], capture_output=True, text=True)
    if r.stdout.strip() != '.githooks':
        ach.append('git config core.hooksPath não é .githooks no kit (o pre-commit de privacidade não roda)')
    return ach


# ---------------------------------------------------------------- instalação

def _modulo_cores(a: Ambiente) -> Path | None:
    achados = sorted(a.kit.glob('plugins/*/skills/**/organizar-projetos/scripts/pastas.py'))
    return achados[0].parents[1] if achados else None


def _sem_cli(a: Ambiente, args: list[str]) -> None:
    """Sem o CLI: guarda o comando equivalente para o Ettore colar numa janela do Claude Code."""
    a.no_painel.append('/' + ' '.join(args))


def instalar(a: Ambiente, claude_md_kit_vence: bool = False) -> list[str]:
    cfg = config(a)
    if not cfg:
        raise SystemExit(f'config\\plugins.json ausente ou inválido em {a.kit}')
    feito = a.feito
    backups = a.casa / 'backups'

    def claude(args: list[str], ok: str) -> bool | None:
        """True: deu certo; False: falhou (anotado); None: sem o CLI (o comando vai para o painel)."""
        r = a.rodar_claude(args)
        if r.returncode == 127:
            _sem_cli(a, [x for x in args if x not in ('--scope', 'user')])
            return None
        feito.append(ok if r.returncode == 0
                     else f'claude {" ".join(args)}: FALHOU ({(r.stderr or r.stdout).strip()[:200]})')
        return r.returncode == 0

    conhecidos = _json(a.casa / 'plugins' / 'known_marketplaces.json')
    for nome, m in cfg.get('marketplaces', {}).items():
        if nome in conhecidos:
            continue
        fonte = str(a.kit) if nome == MKT else m.get('repo') or m.get('caminho')
        claude(['plugin', 'marketplace', 'add', fonte], f'marketplace {nome} registrado')

    usuario = ligados_usuario(a)
    grupos = plugins_do_kit(a)
    quer = [f'{g}@{MKT}' for g, c in cfg.get('grupos', {}).items() if c.get('escopo') == 'usuario' and g in grupos]
    quer += [pid for pid, c in cfg.get('de_fora', {}).items() if c.get('escopo') == 'usuario']
    for pid in quer:
        if usuario.get(pid) is True:
            continue
        r = a.rodar_claude(['plugin', 'install', pid, '--scope', 'user'])
        if r.returncode == 127:
            _sem_cli(a, ['plugin', 'install', pid])
            continue
        if r.returncode != 0:
            r = a.rodar_claude(['plugin', 'enable', pid, '--scope', 'user'])
        feito.append(f'{pid}: ' + ('ligado no escopo de usuário' if r.returncode == 0 else f'FALHOU ({(r.stderr or r.stdout).strip()[:200]})'))
    proj = [f'{g}@{MKT}' for g, c in cfg.get('grupos', {}).items() if c.get('escopo') == 'projeto']
    proj += [pid for pid, c in cfg.get('de_fora', {}).items() if c.get('escopo') == 'projeto']
    for pid in proj:
        if ligados_usuario(a).get(pid) is True:
            claude(['plugin', 'disable', pid, '--scope', 'user'], f'{pid}: desligado no escopo de usuário (é por projeto)')

    r = subprocess.run(['git', '-C', str(a.kit), 'config', 'core.hooksPath'], capture_output=True, text=True)
    if r.stdout.strip() != '.githooks':
        subprocess.run(['git', '-C', str(a.kit), 'config', 'core.hooksPath', '.githooks'], check=True)
        feito.append('git config core.hooksPath .githooks')

    juncoes = juncoes_do_kit(a)
    if juncoes:
        backups.mkdir(parents=True, exist_ok=True)
        lista = backups / f'skills-juncoes-{time.strftime("%Y-%m-%d_%H%M%S")}.txt'
        lista.write_text(''.join(f'{j.name}\t{_alvo_juncao(j)}\n' for j in juncoes), encoding='utf-8')
        for j in juncoes:
            os.rmdir(j)                 # só a junção; o alvo fica intacto
        feito.append(f'{len(juncoes)} junção(ões) antiga(s) tirada(s) de {a.casa / "skills"} (lista em {lista})')

    casa_md, kit_md = a.casa / 'CLAUDE.md', a.kit / 'CLAUDE.md'
    if not casa_md.is_file() or casa_md.read_text(encoding='utf-8-sig').strip() != linha_import(a):
        trocar = True
        if casa_md.is_file() and kit_md.is_file() and not os.path.samefile(casa_md, kit_md):
            igual = casa_md.read_bytes().replace(b'\r\n', b'\n') == kit_md.read_bytes().replace(b'\r\n', b'\n')
            if not igual and not claude_md_kit_vence:
                trocar = False      # este PC tem um CLAUDE.md pessoal diferente: juntar à mão antes
                feito.append(f'ATENÇÃO: {casa_md} difere do {kit_md} e não é hardlink dele; não mexi. Leve ao '
                             'CLAUDE.md do kit o que só este tem e rode de novo com --claude-md-kit-vence.')
        if trocar:
            if casa_md.exists():
                backups.mkdir(parents=True, exist_ok=True)
                shutil.copy2(casa_md, backups / f'CLAUDE.md.{time.strftime("%Y-%m-%d_%H%M%S")}_antes-do-import')
                casa_md.unlink()        # se era hardlink, só este endereço sai; o do kit fica
            casa_md.parent.mkdir(parents=True, exist_ok=True)
            casa_md.write_text(linha_import(a) + '\n', encoding='utf-8')
            feito.append(f'{casa_md}: só a linha de import do CLAUDE.md do kit')

    if a.local_json and a.local_json.is_file():
        lj = _json(a.local_json)
        mod = _modulo_cores(a)
        if mod and Path(lj.get('modulo', '')) != mod:
            _gravar_json(a.local_json, {**lj, 'modulo': str(mod)}, backups)
            feito.append(f'local.json das cores: modulo -> {mod}')

    if 'kit' in grupos:
        p = a.mae / '.claude' / 'settings.json'
        s = _json(p)
        if s.get('enabledPlugins', {}).get(f'kit@{MKT}') is not True:
            s.setdefault('enabledPlugins', {})[f'kit@{MKT}'] = True
            _gravar_json(p, s, backups)
            feito.append(f'janela da raiz: kit@{MKT} ligado em {p}')
    return feito


def trecho(a: Ambiente, tipo: str) -> str:
    tipos = config(a).get('tipos_de_projeto', {})
    if tipo not in tipos:
        raise SystemExit(f'tipo desconhecido: {tipo} (há: {", ".join(tipos)})')
    t = tipos[tipo]
    grupos = plugins_do_kit(a)
    ep = {k: v for k, v in t.get('enabledPlugins', {}).items()
          if not k.endswith('@' + MKT) or k.split('@')[0] in grupos}
    corpo = {'enabledPlugins': ep, **t.get('outros', {})}
    nota = f'\n// {t["nota"]}' if t.get('nota') else ''
    return json.dumps(corpo, ensure_ascii=False, indent=2) + nota


def comando_safety_net(a: Ambiente) -> str:
    inst = _json(a.casa / 'plugins' / 'installed_plugins.json').get('plugins', {})
    versao = next((i.get('version') for i in inst.get('cc-safety-net@cc-marketplace', [])), None) or 'latest'
    return f'npx -y cc-safety-net@{versao} policy apply {a.kit / "scripts" / "safety-net-politica.json"} --global'


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    g = ap.add_mutually_exclusive_group()
    g.add_argument('--verificar', action='store_true', help='só confere; sai com 1 se houver achado')
    g.add_argument('--trecho', metavar='TIPO', help='imprime o enabledPlugins de um tipo de projeto')
    ap.add_argument('--claude-md-kit-vence', action='store_true',
                    help='o ~\\.claude\\CLAUDE.md deste PC difere do kit: guarda uma cópia e põe o import no lugar')
    arg = ap.parse_args(argv)
    a = Ambiente()
    if arg.trecho:
        print(trecho(a, arg.trecho))
        return 0
    if not arg.verificar:
        feito = instalar(a, arg.claude_md_kit_vence)
        print('\n'.join(feito) if feito else 'Instalação: nada a fazer, tudo já estava no lugar.')
        if a.no_painel:
            print('\nO comando claude não está no PATH deste PC (a extensão do VS Code usa o dela). Abra uma janela '
                  'do Claude Code, cole estes comandos um a um e rode este script de novo:')
            print('\n'.join(f'  {c}' for c in a.no_painel))
        print(f'\nA política do safety-net é sua (rode num terminal e confirme):\n  {comando_safety_net(a)}')
    ach = verificar(a)
    grupos = plugins_do_kit(a)
    print('\nGrupos do kit: ' + '; '.join(f'{g} ({len(s)})' for g, s in grupos.items()))
    if ach:
        print(f'\nVerificação: {len(ach)} achado(s)')
        print('\n'.join(f'  - {x}' for x in ach))
        return 1
    print('Verificação: 0 achados')
    return 0


if __name__ == '__main__':
    sys.exit(main())
