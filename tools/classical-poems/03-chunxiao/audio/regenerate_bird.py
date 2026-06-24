# -*- coding: utf-8 -*-
"""春曉 — 僅重做含「鳥」字的7段，使用原始鳥字（不做 workaround）"""
from pathlib import Path
import json, sys, time
import soundfile as sf

VOICE_ROOT = Path(r"C:\2026_Antigravity_語音\voices")
OUTPUT_DIR = Path(__file__).resolve().parent

VOICES = {
    "Sadaltager": VOICE_ROOT / "男-薩達爾塔格(Sadaltager)",
    "Sulafat": VOICE_ROOT / "女-蘇拉法特(Sulafat)",
}

# 只用原始鳥字，不做 workaround
SEGMENTS = [
    ("poem-full-sadaltager", "Sadaltager", "poem-sadaltager.wav",
     "春眠不覺曉，處處聞啼鳥，夜來風雨聲，花落知多少。"),
    ("poem-full-sulafat", "Sulafat", "poem-sulafat.wav",
     "春眠不覺曉，處處聞啼鳥，夜來風雨聲，花落知多少。"),
    ("line2-poem-sadaltager", "Sadaltager", "line2-poem-sadaltager.wav",
     "處處聞啼鳥。"),
    ("line2-poem-sulafat", "Sulafat", "line2-poem-sulafat.wav",
     "處處聞啼鳥。"),
    ("line2-plain-sadaltager", "Sadaltager", "line2-plain-sadaltager.wav",
     "到處都聽到鳥兒在叫。"),
    ("line2-plain-sulafat", "Sulafat", "line2-plain-sulafat.wav",
     "到處都聽到鳥兒在叫。"),
    ("heart-guide", "Sadaltager", "heart-guide-sadaltager.wav",
     "孟浩然在春天的一個早晨醒來，聽到鳥叫，想起昨晚的風雨，心裡想：不知道花落了多少。他喜歡春天，也捨不得春天離開。詩人想告訴我們：春天的花很快就會凋謝，美好的時光要珍惜。每天睜開眼睛，就可以用心感受身邊的美好。"),
]

def main():
    repo = Path(r"C:\2026_Antigravity_語音")
    sys.path.insert(0, str(repo))
    from voxcpm import VoxCPM

    device = "cpu"
    gpu_type = repo / ".gpu_type"
    if gpu_type.exists():
        device = gpu_type.read_text(encoding="utf-8").strip() or "cpu"

    print(f"device={device}, loading VoxCPM2...")
    model = VoxCPM.from_pretrained("openbmb/VoxCPM2", load_denoiser=False, device=device, optimize=False)

    vc = {}
    for sid, vn, fn, txt in SEGMENTS:
        out = OUTPUT_DIR / fn
        if vn not in vc:
            ref = VOICES[vn] / "ref_voice.wav"
            prompt = (VOICES[vn] / "prompt.txt").read_text(encoding="utf-8").strip()
            vc[vn] = (ref, prompt)
        ref, prompt = vc[vn]

        print(f"generating {sid} ({vn}): {txt}")
        started = time.time()
        try:
            wav = model.generate(text=txt, prompt_wav_path=str(ref), prompt_text=prompt,
                                 reference_wav_path=str(ref), cfg_value=2.0, inference_timesteps=10)
            sf.write(str(out), wav, model.tts_model.sample_rate)
            print(f"  OK {fn} ({round(time.time()-started,1)}s)")
        except Exception as e:
            print(f"  FAIL {fn}: {e}")

    print("done.")

if __name__ == "__main__":
    main()
