from pathlib import Path


def register(ctx):
    skills_dir = Path(__file__).parent / "skills"
    for skill_dir in sorted(p for p in skills_dir.iterdir() if (p / "SKILL.md").is_file()):
        ctx.register_skill(skill_dir.name, skill_dir)
