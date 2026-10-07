"""aplicar, conferir, marcar, remover, legenda, vscode, o gancho no settings.json e o ignore do git."""
import json
from pathlib import Path
import subprocess

import pytest

import pastas as P
import regras as R
from conftest import juncao, so_windows


@pytest.fixture
def ctx(cena):
    return P.Contexto(cena.local)


def inis(mae):
    return {p.parent.relative_to(mae).as_posix() for p in mae.rglob('desktop.ini')}


def test_aplicar_ver_não_escreve(ctx, cena, capsys):
    P.cmd_aplicar(ctx, ver=True)
    assert inis(cena.mae) == set()
    assert 'a escrever' in capsys.readouterr().out


def test_aplicar_pinta_e_respeita_sem_cor(ctx, cena):
    P.cmd_aplicar(ctx, ver=False)
    feitos = inis(cena.mae)
    assert {'.', 'app', 'app/src', 'app/src/sub', 'app/docs/para_o_outro', 'app/historico', 'app/historico/2026',
            'app-dados', 'app-dados/_backups', 'app/entrada', 'app/saida', 'app/saida/_extra'} <= feitos
    proibidas = {'app/saida/0210_T', 'app/saida/0210_T/x', 'app/entrada/_ESPERA', 'app/.git', 'app/node_modules',
                 'app/node_modules/pacote', 'app-dados/arquivo/0110_P'}
    assert not feitos & proibidas


def test_aplicar_duas_vezes_não_escreve_nada_na_segunda(ctx, cena):
    P.cmd_aplicar(ctx, ver=False)
    acoes = [a for *_, a in P.plano(ctx)]
    assert 'escrever' not in acoes and 'tirar' not in acoes


def test_conferir_zero_depois_de_aplicar(ctx, capsys):
    P.cmd_aplicar(ctx, ver=False)
    assert P.cmd_conferir(ctx) == 0, capsys.readouterr().out


def test_conferir_acha_o_que_escapou(ctx, cena):
    P.cmd_aplicar(ctx, ver=False)
    (cena.mae / 'app' / 'src' / 'nova').mkdir()                          # pasta nova sem ini
    (cena.mae / 'app' / 'outra').mkdir()                                 # fora do mapa: provisória
    R.gravar_ini(cena.mae / 'app' / 'docs', R.montar_ini(ctx.ico('eu-leio'), 'x', 'eu-leio'))   # verbo errado
    R.gravar_ini(cena.mae / 'app' / 'saida' / '0210_T', R.montar_ini(ctx.ico('eu-leio'), 'x', 'eu-leio'))  # rodada
    (ctx.icones / 'eu-forneco-fontes.ico').unlink()                       # .ico ausente
    ctx.local['lapides'] = [str(cena.tmp / 'LAPIDE_QUE_FALTA')]
    prob, _ = P.achados(ctx)
    texto = '\n'.join(prob)
    assert 'src' in texto and 'nova' in texto
    assert 'provisória pendente' in texto
    assert 'verbo diferente do mapa' in texto
    assert 'ini em pasta sem cor' in texto
    assert '.ico ausente' in texto
    assert 'lápide ausente' in texto


@so_windows
def test_conferir_acha_pasta_com_r(ctx, cena):
    P.cmd_aplicar(ctx, ver=False)
    p = cena.mae / 'app' / 'src'
    R.por_atributos(p, R.atributos(p) | 0x1)
    prob, _ = P.achados(ctx)
    assert any('+r' in x for x in prob)
    P.cmd_aplicar(ctx, ver=False)                                       # o aplicar tira o +r
    assert not R.atributos(p) & 0x1


def test_conferir_acha_ini_dentro_de_rodada(ctx, cena):
    P.cmd_aplicar(ctx, ver=False)
    R.gravar_ini(cena.mae / 'app' / 'saida' / '0210_T' / 'x', R.montar_ini(ctx.ico('eu-leio'), 'x', 'eu-leio'))
    prob, _ = P.achados(ctx)
    assert any('dentro de pasta sem cor' in x for x in prob)


def test_conferir_não_acusa_amostra_com_os_próprios_icones(ctx, cena):
    P.cmd_aplicar(ctx, ver=False)
    amostra = cena.mae / 'app' / 'saida' / '0210_T' / 'amostra'
    amostra.mkdir()
    R.gravar_ini(amostra, R.montar_ini(amostra.parent / '_ico' / 'eu-leio.ico', 'x', 'eu-leio'))
    prob, _ = P.achados(ctx)
    assert not any('dentro de pasta sem cor' in x for x in prob)


def test_aplicar_tira_ini_de_pasta_que_virou_sem_cor(ctx, cena):
    R.gravar_ini(cena.mae / 'app' / 'entrada' / '_ESPERA', R.montar_ini('i.ico', 'x', 'eu-alimento'))
    P.cmd_aplicar(ctx, ver=False)
    assert not (cena.mae / 'app' / 'entrada' / '_ESPERA' / 'desktop.ini').exists()


def test_aplicar_guarda_o_ini_de_antes_alheio_e_de_3009(ctx, cena):
    alheio = cena.mae / 'app' / 'docs' / 'desktop.ini'
    alheio.write_text('[LocalizedFileNames]\nA.md=@A,0\n', encoding='utf-8')
    velho = cena.mae / 'app' / 'src' / 'desktop.ini'
    velho.write_text('[.ShellClassInfo]\nIconResource=C:\\v\\x.ico,0\n; DESOSP icones_pastas\n', encoding='utf-16')
    antes_a, antes_v = alheio.read_bytes(), velho.read_bytes()
    P.cmd_aplicar(ctx, ver=False)
    guardas = list((cena.icones.parent / 'antes').iterdir())
    assert len(guardas) == 1
    assert (guardas[0] / 'app' / 'docs' / 'desktop.ini').read_bytes() == antes_a
    assert (guardas[0] / 'app' / 'src' / 'desktop.ini').read_bytes() == antes_v
    assert not (guardas[0] / 'app' / 'historico' / 'desktop.ini').exists()     # o que não existia não se guarda


def test_troca_o_ini_de_3009(ctx, cena):
    p = cena.mae / 'app' / 'src'
    (p / 'desktop.ini').write_text('[.ShellClassInfo]\nIconResource=C:\\L\\DESOSP\\icones_pastas\\x.ico,0\n'
                                   '; DESOSP icones_pastas\n', encoding='utf-16')
    P.cmd_aplicar(ctx, ver=False)
    assert R.marca_de(R.ler_ini(p / 'desktop.ini')) == ('nosso', 'nao-toco')


@so_windows
def test_aplicar_não_segue_junção(ctx, cena):
    fora = cena.tmp / 'fora'
    (fora / 'dentro').mkdir(parents=True)
    juncao(cena.mae / 'app' / 'src' / 'atalho', fora)
    P.cmd_aplicar(ctx, ver=False)
    assert not list(fora.rglob('desktop.ini'))


def test_marcar_grava_no_mapa_e_pinta(ctx, cena):
    (cena.mae / 'app' / 'nova' / 'filha').mkdir(parents=True)
    P.cmd_marcar(ctx, cena.mae / 'app' / 'nova', 'eu-leio')
    mapa = json.loads((cena.modulo / 'mapa.json').read_text(encoding='utf-8'))
    assert mapa['projetos']['app']['pastas']['nova'] == 'eu-leio'
    assert R.marca_de(R.ler_ini(cena.mae / 'app' / 'nova' / 'desktop.ini')) == ('nosso', 'eu-leio')
    assert R.marca_de(R.ler_ini(cena.mae / 'app' / 'nova' / 'filha' / 'desktop.ini')) == ('nosso', 'eu-leio')


def test_marcar_pasta_da_mãe_como_projeto(ctx, cena):
    (cena.mae / 'novo-projeto').mkdir()
    P.cmd_marcar(ctx, cena.mae / 'novo-projeto', 'projeto-ia')
    mapa = json.loads((cena.modulo / 'mapa.json').read_text(encoding='utf-8'))
    assert mapa['projetos']['novo-projeto']['raiz'] == 'projeto-ia'


def test_marcar_recusa_verbo_desconhecido(ctx, cena):
    with pytest.raises(SystemExit):
        P.cmd_marcar(ctx, cena.mae / 'app' / 'src', 'azul')


def test_remover_tira_só_os_nossos(ctx, cena):
    P.cmd_aplicar(ctx, ver=False)
    alheio = cena.mae / 'app' / 'node_modules' / 'pacote' / 'desktop.ini'
    alheio.write_text('[LocalizedFileNames]\n', encoding='utf-8')
    P.cmd_remover(ctx, None)
    assert inis(cena.mae) == {'app/node_modules/pacote'}
    assert alheio.read_text(encoding='utf-8') == '[LocalizedFileNames]\n'


def test_legenda_tem_todo_verbo_e_todo_projeto(ctx, cena):
    P.cmd_legenda(ctx)
    html = (cena.mae / R.LEGENDA).read_text(encoding='utf-8')
    for d in ctx.mapa.defs.values():
        assert d['nome'].replace('—', '') .split()[0] in html
    assert 'app-dados' in html and '<h3>app' in html


def test_vscode_clones_e_conflito(ctx, cena):
    (cena.mae / 'app' / 'docs' / 'fontes').mkdir(exist_ok=True)
    (cena.mae / 'app' / 'lixo' / 'fontes').mkdir(parents=True)          # "fontes" com dois verbos
    clones, conflitos = P.clones_do_projeto(ctx, cena.mae / 'app')
    assert conflitos == ['fontes']
    nomes = {c['name']: c for c in clones}
    assert 'src' in nomes['claude-nao-toco']['folderNames']
    assert nomes['claude-nao-toco']['base'] == 'src' and nomes['claude-nao-toco']['color'] == '#2F6FD6'


def test_vscode_grava_settings_e_exclude(ctx, cena):
    subprocess.run(['git', 'init', '-q', str(cena.mae / 'app')], check=True)
    vs = cena.mae / 'app' / '.vscode'
    vs.mkdir()
    (vs / 'settings.json').write_text('{"editor.tabSize": 4}', encoding='utf-8')
    assert P.cmd_vscode(ctx, ver=False) == 0
    s = json.loads((vs / 'settings.json').read_text(encoding='utf-8'))
    assert s['editor.tabSize'] == 4 and s['peacock.color'] == '#1565C0'
    assert s['material-icon-theme.folders.customClones']
    assert '.vscode/settings.json' in (cena.mae / 'app' / '.git' / 'info' / 'exclude').read_text(encoding='utf-8')
    P.cmd_vscode(ctx, ver=False)
    assert (cena.mae / 'app' / '.git' / 'info' / 'exclude').read_text(encoding='utf-8').count('.vscode/settings.json') == 1


def test_vscode_não_mexe_em_settings_versionado(ctx, cena):
    app = cena.mae / 'app'
    subprocess.run(['git', 'init', '-q', str(app)], check=True)
    (app / '.vscode').mkdir()
    (app / '.vscode' / 'settings.json').write_text('{}', encoding='utf-8')
    subprocess.run(['git', '-C', str(app), 'add', '.vscode/settings.json'], check=True)
    assert P.cmd_vscode(ctx, ver=False) == 1
    assert (app / '.vscode' / 'settings.json').read_text(encoding='utf-8') == '{}'


def test_desligar_gancho_antigo_sem_apagar_os_outros(tmp_path):
    s = tmp_path / 'settings.json'
    outro = {'matcher': '*', 'hooks': [{'type': 'command', 'command': 'python semanal.py'}]}
    antigo = {'matcher': P.MATCHER, 'hooks': [{'type': 'command', 'timeout': 10,
              'command': 'python "C:/CLAUDE-PROJETOS/claude-kit/plugins/nucleo/skills/uso-do-claude/'
                         'organizar-projetos/scripts/gancho.py" || true'}]}
    s.write_text(json.dumps({'hooks': {'PostToolUse': [outro, antigo], 'SessionStart': [outro]}, 'model': 'x'}),
                 encoding='utf-8')
    assert P.desligar_gancho(s) == 'gancho desligado'
    d = json.loads(s.read_text(encoding='utf-8'))
    assert d['hooks'] == {'PostToolUse': [outro], 'SessionStart': [outro]} and d['model'] == 'x'
    assert list(tmp_path.glob('settings.json.antes-gancho-*'))
    assert P.desligar_gancho(s) == 'não havia gancho nosso'


def test_o_gancho_é_do_plugin_nucleo():
    """O hooks.json do nucleo chama o gancho.py deste módulo, com o matcher de sempre e o "|| true"."""
    d = json.loads(P.GANCHO_DO_PLUGIN.read_text(encoding='utf-8'))
    (g,) = d['hooks']['PostToolUse']
    (h,) = g['hooks']
    assert g['matcher'] == P.MATCHER and h['timeout'] == 10 and h['command'].endswith('|| true')
    alvo = h['command'].split('"')[1].replace('${CLAUDE_PLUGIN_ROOT}', str(P.MODULO.parent))
    assert P.e_gancho_nosso(h['command']) and Path(alvo).resolve() == (P.MODULO / 'scripts' / 'gancho.py').resolve()


def test_ignore_do_git_sem_repetir(tmp_path):
    f = tmp_path / 'git' / 'ignore'
    assert P.pôr_no_ignore(f) is True
    assert P.pôr_no_ignore(f) is False
    assert f.read_text(encoding='utf-8') == 'desktop.ini\n'


def test_instalar_gera_os_icones_e_o_local(cena, tmp_path):
    local = tmp_path / 'lj' / 'local.json'
    P.cmd_instalar(cena.mae, [r'C:\VELHO'], ignore=tmp_path / 'ign', destino_local=local)
    d = json.loads(local.read_text(encoding='utf-8'))
    assert d['mae'] == str(cena.mae) and d['lapides'] == [r'C:\VELHO']
    icos = list((local.parent / 'icones').glob('*.ico'))
    assert len(icos) == 9
    assert (tmp_path / 'ign').read_text(encoding='utf-8') == 'desktop.ini\n'
