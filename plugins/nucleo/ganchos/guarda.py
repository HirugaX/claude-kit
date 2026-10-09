# -*- coding: utf-8 -*-
r"""PreToolUse em Write|Edit|MultiEdit|NotebookEdit, só onde existe docs\ESTADO.md: barra a escrita em pasta de dado
fora da lista aprovada (Q21; ponto da Q10).

Pasta de dado (ADR-0001 D6, ADR-0002):
  - as irmãs <projeto>-dados e <projeto>-backups na pasta-mãe (de qualquer projeto: a sessão não escreve no dado de
    outro);
  - os caminhos do deny (Read/Edit) do .claude\settings.json e do settings.local.json do projeto.
A lista aprovada é a coluna "pasta" da tabela "## Escritas em dado real aprovadas" do docs\PROXIMO.md (caminho
absoluto, ou relativo ao projeto). Escrita dentro de uma pasta aprovada passa; fora, é negada com o motivo.
"""
from __future__ import annotations

import os
import re
from pathlib import Path

from comum import Amb, ler_json, ler_texto, negar_ferramenta, principal, projeto_de, tem_estado

FERRAMENTAS = ('Write', 'Edit', 'MultiEdit', 'NotebookEdit')


def _norm(p: str | Path) -> str:
    return os.path.normcase(os.path.abspath(str(p))).rstrip('\\/')


def _dentro(alvo: str, pasta: str) -> bool:
    return alvo == pasta or alvo.startswith(pasta + os.sep)


def _caminho_da_regra(regra: str, projeto: Path) -> str | None:
    m = re.fullmatch(r'\s*(?:Read|Edit|Write)\((.+)\)\s*', regra)
    if not m:
        return None
    c = m.group(1).strip()
    c = re.sub(r'(/\*\*|/\*)+$', '', c)
    if re.match(r'^//[A-Za-z]/', c):                      # //c/CLAUDE-PROJETOS/x  ->  c:/CLAUDE-PROJETOS/x
        c = c[2] + ':' + c[3:]
    elif c.startswith('~/'):
        c = str(Path.home() / c[2:])
    elif not re.match(r'^[A-Za-z]:', c):
        c = str(projeto / c.lstrip('./'))
    return _norm(c) if c else None


def pastas_de_dado(projeto: Path) -> list[str]:
    pastas = []
    mae = projeto.parent
    try:
        for d in mae.iterdir():
            if d.is_dir() and (d.name.endswith('-dados') or d.name.endswith('-backups')):
                pastas.append(_norm(d))
    except Exception:
        pass
    for nome in ('settings.json', 'settings.local.json'):
        for regra in ((ler_json(projeto / '.claude' / nome).get('permissions') or {}).get('deny') or []):
            c = _caminho_da_regra(str(regra), projeto)
            if c and c != _norm(projeto):
                pastas.append(c)
    return pastas


def aprovadas(projeto: Path) -> list[str]:
    r"""A coluna "pasta" da tabela "## Escritas em dado real aprovadas" do docs\PROXIMO.md."""
    texto = ler_texto(projeto / 'docs' / 'PROXIMO.md') or ''
    m = re.search(r'^## Escritas em dado real aprovadas\s*$(.*?)(?=^## |\Z)', texto, re.M | re.S)
    if not m:
        return []
    saida = []
    for linha in m.group(1).splitlines():
        cel = [c.strip() for c in linha.strip().strip('|').split('|')] if linha.strip().startswith('|') else []
        if len(cel) < 2 or set(cel[1]) <= set('-: ') or cel[1].lower() == 'pasta' or '<' in cel[1]:
            continue
        c = cel[1].strip('`').strip()
        if c:
            saida.append(_norm(c if re.match(r'^[A-Za-z]:', c) else projeto / c))
    return saida


def rodar(entrada: dict, amb: Amb) -> dict | None:
    if entrada.get('tool_name') not in FERRAMENTAS:
        return None
    projeto = projeto_de(entrada, amb)
    if not tem_estado(projeto):
        return None
    ti = entrada.get('tool_input') or {}
    arq = ti.get('file_path') or ti.get('notebook_path')
    if not arq:
        return None
    p = Path(arq)
    if not p.is_absolute():
        p = Path(entrada.get('cwd') or projeto) / p
    alvo = _norm(p)
    dado = next((d for d in pastas_de_dado(projeto) if _dentro(alvo, d)), None)
    if not dado or any(_dentro(alvo, a) for a in aprovadas(projeto)):
        return None
    return negar_ferramenta(
        f'Escrita em pasta de dado ({dado}) fora das "Escritas em dado real aprovadas" do docs\\PROXIMO.md: é ponto '
        'da Q10, nunca sem o "sim". Na execução largada, ponha na fila (docs\\PERGUNTAS.md) e siga com o resto; numa '
        'sessão supervisionada, pergunte.')


if __name__ == '__main__':
    principal(rodar)
