#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "usage: $0 <skill-name>" >&2
  exit 2
fi

skill_name="$1"
repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source_dir="$repo_root/skills/$skill_name"
target_dir="$HOME/.agents/skills/$skill_name"

if [ ! -f "$source_dir/SKILL.md" ]; then
  echo "missing skill: $source_dir/SKILL.md" >&2
  exit 1
fi

mkdir -p "$(dirname "$target_dir")"
rm -rf "$target_dir"
cp -R "$source_dir" "$target_dir"
diff -qr "$source_dir" "$target_dir"
echo "synced $skill_name to $target_dir"
