import base64
import json
import os
import time
import urllib.error
import urllib.request
import wave
from pathlib import Path


BASE = Path(__file__).resolve().parent
API_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
MODEL = "gemini-3.1-flash-tts-preview"


SEGMENTS = [
    ("home-guide", "Sadaltager", "home-guide-sadaltager.wav", "請用台灣國語，語速稍慢，聲音自然，適合國小低年級學生。九月九日憶山東兄弟。唐，王維。請先聽整首詩，想一想：詩人在節日裡，為什麼特別想家？"),
    ("poem-full-sadaltager", "Sadaltager", "poem-sadaltager.wav", "九月九日憶山東兄弟。唐，王維。獨在異鄉為異客。每逢佳節倍思親。遙知兄弟登高處。遍插茱萸少一人。"),
    ("poem-full-sulafat", "Sulafat", "poem-sulafat.wav", "九月九日憶山東兄弟。唐，王維。獨在異鄉為異客。每逢佳節倍思親。遙知兄弟登高處。遍插茱萸少一人。"),
    ("line1-meaning", "Sadaltager", "line1-meaning-sadaltager.wav", "獨在異鄉為異客。 我一個人在外地，不在自己的家鄉。"),
    ("line2-meaning", "Sadaltager", "line2-meaning-sadaltager.wav", "每逢佳節倍思親。 每到節日，我更想念家人。"),
    ("line3-meaning", "Sadaltager", "line3-meaning-sadaltager.wav", "遙知兄弟登高處。 我想到兄弟們正在登高。"),
    ("line4-meaning", "Sadaltager", "line4-meaning-sadaltager.wav", "遍插茱萸少一人。 大家都插著茱萸，可是少了我。"),
    ("heart-guide", "Sadaltager", "heart-guide-sadaltager.wav", "王維一個人在外地。重陽節到了，他想到家人正在一起過節，心裡很想家。這首詩提醒我們，平常也可以多關心家人。"),
    ("game-guide", "Sulafat", "game-guide-sulafat.wav", "請挑出最能表現節日時更想念家人的詩句。"),
    ("game-order-guide", "Leda", "game-order-guide-leda.wav", "請把四句詩的詞語重新排好。"),
    ("game-blank-guide", "Zephyr", "game-blank-guide-zephyr.wav", "請把缺少的詞語放回詩句裡。"),
    ("right", "Puck", "right-puck.wav", "答對了。"),
    ("wrong", "Sulafat", "wrong-sulafat.wav", "再想想，換一個試試。"),
    ("compare-poem-1", "Sulafat", "compare-poem-1-sulafat.wav", "獨在異鄉為異客。"),
    ("compare-poem-2", "Sulafat", "compare-poem-2-sulafat.wav", "每逢佳節倍思親。"),
    ("compare-poem-3", "Sulafat", "compare-poem-3-sulafat.wav", "遙知兄弟登高處。"),
    ("compare-poem-4", "Sulafat", "compare-poem-4-sulafat.wav", "遍插茱萸少一人。"),
    ("compare-plain-1", "Sadaltager", "compare-plain-1-sadaltager.wav", "我一個人在外地，不在自己的家鄉。"),
    ("compare-plain-2", "Sadaltager", "compare-plain-2-sadaltager.wav", "每到節日，我更想念家人。"),
    ("compare-plain-3", "Sadaltager", "compare-plain-3-sadaltager.wav", "我想到兄弟們正在登高。"),
    ("compare-plain-4", "Sadaltager", "compare-plain-4-sadaltager.wav", "大家都插著茱萸，可是少了我。"),
]


def write_wav(path: Path, pcm: bytes) -> None:
    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(24000)
        wf.writeframes(pcm)


def request_audio(text: str, voice: str) -> bytes:
    body = {
        "contents": [{"parts": [{"text": text}]}],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {
                "voiceConfig": {
                    "prebuiltVoiceConfig": {"voiceName": voice}
                }
            },
        },
        "model": MODEL,
    }
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent",
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json", "x-goog-api-key": API_KEY or ""},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=90) as res:
        data = json.loads(res.read().decode("utf-8"))
    b64 = data["candidates"][0]["content"]["parts"][0]["inlineData"]["data"]
    return base64.b64decode(b64)


def main() -> int:
    if not API_KEY:
        raise SystemExit("missing GEMINI_API_KEY or GOOGLE_API_KEY")

    status = []
    for seg_id, voice, filename, text in SEGMENTS:
        out = BASE / filename
        item = {
            "id": seg_id,
            "voice": voice,
            "file": f"audio/{filename}",
            "status": "pending",
            "error": "",
            "model": MODEL,
        }
        if out.exists() and out.stat().st_size > 1024:
            item["status"] = "done"
            item["bytes"] = out.stat().st_size
            status.append(item)
            continue
        try:
            pcm = request_audio(text, voice)
            write_wav(out, pcm)
            if out.stat().st_size < 1024:
                raise RuntimeError(f"invalid tiny wav: {out.stat().st_size} bytes")
            item["status"] = "done"
            item["bytes"] = out.stat().st_size
        except urllib.error.HTTPError as exc:
            item["status"] = "failed"
            item["error"] = f"HTTP {exc.code}: {exc.read().decode('utf-8', errors='ignore')[:600]}"
        except Exception as exc:
            item["status"] = "failed"
            item["error"] = str(exc)
        status.append(item)
        time.sleep(12)

    (BASE / "deck-audio-manifest.json").write_text(
        json.dumps(status, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(status, ensure_ascii=False, indent=2))
    return 0 if any(item["status"] == "done" for item in status) else 1


if __name__ == "__main__":
    raise SystemExit(main())
