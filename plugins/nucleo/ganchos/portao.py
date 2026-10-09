# -*- coding: utf-8 -*-
r"""Stop, só onde existe docs\ESTADO.md: a fase dada como pronta sem o ESTADO.md reescrito não fecha (Q3; skill
fechar-janela).

"Dada como pronta" = a última mensagem traz a linha "Sinais de insuficiência do modelo", que todo resumo de
fechamento leva (CLAUDE.md pessoal). Aí o portão exige:
  - docs\ESTADO.md reescrito nesta sessão: o hash difere do gravado pela abertura (sem o registro, a data do arquivo
    é posterior ao início da transcrição);
  - se a sessão pôs perguntas na fila (gancho fila.py), o docs\PERGUNTAS.md existe com perguntas em "## Abertas".
Fechar com perguntas abertas é aceito quando os dois estão gravados (fechar porque tudo depende da fila).
Bloqueia até 8 vezes seguidas (o Claude Code também corta na 8ª continuação seguida); na 9ª deixa fechar e avisa.
"""
from __future__ import annotations

import os
import re
from pathlib import Path

from comum import Amb, estado_sessao, gravar_sessao, hash_de, ler_texto, principal, projeto_de, tem_estado

MARCA = re.compile(r'sinais de insufici[eê]ncia do modelo', re.I)
MAX_BLOQUEIOS = 8


def _ultima_mensagem(entrada: dict) -> str:
    m = entrada.get('last_assistant_message')
    return m if isinstance(m, str) else ''


def _estado_reescrito(projeto: Path, entrada: dict, sessao: dict) -> bool:
    arq = projeto / 'docs' / 'ESTADO.md'
    if sessao.get('estado_hash'):
        return hash_de(arq) != sessao['estado_hash']
    try:
        inicio = os.path.getctime(entrada['transcript_path'])
        return os.path.getmtime(arq) >= inicio
    except Exception:
        return True                     # sem como saber: não prende a sessão


def _fila_gravada(projeto: Path) -> bool:
    texto = ler_texto(projeto / 'docs' / 'PERGUNTAS.md') or ''
    m = re.search(r'^## Abertas\s*$(.*?)(?=^## |\Z)', texto, re.M | re.S)
    return bool(m and re.search(r'^### P\d+', m.group(1), re.M))


def rodar(entrada: dict, amb: Amb) -> dict | None:
    projeto = projeto_de(entrada, amb)
    if not tem_estado(projeto) or not MARCA.search(_ultima_mensagem(entrada)):
        return None
    sid = entrada.get('session_id')
    s = estado_sessao(amb, sid)
    faltas = []
    if not _estado_reescrito(projeto, entrada, s):
        faltas.append('docs\\ESTADO.md não foi reescrito nesta sessão (modelo e regras: skill fechar-janela, passo 2)')
    if s.get('fila') and not _fila_gravada(projeto):
        faltas.append(f'a sessão pôs {s["fila"]} pergunta(s) na fila, mas o docs\\PERGUNTAS.md não tem nenhuma em '
                      '"## Abertas"')
    if not faltas:
        if s.get('bloqueios'):
            s['bloqueios'] = 0
            gravar_sessao(amb, sid, s)
        return None
    s['bloqueios'] = s.get('bloqueios', 0) + 1
    gravar_sessao(amb, sid, s)
    if s['bloqueios'] > MAX_BLOQUEIOS:
        return {'systemMessage': f'Portão do nucleo: a fase fechou sem o estado gravado depois de {MAX_BLOQUEIOS} '
                                 'bloqueios (' + '; '.join(faltas) + ').'}
    return {'decision': 'block',
            'reason': ('Portão do nucleo: a fase foi dada como pronta, mas ' + '; e '.join(faltas) + '. Grave antes '
                       'de fechar; se tudo o que sobra depende da fila, grave o ESTADO.md e o PERGUNTAS.md e feche '
                       f'assim. (bloqueio {s["bloqueios"]} de {MAX_BLOQUEIOS})')}


if __name__ == '__main__':
    principal(rodar)
