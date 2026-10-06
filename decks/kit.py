"""Shared slide kit for the two portfolio decks (detailed + presenting). Writes project/deck.json and
project/slides/<id>.html under a root folder. Both decks use the same look as mancinitan.com (Sage palette,
Archivo for text, and Archivo at weight 900 and 68% width for display, like the site)."""
import json, os, html, math, datetime

INK = '#14281E'; BODY = '#3E4C44'; MUTED = '#5F6E65'; ACCENT = '#1F6B4A'
LIGHT = '#F4F6EF'; MINT = '#E3EEE3'; CARD = '#FBFCF8'; RULE = '#D3DDD2'
DARK = '#12251B'; BUTTER = '#F2EAC4'
# Text on dark slides uses the site's dark-mode pairing (site.css, sage dark): ink, muted, accent. Pale green, never white.
ON_DARK = '#D4E8DA'; ON_DARK_BODY = '#8AA392'; ON_DARK_ACCENT = '#6FD6A4'
# The site's light hero: ground, the three glows and the deep-green fourth (site.css body background), ink and muted.
SITE_GROUND = '#E2EBDD'; SITE_INK = '#0F1812'; SITE_MUTED = '#4F5F55'; SITE_ACCENT = '#1D6A4C'
BODYF = "'Archivo', Arial, sans-serif"; DISP = "'Archivo Condensed', 'Arial Narrow', Arial, sans-serif"
# Slides drops font-stretch, so the site's display cut (Archivo, weight 900, 68% width) ships as its own static
# font file: fonts/ArchivoCondensed-Black.woff2, made with fontTools from the variable Archivo and uploaded per deck.
DSTYLE = 'font-weight:900'
NSTYLE = 'font-weight:900;font-variant-numeric:tabular-nums'
CONDENSED_SRC = {'detailed': '/_blob/b675ce494d818dd5d2cf1c0b3c37a3a3', 'present': '/_blob/ef1df9f06bc4d06caf1d76cff71a0d41'}
FACES = {
    'archivo': {'family': 'Archivo', 'href': 'https://fonts.googleapis.com/css2?family=Archivo:ital,wdth,wght@0,62..125,300..900;1,62..125,300..900&display=swap'},
}

def light_text(h):
    """Body text on the site is Archivo 300: give every p/ul/ol that doesn't set a weight font-weight:300."""
    import re
    def fix(m):
        style = m.group(2)
        return m.group(0) if 'font-weight' in style else f'<{m.group(1)} style="font-weight:300;{style}"'
    return re.sub(r'<(p|ul|ol) style="([^"]*)"', fix, h)

def e(t):
    """Escape plain text; keep <b> and <br> written as [[b]]…[[/b]] markers."""
    return html.escape(t, quote=False).replace('[[b]]', '<b>').replace('[[/b]]', '</b>').replace('[[br]]', '<br>')

def lines(text, size, width, k=0.5):
    cpl = max(8, int(width / (k * size)))
    out = 0
    for para in text.split('\n'):
        words = para.split(); cur = 0; n = 1
        for w in words:
            if cur and cur + 1 + len(w) > cpl: n += 1; cur = len(w)
            else: cur += (1 if cur else 0) + len(w)
        out += n
    return out

class Deck:
    def __init__(self, root, title, footer_name, condensed_src=None):
        self.condensed_src = condensed_src
        self.root = root; self.title = title; self.order = []; self.sections = {}; self.files = {}
        self.footer_name = footer_name; self.cur_label = ''
        os.makedirs(os.path.join(root, 'project', 'slides'), exist_ok=True)

    def section(self, key, desc, label):
        self.pending_section = (key, desc); self.cur_label = label

    def add(self, sid, inner, bg=LIGHT, color=INK, notes=None, dark=False, footer=True, layout="display:flex;flex-direction:column;gap:32px", pad="128px 128px 160px", transition='fade'):
        if getattr(self, 'pending_section', None):
            k, d = self.pending_section; self.sections[k] = {'description': d, 'start': sid}; self.pending_section = None
        foot = ''
        if footer:
            fc = ON_DARK_BODY if dark else MUTED
            foot = (f'<p style="position:absolute;left:128px;bottom:64px;width:1100px;font-size:24px;color:{fc};font-family:{BODYF}">'
                    f'{e(self.footer_name)}{" · " + e(self.cur_label) if self.cur_label else ""}</p>')
        aside = f'<aside>{e(notes)}</aside>' if notes else ''
        out = (f'<section id="{sid}" data-transition="{transition}" style="background:{bg};color:{color};font-family:{BODYF};'
               f'padding:{pad};{layout}">\n{inner}\n{foot}\n{aside}\n</section>\n')
        self.order.append(sid); self.files[sid] = out

    def write(self):
        idx = {'v': 4, 'createdOnFiles': {'v': 1, 'at': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')},
               'lists': 'css', 'title': self.title, 'order': self.order, 'sections': self.sections, 'cover': self.order[0],
               'faces': {**FACES, **({'archivo-condensed': {'family': 'Archivo Condensed', 'src': self.condensed_src}} if self.condensed_src else {})}, 'designSystems': []}
        json.dump(idx, open(os.path.join(self.root, 'project', 'deck.json'), 'w'), ensure_ascii=False, indent=1)
        for sid, h in self.files.items():
            h = light_text(h)
            open(os.path.join(self.root, 'project', 'slides', f'{sid}.html'), 'w').write(h)
        return len(self.order)

# ------------------------------------------------------------------ building blocks
def eyebrow(t, dark=False):
    c = ON_DARK_ACCENT if dark else ACCENT
    return f'<p style="font-size:24px;font-weight:600;letter-spacing:2px;text-transform:uppercase;color:{c}">{e(t)}</p>'

def h2(t, dark=False, size=64):
    c = ON_DARK if dark else INK
    return f'<h2 style="font-family:{BODYF};font-size:{size}px;font-weight:500;line-height:1.12;letter-spacing:-0.015em;color:{c}">{e(t)}</h2>'

def statement(t, dark=False, size=40):
    c = ON_DARK if dark else ACCENT
    return f'<p style="font-size:{size}px;font-weight:500;line-height:1.25;color:{c}">{e(t)}</p>'

def callout(t, dark=False, size=36):
    """The key line of a slide, in a soft container so it reads first."""
    if dark:
        return statement(t, dark, size)
    return (f'<div style="background:{MINT};border-radius:20px;padding:22px 30px">'
            f'<p style="font-size:{size}px;font-weight:500;line-height:1.3;color:{ACCENT}">{e(t)}</p></div>')

def para(t, dark=False, size=28):
    c = ON_DARK_BODY if dark else BODY
    return f'<p style="font-size:{size}px;font-weight:300;line-height:1.5;color:{c}">{e(t)}</p>'

def img(src, alt, w, h, fit='contain', radius=20, bg=None, shadow=True):
    b = f'background:{bg};' if bg else ''
    s = 'box-shadow:0 24px 48px -28px rgba(20,40,30,0.45);' if shadow else ''
    return f'<img src="{src}" alt="{html.escape(alt)}" style="width:{w}px;height:{h}px;object-fit:{fit};border-radius:{radius}px;{b}{s}">'

def caption(title, text, width, dark=False):
    tc = ON_DARK if dark else INK; bc = ON_DARK_BODY if dark else MUTED
    t = f'<p style="font-size:24px;font-weight:600;color:{tc};line-height:1.3">{e(title)}</p>' if title else ''
    x = f'<p style="font-size:24px;color:{bc};line-height:1.35">{e(text)}</p>' if text else ''
    return f'<div style="width:{width}px;display:flex;flex-direction:column;gap:4px">{t}{x}</div>'

PHONE_RATIO = 0.4615  # 600 x 1300 screens

def phones(items, max_w, max_h, gap=28, caps=True):
    """items: (src, alt, title, text). Returns a row of phone screenshots that fits max_w x max_h."""
    n = len(items)
    cap_h = 86 if caps and any(i[2] or i[3] for i in items) else 0
    h = max_h - cap_h; w = h * PHONE_RATIO
    if n * w + (n - 1) * gap > max_w:
        w = (max_w - (n - 1) * gap) / n; h = w / PHONE_RATIO
    w = int(w); h = int(h)
    cols = []
    for src, alt, t, x in items:
        c = caption(t, x, w) if cap_h else ''
        cols.append(f'<div style="display:flex;flex-direction:column;gap:14px">{img(src, alt, w, h, "cover", 26)}{c}</div>')
    return f'<div style="display:flex;flex-direction:row;gap:{gap}px;align-items:flex-start">{"".join(cols)}</div>'

def text_height(blocks, width):
    """blocks: list of (kind, text). Rough height of a text column."""
    H = 0
    for kind, t in blocks:
        if kind == 'eyebrow': H += 34
        elif kind == 'h2': H += lines(t, 64, width, 0.52) * 64 * 1.1
        elif kind == 'h2s': H += lines(t, 56, width, 0.52) * 56 * 1.1
        elif kind == 'st': H += lines(t, 36, width - 60, 0.5) * 36 * 1.3 + 48
        elif kind == 'st34': H += lines(t, 32, width - 60, 0.5) * 32 * 1.3 + 48
        elif kind == 'p': H += lines(t, 28, width, 0.5) * 28 * 1.5
        elif kind == 'p26': H += lines(t, 26, width, 0.5) * 26 * 1.5
        elif kind == 'p24': H += lines(t, 24, width, 0.5) * 24 * 1.5
        H += 28
    return H

def text_col(blocks, width, dark=False):
    out = []
    for kind, t in blocks:
        if kind == 'eyebrow': out.append(eyebrow(t, dark))
        elif kind == 'h2': out.append(h2(t, dark))
        elif kind == 'h2s': out.append(h2(t, dark, 56))
        elif kind == 'st': out.append(callout(t, dark))
        elif kind == 'st34': out.append(callout(t, dark, 34))
        elif kind == 'p': out.append(para(t, dark))
        elif kind == 'p26': out.append(para(t, dark, 26))
        elif kind == 'p24': out.append(para(t, dark, 24))
    return f'<div style="width:{width}px;display:flex;flex-direction:column;gap:28px">{"".join(out)}</div>'

def fit_blocks(blocks, width, limit):
    """Step body text down from 28 to 26 to 24px until the column fits; returns new blocks and height."""
    for p_kind, s_kind in (('p', 'st'), ('p26', 'st'), ('p24', 'st34')):
        b2 = [(p_kind if k == 'p' else (s_kind if k == 'st' else k), t) for k, t in blocks]
        hgt = text_height(b2, width)
        if hgt <= limit: return b2, hgt
    return b2, hgt

def tile(label, title, text, width=None, dark=False, img_html=''):
    bg = '#1B3527' if dark else CARD; bd = '#2C4A39' if dark else RULE
    tc = ON_DARK if dark else INK; bc = ON_DARK_BODY if dark else BODY
    w = f'width:{width}px;' if width else 'flex:1;'
    lab = (f'<p style="font-size:24px;font-weight:600;color:{ACCENT if not dark else ON_DARK_ACCENT};text-transform:uppercase;letter-spacing:1.5px">{e(label)}</p>' if label else '')
    ti = f'<h3 style="font-size:32px;font-weight:600;line-height:1.2;color:{tc}">{e(title)}</h3>' if title else ''
    tx = f'<p style="font-size:24px;line-height:1.45;color:{bc}">{e(text)}</p>' if text else ''
    return (f'<div style="{w}display:flex;flex-direction:column;gap:14px;background:{bg};border:1px solid {bd};border-radius:20px;padding:32px">'
            f'{img_html}{lab}{ti}{tx}</div>')

def stat(num, label, dark=False, size=112, width=None, small=False):
    nc = ON_DARK_ACCENT if dark else ACCENT; lc = ON_DARK_BODY if dark else BODY
    w = f'width:{width}px;' if width else 'flex:1;'
    ls = 24 if small else 28
    return (f'<div style="{w}display:flex;flex-direction:column;gap:8px">'
            f'<p style="font-family:{DISP};font-size:{size}px;{NSTYLE};line-height:0.9;color:{nc}">{e(num)}</p>'
            f'<p style="font-size:{ls}px;line-height:1.35;color:{lc}">{e(label)}</p></div>')
