# -*- coding: utf-8 -*-
"""春曉詞語彈窗音檔 — Sulafat 語音，含完整詞語+解釋"""

from pathlib import Path
import json, sys, time, numpy as np
import soundfile as sf
import librosa

VOICE_ROOT = Path(r"C:\2026_Antigravity_語音\voices")
OUTPUT_DIR = Path(__file__).resolve().parent

# 這些 ID 跳過 auto_trim，避免內容被誤切（如「啼了——了在叫」被切只剩一聲）
NO_TRIM_IDS = {"word-tiniao"}

WORD_SEGMENTS = [
    ("word-chunmian", "word-chunmian.wav", "春眠——春天睡覺。"),
    ("word-bujue",   "word-bujue.wav",   "不覺——沒有感覺到。"),
    ("word-xiao",    "word-xiao.wav",    "曉——天亮。"),
    ("word-chuchu",  "word-chuchu.wav",  "處處——每個地方，到處。"),
    ("word-wen",     "word-wen.wav",     "聞——聽到。"),
    ("word-tiniao",  "word-tiniao.wav",  "啼了——了在叫。"),
    ("word-yelai",   "word-yelai.wav",   "夜來——夜晚來了。"),
    ("word-fengyu",  "word-fengyu.wav",  "風雨——風和雨。"),
    ("word-sheng",   "word-sheng.wav",   "聲——聲音。"),
    ("word-hualuo",  "word-hualuo.wav",  "花落——花掉下來。"),
    ("word-zhi",     "word-zhi.wav",     "知——知道。"),
    ("word-duoshao", "word-duoshao.wav", "多少——很多還是很少。"),
]

def auto_trim(y, sr):
    if y.ndim > 1:
        y = y[:, 0]
    segments = librosa.effects.split(y, top_db=22)
    if len(segments) == 0:
        return y
    meaningful = []
    for s, e in segments:
        seg = y[s:e]
        rms = float(np.sqrt(np.mean(seg ** 2)))
        fft_len = min(4096, len(seg))
        if fft_len >= 256:
            spec = np.abs(np.fft.rfft(seg[:fft_len]))
            freqs = np.fft.rfftfreq(fft_len, 1 / sr)
            centroid = float(np.sum(freqs * spec) / (np.sum(spec) + 1e-8))
        else:
            centroid = 0
        if rms > 0.05 and not (centroid > 6000 and rms < 0.1):
            meaningful.append((s, e))
    if not meaningful:
        meaningful = [segments[0]]
    start = max(0, meaningful[0][0] - int(0.15 * sr))
    end = min(len(y), meaningful[-1][1] + int(0.1 * sr))
    trimmed = y[start:end]
    silence = np.zeros(int(0.1 * sr))
    result = np.concatenate([silence, trimmed])
    fade = int(0.02 * sr)
    if len(result) > fade:
        result[:fade] *= np.linspace(0, 1, fade)
    return result

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", nargs="*", default=None,
                        help="強制重跑指定 ID（如 --force word-tiniao），不給值則全部重跑")
    args = parser.parse_args()
    force_all = False
    force_ids = set()
    if args.force is not None:
        if len(args.force) == 0:
            force_all = True
        else:
            force_ids = set(args.force)

    repo = Path(r"C:\2026_Antigravity_語音")
    sys.path.insert(0, str(repo))
    from voxcpm import VoxCPM

    device = "cpu"
    gpu_type = repo / ".gpu_type"
    if gpu_type.exists():
        device = gpu_type.read_text(encoding="utf-8").strip() or "cpu"

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    voice_folder = VOICE_ROOT / "女-蘇拉法特(Sulafat)"
    ref_path = voice_folder / "ref_voice.wav"
    prompt_text = (voice_folder / "prompt.txt").read_text(encoding="utf-8").strip()
    if not ref_path.exists():
        raise FileNotFoundError(ref_path)

    print(f"device={device}")
    print("loading VoxCPM2 model...")
    model = VoxCPM.from_pretrained("openbmb/VoxCPM2", load_denoiser=False, device=device, optimize=False)
    sr = model.tts_model.sample_rate

    for sid, fn, txt in WORD_SEGMENTS:
        out = OUTPUT_DIR / fn
        need_force = force_all or sid in force_ids
        if out.exists() and out.stat().st_size > 1000 and not need_force:
            print(f"skip {fn}")
            continue
        print(f"generating {sid}... ", end="", flush=True)
        started = time.time()
        try:
            wav = model.generate(
                text=txt,
                prompt_wav_path=str(ref_path),
                prompt_text=prompt_text,
                reference_wav_path=str(ref_path),
                cfg_value=2.0,
                inference_timesteps=10,
            )
            if sid not in NO_TRIM_IDS:
                wav = auto_trim(wav, sr)
            else:
                # 只加極淡的頭尾 fades，保留完整內容
                fade = int(0.02 * sr)
                if len(wav) > fade * 2:
                    wav[:fade] *= np.linspace(0, 1, fade)
                    wav[-fade:] *= np.linspace(1, 0, fade)
            sf.write(str(out), wav, sr)
            secs = round(time.time() - started, 1)
            print(f"OK ({out.stat().st_size} bytes, {secs}s)")
        except Exception as exc:
            print(f"FAILED: {exc}")

if __name__ == "__main__":
    main()
