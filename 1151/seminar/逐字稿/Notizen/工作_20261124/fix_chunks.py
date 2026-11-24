#!/usr/bin/env python3
"""1151 積欠週次未通過的 8 份：把壞掉的區間切成約 300 秒的片段逐段重轉，量過才接回主檔。

    fix_chunks.py <工作清單.tsv>     （工作目錄為 SCU_Constitutional_Law_Tang 倉根）

清單每行：前綴<TAB>音檔<TAB>提示詞<TAB>區間（"a-b,c-end"）<TAB>詞典<TAB>known（可空）

每段依序試：帶提示詞（carry，短輸入不自動加 -mc 0）提早 0／20／45 秒、尾端多轉 30 秒；
都不過再試不帶提示詞加 -mc 0。過的判準：近似重複最長不到 4 段、提示詞無外漏、片內最大空隙
不到 120 秒、標點每百字（整段與後半取低者）不低於 5。都不過就收最好的一份並記下。
邊界取前後 10 秒內能量最低的 0.3 秒。接回用 asr_resume_collapse.splice_files（六檔同步）。
主檔覆寫前另存 <前綴>.<副檔名>.orig（已有則不覆寫）。
"""
import array
import shutil
import subprocess
import sys
import time
from pathlib import Path

TOOLS = Path.home() / "Documents/NTU/1141/whisper/whisper-rt-full/whisper-realtime/tools"
sys.path.insert(0, str(TOOLS))
import asr_check_output as C  # noqa: E402
import asr_text as TX  # noqa: E402
import asr_resume_collapse as R  # noqa: E402

PY = str(TOOLS.parent / ".venv311/bin/python")
CHUNK = 300.0
SNAP = 10.0
EXTS = R.EXTS
# p＝帶提示詞、n＝不帶提示詞加 -mc 0；N 結尾＝--no-vad。2026-11-24 W04 憲法課 4920 秒那段帶 VAD 試五種
# 都在 30 秒後失去標點，且提早轉的那 20 秒被 VAD 時間碼映到起點之後、與前一段重複；--no-vad 一次即 10.6。
TRIES = [("p", 0, 0), ("p", 20, 0), ("pN", 0, 0), ("pN", 20, 0), ("p", 45, 0), ("p", 0, 60), ("pN", 0, 60),
         ("n", 0, 0), ("nN", 0, 0)]


def log(msg):
    print(time.strftime("%H:%M:%S"), msg, flush=True)


def snap(audio, t):
    lo = max(0.0, t - SNAP)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", "%.2f" % lo, "-t", "%.2f" % (2 * SNAP), "-i", audio,
                          "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True, check=True,
                         stdin=subprocess.DEVNULL).stdout
    s = array.array("h", raw)
    hop, win = 800, 4800
    if len(s) < win:
        return t
    best, bi = None, 0
    for i in range(0, len(s) - win, hop):
        e = sum(x * x for x in s[i:i + win:4])
        if best is None or e < best:
            best, bi = e, i
    return round(lo + (bi + win / 2) / 16000, 2)


def transcribe(audio, out, prompt, ss, dur, vad=True):
    cmd = ["bash", str(TOOLS / "asr_transcribe.sh"), "--in", audio, "--out-prefix", out,
           "--ss", "%g" % ss, "--dur", "%g" % dur]
    if not vad:
        cmd += ["--no-vad"]
    if prompt:
        cmd += ["--prompt-file", prompt]
    else:
        cmd += ["--max-context", "0"]
    for attempt in range(6):
        with open(out + ".trial.log", "w", encoding="utf-8") as fh:
            rc = subprocess.run(cmd, stdin=subprocess.DEVNULL, stdout=fh, stderr=subprocess.STDOUT).returncode
        ok = all(Path("%s.%s" % (out, e)).exists() and Path("%s.%s" % (out, e)).stat().st_size
                 for e in ("srt", "json", "txt"))
        txt = Path(out + ".trial.log").read_text(encoding="utf-8", errors="replace")
        if ok and not Path(out + ".raw.srt").exists():
            # asr_transcribe.sh 的截短、字元密度兩道驗收在轉繁之前，片段落在下課或休息的靜音時會中止；
            # 產物齊全就照它的同一步補轉繁。
            subprocess.run([PY, str(TOOLS / "asr_to_traditional.py"), "--keep-raw",
                            out + ".srt", out + ".txt", out + ".json"], check=True, stdin=subprocess.DEVNULL,
                           stdout=subprocess.DEVNULL)
        if ok:
            return True
        if "轉錄為空" in txt:
            return "empty"
        if "batch-preflight 回非零" in txt or "正在跑（PID" in txt or "仍有 whisper-cli 在跑" in txt:
            log("    preflight／鎖未過，等 120 秒再試（%d）" % (attempt + 1))
            time.sleep(120)
            continue
        return False
    return False


def score(srt, ss, pos, cut_to, prompt_args):
    blocks = [[a + ss, b + ss, t] for a, b, t in C.read(srt)]
    end = float("inf") if cut_to is None else cut_to
    take = [b for b in blocks if pos <= b[0] < end]
    if not take:
        return None
    runs = TX.near_runs(take)
    longest = max((r[0] for r in runs), default=0)
    leaks = C.prompt_leaks(take, prompt_args[0]) + C.list_leaks(take, prompt_args[1], prompt_args[2])
    whole = C.punct_per_100(take, C.WINDOW_MIN_CJK)
    mid = (take[0][0] + take[-1][1]) / 2
    tail = C.punct_per_100([b for b in take if b[0] >= mid], C.WINDOW_MIN_CJK // 2)
    vals = [v for v in (whole, tail) if v is not None]
    punct = min(vals) if vals else None
    gaps = [take[0][0] - pos] + [take[i + 1][0] - take[i][1] for i in range(len(take) - 1)]
    gap = max(gaps)
    ok = longest < 4 and not leaks and (punct is None or punct >= 5.0)
    return dict(n=len(take), longest=longest, leaks=len(leaks), punct=punct, gap=gap, ok=ok)


def rank(s):
    # 小的好：迴圈、外漏、空隙優先，再看標點
    return (s["longest"] >= 4, s["leaks"] > 0, -(s["punct"] if s["punct"] is not None else 99), s["gap"])


def regions_of(spec, total):
    out = []
    for part in spec.split(","):
        a, b = part.split("-")
        out.append((float(a), None if b == "end" else float(b)))
    return out


def fix_one(prefix, audio, prompt, spec, terms, known):
    total = C.audio_duration(audio)
    stem = Path(prefix).name
    work_dir = Path(prefix).parent / ".cache" / ("fix-" + stem)
    work_dir.mkdir(parents=True, exist_ok=True)
    ptext = Path(prompt).read_text(encoding="utf-8").strip()
    pargs = (C.prompt_grams(ptext), C.prompt_items(ptext), ptext)
    log("######## %s（%.0f 秒）區間 %s" % (prefix, total, spec))

    for ext in EXTS:
        src = Path("%s.%s" % (prefix, ext))
        dst = Path("%s.%s.orig" % (prefix, ext))
        if src.exists() and not dst.exists():
            shutil.copy2(src, dst)
    if not Path(prefix + ".raw.srt").exists():
        log("  主檔無 raw（轉錄因截短檢查中止於轉繁之前），補做轉繁 --keep-raw")
        subprocess.run([PY, str(TOOLS / "asr_to_traditional.py"), "--keep-raw",
                        prefix + ".srt", prefix + ".txt", prefix + ".json"], check=True, stdin=subprocess.DEVNULL)

    cur = prefix
    work = str(work_dir / "work")
    for f in work_dir.glob("work.*"):
        f.unlink()
    seams, notes = [], []
    k = 0
    for A, B in regions_of(spec, total):
        B_real = total if B is None else B
        a0 = 0.0 if A <= 1 else snap(audio, A)
        bounds = [a0]
        t = a0 + CHUNK
        while t < B_real - 60:
            bounds.append(snap(audio, t))
            t = bounds[-1] + CHUNK
        bounds.append(None if B is None else snap(audio, B))
        seams += [b for b in bounds if b is not None and b > 0]
        for i in range(len(bounds) - 1):
            pos, cut_to = bounds[i], bounds[i + 1]
            k += 1
            length = (total if cut_to is None else cut_to) - pos
            best = None
            for mode, lead, extra in TRIES:
                if lead > pos:
                    continue
                ss = pos - lead
                dur = min(length + lead + extra, total - ss)
                trial = str(work_dir / ("c%02d_%s_%g_%g" % (k, mode, ss, dur)))
                r = transcribe(audio, trial, prompt if mode.startswith("p") else None, ss, dur, vad=not mode.endswith("N"))
                if r == "empty":
                    sp = C.tail_speech_seconds(audio, pos)
                    log("  段 %d %.0f–%s：轉錄為空（VAD 語音 %s 秒）" % (k, pos, "檔尾" if cut_to is None else "%.0f" % cut_to, sp))
                    continue
                if not r:
                    log("  段 %d：%s ss=%g dur=%g 轉錄失敗，見 %s.trial.log" % (k, mode, ss, dur, trial))
                    continue
                s = score(trial + ".srt", ss, pos, cut_to, pargs)
                if s is None:
                    log("  段 %d：%s ss=%g dur=%g 區間內一段都沒有" % (k, mode, ss, dur))
                    continue
                log("  段 %d %.0f–%s：%s 提早 %g 尾 +%g → %d 段，迴圈 %d，外漏 %d，空隙 %.0f，標點 %s%s" % (
                    k, pos, "檔尾" if cut_to is None else "%.0f" % cut_to, mode, lead, extra, s["n"], s["longest"],
                    s["leaks"], s["gap"], "—" if s["punct"] is None else "%.2f" % s["punct"], "  ✓" if s["ok"] else ""))
                if best is None or rank(s) < rank(best[1]):
                    best = (trial, s, ss, mode)
                if s["ok"]:
                    break
            if best is None:
                sp = speech_seconds(audio, pos, cut_to)
                if sp is not None and sp < 5:
                    log("  段 %d：此段無語音（VAD %.1f 秒），原稿此段刪去" % (k, sp))
                    notes.append("段 %d 自 %.0f 秒到 %s 無語音（VAD %.1f 秒），原稿該段刪去" % (
                        k, pos, "檔尾" if cut_to is None else "%.0f" % cut_to, sp))
                    drop_range(cur, pos, cut_to, work)
                    cur = work
                    continue
                log("  段 %d：全數失敗，停" % k)
                return False, seams, notes
            trial, s, ss, mode = best
            if not s["ok"]:
                notes.append("段 %d（%.0f 秒起）%d 種試法都未全過，收 %s（迴圈 %d、標點 %s）" % (
                    k, pos, len(TRIES), Path(trial).name, s["longest"], s["punct"]))
            if mode.startswith("n"):
                notes.append("段 %d（%.0f 秒起）用不帶提示詞、-mc 0 的那一份" % (k, pos))
            R.splice_files(cur, trial, ss, pos, cut_to, work)
            cur = work
            with open(prefix + ".run.log", "a", encoding="utf-8") as fh:
                fh.write("# 接續　分段重轉 段 %d 自 %g 到 %s 取 %s（ss=%g）\n" % (
                    k, pos, "檔尾" if cut_to is None else "%g" % cut_to, Path(trial).name, ss))

    for ext in EXTS:
        src = Path("%s.%s" % (work, ext))
        if src.exists():
            shutil.copy2(src, "%s.%s" % (prefix, ext))
    return True, seams, notes


def speech_seconds(audio, a, b):
    if b is None:
        return C.tail_speech_seconds(audio, a)
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        clip = str(Path(tmp) / "clip.wav")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(a), "-t", str(b - a), "-i", audio,
                        "-ac", "1", "-ar", "16000", clip], check=True, stdin=subprocess.DEVNULL)
        return C.tail_speech_seconds(clip, 0)


def drop_range(cur, pos, cut_to, out):
    """cur 前綴六檔去掉起點落在 [pos, cut_to) 的段，寫到 out。"""
    end = float("inf") if cut_to is None else cut_to
    b = R.srt_blocks(cur + ".srt")
    keep = [i for i, x in enumerate(b) if not (pos <= x[0] < end)]
    for ext in EXTS:
        p = Path("%s.%s" % (cur, ext))
        if not p.exists():
            continue
        if ext.endswith("srt"):
            bb = R.srt_blocks(p)
            R.write_text("%s.%s" % (out, ext), R.srt_dump([bb[i] for i in keep]))
        elif ext.endswith("txt"):
            ll = R.txt_lines(p)
            R.write_text("%s.%s" % (out, ext), "\n".join(ll[i] for i in keep) + "\n")
        else:
            j = R.json_load(p)
            j["transcription"] = [j["transcription"][i] for i in keep]
            R.write_text("%s.%s" % (out, ext), R.json_dump(j))


def seam_report(prefix, seams):
    b = C.read(prefix + ".srt")
    dup = []
    for s in seams:
        idx = next((i for i, x in enumerate(b) if x[0] >= s - 0.001), len(b))
        print("  —— 邊界 %.2f 秒" % s)
        for x in b[max(0, idx - 3): idx + 3]:
            print("     %8.2f  %s" % (x[0], x[2][:70]))
        for j in (idx, idx + 1):
            if 0 < j < len(b):
                size, text = TX.longest_overlap(b[j - 1][2], b[j][2])
                if size >= 6:
                    dup.append(s)
                    print("     ！%.2f 與 %.2f 兩段有 %d 個字重複：%s" % (b[j - 1][0], b[j][0], size, text[:40]))
    return dup


def main():
    jobs = [l.rstrip("\n").split("\t") for l in open(sys.argv[1], encoding="utf-8") if l.strip() and not l.startswith("#")]
    summary = []
    for prefix, audio, prompt, spec, terms, known in jobs:
        try:
            ok, seams, notes = fix_one(prefix, audio, prompt, spec, terms, known)
        except Exception as exc:  # noqa: BLE001
            import traceback
            traceback.print_exc()
            summary.append((prefix, "例外：%s" % exc))
            continue
        for n in notes:
            log("  注意：" + n)
        if not ok:
            summary.append((prefix, "接回未完成"))
            continue
        log("  邊界前後三段：")
        seam_report(prefix, seams)
        rc = subprocess.run(["/usr/bin/python3", str(TOOLS / "asr_check_output.py"), "--layer", "raw",
                             "--audio", audio, "--prompt", prompt, prefix + ".srt"], stdin=subprocess.DEVNULL).returncode
        if rc != 0:
            summary.append((prefix, "辨識層檢查未過"))
            continue
        cmd = [str(TOOLS / "asr_week.sh"), "--out-dir", str(Path(prefix).parent), "--terms", terms, "--prompt", prompt]
        if known:
            cmd += ["--known", known]
        cmd += ["--files", audio]
        rc = subprocess.run(cmd, stdin=subprocess.DEVNULL).returncode
        summary.append((prefix, "通過" if rc == 0 else "asr_week 未過（rc=%d）" % rc))
    log("======== 總結")
    for p, s in summary:
        log("  %s：%s" % (p, s))


if __name__ == "__main__":
    main()
