#!/bin/bash
# 課程問答集的完整建置：xelatex → biber → xelatex → 四份索引各跑 upmendex → xelatex 兩次。
# 索引以 noautomatic 宣告（見主檔 \CourseNotesLawIndexes），由本腳本依 zh-law.ist 逐份排序。
# 某份索引沒有任何詞條時 idx 為空，略過該份。紀錄寫到 build.log。
set -e
cd "$(dirname "$0")"
MAIN=1151_憲法專題研究_逐字稿
STY="$(sed -n 's/^\\def\\TransLaTeXDir{\(.*\)}.*/\1/p' "$MAIN.tex")"
# biber 預設快取目錄不可用，改指到書目錄下
mkdir -p .biber-tmp
export PAR_GLOBAL_TEMP="$PWD/.biber-tmp"
: > build.log
run() { "$@" </dev/null >>build.log 2>&1 || { echo "失敗：$*（見 build.log）"; exit 1; }; }
indexes() {
  for n in terms statutes cases persons; do
    if [ -s "$n.idx" ]; then
      run upmendex -s "$STY/zh-law.ist" -o "$n.ind" "$n.idx"
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
echo "頁數 $(pdfinfo "$MAIN.pdf" | awk '/^Pages:/{print $2}')；xelatex 錯誤 $(grep -c '^!' "$MAIN.log")；未定義引用 $(grep -c 'undefined' "$MAIN.log")；Overfull $(grep -c 'Overfull' "$MAIN.log")"
