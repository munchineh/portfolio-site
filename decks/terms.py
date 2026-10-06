"""Jargon notes for the presenting script. Each slide id maps to (term, short plain-English explanation).
These go under the script in the speaker notes and the script doc, never on the slide itself."""

TERMS = {
    'about': [
        ('Content design', 'Designing the words and information in a product, such as labels, messages and flows, so people can understand and act.'),
        ('Conversation design', 'Designing how a chatbot or voice assistant talks: what it says, when, and how it handles different replies.'),
        ('Localization', 'Adapting a product for another market, covering language, currency, formats and cultural fit, beyond straight translation.'),
    ],
    'evn-title': [
        ('Free size', 'One size cut to fit a range of bodies, usually relaxed, instead of S, M and L.'),
        ('Liquid', "Shopify's templating language, used to build store themes."),
    ],
    'evn-problem': [
        ('Add-to-cart', 'When a shopper puts an item in their cart. A low add-to-cart rate on a busy page means people are interested but hesitating.'),
    ],
    'evn-touch': [
        ('Touchpoint', 'Any point where a customer meets the brand or product, such as a page, an email or a popup.'),
        ('Social judgment theory', 'A psychology theory that people judge a message against what they already believe, and reject ideas that sit too far from it.'),
        ('Collection', 'A Shopify listing page that groups products, like a category page.'),
    ],
    'evn-store': [
        ('Information architecture (IA)', 'How content is organised, grouped and labelled so people can find things.'),
        ('Taxonomy', 'The system of categories and tags used to classify products.'),
        ('Funnel and session data', 'Funnel data shows where people drop off between steps, like product page to cart to checkout. Session data shows what individual visitors did on the site.'),
        ('Conversion', 'A visitor completing the goal, usually a purchase.'),
        ('MCP (Model Context Protocol)', 'An open standard that lets an AI assistant connect to other tools. The Shopify MCP lets Claude read and work with a store.'),
    ],
    'okx-title': [
        ('Click-through', 'A tap or click on an entry point, here opening Crypto Rewind.'),
        ('DAU (daily active users)', 'The number of unique people who use a product on a given day.'),
        ('Component library', 'A shared set of reusable UI parts, like buttons and cards, that designers and engineers build from.'),
    ],
    'ai-problem': [
        ('Simple Buy', "OKX's quick-buy flow: you get a locked-in price for a few seconds and buy in one step."),
        ('Spot trade', 'Buying or selling at the current market price on the exchange order book. Usually a better rate, but more steps.'),
        ('Handover', 'The point where a conversation passes between the app, the bot and a human agent.'),
    ],
    'ai-prompt': [
        ('System prompt', 'The standing instructions an AI model reads before every conversation. It sets its role, tone and rules.'),
        ('Persona', 'The character the bot plays, which keeps its voice consistent.'),
        ('Guardrails', 'Hard rules the bot must never break, such as never assuming a currency.'),
        ('Edge cases / happy path', 'The happy path is the ideal, expected flow. Edge cases are the unusual situations off it.'),
        ('Few-shot examples', 'A few sample conversations included in the prompt to show the model what good looks like.'),
        ('Hallucination', 'When an AI model states something false with confidence, like a rate that does not exist.'),
        ('USDT', 'Tether, a stablecoin pegged to the US dollar.'),
    ],
    'ai-results': [
        ('Benchmarking', 'Running the bot through a fixed set of test questions to measure quality consistently.'),
        ('Red-teaming', 'Deliberately trying to break a system, here by trying to talk the bot into things it should refuse.'),
        ('Limit order', 'An order to buy or sell only at a set price or better. The bot only supported market orders, which fill at the current price.'),
        ('Intent check', "A step where the bot confirms what the person wants before acting, like the amount and currency."),
    ],
    'orbit': [
        ('Orbiter', "OKX's name for featured traders in Orbit: high-value customers whose posts and trades drive engagement."),
        ('Engagement', 'How much people interact with a product, such as posting, following, commenting or sharing.'),
    ],
    'orbit-result': [
        ('DAU (daily active users)', 'The number of unique people who use a product on a given day.'),
    ],
    'rewind-story': [
        ('Year in review', "A personalised recap of a user's year, like Spotify Wrapped."),
        ('Audit', 'A structured review of past work, here the earlier campaigns, to see what worked and what did not.'),
        ('Dynamic content', 'Content that changes per user based on their data, so each person sees their own version.'),
    ],
    'rewind-share': [
        ('Rarity tag', 'A label showing how uncommon a persona is, which makes it more fun to compare and share.'),
        ('Share sheet', 'The panel that slides up with sharing options, like Telegram, WhatsApp or X.'),
    ],
    'rewind-goals': [
        ('Amplitude', 'A product analytics tool that tracks what users do in an app.'),
        ('Completed journey', 'A user who reached the end of Rewind.'),
        ('Red Dot', 'Red Dot Design Award, a well-known international design prize.'),
    ],
    'bl-title': [
        ('SaaS', 'Software as a service: software you subscribe to and use online.'),
        ('Pre-construction', 'Everything before building starts: planning, quoting, scheduling and approvals.'),
        ('Gantt chart', 'A timeline chart that shows tasks as bars across dates, so you can see order and overlap.'),
        ('Founding designer', 'The first designer at a startup, responsible for the whole product design from the start.'),
        ('Design system', 'Shared components, styles and rules that keep a product consistent and faster to build.'),
        ('Async', 'Working without real-time meetings, through written updates and comments across time zones.'),
    ],
    'bl-form': [
        ('Progressive disclosure', 'Showing only what is needed now and revealing more detail on demand, to keep complex screens manageable.'),
        ('RFI (request for information)', 'A formal construction question sent to the client when something needs their answer before work can continue.'),
    ],
    'bl-mobile': [
        ('Chips', 'Small rounded buttons or tags, often used to filter or switch between options.'),
        ('Accordion', 'A section that expands and collapses when tapped.'),
        ("Thumb's reach", 'The area of a phone screen you can comfortably tap with one thumb, usually the lower middle.'),
    ],
    'nv-title': [
        ('Service recovery', 'What a company does to fix things after something goes wrong for a customer, like a lost or late parcel.'),
        ('Service design', 'Designing the whole service across people, processes and tools, including behind the scenes, beyond the screens.'),
        ('CRM', 'Customer relationship management software, where agents track customers and cases. Ninja Van used Salesforce.'),
        ('Case logging', 'Recording a customer issue as a case so it can be tracked and resolved.'),
    ],
    'nv-research': [
        ('SUS (System Usability Scale)', 'A standard 10-question survey that scores how usable a system feels, from 0 to 100.'),
        ('CES (Customer Effort Score)', 'A survey asking how easy it was to get an issue resolved.'),
    ],
    'nv-portal': [
        ('Self-serve portal', 'An online space where customers can do things themselves, like raise and track issues, without calling support.'),
        ('Close the loop', 'Following up after feedback so the customer sees it was acted on.'),
    ],
    'nv-results': [
        ('Design system', 'Shared components, styles and rules that keep products consistent. Akira is Ninja Van\'s.'),
        ('Design library', 'A shared file of reusable components that designers pull from, for example in Figma.'),
    ],
    'nr-title': [
        ('Micromobility', 'Small shared vehicles for short trips, like e-scooters and e-bikes.'),
        ('Ground operators', 'Field staff who move, charge, fix and rebalance the vehicles around the city.'),
        ('PRD (product requirements document)', 'A document that sets out what a feature should do, used to align product, design and engineering.'),
    ],
    'nr-tasks': [
        ('Shadowing', 'Watching people do their real work in their own environment, to see what they actually do and not only what they say.'),
    ],
    'nr-merge': [
        ('React and Angular', 'Two popular frameworks for building web interfaces.'),
        ('Ant Design', 'An open-source React component library, which we restyled to look like Neuron.'),
        ('Front end', 'The part of software people see and use, as opposed to the back end that stores and processes data.'),
    ],
}


def notes_block(sid):
    """Terms as plain text for the slide's speaker notes."""
    items = TERMS.get(sid)
    if not items:
        return ''
    return '[[br]][[br]]Terms[[br]]' + '[[br]]'.join(f'· {t}: {x}' for t, x in items)


def doc_block(sid):
    """Terms as markdown for the script doc."""
    items = TERMS.get(sid)
    if not items:
        return ''
    return '\n\n*Terms*\n\n' + '\n'.join(f'- **{t}:** {x}' for t, x in items)
