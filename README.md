<div align="center">

# 🎬 Shorts Generator

### Auto-cut any video into YouTube Shorts using AI

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![yt-dlp](https://img.shields.io/badge/yt--dlp-latest-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://github.com/yt-dlp/yt-dlp)
[![moviepy](https://img.shields.io/badge/moviepy-2.x-00BFFF?style=for-the-badge&logo=ffmpeg&logoColor=white)](https://moviepy.readthedocs.io)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

**Works with ANY YouTube video • No API keys • 1080x1920 vertical output**

</div>

---

## 📸 How It Works

![Process Diagram](assets/screenshots/process.png)

```
Input Video → Transcript → AI Analysis → Cut Shorts → Output
```

---

## 🔄 Before & After

![Before vs After](assets/screenshots/before_after.png)

| Input | Output |
|:-----:|:------:|
| ![Input](assets/input/sample_input.jpg) | ![Output](assets/output/sample_output.jpg) |
| **8 min landscape video** | **5 × 30 sec vertical shorts** |

---

## 📸 Screenshots

### Terminal Output

![Terminal](assets/screenshots/terminal.png)

### Generated Shorts

| # | Preview | Duration | Size |
|---|---------|----------|------|
| 1 | 🎬 | 40s | 12.5 MB |
| 2 | 🎬 | 50s | 16.8 MB |
| 3 | 🎬 | 50s | 11.4 MB |
| 4 | 🎬 | 50s | 14.9 MB |

---

## ⚡ Quick Start

```bash
# 1. Clone
git clone https://github.com/RootBugs/shorts-generator.git
cd shorts-generator

# 2. Install
pip install -r requirements.txt

# 3. Run
python auto_shorts.py "https://www.youtube.com/watch?v=ANY_VIDEO_ID"
```

---

## 📦 Dependencies

### Required

| Package | Purpose | Install |
|---------|---------|---------|
| **Python 3.10+** | Runtime | [python.org](https://python.org) |
| **yt-dlp** | Download videos | `pip install yt-dlp` |
| **moviepy** | Edit videos | `pip install moviepy` |
| **Pillow** | Image processing | `pip install Pillow` |
| **numpy** | Numerical ops | `pip install numpy` |
| **ffmpeg** | Video encoding | `winget install ffmpeg` |

### Optional (better AI cuts)

| Package | Purpose | Install |
|---------|---------|---------|
| **Node.js 18+** | ChatGPT integration | [nodejs.org](https://nodejs.org) |
| **Puppeteer** | Browser automation | `npm install puppeteer` |

### requirements.txt

```
moviepy>=2.0
yt-dlp>=2024.1.0
numpy>=1.25.0
Pillow>=9.2.0
imageio>=2.5.0
imageio-ffmpeg>=0.2.0
```

---

## 🛠️ Commands

```bash
# Basic - generate shorts from URL
python auto_shorts.py "https://www.youtube.com/watch?v=VIDEO_ID"

# Generate more shorts
python auto_shorts.py "URL" --clips 8

# Skip ChatGPT (faster)
python auto_shorts.py "URL" --no-chatgpt

# Local video file
python auto_shorts.py "C:\path\to\video.mp4"

# Interactive menu
python main.py
```

---

## ⚙️ Config

Edit `config.py`:

```python
NUM_CLIPS = 5           # Shorts per video
MIN_CLIP_DURATION = 15  # Min seconds
MAX_CLIP_DURATION = 58  # Max (under 60 for shorts)
SHORTS_WIDTH = 1080     # Vertical width
SHORTS_HEIGHT = 1920    # Vertical height
```

---

## 📁 Structure

```
shorts-generator/
├── auto_shorts.py      # Main pipeline
├── transcript.py       # Transcript extraction
├── cutter.py           # Video cutting
├── chatgpt.js          # AI analysis
├── config.py           # Settings
├── main.py             # Menu
├── requirements.txt    # Dependencies
├── assets/             # Screenshots & demos
│   ├── input/          # Input examples
│   ├── output/         # Output examples
│   └── screenshots/    # Process screenshots
├── output/             # Generated shorts
└── temp/               # Temp files
```

---

## 🐛 Troubleshooting

| Error | Fix |
|-------|-----|
| `No transcript` | Video needs subtitles enabled |
| `ffmpeg not found` | `winget install ffmpeg` |
| `Permission denied` | Close video players, run as admin |
| `Slow processing` | Use `--no-chatgpt` |

---

## 📊 Performance

| Video Length | Shorts | Time |
|--------------|--------|------|
| 5 min | 3 | ~5 min |
| 10 min | 5 | ~12 min |
| 20 min | 8 | ~25 min |

---

## 📝 License

MIT - use freely.

<div align="center">

**Made with ❤️ by [RootBugs](https://github.com/RootBugs)**

</div>
