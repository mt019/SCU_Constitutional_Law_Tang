#!/bin/bash
# W10 預習問答集的完整建置：出處一覽 → xelatex → biber → xelatex → 四份索引各跑 upmendex → xelatex 兩次
# → 書目檢查 → 文件資訊檢查。寫法照 ../../課程問答/build.sh 與統計課 tex/build.sh。紀錄寫到 build.log。
set -e
cd "$(dirname "$0")"
MAIN=W10_Law_預習
STY="$(sed -n 's/^\\def\\TransLaTeXDir{\(.*\)}.*/\1/p' "$MAIN.tex")"
mkdir -p "$HOME/Library/Caches/biber-par"
export PAR_GLOBAL_TEMP="$HOME/Library/Caches/biber-par"  # 全機共用，不在書目錄下（2026-11-24 七本書各解壓 3868 檔）
: > build.log
run() { "$@" </dev/null >>build.log 2>&1 || { echo "失敗：$*（見 build.log）"; exit 1; }; }
indexes() {
  for n in terms statutes cases persons; do
    if [ -s "$n.idx" ]; then
      IST="$STY/zh-law.ist"; [ "$n" = cases ] && [ -f zh-law-cases.ist ] && IST=zh-law-cases.ist
      run upmendex -s "$IST" -o "$n.ind" "$n.idx"
    else
      : > "$n.ind"
    fi
  done
}
run xelatex -interaction=nonstopmode "$MAIN"
run biber "$MAIN"
run xelatex -interaction=nonstopmode "$MAIN"
indexes
run xelatex -interaction=nonstopmode "$MAIN"
indexes
run xelatex -interaction=nonstopmode "$MAIN"
grep -q "Rerun to get" "$MAIN.log" && echo "注意：log 仍要求重編"
/usr/bin/python3 -I "$STY/tools/bibcheck.py" "$MAIN.tex" > bibcheck.log 2>&1 || true
BIB="$(tail -1 bibcheck.log)"
META="$(/usr/bin/python3 -I ~/.claude/bin/check-pdf-metadata.py "$MAIN.pdf" 2>&1 | tail -1)"
echo "頁數 $(pdfinfo "$MAIN.pdf" | awk '/^Pages:/{print $2}')；xelatex 錯誤 $(grep -c '^!' "$MAIN.log" || true)；未定義引用 $(grep -c 'undefined' "$MAIN.log" || true)；書目缺出處 $(grep -c 'No source for' "$MAIN.log" || true)；Overfull $(grep -c 'Overfull' "$MAIN.log" || true)；${BIB}；文件資訊 ${META}"
