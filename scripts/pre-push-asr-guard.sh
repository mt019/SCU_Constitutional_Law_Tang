#!/bin/sh
# 東吳兩門課的逐字稿不推上公開遠端（2026-11-24 站主裁定）。
# 擋下：要推的提交裡，凡改動 1151/*/asr/W*/ 底下任何檔者。
# 詞典（terms.json、terms-fixtures.tsv）與提示詞（prompt*.txt）不在此限。
# 安裝：ln -sf ../../scripts/pre-push-asr-guard.sh .git/hooks/pre-push
# 推之前要先把那些提交從歷史中移除（git filter-repo --path-glob '1151/*/asr/W*' --invert-paths），
# 或確定要公開時以 git push --no-verify 越過。

zero=0000000000000000000000000000000000000000
status=0
while read -r local_ref local_sha remote_ref remote_sha; do
  [ "$local_sha" = "$zero" ] && continue
  if [ "$remote_sha" = "$zero" ]; then
    range="$local_sha"
  else
    range="$remote_sha..$local_sha"
  fi
  hits=$(git log --format='%h %s' "$range" -- '1151/*/asr/W*' 2>/dev/null)
  if [ -n "$hits" ]; then
    echo "pre-push：以下提交改動了 1151/*/asr/W*/ 的逐字稿，此倉為公開倉，逐字稿不推（2026-11-24 站主裁定）：" >&2
    echo "$hits" | head -20 >&2
    n=$(echo "$hits" | wc -l | tr -d ' ')
    echo "共 $n 個提交。處理方式見 scripts/pre-push-asr-guard.sh 檔頭。" >&2
    status=1
  fi
done
exit $status
