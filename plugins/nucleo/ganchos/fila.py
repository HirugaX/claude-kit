# -*- coding: utf-8 -*-
r"""A fila (Q35, Q36, Q44): na execução largada, a dúvida vai para docs\PERGUNTAS.md e a fase segue.

Dois eventos, só onde existe docs\ESTADO.md e só na execução largada (comum.largada); fora disso, a pergunta vai ao
chat como sempre (skill orquestrar §4):
  - PreToolUse em AskUserQuestion: grava cada pergunta, com as opções, e NEGA a ferramenta com o motivo "adiada".
    Só adia, nunca escolhe: o gancho não devolve answers, e o Claude não recebe resposta nenhuma.
  - PermissionRequest: grava o pedido (a ferramenta e um resumo de até 200 caracteres) e nega com mensagem, sem
    interromper. Não dispara em -p nem em --bg (hooks#permissionrequest): vale na sessão interativa largada.
"""
from __future__ import annotations

import re
import time
from pathlib import Path

from comum import Amb, estado_sessao, gravar_sessao, largada, negar_ferramenta, principal, projeto_de, tem_estado

CABECA = ('# Perguntas — {projeto}\n\n'
          '<!-- A fila (Q35; skills orquestrar e fechar-janela; modelo em plugins\\nucleo\\skills\\fechar-janela\\'
          'modelos\\PERGUNTAS.md). Nenhum nome de paciente; o pseudônimo, só nos desosp-. -->\n\n'
          '## Abertas\n\n## Respondidas\n')


def _curto(s, n: int) -> str:
    s = re.sub(r'\s+', ' ', str(s or '')).strip()
    return s if len(s) <= n else s[:n - 1] + '…'


def enfileirar(projeto: Path, entradas: list[dict], amb: Amb) -> list[str]:
    """Acrescenta as perguntas em "## Abertas" e devolve os números (P7, P8...)."""
    arq = projeto / 'docs' / 'PERGUNTAS.md'
    texto = arq.read_text(encoding='utf-8') if arq.is_file() else CABECA.format(projeto=projeto.name)
    n = max((int(x) for x in re.findall(r'^### P(\d+)\b', texto, re.M)), default=0)
    data = time.strftime('%d/%m', time.localtime(amb.agora))
    blocos, nums = [], []
    for e in entradas:
        n += 1
        nums.append(f'P{n}')
        ops = ''.join(f'\n  - {chr(97 + i)}) {_curto(o.get("label"), 80)}'
                      + (f' — {_curto(o.get("description"), 160)}' if o.get('description') else '')
                      for i, o in enumerate(e.get('opcoes') or []) if isinstance(o, dict))
        blocos.append(
            f'### P{n} · {_curto(e["titulo"], 70)} — {data}, adiada pelo gancho (execução largada)\n\n'
            f'- **O problema:** {e["problema"]}\n'
            f'- **A pergunta:** {_curto(e["pergunta"], 400)}\n'
            f'- **As opções:**{ops or " (nenhuma listada)"}\n'
            f'- **Recomendação:** (a fase completa ao fechar)\n'
            f'- **O que depende dela:** (a fase completa ao fechar)\n')
    novo = '\n'.join(blocos) + '\n'
    if '## Respondidas' in texto:
        texto = texto.replace('## Respondidas', novo + '## Respondidas', 1)
    elif '## Abertas' in texto:
        texto = texto.rstrip('\n') + '\n\n' + novo
    else:
        texto = texto.rstrip('\n') + '\n\n## Abertas\n\n' + novo
    arq.parent.mkdir(parents=True, exist_ok=True)
    arq.write_text(texto, encoding='utf-8')
    return nums


def _contar(amb: Amb, sessao, nums: list[str]) -> None:
    s = estado_sessao(amb, sessao)
    s['fila'] = s.get('fila', 0) + len(nums)
    gravar_sessao(amb, sessao, s)


def _resumo_ferramenta(nome: str, ti: dict) -> str:
    for k in ('command', 'file_path', 'notebook_path', 'url', 'path', 'pattern'):
        if ti.get(k):
            return f'{nome}: {_curto(ti[k], 200)}'
    return f'{nome}: {_curto(", ".join(sorted(ti)), 120)}'


def rodar(entrada: dict, amb: Amb) -> dict | None:
    projeto = projeto_de(entrada, amb)
    if not tem_estado(projeto) or not largada(projeto, amb):
        return None
    evento = entrada.get('hook_event_name')
    sessao = entrada.get('session_id')
    ti = entrada.get('tool_input') or {}

    if evento == 'PreToolUse' and entrada.get('tool_name') == 'AskUserQuestion':
        qs = [q for q in ti.get('questions') or [] if isinstance(q, dict)]
        if not qs:
            return None
        nums = enfileirar(projeto, [{'titulo': q.get('header') or q.get('question') or 'pergunta',
                                     'problema': 'a fase perguntou com a execução largada (AskUserQuestion).',
                                     'pergunta': q.get('question') or '', 'opcoes': q.get('options')} for q in qs], amb)
        _contar(amb, sessao, nums)
        return negar_ferramenta(
            f'Adiada: ninguém responde agora (execução largada). Gravei em docs\\PERGUNTAS.md como {", ".join(nums)}. '
            'Não escolha por ele: siga com o que não depende disso e, ao fechar, complete a recomendação e o que '
            'depende dela (skill orquestrar §4).')

    if evento == 'PermissionRequest':
        nome = str(entrada.get('tool_name') or 'ferramenta')
        nums = enfileirar(projeto, [{'titulo': f'permissão: {nome}',
                                     'problema': 'a fase pediu uma permissão com a execução largada.',
                                     'pergunta': f'Liberar {_resumo_ferramenta(nome, ti)}?',
                                     'opcoes': [{'label': 'liberar'}, {'label': 'não liberar'}]}], amb)
        _contar(amb, sessao, nums)
        return {'hookSpecificOutput': {'hookEventName': 'PermissionRequest', 'decision': {
            'behavior': 'deny', 'interrupt': False,
            'message': (f'Permissão adiada (execução largada): gravei em docs\\PERGUNTAS.md como {nums[0]}. Não tente '
                        'o mesmo efeito por outro caminho; siga com o que não depende disto.')}}}
    return None


if __name__ == '__main__':
    principal(rodar)
