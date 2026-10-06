"""Local preview of deck slides: renders each slide file at 1920x1080 and saves a contact sheet + overflow report."""
import sys, os, json, re
sys.path.insert(0, os.path.dirname(__file__))
from assets import DETAILED, PRESENT
from playwright.sync_api import sync_playwright
from PIL import Image

root, which = sys.argv[1], sys.argv[2]
only = sys.argv[3].split(',') if len(sys.argv) > 3 else None
amap = DETAILED if which == 'detailed' else PRESENT
rev = {v: (f'/home/claude/portfolio-site/decks/media/{k}.jpg' if k.startswith('m-') else f'/home/claude/portfolio-site/public/assets/{k}.jpg') for k, v in amap.items()}
F = '/tmp/claude-0/-home-claude-portfolio-site/c6dd3ada-264e-5647-a533-99a859b02f2c/scratchpad/chk/node_modules/@fontsource'
VF = '/tmp/claude-0/-home-claude-portfolio-site/c6dd3ada-264e-5647-a533-99a859b02f2c/scratchpad/chk/node_modules/@fontsource-variable/archivo/files'
css = "@font-face{font-family:'Archivo Condensed';font-weight:900;src:url(file:///tmp/claude-0/-home-claude-portfolio-site/c6dd3ada-264e-5647-a533-99a859b02f2c/scratchpad/fonts/ArchivoCondensed-Black.woff2)}" + ''.join(f"@font-face{{font-family:'Archivo';font-style:normal;font-weight:100 900;font-stretch:62% 125%;src:url(file://{VF}/archivo-{s}-wdth-normal.woff2)}}" for s in ('latin', 'latin-ext'))
idx = json.load(open(f'{root}/project/deck.json'))
order = [s for s in idx['order'] if not only or s in only]
out = f'{root}/_preview'; os.makedirs(out, exist_ok=True)
report = []
with sync_playwright() as pw:
    b = pw.chromium.launch(); pg = b.new_page(viewport={'width': 1920, 'height': 1080})
    for sid in order:
        h = open(f'{root}/project/slides/{sid}.html').read()
        for k, v in rev.items(): h = h.replace(k, 'file://' + v)
        h = re.sub(r'<aside>.*?</aside>', '', h, flags=re.S)
        h = h.replace('<x-shape', '<div data-x').replace('</x-shape>', '</div>')
        doc = (f'<!doctype html><html><head><style>{css} *{{box-sizing:border-box;margin:0}} section{{position:relative;width:1920px;height:1080px;overflow:hidden}}'
               f' table{{border-collapse:collapse;width:100%}} td,th{{border-bottom:1px solid #D3DDD2;text-align:left;vertical-align:top}} div[data-x]{{clip-path:polygon(0 30%,60% 30%,60% 0,100% 50%,60% 100%,60% 70%,0 70%)}}</style></head><body>{h}</body></html>')
        open(f'{out}/_tmp.html','w').write(doc); pg.goto('file://'+os.path.abspath(f'{out}/_tmp.html')); pg.wait_for_timeout(300)
        over = pg.evaluate("""() => { const s = document.querySelector('section'); const R = s.getBoundingClientRect(); const bad = [];
          s.querySelectorAll('h1,h2,h3,p,img,table,div').forEach(el => { const r = el.getBoundingClientRect(); if (!r.width) return;
            if (r.bottom > 952 + 1 && !(el.tagName==='P' && Math.round(r.top) >= 940)) bad.push([el.tagName, Math.round(r.bottom), (el.textContent||el.alt||'').slice(0,40)]);
            if (r.right > 1792 + 1) bad.push([el.tagName, 'right', Math.round(r.right), (el.textContent||el.alt||'').slice(0,40)]); });
          return bad.slice(0, 4); }""")
        if over: report.append((sid, over))
        pg.screenshot(path=f'{out}/{sid}.png')
    b.close()
ims = [Image.open(f'{out}/{s}.png').resize((480, 270)) for s in order]
cols = 4; rows = (len(ims) + cols - 1) // cols
sheet = Image.new('RGB', (cols * 490, rows * 280), 'white')
for i, im in enumerate(ims): sheet.paste(im, ((i % cols) * 490, (i // cols) * 280))
sheet.save(f'{out}/_sheet.png')
for r in report: print(r)
print('rendered', len(order))
