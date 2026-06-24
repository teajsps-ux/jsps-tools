# -*- coding: utf-8 -*-
"""春曉 VoxCPM2 音檔 — 僅替換缺陷單字，不改寫句子（學江雪鳥→了做法）"""

from pathlib import Path
import json, sys, time
import soundfile as sf

VOICE_ROOT = Path(r"C:\2026_Antigravity_語音\voices")
OUTPUT_DIR = Path(__file__).resolve().parent
MANIFEST = OUTPUT_DIR / "manifest.json"

VOICES = {
    "Sadaltager": VOICE_ROOT / "男-薩達爾塔格(Sadaltager)",
    "Sulafat": VOICE_ROOT / "女-蘇拉法特(Sulafat)",
}

# ── 缺陷字 workaround（只換字，不改句）──
#   鳥 niǎo → 遼 liáo
#   覺 jué  → 決 jué
#   跡 jī   → 積 jī
#   暈 yùn  → 雲 yún
#   點中   → 點擊

SEGMENTS = [
    ("home-guide", "Sadaltager", "home-guide-sadaltager.wav",
     "春曉。唐，孟浩然。春天的早晨，詩人醒來後聽到了什麼？"),

    ("poem-full-sadaltager", "Sadaltager", "poem-sadaltager.wav",
     "春眠不覺曉，處處聞啼遼，夜來風雨聲，花落知多少。"),
    ("poem-full-sulafat", "Sulafat", "poem-sulafat.wav",
     "春眠不覺曉，處處聞啼遼，夜來風雨聲，花落知多少。"),

    ("line1-poem-sadaltager", "Sadaltager", "line1-poem-sadaltager.wav",
     "春眠不覺曉。"),
    ("line1-poem-sulafat", "Sulafat", "line1-poem-sulafat.wav",
     "春眠不覺曉。"),
    ("line1-plain-sadaltager", "Sadaltager", "line1-plain-sadaltager.wav",
     "春天睡覺，不知不決天就亮了。"),
    ("line1-plain-sulafat", "Sulafat", "line1-plain-sulafat.wav",
     "春天睡覺，不知不決天就亮了。"),

    ("line2-poem-sadaltager", "Sadaltager", "line2-poem-sadaltager.wav",
     "處處聞啼遼。"),
    ("line2-poem-sulafat", "Sulafat", "line2-poem-sulafat.wav",
     "處處聞啼遼。"),
    ("line2-plain-sadaltager", "Sadaltager", "line2-plain-sadaltager.wav",
     "到處都聽到遼兒在叫。"),
    ("line2-plain-sulafat", "Sulafat", "line2-plain-sulafat.wav",
     "到處都聽到遼兒在叫。"),

    ("line3-poem-sadaltager", "Sadaltager", "line3-poem-sadaltager.wav",
     "夜來風雨聲。"),
    ("line3-poem-sulafat", "Sulafat", "line3-poem-sulafat.wav",
     "夜來風雨聲。"),
    ("line3-plain-sadaltager", "Sadaltager", "line3-plain-sadaltager.wav",
     "夜裡傳來風雨的聲音。"),
    ("line3-plain-sulafat", "Sulafat", "line3-plain-sulafat.wav",
     "夜裡傳來風雨的聲音。"),

    ("line4-poem-sadaltager", "Sadaltager", "line4-poem-sadaltager.wav",
     "花落知多少。"),
    ("line4-poem-sulafat", "Sulafat", "line4-poem-sulafat.wav",
     "花落知多少。"),
    ("line4-plain-sadaltager", "Sadaltager", "line4-plain-sadaltager.wav",
     "不知道花朵落了多少。"),
    ("line4-plain-sulafat", "Sulafat", "line4-plain-sulafat.wav",
     "不知道花朵落了多少。"),

    ("heart-guide", "Sadaltager", "heart-guide-sadaltager.wav",
     "孟浩然在春天的一個早晨醒來，聽到遼叫，想起昨晚的風雨，心裡想：不知道花落了多少。他喜歡春天，也捨不得春天離開。詩人想告訴我們：春天的花很快就會凋謝，美好的時光要珍惜。每天睜開眼睛，就可以用心感受身邊的美好。"),

    ("game-cloud-guide", "Sulafat", "game-cloud-guide-sulafat.wav",
     "匀朵找字。詩人仰望天空，匀朵裡藏著詞語，請點擊正確的匀，讓詞語飛回詩句。"),
    ("game-ink-guide", "Sulafat", "game-ink-guide-sulafat.wav",
     "墨積顯字。詩人正在書寫，墨滴落在紙上，請點擊正確的墨，讓墨積雲開顯現詞語。"),
    ("game-flower-guide", "Sulafat", "game-flower-guide-sulafat.wav",
     "落花收集。花瓣飄落，請點擊正確的花瓣，讓它飛入詩句空格。"),

    ("word-tiniao", "Sulafat", "word-tiniao.wav", "遼。"),
]


def load_existing_manifest():
    if not MANIFEST.exists():
        return {"workflow": "local-first", "segments": []}
    try:
        return json.loads(MANIFEST.read_text(encoding="utf-8"))
    except Exception:
        return {"workflow": "local-first", "segments": []}


def save_manifest(m):
    MANIFEST.write_text(json.dumps(m, ensure_ascii=False, indent=2), encoding="utf-8")


def validate_voice(name, folder):
    ref = folder / "ref_voice.wav"
    prompt = folder / "prompt.txt"
    if not ref.exists():
        raise FileNotFoundError(ref)
    if not prompt.exists():
        raise FileNotFoundError(prompt)
    return ref, prompt.read_text(encoding="utf-8").strip()


def main():
    repo = Path(r"C:\2026_Antigravity_語音")
    sys.path.insert(0, str(repo))
    from voxcpm import VoxCPM

    device = "cpu"
    gpu_type = repo / ".gpu_type"
    if gpu_type.exists():
        device = gpu_type.read_text(encoding="utf-8").strip() or "cpu"

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest = load_existing_manifest()
    by_id = {item.get("id"): item for item in manifest.get("segments", [])}

    print(f"device={device}")
    print("loading VoxCPM2 model...")
    model = VoxCPM.from_pretrained("openbmb/VoxCPM2", load_denoiser=False, device=device, optimize=False)

    vc = {}
    cnt = 0
    for sid, vn, fn, txt in SEGMENTS:
        out = OUTPUT_DIR / fn
        if vn not in vc:
            ref, prompt = validate_voice(vn, VOICES[vn])
            vc[vn] = (ref, prompt)
        ref, prompt = vc[vn]

        print(f"generating {sid} with {vn}...")
        started = time.time()
        try:
            wav = model.generate(text=txt, prompt_wav_path=str(ref), prompt_text=prompt,
                                 reference_wav_path=str(ref), cfg_value=2.0, inference_timesteps=10)
            sf.write(str(out), wav, model.tts_model.sample_rate)
            by_id[sid] = {"id": sid, "file": f"audio/{fn}", "voice": vn, "text": txt,
                          "status": "done", "source": "local VoxCPM2",
                          "bytes": out.stat().st_size, "seconds": round(time.time()-started,1)}
            cnt += 1
        except Exception as e:
            by_id[sid] = {"id": sid, "file": f"audio/{fn}", "voice": vn, "text": txt,
                          "status": "failed", "source": "local VoxCPM2", "error": str(e)}
        save_manifest({"workflow": "local-first", "voicesRoot": str(VOICE_ROOT),
                       "segments": [by_id[k] for k,*_ in SEGMENTS if k in by_id]})
    print(f"\nRegenerated {cnt} segments.")


if __name__ == "__main__":
    main()
