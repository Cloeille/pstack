---
name: memory-provider
description: "Provider-specific notes for Hermes memory tools."
version: 0.1.0
author: pstack contributors
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [memory, workflow]
    related_skills: [pstack:recall, pstack:reflect]
---

# Memory provider

## When to Use

Optional notes for one Hermes memory provider. `pstack:recall` and `pstack:reflect` detect memory tools from their own tool list and read the matching `references/<provider>.md` directly. They do not load this file. Read it when adding notes for a new provider.

## Roles

Skills name roles, never provider tools, so they work with any provider:

- **Search.** Return stored facts relevant to a query.
- **Store.** Persist one durable fact.
- **Synthesize.** Optional. Reason over many stored facts. For patterns, not lookups.

The tool descriptions are enough to map a provider onto these roles. A notes file only adds what descriptions miss: quirks, costs, and how to cite results.

## Adding notes for a provider

Write `references/<provider>.md`, where `<provider>` is the prefix of the provider's tool names. List the tool for each role, the arguments that matter, and the pitfalls. Only name tools you have seen in a real tool list. Keep it short: it is read on every `recall` and `reflect` run for that provider.
