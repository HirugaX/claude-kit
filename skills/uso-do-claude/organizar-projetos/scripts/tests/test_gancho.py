"""O gancho PostToolUse (plano 4.4 e 4.5): calado sem pasta nova, calado fora da mãe, pinta a herdeira,
pergunta a provisória, sai 0 diante de qualquer erro, não usa Pillow, não segue junção, e é rápido."""
import json
import os
import subprocess
import sys
import time

import gancho as G
import regras as R
from conftest import SCRIPTS, juncao, so_windows


def entrada(cena, arquivo=None, cwd=None, tool='Write'):
    ti = {'file_path': str(arquivo)} if arquivo else {'command': 'mkdir x'}
    return {'tool_name': tool, 'tool_input': ti, 'cwd': str(cwd or cena.mae / 'app')}


def pintar_tudo(cena):
    import pastas as P
    P.cmd_aplicar(P.Contexto(cena.local), ver=False)


def test_calado_sem_pasta_nova(cena):
    pintar_tudo(cena)
    assert G.rodar(entrada(cena, cena.mae / 'app' / 'src' / 'a.py'), cena.local) is None


def test_calado_fora_da_mãe(cena):
    fora = cena.tmp / 'outro'
    (fora / 'nova').mkdir(parents=True)
    assert G.rodar(entrada(cena, fora / 'nova' / 'a.py', cwd=fora), cena.local) is None
    assert not (fora / 'nova' / 'desktop.ini').exists()


def test_pinta_a_herdeira_calado(cena):
    pintar_tudo(cena)
    nova = cena.mae / 'app' / 'src' / 'modulo_novo'
    nova.mkdir()
    assert G.rodar(entrada(cena, nova / 'a.py'), cena.local) is None
    assert R.marca_de(R.ler_ini(nova / 'desktop.ini')) == ('nosso', 'nao-toco')


def test_pasta_nova_pelo_bash_usa_o_cwd(cena):
    pintar_tudo(cena)
    nova = cena.mae / 'app' / 'docs' / 'notas'
    nova.mkdir()
    assert G.rodar(entrada(cena, tool='Bash'), cena.local) is None
    assert R.marca_de(R.ler_ini(nova / 'desktop.ini')) == ('nosso', 'nao-toco')


def test_provisória_devolve_a_pergunta(cena):
    pintar_tudo(cena)
    nova = cena.mae / 'app' / 'relatorios'
    nova.mkdir()
    saida = G.rodar(entrada(cena, nova / 'a.md'), cena.local)
    d = json.loads(saida)['hookSpecificOutput']
    assert d['hookEventName'] == 'PostToolUse'
    assert str(nova) in d['additionalContext'] and 'marcar' in d['additionalContext']
    assert R.marca_de(R.ler_ini(nova / 'desktop.ini')) == ('nosso', 'provisoria')
    assert G.rodar(entrada(cena, nova / 'b.md'), cena.local) is None      # pergunta uma vez só


def test_cwd_na_mãe_olha_só_o_primeiro_nível(cena):
    pintar_tudo(cena)
    (cena.mae / 'app' / 'src' / 'funda').mkdir()
    (cena.mae / 'projeto-novo').mkdir()
    saida = G.rodar(entrada(cena, tool='Bash', cwd=cena.mae), cena.local)
    assert 'projeto-novo' in saida
    assert not (cena.mae / 'app' / 'src' / 'funda' / 'desktop.ini').exists()


def test_não_pinta_rodada_nem_passageira(cena):
    pintar_tudo(cena)
    (cena.mae / 'app' / 'saida' / '0510_T').mkdir()
    (cena.mae / 'app' / 'entrada' / '_ESPERA2').mkdir()
    G.rodar(entrada(cena, tool='Bash'), cena.local)
    assert not (cena.mae / 'app' / 'saida' / '0510_T' / 'desktop.ini').exists()
    assert not (cena.mae / 'app' / 'entrada' / '_ESPERA2' / 'desktop.ini').exists()


@so_windows
def test_não_segue_junção(cena):
    pintar_tudo(cena)
    fora = cena.tmp / 'fora'
    (fora / 'dentro').mkdir(parents=True)
    juncao(cena.mae / 'app' / 'src' / 'atalho', fora)
    G.rodar(entrada(cena, tool='Bash'), cena.local)
    assert not list(fora.rglob('desktop.ini'))


def test_sem_icones_instalados_não_pinta(cena):
    for f in cena.icones.iterdir():
        f.unlink()
    (cena.mae / 'app' / 'src' / 'x').mkdir()
    assert G.rodar(entrada(cena, tool='Bash'), cena.local) is None
    assert not (cena.mae / 'app' / 'src' / 'x' / 'desktop.ini').exists()


def _rodar_processo(stdin: str, env_local: str):
    env = {**os.environ, 'CLAUDE_PASTAS_LOCAL': env_local}
    return subprocess.run([sys.executable, str(SCRIPTS / 'gancho.py')], input=stdin, capture_output=True, text=True,
                          env=env, timeout=30)


def test_sai_zero_com_entrada_inválida_e_sem_instalação(cena, tmp_path):
    for stdin in ('', 'não é json', '[1, 2]', '{"tool_input": 5}'):
        r = _rodar_processo(stdin, str(tmp_path / 'nao-existe.json'))
        assert r.returncode == 0 and r.stdout == '' and r.stderr == ''


def test_sai_zero_com_mapa_quebrado(cena, tmp_path):
    (cena.modulo / 'mapa.json').write_text('{quebrado', encoding='utf-8')
    lj = tmp_path / 'local.json'
    lj.write_text(json.dumps(cena.local), encoding='utf-8')
    r = _rodar_processo(json.dumps(entrada(cena, tool='Bash')), str(lj))
    assert r.returncode == 0 and r.stdout == ''


def test_não_importa_pillow(cena, tmp_path):
    lj = tmp_path / 'local.json'
    lj.write_text(json.dumps(cena.local), encoding='utf-8')
    (cena.mae / 'app' / 'outra').mkdir()
    codigo = ('import sys, json; sys.modules["PIL"] = None; sys.path.insert(0, sys.argv[1]); import gancho; '
              'print(gancho.rodar(json.loads(sys.argv[2]), json.loads(sys.argv[3])) is not None)')
    r = subprocess.run([sys.executable, '-c', codigo, str(SCRIPTS), json.dumps(entrada(cena, tool='Bash')),
                        json.dumps(cena.local)], capture_output=True, text=True, timeout=30)
    assert r.returncode == 0 and r.stdout.strip() == 'True', r.stderr


def test_p95_abaixo_de_150_ms_numa_árvore_grande(cena):
    """O plano 4.5: 20 chamadas sem pasta nova, p95 < 150 ms (aqui, ~600 pastas num projeto)."""
    for i in range(30):
        for j in range(20):
            (cena.mae / 'app' / 'src' / f'm{i}' / f's{j}').mkdir(parents=True)
    pintar_tudo(cena)
    tempos = []
    for _ in range(20):
        t = time.perf_counter()
        assert G.rodar(entrada(cena, cena.mae / 'app' / 'src' / 'm1' / 'a.py'), cena.local) is None
        tempos.append(time.perf_counter() - t)
    p95 = sorted(tempos)[18]
    assert p95 < 0.150, f'p95 {p95 * 1000:.0f} ms'
