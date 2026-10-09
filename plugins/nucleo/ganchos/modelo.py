# -*- coding: utf-8 -*-
r"""PreModelSwitch, em todo projeto: barra a troca para o Sonnet 5; deixa o Sonnet 5.5 e o resto.

Lição 1 (pesquisas\2026-10-05_fluxo-atual-dos-projetos.md): o atalho "sonnet" abriu o Sonnet 5 e a FF-P3c rodou
inteira nele; regra em texto não chega lá, gancho sim. Em 09/10 (2.1.291) o "/model sonnet" já resolve para o
claude-sonnet-5-5; o gancho continua barrando o claude-sonnet-5 pedido pelo ID, ou por um atalho que volte a ele.
Entrada (hooks#premodelswitch): from_model, to_model (ID), requested_model, source. Bloqueio: decision "block".
"""
from __future__ import annotations

from comum import SONNET_5, Amb, principal


def rodar(entrada: dict, amb: Amb) -> dict | None:
    para = str(entrada.get('to_model') or '')
    if SONNET_5.fullmatch(para):
        pedido = entrada.get('requested_model') or para
        return {'decision': 'block',
                'reason': (f'Troca barrada pelo gancho do nucleo: "{pedido}" abre o Sonnet 5 ({para}), não o 5.5. '
                           'Escolha o Sonnet 5.5 na lista do /model ou use o ID claude-sonnet-5-5.')}
    return None


if __name__ == '__main__':
    principal(rodar)
