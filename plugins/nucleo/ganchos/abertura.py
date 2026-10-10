# -*- coding: utf-8 -*-
r"""SessionStart: o que a janela precisa saber ao abrir. Base: desosp-app\.claude\hooks\abertura.py (só leitura).

1ª camada, em todo projeto (calada quando não há o que dizer):
  - modelo errado: Sonnet 5 ou Opus 5 (o 5.5 é o certo; lição 1). O modelo vem da entrada; em -p ela não o traz, e
    o gancho lê o --model da linha de comando do processo do Claude (CLAUDE_PID; ~1,5 s, só nesse caso);
  - esforço xhigh ou max (o da sessão, CLAUDE_EFFORT, ou o gravado por modelo): só com motivo escrito (lição 2);
  - o git pull --ff-only do kit, no máximo uma vez por hora (sem pedir senha: GIT_TERMINAL_PROMPT=0). Divergiu:
    avisa. Trouxe commit: roda o instalar_kit.py --verificar e dá uma linha só se houver achado;
  - a medição semanal: falta a linha de uma semana fechada → lança o semana.py em segundo plano, sem imprimir;
  - o balanço das métricas vencido (15 dias): uma linha só com números, que manda abrir a janela da raiz.
2ª camada, só onde existe docs\ESTADO.md:
  - o estado curto ("## Onde estamos"), a fila (perguntas abertas), a caixa e o git (arquivo modificado ao abrir
    costuma ser outra janela);
  - no /clear, injeta o docs\PROXIMO.md (a reserva do painel: /clear e "siga");
  - grava o hash do ESTADO.md desta sessão (o portão do Stop confere se ele foi reescrito).
Os avisos (modelo, esforço, kit, balanço) também vão ao usuário (systemMessage).
"""
from __future__ import annotations

import datetime as dt
import os
import re
import subprocess
import sys
from pathlib import Path

from comum import (OPUS_5, SONNET_5, Amb, estado_sessao, gravar_json, gravar_sessao, hash_de, ler_json, ler_texto,
                   modelo_de, pc, principal, projeto_de, tem_estado)

ESFORCO_ALTO = {'xhigh', 'max'}
UMA_HORA = 3600
DIAS_BALANCO = 15
LIMITE_ARQUIVOS = 5
FEITO = ('confirmado', 'lido', 'feito', 'aplicado', 'arquivado')


# ---------------------------------------------------------------- 1ª camada

def modelo_da_linha_de_comando(amb: Amb) -> str | None:
    pid = amb.env.get('CLAUDE_PID', '')
    if amb.sem_rede or not pid.isdigit():
        return None
    try:
        r = subprocess.run(['powershell', '-NoProfile', '-Command',
                            f"(Get-CimInstance Win32_Process -Filter 'ProcessId={pid}').CommandLine"],
                           capture_output=True, text=True, timeout=5)
        m = re.search(r'--model[ =]"?([A-Za-z0-9_.\-\[\]]+)', r.stdout or '')
        return m.group(1) if m else None
    except Exception:
        return None


def aviso_modelo(modelo: str | None) -> str | None:
    if not modelo:
        return None
    if SONNET_5.fullmatch(modelo):
        return (f'modelo {modelo}: é o Sonnet 5, não o 5.5. Troque pela lista do /model (Sonnet 5.5) ou pelo ID '
                'claude-sonnet-5-5 antes de começar.')
    if OPUS_5.fullmatch(modelo):
        return f'modelo {modelo}: é o Opus 5, não o 5.5 (rebaixamento). Volte com /model antes de começar.'
    return None


def aviso_esforco(modelo: str | None, amb: Amb) -> str | None:
    # Numa sessão sem gente (-p, --bg) lançada de dentro de outra, o CLAUDE_EFFORT é o herdado da mãe (visto em
    # 10/10: as perguntas de controle avisaram o max desta janela): ali vale só o gravado.
    sem_gente = amb.env.get('CLAUDE_CODE_SESSION_ATTENDED') == '0'
    nivel = None if sem_gente else (amb.env.get('CLAUDE_EFFORT') or None)
    origem = 'desta sessão'
    if not nivel:
        por_modelo = (ler_json(amb.casa / 'settings.json').get('modelSettings') or {})
        nivel = (por_modelo.get(modelo or 'claude-opus-5-5') or {}).get('effortLevel')
        origem = 'gravado'
    if nivel in ESFORCO_ALTO:
        return (f'esforço {origem}: {nivel} — só com motivo escrito. Se a 1ª linha do prompt pede outro nível, '
                'digite /effort <nível> antes de começar.')
    return None


def _git(kit: Path, *args, timeout=15) -> subprocess.CompletedProcess:
    env = {'GIT_TERMINAL_PROMPT': '0', 'GCM_INTERACTIVE': 'never'}
    return subprocess.run(['git', '-C', str(kit), *args], capture_output=True, text=True, encoding='utf-8',
                          errors='replace', timeout=timeout, env={**os.environ, **env})


def puxar_kit(amb: Amb) -> str | None:
    """git pull --ff-only do kit, uma vez por hora. Devolve uma linha só se divergiu ou se o --verificar achou algo."""
    if amb.sem_rede or not (amb.kit / '.git').exists():
        return None
    reg = ler_json(amb.local / 'abertura.json')
    if amb.agora - float(reg.get('pull', 0)) < UMA_HORA:
        return None
    reg['pull'] = amb.agora
    gravar_json(amb.local / 'abertura.json', reg)
    try:
        antes = _git(amb.kit, 'rev-parse', 'HEAD').stdout.strip()
        r = _git(amb.kit, 'pull', '--ff-only', '--quiet')
        if r.returncode != 0:
            erro = (r.stderr or '').lower()
            if 'fast-forward' in erro or 'diverg' in erro:
                return 'kit: o git pull --ff-only falhou porque o kit divergiu do origin. Resolva numa janela do kit.'
            return None                                    # sem rede, sem login: calado
        if _git(amb.kit, 'rev-parse', 'HEAD').stdout.strip() == antes:
            return None
        v = subprocess.run([sys.executable, str(amb.kit / 'scripts' / 'instalar_kit.py'), '--verificar'],
                           capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=60)
        if v.returncode != 0:
            m = re.search(r'Verificação: (\d+) achado', v.stdout or '')
            n = m.group(1) if m else '?'
            return (f'kit: o pull trouxe commits e o instalar_kit.py --verificar tem {n} achado(s). Rode python '
                    f'{amb.kit}\\scripts\\instalar_kit.py (sem o --verificar, conserta).')
    except Exception:
        return None
    return None


def medir_semana(amb: Amb) -> None:
    if amb.sem_rede:
        return
    try:
        import semana
        if semana.semanas_pendentes(amb.kit, pc(amb), dt.date.fromtimestamp(amb.agora)):
            semana.lancar(amb)
    except Exception:
        pass


def aviso_balanco(amb: Amb) -> str | None:
    """O balanço quinzenal vencido (Q42), só com números."""
    m = amb.kit / 'metricas'
    datas = []
    try:
        for f in (m / 'balancos').glob('*.md'):
            try:
                datas.append(dt.date.fromisoformat(f.stem[:10]))
            except ValueError:
                pass
    except Exception:
        pass
    base = max(datas) if datas else None
    if base is None:
        desde = ler_json(amb.kit / 'config' / 'fluxo.json').get('balanco_desde')
        try:
            base = dt.date.fromisoformat(desde)
        except Exception:
            return None
    hoje = dt.date.fromtimestamp(amb.agora)
    dias = (hoje - base).days
    if dias < DIAS_BALANCO:
        return None
    try:
        import csv
        with open(m / 'uso-semanal.csv', encoding='utf-8') as f:
            novas = sum(1 for r in csv.DictReader(f) if r.get('semana_inicio', '') >= base.isoformat())
    except Exception:
        novas = 0
    ult = f'o último em {base:%d/%m}' if datas else f'nenhum desde {base:%d/%m}'
    return (f'balanço das métricas vencido: {dias} dias ({ult}), {novas} semana(s) no CSV desde então. Abra a janela '
            'da raiz (C:\\CLAUDE-PROJETOS) e peça: rode o claude-kit\\metricas\\BALANCO.md.')


# ---------------------------------------------------------------- 2ª camada

def estado_curto(projeto: Path) -> str | None:
    t = ler_texto(projeto / 'docs' / 'ESTADO.md', 30_000)
    if not t:
        return None
    titulo = next((ln.lstrip('# ').strip() for ln in t.splitlines() if ln.startswith('# ')), '')
    m = re.search(r'^## Onde estamos\s*$(.*?)(?=^## |\Z)', t, re.M | re.S)
    corpo = m.group(1).strip() if m else ''
    if len(corpo) > 1800:
        corpo = corpo[:1800] + ' …'
    return f'estado (docs\\ESTADO.md): {titulo}' + (f'\n{corpo}' if corpo else '')


def fila_aberta(projeto: Path) -> int:
    t = ler_texto(projeto / 'docs' / 'PERGUNTAS.md') or ''
    m = re.search(r'^## Abertas\s*$(.*?)(?=^## |\Z)', t, re.M | re.S)
    return len(re.findall(r'^### P\d+', m.group(1), re.M)) if m else 0


def pendentes(texto: str, serie: str | None = None) -> list[str]:
    """Linhas de índice de caixa sem status de recebido. O status é a última célula; o número, a primeira."""
    saida = []
    for ln in texto.splitlines():
        m = re.match(r'\|\s*([A-Z]{2,4})-(\d+)\s*\|', ln)
        if not m or (serie and m.group(1) != serie):
            continue
        status = [c.strip() for c in ln.strip().strip('|').split('|')][-1]
        if not any(x in status.lower() for x in FEITO):
            saida.append(f'{m.group(1)}-{m.group(2)} ({status[:30]})')
    return saida


def caixa(projeto: Path, amb: Amb) -> str | None:
    itens: list[str] = []
    k = projeto / 'caixa' / 'INDICE.md'                    # a caixa do kit, entre os PCs: este PC lê a série do outro
    if k.is_file():
        itens += pendentes(ler_texto(k) or '', 'DK' if pc(amb) == 'notebook' else 'NB')
    for idx in sorted((projeto / 'docs').glob('para_*/INDICE*.md')):
        itens += pendentes(ler_texto(idx) or '')
    if not itens:
        return None
    return 'caixa: pendentes ' + ', '.join(itens[:10]) + (' …' if len(itens) > 10 else '') + ' — decida o destino de cada um'


def git_do_projeto(projeto: Path) -> str | None:
    try:
        r = subprocess.run(['git', 'status', '--porcelain=v1', '-b'], cwd=projeto, capture_output=True, text=True,
                           encoding='utf-8', errors='replace', timeout=5)
    except Exception:
        return 'não consegui ler o git status'
    if r.returncode != 0:
        return None
    linhas = r.stdout.splitlines()
    cabeca = linhas[0][3:] if linhas and linhas[0].startswith('## ') else ''
    mods = [ln[3:].strip() for ln in linhas[1:] if len(ln) > 3]
    ramo = cabeca.split('...')[0].split(' ')[0] or '?'
    texto = f'git: {ramo}'
    fr = re.search(r'ahead (\d+)', cabeca)
    at = re.search(r'behind (\d+)', cabeca)
    if fr or at:
        texto += f', {fr.group(1) if fr else 0} à frente e {at.group(1) if at else 0} atrás do origin'
    if mods:
        nomes = ', '.join(mods[:LIMITE_ARQUIVOS]) + (' …' if len(mods) > LIMITE_ARQUIVOS else '')
        texto += (f' · {len(mods)} arquivo(s) sem commit: {nomes} — pode ser outra janela trabalhando: confira antes '
                  'de tocar neles')
    return texto


def proximo(projeto: Path) -> str | None:
    t = ler_texto(projeto / 'docs' / 'PROXIMO.md', 9000)
    if not t:
        return None
    return ('docs\\PROXIMO.md (o prompt desta fase, injetado no /clear; quando o usuário disser "siga", siga-o):\n'
            + t.strip())


# ---------------------------------------------------------------- junta

def rodar(entrada: dict, amb: Amb) -> dict | None:
    projeto = projeto_de(entrada, amb)
    fonte = entrada.get('source') or 'startup'
    modelo = modelo_de(entrada) or modelo_da_linha_de_comando(amb)
    avisos = [a for a in (aviso_modelo(modelo), aviso_esforco(modelo, amb), puxar_kit(amb)) if a]
    medir_semana(amb)
    if fonte in ('startup', 'clear'):
        b = aviso_balanco(amb)
        if b:
            avisos.append(b)

    linhas: list[str] = []
    if tem_estado(projeto):
        sid = entrada.get('session_id')
        s = estado_sessao(amb, sid)
        if 'estado_hash' not in s:
            s['estado_hash'] = hash_de(projeto / 'docs' / 'ESTADO.md')
            gravar_sessao(amb, sid, s)
        n = fila_aberta(projeto)
        linhas += [x for x in (estado_curto(projeto),
                               f'fila: {n} pergunta(s) aberta(s) em docs\\PERGUNTAS.md' if n else None,
                               caixa(projeto, amb), git_do_projeto(projeto)) if x]
        if fonte == 'clear':
            p = proximo(projeto)
            if p:
                linhas.append(p)
    if not avisos and not linhas:
        return None
    texto = '\n'.join(['[abertura — gancho do nucleo]'] + [f'🛑 {a}' for a in avisos] + linhas)
    if avisos:
        texto += '\nDiga os avisos 🛑 ao usuário na primeira resposta.'
    saida = {'hookSpecificOutput': {'hookEventName': 'SessionStart', 'additionalContext': texto[:9800]}}
    if avisos:
        saida['systemMessage'] = ' · '.join(avisos)
    return saida


if __name__ == '__main__':
    principal(rodar)
