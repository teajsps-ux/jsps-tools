"""Generate all audio for 尋隱者不遇-demo using VoxCPM2 directly (no subprocess encoding issues)."""
import sys, os, glob, json

# Must run with: C:\2026_Antigravity_語音\.venv\Scripts\python.exe THIS_FILE.py

OUTDIR = r"G:\我的雲端硬碟\slides\尋隱者不遇-demo\audio"
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
    # ═══ Home guide (Sadaltager) ═══
    ("home-guide", SADALTAGER,
     "巡隱者不遇。唐，甲導。詩人去找隱居的人，為什麼沒有見到他呢？",
     "home-guide-sadaltager.wav"),

    # ═══ Full poem (both voices) ═══
    ("poem-full-sadaltager", SADALTAGER,
     "松下問童子。言詩彩藥去。只在此山中。云深不知處。",
     "poem-sadaltager.wav"),
    ("poem-full-sulafat", SULAFAT,
     "松下問童子。言詩彩藥去。只在此山中。云深不知處。",
     "poem-sulafat.wav"),

    # ═══ Line 1: 松下問童子 ═══
    ("line1-poem-sulafat", SULAFAT,
     "松下問童子。",
     "line1-poem-sulafat.wav"),
    ("line1-plain-sulafat", SULAFAT,
     "在松豎下問小童。",
     "line1-plain-sulafat.wav"),

    # ═══ Line 2: 言師採藥去 ═══
    ("line2-poem-sulafat", SULAFAT,
     "顏詩彩要趣。",
     "line2-poem-sulafat.wav"),
    ("line2-plain-sulafat", SULAFAT,
     "童子說，老詩彩藥去了。",
     "line2-plain-sulafat.wav"),

    # ═══ Line 3: 只在此山中 ═══
    ("line3-poem-sulafat", SULAFAT,
     "只在此山中。",
     "line3-poem-sulafat.wav"),
    ("line3-plain-sulafat", SULAFAT,
     "只知道他就在這座山裡。",
     "line3-plain-sulafat.wav"),

    # ═══ Line 4: 雲深不知處 ═══
    ("line4-poem-sulafat", SULAFAT,
     "云深不知處。",
     "line4-poem-sulafat.wav"),
    ("line4-plain-sulafat", SULAFAT,
     "云物太深，不知道他在哪裡。",
     "line4-plain-sulafat.wav"),

    # ═══ Heart guide (Sadaltager) ═══
    ("heart-guide", SADALTAGER,
     "詩人來找隱居的人，卻只看到松豎、山路和云物。他有點失望，但也感受到山裡很安靜、很美。",
     "heart-guide-sadaltager.wav"),

    # ═══ 詩人的心情 - 右邊 (Sulafat) ═══
    ("heart-right", SULAFAT,
     "有時候找不到人，不一定是壞事。可以學會耐心等待，也可以欣賞風景。",
     "heart-right-sulafat.wav"),

    # ═══ Game A: 松下對話 (Sulafat) ═══
    ("game-a-guide", SULAFAT,
     "松下對話。古松之下，詩人與童子的對話，點開卷軸找出答案。",
     "game-a-guide-sulafat.wav"),

    # ═══ Game B: 山徑尋蹤 (Sulafat) ═══
    ("game-b-guide", SULAFAT,
     "山徑尋蹤。沿著山路敲開石頭，找出藏在山中的詞語。",
     "game-b-guide-sulafat.wav"),

    # ═══ Game C: 採藥竹簡 (Sulafat) ═══
     ("game-c-guide", SULAFAT,
      "彩要築撿板。把竹簡詞卡放回正確位置，完成四句詩。",
      "game-c-guide-sulafat.wav"),

    # ═══ Word explanations (Sulafat) ═══
    ("word-songxia", SULAFAT, "松下，松豎下面。", "word-songxia.wav"),
    ("word-wen", SULAFAT, "問，問。", "word-wen.wav"),
    ("word-tongzi", SULAFAT, "童子，小孩子。", "word-tongzi.wav"),
    ("word-yan", SULAFAT, "言，說。", "word-yan.wav"),
    ("word-shi", SULAFAT, "失，老失。", "word-shi.wav"),
    ("word-caiyaoqu", SULAFAT, "彩藥去，彩藥去了。", "word-caiyaoqu.wav"),
    ("word-zhizai", SULAFAT, "只在，就在。", "word-zhizai.wav"),
    ("word-cishanzhong", SULAFAT, "此山中，這座山裡。", "word-cishanzhong.wav"),
    ("word-yunshen", SULAFAT, "芸身，芸狠身、狠農。", "word-yunshen.wav"),
    ("word-buzhichu", SULAFAT, "不知處，不知道在哪裡。", "word-buzhichu.wav"),

    # ═══ Dialogue game answers (Sulafat) ═══
    ("dialogue-songxia", SULAFAT, "松下。詩人走到古松之下，清風徐來。", "dialogue-songxia.wav"),
    ("dialogue-tongzi", SULAFAT, "童子。松樹下站著一位小童，是師父的徒弟。", "dialogue-tongzi.wav"),
    ("dialogue-caiyaoqu", SULAFAT, "彩藥去。童子說，詩父上山彩藥去了。", "dialogue-caiyaoqu.wav"),
    ("dialogue-cishanzhong", SULAFAT, "此山中。童子說，詩父就在這座山裡。", "dialogue-cishanzhong.wav"),
    ("dialogue-yunshenbuzhichu", SULAFAT, "云深不知處。因為云物太深，看不見他在哪裡。", "dialogue-yunshenbuzhichu.wav"),
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
