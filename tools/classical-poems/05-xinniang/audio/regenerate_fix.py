"""Regenerate problematic audio files with adjusted texts."""
import sys, os, glob

OUTDIR = r"G:\我的雲端硬碟\slides\新嫁娘-05-demo\audio"
VOICES_DIR = r"C:\2026_Antigravity_語音\voices"

def find_voice(name):
    pattern = os.path.join(VOICES_DIR, f"*{name}*", "ref_voice.wav")
    matches = glob.glob(pattern)
    if not matches:
        raise FileNotFoundError(f"No voice file found for: {name}")
    return matches[0]

SADALTAGER = find_voice("Sadaltager")
SULAFAT = find_voice("Sulafat")

CONTROL = "Speak slowly and clearly for children, gentle voice, Taiwan Mandarin"

# Strategy for problematic chars 諳/嚐:
# - For poem lines: remove period, the trailing 。might cause model to stop before last char
# - For words: expand text so tricky char is not at the very beginning
# - For full poem: add conversational prefix to set Taiwan Mandarin context

segments = [
    # Line 3 — try without period to see if 。triggers truncation
    ("line3-poem-sadaltager", SADALTAGER,
     "未諳姑食性",
     "line3-poem-sadaltager.wav"),
    ("line3-poem-sulafat", SULAFAT,
     "未諳姑食性",
     "line3-poem-sulafat.wav"),

    # Line 4 — try without period
    ("line4-poem-sadaltager", SADALTAGER,
     "先遣小姑嚐",
     "line4-poem-sadaltager.wav"),
    ("line4-poem-sulafat", SULAFAT,
     "先遣小姑嚐",
     "line4-poem-sulafat.wav"),

    # Full poem — conversational prefix for pronounciation context
    ("poem-full-sadaltager", SADALTAGER,
     "新嫁娘這首詩：三日入廚下，洗手作羹湯，未諳姑食性，先遣小姑嚐。",
     "poem-sadaltager.wav"),
    ("poem-full-sulafat", SULAFAT,
     "新嫁娘這首詩：三日入廚下，洗手作羹湯，未諳姑食性，先遣小姑嚐。",
     "poem-sulafat.wav"),

    # Word 諳 — expand so 諳 is not at start: use "這個字是諳..."
    ("word-an", SULAFAT,
     "諳，這個字讀作安，意思是熟悉、了解。",
     "word-an.wav"),

    # Word 嚐 — same approach
    ("word-chang", SULAFAT,
     "嚐，這個字讀作常，意思是吃吃看味道。",
     "word-chang.wav"),
]

os.makedirs(OUTDIR, exist_ok=True)

from voxcpm.cli import main

print(f"Regenerating {len(segments)} problematic files...\n")
for i, (sid, voice_ref, text, fname) in enumerate(segments):
    out_path = os.path.join(OUTDIR, fname)
    label = fname.replace(".wav", "")
    print(f"[{i+1}/{len(segments)}] {label}")
    print(f"    Text: {text}")

    sys.argv = [
        "voxcpm", "clone",
        "--text", text,
        "--reference-audio", voice_ref,
        "--output", out_path,
        "--control", CONTROL,
    ]
    try:
        main()
        size = os.path.getsize(out_path) if os.path.exists(out_path) else 0
        print(f"    OK ({size:,} bytes)")
    except SystemExit:
        size = os.path.getsize(out_path) if os.path.exists(out_path) else 0
        print(f"    OK ({size:,} bytes)")
    except Exception as e:
        print(f"    ERROR: {e}")
    print()

# Update manifest
import json
manifest_path = os.path.join(OUTDIR, "manifest.json")
with open(manifest_path, "r", encoding="utf-8") as f:
    manifest = json.load(f)

for seg in manifest["segments"]:
    fpath = os.path.join(OUTDIR, seg["file"].replace("audio/", ""))
    if os.path.exists(fpath):
        size = os.path.getsize(fpath)
        seg["bytes"] = size
        seg["seconds"] = round(size / 192000, 2)

with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

total_size = sum(s["bytes"] for s in manifest["segments"])
print(f"\nUpdated manifest: {len(manifest['segments'])} files, {total_size/1024/1024:.1f} MB")
print("Done!")
