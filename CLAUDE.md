# AGENTS.md

Hermes Agent plugin. No build, no deps, no tests. Pure markdown skills + a tiny Python loader.

## Structure

```
plugin.yaml          # name, version, description
__init__.py          # register(ctx) - registers 6 skills, nothing else
skills/
  poteto-mode/       # orchestrator - routes tasks to playbooks
    SKILL.md
    playbooks/*.md   # 7 step-by-step procedures
  how/SKILL.md       # codebase exploration
  architect/SKILL.md # design before code
  interrogate/SKILL.md # adversarial multi-reviewer
  swarm/SKILL.md     # parallel fan-out
  unslop/SKILL.md    # strip AI writing patterns
```

## Editing rules

- **SKILL.md frontmatter** must have: `name`, `description` (≤60 chars, one sentence, period at end), `version`, `author`, `license`, `platforms`, `metadata.hermes.tags`, `metadata.hermes.related_skills`.
- **Cross-references** between skills use `pstack:<name>` (e.g. `pstack:how`, `pstack:architect`).
- **Playbook references** use `skill_view(name='pstack:poteto-mode', file_path='playbooks/<name>.md')`.
- **Hermes tools** to reference: `terminal`, `search_files`, `read_file`, `write_file`, `patch`, `delegate_task`, `web_search`, `web_extract`, `browser_navigate`. No Hermes Agent-specific tools (Task, cronjob, toolsets, etc.).
- **No em dashes** in any prose. Use periods or commas. This is an unslop rule that applies to the project itself.

## Adding a skill

1. Create `skills/<name>/SKILL.md` with proper frontmatter.
2. Add the name to the `SKILLS` tuple in `__init__.py`.
3. That's it. No config, no registration boilerplate.

## Adding a playbook

1. Create `skills/poteto-mode/playbooks/<name>.md`.
2. Add a row to the routing table in `skills/poteto-mode/SKILL.md`.

## What NOT to do

- Don't add Python logic beyond the loader. Skills are markdown.
- Don't add hooks or tools in `__init__.py`. This plugin registers skills only.
- Don't reference Hermes Agent-specific features (worktrees, cronjob, cloud environment, sticky mode).
- Don't write promotional or padded prose. Run unslop on yourself.

## Origin

Adapted from [poteto's pstack](https://github.com/cursor/plugins/tree/main/pstack) for Hermes Agent. The original is a Hermes Agent plugin. This version replaces Hermes Agent's Task tool with `delegate_task`, removes cloud/worktree assumptions, and reformats everything as Hermes SKILL.md files.
