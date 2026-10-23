import re
from pathlib import Path

DESCRIPTION = re.compile(r"^description:\s*([\"']?)(.*)\1\s*$", re.M)


def register(ctx):
    skills_dir = Path(__file__).parent / "skills"
    for skill_dir in sorted(p for p in skills_dir.iterdir() if (p / "SKILL.md").is_file()):
        path = skill_dir / "SKILL.md"
        match = DESCRIPTION.search(path.read_text(encoding="utf-8"))
        ctx.register_skill(skill_dir.name, path, description=match.group(2) if match else "")
