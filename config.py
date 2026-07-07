import os

# Video settings
YTDLP_PATH = "yt-dlp"
INPUT_DIR = os.path.join(os.path.dirname(__file__), "input")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
TEMP_DIR = os.path.join(os.path.dirname(__file__), "temp")

# Shorts format (vertical 9:16)
SHORTS_WIDTH = 1080
SHORTS_HEIGHT = 1920
SHORTS_FPS = 30

# Clip settings
MIN_CLIP_DURATION = 15  # seconds
MAX_CLIP_DURATION = 58  # seconds (under 60 for shorts)
NUM_CLIPS = 5  # clips to generate per video

# Caption settings
CAPTION_FONT = "Arial"
CAPTION_FONTSIZE = 42
CAPTION_COLOR = "white"
CAPTION_BG_COLOR = "black@0.7"
CAPTION_POSITION = "bottom"  # bottom, center, top

# ChatGPT
CHATGPT_COOKIES = os.path.join(os.path.dirname(__file__), "chatgpt_cookies.json")

# Create dirs
for d in [INPUT_DIR, OUTPUT_DIR, TEMP_DIR]:
    os.makedirs(d, exist_ok=True)
