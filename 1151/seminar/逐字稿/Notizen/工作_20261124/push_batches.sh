#!/bin/bash
# 逐提交推，遇到失敗重試兩次；每推一個印一行
cd ~/Documents/NTU/SCU_Constitutional_Law_Tang
for c in $(git rev-list --reverse origin/main..main); do
  for t in 1 2 3; do
    if git -c http.postBuffer=1048576000 push origin "$c:refs/heads/main" >/dev/null 2>&1; then echo "ok $c"; break; fi
    echo "retry $t $c"; sleep 5
    [ $t = 3 ] && { echo "FAIL $c"; exit 1; }
  done
done
echo done
