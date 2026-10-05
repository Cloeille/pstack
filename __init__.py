from pathlib import Path

SKILLS = ("poteto-mode", "unslop", "how", "interrogate", "architect", "swarm", "setup-pstack")

def register(ctx):
    skills_dir = Path(__file__).parent / "skills"
    for name in SKILLS:
        ctx.register_skill(name, skills_dir / name)
