# Translation brief: Sogang Podcasts case (mancinitan.com/podcast.html)

You are translating one case study on Mancini Tan's portfolio into **German (de), Korean (ko), Simplified Chinese (zh-hans) and Traditional Chinese (zh-hant)**. The other pages of the site are already translated; read one of them in each language first to match the voice:

- `evn_de.html`, `evn_ko.html`, `evn_zh-hans.html`, `evn_zh-hant.html` (in this folder)
- The English source page is `podcast.html` (in this folder), so you can see where every string sits.

## Files

| File | What it is |
|---|---|
| `source.json` | Every string to translate: `id`, `en`, and `where` (section › element) or a note for the strings outside the page |
| `glossary.json` | `locked`: strings already used on the site, which must stay word for word. `keep_as_is`: names that are never translated |
| `de.json`, `ko.json`, `zh-hans.json`, `zh-hant.json` | Your output. Each maps `id` → translation. Locked strings are already filled in; fill every empty `""` |
| `check.py` | Run `python3 check.py` (or `python3 check.py ko`) and fix every ERROR. Read the WARNs and fix the real ones |

Only edit the four language files. Don't touch `source.json`, `glossary.json`, the scripts or the reference pages.

## Voice

The page is written in Mancini's own voice: first person, conversational, like talking to a colleague. Simple, polite and confident, with a little dry humour kept under control (for example "Then the maths caught up with me"). Recruiters read it on their phones, so it should be easy to scan. Translate the meaning and tone, not the sentence structure.

| Language | How it should read |
|---|---|
| German | Natural, modern German as on the existing German pages: first person (ich), plain and direct, no stiff nominal style. Avoid addressing the reader directly; where it can't be avoided (the closing CTA), phrase it impersonally as the existing pages do ("Machen wir das Ja-Sagen leichter"). Tech words German workplaces use stay English (Web-App, Podcast, Shadowing) |
| Korean | 해요체 throughout, first person 저/제, like the existing Korean pages. Rhythm of Samsung and Toss product copy. Mancini's name in Korean is 만치니 |
| Simplified Chinese | Short, punchy matched pairs in the style of OPPO and Huawei product pages; case-study wording in the style of ZCOOL case studies. Big headings and the large lead lines (`p.big-p`, `h2`) don't end with 。. Avoid English words unless the English term is what Chinese workplaces actually use (App, UI, UX, AI are fine). Mancini's Chinese name is 陈奕豪, 奕豪 in first person where a name is needed |
| Traditional Chinese | Taiwan usage, written as its own translation, not a character conversion of the Simplified (the site already differs: 所有作品 vs 全部作品, 聯絡 vs 联系, 履歷 vs 简历, 在地化 vs 本地化). Same punchy style |

## Hard rules

1. **No em dashes (—)** anywhere. Rephrase instead.
2. **No "it's not X, it's Y" constructions** (antithesis); they read as machine-written.
3. **Keep every HTML tag** in a string exactly as in the English, in the same order. Some strings contain `<span lang="ko">똑바로</span>` or `<b>…</b>`; translate around them and leave the Korean inside the span untouched.
4. **Korean terms stay in Hangul in every language**: 반말, 합쇼체, 장면, 해설, 복습, 똑바로, 똑까로, 똑빠로, 했어야지요.
5. **Names stay in Latin letters**: Sogang Podcasts, Claude, Gemini 3.8, ElevenLabs, NotebookLM, Anki, GitHub Pages, Whisper. "Sogang" may be 서강 in Korean only where it refers to the school or the books (e.g. "Sogang book" → 서강 교재), never in the product name Sogang Podcasts.
6. **Numbers stay as they are** (67, 2,400+, 330,000, 10, 0.7× to 1.2×). Use each language's normal number formatting (German: 2.400+, 330.000).
7. **Short labels stay short.** `home.more` ("Read the case") and `menu.cat` ("Side Projects") must be 4 characters or fewer in Korean and Chinese. Tag pills (`span.tile-k`, `span.who`, `home.tag*`) should be 1–3 words.
8. **Locked strings** in `glossary.json` are prefilled. Don't change them.
9. Where the English says "Localization" as a skill (`home.tag2`), use the site's existing word: Lokalisierung, 현지화, 本地化, 在地化.
10. The sample Anki card on the page is product UI and stays in English, so its text isn't in `source.json`.
11. `p…` strings that are screen-reader labels (`attr:aria-label`) and image descriptions (`attr:alt`) are translated too; keep them plain and descriptive.

## Terms

| English | Meaning here | Notes |
|---|---|---|
| shadowing | repeating speech right after hearing it, to train pronunciation and rhythm | 쉐도잉 (Korean), 跟读 (Chinese), Shadowing (German) |
| flashcards / cards | Mancini's Anki flashcards | 플래시카드 / 카드, 记忆卡 / 卡片, Karteikarten / Karten |
| syllabus | the Sogang Korean course books, Levels 3 and 4 | 교재 / 커리큘럼, 课程 / 教材, Lehrplan / Kursbücher |
| scene, breakdown, recap | the three parts of every episode (장면, 해설, 복습) | the Korean labels stay; translate the English words beside them |
| side project | a personal project outside work | 사이드 프로젝트, 个人项目, 個人專案, Nebenprojekt |
| free tier | the free usage level of Gemini's API | 무료 티어 / 무료 요금제, 免费额度, 免費額度, Gratis-Kontingent |
| voice direction | casting and directing the AI voices | 보이스 디렉팅, 声音导演 / 配音指导, 配音指導, Stimmregie |
| nasalisation, palatalisation, tensing | Korean sound changes (비음화, 구개음화, 경음화) | Korean: use these Korean terms. Chinese: 鼻音化, 腭化 / 顎化, 紧音化 / 緊音化. German: Nasalierung, Palatalisierung, Verhärtung (Tensierung) |
| "handbag" → "hambag" | an English example of a sound change | Swap in a natural example from the target language if one exists (German: "Bahnhof" is fine to keep English); keep it short |
| speech-to-text | transcribing audio into text | 음성 인식 (STT), 语音转文字, 語音轉文字, Spracherkennung |

## When you're done

1. Run `python3 check.py` until it shows `0 errors` for all four languages.
2. Leave the four files in this folder. Claude builds the pages from them.
3. List any lines you weren't sure about (id + a short reason) in your final reply.
