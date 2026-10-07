"""A mudança lida de um plano: mover, retrato, comparar, lápides, voltar, memória, checar."""
import json
import os
import time
from pathlib import Path

import pytest

import mudanca as M
from conftest import MODULO, juncao, so_windows


@pytest.fixture
def plano(tmp_path):
    velho_a, velho_b = tmp_path / 'velho-a', tmp_path / 'velho_b'
    for v in (velho_a, velho_b):
        (v / 'dados').mkdir(parents=True)
        (v / 'dados' / 'x.txt').write_text(v.name, encoding='utf-8')
        (v / 'leia.md').write_text('oi', encoding='utf-8')
    mae = tmp_path / 'MAE'
    projects = tmp_path / 'projects'
    d = {'data': '2026-10-05', 'mae': str(mae), 'projects': str(projects),
         'movimentos': [{'nome': 'a', 'de': str(velho_a), 'para': str(mae / 'proj-a'), 'insubstituiveis': ['dados']},
                        {'nome': 'b', 'de': str(velho_b), 'para': str(mae / 'proj-b')}],
         'lapides_extras': [{'de': str(tmp_path / 'KIT'), 'para': str(mae / 'kit')}],
         'processos_extras': ['app\\.iniciar']}
    arq = tmp_path / 'plano.json'
    arq.write_text(json.dumps(d), encoding='utf-8')
    return M.ler_plano(arq)


def test_chave_da_memória_confere_com_as_reais():
    assert M.chave(r'C:\CLAUDE-PROJETOS\desosp-censo') == 'C--CLAUDE-PROJETOS-desosp-censo'
    assert M.chave(r'C:\DESOSP_APP') == 'C--DESOSP-APP'
    assert M.chave(r'C:\planilha-hc') == 'C--planilha-hc'


def test_mover_e_rodar_de_novo_pula(plano, capsys):
    assert M.cmd_mover(plano) == 0
    for m in plano['movimentos']:
        assert m['para'].is_dir() and not m['de'].exists()
    assert M.cmd_mover(plano) == 0
    assert 'já movida' in capsys.readouterr().out


def test_mover_para_se_o_destino_existe(plano):
    plano['movimentos'][0]['para'].mkdir(parents=True)
    assert M.cmd_mover(plano) == 1
    assert plano['movimentos'][0]['de'].is_dir()


def test_mover_para_se_algo_segura(plano, monkeypatch):
    chamadas = []

    def falha(a, b):
        chamadas.append(a)
        raise PermissionError('Acesso negado')
    monkeypatch.setattr(M.os, 'rename', falha)
    assert M.cmd_mover(plano, tentativas=3, espera=0) == 1
    assert len(chamadas) == 3 and plano['movimentos'][0]['de'].is_dir()


@so_windows
def test_mover_recusa_junção(plano, tmp_path):
    de = plano['movimentos'][0]['de']
    alvo = tmp_path / 'alvo'
    de.rename(alvo)
    juncao(de, alvo)
    assert M.cmd_mover(plano) == 1


@so_windows
def test_retrato_não_segue_junção_e_a_registra(plano, tmp_path):
    fora = tmp_path / 'fora'
    fora.mkdir()
    (fora / 'muito.txt').write_text('x', encoding='utf-8')
    juncao(plano['movimentos'][0]['de'] / 'node_modules', fora)
    r = M.retrato_de(plano['movimentos'][0]['de'], ['dados'])
    assert 'node_modules/muito.txt' not in r['lista']
    assert list(r['juncoes']) == ['node_modules']
    assert r['arquivos'] == 2 and 'dados/x.txt' in r['hashes']


def test_retrato_antes_e_depois_iguais(plano, tmp_path):
    assert M.cmd_retrato(plano, tmp_path / 'antes.json', novo=False) == 0
    M.cmd_mover(plano)
    assert M.cmd_retrato(plano, tmp_path / 'depois.json', novo=True) == 0
    assert M.cmd_comparar(tmp_path / 'antes.json', tmp_path / 'depois.json') == 0
    (plano['movimentos'][0]['para'] / 'dados' / 'x.txt').write_text('mudou', encoding='utf-8')
    M.cmd_retrato(plano, tmp_path / 'depois2.json', novo=True)
    assert M.cmd_comparar(tmp_path / 'antes.json', tmp_path / 'depois2.json') == 1


def test_lápides_impedem_criar_pasta_e_voltar_desfaz(plano):
    M.cmd_mover(plano)
    assert M.cmd_lapides(plano) == 0
    for velho, novo in M.lapides(plano):
        assert velho.is_file() and M.e_lapide(velho)
        with pytest.raises(OSError):
            os.makedirs(velho / 'entrada', exist_ok=True)
    assert M.cmd_lapides(plano) == 0                       # de novo: "já é lápide"
    assert M.cmd_voltar(plano) == 0
    for m in plano['movimentos']:
        assert m['de'].is_dir() and not m['para'].exists()
    assert not Path(plano['lapides_extras'][0]['de']).exists()


def test_voltar_não_apaga_arquivo_que_não_é_lápide(plano):
    M.cmd_mover(plano)
    estranho = plano['movimentos'][0]['de']
    estranho.write_text('não sou lápide', encoding='utf-8')
    M.cmd_voltar(plano)
    assert estranho.read_text(encoding='utf-8') == 'não sou lápide'


def test_memória_copiada_com_a_chave_em_outra_caixa(plano):
    velha = plano['projects'] / M.chave(plano['movimentos'][0]['de']).lower() / 'memory'
    velha.mkdir(parents=True)
    (velha / 'MEMORY.md').write_text('- x', encoding='utf-8')
    assert M.cmd_memoria(plano) == 0
    nova = plano['projects'] / M.chave(plano['movimentos'][0]['para']) / 'memory' / 'MEMORY.md'
    assert nova.read_text(encoding='utf-8') == '- x'
    assert (velha / 'MEMORY.md').exists()                  # copiar, não mover
    assert M.cmd_memoria(plano) == 1                       # destino já com conteúdo: para


def test_padrão_de_processos(plano):
    rx = M.padrao_processos(plano)
    de = str(plano['movimentos'][1]['de'])
    assert M.presos([f'123 python.exe python {de}\\x.py', '9 code.exe', '5 python -m app.iniciar'], rx) == \
        [f'123 python.exe python {de}\\x.py', '5 python -m app.iniciar']
    assert not M.presos([f'1 python {de}-outro\\x.py', f'1 python {de}_2\\y.py'], rx)


def test_sessões_abertas_dentro_de_pasta_que_vai_mudar(plano):
    d = plano['projects'] / M.chave(plano['movimentos'][0]['de'])
    d.mkdir(parents=True)
    (d / 's.jsonl').write_text('{}', encoding='utf-8')
    assert len(M.sessoes_abertas(plano)) == 1
    antigo = time.time() - 3600
    os.utime(d / 's.jsonl', (antigo, antigo))
    assert M.sessoes_abertas(plano) == []


def test_o_plano_do_notebook_é_válido():
    p = M.ler_plano(MODULO / 'planos' / 'notebook_2026-10-05.json')
    assert len(p['movimentos']) == 5 and M.precisa_admin(p)
