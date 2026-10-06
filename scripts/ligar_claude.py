r"""Liga o kit do Claude (a pasta acima desta) ao Claude Code.

O Claude Code só procura as skills pessoais em C:\Users\<você>\.claude\skills e só lê o
CLAUDE.md pessoal em C:\Users\<você>\.claude\CLAUDE.md. Os arquivos de verdade moram no kit
(hoje C:\CLAUDE-PROJETOS\claude-kit); no lugar que o Claude Code lê ficam só ligações:

  - cada skill: uma junção de pasta (o "atalho" de pasta do Windows, sem precisar de admin);
  - o CLAUDE.md pessoal: um hardlink (o mesmo arquivo com dois endereços).

    python <kit>\scripts\ligar_claude.py                  # confere e liga
    python <kit>\scripts\ligar_claude.py --conferir       # só diz o que faria
    python <kit>\scripts\ligar_claude.py --raiz-antiga C:\VELHO
                                                          # junções que apontam para o kit velho
                                                          # passam a apontar para este
    python <kit>\scripts\ligar_claude.py --pasta-vence    # skill atualizada pelo `npx skills`
    python <kit>\scripts\ligar_claude.py --kit-vence      # cópia velha (de outro PC) não vence o kit

O kit se acha pela posição deste arquivo: mudou de lugar, rode de novo. Junção sem alvo (o kit
velho sumiu) passa a apontar para cá sozinha.

Skill que caiu como pasta de verdade em ~\.claude\skills (o `npx skills` faz isso):
  - não existe no kit: vem para o kit e fica a junção no lugar;
  - existe no kit com o mesmo conteúdo: fica a junção (a pasta repetida vai para _substituidas);
  - existe no kit com conteúdo DIFERENTE: o script avisa e não mexe. Diga quem vence:
    --pasta-vence (atualização pelo npx) ou --kit-vence (o kit é o original).
Nada é apagado: o que sai vai para skills\_substituidas\.

As cores das pastas não são mais daqui: são do pacote das pastas, dentro da skill uso-do-claude.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]      # o kit: a pasta acima de scripts\
CLAUDE_HOME = Path.home() / '.claude'
NAO_MEXER = {'synced'}   # skills sincronizadas pelo claude.ai: quem cuida é o próprio Claude


def _junção(link: Path, alvo: Path) -> None:
    r = subprocess.run(['cmd', '/c', 'mklink', '/J', str(link), str(alvo)], capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f'falhou a junção {link}: {r.stderr or r.stdout}')


def _tirar_junção(link: Path) -> None:
    """Apaga só a junção; o alvo fica intacto. Nunca rmtree numa junção."""
    if not os.path.isjunction(link):
        raise SystemExit(f'{link} não é junção; não apago')
    os.rmdir(link)


def _alvo(link: Path) -> Path:
    return Path(os.path.realpath(link))


def _dentro(p: Path, raiz: Path) -> bool:
    try:
        p.resolve().relative_to(raiz.resolve())
        return True
    except ValueError:
        return False


DE_CADA_PC = {'desktop.ini', 'thumbs.db'}   # o sistema de cores e o Windows os põem em cada PC: não contam


def _impressão(pasta: Path) -> dict:
    """Caminho relativo -> sha256 de cada arquivo (ignora __pycache__, desktop.ini e Thumbs.db)."""
    out = {}
    for f in sorted(pasta.rglob('*')):
        if f.is_file() and '__pycache__' not in f.parts and f.name.lower() not in DE_CADA_PC:
            out[f.relative_to(pasta).as_posix()] = hashlib.sha256(f.read_bytes()).hexdigest()
    return out


def _guardar(p: Path, skills: Path) -> Path:
    guarda = skills / '_substituidas' / f'{p.name}_{time.strftime("%Y%m%d_%H%M%S")}'
    guarda.parent.mkdir(exist_ok=True)
    shutil.move(str(p), str(guarda))
    return guarda


def ligar_skills(skills: Path, skills_home: Path, conferir: bool = False, raiz_antiga: Path | None = None,
                 kit_vence: bool = False, pasta_vence: bool = False) -> list[str]:
    feito: list[str] = []
    if not conferir:
        skills.mkdir(parents=True, exist_ok=True)
        skills_home.mkdir(parents=True, exist_ok=True)
    if skills_home.exists():
        for p in sorted(skills_home.iterdir()):
            if p.name in NAO_MEXER or p.name.startswith('.'):
                continue
            destino = skills / p.name
            if os.path.isjunction(p):
                alvo = _alvo(p)
                if destino.exists() and alvo == destino.resolve():
                    continue
                velho = raiz_antiga is not None and _dentro(alvo, raiz_antiga)
                if destino.is_dir() and (not alvo.exists() or velho):
                    if conferir:
                        feito.append(f're-apontaria {p} -> {destino} (hoje -> {alvo})')
                        continue
                    _tirar_junção(p)
                    _junção(p, destino)
                    feito.append(f'junção {p} re-apontada para {destino} (era {alvo})')
                else:
                    feito.append(f'ATENÇÃO: {p} é junção para outro lugar ({alvo}); não mexi')
                continue
            if not p.is_dir():
                continue
            # uma pasta de verdade
            if not destino.exists():
                if conferir:
                    feito.append(f'moveria {p} -> {destino} e deixaria a junção')
                    continue
                shutil.move(str(p), str(destino))
                _junção(p, destino)
                feito.append(f'skill nova {p.name} trazida para o kit; junção no lugar')
                continue
            igual = _impressão(p) == _impressão(destino)
            if not igual and not (kit_vence or pasta_vence):
                feito.append(f'ATENÇÃO: {p} é pasta de verdade e difere da do kit ({destino}); não mexi. '
                             f'Rode com --pasta-vence (atualização pelo npx) ou --kit-vence (o kit é o original)')
                continue
            if conferir:
                quem = 'iguais' if igual else ('vence a pasta' if pasta_vence else 'vence o kit')
                feito.append(f'trocaria {p} pela junção para {destino} ({quem})')
                continue
            if not igual and pasta_vence:
                g = _guardar(destino, skills)
                shutil.move(str(p), str(destino))
                feito.append(f'{p.name}: a pasta venceu; a versão do kit foi para {g}')
            else:
                g = _guardar(p, skills)
                feito.append(f'{p.name}: {"iguais" if igual else "o kit venceu"}; a pasta foi para {g}')
            _junção(p, destino)
    # skill do kit ainda sem junção na pasta do Claude Code
    if skills.exists():
        for d in sorted(skills.iterdir()):
            if not d.is_dir() or d.name.startswith('_') or d.name.startswith('.'):
                continue
            link = skills_home / d.name
            if not link.exists() and not os.path.isjunction(link):
                if conferir:
                    feito.append(f'faria junção {link} -> {d}')
                else:
                    _junção(link, d)
                    feito.append(f'junção {link} -> {d}')
    return feito


def ligar_claude_md(raiz: Path, claude_home: Path, conferir: bool = False) -> list[str]:
    casa, aqui = claude_home / 'CLAUDE.md', raiz / 'CLAUDE.md'
    if casa.exists() and aqui.exists():
        if os.path.samefile(casa, aqui):
            return []
        return [f'ATENÇÃO: {casa} e {aqui} são arquivos DIFERENTES — junte à mão e rode de novo; não mexi']
    if conferir:
        return [f'ligaria {casa} <-> {aqui}'] if (casa.exists() or aqui.exists()) else []
    if casa.exists():
        os.link(casa, aqui)            # o arquivo de casa ganha um segundo endereço no kit
    elif aqui.exists():
        os.link(aqui, casa)
    else:
        return []
    return [f'CLAUDE.md pessoal mora em {aqui}; {casa} é o mesmo arquivo (hardlink)']


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--conferir', action='store_true', help='só diz o que faria')
    ap.add_argument('--raiz-antiga', type=Path, help='kit velho: junções que apontam para ele passam a apontar para este')
    g = ap.add_mutually_exclusive_group()
    g.add_argument('--kit-vence', action='store_true', help='pasta de verdade diferente vai para _substituidas; o kit fica')
    g.add_argument('--pasta-vence', action='store_true', help='pasta de verdade diferente vence (atualização pelo npx)')
    a = ap.parse_args(argv)
    feito = ligar_skills(RAIZ / 'skills', CLAUDE_HOME / 'skills', a.conferir, a.raiz_antiga, a.kit_vence, a.pasta_vence)
    feito += ligar_claude_md(RAIZ, CLAUDE_HOME, a.conferir)
    print('\n'.join(feito) if feito else 'Tudo já ligado: nada a fazer.')
    return 1 if any(f.startswith('ATENÇÃO') for f in feito) else 0


if __name__ == '__main__':
    sys.exit(main())
