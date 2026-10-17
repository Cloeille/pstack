---name: unslop
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

- **Em dashes** - avoid entirely. Use periods or commas. Every em dash is a sentence that couldn't commit to being one or two sentences.
- **Colons as mid-sentence connectors**: "The answer is clear: we need X" - rewrite as two sentences or drop the windup
- **Rhetorical questions as transitions**: "But what does this mean?" - state it directly
- **One-sentence paragraphs for drama** - merge into surrounding paragraph or cut

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
