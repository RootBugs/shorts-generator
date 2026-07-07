import subprocess
import os
import json
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')
from config import YTDLP_PATH, TEMP_DIR


def download_video(url: str, output_dir: str = None) -> str | None:
    """Download video and return file path."""
    output_dir = output_dir or TEMP_DIR
    os.makedirs(output_dir, exist_ok=True)

    output_template = os.path.join(output_dir, "%(id)s.%(ext)s")
    cmd = [
        YTDLP_PATH,
        "--no-playlist",
        "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "--merge-output-format", "mp4",
        "-o", output_template,
        "--write-info-json",
        url,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    if result.returncode != 0:
        print(f"Download failed: {result.stderr[-300:]}")
        return None

    for f in os.listdir(output_dir):
        if f.endswith(".mp4") and os.path.getsize(os.path.join(output_dir, f)) > 100000:
            return os.path.join(output_dir, f)
    return None


def get_transcript_with_timestamps(video_url: str) -> list[dict]:
    """Get word-level transcript with timestamps using yt-dlp + whisper-like subs."""
    import tempfile

    # Try to get auto-generated subtitles
    tmp = os.path.join(tempfile.gettempdir(), "yt_words")
    cmd = [
        YTDLP_PATH,
        "--write-auto-sub",
        "--sub-lang", "en",
        "--skip-download",
        "--sub-format", "json3",
        "-o", tmp,
        video_url
    ]
    subprocess.run(cmd, capture_output=True, text=True, timeout=60)

    # Parse json3 subtitle format
    for f in os.listdir(tempfile.gettempdir()):
        if f.startswith("yt_words") and f.endswith(".json3"):
            filepath = os.path.join(tempfile.gettempdir(), f)
            with open(filepath, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            os.remove(filepath)
            return parse_json3_subtitles(data)

    # Fallback: get VTT and parse
    return get_vtt_transcript(video_url)


def parse_json3_subtitles(data: dict) -> list[dict]:
    """Parse json3 subtitle format to word-level timestamps."""
    words = []
    for event in data.get("events", []):
        segs = event.get("segs", [])
        for seg in segs:
            if seg.get("utf8", "").strip():
                start = event.get("tStartMs", 0) / 1000
                dur = event.get("dDurationMs", 0) / 1000
                words.append({
                    "word": seg["utf8"].strip(),
                    "start": round(start, 2),
                    "end": round(start + dur, 2),
                })
    return words


def get_vtt_transcript(video_url: str) -> list[dict]:
    """Fallback: parse VTT subtitles."""
    import tempfile
    tmp = os.path.join(tempfile.gettempdir(), "yt_vtt")
    cmd = [
        YTDLP_PATH,
        "--write-auto-sub",
        "--sub-lang", "en",
        "--skip-download",
        "--sub-format", "vtt",
        "-o", tmp,
        video_url
    ]
    subprocess.run(cmd, capture_output=True, text=True, timeout=60)

    words = []
    for f in os.listdir(tempfile.gettempdir()):
        if f.startswith("yt_vtt") and f.endswith(".vtt"):
            filepath = os.path.join(tempfile.gettempdir(), f)
            with open(filepath, "r", encoding="utf-8") as fh:
                content = fh.read()
            os.remove(filepath)
            words = parse_vtt(content)
            break
    return words


def parse_vtt(content: str) -> list[dict]:
    """Parse VTT subtitle to word timestamps."""
    words = []
    lines = content.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if "-->" in line:
            match = re.match(r"(\d{2}):(\d{2}):(\d{2})\.(\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2})\.(\d{3})", line)
            if match:
                g = match.groups()
                start = int(g[0])*3600 + int(g[1])*60 + int(g[2]) + int(g[3])/1000
                end = int(g[4])*3600 + int(g[5])*60 + int(g[6]) + int(g[7])/1000
                i += 1
                text_lines = []
                while i < len(lines) and lines[i].strip() and "-->" not in lines[i]:
                    text_lines.append(lines[i].strip())
                    i += 1
                text = " ".join(text_lines)
                text = re.sub(r"<[^>]+>", "", text)  # strip HTML tags
                if text.strip():
                    words.append({
                        "word": text.strip(),
                        "start": round(start, 2),
                        "end": round(end, 2),
                    })
                    continue
        i += 1
    return words


def words_to_segments(words: list[dict], max_gap: float = 1.5) -> list[dict]:
    """Group words into sentence-level segments."""
    if not words:
        return []

    segments = []
    current = {
        "text": words[0]["word"],
        "start": words[0]["start"],
        "end": words[0]["end"],
        "words": [words[0]]
    }

    for w in words[1:]:
        gap = w["start"] - current["end"]
        if gap > max_gap or len(current["text"]) > 200:
            segments.append(current)
            current = {
                "text": w["word"],
                "start": w["start"],
                "end": w["end"],
                "words": [w]
            }
        else:
            current["text"] += " " + w["word"]
            current["end"] = w["end"]
            current["words"].append(w)

    segments.append(current)
    return segments


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python transcript.py <youtube_url>")
        sys.exit(1)

    words = get_transcript_with_timestamps(sys.argv[1])
    print(f"Found {len(words)} words")
    segments = words_to_segments(words)
    print(f"Grouped into {len(segments)} segments\n")
    for s in segments[:10]:
        print(f"[{s['start']:.1f}s - {s['end']:.1f}s] {s['text'][:80]}")
