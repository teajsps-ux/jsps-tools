# -*- coding: utf-8 -*-
"""只重做含「鳥」字的 7 段音檔，鳥→聊(liáo) workaround"""

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

# 鳥 → 聊(liáo) workaround
SEGMENTS = [
    ("poem-full-sadaltager", "Sadaltager", "poem-sadaltager.wav",
     "春眠不覺曉，處處聞啼聊，夜來風雨聲，花落知多少。"),
    ("poem-full-sulafat", "Sulafat", "poem-sulafat.wav",
     "春眠不覺曉，處處聞啼聊，夜來風雨聲，花落知多少。"),
    ("line2-poem-sadaltager", "Sadaltager", "line2-poem-sadaltager.wav",
     "處處聞啼聊。"),
    ("line2-poem-sulafat", "Sulafat", "line2-poem-sulafat.wav",
     "處處聞啼聊。"),
    ("line2-plain-sadaltager", "Sadaltager", "line2-plain-sadaltager.wav",
     "到處都聽到聊兒在叫。"),
    ("line2-plain-sulafat", "Sulafat", "line2-plain-sulafat.wav",
     "到處都聽到聊兒在叫。"),
    ("heart-guide", "Sadaltager", "heart-guide-sadaltager.wav",
     "孟浩然在春天的一個早晨醒來，聽到聊叫，想起昨晚的風雨，心裡想：不知道花落了多少。他喜歡春天，也捨不得春天離開。詩人想告訴我們：春天的花很快就會凋謝，美好的時光要珍惜。每天睜開眼睛，就可以用心感受身邊的美好。"),
]


def load_manifest():
    if not MANIFEST.exists():
        return {"workflow": "local-first", "segments": []}
    try:
        return json.loads(MANIFEST.read_text(encoding="utf-8"))
    except Exception:
        return {"workflow": "local-first", "segments": []}


def save_manifest(m):
    MANIFEST.write_text(json.dumps(m, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    repo = Path(r"C:\2026_Antigravity_語音")
    sys.path.insert(0, str(repo))
    from voxcpm import VoxCPM

    device = (repo / ".gpu_type").read_text(encoding="utf-8").strip() or "cpu"
    manifest = load_manifest()
    by_id = {item.get("id"): item for item in manifest.get("segments", [])}

    print(f"device={device}")
    print("loading VoxCPM2...")
    model = VoxCPM.from_pretrained("openbmb/VoxCPM2", load_denoiser=False, device=device, optimize=False)

    vc = {}
    for sid, vn, fn, txt in SEGMENTS:
        out = OUTPUT_DIR / fn
        if vn not in vc:
            ref, pt = (VOICES[vn] / "ref_voice.wav", (VOICES[vn] / "prompt.txt").read_text(encoding="utf-8").strip())
            vc[vn] = (str(ref), pt)
        ref, pt = vc[vn]

        print(f"generating {sid} with {vn}...")
        t0 = time.time()
        try:
            wav = model.generate(text=txt, prompt_wav_path=ref, prompt_text=pt,
                                 reference_wav_path=ref, cfg_value=2.0, inference_timesteps=10)
            sf.write(str(out), wav, model.tts_model.sample_rate)
            by_id[sid] = {"id": sid, "file": f"audio/{fn}", "voice": vn, "text": txt,
                          "status": "done", "source": "local VoxCPM2",
                          "bytes": out.stat().st_size, "seconds": round(time.time()-t0,1)}
        except Exception as e:
            by_id[sid] = {"id": sid, "file": f"audio/{fn}", "voice": vn, "text": txt,
                          "status": "failed", "source": "local VoxCPM2", "error": str(e)}
        save_manifest({"workflow": "local-first", "voicesRoot": str(VOICE_ROOT),
                       "segments": [by_id[k] for k,*_ in SEGMENTS if k in by_id]})

    print("done.")


if __name__ == "__main__":
    main()
