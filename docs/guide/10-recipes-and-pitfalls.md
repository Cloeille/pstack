# (no title)
URL: https://raw.githubusercontent.com/cursor/plugins/main/pstack/docs/guide/10-recipes-and-pitfalls.md

# Recipes and pitfalls

Prompts worth copying, then the mistakes everyone makes once. Swap in your own paths and finish conditions. The recipes are deliberately informal. That's how they get typed in practice, and the skills read intent fine.

![She tastes a finished dish while robots cook from a recipe box, with pinned cards reading /how, /tdd, and cronjob above the counter.](./images/recipes.jpg)

## Understand an unfamiliar subsystem

```text
use /how first to understand how this initialization works. then use /why to figure out why it broke recently.
```

Mechanics first, history second. Each skill's report tells you which sources it searched, so you know what the answer is grounded in.

## Get a second opinion on a design

```text
ask /arena for a second opinion on this thread and our approach
```

Your current design becomes one candidate among several, and the synthesis tells you whether the panel found something better or confirmed what you had. Cheap insurance before a costly commitment.

## Check independent slices in parallel

```text
/swarm check every package under packages/ against its check.sh. one worker per package. one report.
```

Each worker owns one package. The parent waits for every slice and returns one `PASS`, `ISSUES`, or `BLOCKED` report instead of raw worker dumps.

## Review a branch skeptically

```text
/interrogate the whole branch, but skeptically. don't change anything yet. no nitpicks unless it's an actual bug or regression in behavior.
```

The qualifiers do real work. "don't change anything yet" keeps it read-only, and the nitpick rule pre-filters the noise so `Act on` findings are worth your time.

## Fix a bug through a failing test

```text
/poteto-mode repro the duplicate write first. if there's a cheap test path, /tdd it. then fix and rerun.
```

"if there's a cheap test path" matters. Forcing a test through brittle mocks proves less than running the real command, and the playbook is allowed to say so.

## Keep a run honest while you're away

```text
im going to bed, keep going autonomously until every fixture passes. do not stop. keep a decision log i can audit in the morning.
```

The full contract is on the [overnight page](./07-overnight.md). The short form works once the task and finish condition are already in the conversation.

## Redirect a drifting run

Steering prompts are one line:

```text
i said the goal is to repro. i did not ask for a fix yet.
```

```text
apply prove it works. show me the real output, not the build log.
```

```text
/unslop that, no emdashes
```

You rarely need more words. You need the right name, and [the principles page](./08-principles.md) is the vocabulary.

## Get the reply in plain words

```text
/bro
```

That's the whole prompt. [`/bro`](../../skills/bro/SKILL.md) restates the last message like one human talking to another, no jargon, shorter. Use it when a reply is technically thorough and you still don't know what it said.

## The pitfalls

- **Enumerating skills i