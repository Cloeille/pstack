# Investigation Playbook

**Trigger:** "How does X work?", "Why was Y built this way?", "Should we do X or Y?"

No code changes. No PR. Read-only answer.

## Steps

1. **Route through `pstack:how`** - pick the right mode:
   - *Explain* for "how does X work" / "where does Y live"
   - *Critique* for "should we do X or Y" / "is this approach sound"

2. **Gather context** - `search_files` + `read_file` to trace the real flow end-to-end. Don't stop at the entry point; follow calls until the picture is complete. Use `web_search` / `web_extract` for external APIs or specs.

3. **Structure the answer:**
   - **Overview** - one paragraph, what it is and why it exists.
   - **Key Concepts** - named things the reader must know (types, config knobs, protocols).
   - **How It Works** - the actual flow, step by step, with file:line references.
   - **Where Things Live** - table of files/modules and their role.
   - **Gotchas** - non-obvious behavior, known limitations, easy mistakes.

4. **Apply `pstack:unslop`** - cut filler, hedging, and unrequested caveats. Every sentence earns its place with a fact or a file reference.

5. **Deliver** - the structured answer is the deliverable. No stubs, no TODOs, no "next steps" unless the user asked for a plan.

## Key Rule

This is a read operation. If you find yourself wanting to fix something, stop. Note it in Gotchas and move on. The user asked a question, not for a patch.
