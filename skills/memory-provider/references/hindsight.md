# Hindsight notes

Provider `hindsight`. Tools come from the Hermes Hindsight memory plugin.

## Roles

- **Search.** `hindsight_recall(query)`. Ranked facts across sessions, already deduplicated. One topic per query. Run two or three narrow queries (the feature, the repo, the bug) rather than one broad one.
- **Store.** `hindsight_retain(content, context, occurred_at, tags)`. `content` is one self-contained fact. `context` is a short label such as `project decision` or `user preference`. Pass `occurred_at` (ISO-8601) when the fact is about an event, omit it for timeless facts.
- **Synthesize.** `hindsight_reflect(query)`. Reasons over many memories. Slower and more expensive than recall. Use it for cross-session patterns, not lookups.

## Quirks

- Hermes injects a block of recalled memories into the user turn on its own. Read it before calling `hindsight_recall`. Do not query again for what it already holds.
- Facts are extracted and paraphrased. They carry a `When:` date, not a session id. Cite them as `hindsight (<date>)`. When an exact quote or a session id matters, confirm in `session_search`.
- Extraction can merge or misattribute details. A fact that drives an action (a branch name, a PR number, a decision) gets checked against live state before you act on it.
- `hindsight_reflect` is a provider tool. It is not `pstack:reflect` and does not edit skills.
- Retain can be slow. Batch the approved facts and retain them after the skill edits, so a timeout does not block the rest of the run.
