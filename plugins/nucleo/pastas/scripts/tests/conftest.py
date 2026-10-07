"""Uma mãe de teste em pasta temporária, com o mesmo vocabulário do mapa real."""
import json
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

SCRIPTS = Path(__file__).resolve().parents[1]
MODULO = SCRIPTS.parent
sys.path.insert(0, str(SCRIPTS))

WIN = sys.platform == 'win32'
so_windows = pytest.mark.skipif(not WIN, reason='junção e atributos são do Windows')

REAL = json.loads((MODULO / 'mapa.json').read_text(encoding='utf-8'))

MAPA_TESTE = {
    'versao': 1,
    'verbos': REAL['verbos'],
    'marcas': REAL['marcas'],
    'nunca_cor': ['.git', 'node_modules', '__pycache__', '*.egg-info'],
    'mae': {'marca': 'projeto-ia', 'pastas': {'rascunhos': 'eu-leio'}},
    'projetos': {
        'app': {'raiz': 'projeto-ia', 'peacock': '#1565C0', 'pastas': {
            'src': 'nao-toco', 'docs': 'nao-toco', 'docs/para_o_outro': 'correio', 'docs/fontes': 'eu-forneco-fontes',
            'entrada': 'eu-alimento', 'entrada/*': 'sem-cor',
            'saida': 'trabalhamos-juntos', 'saida/[0-9][0-9][0-9][0-9]_*': 'sem-cor',
            'historico': 'dado-real', 'lixo/fontes': 'eu-leio'},
            'dicas': {'entrada': 'deposite aqui.'}},
        'app-dados': {'raiz': 'dado-real', 'pastas': {'arquivo/*': 'sem-cor'}},
    },
}


def juncao(link: Path, alvo: Path):
    subprocess.run(['cmd', '/c', 'mklink', '/J', str(link), str(alvo)], check=True, capture_output=True)


def pastas(raiz: Path, *rels):
    for r in rels:
        (raiz / r).mkdir(parents=True, exist_ok=True)


@pytest.fixture
def cena(tmp_path):
    mae = tmp_path / 'MAE'
    modulo = tmp_path / 'modulo'
    icones = tmp_path / 'icones'
    for p in (mae, modulo, icones):
        p.mkdir()
    (modulo / 'mapa.json').write_text(json.dumps(MAPA_TESTE, ensure_ascii=False), encoding='utf-8')
    for d in {**MAPA_TESTE['verbos'], **MAPA_TESTE['marcas']}.values():
        (icones / f'{d["icone"]}.ico').write_bytes(b'ico')
    pastas(mae, 'app/src/sub', 'app/docs/para_o_outro/velhas', 'app/docs/fontes', 'app/entrada/_ESPERA',
           'app/saida/0210_T/x', 'app/saida/_extra', 'app/historico/2026', 'app/.git/objects',
           'app/node_modules/pacote', 'app-dados/arquivo/0110_P', 'app-dados/_backups', 'rascunhos/a')
    local = {'mae': str(mae), 'modulo': str(modulo), 'icones': str(icones), 'lapides': []}
    return SimpleNamespace(tmp=tmp_path, mae=mae, modulo=modulo, icones=icones, local=local)
