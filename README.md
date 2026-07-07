# 🎬 Shorts Generator

Auto-cut any YouTube video into vertical Shorts.

```bash
python auto_shorts.py "https://youtube.com/watch?v=VIDEO_ID"
```

## What It Does

```
Long Video → Transcript → Find Best Moments → Cut → 1080x1920 Shorts
```

## Install

```bash
git clone https://github.com/RootBugs/shorts-generator.git
cd shorts-generator
pip install -r requirements.txt
winget install ffmpeg
```

## Usage

```bash
# Basic
python auto_shorts.py "URL"

# More shorts
python auto_shorts.py "URL" --clips 8

# Faster (no AI)
python auto_shorts.py "URL" --no-chatgpt

# Local file
python auto_shorts.py "video.mp4"

# Menu
python main.py
```

## Config

```python
# config.py
NUM_CLIPS = 5
MIN_CLIP_DURATION = 15
MAX_CLIP_DURATION = 58
SHORTS_WIDTH = 1080
SHORTS_HEIGHT = 1920
```

## Dependencies

- Python 3.10+
- yt-dlp
- moviepy
- ffmpeg

Optional: Node.js + Puppeteer (for ChatGPT smart cuts)

## How It Works

1. **Download** - yt-dlp grabs the video
2. **Transcript** - Extracts words with timestamps
3. **Analysis** - Finds funny/best moments (AI or keyword scoring)
4. **Cut** - MoviePy cuts clips at exact timestamps
5. **Convert** - Resizes to 1080x1920 vertical format

## License

MIT
