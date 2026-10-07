"""Testes do instalar_kit.py, em pastas temporárias, com junções de verdade (Windows) e um `claude` falso."""
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.skipif(sys.platform != 'win32', reason='junção é do Windows')

_spec = importlib.util.spec_from_file_location('instalar_kit', Path(__file__).resolve().parents[1] / 'instalar_kit.py')
ik = importlib.util.module_from_spec(_spec)
sys.modules['instalar_kit'] = ik          # o @dataclass procura o módulo aqui
_spec.loader.exec_module(ik)


def gravar(p: Path, d) -> Path:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(d) if not isinstance(d, str) else d, encoding='utf-8')
    return p


def skill(pasta: Path) -> Path:
    pasta.mkdir(parents=True)
    (pasta / 'SKILL.md').write_text('---\nname: x\n---\n', encoding='utf-8')
    return pasta


def juncao(link: Path, alvo: Path):
    subprocess.run(['cmd', '/c', 'mklink', '/J', str(link), str(alvo)], check=True, capture_output=True)


class ClaudeFalso:
    """Registra as chamadas e aplica no settings.json o que o `claude plugin` faria."""

    def __init__(self, casa: Path):
        self.casa, self.chamadas = casa, []

    def __call__(self, args):
        self.chamadas.append(args)
        s = casa_settings = self.casa / 'settings.json'
        d = json.loads(s.read_text(encoding='utf-8')) if s.exists() else {}
        if args[:2] == ['plugin', 'install'] or args[:2] == ['plugin', 'enable']:
            d.setdefault('enabledPlugins', {})[args[2]] = True
        if args[:2] == ['plugin', 'disable']:
            d.setdefault('enabledPlugins', {})[args[2]] = False
        gravar(casa_settings, d)
        return subprocess.CompletedProcess(args, 0, '', '')


@pytest.fixture
def amb(tmp_path):
    mae = tmp_path / 'CLAUDE-PROJETOS'
    kit = mae / 'claude-kit'
    casa = tmp_path / 'home' / '.claude'
    for g, ss in {'nucleo': ['uso'], 'planejamento': ['grill-me'], 'engenharia': ['tdd']}.items():
        gravar(kit / 'plugins' / g / '.claude-plugin' / 'plugin.json', {'name': g})
        for s in ss:
            skill(kit / 'plugins' / g / 'skills' / s)
    gravar(kit / '.claude-plugin' / 'marketplace.json', {'name': 'claude-kit', 'plugins': [
        {'name': g, 'source': f'./plugins/{g}'} for g in ('nucleo', 'planejamento', 'engenharia')]})
    gravar(kit / 'config' / 'plugins.json', {
        'marketplaces': {'claude-kit': {'fonte': 'pasta'}, 'oficial': {'fonte': 'github', 'repo': 'a/b'}},
        'grupos': {'nucleo': {'escopo': 'usuario'}, 'planejamento': {'escopo': 'usuario'},
                   'engenharia': {'escopo': 'projeto'}, 'kit': {'escopo': 'projeto', 'desde': 'F2a'}},
        'de_fora': {'safety@oficial': {'escopo': 'usuario'}, 'relatorio@oficial': {'escopo': 'projeto'}},
        'tipos_de_projeto': {'codigo': {'enabledPlugins': {'engenharia@claude-kit': True}},
                             'raiz': {'enabledPlugins': {'kit@claude-kit': True}}},
    })
    (kit / 'CLAUDE.md').write_text('# Regras\n', encoding='utf-8')
    subprocess.run(['git', 'init', '-q', str(kit)], check=True)
    (casa / 'skills').mkdir(parents=True)
    gravar(casa / 'plugins' / 'known_marketplaces.json', {})
    a = ik.Ambiente(kit=kit, casa=casa, local_json=None)
    a.claude = ClaudeFalso(casa)
    return a


def test_instalar_e_depois_verificar_sem_achado(amb):
    feito = ik.instalar(amb)
    assert ['plugin', 'marketplace', 'add', str(amb.kit)] in amb.claude.chamadas
    ligados = ik.ligados_usuario(amb)
    assert ligados['nucleo@claude-kit'] and ligados['planejamento@claude-kit'] and ligados['safety@oficial']
    assert 'engenharia@claude-kit' not in ligados and 'relatorio@oficial' not in ligados
    assert (amb.casa / 'CLAUDE.md').read_text(encoding='utf-8').strip() == '@' + (amb.kit / 'CLAUDE.md').as_posix()
    assert any('core.hooksPath' in f for f in feito)
    gravar(amb.casa / 'plugins' / 'known_marketplaces.json',
           {'claude-kit': {'installLocation': str(amb.kit)}, 'oficial': {}})
    assert ik.verificar(amb) == []


def test_instalar_de_novo_nao_faz_nada(amb):
    ik.instalar(amb)
    gravar(amb.casa / 'plugins' / 'known_marketplaces.json',
           {'claude-kit': {'installLocation': str(amb.kit)}, 'oficial': {}})
    amb.feito, amb.claude.chamadas = [], []
    assert ik.instalar(amb) == [] and amb.claude.chamadas == []


def test_juncao_antiga_do_kit_sai_e_o_alvo_fica(amb, tmp_path):
    velha = skill(amb.kit / 'skills' / 'velha')
    juncao(amb.casa / 'skills' / 'velha', velha)
    outra = skill(tmp_path / 'fora' / 'outra')
    juncao(amb.casa / 'skills' / 'outra', outra)          # junção para fora do kit: não é nossa
    assert [j.name for j in ik.juncoes_do_kit(amb)] == ['velha']
    assert any('junção antiga sobrando' in x for x in ik.verificar(amb))
    ik.instalar(amb)
    assert not (amb.casa / 'skills' / 'velha').exists() and (velha / 'SKILL.md').is_file()
    assert os.path.isjunction(amb.casa / 'skills' / 'outra')
    assert list((amb.casa / 'backups').glob('skills-juncoes-*.txt'))


def test_hardlink_vira_import_e_o_arquivo_do_kit_fica(amb):
    os.link(amb.kit / 'CLAUDE.md', amb.casa / 'CLAUDE.md')
    assert any('linha de import' in x for x in ik.verificar(amb))
    ik.instalar(amb)
    assert (amb.kit / 'CLAUDE.md').read_text(encoding='utf-8') == '# Regras\n'
    assert (amb.casa / 'CLAUDE.md').read_text(encoding='utf-8').startswith('@')
    assert list((amb.casa / 'backups').glob('CLAUDE.md.*'))


def test_verificar_acusa_os_erros_de_escopo_e_de_lugar(amb):
    ik.instalar(amb)
    s = json.loads((amb.casa / 'settings.json').read_text(encoding='utf-8'))
    s['enabledPlugins'].update({'engenharia@claude-kit': True, 'relatorio@oficial': True, 'nucleo@claude-kit': False})
    s['hooks'] = {'PostToolUse': [{'hooks': [{'command': 'python x/gancho.py'}]}]}
    gravar(amb.casa / 'settings.json', s)
    skill(amb.casa / 'skills' / 'tdd')                         # cópia solta com o mesmo nome de uma do plugin
    (amb.mae / 'CLAUDE.md').write_text('x', encoding='utf-8')  # carregaria em todo projeto
    gravar(amb.casa / 'plugins' / 'cache' / 'claude-kit' / 'x.json', {})
    ach = '\n'.join(ik.verificar(amb))
    for trecho in ('não está registrado', 'engenharia está ligado no escopo de usuário',
                   'relatorio@oficial está ligado no escopo de usuário', 'grupo nucleo não está ligado',
                   'dispara duas vezes', 'nome repetido: tdd', 'carregaria em TODOS', 'cópia do kit'):
        assert trecho in ach, trecho


def test_plugin_fora_do_marketplace_e_grupo_kit_futuro(amb):
    gravar(amb.kit / 'plugins' / 'solto' / '.claude-plugin' / 'plugin.json', {'name': 'solto'})
    ach = ik.verificar(amb)
    assert any('solto existe em plugins' in x for x in ach)
    assert not any('grupo faltando: kit' in x for x in ach)    # o kit tem "desde": ainda não existe, sem achado


def test_trecho_tira_o_grupo_que_ainda_nao_existe(amb):
    assert json.loads(ik.trecho(amb, 'codigo'))['enabledPlugins'] == {'engenharia@claude-kit': True}
    assert json.loads(ik.trecho(amb, 'raiz'))['enabledPlugins'] == {}
