---
name: setup-pstack
description: "Pick the models and reasoning budget pstack delegates use."
version: 0.1.0
author: poteto (Hermes adaptation)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [engineering, workflow]
    related_skills: []
---

# Setup pstack

Configure the models and reasoning budget that pstack `delegate_task` calls run on. pstack has no config file of its own. It writes Hermes' native `delegation` settings, which every subagent spawned by `pstack:poteto-mode`, `pstack:swarm`, `pstack:interrogate`, and `pstack:architect` reads. With the official `advanced-delegation` plugin, it writes one model route per pstack role, so each role can run on its own model. Without the plugin, every delegate runs on one delegation model.

## Model routes

| Route | Runs | Suggest |
|---|---|---|
| `pstack-worker` | Code delegates and routine helpers. Also the default route, when setup turns routes on and finds no default. | The current `delegation.model` on `delegation.provider`, else the parent's `model.default` on `model.provider`. |
| `pstack-strongest` | The hardest changes, judgment, prose, and synthesis. | The strongest judgment model. |
| `pstack-panel-a`, `pstack-panel-b`, ... | One member each of a review or design panel. | Models from different families. |

A pstack route is a route whose name starts with `pstack-`. Setup writes and replaces only pstack routes. Write none, or two or more `pstack-panel-*` routes, one per panel member. When setup turns routes on and `delegation.backends.model_map.default` is not set, it sets the default to `pstack-worker`, so a task that names no route runs on the `pstack-worker` model. When routes were already on, setup leaves the default alone.

## Keep keys out of the chat

Everything a `terminal` command prints enters the conversation and goes to the model provider. Hermes masks credential-shaped text in tool output by default, but the mask is a pattern match, and the user can turn it off with `security.redact_secrets`. Follow these rules.

- To read config, run only the step 1 commands. They print single values and a route summary with no keys. Do not run `hermes config get` on a whole section such as `delegation` or `model`, because it prints keys when redaction is off.
- Do not read `config.yaml`, `.env`, `auth.json`, or any other file under the Hermes home yourself. Only the step 6 script reads `config.yaml`, in memory.
- Never print the output of a `--raw` read. Only the step 1 route summary reads it, and it prints no keys.
- Do not trace or debug the step 6 script, for example by adding prints or running it under `bash -x`.
- Never write an `api_key` into a pstack route. Use a provider configured in Hermes, which keeps its key in `.env` or `auth.json`. For an endpoint that needs its own key, ask the user to add that route with `hermes delegation config`.

## Steps

### 1. Load current state

Run in `terminal`:

```bash
hermes --version
hermes plugins list --plain --no-bundled | grep advanced-delegation || echo 'advanced-delegation: absent'
for key in model.default model.provider delegation.backend delegation.model delegation.provider delegation.reasoning_effort delegation.backends.model_map.default; do
  value=$(hermes config get "$key" 2>/dev/null) || value="(not set)"
  printf '%s = %s\n' "$key" "$value"
done
hermes config get delegation.backends.model_map.options --json --raw 2>/dev/null | python3 -c '
import json, sys
text = sys.stdin.read()
for route in (json.loads(text) if text.strip() else []):
    print(route.get("name"), route.get("provider") or ("base_url" if route.get("base_url") else "MISSING"), route.get("model"), route.get("reasoning_effort", ""), route.get("description", ""), sep=" | ")
'
```

The last command prints one line per route, with its name, provider, model, reasoning effort, and description, and never its keys. Note the parent chat model, the backend, the routes, and the delegate settings. An empty delegate value means the delegate inherits the parent. The plugin line starts with `enabled`, `not enabled`, or `disabled`. Treat `not enabled` and `disabled` as installed but disabled.

### 2. Detect available models

List the models the user can actually route to, from the models step 1 printed. Ask the user to paste any other slugs they have. Do not run `hermes model`, which is an interactive picker that changes the default model. Do not call a provider's API yourself, because that needs a key. Never write a model you have not confirmed. `inherit-parent` is always valid: it means leave `delegation.model` empty so delegates run on the parent chat model.

### 3. Offer model routes

Without a plugin, Hermes runs every delegate on one model. The `advanced-delegation` plugin adds model routes. `delegate_task` then takes an `option` per task, so pstack can run each role on its own model and run each panel member on a different model.

First check that the current backend can run. `model_map` and `profile_routes` both need the plugin. When step 1 shows either backend and the plugin is disabled or absent, Hermes refuses every subagent. Say so, and ask with `clarify` whether to turn the plugin on as below. The user may have disabled or removed it on purpose. On no, go to step 4 without routes, and step 6 switches the backend back to `default`.

Then pick the branch for the backend:

- **`delegation.backend` is `profile_routes`.** The user routes delegates through Hermes profiles. pstack routes need `model_map`, and a switch changes how every delegate runs. Say so, change nothing more, and go to step 9.
- **`delegation.backend` is `model_map`.** Routes are on. Go to step 4 with routes.
- **Any other backend.** Offer model routes once with `clarify`. The choices are to map pstack roles to models, or to keep one delegate model. Say what accepting does to the plugin. When the plugin is installed but disabled, say so, because the user may have disabled it on purpose. Tell the user that one delegate model is a supported setup. On decline, go to step 4 without routes.

Turn the plugin on only after the user agrees. Match the state from step 1. When it is enabled, do nothing. When it is installed but disabled, run `hermes plugins enable advanced-delegation`. When it is absent, check that `hermes --version` is 0.22.5 or newer, then run `hermes plugins install advanced-delegation --enable`. On an older Hermes, say so and go to step 4 without routes. After an enable or install, run the plugin line from step 1 again. Continue with routes only when it starts with `enabled`. Otherwise tell the user what failed and go to step 4 without routes.

### 4. Ask for a budget

Use `clarify` with these four choices. Name the current budget when `delegation.reasoning_effort` is set, or when the pstack routes share one `reasoning_effort`.

- `unlimited (max)`
- `large (xhigh)`
- `medium (high)`
- `small (medium)`

The value in parentheses is the `reasoning_effort` to write. With routes, every pstack route gets it. Without routes, it goes to `delegation.reasoning_effort`.

### 5. Ask for the delegate models

**With routes.** Show each route from the table with its current model, or the suggestion when the route does not exist yet. Use `clarify` to accept them or change specific ones, from the detected models plus `inherit-parent`. For a route, `inherit-parent` means a route with the parent's `model.default` on `model.provider`. For the panel, propose two models from different families. Let the user add `pstack-panel-c` and more, or remove the panel. A panel keeps two or more routes, or none. If a chosen model needs a provider other than the parent's, ask for that provider too (it must already be configured in Hermes).

**Without routes.** Use `clarify`. Offer `inherit-parent` first, then the detected models. Show the current value. If the chosen model needs a provider other than the parent's, ask for that provider too (it must already be configured in Hermes).

### 6. Write the config

**With routes.** `options` is one list, and `hermes config set` replaces it whole. The merge must start from what the user wrote. `hermes config get` masks keys such as `api_key`, and `--raw` expands `${VAR}` references into the keys they point at, so a write of either output destroys the user's keys or moves them out of `.env`. Run the script below in one `terminal` call. It reads the route list from `config.yaml` with PyYAML, holds it only in memory, never prints it, and captures the output of `hermes config set`, which echoes keys unmasked.

Fill in two values first. `PSTACK_ROUTES` is the JSON list of the pstack routes the user chose. `SWITCH_BACKEND` is `True` when step 1 showed a backend other than `model_map`, else `False`. Each pstack route is an object with these keys:

- `name`, exactly as in the table.
- `description`, the one line the agent reads. Name the model in it, so the agent can pick a different family, as in `pstack worker on <model>. Code delegates and routine helpers.`
- `provider`. For a prefilled `pstack-worker`, use `delegation.provider`, or `model.provider` when that is empty. For another model on the parent's provider, use `model.provider`. Otherwise use the provider from step 5, or `base_url` for a direct endpoint.
- `model` and `reasoning_effort`.

```bash
python3 - <<'PY'
import json, subprocess, sys

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is missing, so no route was written")

PSTACK_ROUTES = json.loads(r"""
[the pstack routes the user chose]
""")
SWITCH_BACKEND = True

def config(*args):
    return subprocess.run(["hermes", "config", *args], capture_output=True, text=True)

if not PSTACK_ROUTES:
    sys.exit("no pstack routes to write")
with open(config("path").stdout.strip()) as f:
    raw = yaml.safe_load(f) or {}
model_map = ((raw.get("delegation") or {}).get("backends") or {}).get("model_map") or {}
routes = [r for r in model_map.get("options") or [] if not str(r.get("name", "")).startswith("pstack-")] + PSTACK_ROUTES

writes = [("delegation.backends.model_map.options", json.dumps(routes))]
if SWITCH_BACKEND:
    if "default" not in model_map:
        writes.append(("delegation.backends.model_map.default", "pstack-worker"))
    writes.append(("delegation.backend", "model_map"))

for key, value in writes:
    if config("set", key, value).returncode != 0:
        sys.exit(f"setting {key} failed, so nothing after it was written")
    print(f"set {key}")
PY
```

The script keeps every route that is not a pstack route, in order and as written, drops every route whose name starts with `pstack-`, and appends the pstack routes the user chose. It writes the routes before the backend and stops at the first failed write, so it never turns `model_map` on without routes. If it fails, report its last line and stop. If PyYAML is missing, ask the user to install it for `python3`, or to add the routes with `hermes delegation config`.

`delegation.model` and `delegation.provider` stop applying in this mode. The user can edit routes later with `hermes delegation config`.

**Without routes.** When step 1 showed `model_map` or `profile_routes`, switch the backend back first, because `delegation.model` and `delegation.provider` apply only to the default backend. The routes stay in config but stop applying:

```bash
hermes config set delegation.backend default
```

Then write the delegate model:

```bash
hermes config set delegation.reasoning_effort <effort>
hermes config set delegation.model <slug>        # skip for inherit-parent
hermes config set delegation.provider <provider> # only if it differs from the parent
```

For `inherit-parent`, clear any old pin: `hermes config unset delegation.model` and `hermes config unset delegation.provider`. Re-running this skill overwrites the same keys, so it stays idempotent.

### 7. Verify

Run the step 1 config commands again, and check that each written value reads back as chosen. With routes, check that every route the user had is still listed, and that each pstack route has a name, a description, a model, and a provider or `base_url`. Hermes skips a route without a provider and only logs it. If a value did not stick, report it and stop.

### 8. Confirm

Tell the user what was written and that it applies to new sessions. With routes, list each pstack route and its model, name the route that runs a task with no route, say that `/delegation model_map --now` applies the routes to the current chat, and say that `delegation.model` no longer applies. Without routes, say whether setup switched the backend back to `default`, and that any routes in config apply again if the user turns the plugin and `model_map` back on. Every delegate runs on one model, so panel skills (`pstack:interrogate`, `pstack:architect`) get their diversity from independent subagents and distinct prompts.

### 9. Offer a verification path (optional)

Check whether the project has a way to drive the real app for proof: a `verify-*` skill or an existing harness (e2e suite, smoke script). If it has neither, say so once and suggest writing one, so agents can prove changes the way a user would. Don't push.

### 10. Offer a formal verification skill (optional)

Check whether the project already has a formal verification skill (a project skill that runs a model checker, a proof, or another verifier against the code). If not, offer once: "want a formal verification skill, so agents can prove a key property of your code holds in every case in scope, not only the cases tests reach? I can generate one with `pstack:create-formal-verification-skill`." On yes, load that skill. On no, move on without pushing.
