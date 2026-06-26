"""Generate all audio for 新嫁娘-05-demo using VoxCPM2 directly (no subprocess encoding issues)."""
import sys, os, glob, json

# Must run with: C:\2026_Antigravity_語音\.venv\Scripts\python.exe THIS_FILE.py

OUTDIR = r"G:\我的雲端硬碟\slides\新嫁娘-05-demo\audio"
VOICES_DIR = r"C:\2026_Antigravity_語音\voices"

def find_voice(name):
    """Find voice ref file using glob (avoids known-path encoding)."""
    pattern = os.path.join(VOICES_DIR, f"*{name}*", "ref_voice.wav")
    matches = glob.glob(pattern)
    if not matches:
        raise FileNotFoundError(f"No voice file found for: {name}")
    return matches[0]

SADALTAGER = find_voice("Sadaltager")
SULAFAT = find_voice("Sulafat")

print(f"Sadaltager ref: {SADALTAGER}")
print(f"Sulafat ref:    {SULAFAT}")

# All segments: (id, voice_ref, text, filename)
# Text EXACTLY matches on-screen HTML content
# Speed control instruction for VoxCPM2
CONTROL = "Speak slowly and clearly for children, gentle voice"

segments = [
    # ═══ Home guide ═══
    ("home-guide", SADALTAGER,
     "新嫁娘。唐，王建。新嫁娘第一天到婆婆家，要親手做飯菜。她會怎麼做呢？",
     "home-guide-sadaltager.wav"),

    # ═══ Full poem (completeness) ═══
    ("poem-full-sadaltager", SADALTAGER,
     "三日入廚下。洗手作羹湯。未諳姑食性。先遣小姑嚐。",
     "poem-sadaltager.wav"),
    ("poem-full-sulafat", SULAFAT,
     "三日入廚下。洗手作羹湯。未諳姑食性。先遣小姑嚐。",
     "poem-sulafat.wav"),

    # ═══ Line 1 ═══
    ("line1-poem-sadaltager", SADALTAGER,
     "三日入廚下。",
     "line1-poem-sadaltager.wav"),
    ("line1-poem-sulafat", SULAFAT,
     "三日入廚下。",
     "line1-poem-sulafat.wav"),
    ("line1-plain-sadaltager", SADALTAGER,
     "新婚第三天，走進廚房。",
     "line1-plain-sadaltager.wav"),
    ("line1-plain-sulafat", SULAFAT,
     "新婚第三天，走進廚房。",
     "line1-plain-sulafat.wav"),

    # ═══ Line 2 ═══
    ("line2-poem-sadaltager", SADALTAGER,
     "洗手作羹湯。",
     "line2-poem-sadaltager.wav"),
    ("line2-poem-sulafat", SULAFAT,
     "洗手作羹湯。",
     "line2-poem-sulafat.wav"),
    ("line2-plain-sadaltager", SADALTAGER,
     "洗洗手，開始做羹湯。",
     "line2-plain-sadaltager.wav"),
    ("line2-plain-sulafat", SULAFAT,
     "洗洗手，開始做羹湯。",
     "line2-plain-sulafat.wav"),

    # ═══ Line 3 ═══
    ("line3-poem-sadaltager", SADALTAGER,
     "未諳姑食性。",
     "line3-poem-sadaltager.wav"),
    ("line3-poem-sulafat", SULAFAT,
     "未諳姑食性。",
     "line3-poem-sulafat.wav"),
    ("line3-plain-sadaltager", SADALTAGER,
     "還不熟悉婆婆喜歡吃什麼。",
     "line3-plain-sadaltager.wav"),
    ("line3-plain-sulafat", SULAFAT,
     "還不熟悉婆婆喜歡吃什麼。",
     "line3-plain-sulafat.wav"),

    # ═══ Line 4 ═══
    ("line4-poem-sadaltager", SADALTAGER,
     "先遣小姑嚐。",
     "line4-poem-sadaltager.wav"),
    ("line4-poem-sulafat", SULAFAT,
     "先遣小姑嚐。",
     "line4-poem-sulafat.wav"),
    ("line4-plain-sadaltager", SADALTAGER,
     "先請小姑子吃吃看味道。",
     "line4-plain-sadaltager.wav"),
    ("line4-plain-sulafat", SULAFAT,
     "先請小姑子吃吃看味道。",
     "line4-plain-sulafat.wav"),

    # ═══ Heart guide ═══
    ("heart-guide", SADALTAGER,
     "新嫁娘第一天到婆婆家，不知道婆婆喜歡吃什麼口味。她很聰明，先請小姑子吃吃看，"
     "如果小姑覺得好吃，婆婆應該也會喜歡。詩人想告訴我們：遇到不熟悉的事情，可以"
     "先問一問、試一試，這樣會做得更好。貼心的人會想到別人的感受。",
     "heart-guide-sadaltager.wav"),

    # ═══ Game guides ═══
    ("game-footprint-guide", SULAFAT,
     "回家路線。新嫁娘要沿著腳印走回廚房。請點擊正確的腳印，讓它飛入詩句空格。",
     "game-footprint-guide-sulafat.wav"),
    ("game-ingredient-guide", SULAFAT,
     "食材收集。做羹湯需要各種食材！請點擊正確的食材，讓它飛入詩句空格。",
     "game-ingredient-guide-sulafat.wav"),
    ("game-soup-guide", SULAFAT,
     "羹湯烹飪。把食材放入鍋中煮湯！請點擊正確的食材，讓它們進入鍋中，完成整首詩。",
     "game-soup-guide-sulafat.wav"),

    # ═══ Word popups ═══
    # Format: "WORD，EXPLANATION" matching popup: title=WORD, body=EXPLANATION
    ("word-sanri", SULAFAT, "三日，新婚第三天。", "word-sanri.wav"),
    ("word-ru", SULAFAT, "入，走進去。", "word-ru.wav"),
    ("word-chuxia", SULAFAT, "廚下，廚房裡面。", "word-chuxia.wav"),
    ("word-xishou", SULAFAT, "洗手，把手洗乾淨，準備做菜。", "word-xishou.wav"),
    ("word-zuo", SULAFAT, "作，做、製作。", "word-zuo.wav"),
    ("word-gengtang", SULAFAT, "羹湯，煮好的湯。", "word-gengtang.wav"),
    ("word-wei", SULAFAT, "未，還不。", "word-wei.wav"),
    ("word-an", SULAFAT, "諳，熟悉、了解。", "word-an.wav"),
    ("word-gu", SULAFAT, "姑，婆婆，丈夫的媽媽。", "word-gu.wav"),
    ("word-shixing", SULAFAT, "食性，喜歡吃什麼的口味。", "word-shixing.wav"),
    ("word-xianqian", SULAFAT, "先遣，先請、先讓。", "word-xianqian.wav"),
    ("word-xiaogu", SULAFAT, "小姑，丈夫的妹妹。", "word-xiaogu.wav"),
    ("word-chang", SULAFAT, "嚐，吃吃看味道。", "word-chang.wav"),
]

os.makedirs(OUTDIR, exist_ok=True)

# Delete all existing .wav first
for f in os.listdir(OUTDIR):
    if f.endswith(".wav"):
        os.remove(os.path.join(OUTDIR, f))
        print(f"Deleted: {f}")

print(f"\nGenerating {len(segments)} audio files...\n")

from voxcpm.cli import main

for i, (sid, voice_ref, text, fname) in enumerate(segments):
    out_path = os.path.join(OUTDIR, fname)
    label = fname.replace(".wav", "")
    print(f"[{i+1}/{len(segments)}] {label}", flush=True)
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

# ─── Create manifest.json ───
print("\nCreating manifest.json...")
manifest = {
    "workflow": "local-first",
    "voicesRoot": VOICES_DIR,
    "segments": [],
}

for fname in sorted(os.listdir(OUTDIR)):
    if not fname.endswith(".wav"):
        continue
    fpath = os.path.join(OUTDIR, fname)
    size = os.path.getsize(fpath)
    duration = round(size / 192000, 2)

    base = fname.replace(".wav", "")
    if base.endswith("-sadaltager"):
        voice = "Sadaltager"
        sid = base.replace("-sadaltager", "")
    elif base.endswith("-sulafat"):
        voice = "Sulafat"
        sid = base.replace("-sulafat", "")
    else:
        voice = "unknown"
        sid = base

    manifest["segments"].append({
        "id": sid, "file": f"audio/{fname}", "voice": voice,
        "text": "",  # not stored in manifest to avoid encoding issues
        "status": "done", "source": "local VoxCPM2",
        "bytes": size, "seconds": duration,
    })

manifest_path = os.path.join(OUTDIR, "manifest.json")
with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

total_size = sum(s["bytes"] for s in manifest["segments"])
print(f"\n{len(manifest['segments'])} files, {total_size/1024/1024:.1f} MB")
print("Done!")
