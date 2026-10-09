# -*- coding: utf-8 -*-
r"""PreToolUse em Agent, em todo projeto: despacho sem effort recebe o lembrete da tabela de papéis. Não bloqueia.

O controle da regra do esforço por papel (skill orquestrar §2): na semana de 29/09, 1.197 chamadas do Sonnet 5.5
rodaram em max, quase todas em subagentes, porque o subagente sem effort herda o da sessão.
"""
from __future__ import annotations

from comum import Amb, contexto, principal

LEMBRETE = ('Despacho sem effort: o subagente herda o esforço da sessão. Fixe model e effort pelo papel (skill '
            'orquestrar §2): explorador haiku (sem esforço) ou sonnet low-medium; especialista e revisor isolado opus '
            'high; implementador SDD sonnet medium; revisor final SDD opus high. Refaça o despacho com effort, salvo '
            'se o herdado for de propósito.')


def rodar(entrada: dict, amb: Amb) -> dict | None:
    if entrada.get('tool_name') not in ('Agent', 'Task'):
        return None
    ti = entrada.get('tool_input') or {}
    if ti.get('effort') or 'haiku' in str(ti.get('model') or ''):    # o haiku não tem esforço
        return None
    return contexto('PreToolUse', LEMBRETE)


if __name__ == '__main__':
    principal(rodar)
