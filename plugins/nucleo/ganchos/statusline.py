# -*- coding: utf-8 -*-
r"""A statusline do terminal (Ficha item 7; Q1, Q39): modelo, esforço, % do contexto, % do limite de 5 h e o semanal.

Ligada no ~\.claude\settings.json ("statusLine": {"type": "command", "command": "python <kit>/plugins/nucleo/ganchos/
statusline.py"}); roda local, sem token. Entrada (statusline#available-data): model.display_name, effort.level,
context_window.used_percentage, rate_limits.five_hour e seven_day (used_percentage, resets_at; só Pro/Max e só depois
da 1ª resposta). Quando os % mudam, acrescenta uma linha em kit-local\limites.jsonl (ts, h5, h5_fim, sem, sem_fim):
é a única fonte do % semanal, e o scripts\medir_semana.py lê o arquivo para a coluna pct_limite_semanal. Só números.
"""
from __future__ import annotations

import json
import sys
import time

from comum import Amb, ler_entrada, ler_json, gravar_json

MAX_BYTES = 2_000_000


def _pct(v) -> int | None:
    try:
        return None if v is None else round(float(v))
    except (TypeError, ValueError):
        return None


def limites(entrada: dict) -> dict:
    rl = entrada.get('rate_limits') or {}
    h5, sem = rl.get('five_hour') or {}, rl.get('seven_day') or {}
    return {'h5': _pct(h5.get('used_percentage')), 'h5_fim': h5.get('resets_at'),
            'sem': _pct(sem.get('used_percentage')), 'sem_fim': sem.get('resets_at')}


def anotar(lim: dict, amb: Amb) -> None:
    if lim['h5'] is None and lim['sem'] is None:
        return
    ult = amb.local / 'limites.ultimo.json'
    chave = {k: lim[k] for k in ('h5', 'sem')}
    if ler_json(ult) == chave:
        return
    try:
        arq = amb.local / 'limites.jsonl'
        amb.local.mkdir(parents=True, exist_ok=True)
        if arq.exists() and arq.stat().st_size > MAX_BYTES:
            arq.replace(arq.with_suffix('.jsonl.1'))
        with open(arq, 'a', encoding='utf-8') as f:
            f.write(json.dumps({'ts': round(amb.agora), **lim}) + '\n')
        gravar_json(ult, chave)
    except Exception:
        pass


def linha(entrada: dict) -> str:
    partes = [str((entrada.get('model') or {}).get('display_name') or (entrada.get('model') or {}).get('id') or '?')]
    esf = (entrada.get('effort') or {}).get('level')
    if esf:
        partes.append(str(esf))
    ctx = _pct((entrada.get('context_window') or {}).get('used_percentage'))
    if ctx is not None:
        partes.append(f'ctx {ctx}%')
    lim = limites(entrada)
    if lim['h5'] is not None:
        partes.append(f'5h {lim["h5"]}%')
    if lim['sem'] is not None:
        partes.append(f'sem {lim["sem"]}%')
    return ' · '.join(partes)


def main() -> None:
    try:
        entrada = ler_entrada()
        amb = Amb(agora=time.time())
        anotar(limites(entrada), amb)
        sys.stdout.buffer.write(linha(entrada).encode('utf-8'))
    except Exception:
        sys.stdout.write('?')


if __name__ == '__main__':
    main()
