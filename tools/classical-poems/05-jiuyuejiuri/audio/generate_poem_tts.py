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

TEXT = (
    "請用台灣國語，語速稍慢，聲音自然有感情，適合國小低年級學生。"
    "請只朗讀下面內容，不要朗讀任何說明文字。"
    "九月九日憶山東兄弟。唐，王維。"
    "獨在異鄉為異客。每逢佳節倍思親。"
    "遙知兄弟登高處。遍插茱萸少一人。"
)

SEGMENTS = [
    {
        "id": "poem-sadaltager",
        "voice": "Sadaltager",
        "file": "poem-sadaltager.wav",
        "text": TEXT,
    },
    {
        "id": "poem-sulafat",
        "voice": "Sulafat",
        "file": "poem-sulafat.wav",
        "text": TEXT,
    },
]


def write_wav(path: Path, pcm: bytes) -> None:
    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(24000)
        wf.writeframes(pcm)


def request_audio(segment: dict) -> bytes:
    body = {
        "contents": [{"parts": [{"text": segment["text"]}]}],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {
                "voiceConfig": {
                    "prebuiltVoiceConfig": {"voiceName": segment["voice"]}
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
    for segment in SEGMENTS:
        item = {
            "id": segment["id"],
            "voice": segment["voice"],
            "file": segment["file"],
            "status": "pending",
            "error": "",
            "model": MODEL,
        }
        try:
            pcm = request_audio(segment)
            out = BASE / segment["file"]
            write_wav(out, pcm)
            if out.stat().st_size < 1024:
                raise RuntimeError(f"invalid tiny wav: {out.stat().st_size} bytes")
            item["status"] = "done"
            item["bytes"] = out.stat().st_size
        except urllib.error.HTTPError as exc:
            item["status"] = "failed"
            item["error"] = f"HTTP {exc.code}: {exc.read().decode('utf-8', errors='ignore')[:500]}"
        except Exception as exc:
            item["status"] = "failed"
            item["error"] = str(exc)
        status.append(item)
        time.sleep(1.5)

    (BASE / "poem-tts-status.json").write_text(
        json.dumps(status, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(status, ensure_ascii=False, indent=2))
    return 0 if any(item["status"] == "done" for item in status) else 1


if __name__ == "__main__":
    raise SystemExit(main())
