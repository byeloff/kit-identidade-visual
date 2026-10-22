#!/usr/bin/env python3
"""Índice navegável do kit de identidade (index.html), igual em todas as marcas.

Fonte única: a skill kit-identidade-visual (github.com/byeloff/kit-identidade-visual). Cada kit guarda uma
cópia em scripts/gerar-index.py e a sua configuração em scripts/index.json
(nome, domínio, descrição, cores e fontes). Só lê arquivos do kit e só escreve
index.html. Uso: python3 scripts/gerar-index.py [pasta-do-kit]
Requer Pillow e rsvg-convert (para medir o contraste das miniaturas SVG).
"""
import html, io, json, re, subprocess, sys
from pathlib import Path
from PIL import Image

ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
CFG = json.loads((ROOT / 'scripts/index.json').read_text())
C = CFG['cores']
IMG = {'.png', '.svg', '.jpg', '.webp'}
ROTULO = {'.svg': 'SVG', '.png': 'PNG', '.pdf': 'PDF', '.html': 'HTML', '.ico': 'ICO', '.webmanifest': 'Manifest',
          '.css': 'CSS', '.json': 'JSON', '.md': 'Texto', '.ttf': 'TTF', '.txt': 'Licença', '.zip': 'ZIP'}
e = lambda s: html.escape(str(s), quote=True)
rel = lambda p: p.relative_to(ROOT).as_posix()


# ---------- cor das miniaturas ----------

def lum(rgb):
    v = [c / 255 for c in rgb]
    v = [c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4 for c in v]
    return .2126 * v[0] + .7152 * v[1] + .0722 * v[2]


def contraste(a, b):
    a, b = sorted((lum(a), lum(b)), reverse=True)
    return (a + .05) / (b + .05)


def hexrgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


_cache = {}
def amostra(p):
    """(cobertura opaca, cor média do conteúdo) de uma imagem do kit."""
    if p in _cache:
        return _cache[p]
    try:
        if p.suffix == '.svg':
            png = subprocess.run(['rsvg-convert', '-w', '96', str(p)], capture_output=True, check=True).stdout
            im = Image.open(io.BytesIO(png))
        else:
            im = Image.open(p)
            im.thumbnail((96, 96))
        im = im.convert('RGBA')
        px = list(im.get_flattened_data() if hasattr(im, "get_flattened_data") else im.getdata())
        vis = [q for q in px if q[3] > 40]
        if not vis:
            r = (0, (0, 0, 0))
        else:
            n = len(vis)
            r = (n / len(px), tuple(sum(q[i] for q in vis) // n for i in range(3)))
    except Exception:
        r = (1, (128, 128, 128))
    _cache[p] = r
    return r


def fundo(p):
    """Fundo da miniatura: transparente ganha o tom da marca com mais contraste."""
    cob, cor = amostra(p)
    if cob > .97:
        return C['superficie']
    return max((C['escuro'], C['claro']), key=lambda f: contraste(cor, hexrgb(f)))


def medidas(p):
    if p.suffix == '.svg':
        m = re.search(r'viewBox="[\d.\-]+\s+[\d.\-]+\s+([\d.]+)\s+([\d.]+)"', p.read_text(errors='ignore')[:3000])
        return f'{float(m[1]):g} × {float(m[2]):g}' if m else ''
    try:
        w, h = Image.open(p).size
        return f'{w} × {h}'
    except Exception:
        return ''


# ---------- agrupamento ----------

def chave(p):
    """Agrupa variantes do mesmo arquivo: @2x, -1x/-4x e tamanhos (-192, -512)."""
    s = re.sub(r'@\dx$', '', p.stem)
    s = re.sub(r'-(\d)x$', '', s)
    s = re.sub(r'-(16|32|48|64|180|192|512|1024)$', '', s)
    return s


def ordem_formato(p):
    return (['.svg', '.png', '.pdf', '.html'].index(p.suffix) if p.suffix in ('.svg', '.png', '.pdf', '.html') else 9, p.name)


def grupos(arquivos):
    g = {}
    for p in arquivos:
        g.setdefault((p.parent, chave(p)), []).append(p)
    out = []
    for (_, nome), fs in g.items():
        imgs = [f for f in fs if f.suffix in IMG]
        if not imgs:
            continue
        svg = [f for f in imgs if f.suffix == '.svg']
        rasters = sorted([f for f in imgs if f.suffix != '.svg'], key=lambda f: f.stat().st_size)
        capa = svg[0] if svg else (rasters[len(rasters) // 2] if len(rasters) > 2 else rasters[0])
        out.append({'nome': nome, 'capa': capa, 'arquivos': sorted(fs, key=ordem_formato)})
    return sorted(out, key=lambda x: x['nome'])


def arquivos(pasta, recursivo=False, ignorar=('fonte', 'fontes', '__pycache__')):
    d = ROOT / pasta
    if not d.is_dir():
        return []
    it = d.rglob('*') if recursivo else d.iterdir()
    return sorted(p for p in it if p.is_file() and p.name != '.DS_Store'
                  and not any(x in ignorar for x in p.relative_to(d).parts[:-1]))


def png_do_logo(svg):
    fam = svg.parent.name
    return [p for p in (ROOT / 'logo/png' / f'{fam}-{svg.stem}-{x}x.png' for x in (1, 4)) if p.exists()]


# ---------- HTML ----------

def chip(p, rotulo=None):
    r = rotulo or ROTULO.get(p.suffix, p.suffix[1:].upper())
    m = re.search(r'(@\dx|-\dx|-\d{2,4})$', p.stem)
    if m and p.suffix == '.png':
        r += ' ' + m[1].lstrip('-')
    return f'<a class="chip" href="{e(rel(p))}">{e(r)}</a>'


def card(g, largo=False):
    capa = g['capa']
    fs = g['arquivos']
    return (f'<figure class="card{" largo" if largo else ""}">'
            f'<a class="tile" href="{e(rel(capa))}" style="background:{fundo(capa)}">'
            f'<img loading="lazy" src="{e(rel(capa))}" alt="{e(g["nome"])}"></a>'
            f'<figcaption><span class="nome">{e(g["nome"])}</span><span class="dim">{e(medidas(capa))}</span>'
            f'<span class="chips">{"".join(chip(f) for f in fs)}</span></figcaption></figure>')


def grade(gs, largo=False, cls=''):
    return f'<div class="grade{(" " + cls) if cls else ""}">' + ''.join(card(g, largo) for g in gs) + '</div>' if gs else ''


def lista(fs):
    return '<ul class="docs">' + ''.join(
        f'<li><a href="{e(rel(p))}"><span>{e(p.relative_to(ROOT).as_posix())}</span><em>{e(ROTULO.get(p.suffix, p.suffix[1:].upper()))}</em></a></li>'
        for p in fs) + '</ul>' if fs else ''


secoes = []
def secao(id_, titulo, corpo, n, nota=''):
    if corpo.strip():
        secoes.append((id_, titulo, n,
                       f'<section id="{id_}"><header class="sec"><h2>{e(titulo)}</h2><span class="n">{n}</span></header>'
                       + (f'<p class="nota">{e(nota)}</p>' if nota else '') + corpo + '</section>'))


# Logo: famílias em SVG, cada uma com os PNGs 1x/4x de logo/png.
corpo, n = '', 0
ordem_fam = ['horizontal', 'vertical', 'wordmark', 'simbolo', 'grafismo']
fams = sorted([d for d in (ROOT / 'logo').iterdir() if d.is_dir() and d.name != 'png'],
              key=lambda d: (ordem_fam.index(d.name) if d.name in ordem_fam else 5, d.name))
for d in fams:
    gs = []
    for svg in sorted(d.glob('*.svg')):
        if svg.stem == 'construcao':
            continue
        extras = [p for p in d.iterdir() if p.stem == svg.stem and p.suffix != '.svg'] + png_do_logo(svg)
        gs.append({'nome': svg.stem, 'capa': svg, 'arquivos': [svg] + sorted(extras, key=ordem_formato)})
    if not gs:
        gs = grupos([p for p in d.iterdir() if p.is_file()])
    n += len(gs)
    corpo += f'<h3>{e(d.name.replace("simbolo", "símbolo"))}</h3>' + grade(gs, cls='logos')
regras = grupos([p for p in arquivos('logo') if p.stem in ('area-protecao', 'reducao-minima')]
                + [p for p in arquivos('logo/simbolo') if p.stem == 'construcao'])
if regras:
    n += len(regras)
    corpo += '<h3>construção e limites</h3>' + grade(regras, largo=True)
secao('logo', 'Logo', corpo, n, 'Clique na miniatura para abrir o arquivo; os botões levam a cada formato.')

for id_, titulo, pasta, largo, nota in [
    ('icone', 'Ícone do app', 'icone-app', False, ''),
    ('favicon', 'Favicon', 'favicon', False, 'Use favicon/integracao.html como snippet do <head>.'),
]:
    fs = arquivos(pasta)
    gs = grupos(fs)
    soltos = [p for p in fs if p.suffix not in IMG]
    secao(id_, titulo, grade(gs, largo) + lista(soltos), len(gs), nota)

for id_, titulo, pasta, extra in [('cores', 'Cores', 'cores', None), ('tipografia', 'Tipografia', 'tipografia', '_fontes')]:
    fs = arquivos(pasta) + (arquivos(extra) if extra else [])
    gs = grupos([p for p in fs if p.suffix in IMG])
    secao(id_, titulo, grade(gs, largo=True) + lista([p for p in fs if p.suffix not in IMG]), len(gs))

for id_, titulo, pasta, rec, largo in [
    ('social', 'Redes sociais', 'social', False, False),
    ('instagram', 'Avatares do Instagram', 'instagram-avatar', False, False),
    ('linkedin', 'LinkedIn e Facebook', 'linkedin', True, True),
    ('wallpapers', 'Wallpapers', 'wallpapers', False, True),
    ('aplicacoes', 'Aplicações', 'aplicacoes', False, True),
]:
    fs = arquivos(pasta, recursivo=rec)
    gs = grupos([p for p in fs if p.suffix in IMG] + [p for p in fs if p.suffix in ('.pdf', '.html') and any(q.stem == p.stem and q.suffix in IMG for q in fs)])
    secao(id_, titulo, grade(gs, largo) + lista([p for p in fs if p.suffix == '.md']), len(gs))

paginas = sorted((ROOT / 'guia/paginas').glob('*.svg')) if (ROOT / 'guia/paginas').is_dir() else []
guia_docs = [p for p in arquivos('guia') if p.suffix in ('.html', '.pdf')]
secao('guia', 'Guia de marca', lista(guia_docs) + grade([{'nome': f'página {p.stem}', 'capa': p, 'arquivos': [p]} for p in paginas], largo=True), len(paginas))

docs = [ROOT / f for f in ('README.md', 'BRIEF-KIT.md', 'manifest.json', 'qa-report.json') if (ROOT / f).exists()]
secao('entrega', 'Entrega', lista(docs + sorted((ROOT / 'scripts').glob('*.py'))), len(docs))

# Logo do cabeçalho: a versão horizontal que aparece sobre o tom escuro da marca.
cands = [ROOT / 'logo/horizontal' / f'{s}.svg' for s in ('escuro', 'negativo', 'claro', 'principal')]
cands = [p for p in cands if p.exists()]
logo_topo = max(cands, key=lambda p: contraste(amostra(p)[1], hexrgb(C['escuro'])))

zip_ = ROOT / '_dist' / f'{ROOT.name}.zip'
acoes = [('guia/guia-de-marca.html', 'Abrir o guia'), ('guia/guia-de-marca.pdf', 'Guia em PDF'),
         (f'_dist/{ROOT.name}.zip', 'Baixar o kit (.zip)'), ('README.md', 'README')]
acoes = [(h, t) for h, t in acoes if (ROOT / h).exists() or h.startswith('_dist/')]
F = CFG['fontes']
fam = lambda s: ', '.join(f'"{x}"' for x in s) + ', system-ui, sans-serif'

css = f''':root{{--fundo:{C['fundo']};--sup:{C['superficie']};--texto:{C['texto']};--suave:{C['suave']};--linha:{C['linha']};
--escuro:{C['escuro']};--claro:{C['claro']};--destaque:{C['destaque']};--sobre-destaque:{C['texto_no_destaque']};--topo-texto:{C['texto_no_escuro']};
--f-titulo:{fam(F['titulo'])};--f-texto:{fam(F['texto'])};--f-mono:{fam(F.get('mono') or F['texto'])};--raio:{CFG.get('raio', 10)}px}}
*{{box-sizing:border-box}}html{{scroll-behavior:smooth;scroll-padding-top:24px}}
body{{margin:0;background:var(--fundo);color:var(--texto);font:16px/1.5 var(--f-texto);-webkit-font-smoothing:antialiased}}
a{{color:inherit}}
.topo{{background:var(--escuro);color:var(--topo-texto)}}
.topo .in{{max-width:1360px;margin:auto;padding:48px 32px 40px;display:grid;gap:28px}}
.topo img.marca{{height:56px;width:auto;max-width:100%}}
.topo p{{margin:0;max-width:62ch;opacity:.86}}
.meta{{font:12px/1.4 var(--f-mono);letter-spacing:.08em;text-transform:uppercase;opacity:.7}}
.acoes{{display:flex;flex-wrap:wrap;gap:10px}}
.acoes a{{text-decoration:none;font-weight:600;font-size:14px;padding:10px 16px;border-radius:var(--raio);border:1px solid color-mix(in srgb,var(--topo-texto) 35%,transparent)}}
.acoes a:first-child{{background:var(--destaque);color:var(--sobre-destaque);border-color:var(--destaque)}}
.acoes a:hover{{border-color:var(--topo-texto)}}
.corpo{{max-width:1360px;margin:auto;padding:32px;display:grid;grid-template-columns:200px minmax(0,1fr);gap:48px;align-items:start}}
nav{{position:sticky;top:24px;display:grid;gap:2px}}
nav a{{display:flex;justify-content:space-between;gap:8px;text-decoration:none;font-size:14px;padding:7px 10px;border-radius:calc(var(--raio) * .6);color:var(--suave)}}
nav a:hover,nav a.ativo{{background:var(--sup);color:var(--texto)}}
nav a span{{font:12px var(--f-mono);opacity:.7}}
.prancha{{margin:0 0 56px;border-radius:var(--raio);overflow:hidden;border:1px solid var(--linha);background:var(--sup)}}
.prancha img{{display:block;width:100%;height:auto}}
section{{margin:0 0 64px}}
header.sec{{display:flex;align-items:baseline;gap:12px;border-bottom:1px solid var(--linha);padding-bottom:12px;margin-bottom:20px}}
h2{{font:700 clamp(24px,3vw,32px)/1.1 var(--f-titulo);margin:0;letter-spacing:-.01em}}
h3{{font:12px/1 var(--f-mono);letter-spacing:.1em;text-transform:uppercase;color:var(--suave);margin:28px 0 12px}}
.n{{font:12px var(--f-mono);color:var(--suave)}}
.nota{{color:var(--suave);font-size:14px;margin:-8px 0 16px}}
.grade{{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:16px}}
.grade:has(.largo){{grid-template-columns:repeat(auto-fill,minmax(300px,1fr))}}
.card{{margin:0;background:var(--sup);border:1px solid var(--linha);border-radius:var(--raio);overflow:hidden;display:flex;flex-direction:column}}
.tile{{display:block;aspect-ratio:4/3;padding:18px;overflow:hidden}}
.largo .tile{{aspect-ratio:16/10;padding:14px}}
.tile img{{width:100%;height:100%;object-fit:contain;display:block}}
.logos .tile{{padding:28px 32px}}
figcaption{{padding:12px 14px 14px;display:grid;gap:8px;border-top:1px solid var(--linha)}}
.nome{{font-weight:600;font-size:14px;overflow-wrap:anywhere}}
.dim{{font:12px var(--f-mono);color:var(--suave)}}
.chips{{display:flex;flex-wrap:wrap;gap:6px}}
.chip{{font:11px/1 var(--f-mono);text-decoration:none;padding:6px 8px;border-radius:999px;border:1px solid var(--linha);color:var(--suave)}}
.chip:hover{{color:var(--texto);border-color:var(--texto)}}
.docs{{list-style:none;padding:0;margin:0 0 20px;display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:8px}}
.docs a{{display:flex;justify-content:space-between;gap:12px;text-decoration:none;padding:12px 14px;background:var(--sup);border:1px solid var(--linha);border-radius:var(--raio);font-size:14px}}
.docs a:hover{{border-color:var(--texto)}}
.docs span{{overflow-wrap:anywhere}}.docs em{{font:normal 11px var(--f-mono);color:var(--suave);white-space:nowrap;align-self:center}}
footer{{max-width:1360px;margin:auto;padding:24px 32px 48px;font:12px var(--f-mono);color:var(--suave)}}
a:focus-visible{{outline:2px solid var(--destaque);outline-offset:2px}}
@media (max-width:820px){{.corpo{{grid-template-columns:1fr;padding:20px 16px;gap:24px}}
nav{{position:sticky;top:0;z-index:2;display:flex;overflow-x:auto;gap:4px;background:var(--fundo);padding:10px 0;margin:0 -16px;padding-inline:16px}}
nav a{{white-space:nowrap;background:var(--sup)}}nav a span{{display:none}}
.topo .in{{padding:32px 16px}}.topo img.marca{{height:40px}}.grade{{grid-template-columns:repeat(auto-fill,minmax(150px,1fr))}}
.grade:has(.largo){{grid-template-columns:1fr}}}}
'''

js = '''const links=[...document.querySelectorAll('nav a')];const io=new IntersectionObserver(es=>{es.forEach(x=>{if(x.isIntersecting){links.forEach(a=>a.classList.toggle('ativo',a.hash==='#'+x.target.id))}})},{rootMargin:'-20% 0px -70% 0px'});document.querySelectorAll('section[id]').forEach(s=>io.observe(s));'''

prancha = ROOT / 'identidade-visual.png'
doc = f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(CFG['nome'])} · identidade visual</title>
<link rel="stylesheet" href="tipografia/fontes.css">
<style>{css}</style>
</head>
<body>
<header class="topo"><div class="in">
<img class="marca" src="{e(rel(logo_topo))}" alt="{e(CFG['nome'])}">
<p class="meta">{e(' · '.join(x for x in (CFG.get('dominio'), CFG.get('status')) if x))}</p>
<p>{e(CFG['descricao'])}</p>
<div class="acoes">{''.join(f'<a href="{e(h)}">{e(t)}</a>' for h, t in acoes)}</div>
</div></header>
<div class="corpo">
<nav aria-label="Seções do kit">{''.join(f'<a href="#{i}">{e(t)}<span>{n}</span></a>' for i, t, n, _ in secoes)}</nav>
<main>
{f'<figure class="prancha"><a href="identidade-visual.png"><img src="identidade-visual.png" alt="Prancha da identidade {e(CFG["nome"])}"></a></figure>' if prancha.exists() else ''}
{''.join(s for *_, s in secoes)}
</main>
</div>
<footer>Kit de identidade visual {e(CFG['nome'])} · gerado por scripts/gerar-index.py · padrão kit-identidade-visual</footer>
<script>{js}</script>
</body>
</html>
'''
(ROOT / 'index.html').write_text(doc)
print(f'index.html: {len(secoes)} seções, {sum(n for _, _, n, _ in secoes)} itens')
