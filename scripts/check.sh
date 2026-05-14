#!/usr/bin/env sh
set -eu

repo_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$repo_root"

. ./scripts/runtime_paths.sh

case "$CONSTITUTION_RUNTIME_DIR" in
  .local/*) ;;
  *)
    printf 'runtime dir must default under .local/: %s\n' "$CONSTITUTION_RUNTIME_DIR" >&2
    exit 1
    ;;
esac

for path in "$CONSTITUTION_EVIDENCE_DIR" "$CONSTITUTION_CACHE_DIR" "$CONSTITUTION_LOG_DIR"; do
  case "$path" in
    "$CONSTITUTION_RUNTIME_DIR"/*) ;;
    *)
      printf 'runtime output path is outside runtime dir: %s\n' "$path" >&2
      exit 1
      ;;
  esac

  if git check-ignore -q "$path/.keep"; then
    :
  else
    printf 'runtime output path is not ignored by git: %s\n' "$path" >&2
    exit 1
  fi
done

tracked_runtime=$(
  git ls-files \
    '.local/**' \
    'tmp/**' \
    '*.log' \
    '*.cache'
)

if [ -n "$tracked_runtime" ]; then
  printf 'runtime output files are tracked:\n%s\n' "$tracked_runtime" >&2
  exit 1
fi

printf 'constitution checks passed\n'
