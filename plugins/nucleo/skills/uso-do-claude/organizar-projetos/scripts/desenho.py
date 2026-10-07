r"""Os ícones do sistema de cores: os quadros PNG (a fonte do desenho, no kit) e o .ico montado em cada PC.

    python desenho.py montar <pasta_destino>          # os .ico de todos os verbos e marcas, nas cores do mapa
    python desenho.py previa <arquivo.html>           # a prévia: 16, 20, 32, 48 e 256 px, fundo claro e escuro
    python desenho.py amostra <pasta>                 # pastas de amostra com desktop.ini, para ver no Explorador
    python desenho.py quadros <pasta_do_pacote_ettore> # (uma vez) refaz icones\ a partir dos .ico do Ettore

Por que montar em cada PC: desde junho de 2026 o Windows ignora desktop.ini com marca da web; .ico baixado
pronto (zip, download) pode vir marcado. Os quadros PNG viajam no kit; o .ico nasce no PC.

O estilo é o do pacote do Ettore (05/10): pasta lisa, a aba ~23% mais escura, emblema branco; de 16 a 24 px
um símbolo simplificado. Recolorir é exato nesse estilo: cada pixel é uma mistura de branco com a cor da
frente (a aba é a mesma cor, mais escura), e a mistura se refaz com a cor nova.

Precisa de Pillow. O gancho não importa este arquivo.
"""
from __future__ import annotations

import argparse
import base64
import io
import json
import struct
import sys
from collections import Counter
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

AQUI = Path(__file__).resolve().parent
MODULO = AQUI.parent
QUADROS = MODULO / 'icones'
TAMANHOS = (16, 20, 24, 32, 40, 48, 64, 128, 256)
PEQUENO = 24          # até aqui, o símbolo simplificado

# id do ícone -> (arquivo do pacote do Ettore, o que fazer). O que fazer: None (o desenho dele como está);
# "chip" (a mão dele, com um chip no lugar do robozinho); um emblema desenhado sobre a pasta dele limpa
# ("cadeado", "interrogacao", "braco-robo", "cadeado-circuito", "robo-pergunta"); "+selo" no fim põe o envelope
# do correio dele. É a versão 4, aprovada pelo Ettore em 05/10 à noite ("aprovo tudo"): o pacote dele (versão 3)
# e, das referências dele (prototipos-icones\referencia_icones), o braço de robô, o chip, o cadeado no circuito e o
# robô com "?", redesenhados no mesmo estilo. As cores vêm do mapa.json.
ORIGEM = {
    'eu-alimento': ('eu-alimento.ico', None),
    'eu-forneco-fontes': ('eu-forneco-fontes.ico', 'chip'),
    'eu-leio': ('eu-leio.ico', None),
    'trabalhamos-juntos': ('trabalhamos-juntos-cabeca.ico', None),
    'nao-toco': ('nao-toco.ico', 'braco-robo'),
    'nao-toco-correio': ('nao-toco.ico', 'braco-robo+selo'),
    'projeto-ia': ('trabalhamos-juntos-engrenagem.ico', None),
    'dado-real': ('nao-toco.ico', 'cadeado-circuito'),
    'provisoria': ('nao-toco.ico', 'robo-pergunta'),
}


# ---------------------------------------------------------------- cor

def hex_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rgb_hex(c) -> str:
    return '#{:02X}{:02X}{:02X}'.format(*c[:3])


def cor_da_frente(img: Image.Image) -> tuple[int, int, int]:
    """A cor mais comum entre os pixels opacos (a frente da pasta)."""
    c = Counter(p[:3] for p in img.convert('RGBA').get_flattened_data() if p[3] == 255 and p[:3] != (255, 255, 255))
    return c.most_common(1)[0][0]


def _decompor(p, F):
    """p ≈ a·branco + b·F (mínimos quadrados): a = quanto de branco, b = quanto da cor (b < 1 na aba)."""
    W = (255, 255, 255)
    dot = lambda u, v: u[0] * v[0] + u[1] * v[1] + u[2] * v[2]
    ww, wf, ff = dot(W, W), dot(W, F), dot(F, F)
    det = ww * ff - wf * wf or 1
    pw, pf = dot(p, W), dot(p, F)
    a = (pw * ff - pf * wf) / det
    b = (pf * ww - pw * wf) / det
    return max(a, 0.0), max(b, 0.0)


def recolorir(img: Image.Image, de, para) -> Image.Image:
    """Troca a cor da pasta preservando a aba mais escura, o branco e o antisserrilhado."""
    de, para = hex_rgb(de) if isinstance(de, str) else de, hex_rgb(para) if isinstance(para, str) else para
    if tuple(de) == tuple(para):
        return img.copy()
    out = img.convert('RGBA').copy()
    px = out.load()
    for y in range(out.height):
        for x in range(out.width):
            r, g, b_, al = px[x, y]
            if not al:
                continue
            a, b = _decompor((r, g, b_), de)
            px[x, y] = tuple(min(255, max(0, round(a * 255 + b * c))) for c in para) + (al,)
    return out


def apagar_emblema(img: Image.Image, cor) -> Image.Image:
    """A pasta sem o emblema: todo branco da frente vira a cor da frente."""
    F = hex_rgb(cor) if isinstance(cor, str) else cor
    out = img.convert('RGBA').copy()
    px = out.load()
    for y in range(out.height):
        for x in range(out.width):
            r, g, b_, al = px[x, y]
            if al:
                a, b = _decompor((r, g, b_), F)
                s = min(1.0, a + b)
                px[x, y] = tuple(round(s * c) for c in F) + (al,)
    return out


def caixa_da_frente(img: Image.Image, cor) -> tuple[int, int, int, int]:
    F = hex_rgb(cor) if isinstance(cor, str) else tuple(cor)
    px = img.load()
    pts = [(x, y) for y in range(img.height) for x in range(img.width) if px[x, y][3] == 255 and px[x, y][:3] == F]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return min(xs), min(ys), max(xs) + 1, max(ys) + 1


# ---------------------------------------------------------------- os dois emblemas novos

def _fonte(tam: int):
    for nome in ('segoeuib.ttf', 'arialbd.ttf', 'DejaVuSans-Bold.ttf'):
        try:
            return ImageFont.truetype(nome, tam)
        except OSError:
            continue
    return ImageFont.load_default()


def _traco(d, u, pontos, w, ponta=True):
    """Linha grossa por vários pontos, com as juntas e (se `ponta`) as pontas arredondadas."""
    pts = [(u(x), u(y)) for x, y in pontos]
    d.line(pts, fill=255, width=max(1, u(w)))
    r = u(w) / 2
    for i, (x, y) in enumerate(pts):
        if ponta or 0 < i < len(pts) - 1:
            d.ellipse([x - r, y - r, x + r, y + r], fill=255)


def _bola(d, u, x, y, r, cor=255):
    d.ellipse([u(x - r), u(y - r), u(x + r), u(y + r)], fill=cor)


def _nivel(s: int) -> str:
    """p = 16-24 px (símbolo simplificado), m = 32-64 px, g = 128-256 px."""
    return 'p' if s <= PEQUENO else ('m' if s <= 64 else 'g')


def _mascara(tipo: str, lado: int, pequeno, nivel: str | None = None) -> Image.Image:
    """O emblema em branco numa máscara quadrada de `lado` px (desenhada a 8× e reduzida).

    Os desenhos novos de 05/10 (braço de robô, chip, cadeado no circuito, robô com "?") são próprios,
    inspirados nas referências do Ettore (claude-kit: prototipos-icones\\referencia_icones), sem decalque."""
    nivel = nivel or ('p' if pequeno else 'g')
    pequeno = nivel == 'p'
    k = 8
    L = lado * k
    m = Image.new('L', (L, L), 0)
    d = ImageDraw.Draw(m)
    u = lambda v: round(v * L)
    if tipo == 'braco-robo':
        g = nivel == 'g'
        bw, aw, jw = (0.16, 0.14, 0.11) if pequeno else ((0.13, 0.11, 0.095) if not g else (0.12, 0.10, 0.09))
        d.rounded_rectangle([u(0.12), u(0.86), u(0.66), u(0.98)], radius=u(0.03), fill=255)       # a base
        d.polygon([(u(0.20), u(0.87)), (u(0.58), u(0.87)), (u(0.48), u(0.74)), (u(0.30), u(0.74))], fill=255)
        _traco(d, u, [(0.39, 0.72), (0.27, 0.36)], bw)                                           # o braço
        _traco(d, u, [(0.27, 0.34), (0.68, 0.22)], aw)                                           # o antebraço
        _bola(d, u, 0.39, 0.72, jw)                                                              # as juntas
        _bola(d, u, 0.27, 0.34, jw)
        _bola(d, u, 0.70, 0.22, jw * 0.72)
        d.rounded_rectangle([u(0.62), u(0.25), u(0.84), u(0.34)], radius=u(0.02), fill=255)      # a garra
        pw = 0.07 if pequeno else 0.05
        if pequeno:
            _traco(d, u, [(0.65, 0.33), (0.65, 0.48)], pw)
            _traco(d, u, [(0.81, 0.33), (0.81, 0.48)], pw)
        else:
            _traco(d, u, [(0.65, 0.33), (0.60, 0.42), (0.65, 0.51)], pw)
            _traco(d, u, [(0.81, 0.33), (0.86, 0.42), (0.81, 0.51)], pw)
        if g:                                                                                    # os eixos
            for x, y in ((0.39, 0.72), (0.27, 0.34)):
                _bola(d, u, x, y, 0.035, 0)
    elif tipo == 'chip':
        d.rounded_rectangle([u(0.22), u(0.22), u(0.78), u(0.78)], radius=u(0.06), fill=255)
        pinos = (0.34, 0.50, 0.66) if nivel == 'g' else (0.38, 0.62)
        pl, pw = 0.13, (0.075 if nivel == 'g' else 0.11)
        for c in pinos:
            d.rectangle([u(c - pw / 2), u(0.22 - pl), u(c + pw / 2), u(0.22)], fill=255)
            d.rectangle([u(c - pw / 2), u(0.78), u(c + pw / 2), u(0.78 + pl)], fill=255)
            d.rectangle([u(0.22 - pl), u(c - pw / 2), u(0.22), u(c + pw / 2)], fill=255)
            d.rectangle([u(0.78), u(c - pw / 2), u(0.78 + pl), u(c + pw / 2)], fill=255)
        if nivel == 'g':
            d.rectangle([u(0.36), u(0.36), u(0.64), u(0.64)], fill=0)
            d.rectangle([u(0.43), u(0.43), u(0.57), u(0.57)], fill=255)
    elif tipo == 'cadeado-circuito':
        if pequeno:
            return _mascara('cadeado', lado, True, 'p')
        g = nivel == 'g'
        esp = 0.075
        d.ellipse([u(0.36), u(0.12), u(0.64), u(0.48)], fill=255)                                # a alça
        d.ellipse([u(0.36 + esp), u(0.12 + esp), u(0.64 - esp), u(0.48 - esp)], fill=0)
        d.rectangle([u(0.30), u(0.30), u(0.70), u(0.48)], fill=0)
        d.rectangle([u(0.36), u(0.30), u(0.36 + esp), u(0.44)], fill=255)
        d.rectangle([u(0.64 - esp), u(0.30), u(0.64), u(0.44)], fill=255)
        d.rounded_rectangle([u(0.29), u(0.41), u(0.71), u(0.80)], radius=u(0.05), fill=255)      # o corpo
        _bola(d, u, 0.50, 0.565, 0.05, 0)                                                        # a fechadura
        d.rectangle([u(0.48), u(0.58), u(0.52), u(0.70)], fill=0)
        tw, rb = (0.035, 0.05) if g else (0.055, 0.07)                                           # o circuito
        trilhas = [[(0.29, 0.70), (0.08, 0.70)], [(0.71, 0.70), (0.92, 0.70)]]
        if g:
            trilhas += [[(0.29, 0.52), (0.18, 0.52), (0.10, 0.42)], [(0.71, 0.52), (0.82, 0.52), (0.90, 0.42)],
                        [(0.50, 0.80), (0.50, 0.93)]]
        for t in trilhas:
            _traco(d, u, t, tw, ponta=False)
            _bola(d, u, t[-1][0], t[-1][1], rb)
    elif tipo == 'robo-pergunta':
        if pequeno:
            return _mascara('interrogacao', lado, True, 'p')
        _traco(d, u, [(0.50, 0.30), (0.50, 0.15)], 0.05)                                         # a antena
        _bola(d, u, 0.50, 0.12, 0.065)
        d.rounded_rectangle([u(0.18), u(0.28), u(0.82), u(0.92)], radius=u(0.14), fill=255)      # a cabeça
        d.rounded_rectangle([u(0.07), u(0.50), u(0.19), u(0.72)], radius=u(0.03), fill=255)      # as orelhas
        d.rounded_rectangle([u(0.81), u(0.50), u(0.93), u(0.72)], radius=u(0.03), fill=255)
        f = _fonte(round(L * 0.52))                                                              # o "?" no rosto
        x0, y0, x1, y1 = d.textbbox((0, 0), '?', font=f)
        d.text((L * 0.5 - (x1 - x0) / 2 - x0, L * 0.60 - (y1 - y0) / 2 - y0), '?', font=f, fill=0)
    elif tipo == 'cadeado':
        esp = 0.13 if pequeno else 0.105           # espessura da alça
        # a alça: meio anel por cima e as duas pernas
        d.ellipse([u(0.24), u(0.06), u(0.76), u(0.58)], fill=255)
        d.ellipse([u(0.24 + esp), u(0.06 + esp), u(0.76 - esp), u(0.58 - esp)], fill=0)
        d.rectangle([u(0.0), u(0.32), u(1.0), u(0.58)], fill=0)
        d.rectangle([u(0.24), u(0.32), u(0.24 + esp), u(0.50)], fill=255)
        d.rectangle([u(0.76 - esp), u(0.32), u(0.76), u(0.50)], fill=255)
        # o corpo
        d.rounded_rectangle([u(0.14), u(0.46), u(0.86), u(0.98)], radius=u(0.07), fill=255)
        if not pequeno:                              # o buraco da chave
            d.ellipse([u(0.43), u(0.60), u(0.57), u(0.74)], fill=0)
            d.rectangle([u(0.475), u(0.68), u(0.525), u(0.86)], fill=0)
    elif tipo == 'interrogacao':
        f = _fonte(round(L * (1.18 if pequeno else 1.10)))
        x0, y0, x1, y1 = d.textbbox((0, 0), '?', font=f)
        d.text(((L - (x1 - x0)) / 2 - x0, (L - (y1 - y0)) / 2 - y0), '?', font=f, fill=255)
    else:
        raise ValueError(tipo)
    return m.resize((lado, lado), Image.LANCZOS)


TAMANHO_DO_EMBLEMA = {'cadeado-circuito': 0.82, 'braco-robo': 0.78, 'robo-pergunta': 0.74}   # × a altura da frente


def com_emblema(base: Image.Image, cor_frente, tipo: str) -> Image.Image:
    """A pasta lisa (já sem emblema) com o emblema branco centrado na frente."""
    s = base.width
    x0, y0, x1, y1 = caixa_da_frente(base, cor_frente)
    nivel = _nivel(s)
    fator = 0.86 if nivel == 'p' else TAMANHO_DO_EMBLEMA.get(tipo, 0.70)
    lado = round((y1 - y0) * fator)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    m = _mascara(tipo, lado, nivel == 'p', nivel)
    branco = Image.new('RGBA', (lado, lado), (255, 255, 255, 255))
    branco.putalpha(m)
    out = base.copy()
    out.alpha_composite(branco, (round(cx - lado / 2), round(cy - lado / 2)))
    return out


def _brancos(img: Image.Image, cor, limiar=0.4) -> set[tuple[int, int]]:
    F = hex_rgb(cor) if isinstance(cor, str) else tuple(cor)
    px = img.load()
    out = set()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = px[x, y]
            if a > 128 and _decompor((r, g, b), F)[0] >= limiar:
                out.add((x, y))
    return out


def _componentes(pontos: set) -> list[set]:
    resto, out = set(pontos), []
    while resto:
        semente = resto.pop()
        comp, pilha = {semente}, [semente]
        while pilha:
            x, y = pilha.pop()
            for v in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if v in resto:
                    resto.remove(v)
                    comp.add(v)
                    pilha.append(v)
        out.append(comp)
    return out


def trocar_por_chip(quadros: dict[int, Image.Image], cor_frente) -> dict[int, Image.Image]:
    """O "Eu forneço fontes" do Ettore com um chip no lugar do robozinho: a mão dele fica, o robô sai.

    A separação se faz uma vez, em 256 px, onde o desenho é nítido: a mão é o maior pedaço branco (o robô, as
    orelhas e as duas perninhas são pedaços soltos). Nos tamanhos de 32 a 128, a área da mão de 256 reduzida diz
    que pixels dele ficam (os da mão ficam exatamente como ele desenhou) e o resto volta a ser pasta. O chip se
    desenha em cada tamanho no lugar do robô. De 16 a 24 px o desenho dele já é um quadradinho sobre a mão (lê
    como chip) e fica como está."""
    F = hex_rgb(cor_frente) if isinstance(cor_frente, str) else tuple(cor_frente)
    g = quadros[256]
    comps = sorted(_componentes(_brancos(g, F, 0.6)), key=len, reverse=True)
    mao = comps[0]
    robo = [p for c in comps[1:] for p in c]
    rx0, rx1 = min(x for x, _ in robo), max(x for x, _ in robo)
    ry0, ry1 = min(y for _, y in robo), max(y for _, y in robo)
    cx = (rx0 + rx1) / 2
    meio = [y for x, y in mao if abs(x - cx) <= (rx1 - rx0) / 2]
    base = (min(meio) if meio else ry1) - 4                                    # 4 px de folga sobre a mão
    lado = min(round((base - ry0) * 1.08), round((rx1 - rx0) * 1.15))
    # a área da mão em 256, com a borda de antisserrilhado dela
    area = Image.new('L', (256, 256), 0)
    pa = area.load()
    for x, y in mao:
        for dx in (-2, -1, 0, 1, 2):
            for dy in (-2, -1, 0, 1, 2):
                if 0 <= x + dx < 256 and 0 <= y + dy < 256:
                    pa[x + dx, y + dy] = 255
    cx0, cy0, cx1, cy1 = caixa_da_frente(apagar_emblema(g, F), F)
    out = {}
    for s, im in quadros.items():
        if s <= PEQUENO:
            out[s] = im.copy()
            continue
        limpa = apagar_emblema(im, F)
        fx0, fy0, fx1, fy1 = caixa_da_frente(limpa, F)
        ex, ey = (fx1 - fx0) / (cx1 - cx0), (fy1 - fy0) / (cy1 - cy0)
        if s == 256:
            area_s = area
        else:
            corte = area.crop((cx0, cy0, cx1, cy1)).resize((fx1 - fx0, fy1 - fy0), Image.LANCZOS)
            area_s = Image.new('L', (s, s), 0)
            area_s.paste(corte, (fx0, fy0))
        pi, pl, pm = im.load(), limpa.load(), area_s.load()
        for y in range(s):
            for x in range(s):
                if pm[x, y] >= 90:                                             # da mão: o pixel dele fica
                    pl[x, y] = pi[x, y]
        lado_s = max(5, round(lado * ex))
        m = _mascara('chip', lado_s, False, _nivel(s))
        branco = Image.new('RGBA', (lado_s, lado_s), (255, 255, 255, 255))
        branco.putalpha(m)
        bx = fx0 + (cx - cx0) * ex
        by = fy0 + (base - cy0) * ey
        limpa.alpha_composite(branco, (round(bx - lado_s / 2), round(by - lado_s)))
        out[s] = limpa
    return out


def com_selo(img: Image.Image, correio: Image.Image, sem_selo: Image.Image) -> Image.Image:
    """Põe o selo do envelope do "Não toco (correio)" do Ettore (canto de baixo, à direita; a partir de 48 px)."""
    s = img.width
    out = img.copy()
    pc, ps, po = correio.load(), sem_selo.load(), out.load()
    for y in range(s // 2, s):
        for x in range(s // 2, s):
            if pc[x, y] != ps[x, y]:
                po[x, y] = pc[x, y]
    return out


# ---------------------------------------------------------------- .ico e quadros

def ler_ico(caminho) -> dict[int, Image.Image]:
    out = {}
    with Image.open(caminho) as im:
        for w, h in sorted(im.ico.sizes()):
            out[w] = im.ico.getimage((w, h)).convert('RGBA')
    return out


def escrever_ico(quadros: dict[int, Image.Image], destino) -> None:
    """ICO com uma entrada PNG por tamanho, cada uma o quadro desenhado para aquele tamanho (sem reduzir)."""
    tam = sorted(quadros)
    dados = []
    for s in tam:
        buf = io.BytesIO()
        quadros[s].save(buf, 'PNG', optimize=True)
        dados.append(buf.getvalue())
    cab = struct.pack('<HHH', 0, 1, len(tam))
    off, ents = 6 + 16 * len(tam), b''
    for s, d in zip(tam, dados):
        ents += struct.pack('<BBBBHHII', s % 256, s % 256, 0, 0, 1, 32, len(d), off)
        off += len(d)
    Path(destino).parent.mkdir(parents=True, exist_ok=True)
    Path(destino).write_bytes(cab + ents + b''.join(dados))


def ler_quadros(id_: str, pasta=QUADROS) -> dict[int, Image.Image]:
    return {s: Image.open(Path(pasta) / id_ / f'{s}.png').convert('RGBA') for s in TAMANHOS}


def cores_dos_quadros(pasta=QUADROS) -> dict[str, str]:
    return json.loads((Path(pasta) / 'quadros.json').read_text(encoding='utf-8'))['cores']


def quadros_na_cor(id_: str, cor: str, pasta=QUADROS) -> dict[int, Image.Image]:
    """Os quadros de um ícone na cor pedida (recolore só se o mapa mudou a cor)."""
    q = ler_quadros(id_, pasta)
    base = cores_dos_quadros(pasta)[id_]
    if base.upper() == cor.upper():
        return q
    return {s: recolorir(im, base, cor) for s, im in q.items()}


def montar(mapa: dict, destino, pasta=QUADROS) -> list[Path]:
    """Um .ico por ícone usado no mapa, na cor do mapa. Devolve os arquivos escritos."""
    feitos = []
    defs = {**mapa['verbos'], **mapa['marcas']}
    for d in defs.values():
        alvo = Path(destino) / f'{d["icone"]}.ico'
        escrever_ico(quadros_na_cor(d['icone'], d['cor'], pasta), alvo)
        feitos.append(alvo)
    return feitos


def fazer_quadro(im: Image.Image, frente: str, operacao: str | None, correio=None, sem_selo=None) -> Image.Image:
    """Um quadro (um tamanho) do pacote do Ettore depois da operação da receita, ainda na cor original."""
    if not operacao:
        return im.copy()
    emblema, _, selo = operacao.partition('+')
    out = com_emblema(apagar_emblema(im, frente), frente, emblema)
    if selo and correio is not None:
        out = com_selo(out, correio, sem_selo)
    return out


def refazer_quadros(pacote, mapa: dict, destino=QUADROS, receita: dict | None = None) -> dict[str, str]:
    """Faz os quadros a partir do pacote do Ettore, pela receita (a ORIGEM, salvo outra), na cor do
    mapa. Devolve a origem de cada ícone (também gravada no quadros.json)."""
    pacote, destino = Path(pacote), Path(destino)
    receita = receita or ORIGEM
    cor_de = {d['icone']: d['cor'] for d in {**mapa['verbos'], **mapa['marcas']}.values()}
    cores, origem = {}, {}
    correio, sem_selo = ler_ico(pacote / 'nao-toco-correio.ico'), ler_ico(pacote / 'nao-toco.ico')
    for id_, (arquivo, operacao) in receita.items():
        q = ler_ico(pacote / arquivo)
        frente = rgb_hex(cor_da_frente(q[256]))
        if operacao == 'chip':
            feitos = trocar_por_chip(q, frente)
        else:
            feitos = {s: fazer_quadro(im, frente, operacao, correio.get(s), sem_selo.get(s)) for s, im in q.items()}
        novo = {s: recolorir(im, frente, cor_de[id_]) for s, im in feitos.items()}
        (destino / id_).mkdir(parents=True, exist_ok=True)
        for s, im in novo.items():
            im.save(destino / id_ / f'{s}.png', optimize=True)
        cores[id_] = cor_de[id_]
        mudou_cor = frente.upper() != cor_de[id_].upper()
        origem[id_] = (f'{arquivo}' + (f' + {operacao}' if operacao else ' (o desenho dele)')
                       + (f', recolorido de {frente} para {cor_de[id_]}' if mudou_cor else ', na cor dele'))
        print(f'{id_:20s} {origem[id_]}')
    (destino / 'quadros.json').write_text(json.dumps({
        'tamanhos': list(TAMANHOS), 'cores': cores, 'origem_de_cada': origem,
        'origem': 'pacote do Ettore "Ícones de pastas — versão 3" (05/10/2026) e, nos desenhos novos, as referências '
                  'dele (prototipos-icones\\referencia_icones), redesenhadas no mesmo estilo (desenho.py)'},
        ensure_ascii=False, indent=1), encoding='utf-8')
    return origem


# ---------------------------------------------------------------- prévia e amostra

def _uri(im: Image.Image) -> str:
    buf = io.BytesIO()
    im.save(buf, 'PNG')
    return 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode()


PREVIA_TAM = (16, 20, 32, 48, 256)


def previa(mapa: dict, destino, alternativas: dict[str, list[tuple[str, str]]] | None = None, pasta=QUADROS) -> None:
    defs = {**mapa['verbos'], **mapa['marcas']}
    linhas, grandes = [], []
    pequenos = [s for s in PREVIA_TAM if s < 256]
    for vid, d in defs.items():
        q = quadros_na_cor(d['icone'], d['cor'], pasta)
        cel = ''.join(f'<td><img class="ic" data-px="{s}" src="{_uri(q[s])}" alt=""></td>' for s in pequenos)
        linhas.append(f'<tr><th>{d["nome"]}<small>{d["cor"]}</small></th>{cel}</tr>')
        if 256 in PREVIA_TAM:
            grandes.append(f'<figure><img class="ic" data-px="256" src="{_uri(q[256])}" alt=""><figcaption>'
                           f'{d["nome"]}</figcaption></figure>')
    tabela = ('<table><tr><th></th>' + ''.join(f'<td class="t">{s} px</td>' for s in pequenos) + '</tr>'
              + ''.join(linhas) + '</table>'
              + (f'<h3>256 px (extragrandes)</h3><div class="grade">{"".join(grandes)}</div>' if grandes else ''))
    alt_html = ''
    for vid, opcoes in (alternativas or {}).items():
        d = defs[vid]
        cel = ''
        for rot, cor in opcoes:
            q = quadros_na_cor(d['icone'], cor, pasta)
            cel += (f'<div class="op"><b>{rot}</b> <code>{cor}</code><br>'
                    + ''.join(f'<img class="ic" data-px="{s}" src="{_uri(q[s])}" alt="">' for s in (16, 20, 32, 48))
                    + '</div>')
        alt_html += f'<h3>{d["nome"]}: a cor ainda não confirmada</h3><div class="ops">{cel}</div>'
    peacock = ''.join(
        f'<div class="mold"><div class="barra" style="background:{p["peacock"]}">{nome}</div>'
        f'<div class="corpo"></div><code>{p["peacock"]}</code></div>'
        for nome, p in mapa.get('projetos', {}).items() if p.get('peacock'))
    html = f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Prévia dos ícones</title>
<style>
:root {{ --fundo:#fafafa; --texto:#1b1b1b; --suave:#666; --linha:#ddd; }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --fundo:#161616; --texto:#eee; --suave:#aaa; --linha:#333; }} }}
:root[data-theme="dark"] {{ --fundo:#161616; --texto:#eee; --suave:#aaa; --linha:#333; }}
body {{ background:var(--fundo); color:var(--texto); font:15px/1.45 "Segoe UI", system-ui, sans-serif; margin:0; padding:16px; }}
main {{ max-width:1100px; margin:auto; }} p, li {{ color:var(--suave); }}
.lados {{ display:flex; flex-direction:column; gap:16px; }}
.lado {{ border-radius:10px; padding:12px 16px; overflow-x:auto; }}
.grade {{ display:flex; flex-wrap:wrap; gap:12px 20px; }} figure {{ margin:0; text-align:center; }}
figcaption {{ font-size:12px; opacity:.7; max-width:210px; }}
.claro {{ background:#ffffff; color:#1b1b1b; }} .escuro {{ background:#191919; color:#eee; }}
table {{ border-collapse:collapse; }} th {{ text-align:left; font-weight:600; padding:6px 12px 6px 0; white-space:nowrap; }}
th small {{ display:block; font-weight:400; opacity:.65; font-family:Consolas, monospace; }}
td {{ padding:6px 10px; vertical-align:middle; text-align:center; }} td.t {{ font-size:12px; opacity:.6; }}
img.ic {{ image-rendering:auto; display:inline-block; vertical-align:middle; margin:0 4px; }}
.ops {{ display:flex; gap:16px; flex-wrap:wrap; }} .op {{ background:#fff; color:#1b1b1b; padding:10px; border-radius:8px; }}
.mold {{ display:inline-block; width:220px; margin:0 12px 12px 0; border:1px solid var(--linha); border-radius:6px; overflow:hidden; }}
.mold .barra {{ color:#fff; padding:6px 10px; font-size:13px; }} .mold .corpo {{ height:50px; background:#1e1e1e; }}
.mold code {{ display:block; padding:4px 10px; }}
</style></head><body><main>
<h1>Os 9 ícones finais e as molduras do VS Code</h1>
<p>Cada ícone aparece no <b>tamanho real da tela</b>: a largura é ajustada pela escala do Windows (a sua está em
<span id="dpr">?</span>×), para os 125% não enganarem. 16 e 20 px são o painel lateral e os Detalhes; 32 e 48, os
ícones médios e grandes; 256, os extragrandes.</p>
<div class="lados"><div class="lado claro"><h2>Fundo claro</h2>{tabela}</div>
<div class="lado escuro"><h2>Fundo escuro</h2>{tabela}</div></div>
{alt_html}
<h2>A moldura de cada janela (Peacock)</h2><div>{peacock}</div>
<h2>O que conferir</h2><ul>
<li>Em 16 e 20 px, cada pasta se distingue das outras (sobretudo Eu leio × Trabalhamos juntos, e Não toco × correio).</li>
<li>O cadeado (Dado real) e o "?" (falta classificar), desenhados agora no estilo do seu pacote.</li>
<li>A cor do Projeto com IA (a marca da raiz de cada projeto e da mãe).</li>
<li>As quatro molduras: uma cor por janela, sem confundir com os ícones.</li></ul>
</main><script>
const r = window.devicePixelRatio || 1; document.getElementById('dpr').textContent = r;
document.querySelectorAll('img.ic').forEach(i => {{ const px = +i.dataset.px; i.style.width = (px / r) + 'px'; i.style.height = (px / r) + 'px'; }});
</script></body></html>'''
    Path(destino).write_text(html, encoding='utf-8')


def amostra(mapa: dict, pasta, pasta_quadros=QUADROS) -> list[Path]:
    """Uma pasta por verbo e marca, cada uma com o seu desktop.ini, para ver no Explorador de verdade.
    Os .ico ficam em <pasta>\\_ico. Nada fora de `pasta` é tocado."""
    sys.path.insert(0, str(AQUI))
    import regras
    pasta = Path(pasta)
    icos = pasta / '_ico'
    montar(mapa, icos, pasta_quadros)
    feitas = []
    defs = {**mapa['verbos'], **mapa['marcas']}
    for i, (vid, d) in enumerate(defs.items(), 1):
        p = pasta / f'{i} {d["nome"].replace("/", "-")}'
        p.mkdir(parents=True, exist_ok=True)
        texto = regras.montar_ini(icos / f'{d["icone"]}.ico', f'{d["nome"]} — {d["dica"]}', vid)
        regras.gravar_ini(p, texto)
        feitas.append(p)
    return feitas


def main(argv=None) -> int:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('comando', choices=['montar', 'previa', 'amostra', 'quadros'])
    ap.add_argument('alvo', type=Path)
    ap.add_argument('--mapa', type=Path, default=MODULO / 'mapa.json')
    a = ap.parse_args(argv)
    mapa = json.loads(a.mapa.read_text(encoding='utf-8'))
    if a.comando == 'montar':
        for f in montar(mapa, a.alvo):
            print(f)
    elif a.comando == 'previa':
        previa(mapa, a.alvo)
        print(a.alvo)
    elif a.comando == 'amostra':
        for p in amostra(mapa, a.alvo):
            print(p)
    else:
        refazer_quadros(a.alvo, mapa)
    return 0


if __name__ == '__main__':
    sys.exit(main())
