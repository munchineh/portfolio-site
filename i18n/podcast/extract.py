"""Pull every translatable string out of public/podcast.html (plus the home section, menu and card strings)
into source.json. The same walk is used by build.py to put translations back, so the order of strings is the key.

Rules for what counts as one string:
- the innermost element holding text, keeping Korean inline spans (<span lang="ko">) inside it as HTML;
- an element that also holds an icon (<svg>) contributes only its own text, so the icon is never sent for translation;
- pure numbers and the native language names in the languages row are skipped;
- alt and aria-label attributes are strings too.
"""
import json, re, sys
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString, Comment

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "public" / "podcast.html"
INLINE = {"span"}          # only <span lang="ko"> is kept inline; checked below
SKIP_PARENTS = {"script", "style", "svg", "title"}


def is_inline_ko(el):
    return el.name in INLINE and el.get("lang") == "ko"


def body_region(soup):
    """Everything from the case hero to the footer, i.e. the page's own content (not the shared nav)."""
    return [el for el in soup.body.find_all(recursive=True) if el.get("data-i18n-root") is not None]


def walk(soup):
    """Yield (kind, node) in document order. kind: 'html' (element inner HTML), 'text' (one text node), 'attr:<name>'."""
    start = soup.find("section", class_="c-hero")
    stop = soup.find("footer")
    seen = set()
    el = start
    nodes = []
    # collect top-level siblings from the hero to the footer
    while el is not None and el is not stop:
        if getattr(el, "name", None):
            nodes.append(el)
        el = el.next_sibling
    for top in nodes:
        for d in [top] + list(top.find_all(True)):
            for a in ("alt", "aria-label"):
                if d.get(a):
                    yield (f"attr:{a}", d)
        for t in top.find_all(string=True):
            if isinstance(t, Comment) or not t.strip():
                continue
            if any(p.name in SKIP_PARENTS for p in t.parents):
                continue
            host = t.parent
            if is_inline_ko(host):
                host = host.parent
            # a bold lead-in inside a caption belongs to the caption's own sentence
            if host.name in ("b", "i", "em", "u") and any(isinstance(c, NavigableString) and c.strip() for c in host.parent.children):
                host = host.parent
            if host.find("svg") is not None or host.find(["div", "p", "figure", "ol", "li", "img", "video"]) is not None:
                key = ("text", id(t))
                if key in seen:
                    continue
                seen.add(key)
                yield ("text", t)
            else:
                key = ("html", id(host))
                if key in seen:
                    continue
                seen.add(key)
                yield ("html", host)


def skip(en, node):
    if re.fullmatch(r"[\d.,+%$×\s]+", en):
        return True
    if re.fullmatch(r"[\uac00-\ud7a3\s]+", en):     # Korean-only labels (장면, 해설 …) stay as they are
        return True
    host = node if getattr(node, "name", None) else node.parent
    if host is not None and host.find_parent(class_="langs-row") is not None:
        return True
    # the Anki card mock is product UI, which stays in English on every language's page
    if host is not None and ("ankim" in (host.get("class") or []) or host.find_parent(class_="ankim") is not None):
        return True
    return False


def items(soup):
    out = []
    for kind, node in walk(soup):
        if kind == "text":
            en = str(node).strip()
        elif kind == "html":
            en = node.decode_contents().strip()
        else:
            en = node[kind.split(":", 1)[1]]
        if skip(re.sub(r"<[^>]+>", "", en), node):
            continue
        out.append((kind, node, en))
    return out


def context(node):
    host = node if getattr(node, "name", None) else node.parent
    sec = host.find_parent("section")
    sid = (sec.get("id") or " ".join(sec.get("class", []))) if sec else ""
    tag = host.name + ("." + ".".join(host.get("class", [])) if host.get("class") else "")
    return f"{sid} › {tag}"


# Strings outside podcast.html's own content: the page title, home section, menu and card stack
EXTRA = [
    ("page.title", "Turning flashcards into a podcast", "Browser tab title, before ' · Mancini Tan'. Same as the case title."),
    ("menu.cat", "Side Projects", "Menu category button, beside 'Product Design', 'E-Commerce'. Short."),
    ("menu.link", "Turning flashcards into a podcast · Sogang Podcasts", "Menu link: case title · project name. Keep 'Sogang Podcasts' as is."),
    ("card.sub", "Sogang Podcasts · Side project", "Small line under the title on the menu card. Keep 'Sogang Podcasts' as is."),
    ("home.label", "Side projects", "Small label at the top of the home page section."),
    ("home.desc", "A Korean listening podcast written from my class syllabus, voiced with AI and played in a web app built for shadowing.", "One-sentence description on the home page card."),
    ("home.tag1", "AI voice design", "Tag pill. Short."),
    ("home.tag2", "Localization", "Tag pill. Use the same word as the site's existing skills chip for Localization."),
    ("home.tag3", "Web app", "Tag pill. Short."),
    ("home.stat1", "episodes from 3,000+ flashcards", "Follows the number 89."),
    ("home.stat2", "subtitle languages", "Follows the number 11."),
    ("home.more", "Read the case", "Link text with an arrow icon. zh/ko: 4 characters or fewer."),
    ("home.video", "An episode of Sogang Podcasts playing, then a tap on a grammar point opens its card", "Screen-reader label for the home page video."),
]

if __name__ == "__main__":
    soup = BeautifulSoup(SRC.read_text(encoding="utf-8"), "html.parser")
    rows = []
    for n, (kind, node, en) in enumerate(items(soup), 1):
        rows.append({"id": f"p{n:03d}", "en": en, "kind": kind, "where": context(node if kind != 'text' else node)})
    for k, en, note in EXTRA:
        rows.append({"id": k, "en": en, "kind": "extra", "where": note})
    (Path(__file__).parent / "source.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    print(len(rows), "strings")
