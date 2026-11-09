#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

for command_name in copilot inotifywait sha256sum awk cmp; do
  if ! command -v "$command_name" >/dev/null 2>&1; then
    printf 'README watcher requires "%s" on PATH.\n' "$command_name" >&2
    exit 1
  fi
done

sync_readme() (
  set -euo pipefail

  local temp_dir initial_hash prompt temp_readme current_hash
  initial_hash="$(sha256sum "$repo_root/README.md" | awk '{print $1}')"
  temp_dir="$(mktemp -d)"
  trap 'rm -rf -- "$temp_dir"' EXIT

  mkdir -p "$temp_dir/.github/agents"
  cp -p "$repo_root/README.md" "$temp_dir/README.md"
  cp -p "$repo_root/main.py" "$temp_dir/main.py"
  for context_file in requirements.txt comandos.txt; do
    if [[ -f "$repo_root/$context_file" ]]; then
      cp -p "$repo_root/$context_file" "$temp_dir/$context_file"
    fi
  done
  cp -p "$repo_root/.github/agents/readme-sync.agent.md" "$temp_dir/.github/agents/readme-sync.agent.md"

  prompt="Update README.md to accurately describe the current implementation in main.py. Use the other files in this working directory only as supporting evidence. Preserve the README's language. Edit README.md only, do not execute code, and do not invent behavior."
  if ! (cd "$temp_dir" && copilot --agent "README Maintainer" --prompt "$prompt" --trust-folder --allow-all-tools --silent); then
    printf 'README sync failed; the project README was left unchanged.\n' >&2
    return 1
  fi

  if cmp -s "$temp_dir/README.md" "$repo_root/README.md"; then
    printf 'README is already in sync with main.py.\n'
    return 0
  fi

  current_hash="$(sha256sum "$repo_root/README.md" | awk '{print $1}')"
  if [[ "$current_hash" != "$initial_hash" ]]; then
    printf 'README changed while sync was running; not overwriting the newer edit.\n' >&2
    return 1
  fi

  temp_readme="$(mktemp "$repo_root/.README.md.XXXXXX")"
  cp --preserve=mode "$temp_dir/README.md" "$temp_readme"
  mv -f -- "$temp_readme" "$repo_root/README.md"
  printf 'README updated from the current main.py.\n'
)

printf 'Watching main.py in %s\n' "$repo_root"
while IFS= read -r changed_file; do
  [[ "$changed_file" == "main.py" ]] || continue

  # Wait for a short quiet period so rapid saves produce one documentation run.
  while IFS= read -r -t 1.5 next_file; do
    :
  done

  sync_readme || true
done < <(inotifywait --monitor --quiet --event close_write,moved_to --format '%f' "$repo_root")
