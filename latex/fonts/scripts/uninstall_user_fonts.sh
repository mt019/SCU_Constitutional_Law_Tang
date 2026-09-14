#!/usr/bin/env bash
set -euo pipefail

DEST_DIR="$HOME/Library/Fonts"

mapfile -t fonts < <(find "$DEST_DIR" -maxdepth 1 -type f -name 'SCUQuoteCards-*' | sort)

if [[ "${#fonts[@]}" -eq 0 ]]; then
  echo "No SCUQuoteCards fonts found in $DEST_DIR"
  exit 0
fi

for font in "${fonts[@]}"; do
  rm -f "$font"
  printf 'removed %s\n' "$font"
done

if command -v fc-cache >/dev/null 2>&1; then
  fc-cache -f "$DEST_DIR" >/dev/null 2>&1 || true
fi

printf '\nRemoved %d SCUQuoteCards fonts from %s\n' "${#fonts[@]}" "$DEST_DIR"
