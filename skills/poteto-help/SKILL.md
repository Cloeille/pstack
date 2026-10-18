---
name: poteto-help
description: "Answer questions about pstack skills, setup, and fixes."
version: 0.1.0
author: poteto (Hermes adaptation)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [help, workflow, reference]
    related_skills: [poteto-mode]
---

# Poteto help

Answer the user's question about pstack, hand them a prompt they can send, and link the file the answer came from. For a help question, don't start the work. The user asked how, and a pstack run spends real tokens, so let them send the prompt.

A message that asks for work, such as "use pstack to fix this bug", is not a help question. Load `pstack:poteto-mode`, do the work under it, and mention once that `pstack:poteto-help` maps the rest of the system.

This skill maps questions to the skills and guide pages that hold the answers. Those files own the details. Read the file you route to before you quote it, and trust it when it disagrees with this map. Paths below are relative to this plugin, which lives at `~/.hermes/plugins/pstack/`. Give the user the path, not a URL, because the plugin is installed locally.

In this fork every skill is a Hermes skill. Invoke it as `/pstack:<name>` in the CLI or TUI, or ask for the `pstack:<name>` skill by name and the agent loads it. There is no bare `/how` command.

## Find out what they need

Infer the need from the message and the conversation. A named situation, such as "which skill reviews a PR?", goes straight to its section. If the need is still unclear, ask one multiple-choice question with these options, then answer only the section they pick:

- Get set up
- Start a task with `pstack:poteto-mode`
- Pick a skill for a situation
- Fix a run that went wrong
- Make pstack my own

Check the state that changes the answer, and mention it only when it does:

- Empty `delegation.model` and `delegation.reasoning_effort` in `hermes config get delegation` means `pstack:setup-pstack` hasn't run, so every delegate runs on the parent chat's model and budget.
- No `verify-*` skill or other app harness in the project means agents have no scripted way to drive the app. Mention `pstack:create-verification-skill` when the question is about proving a change works.

When the delegation settings are unset and it matters, ask whether the user wants to pick a model and a reasoning budget for delegates now. It matters when the user is new, the question is about setup or cost, or the answer depends on which model runs. Ask at most once per chat. If the need is also unclear, ask both questions together. Offer two choices:

- Now: give them `/pstack:setup-pstack` to run, and answer their question too.
- Later: answer their question, and add one line saying delegates keep inheriting the parent model until they run `/pstack:setup-pstack`.

## Get set up

1. Install the plugin by symlinking it into the profile plugins directory, then register its skills for slash commands:

   ```bash
   ln -s /path/to/pstack ~/.hermes/profiles/<profile>/plugins/pstack
   hermes config set skills.external_dirs '["plugins/pstack/skills"]'
   ```

2. Run `/pstack:setup-pstack`. It asks for a reasoning budget, picks the delegate model, and writes `delegation.reasoning_effort`, `delegation.model`, and `delegation.provider`. The settings apply to new sessions.
3. Start a real task with `/pstack:poteto-mode`, a goal, and a check that can pass or fail.

Installing changes nothing until the user invokes a skill. The [README](../../README.md) and [guide page 1](../../docs/guide/01-setup.md) have the details. Offer to word their first prompt with them, per [recipes](references/recipes.md).

If cost is the worry, say where the tokens go and how to spend fewer. pstack spends extra tokens on subagents and review panels. Rerun `/pstack:setup-pstack` and pick a smaller budget or a cheaper delegate model. Leaving `delegation.model` unset makes every delegate inherit the parent chat model, which saves tokens when the chat runs on a cheap model. A shorter panel list runs fewer subagents, one for each entry. Save `pstack:poteto-mode` for work that needs rigor.

The skills use the plain Agent Skills format, so other tools can read them. This fork runs on Hermes tools: `delegate_task` for subagents, `cronjob` for scheduled runs, `session_search` for history. Work that assumed a fleet of background workers maps onto those.

## Start a task with `pstack:poteto-mode`

`pstack:poteto-mode` matches the task to a playbook, copies the playbook's steps into the todo list, and runs the other skills as the steps need them. A step it skips stays in the list as `skip: <reason>`. A good prompt states the goal and how to tell it's done. It doesn't list skills, because a hand-written sequence tends to drop or reorder steps the playbook would keep. Read [recipes](references/recipes.md) before you help word one. [Guide page 2](../../docs/guide/02-poteto-mode.md) has examples.

How long it stays on:

- Typing `/pstack:poteto-mode` attaches the skill to the turn you send. The agent keeps using it while the task runs and drops it when the subject changes.
- For work that spans many turns, say so in the same message: "stay in poteto-mode until this lands". That keeps the orchestrator loaded across the session.
- There is no Custom Mode in Hermes. To make it the default for a project, put the instruction in the project's `AGENTS.md`, which Hermes loads every session.

Mid-chat, "new task" makes the mode match a fresh playbook. `pstack:poteto-mode` already runs its playbook steps as `delegate_task` subagents. To get the same style from a subagent of your own, say in the delegate prompt that it runs under the `pstack:poteto-mode` skill.

## Pick a skill

The default answer is `pstack:poteto-mode`, which runs most of the others when its steps need them. Name a skill directly when the user wants more or less of something than the playbook gives. Read the skill before you recommend it, and give one example prompt.

| The user wants to | Skill |
|---|---|
| Do any non-trivial task with rigor | [`pstack:poteto-mode`](../poteto-mode/SKILL.md) |
| Check that the agent understood their goal and the problem before it starts | [`pstack:in-your-own-words`](../in-your-own-words/SKILL.md) |
| Aim a task higher before starting: more expert, more outcome-focused, not overspecified | [`pstack:sharpen`](../sharpen/SKILL.md) |
| Know how code works now, or where new code should live | [`pstack:how`](../how/SKILL.md) |
| Know why code is shaped this way, or where a number came from | [`pstack:why`](../why/SKILL.md) |
| Understand a change or subsystem, explained plainly | [`pstack:teach`](../teach/SKILL.md) |
| Catch up on their own recent work on a topic | [`pstack:recall`](../recall/SKILL.md) |
| Catch up on what changed in this chat since their last message, in plain words and small visuals | [`pstack:ketchup`](../ketchup/SKILL.md) |
| Know what a small diff could break outside itself | [`pstack:blast-radius`](../blast-radius/SKILL.md) |
| Settle types and module shape before code that crosses a function boundary | [`pstack:architect`](../architect/SKILL.md) |
| Get several attempts at one brief, merged into the best one | [`pstack:arena`](../arena/SKILL.md) |
| Run parallel checks over slices, or race workers | [`pstack:swarm`](../swarm/SKILL.md) |
| Have different reviewers read a diff and try to break it | [`pstack:interrogate`](../interrogate/SKILL.md) |
| Fix a bug test-first when a cheap local test exists | [`pstack:tdd`](../tdd/SKILL.md) |
| Apply TypeScript rules to `.ts` or `.tsx` work | [`pstack:typescript-best-practices`](../typescript-best-practices/SKILL.md) |
| Strip comments before review, using a reviewer that didn't write them | [`pstack:no-comments`](../no-comments/SKILL.md) |
| Clean AI tells out of prose | [`pstack:unslop`](../unslop/SKILL.md) |
| Clean AI code slop out of a diff | [`pstack:deslop`](../deslop/SKILL.md) |
| Make a repeated agent mistake impossible to repeat | [`pstack:correct`](../correct/SKILL.md) |
| Write docs, an RFC, a README, a PR description, or a commit message to a standard | [`pstack:technical-writing`](../technical-writing/SKILL.md) |
| Hear the last reply again in plain words | [`pstack:bro`](../bro/SKILL.md) |
| Give agents a scripted way to drive the app and prove behavior | [`pstack:create-verification-skill`](../create-verification-skill/SKILL.md) |
| Keep a verification skill and its feature map current | [`pstack:maintain-verification-skill`](../maintain-verification-skill/SKILL.md) |
| Formally verify a race, invariant, or other property that tests rarely reach | [`pstack:create-formal-verification-skill`](../create-formal-verification-skill/SKILL.md) |
| Vet a performance number before reporting or acting on it | [`pstack:benchmark-checklist`](../benchmark-checklist/SKILL.md) |
| Run a large or cross-cutting change, or one to review after stepping away | [`pstack:figure-it-out`](../figure-it-out/SKILL.md) |
| Keep a decision log during a run, and review it afterward | [`pstack:show-me-your-work`](../show-me-your-work/SKILL.md) |
| Pick the delegate model and a reasoning budget | [`pstack:setup-pstack`](../setup-pstack/SKILL.md) |
| Turn their own working habits into a personal mode skill | [`pstack:automate-me`](../automate-me/SKILL.md) |
| Turn what a finished task taught into skill edits | [`pstack:reflect`](../reflect/SKILL.md) |
| Find their way around pstack | `pstack:poteto-help` |

If a skill directory next to this one is missing from the table, which happens when the fork grows, read its frontmatter and route by its description. The `principle-*` directories are covered under principles below.

Close calls:

- `pstack:how` explains what the code does. `pstack:why` explains the reasons. `pstack:teach` runs one or both and explains the result plainly.
- `pstack:architect` settles the design, then implements. Add "with checkpoint" to review the design before it writes code.
- `pstack:interrogate` reviews the diff. `pstack:blast-radius` looks for breakage outside the diff and proves the one fact that makes the change safe.
- `pstack:recall` rebuilds context across past sessions. Resuming one specific session is the Session pickup playbook.
- `pstack:figure-it-out` designs one rigorous run. The Orchestrate playbook runs a program that spans days and many PRs. The Autonomous run playbook drives one task to a finish condition.
- `pstack:unslop` fixes prose. `pstack:deslop` fixes code.

Not in pstack:

- pstack has no planning skill of its own. Ask `pstack:poteto-mode` for a plan, or load the standalone `plan` skill if the profile installs one.
- There is no `/loop`. A repeating run is a `cronjob`, or the autonomous run playbook with a falsifiable finish condition.
- pstack has no `/orchestrate` skill. Orchestrate is a `pstack:poteto-mode` playbook.

## Playbooks and principles

Playbooks are step lists inside `pstack:poteto-mode`, not skills, so they have no slash command. Load one with `skill_view(name='pstack:poteto-mode', file_path='playbooks/<name>.md')`. Inside `pstack:poteto-mode`, describing the task picks one, and these phrases name one directly:

- "babysit this pr" or "check on pr 123" runs Babysit. It drives the PR to merge-ready and stops there. It doesn't merge unless the user asks to merge, land, or ship.
- "land the stack" runs Shipping.
- "take over this branch" runs Session pickup.
- "pause safely" runs Pause safely.
- "full autopilot on this queue" runs Autopilot-full. "stack them, don't ship" runs Autopilot-stack.
- "run the eval playbook" runs Eval.

Without `pstack:poteto-mode`, a phrase such as "babysit this pr" doesn't route anywhere. Say which playbook you want, or load the orchestrator first. The Playbooks section of [`poteto-mode`](../poteto-mode/SKILL.md) lists every playbook and when it applies. [Guide page 6](../../docs/guide/06-verify-and-ship.md) covers opening, babysitting, and landing a PR.

For work that spans phases or stacked PRs, ask `pstack:poteto-mode` for a plan. It writes the plan and doesn't implement it. For a design question, the Prototype playbook or `pstack:architect` settles it in code first.

Principles are one-rule skills that `pstack:poteto-mode` reads and cites in its replies. The user rarely invokes one. They steer with the names instead, as in "apply prove it works. show me the real output." Any `principle-*` skill still loads on demand when the user names it. [Guide page 8](../../docs/guide/08-principles.md) lists them.

## Fix a run that went wrong

| Symptom | Fix |
|---|---|
| The mode stopped applying after a few turns | It was attached to one turn. Ask for `pstack:poteto-mode` again, or say "stay in poteto-mode until this lands". |
| A question got treated as the next step of the last task | Say "new task", or say the turn doesn't need the mode. |
| A new model choice had no effect | `pstack:setup-pstack` writes Hermes config, which loads at session start. Start a new session. |
| Runs cost more than expected | See the cost paragraph under Get set up. |
| A skill didn't load on its own | Skills load when you type `/pstack:<name>` or the orchestrator loads them, and it doesn't load every skill. Ask for the skill by name. |
| Parallel agents overwrote each other | Subagents share the workspace. Partition by file, give each one its own scope, and have the orchestrator merge. |
| An overnight run moved but finished nothing | Give it a check that can pass or fail, not a duration. See [guide page 7](../../docs/guide/07-overnight.md). |
| The reply claims success from a green build | Ask for the real command, flow, stored value, or profile. That's the prove-it-works principle. |

For a run that drifts, [recipes](references/recipes.md) has one-line steers. [Guide page 10](../../docs/guide/10-recipes-and-pitfalls.md) has more pitfalls and the recipes worth copying.

## Make pstack my own

- [`pstack:automate-me`](../automate-me/SKILL.md) drafts a personal mode skill from the user's own history, to use alongside `pstack:poteto-mode`.
- [`pstack:reflect`](../reflect/SKILL.md) after a session turns its lessons into skill edits the user approves.
- `pstack:poteto-mode write a skill for <workflow>` runs the authoring playbook. The eval playbook tests a skill change blind.
- Fix a misbehaving skill in its own change, not inside the feature work where it went wrong.

[Guide page 9](../../docs/guide/09-make-it-yours.md) covers each of these.

## Reply

Lead with the answer. Give at most one example prompt in a code block, adapted from [recipes](references/recipes.md) when one fits, then the link to that file. Keep it short unless the user asked for the whole map.
