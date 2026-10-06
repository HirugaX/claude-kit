"""Testes do ligar_claude.py, em pastas temporárias, com junções de verdade (Windows)."""
import importlib.util
import os
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.skipif(sys.platform != 'win32', reason='junção é do Windows')

_spec = importlib.util.spec_from_file_location('ligar_claude', Path(__file__).resolve().parents[1] / 'ligar_claude.py')
lc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(lc)


def junção(link: Path, alvo: Path):
    subprocess.run(['cmd', '/c', 'mklink', '/J', str(link), str(alvo)], check=True, capture_output=True)


def skill(pasta: Path, texto: str = 'x') -> Path:
    pasta.mkdir(parents=True)
    (pasta / 'SKILL.md').write_text(texto, encoding='utf-8')
    return pasta


@pytest.fixture
def cena(tmp_path):
    kit = tmp_path / 'claude-kit' / 'skills'
    casa = tmp_path / 'home' / '.claude' / 'skills'
    velho = tmp_path / 'CLAUDE' / 'skills'
    casa.mkdir(parents=True)
    return kit, casa, velho


def test_skill_do_kit_sem_junção_ganha_junção(cena):
    kit, casa, _ = cena
    skill(kit / 'a')
    lc.ligar_skills(kit, casa)
    assert os.path.isjunction(casa / 'a')
    assert (casa / 'a' / 'SKILL.md').read_text(encoding='utf-8') == 'x'


def test_junção_para_o_kit_velho_é_re_apontada_e_o_velho_fica_intacto(cena):
    kit, casa, velho = cena
    skill(kit / 'a', 'novo')
    skill(velho / 'a', 'velho')
    junção(casa / 'a', velho / 'a')
    feito = lc.ligar_skills(kit, casa, raiz_antiga=velho.parent)
    assert any('re-apontada' in f for f in feito)
    assert Path(os.path.realpath(casa / 'a')) == (kit / 'a').resolve()
    assert (velho / 'a' / 'SKILL.md').read_text(encoding='utf-8') == 'velho'   # o alvo antigo não foi apagado


def test_junção_para_o_kit_velho_sem_raiz_antiga_não_mexe(cena):
    kit, casa, velho = cena
    skill(kit / 'a')
    skill(velho / 'a')
    junção(casa / 'a', velho / 'a')
    feito = lc.ligar_skills(kit, casa)
    assert any(f.startswith('ATENÇÃO') for f in feito)
    assert Path(os.path.realpath(casa / 'a')) == (velho / 'a').resolve()


def test_junção_sem_alvo_é_re_apontada(cena):
    kit, casa, velho = cena
    skill(kit / 'a')
    skill(velho / 'a')
    junção(casa / 'a', velho / 'a')
    (velho / 'a' / 'SKILL.md').unlink()
    (velho / 'a').rmdir()
    lc.ligar_skills(kit, casa)
    assert Path(os.path.realpath(casa / 'a')) == (kit / 'a').resolve()


def test_cópia_velha_diferente_não_vence_o_kit(cena):
    kit, casa, _ = cena
    skill(kit / 'a', 'do kit')
    skill(casa / 'a', 'cópia velha')
    feito = lc.ligar_skills(kit, casa)
    assert any(f.startswith('ATENÇÃO') for f in feito)
    assert (kit / 'a' / 'SKILL.md').read_text(encoding='utf-8') == 'do kit'
    assert not os.path.isjunction(casa / 'a')


def test_kit_vence_guarda_a_cópia_e_liga_o_kit(cena):
    kit, casa, _ = cena
    skill(kit / 'a', 'do kit')
    skill(casa / 'a', 'cópia velha')
    lc.ligar_skills(kit, casa, kit_vence=True)
    assert os.path.isjunction(casa / 'a')
    assert (casa / 'a' / 'SKILL.md').read_text(encoding='utf-8') == 'do kit'
    guardadas = list((kit / '_substituidas').iterdir())
    assert len(guardadas) == 1 and (guardadas[0] / 'SKILL.md').read_text(encoding='utf-8') == 'cópia velha'


def test_pasta_vence_atualiza_o_kit_e_guarda_a_versão_antiga(cena):
    kit, casa, _ = cena
    skill(kit / 'a', 'antiga')
    skill(casa / 'a', 'do npx')
    lc.ligar_skills(kit, casa, pasta_vence=True)
    assert (kit / 'a' / 'SKILL.md').read_text(encoding='utf-8') == 'do npx'
    assert os.path.isjunction(casa / 'a')
    guardadas = list((kit / '_substituidas').iterdir())
    assert (guardadas[0] / 'SKILL.md').read_text(encoding='utf-8') == 'antiga'


def test_pasta_igual_vira_junção(cena):
    kit, casa, _ = cena
    skill(kit / 'a', 'igual')
    skill(casa / 'a', 'igual')
    lc.ligar_skills(kit, casa)
    assert os.path.isjunction(casa / 'a')


def test_desktop_ini_do_sistema_de_cores_não_faz_a_skill_parecer_diferente(cena):
    kit, casa, _ = cena
    skill(kit / 'a', 'igual')
    (kit / 'a' / 'desktop.ini').write_text('; claude-pastas v1 nao-toco\r\n', encoding='utf-16')
    skill(casa / 'a', 'igual')
    feito = lc.ligar_skills(kit, casa)
    assert not any(f.startswith('ATENÇÃO') for f in feito)
    assert os.path.isjunction(casa / 'a')


def test_skill_nova_do_npx_vem_para_o_kit(cena):
    kit, casa, _ = cena
    kit.mkdir(parents=True)
    skill(casa / 'nova', 'n')
    lc.ligar_skills(kit, casa)
    assert (kit / 'nova' / 'SKILL.md').read_text(encoding='utf-8') == 'n'
    assert os.path.isjunction(casa / 'nova')


def test_conferir_não_mexe_em_nada(cena):
    kit, casa, velho = cena
    skill(kit / 'a')
    skill(velho / 'a')
    junção(casa / 'a', velho / 'a')
    feito = lc.ligar_skills(kit, casa, conferir=True, raiz_antiga=velho.parent)
    assert any('re-apontaria' in f for f in feito)
    assert Path(os.path.realpath(casa / 'a')) == (velho / 'a').resolve()


def test_synced_não_se_mexe(cena):
    kit, casa, _ = cena
    kit.mkdir(parents=True)
    skill(casa / 'synced')
    lc.ligar_skills(kit, casa)
    assert not (kit / 'synced').exists()


def test_claude_md_ganha_endereço_no_kit_e_continua_o_mesmo_arquivo(tmp_path):
    raiz, casa = tmp_path / 'kit', tmp_path / 'home'
    raiz.mkdir(); casa.mkdir()
    (casa / 'CLAUDE.md').write_text('regras', encoding='utf-8')
    lc.ligar_claude_md(raiz, casa)
    assert os.path.samefile(raiz / 'CLAUDE.md', casa / 'CLAUDE.md')
    assert lc.ligar_claude_md(raiz, casa) == []


def test_claude_md_diferentes_avisa(tmp_path):
    raiz, casa = tmp_path / 'kit', tmp_path / 'home'
    raiz.mkdir(); casa.mkdir()
    (casa / 'CLAUDE.md').write_text('a', encoding='utf-8')
    (raiz / 'CLAUDE.md').write_text('b', encoding='utf-8')
    assert lc.ligar_claude_md(raiz, casa)[0].startswith('ATENÇÃO')
