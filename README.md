# pstack — Hermes Plugin

Poteto's engineering rigor stack, adapted for [Hermes Agent](https://hermes-agent.nousresearch.com).

Fork of [pstack](https://github.com/cursor/plugins/tree/main/pstack) by poteto (Meta/Netflix/Cursor, React core team). Originally built as a Cursor plugin, rebuilt here as a Hermes plugin with native skills, delegate_task orchestration, and playbook routing.

## What it does

One orchestrator skill (`poteto-mode`) that routes tasks to playbooks and enforces principles. Five satellite skills for specific capabilities.

| Skill | Purpose |
|-------|---------|
| `pstack:poteto-mode` | Orchestrator. Task → playbook routing, principles, autonomy rules, delegation patterns. |
| `pstack:how` | Codebase exploration. "How does X work?" with explain/critique modes. |
| `pstack:architect` | Design types and module boundaries before implementing. "Design it twice." |
| `pstack:interrogate` | Multi-reviewer adversarial code review via parallel delegates. |
| `pstack:swarm` | Fan out N parallel workers, drain, report. |
| `pstack:unslop` | Strip AI writing patterns. Apply to all prose. |
| `pstack:setup-pstack` | Pick the model and reasoning budget delegates use. Writes Hermes `delegation` config. |

## Playbooks

Loaded via `skill_view(name='pstack:poteto-mode', file_path='playbooks/<name>.md')`:

- `investigation.md` — read-only question, trace behavior
- `bug-fix.md` — reproduce, root-cause, fix with evidence
- `feature.md` — plan, design, delegate, verify
- `perf-issue.md` — measure, profile, fix, measure again
- `refactoring.md` — behavior-preserving restructuring
- `autonomous-run.md` — long task with falsifiable exit predicate
- `figure-it-out.md` — large/cross-cutting work, design your own workflow

## Guide

Read the guide in order the first time. After that, each page stands alone.

1. [Set up pstack](docs/guide/01-setup.md) — install, pick models, first task
2. [Route work through poteto-mode](docs/guide/02-poteto-mode.md) — give it a goal, watch it pick a playbook
3. [Understand the code](docs/guide/03-understand.md) — pstack:how before you edit anything
4. [Design the change](docs/guide/04-design.md) — pstack:architect and pstack:interrogate before code locks in
5. [Build and clean](docs/guide/05-build-and-clean.md) — build playbooks, TDD, unslop
6. [Verify and ship](docs/guide/06-verify-and-ship.md) — prove behavior, open a PR, merge
7. [Run work overnight](docs/guide/07-overnight.md) — autonomous contracts, decision logs
8. [Principles](docs/guide/08-principles.md) — the full set in detail
9. [Make it yours](docs/guide/09-make-it-yours.md) — customize skills and playbooks
10. [Recipes and pitfalls](docs/guide/10-recipes-and-pitfalls.md) — prompts to copy, mistakes to skip

## Slash commands

Add the plugin's skills directory to `skills.external_dirs` so each skill registers as a slash command:

```bash
hermes config set skills.external_dirs '["plugins/pstack/skills"]'
```

Then in any chat session:

| Command | What it does |
|---------|--------------|
| `/poteto-mode` | Load the orchestrator (task routing, principles, delegation). |
| `/how` | Codebase exploration. "How does X work?" |
| `/architect` | Design types and boundaries before building. |
| `/interrogate` | Adversarial multi-reviewer code review. |
| `/swarm` | Fan out parallel workers. |
| `/unslop` | Strip AI writing patterns from prose. |
| `/setup-pstack` | Pick the delegate model and reasoning budget. |

Append an instruction after the command: `/how how does auth work in this repo`

Skills are also loadable programmatically via `skill_view(name='pstack:<skill>')`.

## Install

Symlink or copy into your Hermes profile plugins directory:

```bash
ln -s /path/to/pstack ~/.hermes/profiles/<profile>/plugins/pstack

# Enable slash commands
hermes config set skills.external_dirs '["plugins/pstack/skills"]'
```

Hermes loads it on next session start.

## License

MIT
