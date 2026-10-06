"""A conferência antes do primeiro envio: segredo, termo sensível (sem nunca imprimir o termo), histórico, .env."""
import subprocess

import pytest

import antes_do_github as A

FALSO_TOKEN = 'ghp_' + 'A1b2C3d4' * 5          # montado aqui para o próprio teste não ter um token inteiro


def git(repo, *args):
    subprocess.run(['git', '-C', str(repo), '-c', 'user.name=t', '-c', 'user.email=t@t', *args], check=True,
                   capture_output=True)


@pytest.fixture
def repo(tmp_path):
    r = tmp_path / 'r'
    r.mkdir()
    git(r, 'init', '-q')
    (r / 'app.py').write_text('print("oi")\n', encoding='utf-8')
    git(r, 'add', '.')
    git(r, 'commit', '-q', '-m', 'um')
    return r


def test_limpo_passa(repo, capsys):
    assert A.main([str(repo), '--sem-historia']) == 0
    assert '--private' in capsys.readouterr().out


def test_segredo_no_arquivo_novo(repo):
    (repo / 'conf.py').write_text(f'TOKEN = "{FALSO_TOKEN}"\n', encoding='utf-8')
    prob, _ = A.conferir(repo, [])
    assert any('token do GitHub' in p and 'conf.py:1' in p for p in prob)


def test_segredo_que_só_existe_no_histórico(repo):
    (repo / 'velho.py').write_text(f'chave = "{FALSO_TOKEN}"\n', encoding='utf-8')
    git(repo, 'add', '.')
    git(repo, 'commit', '-q', '-m', 'dois')
    (repo / 'velho.py').unlink()
    git(repo, 'commit', '-q', '-am', 'tres')
    prob, _ = A.conferir(repo, [], historia=True)
    assert any('no histórico' in p for p in prob)
    prob, _ = A.conferir(repo, [], historia=False)
    assert not prob


def test_termo_sensível_sem_imprimir_o_termo(repo, tmp_path, capsys):
    termos = tmp_path / 'termos.txt'
    termos.write_text('# um por linha\nFulano Beltrano\n', encoding='utf-8')
    (repo / 'notas.md').write_text('caso do fulano beltrano\n', encoding='utf-8')
    assert A.main([str(repo), '--termos', str(termos)]) == 1
    out = capsys.readouterr().out
    assert 'termo sensível nº 1: notas.md:1' in out
    assert 'fulano' not in out.casefold()


def test_env_e_extensão_de_dado(repo):
    (repo / '.env').write_text('X=1\n', encoding='utf-8')
    (repo / '.env.example').write_text('X=\n', encoding='utf-8')
    (repo / 'base.xlsx').write_bytes(b'PK')
    prob, avisos = A.conferir(repo, [])
    assert 'arquivo .env iria junto: .env' in prob
    assert not any('.env.example' in p for p in prob)
    assert any('.xlsx' in a for a in avisos)


def test_ignorado_não_conta(repo):
    (repo / '.gitignore').write_text('segredo.txt\n', encoding='utf-8')
    (repo / 'segredo.txt').write_text(f'{FALSO_TOKEN}\n', encoding='utf-8')
    prob, _ = A.conferir(repo, [], historia=False)
    assert not prob
