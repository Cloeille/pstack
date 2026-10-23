#!/usr/bin/env python3
"""Reject broken markdown links, skill references, playbook references, Cursor leftovers, and prose drift."""
from pathlib import Path
import importlib.util, re, sys

ROOT = Path(__file__).resolve().parents[1]
SKILLS = {p.name for p in (ROOT / "skills").iterdir() if (p / "SKILL.md").is_file()}
errors = []
files = list(ROOT.rglob("*.md"))

class Ctx:
    registered = []
    def register_skill(self, name, path, description="", **kwargs): self.registered.append((name, Path(path), description))

spec = importlib.util.spec_from_file_location("pstack_init", ROOT / "__init__.py")
loader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(loader)
loader.register(ctx := Ctx())
DANGLING = re.compile(r"(?: (?:and|or|a|the|with|of|to|for|from|that|your)|[:,.])\.$")
for name, path, description in ctx.registered:
    if path.name != "SKILL.md" or not path.is_file():
        errors.append(f"__init__.py: {name} registered with {path}, not a SKILL.md file")
        continue
    text = path.read_text(encoding="utf-8")
    m = re.search(r"^description:\s*([\"']?)(.*)\1\s*$", text.split("---", 2)[1] if text.startswith("---\n") else "", re.M)
    if not text.startswith("---\n"):
        errors.append(f"skills/{name}/SKILL.md: frontmatter must start with '---' on its own line")
    if not description:
        errors.append(f"__init__.py: {name} registered with empty description")
    elif not m or description != m.group(2):
        errors.append(f"__init__.py: {name} description differs from SKILL.md frontmatter")
    if len(description) > 60:
        errors.append(f"skills/{name}/SKILL.md: description over 60 chars")
    if not description.endswith("."):
        errors.append(f"skills/{name}/SKILL.md: description must end with a period")
    if DANGLING.search(description):
        errors.append(f"skills/{name}/SKILL.md: description looks cut mid-sentence: {description!r}")
if {n for n, _, _ in ctx.registered} != SKILLS:
    errors.append("__init__.py: registered skills differ from skills/ directories")

CURSOR_LEFTOVERS = re.compile(
    r"\.cursor/|~/\.cursor|pstack-models\.mdc|AskQuestion|subagent_type"
    r"|\bTask tool\b|\bTask\(|`Read`|`Grep`|`Glob`|`Shell`|StrReplace"
    r"|agent-transcripts|orch\.ts|Hermes session history/"
    r"|environment: \"cloud\"|cursor-team-kit|control-ui|control-cli|orch ledger|cloud agent"
    r"|\bgt (?:submit|restack|sync|log|create|modify|checkout)\b"
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
if errors:
    print("\n".join(errors)); sys.exit(1)
print(f"checked {len(files)} markdown files, {len(SKILLS)} skills")
