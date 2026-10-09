# -*- coding: utf-8 -*-
r"""PreToolUse em Bash|PowerShell, só nas pastas de teste (teste-fluxo, teste-ferramentas; Q40): barra o
analyze-sessions do session-report sem --dir.

Sem --dir, o analisador lê as transcrições de todos os projetos deste PC, inclusive as dos desosp- (dado de
paciente). Ligado pelo .claude\settings.json de cada pasta de teste (config\plugins.json, tipo "teste").
"""
from __future__ import annotations

import re

from comum import Amb, negar_ferramenta, principal


def rodar(entrada: dict, amb: Amb) -> dict | None:
    cmd = str((entrada.get('tool_input') or {}).get('command') or '')
    if 'analyze-sessions' not in cmd or re.search(r'(^|\s)--dir(\s|=|$)', cmd):
        return None
    return negar_ferramenta('analyze-sessions sem --dir lê as transcrições de todos os projetos (Q40). Rode de novo '
                            'com --dir apontando para a pasta das transcrições deste projeto em ~/.claude/projects.')


if __name__ == '__main__':
    principal(rodar)
