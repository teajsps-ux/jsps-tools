"""Update manifest.json with actual text content for each audio segment."""
import json, os

OUTDIR = r"G:\我的雲端硬碟\slides\尋隱者不遇-demo\audio"
MANIFEST = os.path.join(OUTDIR, "manifest.json")

# Text mapping from generate_audio.py segments
TEXT_MAP = {
    "home-guide": "尋隱者不遇。唐，賈島。詩人去找隱居的人，為什麼沒有見到他呢？",
    "poem-full-sadaltager": "松下問童子。言師採藥去。只在此山中。雲深不知處。",
    "poem-full-sulafat": "松下問童子。言師採藥去。只在此山中。雲深不知處。",
    "line1-poem-sulafat": "松下問童子。",
    "line1-plain-sulafat": "在松樹下問小童。",
    "line2-poem-sulafat": "言師採藥去。",
    "line2-plain-sulafat": "童子說，老師採藥去了。",
    "line3-poem-sulafat": "只在此山中。",
    "line3-plain-sulafat": "只知道他就在這座山裡。",
    "line4-poem-sulafat": "雲深不知處。",
    "line4-plain-sulafat": "雲霧太深，不知道他在哪裡。",
    "heart-guide": "詩人來找隱居的人，卻只看到松樹、山路和雲霧。他有點失望，但也感受到山裡很安靜、很美。",
    "game-a-guide": "松下對話。古松之下，詩人與童子的對話，點開卷軸找出答案。",
    "game-b-guide": "山徑尋蹤。沿著山路敲開石頭，找出藏在山中的詞語。",
    "game-c-guide": "採藥竹簡版。把竹簡詞卡放回正確位置，完成四句詩。",
    "word-songxia": "松下，松樹下面。",
    "word-wen": "問，問。",
    "word-tongzi": "童子，小孩子。",
    "word-yan": "言，說。",
    "word-shi": "師，老師。",
    "word-caiyaoqu": "採藥去，採藥去了。",
    "word-zhizai": "只在，就在。",
    "word-cishanzhong": "此山中，這座山裡。",
    "word-yunshen": "雲深，雲很深、很濃。",
    "word-buzhichu": "不知處，不知道在哪裡。",
    "dialogue-songxia": "松下。詩人走到古松之下，清風徐來。",
    "dialogue-tongzi": "童子。松樹下站著一位小童，是師父的徒弟。",
    "dialogue-caiyaoqu": "採藥去。童子說，師父上山採藥去了。",
    "dialogue-cishanzhong": "此山中。童子說，師父就在這座山裡。",
    "dialogue-yunshenbuzhichu": "雲深不知處。因為雲霧太深，看不見他在哪裡。",
}

with open(MANIFEST, "r", encoding="utf-8") as f:
    manifest = json.load(f)

for seg in manifest["segments"]:
    sid = seg["id"]
    if sid in TEXT_MAP:
        seg["text"] = TEXT_MAP[sid]

with open(MANIFEST, "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

print(f"Updated {len(manifest['segments'])} segments with text content.")
