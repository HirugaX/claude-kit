"""O inventário do que o PC já tem: o veredito de cada item, sem nunca seguir junção."""
import json
import os
import subprocess

import inventario as I
import regras as R
from conftest import juncao, so_windows


def skill(p, texto='x'):
    p.mkdir(parents=True)
    (p / 'SKILL.md').write_text(texto, encoding='utf-8')


@so_windows
def test_skills_cada_veredito(tmp_path):
    casa, kit = tmp_path / 'casa', tmp_path / 'kit'
    skill(kit / 'skills' / 'ligada')
    skill(kit / 'skills' / 'igual', 'i')
    skill(kit / 'skills' / 'diferente', 'kit')
    skill(kit / 'skills' / 'so-no-kit')
    (casa / 'skills').mkdir(parents=True)
    juncao(casa / 'skills' / 'ligada', kit / 'skills' / 'ligada')
    skill(casa / 'skills' / 'igual', 'i')
    skill(casa / 'skills' / 'diferente', 'cópia')
    skill(casa / 'skills' / 'nova')
    skill(casa / 'skills' / 'synced')
    v = {s['nome']: s['veredito'].split(':')[0] for s in I.skills(casa, kit)}
    assert v == {'ligada': 'SERVE', 'igual': 'DUPLICARIA', 'diferente': 'ATENÇÃO', 'nova': 'SERVE',
                 'synced': 'SERVE', 'so-no-kit': 'FALTA'}


def test_impressao_ignora_os_arquivos_de_cada_pc(tmp_path):
    a, b = tmp_path / 'a', tmp_path / 'b'
    skill(a, 'igual')
    skill(b, 'igual')
    (a / 'desktop.ini').write_text('; claude-pastas v1 nao-toco', encoding='utf-8')
    (b / 'Thumbs.db').write_bytes(b'x')
    assert I.impressao(a) == I.impressao(b)


def test_settings_acha_o_gancho_e_os_outros(tmp_path):
    casa = tmp_path / 'casa'
    casa.mkdir()
    nosso = {'type': 'command', 'command': 'python "C:/k/organizar-projetos/scripts/gancho.py" || true'}
    outro = {'type': 'command', 'command': 'python semanal.py'}
    (casa / 'settings.json').write_text(json.dumps({'hooks': {'PostToolUse': [{'matcher': '*', 'hooks': [nosso]}]},
                                                    'effortLevel': 'xhigh'}), encoding='utf-8')
    proj = tmp_path / 'p'
    (proj / '.claude').mkdir(parents=True)
    (proj / '.claude' / 'settings.json').write_text(json.dumps({'hooks': {'SessionStart': [{'hooks': [outro]}]}}),
                                                    encoding='utf-8')
    r = I.settings(casa, [proj])
    assert r[0]['veredito'].startswith('DUPLICARIA') and 'effortLevel' in r[0]['veredito']
    assert r[1]['veredito'].startswith('SERVE: há outros ganchos')


def test_claude_md_linhas_só_deste_pc_e_hardlink(tmp_path):
    casa, kit = tmp_path / 'casa', tmp_path / 'kit'
    casa.mkdir()
    kit.mkdir()
    (kit / 'CLAUDE.md').write_text('# regras\n- a\n- b\n', encoding='utf-8')
    (casa / 'CLAUDE.md').write_text('# regras\n- a\n- só aqui\n', encoding='utf-8')
    r = I.claude_md(casa, kit)
    assert r['so_neste_pc'] == ['- só aqui'] and r['veredito'].startswith('ATENÇÃO')
    (casa / 'CLAUDE.md').unlink()
    os.link(kit / 'CLAUDE.md', casa / 'CLAUDE.md')
    r = I.claude_md(casa, kit)
    assert r['veredito'].startswith('SERVE') and r['nomes_do_arquivo'] == 2


def test_inis_por_marca_sem_seguir_junção(tmp_path):
    raiz = tmp_path / 'r'
    for nome, texto in (('a', R.montar_ini('i.ico', 'd', 'eu-leio')), ('b', '[.ShellClassInfo]\n; DESOSP icones_pastas\n'),
                        ('c', '[LocalizedFileNames]\n')):
        (raiz / nome).mkdir(parents=True)
        (raiz / nome / 'desktop.ini').write_text(texto, encoding='utf-8')
    if os.name == 'nt':
        juncao(raiz / 'atalho', raiz / 'a')
    r = I.inis([raiz])
    assert r['contagem'] == {'nosso': 1, '3009': 1, 'alheio': 1}


def test_projetos_git_sem_remote_e_memória(tmp_path):
    raiz = tmp_path / 'raiz'
    p = raiz / 'meu-app'
    p.mkdir(parents=True)
    subprocess.run(['git', 'init', '-q', str(p)], check=True)
    (p / 'CLAUDE.md').write_text('x', encoding='utf-8')
    casa = tmp_path / 'casa'
    mem = casa / 'projects' / I.chave_memoria(p).upper() / 'memory'
    mem.mkdir(parents=True)
    (mem / 'a.md').write_text('x', encoding='utf-8')
    r = I.projetos([raiz], casa)
    assert len(r) == 1
    assert r[0]['git'] and r[0]['remote'] == '' and r[0]['memoria_arquivos'] == 1
    assert 'FALTA' in r[0]['veredito']


def test_kit_acusa_claude_md_na_raiz_da_mãe(tmp_path):
    mae = tmp_path / 'MAE'
    (mae / 'claude-kit').mkdir(parents=True)
    (mae / 'CLAUDE.md').write_text('x', encoding='utf-8')
    assert 'CLAUDE.md na raiz da mãe' in I.kit(mae / 'claude-kit', mae)['veredito']
