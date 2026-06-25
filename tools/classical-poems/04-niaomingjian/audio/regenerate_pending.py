# -*- coding: utf-8 -*-
"""Regenerate only the 3 pending segments after slides.html redesign."""
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
PENDING = [
    ("line2-poem-sulafat", "Sulafat", "line2-poem-sulafat.wav",
     "頁鏡春山空。"),
]

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

    print(f"device={device}")
    print("loading VoxCPM2 model...")
    model = VoxCPM.from_pretrained("openbmb/VoxCPM2", load_denoiser=False, device=device, optimize=False)

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    by_id = {item["id"]: item for item in manifest["segments"]}
    vc = {}
    cnt = 0
    for sid, vn, fn, txt in PENDING:
        out = OUTPUT_DIR / fn
        if vn not in vc:
            ref, prompt = validate_voice(vn, VOICES[vn])
            vc[vn] = (ref, prompt)
        ref, prompt = vc[vn]
        print(f"generating {sid} with {vn}...")
        started = time.time()
        try:
            wav = model.generate(text=txt, prompt_wav_path=str(ref), prompt_text=prompt,
                                 reference_wav_path=str(ref), cfg_value=2.0, inference_timesteps=20)
            sf.write(str(out), wav, model.tts_model.sample_rate)
            by_id[sid] = {"id": sid, "file": f"audio/{fn}", "voice": vn, "text": txt,
                          "status": "done", "source": "local VoxCPM2",
                          "bytes": out.stat().st_size, "seconds": round(time.time()-started, 1)}
            cnt += 1
        except Exception as e:
            by_id[sid] = {"id": sid, "file": f"audio/{fn}", "voice": vn, "text": txt,
                          "status": "failed", "source": "local VoxCPM2", "error": str(e)}
        manifest["segments"] = [by_id[s["id"]] for s in manifest["segments"]]
        MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nRegenerated {cnt}/{len(PENDING)} pending segments.")

if __name__ == "__main__":
    main()
