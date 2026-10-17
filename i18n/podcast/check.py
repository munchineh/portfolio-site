"""Check a translation file against source.json and the brief's hard rules.

    python3 check.py de        (or ko, zh-hans, zh-hant, or no argument for all four)

Prints one line per problem, then a summary line. Exit code 1 if there are errors.
"""
import json, re, sys
from pathlib import Path

HERE = Path(__file__).parent
SRC = json.loads((HERE / "source.json").read_text(encoding="utf-8"))
GLOSS = json.loads((HERE / "glossary.json").read_text(encoding="utf-8"))
LANGS = ["de", "ko", "zh-hans", "zh-hant"]
CJK_SHORT = {"home.more"}          # 4 characters or fewer in zh / ko (buttons and the menu category)
TAG = re.compile(r"</?[a-z][^>]*>")
HANGUL_SPAN = re.compile(r'<span lang="ko">([^<]*)</span>')


def check(lang):
    errs, warns = [], []
    path = HERE / f"{lang}.json"
    if not path.exists():
        return [f"{lang}: {path.name} is missing"], []
    tr = json.loads(path.read_text(encoding="utf-8"))
    locked = GLOSS["locked"][lang]
    for r in SRC:
        i, en = r["id"], r["en"]
        v = tr.get(i)
        if v is None:
            errs.append(f"{i}: missing"); continue
        if not v.strip():
            errs.append(f"{i}: empty"); continue
        if en in locked and v != locked[en]:
            errs.append(f"{i}: locked string changed, must be {locked[en]!r}")
        if en in GLOSS["keep_as_is"] and v != en:
            errs.append(f"{i}: must stay {en!r}")
        if [t for t in TAG.findall(en)] != [t for t in TAG.findall(v)]:
            errs.append(f"{i}: HTML tags differ from the English (keep every tag, in the same order)")
        if HANGUL_SPAN.findall(en) != HANGUL_SPAN.findall(v):
            errs.append(f"{i}: Korean inside <span lang=\"ko\"> must stay exactly as in the English")
        if "—" in v:
            errs.append(f"{i}: em dash (—) is not allowed; rephrase")
        if lang != "de" and re.search(r"\b(the|and|with|your|my)\b", re.sub(r"<[^>]+>", "", v)):
            warns.append(f"{i}: looks like English was left in")
        if lang in ("ko", "zh-hans", "zh-hant") and i in CJK_SHORT and len(re.sub(r"\s", "", v)) > 4:
            errs.append(f"{i}: must be 4 characters or fewer, got {v!r}")
        for name in ("Claude", "Gemini", "ElevenLabs", "NotebookLM", "Anki", "GitHub"):
            if name in en and name not in v:
                warns.append(f"{i}: {name} should stay in Latin letters")
        if lang == "zh-hant" and re.search(r"[们这为说时会来过个么还对发开关题后头]", v):
            warns.append(f"{i}: possible Simplified characters in Traditional")
        if lang == "zh-hans" and re.search(r"[們這為說時會來過個麼還對發開關題後頭]", v):
            warns.append(f"{i}: possible Traditional characters in Simplified")
    extra = set(tr) - {r["id"] for r in SRC}
    for i in sorted(extra):
        warns.append(f"{i}: not in source.json (ignored)")
    return errs, warns


if __name__ == "__main__":
    bad = 0
    for lang in (sys.argv[1:] or LANGS):
        errs, warns = check(lang)
        for e in errs: print(f"ERROR {lang} {e}")
        for w in warns: print(f"WARN  {lang} {w}")
        print(f"{lang}: {len(errs)} errors, {len(warns)} warnings")
        bad += len(errs)
    sys.exit(1 if bad else 0)
