# -*- coding: utf-8 -*-
r"""O que os ganchos do nucleo dividem: entrada, projeto, estado local, saída.

Cada gancho é um script deste diretório chamado pelo plugins\nucleo\hooks\hooks.json com
python "${CLAUDE_PLUGIN_ROOT}/ganchos/<gancho>.py". Todos seguem a mesma forma:
  - rodar(entrada, amb) -> dict | None   o trabalho, sem efeito no stdout (os testes chamam direto);
  - main()                              lê o JSON do stdin, imprime o dict como JSON, sai sempre com 0.
Um gancho nunca derruba a sessão: erro vira silêncio (ou uma linha "não consegui ler X" na abertura).

As duas camadas (plano, Ficha item 4): a 1ª vale em todo projeto; a 2ª só onde existe docs\ESTADO.md
(tem_estado). Nos projetos ainda não migrados, os ganchos antigos deles continuam.

O estado local (fora do git, por PC) mora em ~\.claude\kit-local\ (KIT_LOCAL troca, nos testes):
  limites.jsonl         o % de 5 h e o semanal, gravados pela statusline (o medir_semana.py lê)
  abertura.json         a hora do último git pull do kit e da última medição lançada
  sessoes\<id>.json     por sessão: o hash do ESTADO.md ao abrir, perguntas enfileiradas, bloqueios do portão
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

KIT = Path(__file__).resolve().parents[3]          # ganchos -> nucleo -> plugins -> claude-kit


@dataclass
class Amb:
    """O ambiente de um gancho. Os testes trocam os caminhos e desligam rede, processo e relógio."""
    kit: Path = field(default_factory=lambda: Path(os.environ.get('KIT_RAIZ') or KIT))
    local: Path = field(default_factory=lambda: Path(os.environ.get('KIT_LOCAL') or Path.home() / '.claude' / 'kit-local'))
    casa: Path = field(default_factory=lambda: Path(os.environ.get('KIT_CASA') or Path.home() / '.claude'))
    env: dict = field(default_factory=lambda: dict(os.environ))
    agora: float = field(default_factory=time.time)

    @property
    def sem_rede(self) -> bool:
        """KIT_SEM_REDE=1: sem git pull, sem processo em segundo plano, sem ler a linha de comando do pai."""
        return self.env.get('KIT_SEM_REDE') == '1'


def ler_entrada() -> dict:
    try:
        bruto = sys.stdin.buffer.read().decode('utf-8', 'replace')
        d = json.loads(bruto) if bruto.strip() else {}
        return d if isinstance(d, dict) else {}
    except Exception:
        return {}


def projeto_de(entrada: dict, amb: Amb) -> Path | None:
    p = amb.env.get('CLAUDE_PROJECT_DIR') or entrada.get('cwd')
    return Path(p) if p else None


def tem_estado(projeto: Path | None) -> bool:
    """A 2ª camada dos ganchos só age onde o projeto já migrou para o fluxo novo."""
    return bool(projeto) and (projeto / 'docs' / 'ESTADO.md').is_file()


def largada(projeto: Path | None, amb: Amb) -> bool:
    r"""Execução largada (skill orquestrar §4): ninguém olha a sessão.

    Sinais: a sessão não tem gente (CLAUDE_CODE_SESSION_ATTENDED=0: -p e --bg; visto em 09/10, 2.1.291, não
    documentado); KIT_LARGADA=1 no ambiente de quem lançou; ou o arquivo .claude\largada no projeto (a fase o cria
    ao ser largada numa aba interativa e o apaga ao fechar).
    """
    if amb.env.get('KIT_LARGADA') == '1' or amb.env.get('CLAUDE_CODE_SESSION_ATTENDED') == '0':
        return True
    return bool(projeto) and (projeto / '.claude' / 'largada').exists()


def ler_texto(p: Path, limite: int | None = None) -> str | None:
    try:
        with open(p, encoding='utf-8', errors='replace') as f:
            return f.read(limite) if limite else f.read()
    except Exception:
        return None


def ler_json(p: Path) -> dict:
    try:
        d = json.loads(p.read_text(encoding='utf-8-sig'))
        return d if isinstance(d, dict) else {}
    except Exception:
        return {}


def gravar_json(p: Path, d: dict) -> None:
    try:
        p.parent.mkdir(parents=True, exist_ok=True)
        tmp = p.with_suffix(p.suffix + '.tmp')
        tmp.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding='utf-8')
        os.replace(tmp, p)
    except Exception:
        pass


def hash_de(p: Path) -> str | None:
    try:
        return hashlib.sha1(p.read_bytes()).hexdigest()
    except Exception:
        return None


def _id_seguro(sessao: str | None) -> str | None:
    return sessao if sessao and re.fullmatch(r'[A-Za-z0-9_\-]{1,80}', sessao) else None


def estado_sessao(amb: Amb, sessao: str | None) -> dict:
    s = _id_seguro(sessao)
    return ler_json(amb.local / 'sessoes' / f'{s}.json') if s else {}


def gravar_sessao(amb: Amb, sessao: str | None, d: dict) -> None:
    s = _id_seguro(sessao)
    if s:
        gravar_json(amb.local / 'sessoes' / f'{s}.json', d)


def pc(amb: Amb) -> str:
    r"""O rótulo deste PC (coluna pc do CSV, série da caixa): config\fluxo.json "pcs", ou o nome do computador."""
    nome = amb.env.get('COMPUTERNAME', '')
    rotulo = (ler_json(amb.kit / 'config' / 'fluxo.json').get('pcs') or {}).get(nome)
    return rotulo or re.sub(r'[^a-z0-9_.\-]', '', nome.lower()) or 'pc'


def modelo_de(entrada: dict) -> str | None:
    m = entrada.get('model')
    if isinstance(m, dict):
        m = m.get('id')
    return m if isinstance(m, str) and m else None


SONNET_5 = re.compile(r'claude-sonnet-5(\[[^\]]*\])?')
OPUS_5 = re.compile(r'claude-opus-5(\[[^\]]*\])?')


def emitir(saida: dict | None) -> None:
    if saida:
        sys.stdout.buffer.write(json.dumps(saida, ensure_ascii=False).encode('utf-8'))


def principal(rodar) -> None:
    """O main de todo gancho: entrada → rodar → JSON; sempre sai com 0."""
    try:
        emitir(rodar(ler_entrada(), Amb()))
    except Exception:
        pass
    sys.exit(0)


def contexto(evento: str, texto: str, aviso: str | None = None) -> dict:
    """additionalContext (para o Claude) e, se houver, systemMessage (aparece ao usuário)."""
    d: dict = {'hookSpecificOutput': {'hookEventName': evento, 'additionalContext': texto[:9500]}}
    if aviso:
        d['systemMessage'] = aviso
    return d


def negar_ferramenta(motivo: str) -> dict:
    return {'hookSpecificOutput': {'hookEventName': 'PreToolUse', 'permissionDecision': 'deny',
                                   'permissionDecisionReason': motivo}}
