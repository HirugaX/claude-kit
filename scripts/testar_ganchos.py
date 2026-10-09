# -*- coding: utf-8 -*-
r"""Testa os ganchos do nucleo por JSON (F2b): cada caso roda o script do gancho como o Claude Code o roda — um
processo com o JSON da entrada no stdin — e confere o JSON da saída.

    python scripts\testar_ganchos.py          # todos os casos; sai com 1 se algum falhar
    python scripts\testar_ganchos.py -v       # mostra também a saída de cada caso

Tudo acontece numa pasta temporária: uma pasta-mãe falsa com um projeto (com e sem docs\ESTADO.md), a irmã
<projeto>-dados, um kit falso (config\fluxo.json, metricas\) e o kit-local. Sem rede: KIT_SEM_REDE=1 desliga o git
pull, o processo em segundo plano e a leitura da linha de comando do Claude.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

KIT = Path(__file__).resolve().parents[1]
GANCHOS = KIT / 'plugins' / 'nucleo' / 'ganchos'
HOOKS_JSON = KIT / 'plugins' / 'nucleo' / 'hooks' / 'hooks.json'
VERBOSO = '-v' in sys.argv

resultados: list[tuple[str, bool, str]] = []


def caso(nome: str, ok: bool, detalhe: str = '') -> None:
    resultados.append((nome, bool(ok), detalhe))


class Mundo:
    def __init__(self, raiz: Path):
        self.raiz = raiz
        self.mae = raiz / 'mae'
        self.proj = self.mae / 'proj'
        self.sem = self.mae / 'semestado'
        self.dados = self.mae / 'proj-dados'
        self.kit = raiz / 'kit'
        self.local = raiz / 'local'
        self.casa = raiz / 'casa'
        for d in (self.proj / 'docs', self.sem, self.dados / 'saida', self.dados / 'outra', self.kit / 'config',
                  self.kit / 'metricas' / 'balancos', self.local, self.casa, self.proj / '.claude'):
            d.mkdir(parents=True, exist_ok=True)
        (self.proj / 'docs' / 'ESTADO.md').write_text(
            '# Estado do proj — 09/10/2026, F1\n\n## Objetivo\n\nx\n\n## Onde estamos\n\n- **Feito:** a fase F0\n'
            '- **Próximo passo:** a F1\n\n## Riscos\n\n- nenhum\n', encoding='utf-8')
        (self.proj / '.claude' / 'settings.json').write_text(
            json.dumps({'permissions': {'deny': ['Edit(./workspace_dev/**)', 'Read(./workspace_dev/**)']}}),
            encoding='utf-8')
        (self.kit / 'config' / 'fluxo.json').write_text(json.dumps(
            {'pcs': {'PCTESTE': 'notebook'}, 'balanco_desde': dt.date.today().isoformat()}), encoding='utf-8')
        (self.kit / 'metricas' / 'uso-semanal.csv').write_text('semana_inicio,pc\n', encoding='utf-8')
        (self.casa / 'settings.json').write_text(json.dumps(
            {'modelSettings': {'claude-opus-5-5': {'effortLevel': 'high'}}}), encoding='utf-8')

    def env(self, **extra) -> dict:
        e = {k: v for k, v in os.environ.items() if not k.startswith(('CLAUDE', 'KIT_'))}
        e.update(KIT_LOCAL=str(self.local), KIT_CASA=str(self.casa), KIT_RAIZ=str(self.kit), KIT_SEM_REDE='1',
                 CLAUDE_PROJECT_DIR=str(self.proj), CLAUDE_CODE_SESSION_ATTENDED='1', COMPUTERNAME='PCTESTE',
                 PYTHONIOENCODING='utf-8')
        e.update({k: str(v) for k, v in extra.items()})
        return e

    def rodar(self, gancho: str, entrada: dict, **env) -> dict | str | None:
        entrada = {'session_id': 'sessao-teste', 'cwd': str(env.get('CLAUDE_PROJECT_DIR', self.proj)), **entrada}
        r = subprocess.run([sys.executable, str(GANCHOS / f'{gancho}.py')], input=json.dumps(entrada).encode('utf-8'),
                           capture_output=True, env=self.env(**env), timeout=60)
        out = r.stdout.decode('utf-8', 'replace').strip()
        if VERBOSO:
            print(f'  [{gancho}] saída {r.returncode}: {out[:300]}', r.stderr.decode('utf-8', 'replace')[:300])
        if r.returncode != 0:
            return f'<saída {r.returncode}>'
        if not out:
            return None
        try:
            return json.loads(out)
        except Exception:
            return out


def decisao(saida) -> str | None:
    if not isinstance(saida, dict):
        return None
    h = saida.get('hookSpecificOutput') or {}
    return h.get('permissionDecision') or (h.get('decision') or {}).get('behavior') or saida.get('decision')


def ctx(saida) -> str:
    return ((saida or {}).get('hookSpecificOutput') or {}).get('additionalContext', '') if isinstance(saida, dict) else ''


# ---------------------------------------------------------------- os casos

def testar_hooks_json() -> None:
    d = json.loads(HOOKS_JSON.read_text(encoding='utf-8'))
    caso('hooks.json: tem o invólucro "hooks"', isinstance(d.get('hooks'), dict))
    faltando = []
    for ev, grupos in d['hooks'].items():
        for g in grupos:
            for h in g['hooks']:
                c = h['command']
                alvo = c.split('${CLAUDE_PLUGIN_ROOT}/')[1].split('"')[0] if '${CLAUDE_PLUGIN_ROOT}/' in c else ''
                if not (KIT / 'plugins' / 'nucleo' / alvo).is_file():
                    faltando.append(f'{ev}:{alvo}')
    caso('hooks.json: todo script citado existe', not faltando, ', '.join(faltando))
    eventos = set(d['hooks'])
    caso('hooks.json: os 6 eventos do F2b + o das cores',
         {'SessionStart', 'PreModelSwitch', 'Stop', 'PreToolUse', 'PermissionRequest', 'PostToolUse'} <= eventos)


def testar_modelo(m: Mundo) -> None:
    for para, barra in (('claude-sonnet-5', True), ('claude-sonnet-5[1m]', True), ('claude-sonnet-5-5', False),
                        ('claude-opus-5-5', False)):
        s = m.rodar('modelo', {'hook_event_name': 'PreModelSwitch', 'from_model': 'claude-opus-5-5',
                               'to_model': para, 'requested_model': 'sonnet', 'source': 'command'})
        caso(f'PreModelSwitch: {para} {"barrado" if barra else "passa"}', (decisao(s) == 'block') == barra, str(s))


def testar_despacho(m: Mundo) -> None:
    base = {'hook_event_name': 'PreToolUse', 'tool_name': 'Agent'}
    s = m.rodar('despacho', {**base, 'tool_input': {'prompt': 'x', 'subagent_type': 'Explore', 'model': 'sonnet'}})
    caso('Agent sem effort: lembrete da tabela, sem bloquear', 'orquestrar §2' in ctx(s) and decisao(s) is None, str(s))
    s = m.rodar('despacho', {**base, 'tool_input': {'prompt': 'x', 'model': 'sonnet', 'effort': 'medium'}})
    caso('Agent com effort: calado', s is None, str(s))
    s = m.rodar('despacho', {**base, 'tool_input': {'prompt': 'x', 'model': 'haiku'}})
    caso('Agent em haiku (sem esforço): calado', s is None, str(s))


def testar_guarda(m: Mundo) -> None:
    def w(caminho, **env):
        return m.rodar('guarda', {'hook_event_name': 'PreToolUse', 'tool_name': 'Write',
                                  'tool_input': {'file_path': str(caminho), 'content': 'x'}}, **env)
    caso('guarda: Write na irmã proj-dados sem lista → nega', decisao(w(m.dados / 'saida' / 'a.csv')) == 'deny')
    caso('guarda: Write no próprio projeto → passa', w(m.proj / 'src' / 'a.py') is None)
    caso('guarda: Write no deny interno (workspace_dev) → nega', decisao(w(m.proj / 'workspace_dev' / 'a.db')) == 'deny')
    (m.proj / 'docs' / 'PROXIMO.md').write_text(
        'Opus 5.5 · /effort medium\n\n## Escritas em dado real aprovadas\n| comando ou rotina | pasta | limite |\n'
        f'|---|---|---|\n| python x.py | `{m.dados / "saida"}` | uma vez |\n| <ex.> | <pasta> | <lim> |\n\n'
        '## Decisões pré-aprovadas\n', encoding='utf-8')
    caso('guarda: Write na pasta aprovada no PROXIMO.md → passa', w(m.dados / 'saida' / 'b.csv') is None)
    caso('guarda: Write em outra pasta de dado → nega', decisao(w(m.dados / 'outra' / 'b.csv')) == 'deny')
    s = w(m.dados / 'outra' / 'b.csv', CLAUDE_PROJECT_DIR=m.sem)
    caso('guarda: projeto sem ESTADO.md → calada (2ª camada)', s is None, str(s))


def testar_fila(m: Mundo) -> None:
    perg = m.proj / 'docs' / 'PERGUNTAS.md'
    if perg.exists():
        perg.unlink()
    ask = {'hook_event_name': 'PreToolUse', 'tool_name': 'AskUserQuestion', 'tool_input': {'questions': [
        {'question': 'Qual formato do relatório?', 'header': 'Formato', 'multiSelect': False,
         'options': [{'label': 'CSV', 'description': 'simples'}, {'label': 'XLSX', 'description': 'com abas'}]}]}}
    s = m.rodar('fila', ask)
    caso('fila: AskUserQuestion com gente olhando → calada (vai ao chat)', s is None and not perg.exists(), str(s))
    s = m.rodar('fila', ask, CLAUDE_CODE_SESSION_ATTENDED='0')
    t = perg.read_text(encoding='utf-8') if perg.exists() else ''
    caso('fila: AskUserQuestion largada → nega com "Adiada" e grava P1',
         decisao(s) == 'deny' and 'Adiada' in str(s) and '### P1 · Formato' in t and 'a) CSV' in t, str(s))
    caso('fila: o gancho não responde (sem answers nem updatedInput)', 'answers' not in json.dumps(s)
         and 'updatedInput' not in json.dumps(s))
    s = m.rodar('fila', {'hook_event_name': 'PermissionRequest', 'tool_name': 'Bash',
                         'tool_input': {'command': 'rm -rf build'}}, KIT_LARGADA='1')
    t = perg.read_text(encoding='utf-8')
    caso('fila: PermissionRequest largada → deny sem interromper e grava P2',
         decisao(s) == 'deny' and s['hookSpecificOutput']['decision']['interrupt'] is False and '### P2' in t, str(s))
    caso('fila: P2 entra antes de "## Respondidas"', t.index('### P2') < t.index('## Respondidas'))
    (m.proj / '.claude' / 'largada').write_text('', encoding='utf-8')
    s = m.rodar('fila', ask)
    caso('fila: o arquivo .claude\\largada liga a execução largada', decisao(s) == 'deny', str(s))
    (m.proj / '.claude' / 'largada').unlink()
    s = m.rodar('fila', ask, CLAUDE_CODE_SESSION_ATTENDED='0', CLAUDE_PROJECT_DIR=m.sem)
    caso('fila: projeto sem ESTADO.md → calada', s is None, str(s))


def testar_portao(m: Mundo) -> None:
    for f in (m.local / 'sessoes').glob('*.json') if (m.local / 'sessoes').exists() else []:
        f.unlink()
    m.rodar('abertura', {'hook_event_name': 'SessionStart', 'source': 'startup', 'model': 'claude-opus-5-5'})
    fim = {'hook_event_name': 'Stop', 'stop_hook_active': False,
           'last_assistant_message': 'Resumo.\nSinais de insuficiência do modelo: nenhum'}
    s = m.rodar('portao', {**fim, 'last_assistant_message': 'Feito o passo 2; sigo para o 3.'})
    caso('Stop: sem resumo de fechamento → calado', s is None, str(s))
    s = m.rodar('portao', fim)
    caso('Stop: fase dada como pronta sem ESTADO.md reescrito → bloqueia', decisao(s) == 'block', str(s))
    estado = m.proj / 'docs' / 'ESTADO.md'
    original = estado.read_text(encoding='utf-8')
    estado.write_text(original.replace('a fase F0', 'as fases F0 e F1'), encoding='utf-8')
    s = m.rodar('portao', fim)
    caso('Stop: com ESTADO.md reescrito → deixa fechar', s is None, str(s))
    sess = m.local / 'sessoes' / 'sessao-teste.json'
    d = json.loads(sess.read_text(encoding='utf-8'))
    d['fila'] = 2
    sess.write_text(json.dumps(d), encoding='utf-8')
    perg = m.proj / 'docs' / 'PERGUNTAS.md'
    guardado = perg.read_text(encoding='utf-8')
    perg.unlink()
    s = m.rodar('portao', fim)
    caso('Stop: a sessão enfileirou e o PERGUNTAS.md sumiu → bloqueia', decisao(s) == 'block', str(s))
    perg.write_text(guardado, encoding='utf-8')
    s = m.rodar('portao', fim)
    caso('Stop: ESTADO.md e PERGUNTAS.md gravados → fecha com a fila aberta', s is None, str(s))
    estado.write_text(original, encoding='utf-8')
    d = json.loads(sess.read_text(encoding='utf-8'))
    d.update(estado_hash='outro', fila=0, bloqueios=0)
    d['estado_hash'] = __import__('hashlib').sha1(estado.read_bytes()).hexdigest()
    sess.write_text(json.dumps(d), encoding='utf-8')
    saidas = [m.rodar('portao', {**fim, 'stop_hook_active': True}) for _ in range(9)]
    caso('Stop: bloqueia 8 vezes seguidas e na 9ª deixa fechar com aviso',
         all(decisao(x) == 'block' for x in saidas[:8]) and decisao(saidas[8]) is None
         and 'systemMessage' in (saidas[8] or {}), str(saidas[8]))
    s = m.rodar('portao', fim, CLAUDE_PROJECT_DIR=m.sem)
    caso('Stop: projeto sem ESTADO.md → calado', s is None, str(s))


def testar_abertura(m: Mundo) -> None:
    ab = {'hook_event_name': 'SessionStart', 'source': 'startup'}
    s = m.rodar('abertura', {**ab, 'model': 'claude-opus-5-5'}, CLAUDE_PROJECT_DIR=m.sem)
    caso('abertura: projeto sem ESTADO.md, modelo e esforço certos → calada', s is None, str(s))
    s = m.rodar('abertura', {**ab, 'model': 'claude-sonnet-5'}, CLAUDE_PROJECT_DIR=m.sem)
    caso('abertura: Sonnet 5 → aviso ao usuário (systemMessage)', 'Sonnet 5' in (s or {}).get('systemMessage', ''), str(s))
    s = m.rodar('abertura', {**ab, 'model': {'id': 'claude-opus-5'}}, CLAUDE_PROJECT_DIR=m.sem)
    caso('abertura: Opus 5 (rebaixamento) → aviso', 'Opus 5' in (s or {}).get('systemMessage', ''), str(s))
    s = m.rodar('abertura', {**ab, 'model': 'claude-opus-5-5'}, CLAUDE_PROJECT_DIR=m.sem, CLAUDE_EFFORT='max')
    caso('abertura: esforço max na sessão → aviso', 'max' in (s or {}).get('systemMessage', ''), str(s))
    (m.casa / 'settings.json').write_text(json.dumps({'modelSettings': {'claude-opus-5-5': {'effortLevel': 'xhigh'}}}),
                                          encoding='utf-8')
    s = m.rodar('abertura', {**ab, 'model': 'claude-opus-5-5'}, CLAUDE_PROJECT_DIR=m.sem)
    caso('abertura: xhigh gravado → aviso', 'xhigh' in (s or {}).get('systemMessage', ''), str(s))
    (m.casa / 'settings.json').write_text(json.dumps({}), encoding='utf-8')

    para = m.proj / 'docs' / 'para_proj'
    para.mkdir(exist_ok=True)
    (para / 'INDICE.md').write_text('| Nº | Data | Assunto | Status |\n|---|---|---|---|\n| AT-001 | 01/10 | x | enviado |\n'
                                    '| AT-002 | 02/10 | y | confirmado |\n', encoding='utf-8')
    s = m.rodar('abertura', {**ab, 'model': 'claude-opus-5-5'}, CLAUDE_PROJECT_DIR=m.proj)
    c = ctx(s)
    caso('abertura (ESTADO): estado curto, fila e caixa',
         'Feito:** a fase F0' in c and 'fila: 3 pergunta' in c and 'AT-001' in c and 'AT-002' not in c, c[:400])
    caso('abertura (ESTADO): sem aviso, sem systemMessage', 'systemMessage' not in (s or {}), str(s)[:200])
    caso('abertura (ESTADO): sem o PROXIMO.md fora do /clear', 'Escritas em dado real' not in c)
    s = m.rodar('abertura', {**ab, 'source': 'clear', 'session_id': 'outra', 'model': 'claude-opus-5-5'})
    caso('abertura no /clear: injeta o PROXIMO.md', 'Escritas em dado real aprovadas' in ctx(s), ctx(s)[:200])

    fluxo = m.kit / 'config' / 'fluxo.json'
    base = (dt.date.today() - dt.timedelta(days=20)).isoformat()
    fluxo.write_text(json.dumps({'pcs': {'PCTESTE': 'notebook'}, 'balanco_desde': base}), encoding='utf-8')
    s = m.rodar('abertura', {**ab, 'model': 'claude-opus-5-5'}, CLAUDE_PROJECT_DIR=m.sem)
    caso('abertura: balanço vencido (20 dias) → uma linha com a janela da raiz',
         '20 dias' in (s or {}).get('systemMessage', '') and 'C:\\CLAUDE-PROJETOS' in (s or {}).get('systemMessage', ''),
         str(s))
    (m.kit / 'metricas' / 'balancos' / f'{dt.date.today().isoformat()}.md').write_text('x', encoding='utf-8')
    s = m.rodar('abertura', {**ab, 'model': 'claude-opus-5-5'}, CLAUDE_PROJECT_DIR=m.sem)
    caso('abertura: balanço de hoje → calada', s is None, str(s))


def testar_statusline(m: Mundo) -> None:
    ent = {'model': {'id': 'claude-opus-5-5', 'display_name': 'Opus 5.5'}, 'effort': {'level': 'medium'},
           'context_window': {'used_percentage': 34.4},
           'rate_limits': {'five_hour': {'used_percentage': 12, 'resets_at': 1760000000},
                           'seven_day': {'used_percentage': 40.2, 'resets_at': 1760500000}}}

    def rodar(e):
        r = subprocess.run([sys.executable, str(GANCHOS / 'statusline.py')], input=json.dumps(e).encode('utf-8'),
                           capture_output=True, env=m.env(), timeout=30)
        return r.stdout.decode('utf-8', 'replace')
    out = rodar(ent)
    caso('statusline: modelo, esforço, contexto, 5 h e semanal', out == 'Opus 5.5 · medium · ctx 34% · 5h 12% · sem 40%', out)
    rodar(ent)
    arq = m.local / 'limites.jsonl'
    n1 = len(arq.read_text(encoding='utf-8').splitlines()) if arq.exists() else 0
    ent['rate_limits']['seven_day']['used_percentage'] = 41
    rodar(ent)
    n2 = len(arq.read_text(encoding='utf-8').splitlines()) if arq.exists() else 0
    caso('statusline: grava o % em limites.jsonl só quando muda', (n1, n2) == (1, 2), f'{n1}, {n2}')
    out = rodar({'model': {'display_name': 'Haiku 4.5'}})
    caso('statusline: sem rate_limits nem esforço (1ª resposta ainda não veio)', out == 'Haiku 4.5', out)


def testar_so_com_dir(m: Mundo) -> None:
    def b(cmd):
        return m.rodar('so_com_dir', {'hook_event_name': 'PreToolUse', 'tool_name': 'Bash', 'tool_input': {'command': cmd}})
    caso('session-report: analyze-sessions sem --dir → nega',
         decisao(b('node C:/x/analyze-sessions.mjs --json --since 7d > /tmp/r.json')) == 'deny')
    caso('session-report: com --dir → passa', b('node C:/x/analyze-sessions.mjs --dir C:/u/.claude/projects/p --json') is None)
    caso('session-report: outro comando → passa', b('git status') is None)


def testar_semana() -> None:
    sys.path.insert(0, str(GANCHOS))
    import semana
    with tempfile.TemporaryDirectory() as t:
        k = Path(t)
        (k / 'metricas').mkdir()
        (k / 'metricas' / 'uso-semanal.csv').write_text('semana_inicio,pc\n2026-09-29,notebook\n2026-09-22,desktop\n',
                                                        encoding='utf-8')
        p = semana.semanas_pendentes
        caso('semana: 09/10 (sexta) → nenhuma pendente (06/10 fecha em 13/10)', p(k, 'notebook', dt.date(2026, 10, 9)) == [])
        caso('semana: 13/10 → a de 06/10', p(k, 'notebook', dt.date(2026, 10, 13)) == ['2026-10-06'])
        caso('semana: 21/10 → 06/10 e 13/10', p(k, 'notebook', dt.date(2026, 10, 21)) == ['2026-10-06', '2026-10-13'])
        caso('semana: cada PC pela sua linha', p(k, 'desktop', dt.date(2026, 10, 9)) == ['2026-09-29'])
        caso('semana: PC sem linha → só a última fechada', p(k, 'outro', dt.date(2026, 10, 9)) == ['2026-09-29'])


def main() -> int:
    t0 = time.perf_counter()
    raiz = Path(tempfile.mkdtemp(prefix='ganchos-'))
    try:
        m = Mundo(raiz)
        testar_hooks_json()
        testar_modelo(m)
        testar_despacho(m)
        testar_guarda(m)
        testar_fila(m)
        testar_portao(m)
        testar_abertura(m)
        testar_statusline(m)
        testar_so_com_dir(m)
        testar_semana()
    finally:
        shutil.rmtree(raiz, ignore_errors=True)
    falhas = [r for r in resultados if not r[1]]
    for nome, ok, det in resultados:
        if VERBOSO or not ok:
            print(f'{"ok   " if ok else "FALHA"} {nome}' + (f'\n      {det[:500]}' if det and not ok else ''))
    print(f'\ntestar_ganchos: {len(resultados) - len(falhas)} de {len(resultados)} verdes '
          f'({time.perf_counter() - t0:.1f} s)')
    return 1 if falhas else 0


if __name__ == '__main__':
    sys.exit(main())
