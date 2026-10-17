"""Build the localised Sogang Podcasts case pages and wire them into the site.

    python3 build.py de zh-hans zh-hant        (any subset; each needs a finished <lang>.json)

For each language:
  1. public/<lang>/podcast.html: the English page's content with every string from <lang>.json put back in place
     (same walk as extract.py), inside the head and nav shell of that language's evn.html.
  2. Side Projects added to the menu and card stack of every page in public/<lang>/ (idempotent).
  3. The Side projects section added to public/<lang>/index.html (idempotent).
Then the language switcher and hreflang links on all podcast pages are pointed at the languages that exist.
The worker's language redirect is updated separately (src/worker.js).
"""
import json, re, sys
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString

HERE = Path(__file__).resolve().parent
import os
PUB = Path(os.environ.get("PUB") or HERE.parents[1] / "public")
sys.path.insert(0, str(HERE))
from extract import items  # noqa: E402

ALL = ["en", "de", "ko", "zh-hans", "zh-hant"]
HREFLANG = {"en": "en", "de": "de", "ko": "ko", "zh-hans": "zh-Hans", "zh-hant": "zh-Hant"}


def built():
    return ["en"] + [l for l in ALL[1:] if (PUB / l / "podcast.html").exists()]


def page_body(lang, tr):
    soup = BeautifulSoup((PUB / "podcast.html").read_text(encoding="utf-8"), "html.parser")
    src = json.loads((HERE / "source.json").read_text(encoding="utf-8"))
    ids = [r["id"] for r in src if r["kind"] != "extra"]
    found = items(soup)
    assert len(found) == len(ids), (len(found), len(ids))
    for (kind, node, en), i in zip(found, ids):
        v = tr[i]
        if kind == "text":
            raw = str(node); lead = raw[: len(raw) - len(raw.lstrip())]; tail = raw[len(raw.rstrip()):]
            node.replace_with(NavigableString(lead + v + tail))
        elif kind == "html":
            node.clear()
            for c in list(BeautifulSoup(v, "html.parser").contents):
                node.append(c)
        else:
            node[kind.split(":", 1)[1]] = v
    html = str(soup)
    body = html[html.index("<!-- ============ Case hero"): html.index("</body>")]
    style = html[html.index("<style>"): html.index("</style>") + len("</style>")]
    body = re.sub(r'(src|poster|href)="(assets/|Mancini_Tan_Resume\.pdf|site\.js)', r'\1="../\2', body)
    if lang == "de":
        body = body.replace("2,400+", "2.400+")
    return body, style


def menu_patch(html, tr):
    if 'data-cat="side"' in html:
        return html
    m = re.search(r'<div class="cases" data-for="ecom"><div>.*?</div></div>', html, re.S)
    assert m, "menu anchor"
    add = (f'<button class="cat" data-cat="side">{tr["menu.cat"]} <small>1</small></button>'
           f'<div class="cases" data-for="side"><div><a href="podcast.html">{tr["menu.link"]}</a></div></div>')
    html = html[: m.end()] + add + html[m.end():]
    m = re.search(r'<a class="scard" data-cat="ecom"[^>]*>.*?</a>', html, re.S)
    assert m, "stack anchor"
    card = (f'\n<a class="scard" data-cat="side" href="podcast.html"><div><b>{tr["page.title"]}</b><span>{tr["card.sub"]}</span></div>'
            f'<div class="thumb"><img alt="" height="52" src="../assets/logo-podcast.png" width="52"/></div></a>')
    return html[: m.end()] + card + html[m.end():]


def home_patch(html, tr):
    if 'id="side"' in html:
        return html
    en = (PUB / "index.html").read_text(encoding="utf-8")
    css = en[en.index("  /* ---------- Side projects ---------- */"): en.index("  .about { display: grid;")]
    anchor = "  .about { display: grid; grid-template-columns: repeat(12, 1fr); gap: var(--gap); }"
    assert anchor in html
    html = html.replace(anchor, css + anchor)
    sec = en[en.index('  <section class="panel side" id="side">'): en.index('  <section class="about" id="about">')]
    sec = re.sub(r'(src|poster)="assets/', r'\1="../assets/', sec)
    rep = {
        '<span>Side projects</span>': f'<span>{tr["home.label"]}</span>',
        '<h3>Turning flashcards into a podcast</h3>': f'<h3>{tr["page.title"]}</h3>',
        'A Korean listening podcast written from my class syllabus, voiced with AI and played in a web app built for shadowing.': tr["home.desc"],
        '<span class="tag">AI voice design</span>': f'<span class="tag">{tr["home.tag1"]}</span>',
        '<span class="tag">Localization</span>': f'<span class="tag">{tr["home.tag2"]}</span>',
        '<span class="tag">Web app</span>': f'<span class="tag">{tr["home.tag3"]}</span>',
        '<span>episodes from 2,400+ flashcards</span>': f'<span>{tr["home.stat1"]}</span>',
        '<span>subtitle languages</span>': f'<span>{tr["home.stat2"]}</span>',
        '</i>Read the case</span>': f'</i>{tr["home.more"]}</span>',
        'An episode of Sogang Podcasts playing, then a tap on a grammar point opens its card': tr["home.video"],
        '>Oct 2026<': '>' + tr.get("p017", "Oct 2026") + '<',
    }
    for a, b in rep.items():
        assert a in sec, a
        sec = sec.replace(a, b)
    anchor = '<section class="about" id="about">'
    i = html.index(anchor); i = html.rindex("\n", 0, i) + 1
    html = html[:i] + sec + html[i:]
    js = en[en.index("<script>\n/* Side project demo"): en.index("</script>\n</body>") + len("</script>\n")]
    i = html.rindex("</body>")
    return html[:i] + js + html[i:]


def build(lang):
    tr = json.loads((HERE / f"{lang}.json").read_text(encoding="utf-8"))
    shell = (PUB / lang / "evn.html").read_text(encoding="utf-8")
    body, style = page_body(lang, tr)
    head = shell[: shell.index("<!-- ============ Case hero")]
    head = head[: head.index("<style>")] + style + head[head.index("</style>") + len("</style>"):]
    head = re.sub(r"<title>[^<]*·\s*([^<]*)</title>", lambda m: f"<title>{tr['page.title']} · {m.group(1)}</title>", head)
    out = head + body + "</body>\n</html>\n"
    out = menu_patch(out, tr)
    (PUB / lang / "podcast.html").write_text(out, encoding="utf-8")
    for f in sorted((PUB / lang).glob("*.html")):
        s = f.read_text(encoding="utf-8"); n = menu_patch(s, tr)
        if f.name == "index.html":
            n = home_patch(n, tr)
        if n != s:
            f.write_text(n, encoding="utf-8")
    print(lang, "built")


def relink():
    have = built()
    for lang in have:
        f = PUB / ("podcast.html" if lang == "en" else f"{lang}/podcast.html")
        s = f.read_text(encoding="utf-8")
        for l in ALL:
            want = ("/podcast.html" if l == "en" else f"/{l}/podcast.html") if l in have else ("/index.html" if l == "en" else f"/{l}/index.html")
            s = re.sub(rf'href="/(?:{l}/)?(?:evn|podcast|index)\.html"(?= hreflang="{HREFLANG[l]}")' if l != "en" else r'href="/(?:evn|podcast|index)\.html"(?= hreflang="en")', f'href="{want}"', s)
        s = re.sub(r'<link rel="alternate" hreflang="[^"]+" href="https://mancinitan\.com/[^"]*">\n?', "", s)
        alts = "".join(f'<link rel="alternate" hreflang="{HREFLANG[l]}" href="https://mancinitan.com/{"" if l == "en" else l + "/"}podcast.html">\n' for l in have)
        alts += '<link rel="alternate" hreflang="x-default" href="https://mancinitan.com/podcast.html">\n'
        s = s.replace("</head>", alts + "</head>", 1)
        f.write_text(s, encoding="utf-8")
    print("relinked:", have)


if __name__ == "__main__":
    for lang in sys.argv[1:]:
        build(lang)
    relink()
