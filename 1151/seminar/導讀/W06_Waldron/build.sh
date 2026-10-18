#!/bin/bash
# 問答集建置：xelatex → biber → xelatex 兩次。紀錄寫到 build.log。
set -e
cd "$(dirname "$0")"
MAIN=W06_Waldron_導讀問答
: > build.log
run() { "$@" </dev/null >>build.log 2>&1 || { echo "失敗：$*（見 build.log）"; exit 1; }; }
run xelatex -interaction=nonstopmode "$MAIN"
run biber "$MAIN"
run xelatex -interaction=nonstopmode "$MAIN"
run xelatex -interaction=nonstopmode "$MAIN"
grep -q "Rerun to get" "$MAIN.log" && echo "注意：log 仍要求重編"
echo "頁數 $(pdfinfo "$MAIN.pdf" | awk '/^Pages:/{print $2}')；未定義引用 $(grep -c 'undefined' "$MAIN.log")；Overfull $(grep -c 'Overfull' "$MAIN.log")"
