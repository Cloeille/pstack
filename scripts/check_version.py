#!/usr/bin/env python3
"""Fail when HEAD changes files relative to a base ref without raising plugin.yaml's version."""
import re, subprocess, sys

def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout

def version(text):
    m = re.search(r'^version:\s*["\']?(\d+)\.(\d+)\.(\d+)["\']?\s*$', text, re.M)
    if not m: sys.exit("plugin.yaml: no MAJOR.MINOR.PATCH version found")
    return tuple(map(int, m.groups()))

base = sys.argv[1]
head_v = version(git("show", "HEAD:plugin.yaml"))
base_v = version(git("show", f"{base}:plugin.yaml"))
if git("diff", "--name-only", f"{base}...HEAD").strip() and head_v <= base_v:
    fmt = lambda v: ".".join(map(str, v))
    print(f"plugin.yaml version {fmt(head_v)} must be greater than {fmt(base_v)} on {base}. "
          "Bump it: patch for fixes and wording, minor for new skills or playbooks, major for breaking renames.")
    sys.exit(1)
print("OK")
