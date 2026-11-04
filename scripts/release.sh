#!/usr/bin/env bash
# Tag and release the plugin.yaml version at HEAD, then open or update the Hermes catalog PR.
#
# A version counts as released once its GitHub release exists, so a run that failed after
# tagging resumes where it stopped. A failed catalog step is retried with FORCE=true.
#
# Env: FORCE=true         skip the quiet-period wait; on a released version, rerun the catalog step only
#      DEBOUNCE_HOURS=3   quiet period HEAD must have survived before releasing
#      CATALOG_TOKEN      classic PAT (public_repo) from Cloeille; without it the catalog step is skipped
#      DRY_RUN=1          print every mutating command instead of running it
set -euo pipefail

UPSTREAM=NousResearch/hermes-agent
FORK=Cloeille/hermes-agent
FILE=plugin-catalog/pstack.yaml
SELF=https://github.com/Cloeille/pstack
TITLE_PREFIX='chore(plugin-catalog): bump pstack'

run() {
  if [ "${DRY_RUN:-}" = 1 ]; then
    printf '[dry-run]'
    printf ' %q' "$@"
    echo
  else
    "$@"
  fi
}

field() { sed -nE "s/^$2: \"?([^\"]*)\"?\$/\\1/p" "$1"; }

VERSION=$(git show HEAD:plugin.yaml |
  sed -nE "s/^version:[[:space:]]*[\"']?([0-9]+\.[0-9]+\.[0-9]+)[\"']?[[:space:]]*\$/\1/p")
[ -n "$VERSION" ] || { echo "plugin.yaml: no MAJOR.MINOR.PATCH version found" >&2; exit 1; }
git fetch --tags --quiet origin

released() { gh release view "$VERSION" >/dev/null 2>&1; }

if [ "${FORCE:-}" != true ] && released; then
  echo "already released: $VERSION"
  exit 0
fi

if git rev-parse -q --verify "refs/tags/$VERSION" >/dev/null; then
  SHA=$(git rev-parse "$VERSION^{commit}")
else
  SHA=$(git rev-parse HEAD)
  age=$(( $(date +%s) - $(git log -1 --format=%ct HEAD) ))
  limit=$(( ${DEBOUNCE_HOURS:-3} * 3600 ))
  if [ "${FORCE:-}" != true ] && [ "$age" -lt "$limit" ]; then
    echo "waiting: HEAD is $((age / 60)) min old, releasing $VERSION after $((limit / 60)) min of quiet"
    exit 0
  fi
  python3 scripts/check_refs.py
  run git tag -a "$VERSION" -m "$VERSION" "$SHA"
  run git push origin "refs/tags/$VERSION"
fi

released || run gh release create "$VERSION" --verify-tag --title "$VERSION" --generate-notes --latest

if [ -z "${CATALOG_TOKEN:-}" ]; then
  echo "::warning::CATALOG_TOKEN is not set, skipping the Hermes catalog PR for $VERSION"
  exit 0
fi
export GH_TOKEN=$CATALOG_TOKEN

tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

raw=(-H 'Accept: application/vnd.github.raw+json')
gh api "${raw[@]}" "repos/$UPSTREAM/contents/$FILE?ref=main" >"$tmp/main.yaml"
old_sha=$(field "$tmp/main.yaml" sha)
old_version=$(field "$tmp/main.yaml" version)
if [ "$old_sha" = "$SHA" ]; then
  echo "catalog already pins $SHA"
  exit 0
fi

pr_number='' branch="chore/plugin-catalog-pstack-$VERSION"
found=$(gh pr list -R "$UPSTREAM" --author Cloeille --state open \
  --json number,headRefName,title \
  --jq "[.[] | select(.title | startswith(\"$TITLE_PREFIX\"))][0] // empty | \"\\(.number) \\(.headRefName)\"")
[ -z "$found" ] || read -r pr_number branch <<<"$found"

# Edit the file where the PUT lands: a reused branch keeps its earlier edits, a new one starts from main.
src="repos/$UPSTREAM/contents/$FILE?ref=main"
if gh api "repos/$FORK/git/ref/heads/$branch" >/dev/null 2>&1; then
  src="repos/$FORK/contents/$FILE?ref=$branch"
else
  main_sha=$(gh api "repos/$UPSTREAM/git/ref/heads/main" --jq .object.sha)
  run gh api "repos/$FORK/git/refs" -f "ref=refs/heads/$branch" -f "sha=$main_sha"
fi
blob=$(gh api "$src" --jq .sha)
gh api "${raw[@]}" "$src" >"$tmp/base.yaml"
sed -E "s/^sha: .*/sha: $SHA/; s/^version: .*/version: \"$VERSION\"/" "$tmp/base.yaml" >"$tmp/new.yaml"
[ "$(field "$tmp/new.yaml" sha)" = "$SHA" ] && [ "$(field "$tmp/new.yaml" version)" = "$VERSION" ] ||
  { echo "$FILE: missing sha or version line" >&2; exit 1; }
diff -u "$tmp/main.yaml" "$tmp/new.yaml" || true

title="$TITLE_PREFIX entry sha to $VERSION"
cmp -s "$tmp/base.yaml" "$tmp/new.yaml" ||
  run gh api -X PUT "repos/$FORK/contents/$FILE" -f "message=$title" -f "branch=$branch" \
    -f "sha=$blob" -f "content=$(base64 -w0 "$tmp/new.yaml")"

cat >"$tmp/body.md" <<EOF
## What does this PR do?

Re-pins \`$FILE\` from $old_version (\`${old_sha:0:8}\`) to **$VERSION** (\`${SHA:0:8}\`). No Hermes code changes.

Owner update under rule 5: I own [Cloeille/pstack]($SELF) and submitted the original entry (#114322).

## Release being pinned

- Tag: [\`$VERSION\`]($SELF/releases/tag/$VERSION)
- Pinned commit: \`$SHA\`
- Range under review: [\`${old_sha:0:8}...${SHA:0:8}\`]($SELF/compare/$old_sha...$SHA)

The [release notes]($SELF/releases/tag/$VERSION) list the changes since the previous release.

## Entry changes

- Automated bump: only \`sha\` and \`version\` are rewritten.
- \`capabilities\` unchanged. The plugin still registers skills only: no tools, hooks, middleware or env vars.

## Disclosure (rule 13)

- Markdown skills plus a stdlib-only loader that reads each \`SKILL.md\` it registers.
- No network calls, no background processes, no credentials, no telemetry.
- \`skills/show-me-your-work/scripts/log.sh\` is a helper script the agent may run on request to append rows to a local TSV decision log. It is not run at load time.

## Type of Change

- [x] 🐛 Bug fix (non-breaking change that fixes an issue)
EOF
[ "${DRY_RUN:-}" != 1 ] || { echo '--- PR body ---'; cat "$tmp/body.md"; echo '--- end PR body ---'; }

if [ -n "$pr_number" ]; then
  echo "reusing $UPSTREAM#$pr_number (branch $branch)"
  run gh pr edit "$pr_number" -R "$UPSTREAM" --title "$title" --body-file "$tmp/body.md"
else
  run gh pr create -R "$UPSTREAM" --base main --head "Cloeille:$branch" --title "$title" --body-file "$tmp/body.md"
fi
