import sys
sys.path.insert(0, "/Users/iw/Documents/NTU/1141/whisper/whisper-rt-full/whisper-realtime/tools")
import asr_check_output as C, asr_text as T
for p in sys.argv[1:]:
    b = C.read(p)
    print("==", p, len(b), "segs, last", b[-1][1])
    idx = {x[0]: i for i, x in enumerate(b)}
    for n, st, txt in T.near_runs(b):
        i = idx[st]; end = b[i+n-1][1]
        print("  run %4d  %7.1f-%7.1f  %s" % (n, st, end, txt[:30]))
    print("  punct:", " ".join("—" if d is None else "%.1f" % d for a, d in C.punct_windows(b)))
