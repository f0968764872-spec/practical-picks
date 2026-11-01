import os
import asyncio
import subprocess
from datetime import datetime

async def _synthesize_voice(text, voice, rate, output_mp3, output_srt):
    import edge_tts
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    submaker = edge_tts.SubMaker()
    with open(output_mp3, "wb") as file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                submaker.create_sub((chunk["offset"], chunk["duration"]), chunk["text"])
    with open(output_srt, "w", encoding="utf-8") as file:
        file.write(submaker.generate_subs())


def build_daily_shorts(posts, config, output_dir="output_shorts"):
    """
    將每日第一篇精選情報自動轉換為美式真人感英語短影音 (YouTube Shorts / TikTok US)。
    預設使用微軟自然美式男聲 en-US-AndrewNeural。
    """
    os.makedirs(output_dir, exist_ok=True)
    if not posts:
        return

    top_post = posts[0]
    script_text = top_post.get("shorts_script", "")
    date_tag = datetime.now().strftime("%Y%m%d_%H%M")

    script_path = os.path.join(output_dir, f"us_short_{date_tag}_script.txt")
    mp3_path = os.path.join(output_dir, f"us_short_{date_tag}_audio.mp3")
    srt_path = os.path.join(output_dir, f"us_short_{date_tag}_subs.srt")
    mp4_path = os.path.join(output_dir, f"us_short_{date_tag}_video.mp4")

    with open(script_path, "w", encoding="utf-8") as f:
        f.write(f"[Title]\n{top_post.get('title', '')}\n\n")
        f.write(f"[30s Casual US Voiceover Script]\n{script_text}\n\n")
        f.write(f"[Pinned Comment / Reddit / X Post]\n{top_post.get('telegram_text', '')}\n")

    voice = config.get("voice_settings", {}).get("voice", "en-US-AndrewNeural")
    rate = config.get("voice_settings", {}).get("rate", "+5%")

    try:
        asyncio.run(_synthesize_voice(script_text, voice, rate, mp3_path, srt_path))
    except Exception:
        return

    try:
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi", "-i", "color=c=#1c1917:s=1080x1920:r=30",
            "-i", mp3_path,
            "-shortest",
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k",
            mp4_path
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    except Exception:
        pass
