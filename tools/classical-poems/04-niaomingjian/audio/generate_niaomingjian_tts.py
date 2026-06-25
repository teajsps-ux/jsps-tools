# -*- coding: utf-8 -*-
"""鳥鳴澗 VoxCPM2 音檔 — 鳥→遼 workaround（同春曉做法）"""

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

# 鳥 → 遼（VoxCPM2 缺陷字 workaround）
SEGMENTS = [
     ("home-guide", "Sadaltager", "home-guide-sadaltager.wav",
      "遼鳴箭。唐，王維。天黑啦～月姑娘探出頭來。王維靜靜站在春天的山裡，樹起耳朵，你猜，他聽到了什麼？"),

    ("poem-full-sadaltager", "Sadaltager", "poem-sadaltager.wav",
     "人閒桂花落，夜靜春山空，月出驚山遼，時鳴春箭中。"),
    ("poem-full-sulafat", "Sulafat", "poem-sulafat.wav",
     "人閒桂花落，夜靜春山空，月出驚山遼，時鳴春箭中。"),

    ("line1-poem-sadaltager", "Sadaltager", "line1-poem-sadaltager.wav", "人閒桂花落。"),
    ("line1-poem-sulafat", "Sulafat", "line1-poem-sulafat.wav", "人閒桂花落。"),
    ("line1-plain-sadaltager", "Sadaltager", "line1-plain-sadaltager.wav", "人們悠閒自在，桂花輕輕飄落。"),
    ("line1-plain-sulafat", "Sulafat", "line1-plain-sulafat.wav", "人們悠閒自在，桂花輕輕飄落。"),

    ("line2-poem-sadaltager", "Sadaltager", "line2-poem-sadaltager.wav", "夜靜春山空。"),
    ("line2-poem-sulafat", "Sulafat", "line2-poem-sulafat.wav", "頁鏡春山空。"),
    ("line2-plain-sadaltager", "Sadaltager", "line2-plain-sadaltager.wav", "夜晚寧靜，春天的山林顯得空曠。"),
    ("line2-plain-sulafat", "Sulafat", "line2-plain-sulafat.wav", "夜晚寧靜，春天的山林顯得空曠。"),

    ("line3-poem-sadaltager", "Sadaltager", "line3-poem-sadaltager.wav", "月出驚山遼。"),
    ("line3-poem-sulafat", "Sulafat", "line3-poem-sulafat.wav", "月出驚山遼。"),
    ("line3-plain-sadaltager", "Sadaltager", "line3-plain-sadaltager.wav", "月亮出來了，驚動了山中的遼兒。"),
    ("line3-plain-sulafat", "Sulafat", "line3-plain-sulafat.wav", "月亮出來了，驚動了山中的遼兒。"),

    ("line4-poem-sadaltager", "Sadaltager", "line4-poem-sadaltager.wav", "時鳴春箭中。"),
    ("line4-poem-sulafat", "Sulafat", "line4-poem-sulafat.wav", "時鳴春箭中。"),
    ("line4-plain-sadaltager", "Sadaltager", "line4-plain-sadaltager.wav", "遼兒不時在春天的溪谷裡鳴叫。"),
    ("line4-plain-sulafat", "Sulafat", "line4-plain-sulafat.wav", "遼兒不時在春天的溪谷裡鳴叫。"),

    ("heart-guide", "Sadaltager", "heart-guide-sadaltager.wav",
     "王維在春天的夜晚，一個人靜靜地站著。桂花輕輕飄落，春天的山很安靜。月亮出來的時候，遼兒被驚動了，在山谷裡叫了起來。他覺得這個夜晚又安靜又熱鬧。詩人想告訴我們：有時候，越安靜的環境，越能聽見細小的聲音。當我們靜下心來，就能發現身邊有很多美好的聲音和變化。"),

    ("game-flower-guide", "Sulafat", "game-flower-guide-sulafat.wav",
     "桂花收集。桂花飄落，詩人伸手接住。請點擊正確的桂花，讓花瓣飛入詩句空格。"),
     ("game-cloud-guide", "Sulafat", "game-cloud-guide-sulafat.wav",
      "月光驚遼。月亮出來了，山遼被驚醒，四處驚慌飛舞。請點擊正確的遼，讓詞語飛回詩句。"),
     ("game-ink-guide", "Sulafat", "game-ink-guide-sulafat.wav",
      "月光石。月亮倒映在山箭中，水底的月光石閃閃發亮。請點擊正確的石頭，讓它浮出水面送字回詩句。"),

    ("word-renxian", "Sulafat", "word-renxian.wav", "人閒——人們悠閒自在。"),
    ("word-guihua", "Sulafat", "word-guihua.wav", "桂花——一種花，秋天開花，有香氣。"),
    ("word-luo", "Sulafat", "word-luo.wav", "駱——掉下來。"),
    ("word-yejing", "Sulafat", "word-yejing.wav", "夜靜——夜晚安靜。"),
    ("word-chunshan", "Sulafat", "word-chunshan.wav", "春山——春天的山。"),
    ("word-kong", "Sulafat", "word-kong.wav", "空——空曠，安靜沒有聲音。"),
    ("word-yuechu", "Sulafat", "word-yuechu.wav", "月出——月亮出來了。"),
    ("word-jing", "Sulafat", "word-jing.wav", "驚——驚動、嚇到。"),
    ("word-shandiao", "Sulafat", "word-shandiao.wav", "山遼——山中的遼兒。"),
    ("word-shiing", "Sulafat", "word-shiing.wav", "時鳴——時而鸣叫、不時地叫。"),
    ("word-chunjian", "Sulafat", "word-chunjian.wav", "春箭——春天的小溪、山溝。"),
    ("word-zhong", "Sulafat", "word-zhong.wav", "中——裡面。"),
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

    device = "cuda"
    gpu_type = repo / ".gpu_type"
    if gpu_type.exists():
        device = gpu_type.read_text(encoding="utf-8").strip() or "cuda"

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
                          "bytes": out.stat().st_size, "seconds": round(time.time()-started, 1)}
            cnt += 1
        except Exception as e:
            by_id[sid] = {"id": sid, "file": f"audio/{fn}", "voice": vn, "text": txt,
                          "status": "failed", "source": "local VoxCPM2", "error": str(e)}
        save_manifest({"workflow": "local-first", "voicesRoot": str(VOICE_ROOT),
                       "segments": [by_id[k] for k, *_ in SEGMENTS if k in by_id]})
    print(f"\nGenerated {cnt}/{len(SEGMENTS)} segments.")

if __name__ == "__main__":
    main()
