
import os
import yt_dlp
import subprocess


# ----------------------------
# 1. DOWNLOAD FROM YOUTUBE
# ----------------------------
def download_youtube_audio(youtube_url, output_dir="storage/uploads"):
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio/best',
        'ffmpeg_location': r'C:\ffmpeg\bin',  # change if needed
        'outtmpl': os.path.join(output_dir, '%(id)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=True)

        # SAFE file path
        file_path = os.path.join(output_dir, f"{info['id']}.mp3")

        return file_path


# ----------------------------
# 2. CONVERT TO WAV (NO PYDUB)
# ----------------------------
def convert_to_wav(input_path: str) -> str:
    output_path = os.path.splitext(input_path)[0] + ".wav"

    subprocess.run([
        r"C:\ffmpeg\bin\ffmpeg.exe",  # MUST be correct path
        "-y",
        "-i", input_path,
        "-ar", "16000",
        "-ac", "1",
        output_path
    ], check=True)

    return output_path


# ----------------------------
# 3. CHUNK AUDIO (NO PYDUB? NO PROBLEM)
# ----------------------------
import subprocess
import os


def chunk_audio(wav_path: str, chunk_minutes: int = 10) -> list:
    output_dir = os.path.dirname(wav_path)
    base_name = os.path.splitext(os.path.basename(wav_path))[0]

    chunk_pattern = os.path.join(output_dir, f"{base_name}_chunk_%03d.wav")

    subprocess.run([
        r"C:\ffmpeg\bin\ffmpeg.exe",
        "-i", wav_path,
        "-f", "segment",
        "-segment_time", str(chunk_minutes * 60),
        "-c", "copy",
        chunk_pattern
    ], check=True)

    # collect chunks
    chunks = sorted([
        os.path.join(output_dir, f)
        for f in os.listdir(output_dir)
        if f.startswith(base_name + "_chunk")
    ])

    return chunks


# ----------------------------
# 4. MAIN PIPELINE
# ----------------------------
def process_input(source: str) -> list:
    if source.startswith("http"):
        print("Downloading YouTube audio...")
        wav_path = download_youtube_audio(source)
        wav_path = convert_to_wav(wav_path)
    else:
        print("Local file detected...")
        wav_path = convert_to_wav(source)

    print("Chunking audio...")
    chunks = chunk_audio(wav_path)

    print(f"Done! {len(chunks)} chunks created.")
    return chunks

"""
# ----------------------------
# RUN TEST
# ----------------------------
if __name__ == "__main__":
    data = process_input("https://www.youtube.com/watch?v=J8DzuMmSDEU")
    print(data)"""