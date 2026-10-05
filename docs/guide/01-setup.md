# Set up pstack

> Originally by [poteto](https://github.com/poteto) for [Cursor pstack](https://github.com/cursor/plugins/tree/main/pstack). Adapted for Hermes Agent.

In this page you install the plugin, pick which models pstack uses, and run your first task. Setup is one command plus a short conversation.

## Install the plugin

Install via the Hermes CLI:

```text
hermes plugin add pstack
```

Hermes confirms the plugin is installed.

## Pick your models

Load the setup skill:

```text
load pstack:setup-pstack
```

[`pstack:setup-pstack`](../../skills/setup-pstack/SKILL.md) reads your current Hermes config, detects the models you can route to, asks for a reasoning budget and a delegate model, then writes Hermes' native `delegation` settings (`delegation.model`, `delegation.provider`, `delegation.reasoning_effort`). Every `delegate_task` call pstack makes reads them.

Pick `inherit-parent` to keep delegates on your chat model. A rerun overwrites the same keys. To go back to the default, run `hermes config unset delegation.model`.

Hermes runs every delegate of one call on the same delegation model. Panels in `pstack:interrogate` and `pstack:architect` get their independence from separate subagents and distinct prompts. For a multi-model panel, change `delegation.model` between runs.

## Accept the verification offer, or don't

At the end of setup, `pstack:setup-pstack` checks whether your project has a way to prove app behavior, either a `verify-*` skill or an existing harness. If it finds neither, it says so once and suggests writing one. [Verify and ship](./06-verify-and-ship.md#create-a-project-verification-skill) covers when it earns its place.

After setup, start a new chat. The model configuration applies to new sessions.

## Run your first task

Pick something real but small, and describe it the way you'd describe it to a colleague:

```text
load pstack:poteto-mode add a --json flag to this command. text output stays byte-identical. verify both.
```

Watch the todo list. Its first items are the matched playbook's steps copied in, the Feature playbook for this prompt. If `pstack:poteto-mode` skips a step, the step stays in the list with `skip: <reason>`, so you can see what it chose not to do.

From here you can type normal follow-ups. `pstack:poteto-mode` is sticky. It stays on for the conversation until you opt out by saying so.

Next: [Route work through `pstack:poteto-mode`](./02-poteto-mode.md).
