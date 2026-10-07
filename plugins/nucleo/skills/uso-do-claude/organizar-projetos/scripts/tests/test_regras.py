"""A regra de cada pasta (plano 4.2), o andar sem junção e o formato do desktop.ini (plano 4.3 e 4.4)."""
import os
import shutil

import pytest

import regras as R
from conftest import MAPA_TESTE, MODULO, REAL, juncao, so_windows


@pytest.fixture
def m(cena):
    return R.Mapa(MAPA_TESTE, cena.mae)


def v(m, caminho, mae_verbo=None):
    """O verbo de um caminho relativo à mãe, descendo pela regra (sem precisar da pasta existir)."""
    partes, atual = (), m.verbo((), None)
    for nome in caminho.split('/'):
        partes += (nome.casefold(),)
        atual = m.verbo(partes, atual)
        if atual == R.SEM_COR:
            return atual
    return atual


# ---------------------------------------------------------------- a regra

def test_mae_e_raiz_de_projeto(m):
    assert m.verbo((), None) == 'projeto-ia'
    assert v(m, 'app') == 'projeto-ia'
    assert v(m, 'app-dados') == 'dado-real'


def test_entrada_exata_e_herança(m):
    assert v(m, 'app/src') == 'nao-toco'
    assert v(m, 'app/src/sub/neta') == 'nao-toco'
    assert v(m, 'app/docs/fontes/livro') == 'eu-forneco-fontes'


def test_maiuscula_não_importa(m):
    assert v(m, 'APP/SRC') == 'nao-toco'


def test_correio_e_dado_real_não_passam_às_filhas(m):
    assert v(m, 'app/docs/para_o_outro') == 'correio'
    assert v(m, 'app/docs/para_o_outro/velhas') == 'nao-toco'
    assert v(m, 'app/historico') == 'dado-real'
    assert v(m, 'app/historico/2026') == 'nao-toco'
    assert v(m, 'app-dados/_backups') == 'nao-toco'


def test_nunca_cor_vence_tudo(m):
    assert v(m, 'app/.git') == R.SEM_COR
    assert v(m, 'app/src/node_modules') == R.SEM_COR
    assert v(m, 'app/src/x.egg-info') == R.SEM_COR


def test_rodada_e_passageira_sem_cor_e_sem_descer(m):
    assert v(m, 'app/saida/0210_T') == R.SEM_COR
    assert v(m, 'app/saida/0210_T/dentro') == R.SEM_COR
    assert v(m, 'app/saida/_extra') == 'trabalhamos-juntos'
    assert v(m, 'app/entrada/_ESPERA') == R.SEM_COR
    assert v(m, 'app-dados/arquivo/0110_P') == R.SEM_COR


def test_fora_do_mapa_vira_provisória_e_as_filhas_ficam_sem_cor(m):
    assert v(m, 'app/nova') == R.PROVISORIA
    assert v(m, 'outro-projeto') == R.PROVISORIA
    assert v(m, 'app/nova/filha') == R.SEM_COR


def test_entrada_da_mãe(m):
    assert v(m, 'rascunhos') == 'eu-leio'
    assert v(m, 'rascunhos/a') == 'eu-leio'


def test_prefixo_não_engana_app_e_app_dados(cena):
    m = R.Mapa(MAPA_TESTE, cena.mae)
    assert m.rel(cena.mae / 'app-dados' / 'x') == ('app-dados', 'x')
    assert m.rel(cena.mae.parent / 'MAE-outra') is None          # irmã com o mesmo começo
    assert v(m, 'app-dados') == 'dado-real' and v(m, 'app') == 'projeto-ia'


def test_verbo_desconhecido_no_mapa_é_recusado(cena):
    ruim = {**MAPA_TESTE, 'projetos': {'p': {'raiz': 'projeto-ia', 'pastas': {'a': 'azul'}}}}
    with pytest.raises(ValueError):
        R.Mapa(ruim, cena.mae)


# ---------------------------------------------------------------- andar

def test_andar_não_desce_em_sem_cor_nem_nunca_cor(cena, m):
    vistas = {'/'.join(p) for _, p, _ in m.andar()}
    assert 'app/saida/0210_t' in vistas and 'app/saida/0210_t/x' not in vistas
    assert 'app/.git' in vistas and 'app/.git/objects' not in vistas
    assert 'app/node_modules/pacote' not in vistas


@so_windows
def test_andar_e_verbo_de_nunca_seguem_junção(cena, m):
    fora = cena.tmp / 'fora'
    (fora / 'dentro').mkdir(parents=True)
    juncao(cena.mae / 'app' / 'src' / 'atalho', fora)
    vistas = {'/'.join(p) for _, p, _ in m.andar()}
    assert not any('atalho' in x for x in vistas)
    assert m.verbo_de(cena.mae / 'app' / 'src' / 'atalho' / 'dentro') == R.SEM_COR


def test_verbo_de_fora_da_mãe(cena, m):
    assert m.verbo_de(cena.tmp) is None


def test_andar_com_nível_máximo(cena, m):
    vistas = {'/'.join(p) for _, p, _ in m.andar(cena.mae, 1)}
    assert vistas == {'', 'app', 'app-dados', 'rascunhos'}


# ---------------------------------------------------------------- o mapa real

def test_mapa_real_carrega_e_cada_ícone_tem_os_quadros():
    m = R.Mapa(REAL, r'C:\CLAUDE-PROJETOS')
    import desenho
    for d in m.defs.values():
        for s in desenho.TAMANHOS:
            assert (MODULO / 'icones' / d['icone'] / f'{s}.png').is_file(), (d['icone'], s)


@pytest.mark.parametrize('caminho, esperado', [
    ('desosp-censo', 'projeto-ia'),
    ('desosp-censo/saida/0210_T', 'sem-cor'),
    ('desosp-censo/saida/_extracao', 'nao-toco'),
    ('desosp-censo/saida/_revisao_02out/backup', 'nao-toco'),
    ('desosp-censo/arquivo/0110_P', 'sem-cor'),
    ('desosp-censo/entrada', 'eu-alimento'),
    ('desosp-censo/entrada/_ESPERA', 'sem-cor'),
    ('desosp-censo/historico', 'dado-real'),
    ('desosp-censo/historico/sub', 'nao-toco'),
    ('desosp-censo/docs/para_o_app', 'correio'),
    ('desosp-censo/docs/gpt', 'eu-leio'),
    ('desosp-censo/docs/guia', 'nao-toco'),
    ('desosp-censo/.claude/worktrees', 'sem-cor'),
    ('desosp-app/docs/fontes/x', 'eu-forneco-fontes'),
    ('desosp-app/tests/vendor', 'nao-toco'),
    ('desosp-app-dados', 'dado-real'),
    ('desosp-app-dados/_backups', 'nao-toco'),
    ('desosp-app-dados/saida/0210_T', 'sem-cor'),
    ('desosp-hc/docs/premiacoes/arte', 'eu-forneco-fontes'),
    ('desosp-hc/privado', 'dado-real'),
    ('desosp-hc/historico/rodadas/2026-09', 'sem-cor'),
    ('desosp-hc/historico/_arquivo_tecnico/a', 'nao-toco'),
    ('desosp-hc/saida/boletins', 'sem-cor'),
    ('desosp-hc/node_modules', 'sem-cor'),
    ('claude-kit/pesquisas', 'eu-leio'),
    ('claude-kit/plugins/nucleo/skills/uso-do-claude/fontes', 'eu-forneco-fontes'),
    ('claude-kit/plugins/nucleo/skills/uso-do-claude/organizar-projetos', 'nao-toco'),
    ('prototipos-icones', 'eu-leio'),
    ('projeto-que-ainda-nao-existe', 'provisoria'),
])
def test_mapa_real_as_regras_do_plano(caminho, esperado):
    m = R.Mapa(REAL, r'C:\CLAUDE-PROJETOS')
    assert v(m, caminho) == esperado


# ---------------------------------------------------------------- o desktop.ini

def test_formato_do_ini(cena):
    t = R.montar_ini(r'C:\x\eu-alimento.ico', 'Eu alimento — deposite. Legenda: C:\\MAE\\LEGENDA DAS PASTAS.html', 'eu-alimento')
    assert t.startswith(R.MARCA + ' eu-alimento\r\n[.ShellClassInfo]\r\n')
    assert 'IconResource=C:\\x\\eu-alimento.ico,0\r\n' in t
    assert 'ConfirmFileOp' not in t
    R.gravar_ini(cena.mae, t)
    b = (cena.mae / 'desktop.ini').read_bytes()
    assert b[:2] == b'\xff\xfe'
    texto = b[2:].decode('utf-16-le')
    assert '\r\n' in texto and '\n' not in texto.replace('\r\n', '')
    infotip = [l for l in texto.splitlines() if l.startswith('InfoTip=')][0]
    assert infotip.endswith('Legenda: C:\\MAE\\LEGENDA DAS PASTAS.html')
    assert R.marca_de(texto) == ('nosso', 'eu-alimento')


def test_infotip_termina_na_legenda_e_usa_a_dica_da_pasta(cena, m):
    t = m.infotip(('app', 'entrada'), 'eu-alimento')
    assert t.startswith('Eu alimento — deposite aqui.')
    assert t.endswith(f'Legenda: {cena.mae / R.LEGENDA}')


@so_windows
def test_atributos_pasta_s_sem_r_e_ini_oculto_e_de_sistema(cena):
    p = cena.mae / 'app' / 'src'
    R.por_atributos(p, R.atributos(p) | 0x1)        # o +r do pacote de 30/09
    R.gravar_ini(p, R.montar_ini('i.ico', 'dica', 'nao-toco'))
    a = R.atributos(p)
    assert a & 0x4 and not a & 0x1
    ai = R.atributos(p / 'desktop.ini')
    assert ai & 0x2 and ai & 0x4


def test_idempotente(cena):
    p = cena.mae / 'app' / 'src'
    t = R.montar_ini('i.ico', 'dica', 'nao-toco')
    assert R.gravar_ini(p, t) is True
    assert R.gravar_ini(p, t) is False
    assert R.gravar_ini(p, R.montar_ini('i.ico', 'outra dica', 'nao-toco')) is True   # regrava oculto


def test_copiar_e_apagar_pasta_pintada_funciona(cena):
    """A regressão do WinError 5 (01/10): com +r, a cópia não se apagava."""
    p = cena.mae / 'app' / 'src'
    R.gravar_ini(p, R.montar_ini('i.ico', 'dica', 'nao-toco'))
    copia = cena.tmp / 'copia'
    shutil.copytree(p, copia)
    shutil.rmtree(copia)
    assert not copia.exists()


def test_ini_de_3009_é_trocado_inteiro(cena):
    velho = '[.ShellClassInfo]\r\nIconResource=C:\\v\\x.ico,0\r\nInfoTip=velha\r\n; DESOSP icones_pastas\r\n'
    t = R.montar_ini('n.ico', 'nova', 'eu-leio', velho)
    assert 'velha' not in t and 'DESOSP icones_pastas' not in t and 'n.ico' in t


def test_ini_alheio_preservado_em_utf8(cena):
    p = cena.mae / 'rascunhos'
    (p / 'desktop.ini').write_text('[LocalizedFileNames]\r\nARQ.md=@ARQ,0\r\n[.ShellClassInfo]\r\nLocalizedResourceName=X\r\n',
                                   encoding='utf-8')
    alheio = R.ler_ini(p / 'desktop.ini')
    assert R.marca_de(alheio)[0] == 'alheio'
    t = R.montar_ini('i.ico', 'dica', 'eu-leio', alheio)
    assert '[LocalizedFileNames]\r\nARQ.md=@ARQ,0' in t and 'LocalizedResourceName=X' in t
    R.gravar_ini(p, t)
    assert R.tirar_ini(p) is True
    resto = R.ler_ini(p / 'desktop.ini')
    assert 'ARQ.md=@ARQ,0' in resto and R.MARCA not in resto and 'IconResource' not in resto


def test_tirar_o_nosso_apaga_o_arquivo(cena):
    p = cena.mae / 'app' / 'src'
    R.gravar_ini(p, R.montar_ini('i.ico', 'dica', 'nao-toco'))
    assert R.tirar_ini(p) is True
    assert not (p / 'desktop.ini').exists()
    assert R.tirar_ini(p) is False


def test_ler_ini_aceita_utf16_utf8_e_ausente(cena):
    p = cena.mae / 'a.ini'
    p.write_bytes(b'\xff\xfe' + 'ação'.encode('utf-16-le'))
    assert R.ler_ini(p) == 'ação'
    p.write_text('ação', encoding='utf-8')
    assert R.ler_ini(p) == 'ação'
    assert R.ler_ini(cena.mae / 'nao-existe.ini') is None
