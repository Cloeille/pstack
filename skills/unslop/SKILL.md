---
name: unslop
description: "Cut AI tells from writing. Apply to all prose surfaces."
version: 0.1.0
author: poteto (Hermes adaptation)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [engineering, workflow]
    related_skills: []
---

# Unslop

Remove AI-generated writing patterns. Make prose sound human.

## When to Use

Apply after drafting any user-facing text: docs, READMEs, commit messages, comments, reports, emails. Run as a final pass before delivery.

## Patterns to Detect and Kill

### Content Smells

- **Puffery**: "revolutionary", "groundbreaking", "elegant" - delete or replace with specifics
- **Name-dropping**: gratuitous mentions of frameworks/people for authority - cut unless citing a source
- **Superficial -ing phrases**: "leveraging the power of", "harnessing cutting-edge" - say what it does
- **Promotional language**: "exciting", "powerful", "seamless" - state facts instead
- **Vague attributions**: "experts say", "studies show" - cite or cut

### Language Smells

- **AI vocabulary** - ban list: additionally, crucial, delve, enhance, foster, garner, interplay, intricate, landscape, pivotal, showcase, tapestry, testament, underscore, vibrant. Replace with plain words or restructure.
- **Fancy 'is' substitutes**: "represents", "constitutes", "serves as" - just say "is"
- **"Not just X but Y"** - pick the stronger claim and say it once
- **Rule of three**: "fast, reliable, and scalable" - pick the one that matters most here
- **Synonym cycling**: using three words for the same thing to sound varied - pick one and repeat it

### Style Smells

- **Em dashes** (rule 13) - avoid entirely, and en dashes and hyphens used as dashes too. Use a period or a comma, not parentheses. Every em dash is a sentence that couldn't commit to being one or two sentences.
- **Colons as mid-sentence connectors** (rule 14): "The answer is clear: we need X" - rewrite as two sentences or drop the windup. A colon before a list or an example is fine.
- **Rhetorical questions as transitions**: "But what does this mean?" - state it directly
- **One-sentence paragraphs for drama** - merge into surrounding paragraph or cut
- **Boldface and inline-header lists** (rules 15, 16): don't bold every proper noun or acronym. Drop a bold label that restates its line ("**Performance:** Performance improved..."). A bold lead-in that ends in a period and adds new detail is fine.
- **Format tells** (rules 17, 18, 19): sentence case headings, no decorative emojis, straight quotes.

### Communication, Filler, and Plain-Speech Smells

- **False ranges** (rule 12): "from X to Y" where X and Y sit on no real scale - list the topics
- **Chatbot phrases and praise openers** (rules 20, 22): "I hope this helps!", "Let me know if...", "Great question!" - respond directly
- **Filler and hedging** (rules 23, 24): "In order to" becomes "to", delete "it is important to note that", and keep one hedge at most ("may")
- **Generic conclusions** (rule 25): "The future looks bright." - state specific plans or facts
- **Abstract metaphor nouns** (rule 26): substrate, wedge, vector, locus, nexus, primitive, harness, surface (as in "API surface"), bedrock, scaffolding, modality, paradigm, gold-plating, ratchet, evacuate (for moving code), endgame, north star, flywheel - use the concrete word
- **Feelings instead of mechanisms** (rule 27): "SQL you can read" names a feeling. Name the mechanism or the number. Cut a sentence that could appear unchanged in another project's docs.
- **Dense sentences** (rule 28): one idea per sentence, split what the reader has to reread
- **Passive voice** (rule 29): name the actor unless it is unknown or doesn't matter
- **Adverbs** (rule 30): "runs quickly" becomes the number, and "significantly improves" becomes the measured delta
- **Fancy words** (rule 31): "use", not "utilize" or "leverage". "Help", not "facilitate".
- **Mannered prose** (rule 32): no aphorism, rhetorical fragment, personified code ("the plan holds it"), or figurative verb ("rides along") where a literal phrase exists. Rule 26 covers the metaphor nouns.
- **Over-compression** (rule 33): write whole sentences with their articles and verbs, and spell out arrows and abbreviations. "Parser rejects bad date → exit 2, no write" becomes "The parser rejects a bad date, exits with code 2, and writes nothing."

## Procedure

1. **Scan** - read all prose surfaces (docs, comments, UI strings) via `read_file` or `search_files`. Flag pattern matches from the lists above.

2. **Rewrite** - fix each flag. Preserve meaning. Shorter is better. Use `patch` for targeted fixes.
   - Replace banned words with plain equivalents
   - Collapse inflated phrases to direct statements
   - Break em-dash sentences into two sentences
   - Delete puffery that carries no information

3. **Add soul** - mechanical de-slopping produces bland text. After cleaning:
   - **Have opinions**: "X is better than Y because Z" beats "X and Y each have tradeoffs"
   - **Vary rhythm**: mix short sentences with longer ones. Not every sentence needs a clause.
   - **Acknowledge complexity**: "this breaks when..." is more trustworthy than "this handles..."
   - **Use 'I' when it fits**: first person beats passive voice for decisions and recommendations
   - **Let some mess in**: one imperfect-but-honest sentence beats three polished-but-empty ones
   - **Be specific**: "saves ~200ms per request" beats "significantly improves performance"

4. **Self-audit** - reread the final text. If any sentence could appear in a random AI blog post without looking out of place, rewrite it.
