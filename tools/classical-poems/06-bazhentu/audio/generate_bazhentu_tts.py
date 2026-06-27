# -*- coding: utf-8 -*-
"""八陣圖 VoxCPM2 音檔生成"""

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

SEGMENTS = [
    ("home-guide", "Sadaltager", "home-guide-sadaltager.wav",
     "小朋友們，你們聽過諸葛亮嗎？他是三國時代最聰明的軍師！他設計了一個超厲害的陣法，叫做八陣圖。今天我們要來學杜甫寫的這首詩，看看諸葛亮有多厲害，也聽聽他有什麼遺憾。準備好了嗎？讓我們一起來聽！"),

    ("line1-poem-sadaltager", "Sadaltager", "line1-poem-sadaltager.wav", "功蓋三分國。"),
    ("line1-poem-sulafat", "Sulafat", "line1-poem-sulafat.wav", "功蓋三分國。"),
    ("line1-plain-sadaltager", "Sadaltager", "line1-plain-sadaltager.wav", "諸葛亮的功勞蓋過三國時期的所有人。"),
    ("line1-plain-sulafat", "Sulafat", "line1-plain-sulafat.wav", "諸葛亮的功勞蓋過三國時期的所有人。"),

    ("line2-poem-sadaltager", "Sadaltager", "line2-poem-sadaltager.wav", "名成八陣圖。"),
    ("line2-poem-sulafat", "Sulafat", "line2-poem-sulafat.wav", "名成八陣圖。"),
    ("line2-plain-sadaltager", "Sadaltager", "line2-plain-sadaltager.wav", "他因為設計八陣圖而聞名天下。"),
    ("line2-plain-sulafat", "Sulafat", "line2-plain-sulafat.wav", "他因為設計八陣圖而聞名天下。"),

    ("line3-poem-sadaltager", "Sadaltager", "line3-poem-sadaltager.wav", "江流石不轉。"),
    ("line3-poem-sulafat", "Sulafat", "line3-poem-sulafat.wav", "江流石不轉。"),
    ("line3-plain-sadaltager", "Sadaltager", "line3-plain-sadaltager.wav", "江水日夜奔流，但八陣圖的石頭從來不動。"),
    ("line3-plain-sulafat", "Sulafat", "line3-plain-sulafat.wav", "江水日夜奔流，但八陣圖的石頭從來不動。"),

    ("line4-poem-sadaltager", "Sadaltager", "line4-poem-sadaltager.wav", "遺恨失吞吳。"),
    ("line4-poem-sulafat", "Sulafat", "line4-poem-sulafat.wav", "遺恨失吞吳。"),
    ("line4-plain-sadaltager", "Sadaltager", "line4-plain-sadaltager.wav", "最遺憾的是沒能成功阻止先主去攻打吳國。"),
    ("line4-plain-sulafat", "Sulafat", "line4-plain-sulafat.wav", "最遺憾的是沒能成功阻止先主去攻打吳國。"),

    ("heart-read", "Sadaltager", "heart-guide-sadaltager.wav",
     "諸葛亮是三國時代最有智慧的人。他發明的八陣圖非常厲害，連江水都沖不走。但是，他也有做不到的事。這首詩告訴我們，再厲害的人也會有遺憾，所以我們要珍惜每個機會。"),

    ("game1-guide", "Sulafat", "game1-guide-sulafat.wav",
     "排兵布陣。把打亂的字排入正確位置，完成八陣圖！"),
    ("game2-guide", "Sulafat", "game2-guide-sulafat.wav",
     "江水流字。小船在江上漂流，按順序點擊正確的字！"),
    ("game3-guide", "Sulafat", "game3-guide-sulafat.wav",
     "石壘守城。點擊石壘找出隱藏的字，補上城牆缺口！"),

    ("word-gonggai", "Sulafat", "word-gonggai.wav", "功蓋——功勞最大、最厲害。"),
    ("word-sanfen", "Sulafat", "word-sanfen.wav", "三分——三個國家。"),
    ("word-guo", "Sulafat", "word-guo.wav", "國——國家。"),
    ("word-mingcheng", "Sulafat", "word-mingcheng.wav", "名成——名聲最大、最有名。"),
    ("word-bazhen", "Sulafat", "word-bazhen.wav", "八陣——八種陣法。"),
    ("word-tu", "Sulafat", "word-tu.wav", "圖——陣法的圖形。"),
    ("word-jiangliu", "Sulafat", "word-jiangliu.wav", "江流——江水一直流。"),
    ("word-shi", "Sulafat", "word-shi.wav", "石——石頭。"),
    ("word-buzhuan", "Sulafat", "word-buzhuan.wav", "不轉——不動、不改變。"),
    ("word-yihen", "Sulafat", "word-yihen.wav", "遺恨——很可惜、很遺憾。"),
    ("word-shi2", "Sulafat", "word-shi2.wav", "失——失去、沒能成功。"),
    ("word-tunwu", "Sulafat", "word-tunwu.wav", "吞吳——打敗吳國。"),
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
