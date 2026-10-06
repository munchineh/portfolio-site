"""Presenting deck: short like the website, with the extra numbers I can share in an interview, and a script on every slide."""
import sys
from layouts import *
from assets import PRESENT as A

ROOT = sys.argv[1]
d = Deck(ROOT, 'Mancini Tan · Interview presentation', 'Mancini Tan')

# Jargon notes go under each slide's script (speaker notes only, never on the slide)
from terms import notes_block
_add = d.add
def _add_with_terms(sid, inner, **kw):
    if kw.get('notes'): kw['notes'] += notes_block(sid)
    _add(sid, inner, **kw)
d.add = _add_with_terms

def bullets(items, size=30):
    lis = ''.join(f'<li>{e(x)}</li>' for x in items)
    return f'<ul style="font-size:{size}px;line-height:1.5;color:{BODY};display:flex;flex-direction:column;gap:10px">{lis}</ul>'

def point_slide(sid, eb, head, items, visual, vis_w, notes):
    """Heading, 2 to 4 short points, and a visual on the right."""
    tw = FULL_W - vis_w - 72
    left = f'<div style="width:{tw}px;display:flex;flex-direction:column;gap:28px">{eyebrow(eb)}{h2(head)}{bullets(items)}</div>'
    d.add(sid, f'<div style="display:flex;flex-direction:row;gap:72px;align-items:flex-start">{left}<div style="width:{vis_w}px;display:flex;justify-content:center">{visual}</div></div>', notes=notes)

def numbers(sid, eb, head, stats, note, notes, dark=True):
    stats_slide(d, sid, eb, head, stats, note=note, notes=notes, dark=dark)

# ------------------------------------------------------------------ Intro
d.section('intro', 'Who I am and how I work.', '')
cover(d, 'cover', 'Mancini Tan', 'Product, content and conversation design', 'Portfolio · 2026', A['portrait'],
      notes="Hi everyone, thank you so much for having me today. I'm Mancini. I'm a product designer with a strong content and conversation design background, and I'll walk you through a few projects that show how I work. I'll keep each one short, and I'm very happy to go deeper on anything that's useful for the role.")
about(d, 'about', "I design things people don't have to think about.",
      "5+ years across fintech, logistics and e-commerce. Singaporean, based in Seoul, open to roles anywhere.",
      [('Experience', '5+ years: DBS, Ninja Van, Neuron, OKX, Buildlr, plus my own store'),
       ('Industries', 'Fintech, logistics, e-commerce, construction tech, mobility'),
       ('Skills', 'UI design, conversation design, content design, localization'),
       ('Languages', 'English (native), Chinese (proficient), Korean and German (intermediate)')],
      notes="A quick bit about me. I've spent over five years designing across banking at DBS, logistics at Ninja Van, micromobility at Neuron and crypto at OKX, and more recently as a founding designer at Buildlr. I also run my own menswear store, EVN Archive. The thread running through all of it is taking something complicated and making it easy to use. I work in English and Chinese every day, and at OKX and Neuron a lot of my collaboration with product and engineering happened in Mandarin.")
contents(d, 'contents', [
    ('01', 'Helping shoppers find their fit', 'EVN Archive', 'E-commerce, end to end'),
    ('02', 'An assistant that trades in chat', 'OKX', 'AI conversation design'),
    ('03', 'Making trading social', 'OKX · Orbit', 'Content design, growth'),
    ('04', 'Personalized content at scale', 'OKX · Crypto Rewind', 'Dynamic content'),
    ('05', 'Simplifying operational tools', 'Buildlr', 'SaaS, complex forms'),
    ('06', 'Service recovery at scale', 'Ninja Van', 'Research, service design'),
    ('07', 'Shift plans that stick', 'Neuron Mobility', 'Internal tools')], head="Today's cases",
    notes="Here's what I've picked for today. Feel free to stop me at any point, and if one of these is closer to what your team is working on, I'm happy to spend more time there.")

# ------------------------------------------------------------------ EVN
d.section('evn', 'EVN Archive: a sizing tool that lifted free-size sales 400%+.', 'EVN Archive')
case_title(d, 'evn-title', 'Case 01 · E-commerce', 'Helping shoppers find their fit',
           'My own Shopify store for independent Korean menswear, designed and built end to end. This case covers the sizing tool that helps shoppers buy free size with confidence.',
           [('Role', 'Founder and designer'), ('Timeline', 'May 2026 to now'), ('Stack', 'Shopify, Liquid, CSS, JS'), ('Team', 'Just me')],
           [('400%+', 'increase in free-size sales'), ('4', "free-size sales in the sizing tool's first week")],
           wide(A['evn-pdp'], 'The product page with How it\'ll fit you', 560, 305),
           notes="The first one is my own store, EVN Archive. I run it end to end: the storefront design, the product copy, the pricing, support, and the front-end code. Free-size pieces were some of my best designs, but they sold the least. So I designed and built a sizing tool, and free-size sales went up more than 400%. In its first week alone, four free-size pieces sold.")
point_slide('evn-problem', 'The problem and the idea', 'Hundreds of visits, almost no carts',
            ["No size chart to lean on, so shoppers couldn't picture the fit",
             'The tool compares height and weight with each garment\'s measurements',
             'It returns snug, recommended or relaxed, in plain words',
             'It reads the Size & Fit copy already on each product page, so new products just work'],
            wide(A['evn-finder'], 'The Find your fit pop-up', 620, 584), 620,
            notes="Three free-size jackets had hundreds of visits and almost no add-to-carts. When I looked at it from the shopper's side, the issue was simple: there's no size chart, so you can't picture how it'll sit on you. The tool asks for height and weight, compares them with each garment's actual measurements, and gives you a plain answer. One decision I'm happy with is that it reads the product copy that's already on the page, so there's no separate database to maintain. A new product works the day it goes live.")
d.add('evn-touch', f'{eyebrow("Touchpoints")}{h2("One recommendation, everywhere you shop")}'
      '<div style="display:flex;flex-direction:row;gap:24px;align-items:stretch">' + ''.join(
        tile(None, t, x, None, False, wide(A[k], alt, 330, 190)) for t, x, k, alt in [
          ('Homepage', 'A Free Size Edit and a fit prompt near the top.', 'evn-home', 'Free Size Edit'),
          ('Fit profile', 'Height and weight first, more detail optional. Saved once.', 'evn-finder', 'Find your fit'),
          ('Collection', 'Filter to pieces recommended for you.', 'evn-collection-z', 'Recommended filter'),
          ('Product page', 'A plain-words fit read under every size.', 'evn-pdp-z', 'Fit read on the product page')]) + '</div>'
      + statement('Plus a 20% free-size offer and short videos on how free size fits, to move people past "it won\'t fit me".', size=34),
      notes="A good solution rarely lives on one screen, so the recommendation follows you through the store: the homepage, your fit profile, a filtered collection, and every product page. Around the tool I added two nudges, based on social judgment theory, the idea that people tune out anything too far from what they already believe. A limited 20% offer on free size lowered the risk of a first try, and short videos showed how pleats and drawcords fit different bodies.")
point_slide('evn-store', 'Beyond the sizing tool', 'Owning the whole experience',
            ['Information architecture and a two-way taxonomy: Foundations and Statement',
             'A small set of price tiers, so prices read at a glance',
             'Funnel and session data to fix the pages losing conversion',
             'Localised for our top Asian markets, guided by Meta ad data',
             'All customer support and reviews, feeding back into the design'],
            wide(A['evn-home'], 'The EVN Archive homepage', 620, 264), 620,
            notes="Running my own store means I own everything around the feature too. I set up the categories and an editorial taxonomy, a simple pricing framework, and I use session and funnel data to find the pages losing conversion, things like gallery order and sold-out states. I localised the storefront for the markets our Meta ads showed us we really have, and I handle every customer email myself, which is honestly the fastest research loop I've ever had. I also built the sizing tool with an AI-assisted workflow, Claude with the Shopify MCP, which let me move from idea to a live feature quickly.")

# ------------------------------------------------------------------ OKX overview
d.section('okx', 'OKX overview: three products that made crypto more social.', 'OKX')
case_title(d, 'okx-title', 'Cases 02 to 04 · Fintech', 'Making crypto social',
           'Three products that made crypto more social: an AI assistant that trades in chat, Orbit, a social layer for traders, and Crypto Rewind, a personalised year in review.',
           [('Role', 'Senior content designer'), ('Timeline', 'Mar 2024 to Dec 2025'), ('Worked in', 'English and Mandarin'), ('Scope', 'Conversation, social, dynamic content')],
           [('3.26M', 'Crypto Rewind click-throughs, against a 1.5M goal'), ('200%', "growth in Orbit's daily active users")],
           phones([(A['okx-50k'], 'Simple Buy at 50,000 USD', None, None)], 420, 700, caps=False),
           notes="Next is OKX, where I was a senior content designer for almost two years. Crypto is still young, and part of making it feel normal is making it social, so I'll show three products: an AI assistant that trades with you in chat, Orbit, a social layer for traders, and Crypto Rewind, our year in review. The team worked largely in Mandarin, so most of my day-to-day was bilingual. I also built content standards into the core component library with our design systems team, which cut UI copy inconsistencies by about 90%.")

# ------------------------------------------------------------------ AI assistant
d.section('okx-ai', 'AI trading assistant: prompt design, guardrails and red-teaming.', 'OKX · AI assistant')
point_slide('ai-problem', '02 · AI conversation design', 'A personal desk for big trades',
            ['Simple Buy is fast, but the rate is worse than spot. On big orders, that gets expensive',
             'Live agents in Greater China already offered better rates over chat',
             'The AI assistant takes that service to every market, from 50,000 USD up',
             'The team stays on the conversations that need a human'],
            phones([(A['okx-50k'], 'A better rate offered at 50,000 USD', '50,000 USD', 'A better rate.'), (A['okx-sheet'], 'The handover to chat', 'The handover', 'Into the chat.')], 640, 780), 640,
            notes="Simple Buy locks in a quote in seconds, but the rate is worse than a spot trade, which gets expensive on large orders. Our live agents in Greater China already offered big traders a better rate over chat, and it worked beautifully, but a small team can only be in so many markets at once. So from 50,000 USD up, the app offers a preferential rate and hands you to an AI assistant that works alongside the agents. The agents set the standard for how personal it should feel, and they stay on the conversations that need a human.")
table_slide(d, 'ai-prompt', [('eyebrow', 'The system prompt'), ('h2', 'Five layers, so the bot never improvises with money')],
     ['Layer', 'What it does'],
     [['01 Persona', 'A senior trading consultant. Assuring, natural, "substantial" never "massive".'],
      ['02 Adaptive tone', "Mirrors the user's vocabulary, from plain English to trader talk."],
      ['03 Guardrails', 'Confirm both sides, never assume a currency, market orders only.'],
      ['04 Edge cases', 'Fearful language switches it to a calm, human register.'],
      ['05 Few-shot examples', 'One worked example per persona: beginner, expert, distressed.']],
     [28, 72], size=28,
     notes="I designed the system prompt in five layers. Each answers one question: who it is, how it should talk to this person, what it must always and never do, what happens off the happy path, and what good looks like. The guardrails layer is the one I'd point to. With people's money at stake, a hallucinated rate or an assumed currency could cost someone thousands, so if someone types fifty K, it always asks: USD, SGD or USDT?")
numbers('ai-results', 'Testing', 'Benchmarked, then red-teamed',
        [('100%', 'persona consistency in testing'), ('0', 'successful attempts to bypass the guardrails'), ('3', 'rounds of prompt iteration')],
        'I also hand-wrote the moments that build trust: the welcome, the intent check and the order card.',
        notes="I benchmarked it against a standard query set, then red-teamed it myself, trying to talk it into limit orders and vague trades. That surfaced things like it calling large orders massive, which makes people nervous, or offering order types we hadn't built. Three rounds of iteration later, we had full persona consistency and no successful guardrail bypasses in adversarial testing. I also chose which moments stay hand-written: the welcome, the intent check and the order card, because that's where people need reassurance before a large trade.")

# ------------------------------------------------------------------ Orbit
d.section('okx-orbit', 'Orbit: a social layer for traders, 200% DAU growth.', 'OKX · Orbit')
point_slide('orbit', '03 · Content design, social', 'Credibility you can see',
            ['Orbiters: high-value customers whose posts, groups and trades drive engagement',
             'I designed onboarding, the feed and both profile types',
             'Profiles lead with a real OKX track record',
             'Minimum trading volume and asset balance keep every Orbiter credible'],
            phones([(A['orbit-feed'], 'The Orbit feed', 'The feed', None), (A['orbit-profile'], 'An Orbiter profile', 'Orbiter profile', None)], 640, 780), 640,
            notes="Orbit is OKX's social space, where traders post, follow each other and share trades. In a crypto feed everyone sounds like an expert, so credibility was the design problem. Orbiters are our key influencers, high-value customers whose activity drives engagement, and their profiles lead with their actual track record on OKX. Upgrading leads with benefits like trade commission, and hard requirements behind it keep every Orbiter credible. I worked on onboarding, the feed and both versions of the profile.")
numbers('orbit-result', 'Result', 'Daily active users', [('200%', "growth in Orbit's daily active users")],
        'Measured in the three months after launch, before I left OKX.',
        notes="In the three months after launch, daily active users grew 200%. I left OKX about three months after Orbit went live, so that's the window I can speak to.")

# ------------------------------------------------------------------ Crypto Rewind
d.section('okx-rewind', 'Crypto Rewind: a year in review that beat every goal.', 'OKX · Crypto Rewind')
point_slide('rewind-story', '04 · Dynamic content', 'Your year, played back like a playlist',
            ['Past campaigns: too many numbers, too personal to share, late legal changes',
             'Three parts: assets, how you traded, and a trader persona',
             'One space theme across every screen and language',
             'Good years are "out of this world". Hard years get kinder framing'],
            phones([(A['cr-open'], 'Part 1 of 3', 'The opening', None), (A['cr-earn'], 'A good year', 'A good year', None), (A['cr-loss'], 'A hard year', 'A hard year', None)], 760, 780), 760,
            notes="Every year end, OKX looks back on each user's year of trading. I audited the 2022 and 2023 campaigns and spoke to the teams behind them. People liked seeing their own data, but they didn't finish and they didn't share, and legal feedback landed so late that copy churned until launch. So I framed 2024 as a playlist in three parts, with one space theme that gave Legal, Marketing and every translator the same brief early. Good years are out of this world, and hard years get a kinder line about getting ready for the next takeoff.")
point_slide('rewind-share', 'Built for shareability', 'Personal, then social',
            ['A trader persona with a rarity tag, and no balances, so it\'s safe to post',
             'A gift for sharing, one tap to Telegram, WhatsApp or X',
             'A QR code invites friends to play their own'],
            phones([(A['cr-persona'], "The persona reveal: You're a Comet", 'The persona', None), (A['cr-share'], 'The share sheet', 'Share sheet', None)], 640, 780), 640,
            notes="The ending is where Rewind starts to travel. Each journey ends on a trader persona, like Crypto Comet, with a rarity tag and no balances, so it's safe to post and fun to compare. Sharing comes with a gift, and the card has a QR code that brings whoever sees it into the app to play their own. Each share pulls someone new in and gives the community something to talk about.")
d.add('rewind-goals', f'{eyebrow("Actual vs goal", True)}{h2("Every target beaten", True)}'
      '<div style="display:flex;flex-direction:row;gap:56px;padding:24px 0 0 0">' +
      stat('3.26M', 'click-throughs, against 1.5M', True, 130) + stat('1.22M', 'completed journeys, against 800K', True, 130) + stat('117K', 'shares, against 50K', True, 130) +
      f'</div>{para("Amplitude, as of 28 Feb 2025. The 2025 edition, which I also worked on, won a Red Dot design award in 2026.", True, 26)}',
      bg=DARK, color=ON_DARK, dark=True,
      notes="Every goal was set against the year before, adjusted for user growth, and we beat all three: 3.26 million click-throughs against 1.5 million, 1.22 million completed journeys against 800 thousand, and 117 thousand shares against 50 thousand. I also worked on the 2025 edition before I left, and it went on to win a Red Dot design award this year.")

# ------------------------------------------------------------------ Buildlr
d.section('buildlr', 'Buildlr: a five-tier quote form, from tablet to phone.', 'Buildlr')
case_title(d, 'bl-title', 'Case 05 · Construction tech', 'Simplifying operational tools',
           'A pre-construction SaaS for the German market, built from zero: quotes, task management and Gantt scheduling. Designed for consultants on tablets and contractors on phones.',
           [('Role', 'Founding designer, freelance'), ('Timeline', 'Jun 2025 to Feb 2026'), ('Team', 'Me and the founder'), ('Scope', 'SaaS, IA, design system')],
           [('140', 'final screens in eight months'), ('167', 'components across 25 sets, light and dark')],
           wide(A['bl-rows'], 'The Tasks step of a new quote', 560, 379),
           notes="Buildlr is a pre-construction SaaS for the German market. I was the founding designer, working async between Seoul and the founder in Europe, and I owned everything from discovery to launch: information architecture, the visual identity, prototypes and the design system. In eight months that came to 140 final screens and a library of 167 components across 25 sets, in light and dark mode.")
point_slide('bl-form', 'Complex forms', 'Only the tier you need',
            ['Every quote runs five tiers deep, from project to sub-task',
             'A persistent tree keeps consultants oriented',
             'Tasks switch on as rows, and pricing recalculates live',
             'Client questions become RFIs inside the task, with a deadline'],
            wide(A['bl-rfi'], 'A suggested RFI inside a task', 860, 582), 860,
            notes="Every quote runs five tiers deep, so the challenge was keeping that much detail manageable with a client looking over your shoulder. I used progressive disclosure: a persistent tree for orientation, tasks you switch on as rows, and pricing that recalculates live. Only one task opens at a time. Consultants also kept stalling on things only the client could answer, so a request for information now lives inside the task itself, pre-written with a deadline, and it goes straight to the client's phone.")
d.add('bl-mobile', f'{eyebrow("Mobile")}{h2("Same tree, one thumb")}' +
      phones([(A['bl-m-specs'], 'Specs tab', 'Hierarchy you can navigate', 'Tabs, chips and cards, layered.'),
              (A['bl-m-media'], 'Task detail', 'Scan fast, act faster', "A big button in thumb's reach."),
              (A['bl-m-timer'], 'Working, with the time ring', 'A familiar control, made distinct', 'The timer is a time-tracking ring.')], FULL_W, 600),
      notes="The same quote goes to contractors on their phones. Rooms became chips, categories became accordions, and tasks became cards, so the hierarchy carries over from desktop. Details stay quick to scan, while a big button keeps the next action within thumb's reach. And for logging time, I took a familiar control and made it distinct: the start and stop button doubles as a ring that fills as the hour goes by.")

# ------------------------------------------------------------------ Ninja Van
d.section('ninjavan', 'Ninja Van: research with 59 people, then a self-serve portal and CRM tools.', 'Ninja Van')
case_title(d, 'nv-title', 'Case 06 · Logistics', 'Service recovery at scale',
           'I researched how service recovery worked across Southeast Asia, then designed a self-serve portal for merchants and the Salesforce CRM tools agents use behind it.',
           [('Role', 'Product designer II'), ('Timeline', 'Jul 2021 to Jan 2023'), ('Company', 'Ninja Van'), ('Scope', 'Service design, research, UI')],
           [('60%', 'faster case resolution'), ('70%', 'of case logging automated for delays')],
           wide(A['nv-case'], 'A case in the merchant portal', 560, 350),
           notes="At Ninja Van I worked on service recovery, what happens when a parcel goes wrong. Three teams get involved, and the merchant often hears nothing. I researched the whole chain, then designed a self-serve portal for merchants and the Salesforce CRM screens agents use behind it. Overall it cut resolution time by about 60%, and it automated about 70% of case logging for delayed pickups and deliveries.")
table_slide(d, 'nv-research', [('eyebrow', 'Research'), ('h2', '59 people, three groups'),
      ('st', 'Each with their own experience and pain points. Fixing one in isolation just moves the problem.')],
     ['Group', 'Method', 'People'],
     [['Support agents', 'SUS survey and interviews', '24'], ['Merchants', 'CES survey and interviews', '18'], ['Resolution teams', 'Finance, warehouse, drivers', '17']],
     [40, 45, 15], size=30,
     notes="I interviewed 59 people across Southeast Asia: support agents, merchants and the resolution teams in finance, warehouse and delivery. Alongside the interviews I ran a usability survey for agents and a Customer Effort Score survey for merchants. Then I prioritised themes by case volume and response time, so we'd fix what helped the whole system most, rather than moving the problem from one team to another.")
point_slide('nv-portal', 'Self-serve portal', 'Issues live where orders live',
            ['Raise issues in the portal merchants already use',
             'Fields in the same order agents need them',
             'Delays open cases automatically',
             'The survey became a way to close the loop: a low score reopens the case'],
            wide(A['nv-issues'], 'Open issues in the merchant portal', 860, 538), 860,
            notes="Raising an issue used to mean finding a phone number and hoping someone received it. Now it happens in the portal merchants already use for their orders, with fields in the same order agents enter them, which cut a lot of back and forth. Delays open cases on their own. And the effort survey moved from cold calls into the portal and new branded emails, one tap from each case. Low scores also allow merchants to reopen the case, for a more satisfying journey.")
numbers('nv-results', 'Results', 'Faster recovery, one design language',
        [('66%', 'less time to identify a parcel as missing'), ('9', 'design libraries merged into one'), ('27', 'active products across the portfolio')],
        'I also documented Akira, Ninja Van\'s design system, and built content standards into its components.',
        notes="Beyond service recovery, identifying a missing parcel took about two thirds less time. I also contributed to Akira, Ninja Van's design system, which spans 27 active products. Along the way we merged nine design libraries into one, and I worked on the documentation and the content standards built into the components.")

# ------------------------------------------------------------------ Neuron
d.section('neuron', 'Neuron: tasks managers can track, 90%+ less Slack, and two platforms merged.', 'Neuron')
case_title(d, 'nr-title', 'Case 07 · Mobility', 'Shift plans that stick',
           'Neuron runs shared e-scooters and e-bikes across Australia and beyond. I redesigned how managers and ground operators work together, then merged two internal platforms into one.',
           [('Role', 'Senior product designer'), ('Timeline', 'Jan 2023 to Dec 2023'), ('Company', 'Neuron Mobility'), ('Scope', 'Internal tools, research, IA')],
           [('90%+', 'less reliance on Slack for task updates'), ('10%', 'more efficient field operations')],
           wide(A['neuron-map'], 'Assigning tasks on the map', 560, 350),
           notes="At Neuron, which runs shared e-scooters and e-bikes across Australia and beyond, I worked on the internal tools for operations. Managers planned shifts in a web dashboard, operators worked from a dense mobile app, and everything in between ran over Slack, so nobody could tell which tasks got done. Our dev team was in Wuhan, so PRDs and dev collaboration happened in Chinese.")
point_slide('nr-tasks', 'Field research', 'Tasks you can assign, and see done',
            ['Remote interviews with ops managers across markets',
             'Shadowing ground operators on shift in Melbourne and Perth',
             'Managers assign tasks on the map, and they land in the operator\'s list',
             'Recorded assignments gave managers a real measure of a shift'],
            wide(A['neuron-map'], 'The task map', 860, 538), 860,
            notes="I interviewed operations managers remotely, then shadowed operators on shift in Melbourne and Perth to see how they decide what to do next on the street. The result is simple: a manager assigns a task on the map and it lands in that operator's list, with the vehicle, battery and nearest station. Because assignments are recorded, managers finally had a real measure of a shift. Slack reliance for task updates dropped by more than 90%, and field operations got about 10% more efficient.")
numbers('nr-merge', 'Two platforms, one stack', 'Merged onto React, ahead of schedule',
        [('60%', 'faster page loads on average'), ('2', 'front ends merged into one'), ('3', 'markets localised: AU, NZ and UK')],
        'An Ant Design-based component library, styled for Neuron. Several tools moved from developers to city teams.',
        notes="I also worked on merging two internal tools that had grown into each other, one on Angular and one on React. I audited both with the teams using them and rebuilt the information architecture, and we moved onto React with an Ant Design-based library styled for Neuron. Pages loaded about 60% faster, the migration finished ahead of schedule, and I localised the tools for Australia, New Zealand and the UK.")

# ------------------------------------------------------------------ Close
d.section('close', 'Thank you and contact.', '')
closing(d, 'close', "Think less, not thoughtless. Let's make better products together.", ['mancini.tan@gmail.com', 'mancinitan.com'],
        notes="That's everything from me. Thank you so much for your time. I'd love to hear more about what your team is working on, and I'm happy to go deeper into any of these projects.")
print(d.write(), 'slides')
