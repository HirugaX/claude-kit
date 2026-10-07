r"""O gancho PostToolUse do sistema de cores: pinta a pasta que acabou de nascer.

Ligado por "pastas.py ligar-gancho" no settings.json de usuário, com o matcher
Write|Edit|MultiEdit|NotebookEdit|Bash|PowerShell e o comando  python "<módulo>/scripts/gancho.py" || true
(os ganchos rodam no Git Bash: o "|| true" impede que um erro apareça ao Claude em todo comando).

O que faz:
  - fora da mãe (ou sem o sistema instalado neste PC): sai calado;
  - varre o projeto do arquivo tocado (ou do cwd); com o cwd na própria mãe, só o primeiro nível;
  - pasta "nova" = pasta com cor no mapa e sem desktop.ini: pinta calado;
  - se a pasta nova é provisória (fora do mapa), pinta com o "?" e devolve additionalContext pedindo ao
    Claude que pergunte a cor;
  - sem pasta nova, não imprime nada (zero token).
Sai sempre com 0, inclusive diante de entrada inválida, mapa ausente ou erro. Não usa Pillow.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent


def _alvo(entrada: dict) -> Path | None:
    ti = entrada.get('tool_input') or {}
    for k in ('file_path', 'notebook_path', 'path'):
        if isinstance(ti.get(k), str) and ti[k]:
            p = Path(ti[k])
            if not p.is_absolute() and entrada.get('cwd'):
                p = Path(entrada['cwd']) / p
            return p if p.is_dir() else p.parent
    return Path(entrada['cwd']) if entrada.get('cwd') else None


def rodar(entrada: dict, local: dict | None = None) -> str | None:
    """O trabalho do gancho. Devolve o texto JSON a imprimir, ou None (calado)."""
    sys.path.insert(0, str(AQUI))
    import regras as R
    local = local or R.ler_local()
    if not local:
        return None
    alvo = _alvo(entrada)
    if alvo is None:
        return None
    mapa = R.Mapa(R.carregar_mapa(Path(local['modulo']) / 'mapa.json'), local['mae'])
    partes = mapa.rel(alvo)
    if partes is None:
        return None
    if partes:
        escopo, nivel = mapa.mae / Path(os.path.abspath(alvo)).parts[len(mapa.mae.parts)], None
    else:
        escopo, nivel = mapa.mae, 1
    icones = Path(local['icones'])
    novas = []
    for p, ps, v in mapa.andar(escopo, nivel):
        if v == R.SEM_COR or (p / 'desktop.ini').exists():
            continue
        ico = icones / f'{mapa.defs[v]["icone"]}.ico'
        if not ico.exists():
            continue
        R.gravar_ini(p, R.montar_ini(ico, mapa.infotip(ps, v), v))
        if v == R.PROVISORIA:
            novas.append(str(p))
    if not novas:
        return None
    pastas_py = (Path(local['modulo']) / 'scripts' / 'pastas.py').as_posix()
    nomes = ', '.join(f'"{d}" ({mapa.defs[d]["nome"]})' for d in mapa.dados.get('verbos', {}))
    texto = (f'Sistema de cores das pastas: pasta(s) nova(s) fora do mapa, marcada(s) como provisória ("?"): '
             f'{"; ".join(novas)}. Pergunte ao usuário qual verbo cada uma recebe ({nomes}; ou "sem-cor" se for '
             f'passageira) e grave com: python "{pastas_py}" marcar "<pasta>" <verbo>.')
    return json.dumps({'hookSpecificOutput': {'hookEventName': 'PostToolUse', 'additionalContext': texto}},
                      ensure_ascii=False)


def main() -> int:
    try:
        entrada = json.loads(sys.stdin.read() or '{}')
        if not isinstance(entrada, dict):
            return 0
        saida = rodar(entrada)
        if saida:
            sys.stdout.reconfigure(encoding='utf-8')
            print(saida)
    except Exception:
        pass
    return 0


if __name__ == '__main__':
    sys.exit(main())
