Paste this into Antigravity, with this folder open:

---

Translate the strings in this folder into German, Korean, Simplified Chinese and Traditional Chinese for my portfolio site.

1. Read BRIEF.md first and follow it exactly. It has the voice, the hard rules and the terms.
2. source.json has every English string with where it appears. glossary.json has strings that are already fixed.
3. Fill every empty "" in de.json, ko.json, zh-hans.json and zh-hant.json. Don't change the prefilled values or any other file.
4. Write Traditional Chinese as its own Taiwan-usage translation, not a conversion of the Simplified.
5. Run `python3 check.py` and fix every ERROR, and any WARN that's a real problem, until all four show 0 errors.
6. Reply with the final checker summary and a short list of any lines you weren't sure about (id + reason).

The English page itself is in the pack as podcast.html (reference only), and evn_<lang>.html are existing pages in each language to match the voice.
