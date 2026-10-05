---
name: setup-pstack
description: 'Pick the model and reasoning budget pstack delegates use.'
version: 0.1.0
author: poteto (Hermes adaptation)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [setup, configuration, models, delegation]
    related_skills: [pstack:poteto-mode, pstack:swarm, pstack:interrogate]
---

# Setup pstack

Configure the model and reasoning budget that every pstack `delegate_task` call runs on. pstack has no config file of its own. It writes Hermes' native `delegation` settings, which every subagent spawned by `pstack:poteto-mode`, `pstack:swarm`, `pstack:interrogate`, and `pstack:architect` reads.

## Steps

### 1. Load current state

Run in `terminal`:

```bash
hermes config get model
hermes config get delegation
```

Note the parent chat model (`model.default`, `model.provider`) and the current `delegation.model`, `delegation.provider`, and `delegation.reasoning_effort`. An empty value means the delegate inherits the parent.

### 2. Detect available models

List the models the user can actually route to. Use `hermes model` output, the provider's `/v1/models` endpoint, or the models already present in config. If you cannot confirm any, ask the user to paste the slugs they have. Never write a model you have not confirmed. `inherit-parent` is always valid: it means leave `delegation.model` empty so delegates run on the parent chat model.

### 3. Ask for a budget

Use `clarify` with these four choices. Name the current budget when `delegation.reasoning_effort` is set.

- `unlimited (max)`
- `large (xhigh)`
- `medium (high)`
- `small (medium)`

The value in parentheses is the `delegation.reasoning_effort` to write.

### 4. Ask for the delegate model

Use `clarify`. Offer `inherit-parent` first, then the detected models. Show the current value. If the chosen model needs a provider other than the parent's, ask for that provider too (it must already be configured in Hermes).

### 5. Write the config

```bash
hermes config set delegation.reasoning_effort <effort>
hermes config set delegation.model <slug>        # skip for inherit-parent
hermes config set delegation.provider <provider> # only if it differs from the parent
```

For `inherit-parent`, clear any old pin: `hermes config unset delegation.model` and `hermes config unset delegation.provider`. Re-running this skill overwrites the same keys, so it stays idempotent.

### 6. Verify

Run `hermes config get delegation` and check that each written key reads back as chosen. If a value did not stick, report it and stop.

### 7. Confirm

Tell the user what was written and that it applies to new sessions. Panel skills (`pstack:interrogate`, `pstack:architect`) get their diversity from independent subagents and distinct prompts. Hermes runs every delegate of one call on the same delegation model, so a multi-model panel means changing `delegation.model` between runs.

### 8. Offer a verification path (optional)

Check whether the project has a way to drive the real app for proof: a `verify-*` skill or an existing harness (e2e suite, smoke script). If it has neither, say so once and suggest writing one, so agents can prove changes the way a user would. Don't push.
