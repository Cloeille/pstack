---
name: why
description: "Use for 'why does X work this way' or 'why did we pick Y'."
version: 0.2.0
author: poteto (Hermes adaptation)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [engineering, workflow]
    related_skills: []
---

# Why

Answer from the record, not the code: read the commits and PR discussions that introduced the target and each later change (`git log --follow -p`, `git blame`, `gh pr view`), and other sources if the trail is thin. Cite what the authors wrote, mark your own inferences as inferences, and say what the record does not answer.
