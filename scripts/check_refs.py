#!/usr/bin/env python3
"""Reject broken markdown links, skill references, playbook references, Cursor leftovers, and prose drift."""
from pathlib import Path
import re, sys

ROOT = Path(__file__).resolve().parents[1]
SKILLS = {p.name for p in (ROOT / "skills").iterdir() if (p / "SKILL.md").is_file()}
errors = []
files = list(ROOT.rglob("*.md"))

CURSOR_LEFTOVERS = re.compile(
    r"\.cursor/|~/\.cursor|pstack-models\.mdc|AskQuestion|subagent_type"
    r"|\bTask tool\b|\bTask\(|`Read`|`Grep`|`Glob`|`Shell`|StrReplace"
    r"|agent-transcripts|orch\.ts|Hermes session history/"
)

for path in files:
    text = path.read_text(encoding="utf-8")
    no_fenced = re.sub(r"```.*?```", "", text, flags=re.S)
    clean = re.sub(r"`[^`]*`", "", no_fenced)
    for target in re.findall(r"\[[^]]*\]\(([^)]+)\)", clean):
        target = target.split("#", 1)[0]
        if target and not re.match(r"(?:https?:|mailto:|#|<)", target):
            if not (path.parent / target).resolve().exists():
                errors.append(f"{path.relative_to(ROOT)}: broken link {target}")
    for name in re.findall(r"pstack:([A-Za-z0-9_-]+)", text):
        if name not in SKILLS:
            errors.append(f"{path.relative_to(ROOT)}: missing skill pstack:{name}")
    for name in re.findall(r"file_path=['\"]playbooks/([^'\"]+)", clean):
        if not (ROOT / "skills/poteto-mode/playbooks" / name).exists():
            errors.append(f"{path.relative_to(ROOT)}: missing playbook {name}")
    if path.is_relative_to(ROOT / "skills") or path.is_relative_to(ROOT / "docs"):
        if "—" in text:
            errors.append(f"{path.relative_to(ROOT)}: em dash")
        for lineno, line in enumerate(text.splitlines(), 1):
            if "github.com/cursor/plugins" in line:
                continue
            m = CURSOR_LEFTOVERS.search(line)
            if m:
                errors.append(f"{path.relative_to(ROOT)}:{lineno}: Cursor leftover {m.group(0)!r}")
    if path.name == "SKILL.md":
        head = text.split("---", 2)[1] if text.startswith("---") else ""
        for field in ("name:", "description:", "version:", "author:", "license:", "platforms:", "metadata:", "hermes:", "tags:", "related_skills:"):
            if field not in head: errors.append(f"{path.relative_to(ROOT)}: missing frontmatter {field}")
        m = re.search(r"^description:\s*[\"']?(.*?)[\"']?\s*$", head, re.M)
        if m and len(m.group(1).strip('"')) > 60: errors.append(f"{path.relative_to(ROOT)}: description over 60 chars")
if errors:
    print("\n".join(errors)); sys.exit(1)
print(f"checked {len(files)} markdown files, {len(SKILLS)} skills")
