"""Os quadros, a recoloração, o .ico montado e a prévia."""
import json

from PIL import Image

import desenho as D
from conftest import MODULO, REAL


def pasta(frente=(47, 111, 214)):
    """Uma pasta lisa de 8x8: aba (0,77 × frente) em cima, frente embaixo, um pixel branco no meio."""
    im = Image.new('RGBA', (8, 8), (0, 0, 0, 0))
    aba = tuple(round(c * 0.77) for c in frente)
    for x in range(8):
        im.putpixel((x, 1), aba + (255,))
        for y in range(2, 8):
            im.putpixel((x, y), frente + (255,))
    im.putpixel((4, 5), (255, 255, 255, 255))
    return im


def test_recolorir_troca_a_frente_mantém_o_branco_e_escurece_a_aba():
    im = D.recolorir(pasta(), (47, 111, 214), '#D23B3B')
    assert im.getpixel((0, 4))[:3] == (210, 59, 59)
    assert im.getpixel((4, 5))[:3] == (255, 255, 255)
    aba = im.getpixel((0, 1))[:3]
    assert all(abs(a - round(c * 0.77)) <= 2 for a, c in zip(aba, (210, 59, 59)))
    assert im.getpixel((0, 0))[3] == 0


def test_recolorir_para_a_mesma_cor_não_muda():
    a = pasta()
    assert D.recolorir(a, (47, 111, 214), (47, 111, 214)).tobytes() == a.tobytes()


def test_apagar_emblema():
    im = D.apagar_emblema(pasta(), (47, 111, 214))
    assert im.getpixel((4, 5))[:3] == (47, 111, 214)


def test_quadros_completos_com_o_tamanho_certo():
    cores = D.cores_dos_quadros()
    ids = {d['icone'] for d in {**REAL['verbos'], **REAL['marcas']}.values()}
    assert set(cores) == ids
    for i in ids:
        for s in D.TAMANHOS:
            with Image.open(MODULO / 'icones' / i / f'{s}.png') as im:
                assert im.size == (s, s) and im.mode == 'RGBA'


def test_ico_tem_cada_tamanho_com_o_quadro_exato(tmp_path):
    q = D.ler_quadros('eu-leio')
    D.escrever_ico(q, tmp_path / 'x.ico')
    lido = D.ler_ico(tmp_path / 'x.ico')
    assert sorted(lido) == sorted(D.TAMANHOS)
    for s in D.TAMANHOS:
        assert lido[s].tobytes() == q[s].tobytes()


def test_montar_faz_os_9_na_cor_do_mapa(tmp_path):
    mapa = json.loads(json.dumps(REAL))
    mapa['marcas']['projeto-ia']['cor'] = '#4A5260'          # outra cor no mapa: recolore na montagem
    feitos = D.montar(mapa, tmp_path)
    assert len(feitos) == 9
    ia = D.ler_ico(tmp_path / 'projeto-ia.ico')[256]
    assert D.cor_da_frente(ia) == (0x4A, 0x52, 0x60)


def test_previa_tem_os_9_nos_5_tamanhos_e_dois_fundos(tmp_path):
    D.previa(REAL, tmp_path / 'p.html', {'projeto-ia': [('A', '#D4A21A'), ('B', '#4A5260')]})
    html = (tmp_path / 'p.html').read_text(encoding='utf-8')
    assert html.count('class="ic" data-px=') == 9 * 5 * 2 + 2 * 4
    assert 'devicePixelRatio' in html and '#2E7D32' in html


# ---------------------------------------------------------------- os desenhos das referências (05/10, noite)

from pathlib import Path  # noqa: E402

import pytest  # noqa: E402

PACOTE = Path(r'C:\CLAUDE-PROJETOS\prototipos-icones\amostra_gerada_ettore')
com_pacote = pytest.mark.skipif(not (PACOTE / 'eu-forneco-fontes.ico').exists(), reason='o pacote do Ettore não está neste PC')


@pytest.mark.parametrize('tipo', ['braco-robo', 'chip', 'cadeado-circuito', 'robo-pergunta', 'cadeado', 'interrogacao'])
@pytest.mark.parametrize('nivel', ['p', 'm', 'g'])
def test_cada_emblema_novo_desenha_algo_em_cada_nivel(tipo, nivel):
    m = D._mascara(tipo, 64, nivel == 'p', nivel)
    branco = sum(1 for v in m.tobytes() if v > 128)
    assert 64 * 64 * 0.04 < branco < 64 * 64 * 0.75, (tipo, nivel, branco)


def pasta_com_mao_e_robo(s):
    """Uma pasta azul de s px: a "mão" (bloco largo embaixo), o "robô" (bloco no alto) e duas perninhas
    finas que descem do robô até encostar na mão, como no desenho do Ettore."""
    F, W = (47, 111, 214), (255, 255, 255, 255)
    im = Image.new('RGBA', (s, s), (0, 0, 0, 0))
    k = s / 256
    for y in range(round(35 * k), round(77 * k)):
        for x in range(round(15 * k), round(110 * k)):
            im.putpixel((x, y), tuple(round(c * 0.77) for c in F) + (255,))
    for y in range(round(77 * k), round(225 * k)):
        for x in range(round(16 * k), round(240 * k)):
            im.putpixel((x, y), F + (255,))
    caixa = lambda x0, y0, x1, y1: [im.putpixel((x, y), W) for y in range(round(y0 * k), round(y1 * k))
                                    for x in range(round(x0 * k), round(x1 * k))]
    caixa(70, 160, 200, 210)          # a mão
    caixa(110, 100, 150, 136)         # o robô
    caixa(116, 140, 122, 158)         # as perninhas: soltas do robô e quase na mão (no desenho dele, só na diagonal)
    caixa(138, 140, 144, 158)
    return im


def test_trocar_por_chip_tira_o_robo_e_deixa_a_mao_intacta():
    F = '#2F6FD6'
    q = {s: pasta_com_mao_e_robo(s) for s in D.TAMANHOS}
    out = D.trocar_por_chip(q, F)
    for s in (16, 20, 24):
        assert out[s].tobytes() == q[s].tobytes()
    branco = lambda im, p: D._decompor(im.getpixel(p)[:3], D.hex_rgb(F))[0] >= 0.5
    for s in (32, 64, 128, 256):
        k = s / 256
        mao = [(x, y) for y in range(round(165 * k), round(205 * k)) for x in range(round(75 * k), round(195 * k))]
        assert all(out[s].getpixel(p) == q[s].getpixel(p) for p in mao), s
        assert not branco(out[s], (round(130 * k), int(101 * k))), s            # o alto do robô (acima do chip) saiu
    assert not branco(out[256], (117, 154)), 'a perninha ficou (entre o chip e a mão)'
    assert D._brancos(out[256], F) - D._brancos(q[256], F), 'o chip não foi desenhado'


def test_com_selo_copia_só_o_canto_de_baixo():
    a = Image.new('RGBA', (48, 48), (10, 20, 30, 255))
    correio = a.copy()
    correio.putpixel((40, 40), (1, 2, 3, 255))       # o selo
    correio.putpixel((5, 5), (9, 9, 9, 255))         # fora do canto: não vem
    alvo = Image.new('RGBA', (48, 48), (0, 0, 0, 255))
    out = D.com_selo(alvo, correio, a)
    assert out.getpixel((40, 40)) == (1, 2, 3, 255) and out.getpixel((5, 5)) == (0, 0, 0, 255)


@com_pacote
def test_receita_das_referencias_com_o_pacote_dele(tmp_path):
    mapa = json.loads(json.dumps(REAL))
    origem = D.refazer_quadros(PACOTE, mapa, tmp_path)
    assert set(origem) == {d['icone'] for d in {**REAL['verbos'], **REAL['marcas']}.values()}
    assert 'chip' in origem['eu-forneco-fontes'] and 'braco-robo' in origem['nao-toco']
    for i in origem:
        for s in D.TAMANHOS:
            assert (tmp_path / i / f'{s}.png').is_file()
    # os desenhos que não mudam são os dele, pixel a pixel
    dele = D.ler_ico(PACOTE / 'eu-leio.ico')
    assert all(D.ler_quadros('eu-leio', tmp_path)[s].tobytes() == dele[s].tobytes() for s in D.TAMANHOS)
