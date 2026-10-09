# -*- coding: utf-8 -*-
r"""A medição semanal em segundo plano (Q39, Q42): a abertura lança este script, desligado, quando falta a linha de
uma semana já fechada no metricas\uso-semanal.csv deste PC. Não imprime nada.

Para cada semana que falta (terça a segunda, fuso local, só as já terminadas): roda o scripts\medir_semana.py com
--csv, --ctx0-csv e --mapa; depois refaz a planilha metricas\uso.xlsx. Um arquivo-trava em kit-local impede duas
medições ao mesmo tempo (duas janelas abrindo juntas). O registro (só datas e códigos de saída) fica em
kit-local\semana.log.

    python semana.py              # mede o que falta e refaz a planilha
    python semana.py --pendentes  # só lista as semanas que faltam (para conferir)
"""
from __future__ import annotations

import csv
import datetime as dt
import os
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comum import Amb, pc  # noqa: E402

TRAVA_SEG = 3 * 3600


def semanas_pendentes(kit: Path, rotulo: str, hoje: dt.date) -> list[str]:
    """As terças de início das semanas fechadas (início + 7 <= hoje) depois da última linha deste PC.

    Sem linha deste PC, só a última semana fechada (a linha de base de cada PC nasce na mão, como a da R1).
    """
    ultimo = None
    try:
        with open(kit / 'metricas' / 'uso-semanal.csv', encoding='utf-8') as f:
            for r in csv.DictReader(f):
                if r.get('pc') == rotulo and r.get('semana_inicio'):
                    d = dt.date.fromisoformat(r['semana_inicio'])
                    ultimo = d if not ultimo or d > ultimo else ultimo
    except Exception:
        pass
    fechada = hoje - dt.timedelta(days=7)
    ultima_fechada = fechada - dt.timedelta(days=(fechada.weekday() - 1) % 7)     # a terça de início
    if ultimo is None:
        return [ultima_fechada.isoformat()]
    saida, d = [], ultimo + dt.timedelta(days=7)
    while d <= ultima_fechada:
        saida.append(d.isoformat())
        d += dt.timedelta(days=7)
    return saida


def trava_livre(amb: Amb) -> bool:
    t = amb.local / 'semana.trava'
    try:
        return not t.exists() or amb.agora - t.stat().st_mtime > TRAVA_SEG
    except Exception:
        return False


def lancar(amb: Amb) -> bool:
    """Lança este script desligado do gancho (sobrevive ao fim da sessão). Devolve se lançou."""
    if not trava_livre(amb):
        return False
    try:
        amb.local.mkdir(parents=True, exist_ok=True)
        (amb.local / 'semana.trava').write_text(str(amb.agora), encoding='utf-8')
        flags = 0
        if os.name == 'nt':
            flags = subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
        kw = dict(stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, close_fds=True,
                  cwd=str(amb.kit))
        try:
            subprocess.Popen([sys.executable, str(Path(__file__).resolve())], creationflags=flags | 0x01000000, **kw)
        except OSError:                                    # o job do Claude Code não deixa sair: lança sem o breakaway
            subprocess.Popen([sys.executable, str(Path(__file__).resolve())], creationflags=flags, **kw)
        return True
    except Exception:
        return False


def _log(amb: Amb, texto: str) -> None:
    try:
        with open(amb.local / 'semana.log', 'a', encoding='utf-8') as f:
            f.write(time.strftime('%Y-%m-%d %H:%M ') + texto + '\n')
    except Exception:
        pass


def main() -> int:
    amb = Amb()
    rotulo = pc(amb)
    pend = semanas_pendentes(amb.kit, rotulo, dt.date.today())
    if '--pendentes' in sys.argv:
        print(' '.join(pend) or 'nenhuma')
        return 0
    m = amb.kit / 'metricas'
    script = amb.kit / 'scripts' / 'medir_semana.py'
    try:
        for s in pend:
            r = subprocess.run([sys.executable, str(script), '--inicio', s, '--so-linha', '--pc', rotulo,
                                '--csv', str(m / 'uso-semanal.csv'), '--ctx0-csv', str(m / 'ctx0-por-projeto.csv'),
                                '--mapa', str(m / 'pastas-projetos.csv')],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=1800)
            _log(amb, f'semana {s} pc {rotulo}: saída {r.returncode}')
        r = subprocess.run([sys.executable, str(script), '--planilha', str(m / 'uso.xlsx'), '--csv',
                            str(m / 'uso-semanal.csv')], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                           timeout=300)
        _log(amb, f'planilha: saída {r.returncode}')
    finally:
        try:
            (amb.local / 'semana.trava').unlink()
        except Exception:
            pass
    return 0


if __name__ == '__main__':
    sys.exit(main())
