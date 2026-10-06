"""Detailed deck: the full long-form case studies, for someone to read on their own or as a PDF.
Copy follows archive/long-copy-2026-10-06.md, plus every phrasing change made since."""
import sys
from cards import *
from assets import DETAILED as A

ROOT = sys.argv[1]
d = Deck(ROOT, 'Mancini Tan · Case studies (detailed)', 'Mancini Tan · Case studies', condensed_src=CONDENSED_SRC['detailed'])

# ------------------------------------------------------------------ Intro
d.section('intro', 'Who I am, what I do and the cases inside.', '')
cover(d, 'cover', 'Mancini Tan', 'Product, content and conversation design. Case studies from fintech, logistics, construction tech, mobility and my own e-commerce store.', 'Portfolio · Detailed edition · 2026', A['portrait'])
about(d, 'about', "I design things people don't have to think about.",
      "I'm Mancini, and I make complicated products easier. 5+ years across fintech, logistics and e-commerce. Singaporean, based in Seoul, and open to roles anywhere.",
      [('Experience', '5+ years across agency, in-house teams and my own e-commerce product'),
       ('Industries', 'Fintech, logistics, e-commerce, construction tech, mobility, advertising'),
       ('Skills', 'UI design, conversation design, content design, localization'),
       ('Languages', 'English (native), Chinese (proficient), Korean (intermediate), German (intermediate)')])
three_cards(d, 'what-i-do', 'What I do', 'Three ways I work',
            [('Content and conversation design', 'I write the words and design the conversations, from microcopy to AI chat flows, so every screen speaks as clearly as it looks.'),
             ('Making hard things feel easy', 'Crypto trading apps, support dashboards, field tools. I make fintech and ops products simple enough that anyone can jump in with confidence.'),
             ('End to end, zero to launch', "I've been the founding designer at start-ups and built my own store, EVN Archive, from scratch. I take products from first research to launch, and keep making them better.")])
contents(d, 'contents', [
    ('01', 'Helping shoppers find their fit', 'EVN Archive', 'E-commerce, UX, front-end'),
    ('02', 'An assistant that trades in chat', 'OKX', 'AI conversation design'),
    ('03', 'Making trading social', 'OKX · Orbit', 'Content design, social'),
    ('04', 'Personalized content at scale', 'OKX · Crypto Rewind', 'Dynamic content, growth'),
    ('05', 'Simplifying operational tools', 'Buildlr', 'SaaS, complex forms'),
    ('06', 'Service recovery at scale', 'Ninja Van', 'Research, service design'),
    ('07', 'Shift plans that stick', 'Neuron Mobility', 'Internal tools, research')])

# ------------------------------------------------------------------ EVN
d.section('evn', 'EVN Archive: a sizing tool that helps shoppers buy free size with confidence.', 'EVN Archive')
case_hero(d, 'evn-title', 'Case 01 · E-commerce', 'Helping shoppers find their fit',
           'EVN Archive is a Shopify store for independent Korean menswear, which I design and run. This case covers the sizing tool I built to help people buy free-size clothing online with confidence.',
           [('Role', 'Designer and founder. UX, UI, content and front-end'), ('Timeline', 'May 2026 to now'), ('Platform', 'Shopify, custom theme code'), ('Team', 'Just me')],
           [('4', "free-size sales in the sizing tool's first week"), ('400%+', 'increase in free-size sales')],
           hero_img(A, 'm-h-evn', "The Aura Windbreaker product page, with How it'll fit you under the size"), None)
side(d, 'evn-carts', [('eyebrow', 'The problem'), ('h2', 'Plenty of visits, very few carts'),
      ('st', 'Free size pieces are some of the strongest designs in the archive. They were also the ones that sold the least.'),
      ('p', "Three free-size jackets had hundreds of visits between them, and almost nobody added one to cart. Buying clothes online already asks for some trust. Free size asks for more, because there's no size chart to lean on. People couldn't picture how a piece would sit on them, so they left.")],
     framed(A, 'evn', 'A free-size jacket product page before the sizing tool', 860, 700, pad=40), 860)
side(d, 'evn-tool', [('eyebrow', 'The idea'), ('h2', 'A sizing tool that reads the garment'),
      ('st', 'You tell it your height and weight. It tells you how each piece will fit you.'),
      ('p', 'The sizing tool compares your numbers with each garment\'s own measurements and returns a fit read: snug, recommended or relaxed. Build and body measurements are optional, for people who want it exact.'),
      ('p', "It reads the Size & Fit copy that's already on every product page, so there's no separate database to keep in sync. A new product works the day it goes live, as long as its measurements are written properly.")],
     framed(A, 'm-evn-card', "How it'll fit you, on the product page", 820, 760, pad=48, radius=22), 820)
TP = [('Start where shoppers land', "The Free Size Edit sits near the top of the homepage, with a prompt to find your fit right below it. Shoppers can get a recommendation before they've even opened a product.", 'm-evn-t-home', 'The Free Size Edit on the homepage'),
      ('Share as much or as little as you like', "Height and weight are enough for a first recommendation. Shoppers who want a closer match can pick their build or add body measurements, in metric or imperial. It's saved, so they only do it once.", 'm-evn-t-finder', 'The Find your fit pop-up'),
      ('A shop that fits you', 'Once a shopper has a fit profile, the shop can narrow down to pieces recommended for them. One tap clears it, so browsing everything is never more than a click away.', 'm-evn-t-coll', 'The shop filtered to recommended pieces'),
      ('An answer on every product', 'Each product page says how that piece will fit, right under the size, in plain words like "This is your recommended size". Shoppers can edit their details from there if something looks off.', 'm-evn-t-pdp', 'How it will fit you on the product page')]
for i, sid in ((0, 'evn-touch'), (2, 'evn-touch2')):
    hd = [('eyebrow', 'Touchpoints'), ('h2', 'One recommendation, everywhere you shop'), ('st', 'The sizing tool shows up at four points, so the answer follows you from the homepage to checkout.')] if i == 0 else [('eyebrow', 'Touchpoints, continued'), ('h2', 'One recommendation, everywhere you shop')]
    tiles_slide(d, sid, hd, [(f'{i + j + 1} of 4', t, x, None, False, img(A[k], alt, 744, 220, 'cover', 14, None, False)) for j, (t, x, k, alt) in enumerate(TP[i:i + 2])])
tiles_slide(d, 'evn-steps', [('eyebrow', 'Behaviour'), ('h2', 'Moving people a step at a time'), ('st', 'People say yes in small steps.'),
      ('p', 'Social judgment theory explains why. People weigh a new idea against what they already believe, and tune out anything too far from it. For free size, that belief was "it won\'t fit me". So I met shoppers with three small steps across the places they already were.')],
     [('Social media', None, 'Short videos on how free-size pieces use techniques like pleats, drawcords and dropped shoulders to fit a range of body types.'),
      ('20% off', None, 'A limited discount on every free-size piece, shown on the homepage and in the announcement bar, so a first try felt lower risk.'),
      ('Sizing tool', None, 'A fit read on every product page, so shoppers feel sure before they add to cart.')])
big_statement(d, 'evn-lesson', 'A good product solution rarely lives on one screen.',
              'This applies well beyond clothing. The feature does the heavy lifting, but the content and offers around it, on the product and off it, are what bring people close enough to use it.')
d.add('evn-beyond', f'{eyebrow("Beyond the sizing tool")}{h2("Running my own store means owning the whole experience")}'
      '<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:24px">' + ''.join(tile(None, t, x) for t, x in [
        ('Information architecture', 'Categories and filters shaped around how people actually shop for clothes.'),
        ('Clear pricing', 'A small set of price tiers per garment type, so prices are easy to read at a glance.'),
        ('Content design', 'Product copy for the whole catalogue, plus search titles and descriptions.'),
        ('Data-driven localisation', 'Meta ad data showed where our shoppers really are, so the storefront is localised for those markets in Asia and written fresh for each.'),
        ('Support and reviews', "I run customer support over email and set up product reviews, so real buyers answer the next shopper's questions. Both feed straight back into the design."),
        ('Design and front-end', 'I designed and built the storefront myself, from the type and component system to custom features like the sizing tool, coded in Liquid, CSS and JavaScript.')]) + '</div>')

# ------------------------------------------------------------------ OKX overview
d.section('okx', 'OKX overview: three products that made crypto more social.', 'OKX')
case_hero(d, 'okx-title', 'Cases 02 to 04 · Fintech', 'Making crypto social',
           'Crypto is still young, and part of making it feel normal is making it social. Three products from my time at OKX: an assistant that trades with you in chat, Orbit, a social layer for traders, and Crypto Rewind, a year in review you play back like a playlist.',
           [('Role', 'Senior content designer. Content and conversation design'), ('Timeline', 'Mar 2024 to Dec 2025'), ('Worked in', 'English and Mandarin'), ('Scope', 'Conversation, social, dynamic content')],
           [('3.26M', 'Crypto Rewind click-throughs, against a 1.5M goal'), ('200%', "growth in Orbit's daily active users")],
           hero_phone(A, 'okx-50k', 'Simple Buy with 50,000 USD entered'), None,
           note='Crypto Rewind figures from Amplitude, as of 28 Feb 2025.')

# ------------------------------------------------------------------ OKX assistant
d.section('okx-ai', 'An AI trading assistant: system prompt design, guardrails and testing.', 'OKX · AI assistant')
chapter(d, 'ai-chapter', '02', 'An assistant that trades in chat', 'A live agent service for big orders, extended with AI so it reaches every market.', ['AI conversation design', 'Prompt design'])
side(d, 'ai-scale', [('eyebrow', '2.1'), ('h2', "A great service that couldn't scale"), ('st', 'Big orders were paying a worse rate than they needed to.'),
      ('p', "A lot of people use Simple Buy because it locks in a quote within seconds, even though the rate is worse than a regular spot trade. On small amounts, nobody notices. On large ones, it gets expensive."),
      ('p', 'For some users we already handled this with live agents, who offered a better rate over chat. It worked beautifully, but a small team can only be in so many markets at once.')],
     phones_framed(A, [('okx-500', 'Simple Buy with 500 USD entered')], 560, 792, pad=40), 560)
side(d, 'ai-desk', [('eyebrow', '2.2'), ('h2', 'A personal desk for big trades'), ('st', 'Big trades deserve white-glove service. The challenge was offering it at scale.'),
      ('p', 'Orders of fifty thousand dollars and up carry a slippage risk, since the price can move before the trade fills, and they usually come from high-value customers who deserve more than an instant quote. So big orders get a personal service with a preferential rate. That service was built by a dedicated team of agents in Greater China, real people who set the standard for how personal it should feel. To take it international, the AI assistant works alongside them, so the same treatment reaches every market the moment an order crosses the threshold, and the team stays on the conversations that need a human.')],
     phones([(A['okx-500'], '500 USD', '500 USD', 'Nothing changes.'), (A['okx-50k'], '50,000 USD with a better rate offered', '50,000 USD', 'A better rate is offered.'), (A['okx-sheet'], 'The handover sheet', 'The handover', 'What happens next.')], 880, 792), 880)
rows_slide(d, 'ai-prompt', [('eyebrow', '2.3'), ('h2', 'Designing the system prompt'), ('st', "When it's someone's money, the bot doesn't get to improvise."),
      ('p', 'A hallucinated rate, a vague phrase or a misread intent could cost someone thousands, so I built the prompt in five layers. Each one answers a different question.')],
     [('01 Persona', 'Who is it, and what is it for?', 'A senior trading consultant: assuring, natural, never "massive", always "substantial". Without one, a model sounds unsure right when someone is moving a lot of money.'),
      ('02 Adaptive tone', 'How should it talk to this person?', "Plain English by default; trading vernacular when the user says \"bps\" or \"fill or kill\". It mirrors the user's own vocabulary."),
      ('03 Guardrails', 'What must it always, and never, do?', 'Confirm both sides of the pair, never assume a currency, confirm instead of guessing, market orders only.'),
      ('04 Edge cases', 'What happens off the happy path?', 'Urgent or fearful language switches it to a human register: no jargon, no empty apologies, ask for the order ID.'),
      ('05 Few-shot examples', 'What does good look like?', 'One worked example per persona, so every layer above has ground truth to copy.')])
d.add('ai-shots', f'{eyebrow("2.3 · Few-shot examples")}{h2("What good looks like")}'
      '<div style="display:flex;flex-direction:row;gap:24px;align-items:stretch">' + ''.join(
        tile(who, None, None, None, False,
             f'<p style="font-size:26px;line-height:1.4;color:{INK};background:{MINT};padding:20px 24px;border-radius:18px">{e(u)}</p>'
             f'<p style="font-size:26px;line-height:1.45;color:{BODY};padding:4px 4px">{e(a)}</p>')
        for who, u, a in [('Beginner', 'I want to buy $50,000 of Solana.', "I can certainly help. Since this is a substantial amount, I'll secure a preferential rate. Is that $50,000 in USD, SGD or USDT?"),
                          ('Experienced trader', 'Offloading 50K USDT to ETH. Slippage?', 'Liquidity is deep. I can fill the full amount with minimal slippage, likely under 10bps. Want a firm price?'),
                          ('Distressed', "Transfer stuck!! I'm losing money!!", "I understand the urgency. Please send the order ID and I'll check what's holding it up right now.")]) +
      f'</div>{para("Few-shot examples give the model ground truth to copy before it meets a real user. One per persona, so every layer above has a worked example.")}')
tiles_slide(d, 'ai-human', [('eyebrow', '2.4'), ('h2', 'A human touch where it counts'), ('st', 'Good conversation design is a mix. AI for speed, and a human hand on the moments that need care.'),
      ('p', 'Like the rest of UX, the craft is in knowing which is which. I mapped every touchpoint in the chat. The welcome message, the line confirming what you want to do and the order card are hand-written, because that\'s where people need reassurance before a large trade, and the card matches order cards everywhere else in the app. The model handles everything after that: changes of mind, follow-up questions, the same thing explained another way.')],
     [('Human touch', None, 'The welcome, the intent check and the order card. Written and reviewed by a person.'),
      ('AI-generated', None, 'Follow-ups, changes of mind and clarifications. Quick to respond, and still inside the guardrails.')])
tiles_grid(d, 'ai-break', [('eyebrow', '2.5'), ('h2', 'Then I tried to break it'), ('st', 'Testing ran two ways, and the red-teaming taught me more.'),
      ('p', 'I benchmarked the prompt against a standard set of queries, checking every answer against the content guidelines and the conversation structure. Then I red-teamed it, trying to talk it into limit orders and vague trades to see whether the guardrails held. Three rounds of prompt iteration came out of it.')],
     [('Consistent persona', 'It kept calling large orders "massive", which makes people nervous.', "Alarmist adjectives banned. It now mirrors the user's own register."),
      ('Always asks', 'Vague amounts slipped through. "$50K", no currency.', 'The no-assumptions rule became a hard stop: USD, SGD or USDT?'),
      ('Market orders only', "It offered order types we hadn't built, like limit orders.", 'What it can execute is hard-coded. Anything else gets a polite redirect to a quote.')], cols=3, limit=420)

# ------------------------------------------------------------------ Orbit
d.section('okx-orbit', 'Orbit: a social layer for traders, built around credible influencers.', 'OKX · Orbit')
chapter(d, 'orbit-chapter', '03', 'Making trading social', 'Part of making crypto feel normal is making it social, so OKX wanted traders talking to each other inside the app. That became Orbit, a space to post, follow other traders and share trades.', ['Content design', 'Social', 'Growth'])
side(d, 'orbit-cred', [('eyebrow', '3.1'), ('h2', 'Credibility you can see'), ('st', 'In a crypto feed, everyone sounds like an expert.'),
      ('p', 'Orbiters are our key influencers. The idea was to find high-value customers and build social networks and communities around them, so their posts, groups and shared trades drive engagement the way great UGC does. I worked on onboarding, the feed and both versions of a profile: Orbiters, who can post, create groups and share trades, and everyone else.'),
      ('p', "An Orbiter's profile puts their track record up front, pulled from what they actually did on OKX. Upgrading is designed to feel empowering, leading with the benefits, from commission on trades to the standing that comes with the title. Behind the invitation sit hard requirements, like a minimum trading volume and asset balance, which keep every Orbiter credible.")],
     phones_framed(A, [('orbit-follow', 'Onboarding'), ('orbit-feed', 'The feed')], 780, 792), 780)
d.add('orbit-screens', f'{eyebrow("3.2 · Screens")}{h2("Onboarding, feed, profile and upgrade")}' +
      phones([(A['orbit-follow'], 'Onboarding: follow top Orbiters', 'Onboarding', 'Start with people worth following.'),
              (A['orbit-feed'], 'The feed, posts tagged to coins', 'The feed', "Posts carry the coin they're about."),
              (A['orbit-profile'], 'An Orbiter profile', 'Orbiter profile', 'Track record first, bio second.'),
              (A['orbit-upgrade'], 'Upgrading to Orbiter', 'Upgrading', 'What you can do, in three lines.')], FULL_W, 610))
stats_slide(d, 'orbit-result', '3.3 · Result', 'Daily active users after launch', [('200%', "growth in Orbit's daily active users")], note='Measured in the three months after launch, before I left OKX.')

# ------------------------------------------------------------------ Crypto Rewind
d.section('okx-rewind', 'Crypto Rewind: a personalised year in review that people finished and shared.', 'OKX · Crypto Rewind')
chapter(d, 'rewind-chapter', '04', 'Personalized content at scale', "Every year end, OKX runs a growth campaign that looks back on each user's year of trading. In 2024 it was Crypto Rewind, your year played back in three parts.", ['Dynamic content', 'Localization', 'Growth'])
tiles_slide(d, 'rewind-last', [('eyebrow', '4.1'), ('h2', 'What last year taught us'), ('st', "People liked seeing their own data. They just didn't finish, and they didn't share."),
      ('p', 'I audited the 2022 and 2023 campaigns, went through user feedback and spoke to the designers and PMs who ran them. Three problems kept coming up.')],
     [('Drop-off', 'Too many numbers', 'Page after page of figures got repetitive, and people left halfway.'),
      ('Sharing', 'Too personal', "Many didn't want their trading performance on social media."),
      ('Process', 'Late changes', 'Legal and Marketing feedback landed late, so copy churned until launch.')])
side(d, 'rewind-story', [('eyebrow', '4.2'), ('h2', 'Playing back your highlights, and highlighting you'), ('st', 'One space narrative tied the story, the tone and the brand together.'),
      ('p', 'Rewind turns the year into a playlist in three parts: your assets, how you traded, and a trader persona at the end. The line gave Legal and Marketing something to sign off early, and gave every writer and translator the same brief.'),
      ('p', 'Every line lives in that world. Good years are "out of this world". Bad years matter just as much, because plenty of people lost money in 2024. They get "You\'re only getting ready for your next takeoff", which is honest without rubbing it in.')],
     phones([(A['cr-open'], 'Part 1 of 3: the opening', 'The opening', 'Part 1 of 3.'), (A['cr-earn'], 'A good year', 'A good year', '"Talk about astronomical."'), (A['cr-loss'], 'A hard year', 'A hard year', 'Kinder framing.')], 920, 792), 920)
big_statement(d, 'rewind-theme', 'One theme, every screen, every language.', 'Keeping the theme consistent across every screen and language is what turned a lot of complex data into one story, and it made the brand feel stronger for it.')
side(d, 'rewind-share', [('eyebrow', '4.3'), ('h2', 'Personal, then social'), ('st', 'The end of the journey is where Rewind starts to travel.'),
      ('p', "Rewind is personal by design, and the persona at the end is what makes it social. Each journey ends on a trader type, like Crypto Comet or Market Maestro, with a rarity tag and a line about why you earned it. It celebrates how you trade and leaves your balances off, so it's safe to post and fun to compare with friends. One tap sends it to Telegram, WhatsApp or X, and the QR code brings whoever sees it into the app to play their own. Each share pulls someone new in, brings people back to see where their friends landed, and gives the community something to talk about long after the campaign. It paid off: shares came in at 117K, more than double the 50K goal.")],
     phones([(A['cr-persona'], 'The persona reveal: You\'re a Comet', 'The persona', 'Share to receive a gift.'), (A['cr-share'], 'Share your Crypto Rewind sheet', 'Built for shareability', 'A gift for sharing, and a QR code.')], 760, 792), 760)
d.add('rewind-goals', f'{eyebrow("4.4 · Actual vs goal")}{h2("Every target beaten")}'
      '<div style="display:flex;flex-direction:row;gap:56px;padding:24px 0 0 0">' +
      stat('217%', 'Click-throughs: 3.26M against a 1.5M goal', size=130) + stat('153%', 'Completed journeys: 1.22M against an 800K goal', size=130) + stat('234%', 'Shares: 117K against a 50K goal', size=130) +
      f'</div>{para("Goals were set against the year before, adjusted for user growth. Amplitude, as of 28 Feb 2025.", size=24)}'
      f'{statement("I also worked on the 2025 edition before I left OKX, which went on to win the Red Dot design award in 2026.", size=34)}')

# ------------------------------------------------------------------ Buildlr
d.section('buildlr', 'Buildlr: a pre-construction SaaS, from tablet quotes to phone task timers.', 'Buildlr')
case_hero(d, 'bl-title', 'Case 05 · Construction tech', 'Simplifying operational tools',
           'A pre-construction SaaS for the German market, built from zero, covering quotes, task management, Gantt scheduling and more. One of its key designs is a very deep quote form, made for consultants on a tablet beside their client and contractors on a phone with one hand free.',
           [('Role', 'Founding designer, freelance'), ('Timeline', 'Jun 2025 to Feb 2026'), ('Client', 'Buildlr'), ('Scope', 'SaaS, complex forms, scheduling, IA, design system')],
           [('140', 'final screens, designed from zero in eight months'), ('167', 'components across 25 sets, in light and dark')],
           hero_img(A, 'm-h-bl', 'Tasks switched on as rows in a new quote'), None, note='One designer, from discovery to launch.')
side(d, 'bl-days', [('eyebrow', '01'), ('h2', 'One quote, two very different days'), ('st', 'Buildlr takes a building job from the first client visit to the last task on site.'),
      ('p', "Consultants sit down with homeowners, usually with a tablet, and build the quote room by room as they talk. Once it's signed, contractors pick up that same quote on their phones to see what's next and log their hours. Every quote runs five tiers deep, from project to room, section, category, task and sub-task, and each carries its own quantities and prices."),
      ('p', "So the real job was keeping that much detail manageable in a client's living room and on a building site, without designing two different products.")],
     phones_framed(A, [('bl-m-specs', 'Mobile specs tab')], 520, 792, pad=40), 520)
side(d, 'bl-tier', [('eyebrow', '02'), ('h2', 'Only the tier you need'), ('st', 'Progressive disclosure keeps a five-tier quote from turning into a wall of numbers.'),
      ('p', "The tree lives in the left rail, so consultants always know which room and section they're in. Tasks are rows you switch on with a toggle. Open one and its sub-tasks unfold inside it, each with its own parameters, while the cost panel recalculates as you go. Only one task opens at a time, which keeps the page readable at forty rows deep, even with a client looking over your shoulder.")],
     framed(A, 'm-bl-rows', 'The Tasks step with rooms and sections on the left and tasks as rows', 900, 700, pad=36), 900)
side(d, 'bl-rfi', [('eyebrow', '03'), ('h2', 'The question lives in the form'), ('st', 'Consultants kept getting stuck on things only the client could answer.'),
      ('p', "Questions like which colour or which finish often held up a quote, and the habit was to leave the line blank and follow up by email. So the request for information (RFI) became part of the task itself. When a task needs a client decision, a suggested RFI appears right there with the question written and a deadline attached, and the client can answer it from their phone. The line stays flagged until it's answered.")],
     framed(A, 'm-bl-rfi', 'A suggested RFI inside the Install flooring task', 900, 640, pad=36) + caption(None, 'Drafted where the gap is. Once sent, every RFI is tracked on its own page with the thread attached.', 900), 900)
side(d, 'bl-mobile', [('eyebrow', '04'), ('h2', 'Same tree, one thumb'), ('st', 'The field app reads the same quote, one contractor at a time.'),
      ('p', 'Rooms became filter chips along the top. Categories became accordions. Each task is a card, parameters are label and value rows, and sub-tasks sit one indent in, just like on desktop, so the hierarchy survives the move. Anything still waiting on the client is flagged in red inside the card, because nobody should find that out on a ladder.')],
     phones([(A['bl-m-specs'], 'Specs tab', 'Hierarchy you can navigate', 'Tabs, chips and cards, layered.'),
             (A['bl-m-media'], 'Task detail', 'Scan fast, act faster', 'A big button in thumb\'s reach.'),
             (A['bl-m-timer'], 'Working with the timer', 'A familiar control, made distinct', 'A time-tracking ring.')], 1000, 792), 1000)
table_slide(d, 'bl-map', [('eyebrow', '05'), ('h2', 'How each tier travelled'), ('st', 'On a tablet, one page, always in context. On a phone, one task, always in reach.')],
     ['Tier', 'Tablet and desktop', 'Phone'],
     [['Room', 'Left rail, always visible', 'Filter chips along the top'], ['Section and category', 'Rail children, collapsible', 'Accordions'],
      ['Task', 'Row with a toggle, one open at a time', 'Card with a status line'], ['Sub-task', 'Section inside the open task', 'Indented block inside the card'],
      ['Parameters', 'Inline inputs with units', 'Label and value rows'], ['Client decision', 'Suggested RFI, pre-written', 'Red "client to provide" block']],
     [24, 38, 38], size=26)
big_statement(d, 'bl-async', 'Everything ran async, on top of the design system.',
              "Seoul and Europe share very few working hours. The library has no token layer yet, since it was built for speed with a two-person team. Tokens are the first thing I'd add with more runway.")

# ------------------------------------------------------------------ Ninja Van
d.section('ninjavan', 'Ninja Van: research with 59 people, then a self-serve portal and CRM tools.', 'Ninja Van')
case_hero(d, 'nv-title', 'Case 06 · Logistics', 'Service recovery at scale',
           'When a parcel goes wrong, three teams get involved and the merchant usually hears nothing. I researched how that chain really worked across Southeast Asia, then designed a self-serve portal for merchants and the tools support agents use behind it.',
           [('Role', 'Product designer II'), ('Timeline', 'Jul 2021 to Jan 2023'), ('Company', 'Ninja Van'), ('Scope', 'Service design, research, UI')],
           [('70%', 'of case logging automated for delayed pickups and deliveries'), ('66%', 'less time to identify a parcel as missing')],
           hero_img(A, 'm-h-nv', 'A case in the merchant portal'), None, note='Both figures are approximate.')
d.add('nv-handover', f'{eyebrow("01")}{h2("Five handovers, three teams")}{statement("A bit of information went missing at every handover.")}'
      + para("When a merchant raised an issue, a support agent logged it, the right resolution team investigated, and the answer made its way back along the same chain. In interviews, merchants told us the hardest part was often not knowing whether anyone was working on their case at all. And once a case was closed, the only way to dispute the outcome was to raise a new one and explain everything again.", size=26)
      + handover_row([('Merchant', 'Raises the issue'), ('Support agent', 'Logs it in the CRM'), ('Resolution team', 'Investigates'), ('Support agent', 'Gets the outcome'), ('Merchant', 'Hears back')])
      + para('What the merchant heard back: "Your case is under investigation."', size=26))
NV_RESEARCH = [('eyebrow', '02'), ('h2', 'Mapping the whole ecosystem'),
      ('st', 'Service recovery touches three groups, each with their own experience and pain points. Fixing one in isolation just moves the problem.'),
      ('p', 'So I looked at it from every side. I interviewed merchants, support agents and resolution teams across Southeast Asia, alongside a usability survey for agents and a Customer Effort Score survey for merchants. Then I weighed how often each theme came up against case volumes and response times, to find the changes that would help the whole system most.')]
_b, _ = fit_blocks(NV_RESEARCH, 900, 792)
d.add('nv-research', f'<div style="display:flex;flex-direction:row;gap:64px;align-items:flex-start">{text_col(_b, 900)}'
      f'<div style="width:700px;display:flex;flex-direction:column;gap:14px">' +
      number_cards([('24', 'Support agents', 'SUS survey and interviews'), ('18', 'Merchants', 'CES survey and interviews'),
                    ('17', 'Resolution teams', 'Finance, warehouse, drivers'), ('59', 'In total', 'Across Southeast Asia')]) + '</div></div>')
side(d, 'nv-portal', [('eyebrow', '03'), ('h2', 'Issues live where orders live'), ('st', 'The place you book a pickup is now the place you chase it.'),
      ('p', 'Raising an issue used to mean searching the website for a phone number, then hoping it had been received. So I built service recovery into the parcel portal merchants already used to manage their orders. The form asks for order IDs, issue type and proof of value in the same order agents enter them on their side, which cut out a lot of back and forth. Delayed pickups and deliveries now open cases automatically.')],
     framed(A, 'm-nv-issues', 'Open issues in the merchant portal', 900, 620, pad=36) + caption('Fields that change with the case.', "Each issue type has its own status steps and details. A damaged parcel shows claim details and a way to dispute the amount, while a delayed pickup only shows what's relevant to it.", 900), 900)
tiles_slide(d, 'nv-loop', [('eyebrow', '04'), ('h2', 'A bad score reopens the case'), ('st', 'The survey became a way to close the loop.'),
      ('p', "Customer Effort Score surveys used to go out by cold call and email, which was tedious for everyone and got very few replies. I moved the survey into the portal, right next to the case it's about, and into new HTML email templates designed for each issue type. Low scores also allowed users to reopen the case for a more satisfying user journey.")],
     [('Before', 'Cold calls and email', 'Generic text-only emails, with no way to leave a score.'),
      ('After', 'Next to the case', 'One tap to rate, from the portal or any email.'),
      ('Closing the loop', 'A low score reopens it', 'Merchants can question an outcome without starting over.')])
tiles_slide(d, 'nv-emails', [('eyebrow', '04 · Emails and CRM'), ('h2', 'From plain text to on-brand emails'),
      ('p', 'Updates used to be text-only. Each case type now has its own branded template that feels clearly, legitimately Ninja Van, and ends with a one-tap rating, so every update collects feedback and keeps the recovery journey going.')],
     [('Email template', 'A new pickup has been arranged', 'Apology, the new reservation details and a clear way to reply.'),
      ('Email template', 'New delivery estimates', 'The updated dates, plus a Rate experience button.'),
      ('Designing both sides of the service', 'Salesforce CRM screens', 'Support agents worked in a Salesforce-based CRM, so I also designed the screens they used to log and manage cases. Service recovery only works when both sides are looked after.')])
stats_slide(d, 'nv-akira', 'Also at Ninja Van: Akira', 'The case for a design system, in numbers',
            [('27', 'active products across the portfolio'), ('70%', 'of implementation on locally customised components')],
            note="Akira was Ninja Van's design system initiative. I worked on the documentation and on building content standards into the component library itself. It's a quiet way to keep a product consistent, and it lasts.")

# ------------------------------------------------------------------ Neuron
d.section('neuron', 'Neuron: shift plans managers can track, and two internal platforms merged into one.', 'Neuron')
case_hero(d, 'nr-title', 'Case 07 · Mobility', 'Shift plans that stick',
           'Neuron runs shared e-scooters and e-bikes across Australia and beyond. Managers plan where vehicles should go, and ground operators move them. I redesigned how those two sides work together, then helped merge two internal platforms into one.',
           [('Role', 'Senior product designer'), ('Timeline', 'Jan 2023 to Dec 2023'), ('Company', 'Neuron Mobility'), ('Scope', 'Internal tools, research, IA, web and mobile')],
           [('60%', 'faster page loads on average, after the merge'), ('10%', 'more actions per operator, per hour')],
           hero_img(A, 'm-h-nr', 'Assigned tasks beside the task map'), None, note='Both figures are approximate.')
tiles_slide(d, 'nr-slack', [('eyebrow', '01'), ('h2', 'The plan lived in Slack'), ('st', "Managers could make a good plan. They just couldn't tell if anyone followed it."),
      ('p', 'Rebalancing means moving vehicles from quiet areas to busy ones, and swapping batteries and pulling broken ones along the way. Managers planned shifts in a web dashboard, operators worked from a mobile app, and everything in between happened over Slack messages. Performance was measured by operators reporting their own counts.')],
     [('Operators', 'A crowded app', 'The mobile app mirrored the dashboard feature for feature, so it was dense with no clear next step.'),
      ('Managers', 'No way to check', 'Tasks went out by message, and there was no record of which ones got done.')])
text_only(d, 'nr-research', [('eyebrow', '02'), ('h2', 'Remote interviews, then shadowing in the field'), ('st', 'I needed to see how operators decide what to do next, on the street.'),
      ('p', 'I interviewed operations managers remotely across countries and cities of different sizes, then shadowed ground operators on shift in Melbourne and Perth. Watching them juggle a plan against what they found on the ground shaped almost every decision that followed.')])
side(d, 'nr-tasks', [('eyebrow', '03'), ('h2', 'Tasks you can assign, and see done'), ('st', "A manager assigns a task on the map, and it lands in that operator's list."),
      ('p', 'Each task says what to do and where: battery swap, pick up or deploy, the vehicle, its battery and the nearest station, plus who assigned it and when. Operators filter by task type, and closed tasks move out of the way. Because assignments are now recorded, managers finally get a real measure of a shift: how many assigned tasks got done.')],
     framed(A, 'm-nr-live', 'Assigning tasks on the map', 900, 640, pad=36), 900)
stats_slide(d, 'nr-results', '03 · Results', 'Less chasing, more doing',
            [('90%+', 'less reliance on Slack for task updates and completion'), ('10%', 'more efficient field operations, with task adherence tracked for the first time')])
text_only(d, 'nr-merge', [('eyebrow', '04'), ('h2', 'Two platforms, one stack'), ('st', 'Two web tools had grown into each other.'),
      ('p', 'Dashboard ran on Angular and handled operations. Tech House was built by the backend team for themselves on React, then gradually handed to ops. That left duplicated data, overlapping features, and developers maintaining two front ends. I audited both, sat with the teams using them to learn why each page existed, and rebuilt the information architecture around what was really different.'),
      ('p', "We merged onto React with a component library built on Ant Design and adjusted to Neuron's look, so components stayed cheap to build without looking borrowed. The migration finished ahead of schedule, and several tools became simple enough to hand from developers to city teams.")])

# ------------------------------------------------------------------ Close
d.section('close', 'Contact.', '')
closing(d, 'close', "Think less, not thoughtless. Let's make better products together.", ['mancini.tan@gmail.com', 'mancinitan.com', 'linkedin.com/in/mancini-tan-37544b114'])
print(d.write(), 'slides')
