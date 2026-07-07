# Shorts Generator

Auto-generate YouTube Shorts from long comedy/cartoon videos using transcript analysis.

## How It Works

```
Long Video → Transcript → Find Funny Moments → Cut Shorts → 1080x1920 Vertical
```

## Quick Start

```bash
# Install dependencies
pip install moviepy yt-dlp

# Generate shorts from YouTube URL
python auto_shorts.py "https://www.youtube.com/watch?v=VIDEO_ID"

# Generate from local video
python auto_shorts.py "C:\path\to\video.mp4"
```

## Features

- **Transcript Analysis** - Finds funniest moments using word timestamps
- **ChatGPT Integration** - Smart clip selection with AI (optional)
- **Auto Captions** - Adds word-by-word captions from transcript
- **Vertical Format** - Auto-converts to 1080x1920 for YouTube Shorts
- **Scene Detection** - Works even without transcript (cartoons)

## Commands

| Command | Description |
|---------|-------------|
| `python auto_shorts.py URL` | Generate shorts from URL |
| `python auto_shorts.py URL --clips 8` | Generate 8 shorts |
| `python auto_shorts.py URL --no-chatgpt` | Skip ChatGPT (faster) |
| `python main.py` | Interactive menu |

## Config

Edit `config.py`:
```python
NUM_CLIPS = 5           # Shorts per video
MIN_CLIP_DURATION = 15  # Min seconds
MAX_CLIP_DURATION = 58  # Max seconds (under 60 for shorts)
SHORTS_WIDTH = 1080     # Vertical width
SHORTS_HEIGHT = 1920    # Vertical height
```

## Output

Shorts saved to `output/` folder, ready to upload as YouTube Shorts.

## Time

| Step | Time |
|------|------|
| Download | 30-60s |
| Transcript | 10s |
| Analysis | 15s |
| Cut per short | 2-3 min |
| **Total (5 shorts)** | **~12-15 min** |

## Requirements

- Python 3.10+
- yt-dlp
- moviepy
- ffmpeg (comes with moviepy)

## License

MIT
