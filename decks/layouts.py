from kit import *

CONTENT_H = 792   # 1080 - 128 top - 160 bottom
FULL_W = 1664

def cover(d, sid, title, sub, small, portrait, notes=None):
    inner = (f'<div style="position:absolute;left:0;top:0;width:1920px;height:1080px;background:radial-gradient(circle at 18% 20%, #2B6E4C, {DARK} 60%)"></div>'
             f'<img src="{portrait}" alt="Portrait of Mancini Tan" style="position:absolute;right:128px;top:160px;width:560px;height:760px;object-fit:cover;border-radius:28px">'
             f'<div style="position:absolute;left:128px;top:160px;width:1000px;display:flex;flex-direction:column;gap:36px">'
             f'{eyebrow(small, True)}'
             f'<h1 style="font-family:{DISP};font-size:200px;{DSTYLE};line-height:0.92;text-transform:uppercase;color:{ON_DARK};letter-spacing:-2px">{e(title)}</h1>'
             f'<p style="font-size:44px;line-height:1.25;color:{ON_DARK_BODY};width:900px">{e(sub)}</p></div>')
    d.add(sid, inner, bg=DARK, color=ON_DARK, notes=notes, dark=True, footer=False, layout='display:flex', pad='128px')

def about(d, sid, head, body, facts, notes=None):
    cards = ''.join(tile(k, None, v) for k, v in facts)
    inner = (f'{eyebrow("About")}'
             f'<h2 style="font-family:{DISP};font-size:104px;{DSTYLE};line-height:0.98;text-transform:uppercase;color:{INK};width:1500px">{e(head)}</h2>'
             f'{para(body, size=32)}'
             f'<div style="display:flex;flex-direction:row;gap:24px">{cards}</div>')
    d.add(sid, inner, notes=notes)

def three_cards(d, sid, eb, head, cards, notes=None, bg=LIGHT):
    row = ''.join(tile(None, t, x) for t, x in cards)
    inner = f'{eyebrow(eb)}{h2(head)}<div style="display:flex;flex-direction:row;gap:24px;flex:1;align-items:stretch">{row}</div>'
    d.add(sid, inner, notes=notes, bg=bg)

def contents(d, sid, rows, notes=None, head='Case studies'):
    trs = ''.join(
        f'<tr><td style="color:{ACCENT};font-weight:600">{e(n)}</td><td style="color:{INK};font-weight:600">{e(t)}</td>'
        f'<td style="color:{BODY}">{e(c)}</td><td style="color:{MUTED}">{e(k)}</td></tr>' for n, t, c, k in rows)
    table = (f'<table style="font-size:28px;font-family:{BODYF};padding:16px">'
             f'<tr><th style="width:8%;color:{MUTED}">No.</th><th style="width:42%;color:{MUTED}">Case</th>'
             f'<th style="width:24%;color:{MUTED}">Company</th><th style="width:26%;color:{MUTED}">Skills</th></tr>{trs}</table>')
    d.add(sid, f'{eyebrow("Contents")}{h2(head)}{table}', notes=notes)

def case_title(d, sid, no, title, lede, meta, stats, visual, note=None, notes=None, lede_size=26):
    metas = ''.join(f'<div style="display:flex;flex-direction:column;gap:4px;flex:1"><p style="font-size:24px;color:{MUTED}">{e(k)}</p>'
                    f'<p style="font-size:24px;color:{INK};line-height:1.35">{e(v)}</p></div>' for k, v in meta)
    sts = ''.join(stat(n, l, size=80, small=True) for n, l in stats)
    nt = f'<p style="font-size:24px;color:{MUTED}">{e(note)}</p>' if note else ''
    left = (f'<div style="width:1080px;display:flex;flex-direction:column;gap:22px">'
            f'{eyebrow(no)}'
            f'<h1 style="font-family:{DISP};font-size:96px;{DSTYLE};line-height:0.95;text-transform:uppercase;color:{INK};letter-spacing:-1px">{e(title)}</h1>'
            f'<p style="font-size:{lede_size}px;line-height:1.42;color:{BODY}">{e(lede)}</p>'
            f'<div style="display:flex;flex-direction:row;gap:24px;border-top:1px solid {RULE};padding:16px 0 0 0">{metas}</div>'
            f'<div style="display:flex;flex-direction:row;gap:40px">{sts}</div>{nt}</div>')
    inner = f'<div style="display:flex;flex-direction:row;gap:56px;align-items:center">{left}{visual}</div>'
    d.add(sid, inner, bg=f'linear-gradient(135deg, {MINT} 0%, {LIGHT} 55%, {BUTTER} 100%)', notes=notes, layout='display:flex;flex-direction:column;justify-content:center', pad='96px 128px 140px')

def chapter(d, sid, no, title, intro, tags, notes=None):
    tg = ''.join(f'<p style="font-size:24px;color:{ON_DARK};background:#24432F;padding:10px 22px;border-radius:999px">{e(t)}</p>' for t in tags)
    inner = (f'<p style="font-family:{DISP};font-size:220px;{DSTYLE};line-height:0.9;color:#2F5E44">{e(no)}</p>'
             f'<h1 style="font-family:{DISP};font-size:112px;{DSTYLE};line-height:0.95;text-transform:uppercase;color:{ON_DARK};width:1500px">{e(title)}</h1>'
             f'<p style="font-size:36px;line-height:1.4;color:{ON_DARK_BODY};width:1300px">{e(intro)}</p>'
             f'<div style="display:flex;flex-direction:row;gap:16px">{tg}</div>')
    d.add(sid, inner, bg=DARK, color=ON_DARK, dark=True, notes=notes, layout='display:flex;flex-direction:column;justify-content:center;gap:28px')

def side(d, sid, blocks, visual, vis_w, notes=None, bg=LIGHT, text_w=None):
    tw = text_w or (FULL_W - vis_w - 72)
    b2, hgt = fit_blocks(blocks, tw, CONTENT_H)
    inner = (f'<div style="display:flex;flex-direction:row;gap:72px;align-items:flex-start">'
             f'{text_col(b2, tw)}<div style="width:{vis_w}px;display:flex;flex-direction:column;align-items:center;justify-content:center">{visual}</div></div>')
    d.add(sid, inner, notes=notes, bg=bg)
    return hgt

def stack(d, sid, blocks, visual, notes=None, bg=LIGHT, text_w=1400):
    b2, _ = fit_blocks(blocks, text_w, 400)
    inner = f'{text_col(b2, text_w)}<div style="display:flex;flex-direction:row;justify-content:flex-start">{visual}</div>'
    d.add(sid, inner, notes=notes, bg=bg)

def text_only(d, sid, blocks, notes=None, bg=LIGHT, width=1240):
    b2, _ = fit_blocks(blocks, width, CONTENT_H)
    d.add(sid, text_col(b2, width), notes=notes, bg=bg)

def tiles_slide(d, sid, blocks, tiles, notes=None, bg=LIGHT, text_w=1300):
    b2, _ = fit_blocks(blocks, text_w, 420)
    row = ''.join(tile(*t) for t in tiles)
    inner = f'{text_col(b2, text_w)}<div style="display:flex;flex-direction:row;gap:24px;align-items:stretch">{row}</div>'
    d.add(sid, inner, notes=notes, bg=bg)

def big_statement(d, sid, text, sub=None, notes=None):
    s = f'<p style="font-size:32px;line-height:1.45;color:{ON_DARK_BODY};width:1300px">{e(sub)}</p>' if sub else ''
    inner = (f'<p style="font-family:{DISP};font-size:96px;{DSTYLE};line-height:1.02;color:{ON_DARK};width:1560px">{e(text)}</p>{s}')
    d.add(sid, inner, bg=ACCENT, color=ON_DARK, dark=True, notes=notes, layout='display:flex;flex-direction:column;justify-content:center;gap:40px')

def table_slide(d, sid, blocks, head, rows, widths, notes=None, size=26):
    b2, _ = fit_blocks(blocks, 1500, 330)
    th = ''.join(f'<th style="width:{w}%;color:{MUTED}">{e(h)}</th>' for h, w in zip(head, widths))
    trs = ''.join('<tr>' + ''.join(f'<td style="color:{INK if i == 0 else BODY}">{e(c)}</td>' for i, c in enumerate(r)) + '</tr>' for r in rows)
    table = f'<table style="font-size:{size}px;font-family:{BODYF};padding:14px"><tr>{th}</tr>{trs}</table>'
    d.add(sid, f'{text_col(b2, 1500)}{table}', notes=notes)

def stats_slide(d, sid, eb, head, stats, note=None, notes=None, dark=True):
    sts = ''.join(stat(n, l, dark=dark, size=140) for n, l in stats)
    nt = f'<p style="font-size:24px;color:{ON_DARK_BODY if dark else MUTED}">{e(note)}</p>' if note else ''
    inner = f'{eyebrow(eb, dark)}{h2(head, dark)}<div style="display:flex;flex-direction:row;gap:56px;align-items:flex-start;padding:40px 0 0 0">{sts}</div>{nt}'
    d.add(sid, inner, bg=DARK if dark else LIGHT, color=ON_DARK if dark else INK, dark=dark, notes=notes)

def closing(d, sid, head, lines_, notes=None):
    ls = ''.join(f'<p style="font-size:36px;color:{ON_DARK_BODY}">{e(x)}</p>' for x in lines_)
    inner = (f'<h1 style="font-family:{DISP};font-size:120px;{DSTYLE};line-height:0.95;text-transform:uppercase;color:{ON_DARK};width:1660px">{e(head)}</h1>'
             f'<div style="display:flex;flex-direction:column;gap:12px">{ls}</div>')
    d.add(sid, inner, bg=f'radial-gradient(circle at 80% 20%, #2B6E4C, {DARK} 60%)', color=ON_DARK, dark=True, notes=notes,
          layout='display:flex;flex-direction:column;justify-content:center;gap:56px', footer=False, pad='128px')

def wide(src, alt, w, h):
    return img(src, alt, w, h, 'contain', 18, CARD)

def handover_row(steps):
    """steps: (who, what). A simple left-to-right chain of boxes with arrows."""
    parts = []
    for i, (who, what) in enumerate(steps):
        if i: parts.append(f'<x-shape kind="arrow-right" style="width:56px;height:28px;background:{ACCENT}"></x-shape>')
        parts.append(f'<div style="flex:1;display:flex;flex-direction:column;gap:8px;background:{CARD};border:1px solid {RULE};border-radius:18px;padding:24px">'
                     f'<p style="font-size:24px;font-weight:600;color:{ACCENT}">{e(str(i + 1))}</p>'
                     f'<p style="font-size:26px;font-weight:600;color:{INK};line-height:1.25">{e(what)}</p>'
                     f'<p style="font-size:24px;color:{MUTED}">{e(who)}</p></div>')
    return f'<div style="display:flex;flex-direction:row;gap:16px;align-items:center">{"".join(parts)}</div>'
