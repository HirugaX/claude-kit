"""A varredura dos caminhos velhos, lida do plano."""
import json

import varredura as V
from conftest import juncao, so_windows

PLANO = {'movimentos': [{'nome': 'k', 'de': 'C:/OLD', 'para': 'C:/MAE/novo', 'repo': True}],
         'lapides_extras': [{'de': 'C:/KIT', 'para': 'C:/MAE/claude-kit'}],
         'nao_casar': ['C:/OLD ARQUIVO']}


def achar(texto):
    rx, nao = V.regex_do_plano(PLANO)
    return [m.group(0) for m in rx.finditer(texto)
            if not any(V._normal(texto[m.start():]).startswith(n) for n in nao)]


def test_todas_as_formas_do_caminho():
    assert achar(r'C:\OLD\x') == [r'C:\OLD']
    assert achar('c:/old/x') == ['c:/old']
    assert achar('/c/OLD/x') == ['/c/OLD']
    assert achar('//c/OLD') == ['//c/OLD']
    assert achar(r"'C:\\OLD\\x'") == [r'C:\\OLD']
    assert achar('a chave C--OLD e C--KIT') == ['C--OLD', 'C--KIT']


def test_fronteira_e_não_casar():
    assert achar(r'C:\OLD-NOVO\x') == []
    assert achar(r'C:\OLD_2') == []
    assert achar(r'C:\KIT-PROJETOS') == []
    assert achar(r'C:\OLD ARQUIVO\x') == []
    assert achar(r'D:\OLD') == []


def test_varrer_pula_dados_subpasta_e_junção(tmp_path):
    raiz = tmp_path / 'proj'
    for rel, txt in {'app/config.py': 'RAIZ = r"C:\\OLD"', 'tests/test_a.py': "x = 'C:/OLD'",
                     'docs/HANDOFF.md': 'era C:\\OLD', 'README.md': 'rode em C:\\OLD', 'entrada/d.txt': 'C:\\OLD',
                     'a/b/pular.md': 'C:\\OLD', '.git/config': 'url = C:/OLD', 'conf.json': '{"p": "C:/KIT"}'}.items():
        (raiz / rel).parent.mkdir(parents=True, exist_ok=True)
        (raiz / rel).write_text(txt, encoding='utf-8')
    rx, nao = V.regex_do_plano(PLANO)
    r = V.varrer(raiz, rx, nao, pular=['entrada', 'a/b'])
    assert set(r['código']) == {'app/config.py'}
    assert set(r['teste']) == {'tests/test_a.py'}
    assert set(r['histórico']) == {'docs/HANDOFF.md'}
    assert set(r['doc vivo']) == {'README.md'}
    assert set(r['config']) == {'.git/config', 'conf.json'}
    tudo = json.dumps(r)
    assert 'entrada' not in tudo and 'pular.md' not in tudo


@so_windows
def test_varrer_não_segue_junção(tmp_path):
    raiz, fora = tmp_path / 'proj', tmp_path / 'fora'
    raiz.mkdir()
    fora.mkdir()
    (fora / 'x.py').write_text('C:\\OLD', encoding='utf-8')
    juncao(raiz / 'node', fora)
    rx, nao = V.regex_do_plano(PLANO)
    assert V.varrer(raiz, rx, nao) == {}
