#!/bin/bash
# 1151 研討會與憲法課積欠的週次，一次一份依序轉錄（2026-11-24 站主「照辦」）。
# 研討會＝週一第 3–4 節（上午），憲法課＝週一第 7–8 節（下午），依兩份 syllabus.md。
# 錄音一律取語音備忘錄；研討會 W08（11-02）、W09（11-09）上午只有 DJI TX02，麥克風未接上，不在本批。
#
# 轉錄直接呼叫 asr_transcribe.sh 並顯式傳 --max-context 224：asr_week.sh 不轉傳此參數，
# 超過一小時的輸入會被自動加 -mc 0，提示詞因而無效（稅法 1105-1-2 於 2026-11-24 因此未通過）。
# 轉完再以 asr_week.sh --files 跑校正、輸出檢查、待核清單（已有 .srt 者不重轉）。
# 已有 .srt 的週次跳過轉錄，可重跑。
#
# 執行：runlog asr-scu-backlog bash 1151/seminar/asr/run_backlog_20261124.sh（工作目錄為倉根）

set -u
cd "$(dirname "$0")/../../.." || exit 1
T=~/Documents/NTU/1141/whisper/whisper-rt-full/whisper-realtime/tools
VM="$HOME/Library/Group Containers/group.com.apple.VoiceMemos.shared/Recordings"
TERMS=1151/seminar/asr/terms.json
KNOWN=1151/seminar/readings/index.md

# 前一支轉錄（別的倉的批次）還在跑就等；這台機器一次只跑一支 whisper。
wait_idle() {
  while pgrep -f 'whisper-cli' >/dev/null || pgrep -f 'asr_week.sh' >/dev/null; do
    sleep 120
  done
}

FAILED=""
# 欄位：輸出目錄｜提示詞｜音檔（檔名，位於語音備忘錄目錄）
while IFS='|' read -r OUT PROMPT FILE; do
  [ -z "$OUT" ] && continue
  AUDIO="$VM/$FILE"
  STEM="$(basename "$FILE" .m4a | tr ' ' '_')"
  echo
  echo "######## $OUT  $STEM"
  [ -f "$AUDIO" ] || { echo "找不到音檔：$AUDIO"; FAILED="$FAILED $OUT/$STEM(無音檔)"; continue; }
  mkdir -p "$OUT"
  if [ ! -s "$OUT/$STEM.srt" ]; then
    wait_idle
    "$T/asr_transcribe.sh" --in "$AUDIO" --out-prefix "$OUT/$STEM" \
      --prompt-file "$PROMPT" --max-context 224 < /dev/null \
      || { FAILED="$FAILED $OUT/$STEM(轉錄)"; continue; }
  fi
  KARGS=()
  case "$OUT" in 1151/seminar/*) KARGS=(--known "$KNOWN") ;; esac
  "$T/asr_week.sh" --out-dir "$OUT" --terms "$TERMS" --prompt "$PROMPT" ${KARGS[@]+"${KARGS[@]}"} \
    --files "$AUDIO" < /dev/null || FAILED="$FAILED $OUT/$STEM(校正或檢查)"
done <<'EOF'
1151/seminar/asr/W11_1123|1151/seminar/asr/prompt-W11.txt|20261123 104009.m4a
1151/constitution/asr/W11_1123|1151/constitution/asr/prompt-W11.txt|20261123 152005.m4a
1151/seminar/asr/W10_1116|1151/seminar/asr/prompt-W10.txt|20261116 103434.m4a
1151/constitution/asr/W09_1109|1151/constitution/asr/prompt-W09.txt|20261109 151227.m4a
1151/constitution/asr/W08_1102|1151/constitution/asr/prompt-W08.txt|20261102 151419.m4a
1151/constitution/asr/W06_1019|1151/constitution/asr/prompt-W06.txt|20261019 151358.m4a
1151/seminar/asr/W05_1012|1151/seminar/asr/prompt-W05.txt|20261012 101334.m4a
1151/constitution/asr/W05_1012|1151/constitution/asr/prompt-W05.txt|20261012 151333-A71D100C.m4a
1151/constitution/asr/W05_1012|1151/constitution/asr/prompt-W05.txt|20261012 160249-70FAD146.m4a
1151/seminar/asr/W04_1005|1151/seminar/asr/prompt-W04.txt|20261005 101248-6A8B0EBB.m4a
1151/constitution/asr/W04_1005|1151/constitution/asr/prompt-W04.txt|20261005 151152.m4a
1151/constitution/asr/W02_0921|1151/constitution/asr/prompt-W02.txt|20260921 151053.m4a
EOF

echo
if [ -n "$FAILED" ]; then
  echo "未通過：$FAILED"
  exit 1
fi
echo "全部通過。"
