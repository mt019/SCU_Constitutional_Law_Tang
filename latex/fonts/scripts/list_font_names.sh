#!/usr/bin/env bash
set -euo pipefail

DEST_DIR="$HOME/Library/Fonts"
INSTALL_PREFIX="${FONT_INSTALL_PREFIX:-SCUQuoteCards}"

if command -v fc-scan >/dev/null 2>&1; then
  find "$DEST_DIR" -maxdepth 1 -type f -name "$INSTALL_PREFIX-*" -print0 |
    sort -z |
    while IFS= read -r -d '' file; do
      printf '\n%s\n' "$(basename "$file")"
      fc-scan --format '  %{family} | %{style}\n' "$file" 2>/dev/null | sort -u || true
    done
else
  find "$DEST_DIR" -maxdepth 1 -type f -name "$INSTALL_PREFIX-*" -print | sort
fi
