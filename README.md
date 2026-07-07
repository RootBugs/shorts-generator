<div align="center">

# 🎬 Shorts Generator

### Auto-cut comedy & cartoon clips from long videos into YouTube Shorts

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![yt-dlp](https://img.shields.io/badge/yt--dlp-latest-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://github.com/yt-dlp/yt-dlp)
[![moviepy](https://img.shields.io/badge/moviepy-2.x-00BFFF?style=for-the-badge&logo=ffmpeg&logoColor=white)](https://moviepy.readthedocs.io)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

**No API keys required • Works with any YouTube video • 1080x1920 vertical output**

</div>

---

## 📸 How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                     INPUT: Long Video                           │
│         (Tom & Jerry, Mr Bean, Comedy Compilations)             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 1: Download Video                                         │
│  ─────────────────────                                          │
│  • Uses yt-dlp to download from YouTube                         │
│  • Supports any public video                                    │
│  • Auto-selects best quality                                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 2: Extract Transcript                                     │
│  ────────────────────────                                       │
│  • Gets word-level timestamps                                   │
│  • Groups words into sentences                                  │
│  • Works with auto-generated subtitles                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 3: Find Funniest Moments                                  │
│  ────────────────────────────                                   │
│  • ChatGPT analyzes transcript for jokes                        │
│  • Identifies setup → punchline sequences                       │
│  • Selects clips with complete funny moments                    │
│  • Fallback: keyword scoring if ChatGPT unavailable             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 4: Cut & Convert                                          │
│  ────────────────────                                           │
│  • Cuts video at exact timestamps                               │
│  • Converts to 1080x1920 vertical (9:16)                        │
│  • Maintains audio quality                                      │
│  • Adds auto-captions from transcript                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     OUTPUT: Ready Shorts                        │
│              (Upload directly to YouTube Shorts)                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎥 Demo

### Example: Tom & Jerry → 5 Shorts

| Input | Output |
|-------|--------|
| ![Tom & Jerry Full](https://via.placeholder.com/400x225/1a1a2e/e94560?text=Tom+%26+Jerry+17+min) | ![Short 1](https://via.placeholder.com/180x320/16213e/0f3460?text=Short+1+30s) |
| **8 min compilation** | **5 × 30-50 sec shorts** |

### Generated Shorts

| # | Clip | Duration | Size |
|---|------|----------|------|
| 1 | `tomjerry_opening_chase.mp4` | 40s | 12.5 MB |
| 2 | `tomjerry_jerry_prank.mp4` | 50s | 16.8 MB |
| 3 | `tomjerry_tom_fall.mp4` | 50s | 11.4 MB |
| 4 | `tomjerry_cheese_trap.mp4` | 50s | 14.9 MB |
| 5 | `tomjerry_dog_chase.mp4` | 50s | 7.6 MB |

---

## ⚡ Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/RootBugs/shorts-generator.git
cd shorts-generator
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run

```bash
# Interactive menu
python main.py

# Or direct command
python auto_shorts.py "https://www.youtube.com/watch?v=Or-XHvRZFq0"
```

### 4. Find your shorts

```
output/
├── tomjerry_short_01.mp4   ← Ready to upload!
├── tomjerry_short_02.mp4
├── tomjerry_short_03.mp4
└── ...
```

---

## 📦 Dependencies

### Required

| Package | Version | Purpose | Install |
|---------|---------|---------|---------|
| **Python** | 3.10+ | Runtime | [python.org](https://python.org) |
| **yt-dlp** | latest | Video downloading | `pip install yt-dlp` |
| **moviepy** | 2.x | Video editing | `pip install moviepy` |
| **ffmpeg** | any | Video encoding | `winget install ffmpeg` |

### Optional (for better results)

| Package | Version | Purpose | Install |
|---------|---------|---------|---------|
| **Node.js** | 18+ | ChatGPT integration | [nodejs.org](https://nodejs.org) |
| **Puppeteer** | latest | Browser automation | `npm install puppeteer` |

### Full requirements.txt

```
moviepy>=2.0
yt-dlp>=2024.1.0
numpy>=1.25.0
Pillow>=9.2.0
imageio>=2.5.0
imageio-ffmpeg>=0.2.0
```

---

## 🛠️ All Commands

```bash
# Basic usage - generate shorts from YouTube URL
python auto_shorts.py "https://www.youtube.com/watch?v=VIDEO_ID"

# Generate 8 shorts instead of default 5
python auto_shorts.py "URL" --clips 8

# Skip ChatGPT (faster, uses local analysis)
python auto_shorts.py "URL" --no-chatgpt

# Use local video file
python auto_shorts.py "C:\path\to\video.mp4"

# Interactive menu with all options
python main.py

# Preview transcript before cutting
python main.py  # Select option 3

# Quick test with sample video
python main.py  # Select option 4
```

---

## ⚙️ Configuration

Edit `config.py` to customize:

```python
# Number of shorts to generate per video
NUM_CLIPS = 5

# Clip duration limits (seconds)
MIN_CLIP_DURATION = 15
MAX_CLIP_DURATION = 58  # Under 60 for YouTube Shorts

# Output format (vertical 9:16)
SHORTS_WIDTH = 1080
SHORTS_HEIGHT = 1920
SHORTS_FPS = 30

# Caption settings
CAPTION_FONT = "Arial"
CAPTION_FONTSIZE = 42
CAPTION_COLOR = "white"
```

---

## 📁 Project Structure

```
shorts-generator/
│
├── auto_shorts.py      # Main pipeline - orchestrates everything
├── transcript.py       # Extracts transcript with timestamps
├── cutter.py           # Cuts clips and converts to vertical
├── chatgpt.js          # ChatGPT integration for smart cuts
├── config.py           # All settings in one place
├── main.py             # Interactive menu
├── setup.py            # Check if everything is installed
│
├── input/              # Drop local videos here
├── output/             # Generated shorts appear here
├── temp/               # Temporary files (auto-cleaned)
├── generated/          # Metadata JSON files
│
├── requirements.txt    # Python dependencies
├── README.md           # This file
└── .gitignore          # Ignores temp/output/cache
```

---

## 🎯 What Makes This Different?

| Feature | This Tool | Manual Editing |
|---------|-----------|----------------|
| **Speed** | 5 shorts in ~12 min | 1-2 hours manual |
| **Smart Cuts** | AI analyzes transcript | You watch entire video |
| **Format** | Auto 1080x1920 | Manual resize |
| **Captions** | Auto word-by-word | Type manually |
| **Batch** | Unlimited videos | One at a time |

---

## 🐛 Troubleshooting

### "No transcript found"
- Video might not have subtitles
- Try a different video with auto-captions enabled
- Use `--no-chatgpt` for local analysis

### "ffmpeg not found"
```bash
# Windows
winget install ffmpeg

# Mac
brew install ffmpeg

# Linux
sudo apt install ffmpeg
```

### "Permission denied" on output
- Close any video players using the files
- Run terminal as administrator
- Check antivirus isn't blocking

### Slow processing
- Use `--no-chatgpt` to skip AI analysis
- Reduce `NUM_CLIPS` in config.py
- Use lower quality source video

---

## 📊 Performance

| Video Length | Shorts Generated | Processing Time |
|--------------|------------------|-----------------|
| 5 min | 3 | ~5 min |
| 10 min | 5 | ~12 min |
| 20 min | 8 | ~25 min |
| 60 min | 15 | ~60 min |

---

## 🤝 Contributing

1. Fork the repo
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push (`git push origin feature/amazing`)
5. Open Pull Request

---

## 📝 License

MIT License - use freely, modify freely.

---

## ⭐ Star History

If this helped you, give it a star!

<div align="center">

**Made with ❤️ by [RootBugs](https://github.com/RootBugs)**

</div>
