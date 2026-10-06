"""Presenting deck: short like the website, with the extra numbers I can share in an interview, and a script on every slide.
Points sit in numbered cards (bold lead, one short line) and visuals take most of the slide, so it scans at a glance."""
import sys
from cards import *
from assets import PRESENT as A
from script import SCRIPT as S

ROOT = sys.argv[1]
d = Deck(ROOT, 'Mancini Tan · Interview presentation', 'Mancini Tan', condensed_src=CONDENSED_SRC['present'])

# Jargon notes go under each slide's script (speaker notes only, never on the slide)
from terms import notes_block
_add = d.add
def _add_with_terms(sid, inner, **kw):
    kw['notes'] = S[sid] + notes_block(sid)
    _add(sid, inner, **kw)
d.add = _add_with_terms

# ------------------------------------------------------------------ Intro
d.section('intro', 'Who I am and how I work.', '')
cover(d, 'cover', 'Mancini Tan', 'Product, content and conversation design', 'Portfolio · 2026', A['portrait'])

ABOUT_HEAD = "I design things people don't have to think about."
facts = [('Experience', '5+ years: DBS, Ninja Van, Neuron, OKX, Buildlr, plus my own store'),
         ('Industries', 'Fintech, logistics, e-commerce, construction tech, mobility'),
         ('Skills', 'UI, conversation and content design, localization'),
         ('Languages', 'English (native), Chinese (proficient), Korean and German (intermediate)')]
fact_cards = ''.join(
    f'<div style="flex:1;display:flex;flex-direction:column;gap:12px;background:{CARD};border:1px solid {RULE};border-radius:20px;padding:28px">'
    f'<p style="font-size:24px;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;color:{ACCENT}">{e(k)}</p>'
    f'<p style="font-size:30px;font-weight:400;line-height:1.3;color:{INK}">{e(v)}</p></div>' for k, v in facts)
d.add('about', f'{eyebrow("About")}'
      f'<h2 style="font-family:{DISP};font-size:112px;{DSTYLE};line-height:0.92;text-transform:uppercase;color:{INK};width:1500px">{e(ABOUT_HEAD)}</h2>'
      f'<p style="font-size:34px;font-weight:400;line-height:1.4;color:{BODY}">5+ years across fintech, logistics and e-commerce. Singaporean, based in Seoul, open to roles anywhere.</p>'
      f'<div style="display:flex;flex-direction:row;gap:20px;align-items:stretch">{fact_cards}</div>',
      pad=PAD, layout='display:flex;flex-direction:column;justify-content:center;gap:36px')

CONTENTS_HEAD = "Today's cases"
cases = [('01', 'Helping shoppers find their fit', 'EVN Archive', 'E-commerce, end to end'),
         ('02', 'An assistant that trades in chat', 'OKX', 'AI conversation design'),
         ('03', 'Making trading social', 'OKX · Orbit', 'Content design, growth'),
         ('04', 'Personalized content at scale', 'OKX · Crypto Rewind', 'Dynamic content'),
         ('05', 'Simplifying operational tools', 'Buildlr', 'SaaS, complex forms'),
         ('06', 'Service recovery at scale', 'Ninja Van', 'Research, service design'),
         ('07', 'Shift plans that stick', 'Neuron Mobility', 'Internal tools')]
rows = ''.join(
    f'<div style="display:flex;flex-direction:row;gap:28px;align-items:center;background:{CARD};border:1px solid {RULE};border-radius:18px;padding:16px 28px">'
    f'<p style="font-family:{DISP};font-size:44px;{DSTYLE};line-height:1;color:{ACCENT};width:56px">{n}</p>'
    f'<p style="flex:1;font-size:32px;font-weight:600;color:{INK}">{e(t)}</p>'
    f'<p style="width:330px;font-size:26px;font-weight:400;color:{BODY}">{e(c)}</p>'
    f'<p style="width:330px;font-size:26px;font-weight:400;color:{MUTED}">{e(k)}</p></div>' for n, t, c, k in cases)
d.add('contents', f'<div style="display:flex;flex-direction:column;gap:14px">{head("Contents", CONTENTS_HEAD)}</div>'
      f'<div style="display:flex;flex-direction:column;gap:12px">{rows}</div>',
      pad=PAD, layout='display:flex;flex-direction:column;gap:32px')

# ------------------------------------------------------------------ EVN
d.section('evn', 'EVN Archive: a sizing tool that lifted free-size sales 400%+.', 'EVN Archive')
case_hero(d, 'evn-title', 'Case 01 · E-commerce', 'Helping shoppers find their fit',
          'My own Shopify store for independent Korean menswear, designed and built end to end. This case covers the sizing tool that helps shoppers buy free size with confidence.',
          [('Role', 'Founder and designer'), ('Timeline', 'May 2026 to now'), ('Stack', 'Shopify, Liquid, CSS, JS'), ('Team', 'Just me')],
          [('400%+', 'increase in free-size sales'), ('4', "free-size sales in the tool's first week")],
          hero_img(A, 'm-h-evn', "The product page with How it'll fit you"), None)
media_slide(d, 'evn-problem', 'The problem and the idea', 'Hundreds of visits, almost no carts',
            [('No size chart to lean on', "Shoppers couldn't picture how free size would fit"),
             ('Height and weight in', "Compared with each garment's real measurements"),
             ('A plain-words answer', 'Snug, recommended or relaxed'),
             ('Zero upkeep', 'Reads the Size & Fit copy already on each page')],
            framed(A, 'm-evn-card', "How it'll fit you, on the product page", 900, 840, pad=56, radius=24), 900, None)

TOUCH_NOTE = 'Plus a 20% free-size offer and short videos on how free size fits, to get people past "it won\'t fit me".'
touch = [('Homepage', 'A Free Size Edit and a fit prompt', 'm-evn-t-home'),
         ('Fit profile', 'Height and weight first, saved once', 'm-evn-t-finder'),
         ('Collection', 'Filter to pieces that fit you', 'm-evn-t-coll'),
         ('Product page', 'A plain-words fit read', 'm-evn-t-pdp')]
tcards = ''.join(
    f'<div style="flex:1;display:flex;flex-direction:column;background:{CARD};border:1px solid {RULE};border-radius:20px;overflow:hidden">'
    f'<img src="{A[k]}" alt="{e(t)}" style="width:399px;height:299px;object-fit:cover">'
    f'<div style="display:flex;flex-direction:column;gap:6px;padding:22px 26px">'
    f'<p style="font-size:34px;font-weight:600;line-height:1.15;color:{INK}">{e(t)}</p>'
    f'<p style="font-size:26px;font-weight:400;line-height:1.35;color:{BODY}">{e(x)}</p></div></div>' for t, x, k in touch)
d.add('evn-touch', f'<div style="display:flex;flex-direction:column;gap:14px">{head("Touchpoints", "One recommendation, everywhere you shop")}</div>'
      f'<div style="display:flex;flex-direction:row;gap:22px;align-items:stretch">{tcards}</div>'
      f'<div style="background:{MINT};border-radius:20px;padding:26px 32px"><p style="font-size:30px;font-weight:500;line-height:1.35;color:{ACCENT}">'
      f'{e(TOUCH_NOTE)}</p></div>',
      pad=PAD, layout='display:flex;flex-direction:column;gap:32px')
media_slide(d, 'evn-store', 'Beyond the sizing tool', 'Owning the whole experience',
            [('Clear structure', 'A two-way taxonomy: Foundations and Statement'),
             ('Simple pricing', 'A few price tiers that read at a glance'),
             ('Data-led fixes', 'Funnel and session data on pages losing sales'),
             ('Close to customers', 'Localised for top markets, every email answered')],
            framed(A, 'm-evn-home3', 'The Free Size Edit on the homepage', 900, 600, pad=48), 900, None)

# ------------------------------------------------------------------ OKX overview
d.section('okx', 'OKX overview: three products that made crypto more social.', 'OKX')
case_hero(d, 'okx-title', 'Cases 02 to 04 · Fintech', 'Making crypto social',
          'Three products that made crypto more social: an AI assistant that trades in chat, Orbit, a social layer for traders, and Crypto Rewind, a personalised year in review.',
          [('Role', 'Senior content designer'), ('Timeline', 'Mar 2024 to Dec 2025'), ('Worked in', 'English and Mandarin'), ('Scope', 'Conversation, social, dynamic content')],
          [('3.26M', 'Crypto Rewind click-throughs, against a 1.5M goal'), ('200%', "growth in Orbit's daily active users")],
          hero_phone(A, 'okx-50k', 'Simple Buy at 50,000 USD'), None)

# ------------------------------------------------------------------ AI assistant
d.section('okx-ai', 'AI trading assistant: prompt design, guardrails and red-teaming.', 'OKX · AI assistant')
media_slide(d, 'ai-problem', '02 · AI conversation design', 'A personal desk for big trades',
            [('Simple Buy costs more', 'Worse than spot, which hurts on big orders'),
             ('Agents already did it better', 'Live chat in Greater China offered better rates'),
             ('AI takes it everywhere', 'Every market, from 50,000 USD up'),
             ('Humans stay in the loop', 'The team keeps the chats that need a person')],
            phones_framed(A, [('okx-50k', 'A better rate offered at 50,000 USD'), ('okx-sheet', 'The handover to chat')], 860, 840), 860, None)

layers = [('01', 'Persona', 'Senior trading consultant: assuring, "substantial" never "massive"'),
          ('02', 'Adaptive tone', 'Mirrors the user, from plain English to trader talk'),
          ('03', 'Guardrails', 'Confirm both sides, never assume a currency, market orders only'),
          ('04', 'Edge cases', 'Fearful language gets a calm, human register'),
          ('05', 'Few-shot examples', 'One worked example each: beginner, expert, distressed')]
lrows = ''.join(
    f'<div style="display:flex;flex-direction:row;gap:20px;align-items:flex-start;background:{CARD};border:1px solid {RULE};border-radius:18px;padding:20px 26px">'
    f'<p style="font-family:{DISP};font-size:44px;{DSTYLE};line-height:1;color:{ACCENT};width:52px">{n}</p>'
    f'<div style="flex:1;display:flex;flex-direction:column;gap:4px"><p style="font-size:32px;font-weight:600;line-height:1.15;color:{INK}">{e(t)}</p>'
    f'<p style="font-size:25px;font-weight:400;line-height:1.35;color:{BODY}">{e(x)}</p></div></div>' for n, t, x in layers)
d.add('ai-prompt', f'<div style="display:flex;flex-direction:row;gap:56px;align-items:center;height:{CH}px">'
      f'<div style="width:888px;display:flex;flex-direction:column;gap:24px"><div style="display:flex;flex-direction:column;gap:14px">{head("The system prompt", "Five layers, so the bot never improvises with money", size=48)}</div>'
      f'<div style="display:flex;flex-direction:column;gap:12px">{lrows}</div></div>'
      f'{framed(A, "m-okx-chat-v", "The assistant hands over an updated quote", 720, 840, pad=40, radius=18, bg="#0B0F0C")}</div>',
      pad=PAD, layout='display:flex;flex-direction:column')
big_numbers(d, 'ai-results', 'Testing', 'Benchmarked, then red-teamed',
            [('100%', 'persona consistency in testing'), ('0', 'successful attempts to bypass the guardrails'), ('3', 'rounds of prompt iteration')],
            'I also hand-wrote the moments that build trust: the welcome, the intent check and the order card.', None)

# ------------------------------------------------------------------ Orbit
d.section('okx-orbit', 'Orbit: a social layer for traders, 200% DAU growth.', 'OKX · Orbit')
media_slide(d, 'orbit', '03 · Content design, social', 'Credibility you can see',
            [('Orbiters lead the feed', 'High-value traders whose posts drive engagement'),
             ('Proof on every profile', 'A real OKX track record, up front'),
             ('A bar to get in', 'Minimum volume and balance keep it credible'),
             ('My scope', 'Onboarding, the feed and both profile types')],
            phones_framed(A, [('orbit-feed', 'The Orbit feed'), ('orbit-profile', 'An Orbiter profile')], 860, 840), 860, None)
big_numbers(d, 'orbit-result', 'Result', 'Daily active users', [('200%', "growth in Orbit's daily active users")],
            'Measured in the three months after launch, before I left OKX.', None,
            visual=phones_framed(A, [('orbit-follow', 'Follow top Orbiters'), ('orbit-upgrade', 'Upgrade to Orbiter')], 760, 840, bg='#1B3527'), vis_w=760)

# ------------------------------------------------------------------ Crypto Rewind
d.section('okx-rewind', 'Crypto Rewind: a year in review that beat every goal.', 'OKX · Crypto Rewind')
media_slide(d, 'rewind-story', '04 · Dynamic content', 'Your year, played back like a playlist',
            [('What we learned', 'Too many numbers, too personal to share'),
             ('Three parts', 'Assets, how you traded, your trader persona'),
             ('One space theme', 'Across every screen and language'),
             ('Kind to hard years', 'Good years are "out of this world"')],
            phones_framed(A, [('cr-open', 'Part 1 of 3'), ('cr-earn', 'A good year'), ('cr-loss', 'A hard year')], 1000, 840, gap=20), 1000, None, head_size=48)
media_slide(d, 'rewind-share', 'Built for shareability', 'Personal, then social',
            [('Safe to post', 'A trader persona with a rarity tag, no balances'),
             ('Worth sharing', 'A gift for sharing, one tap to Telegram, WhatsApp or X'),
             ('Built to spread', 'A QR code invites friends to play their own')],
            phones_framed(A, [('cr-persona', "The persona reveal: You're a Comet"), ('cr-share', 'The share sheet')], 860, 840), 860, None)
big_numbers(d, 'rewind-goals', 'Actual vs goal', 'Every target beaten',
            [('3.26M', 'click-throughs, against 1.5M'), ('1.22M', 'completed journeys, against 800K'), ('117K', 'shares, against 50K')],
            'Amplitude, as of 28 Feb 2025. The 2025 edition, which I also worked on, won a Red Dot design award in 2026.', None)

# ------------------------------------------------------------------ Buildlr
d.section('buildlr', 'Buildlr: a five-tier quote form, from tablet to phone.', 'Buildlr')
case_hero(d, 'bl-title', 'Case 05 · Construction tech', 'Simplifying operational tools',
          'A pre-construction SaaS for the German market, built from zero: quotes, task management and Gantt scheduling. Designed for consultants on tablets and contractors on phones.',
          [('Role', 'Founding designer, freelance'), ('Timeline', 'Jun 2025 to Feb 2026'), ('Team', 'Me and the founder'), ('Scope', 'SaaS, IA, design system')],
          [('140', 'final screens in eight months'), ('167', 'components across 25 sets, light and dark')],
          hero_img(A, 'm-h-bl', 'Tasks switched on as rows in a quote'), None)
media_slide(d, 'bl-form', 'Complex forms', 'Only the tier you need',
            [('Five tiers deep', 'From project down to sub-task'),
             ('Always oriented', 'A persistent tree shows where you are'),
             ('Live pricing', 'Tasks switch on as rows, totals update'),
             ('Questions in context', 'Client RFIs sit inside the task')],
            framed(A, 'm-bl-rfi', 'A suggested RFI inside a task', 940, 680, pad=40), 940, None)
media_slide(d, 'bl-mobile', 'Mobile', 'Same tree, one thumb',
            [('Hierarchy you can navigate', 'Tabs, chips and cards, layered'),
             ('Scan fast, act faster', "A big button in thumb's reach"),
             ('A familiar control, made distinct', 'The timer doubles as a time-tracking ring')],
            phones_framed(A, [('bl-m-specs', 'Specs tab'), ('bl-m-media', 'Task detail'), ('bl-m-timer', 'Working, with the time ring')], 1020, 840, gap=20), 1020, None)

# ------------------------------------------------------------------ Ninja Van
d.section('ninjavan', 'Ninja Van: research with 59 people, then a self-serve portal and CRM tools.', 'Ninja Van')
case_hero(d, 'nv-title', 'Case 06 · Logistics', 'Service recovery at scale',
          'I researched how service recovery worked across Southeast Asia, then designed a self-serve portal for merchants and the Salesforce CRM tools agents use behind it.',
          [('Role', 'Product designer II'), ('Timeline', 'Jul 2021 to Jan 2023'), ('Company', 'Ninja Van'), ('Scope', 'Service design, research, UI')],
          [('60%', 'faster case resolution'), ('70%', 'of case logging automated for delays')],
          hero_img(A, 'm-h-nv', 'A case in the merchant portal'), None)
groups = [('24', 'Support agents', 'SUS survey and interviews'), ('18', 'Merchants', 'CES survey and interviews'), ('17', 'Resolution teams', 'Finance, warehouse, drivers')]
gcards = ''.join(
    f'<div style="display:flex;flex-direction:row;gap:24px;align-items:center;background:{CARD};border:1px solid {RULE};border-radius:20px;padding:22px 28px">'
    f'<p style="font-family:{DISP};font-size:88px;{NSTYLE};line-height:0.9;color:{ACCENT};width:110px">{n}</p>'
    f'<div style="flex:1;display:flex;flex-direction:column;gap:4px"><p style="font-size:34px;font-weight:600;color:{INK}">{e(g)}</p>'
    f'<p style="font-size:26px;font-weight:400;color:{BODY}">{e(m)}</p></div></div>' for n, g, m in groups)
d.add('nv-research', f'<div style="display:flex;flex-direction:row;gap:56px;align-items:center;height:{CH}px">'
      f'<div style="width:620px;display:flex;flex-direction:column;gap:28px"><div style="display:flex;flex-direction:column;gap:14px">{head("Research", "59 people, three groups")}</div>'
      f'<div style="display:flex;flex-direction:column;gap:14px">{gcards}</div></div>'
      f'<div style="width:988px;display:flex;flex-direction:column;gap:24px">'
      f'<div style="background:{MINT};border-radius:20px;padding:24px 30px"><p style="font-size:30px;font-weight:500;line-height:1.35;color:{ACCENT}">Each group has its own experience and pain points. Fixing one in isolation just moves the problem.</p></div>'
      f'{framed(A, "m-nv-relay", "One issue passing between three teams", 988, 480, pad=24, radius=12)}</div></div>',
      pad=PAD, layout='display:flex;flex-direction:column')
media_slide(d, 'nv-portal', 'Self-serve portal', 'Issues live where orders live',
            [('Where orders live', 'Issues raised in the portal merchants already use'),
             ('Agent-ready fields', 'In the order agents need them'),
             ('Automatic for delays', 'Late parcels open cases on their own'),
             ('Closing the loop', 'A low survey score reopens the case')],
            framed(A, 'm-nv-issues', 'Open issues in the merchant portal', 940, 700, pad=40), 940, None)
big_numbers(d, 'nv-results', 'Results', 'Faster recovery, one design language',
            [('66%', 'less time to identify a parcel as missing'), ('9', 'design libraries merged into one'), ('27', 'active products across the portfolio')],
            "I also documented Akira, Ninja Van's design system, and built content standards into its components.", None)

# ------------------------------------------------------------------ Neuron
d.section('neuron', 'Neuron: tasks managers can track, 90%+ less Slack, and two platforms merged.', 'Neuron')
case_hero(d, 'nr-title', 'Case 07 · Mobility', 'Shift plans that stick',
          'Neuron runs shared e-scooters and e-bikes across Australia and beyond. I redesigned how managers and ground operators work together, then merged two internal platforms into one.',
          [('Role', 'Senior product designer'), ('Timeline', 'Jan 2023 to Dec 2023'), ('Company', 'Neuron Mobility'), ('Scope', 'Internal tools, research, IA')],
          [('90%+', 'less reliance on Slack for task updates'), ('10%', 'more efficient field operations')],
          hero_img(A, 'm-h-nr', 'Assigned tasks beside the map'), None)
media_slide(d, 'nr-tasks', 'Field research', 'Tasks you can assign, and see done',
            [('Remote interviews', 'Ops managers across markets'),
             ('Shadowing on shift', 'Ground operators in Melbourne and Perth'),
             ('Assign on the map', "Tasks land straight in the operator's list"),
             ('A real measure', 'Recorded assignments show how a shift went')],
            framed(A, 'm-nr-live', 'Assigning tasks on the map', 940, 660, pad=40), 940, None, head_size=48)
big_numbers(d, 'nr-merge', 'Two platforms, one stack', 'Merged onto React, ahead of schedule',
            [('60%', 'faster page loads on average'), ('2', 'front ends merged into one'), ('3', 'markets localised: AU, NZ and UK')],
            'An Ant Design-based component library, styled for Neuron. Several tools moved from developers to city teams.', None)

# ------------------------------------------------------------------ Close
d.section('close', 'Thank you and contact.', '')
closing(d, 'close', "Think less, not thoughtless. Let's make better products together.", ['mancini.tan@gmail.com', 'mancinitan.com'])
print(d.write(), 'slides')
