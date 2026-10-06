"""Testes do checa_kit.py. Os números de teste são montados aqui, nunca escritos por extenso (o próprio arquivo é varrido)."""
import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location('checa_kit', Path(__file__).resolve().parents[1] / 'checa_kit.py')
ck = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ck)


def cpf_de(base):
    """Completa 9 dígitos com os dois verificadores."""
    d = base
    for n in (9, 10):
        d += str(sum(int(d[i]) * (n + 1 - i) for i in range(n)) * 10 % 11 % 10)
    return d


def cns_de(base14):
    """Acha o 15º dígito que fecha a soma do CNS (para base começando em 7, 8 ou 9)."""
    for ultimo in '0123456789':
        if ck.cns_valido(base14 + ultimo):
            return base14 + ultimo
    raise AssertionError('sem dígito')


def test_cpf_valido_com_e_sem_pontuacao():
    c = cpf_de('123' + '456' + '789')
    assert ck.varre_linha(f'cpf {c}') == ['cpf']
    assert ck.varre_linha(f'cpf {c[:3]}.{c[3:6]}.{c[6:9]}-{c[9:]}') == ['cpf']


def test_cpf_invalido_ou_repetido_passa():
    c = cpf_de('123' + '456' + '789')
    errado = c[:-1] + str((int(c[-1]) + 1) % 10)
    assert 'cpf' not in ck.varre_linha(errado)
    assert 'cpf' not in ck.varre_linha('1' * 11)


def test_cns():
    n = cns_de('7' + '0' * 6 + '1234567')
    assert 'cns' in ck.varre_linha(f'cartão {n}')
    assert 'cns' not in ck.varre_linha(f'cartão {n[:-1]}{(int(n[-1]) + 1) % 10}')


def test_telefone_com_separador():
    assert 'telefone' in ck.varre_linha('ligar (1' + '1) 9' + '8765-4321')
    assert 'telefone' in ck.varre_linha('ligar 1' + '1 3456 7890')


def test_data_e_numero_comum_nao_sao_telefone():
    for linha in ('06/10/2026', '2026-10-06', 'versão 3.16', '199-317 mil', 'commit 9a5d07a', '575 KB'):
        assert ck.varre_linha(linha) == [], linha


def test_caminho_de_dado_so_com_arquivo():
    assert ck.varre_linha('ver desosp-app-dados/x' + '.xlsx') == ['caminho_dado']
    assert ck.varre_linha('ver historico\\2026\\base' + '.csv') == ['caminho_dado']
    assert ck.varre_linha('Read(//c/CLAUDE-PROJETOS/desosp-app-dados/**)') == []
    assert ck.varre_linha('deny de entrada\\, historico\\ e privado\\') == []


def test_segredo():
    assert ck.varre_linha('token ghp_' + 'a' * 36) == ['segredo']
    assert ck.varre_linha('chave sk-ant-' + 'b' * 30) == ['segredo']
    assert ck.varre_linha('senha = "' + 'c' * 10 + '"') == ['segredo']
    assert ck.varre_linha('a senha da versão fica em privado') == []
