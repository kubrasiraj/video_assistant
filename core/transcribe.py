import whisper
import os
import requests
import subprocess

os.environ["PATH"] += os.pathsep + r"C:\ffmpeg\bin"

# ---------------- CONFIG ----------------
SARVAM_PIECE_SECONDS = 25
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "small")

SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")
SARVAM_STT_TRANSLATE_URL = "https://api.sarvam.ai/speech-to-text-translate"
SARVAM_MODEL = os.getenv("SARVAM_STT_MODEL", "saaras:v2.5")

_model = None


# ---------------- WHISPER LOAD ----------------
def load_model():
    global _model
    if _model is None:
        print(f"Loading Whisper model: {WHISPER_MODEL}")
        _model = whisper.load_model(WHISPER_MODEL)
    return _model


# ---------------- WHISPER ----------------
def transcribe_chunk_whisper(chunk_path: str) -> str:
    model = load_model()
    result = model.transcribe(chunk_path)
    return result["text"]


# ---------------- SARVAM API ----------------
def _send_to_sarvam(piece_path: str) -> str:
    headers = {"api-subscription-key": SARVAM_API_KEY}

    with open(piece_path, "rb") as f:
        files = {"file": (os.path.basename(piece_path), f, "audio/wav")}
        data = {
            "model": SARVAM_MODEL,
            "with_diarization": "false"
        }

        response = requests.post(
            SARVAM_STT_TRANSLATE_URL,
            headers=headers,
            files=files,
            data=data,
            timeout=120,
        )

    response.raise_for_status()
    return response.json().get("transcript", "")


# ---------------- CHUNK AUDIO (FFMPEG ONLY) ----------------
def chunk_audio(wav_path: str, chunk_seconds: int = 25):
    output_dir = os.path.dirname(wav_path)
    base = os.path.splitext(os.path.basename(wav_path))[0]

    output_pattern = os.path.join(output_dir, f"{base}_chunk_%03d.wav")

    subprocess.run([
        r"C:\ffmpeg\bin\ffmpeg.exe",
        "-y",
        "-i", wav_path,
        "-f", "segment",
        "-segment_time", str(chunk_seconds),
        "-ar", "16000",
        "-ac", "1",
        "-c:a", "pcm_s16le",
        output_pattern
    ], check=True)

    return sorted([
        os.path.join(output_dir, f)
        for f in os.listdir(output_dir)
        if f.startswith(base + "_chunk") and f.endswith(".wav")
    ])


# ---------------- ROUTER ----------------
def transcribe_chunk(chunk_path: str, language: str = "english") -> str:
    if language.lower() == "hinglish":
        return transcribe_chunk_sarvam(chunk_path)
    return transcribe_chunk_whisper(chunk_path)


# ---------------- SARVAM CHUNK PROCESS ----------------
def transcribe_chunk_sarvam(chunk_path: str) -> str:
    if not SARVAM_API_KEY:
        raise RuntimeError("SARVAM_API_KEY missing")

    audio = subprocess.Popen  # placeholder safety (no pydub needed)

    # NOTE: simplified approach → assume chunk already ≤25s
    return _send_to_sarvam(chunk_path)


# ---------------- FULL PIPELINE ----------------
def transcribe_all(chunks: list, language: str = "english") -> str:
    full_text = ""

    engine = "Sarvam" if language == "hinglish" else "Whisper"
    print(f"Using {engine}")

    for i, chunk in enumerate(chunks):
        print(f"Chunk {i+1}/{len(chunks)}")
        text = transcribe_chunk(chunk, language)
        full_text += text + " "

    return full_text.strip()