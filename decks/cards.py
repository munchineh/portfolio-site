"""Scannable layouts for the presenting deck: points live in numbered cards (a bold lead plus one short line),
and visuals get most of the slide, framed like the site's demo panels."""
from layouts import *
from assets import aspect

PAD = '96px 128px 144px'      # content box 1664 x 840; footer row sits below it
CW, CH = 1664, 840
FRAME_BG = 'linear-gradient(135deg, #CFE6D5 0%, #E7EEDD 50%, #F3EAC4 100%)'


def head(eb, title, dark=False, size=56):
    c = ON_DARK if dark else INK
    return (f'{eyebrow(eb, dark)}'
            f'<h2 style="font-family:{BODYF};font-size:{size}px;font-weight:500;line-height:1.1;letter-spacing:-0.015em;color:{c}">{e(title)}</h2>')


def card(lead, detail=None, n=None, lead_size=34, detail_size=26, pad='22px 28px'):
    num = (f'<p style="font-family:{DISP};font-size:44px;{DSTYLE};line-height:1;color:{ACCENT};width:52px">{e(n)}</p>' if n else '')
    det = (f'<p style="font-size:{detail_size}px;font-weight:400;line-height:1.35;color:{BODY}">{e(detail)}</p>' if detail else '')
    return (f'<div style="display:flex;flex-direction:row;gap:20px;align-items:flex-start;background:{CARD};border:1px solid {RULE};border-radius:20px;padding:{pad}">'
            f'{num}<div style="flex:1;display:flex;flex-direction:column;gap:6px">'
            f'<p style="font-size:{lead_size}px;font-weight:600;line-height:1.15;color:{INK}">{e(lead)}</p>{det}</div></div>')


def cards_col(items, gap=14, numbered=True, **kw):
    return (f'<div style="display:flex;flex-direction:column;gap:{gap}px">'
            + ''.join(card(l, x, f'{i + 1:02d}' if numbered else None, **kw) for i, (l, x) in enumerate(items)) + '</div>')


def fit(key, w, h):
    a = aspect(key)
    if w / h > a:
        return int(h * a), int(h)
    return int(w), int(w / a)


def framed(A, key, alt, w, h, pad=40, radius=14, bg=FRAME_BG):
    """A screenshot fitted inside a soft gradient panel, like the demo panels on the site."""
    iw, ih = fit(key, w - 2 * pad, h - 2 * pad)
    return (f'<div style="width:{w}px;height:{h}px;display:flex;align-items:center;justify-content:center;background:{bg};border-radius:28px">'
            f'<img src="{A[key]}" alt="{html.escape(alt)}" style="width:{iw}px;height:{ih}px;object-fit:contain;border-radius:{radius}px;box-shadow:0 24px 48px -24px rgba(20,40,30,0.45)"></div>')


def phones_framed(A, keys, w, h, pad=44, gap=24, bg=FRAME_BG):
    n = len(keys)
    ph = h - 2 * pad
    pw = ph * aspect(keys[0][0])
    if n * pw + (n - 1) * gap > w - 2 * pad:
        pw = (w - 2 * pad - (n - 1) * gap) / n
        ph = pw / aspect(keys[0][0])
    pw, ph = int(pw), int(ph)
    imgs = ''.join(f'<img src="{A[k]}" alt="{html.escape(alt)}" style="width:{pw}px;height:{ph}px;object-fit:cover;border-radius:{int(pw * 0.11)}px;box-shadow:0 24px 48px -24px rgba(20,40,30,0.5)">' for k, alt in keys)
    return (f'<div style="width:{w}px;height:{h}px;display:flex;flex-direction:row;gap:{gap}px;align-items:center;justify-content:center;background:{bg};border-radius:28px">{imgs}</div>')


def media_slide(d, sid, eb, title, items, visual, vis_w, notes, gap=56, head_size=52, numbered=True, **kw):
    """Heading and numbered point cards on the left, a big visual on the right."""
    tw = CW - vis_w - gap
    left = (f'<div style="width:{tw}px;display:flex;flex-direction:column;gap:28px">'
            f'<div style="display:flex;flex-direction:column;gap:14px">{head(eb, title, size=head_size)}</div>'
            f'{cards_col(items, numbered=numbered, **kw)}</div>')
    d.add(sid, f'<div style="display:flex;flex-direction:row;gap:{gap}px;align-items:center;height:{CH}px">{left}{visual}</div>',
          notes=notes, pad=PAD, layout='display:flex;flex-direction:column')


def case_hero(d, sid, no, title, lede, meta, stats, hero_html, notes, note=None):
    metas = ''.join(f'<div style="display:flex;flex-direction:column;gap:4px;flex:1"><p style="font-size:24px;color:{MUTED}">{e(k)}</p>'
                    f'<p style="font-size:26px;font-weight:400;color:{INK};line-height:1.3">{e(v)}</p></div>' for k, v in meta)
    sts = ''.join(stat(n, l, size=88, small=False) for n, l in stats)
    left = (f'<div style="width:960px;display:flex;flex-direction:column;gap:24px">'
            f'{eyebrow(no)}'
            f'<h1 style="font-family:{DISP};font-size:104px;{DSTYLE};line-height:0.92;text-transform:uppercase;color:{INK}">{e(title)}</h1>'
            f'<p style="font-size:28px;font-weight:400;line-height:1.4;color:{BODY}">{e(lede)}</p>'
            f'<div style="display:flex;flex-direction:row;gap:24px;border-top:1px solid {RULE};padding:18px 0 0 0">{metas}</div>'
            f'<div style="display:flex;flex-direction:row;gap:40px">{sts}</div>'
            + (f'<p style="font-size:24px;color:{MUTED}">{e(note)}</p>' if note else '') + '</div>')
    d.add(sid, f'<div style="display:flex;flex-direction:row;gap:64px;align-items:center;height:{CH}px">{left}{hero_html}</div>',
          bg=f'linear-gradient(135deg, {MINT} 0%, {LIGHT} 55%, {BUTTER} 100%)', notes=notes, pad=PAD, layout='display:flex;flex-direction:column')


def hero_img(A, key, alt, w=640, h=800):
    return (f'<img src="{A[key]}" alt="{html.escape(alt)}" style="width:{w}px;height:{h}px;object-fit:cover;border-radius:28px;'
            f'box-shadow:0 32px 64px -32px rgba(20,40,30,0.5)">')


def hero_phone(A, key, alt, w=640, h=800):
    return phones_framed(A, [(key, alt)], w, h, pad=56)


def big_numbers(d, sid, eb, title, stats, note, notes, visual=None, vis_w=0):
    """Dark results slide: big numbers, a note card, and an optional visual."""
    sts = ''.join(stat(n, l, dark=True, size=150) for n, l in stats)
    nt = (f'<div style="background:#1B3527;border:1px solid #2C4A39;border-radius:20px;padding:24px 28px">'
          f'<p style="font-size:28px;font-weight:400;line-height:1.4;color:{ON_DARK}">{e(note)}</p></div>') if note else ''
    tw = CW - (vis_w + 64 if visual else 0)
    left = (f'<div style="width:{tw}px;display:flex;flex-direction:column;gap:40px">'
            f'<div style="display:flex;flex-direction:column;gap:14px">{head(eb, title, dark=True)}</div>'
            f'<div style="display:flex;flex-direction:row;gap:56px;align-items:flex-start">{sts}</div>{nt}</div>')
    inner = f'<div style="display:flex;flex-direction:row;gap:64px;align-items:center;height:{CH}px">{left}{visual or ""}</div>'
    d.add(sid, inner, bg=DARK, color=ON_DARK, dark=True, notes=notes, pad=PAD, layout='display:flex;flex-direction:column')


def tiles_grid(d, sid, blocks, tiles, cols=3, text_w=1500, limit=330):
    """Header text, then tiles (label, title, text) in a grid: the detailed deck's version of a table."""
    b2, _ = fit_blocks(blocks, text_w, limit)
    grid = ''.join(tile(*t) for t in tiles)
    d.add(sid, f'{text_col(b2, text_w)}<div style="display:grid;grid-template-columns:repeat({cols}, 1fr);gap:20px">{grid}</div>')


def number_cards(groups, num_size=88):
    """(number, title, detail) rows with a big accent number, for counts like research participants."""
    return ''.join(
        f'<div style="display:flex;flex-direction:row;gap:24px;align-items:center;background:{CARD};border:1px solid {RULE};border-radius:20px;padding:20px 28px">'
        f'<p style="font-family:{DISP};font-size:{num_size}px;{NSTYLE};line-height:0.9;color:{ACCENT};width:{int(num_size * 1.25)}px">{e(n)}</p>'
        f'<div style="flex:1;display:flex;flex-direction:column;gap:4px"><p style="font-size:32px;font-weight:600;color:{INK}">{e(g)}</p>'
        f'<p style="font-size:26px;font-weight:400;color:{BODY}">{e(m)}</p></div></div>' for n, g, m in groups)


def rows_slide(d, sid, blocks, rows, text_w=560, gap=56):
    """Header text on the left, (label, title, text) rows on the right: a table, set as containers."""
    rw = CW - text_w - gap
    b2, _ = fit_blocks(blocks, text_w, CH)
    rws = ''.join(
        f'<div style="display:flex;flex-direction:row;gap:24px;align-items:flex-start;background:{CARD};border:1px solid {RULE};border-radius:18px;padding:18px 24px">'
        f'<div style="width:300px;display:flex;flex-direction:column;gap:4px">'
        f'<p style="font-size:24px;font-weight:600;letter-spacing:1px;text-transform:uppercase;color:{ACCENT}">{e(l)}</p>'
        f'<p style="font-size:26px;font-weight:600;line-height:1.25;color:{INK}">{e(t)}</p></div>'
        f'<p style="flex:1;font-size:24px;font-weight:400;line-height:1.4;color:{BODY}">{e(x)}</p></div>' for l, t, x in rows)
    d.add(sid, f'<div style="display:flex;flex-direction:row;gap:{gap}px;align-items:center;height:{CH}px">{text_col(b2, text_w)}'
          f'<div style="width:{rw}px;display:flex;flex-direction:column;gap:12px">{rws}</div></div>', pad=PAD, layout='display:flex;flex-direction:column')
