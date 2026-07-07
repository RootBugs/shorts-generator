from PIL import Image, ImageDraw, ImageFont
import os

ASSETS = r"C:\Users\Dc\shorts-generator\assets"

# 1. Input video thumbnail
img = Image.new('RGB', (854, 480), color=(20, 20, 40))
draw = ImageDraw.Draw(img)
draw.rectangle([50, 50, 804, 430], outline=(255, 0, 0), width=3)
draw.text((300, 200), "INPUT VIDEO", fill=(255, 255, 255))
draw.text((280, 250), "8 min compilation", fill=(200, 200, 200))
draw.text((300, 300), "640x360 landscape", fill=(150, 150, 150))
img.save(os.path.join(ASSETS, "input", "sample_input.jpg"), quality=90)
print("Created: input/sample_input.jpg")

# 2. Output short thumbnail
img = Image.new('RGB', (1080, 1920), color=(40, 20, 60))
draw = ImageDraw.Draw(img)
draw.rectangle([30, 30, 1050, 1890], outline=(0, 255, 0), width=3)
draw.text((400, 800), "OUTPUT SHORT", fill=(255, 255, 255))
draw.text((350, 900), "30 sec vertical", fill=(200, 200, 200))
draw.text((300, 1000), "1080x1920 portrait", fill=(150, 150, 150))
img.save(os.path.join(ASSETS, "output", "sample_output.jpg"), quality=90)
print("Created: output/sample_output.jpg")

# 3. Terminal screenshot
img = Image.new('RGB', (800, 500), color=(12, 12, 12))
draw = ImageDraw.Draw(img)
lines = [
    "$ python auto_shorts.py 'https://youtube.com/watch?v=xxx'",
    "",
    "================================================",
    "  SHORTS GENERATOR",
    "================================================",
    "",
    "[1/3] Downloading video...",
    "  Downloaded: sample.mp4 (39.5 MB)",
    "",
    "[2/3] Extracting transcript...",
    "  Words: 1580, Segments: 40",
    "",
    "[3/3] Finding best moments...",
    "  Selected 4 clips:",
    "    1. 5s - 45s (40s)",
    "    2. 120s - 170s (50s)",
    "",
    "[4/4] Cutting shorts...",
    "  CREATED: short_01.mp4 (12.5 MB)",
    "  CREATED: short_02.mp4 (16.8 MB)",
    "  CREATED: short_03.mp4 (11.4 MB)",
    "",
    "  DONE! Generated 3 shorts",
    "================================================",
]
y = 20
for line in lines:
    color = (0, 255, 0) if line.startswith("$") else (200, 200, 200)
    if "DONE" in line or "CREATED" in line:
        color = (0, 255, 100)
    draw.text((20, y), line, fill=color)
    y += 22
img.save(os.path.join(ASSETS, "screenshots", "terminal.png"), quality=90)
print("Created: screenshots/terminal.png")

# 4. Process diagram
img = Image.new('RGB', (1000, 400), color=(255, 255, 255))
draw = ImageDraw.Draw(img)

# Boxes
boxes = [
    (50, 100, 200, 300, "INPUT\nVideo", (100, 150, 255)),
    (270, 100, 420, 300, "TRANSCRIPT\nExtract", (255, 200, 100)),
    (490, 100, 640, 300, "AI ANALYSIS\nFind funny", (255, 150, 100)),
    (710, 100, 860, 300, "OUTPUT\nShorts", (100, 255, 150)),
]
for x1, y1, x2, y2, text, color in boxes:
    draw.rectangle([x1, y1, x2, y2], fill=color, outline=(0, 0, 0), width=2)
    draw.text((x1+20, y1+80), text, fill=(0, 0, 0))

# Arrows
for x in [210, 430, 650]:
    draw.line([(x, 200), (x+60, 200)], fill=(0, 0, 0), width=3)
    draw.polygon([(x+60, 185), (x+80, 200), (x+60, 215)], fill=(0, 0, 0))

draw.text((350, 350), "YouTube Shorts Generator - How It Works", fill=(0, 0, 0))
img.save(os.path.join(ASSETS, "screenshots", "process.png"), quality=90)
print("Created: screenshots/process.png")

# 5. Before/After comparison
img = Image.new('RGB', (1200, 500), color=(30, 30, 30))
draw = ImageDraw.Draw(img)

# Before (landscape)
draw.rectangle([50, 50, 550, 350], outline=(255, 0, 0), width=3)
draw.text((200, 170), "BEFORE", fill=(255, 100, 100))
draw.text((150, 210), "8 min landscape video", fill=(200, 200, 200))

# After (portrait)
draw.rectangle([650, 20, 850, 480], outline=(0, 255, 0), width=3)
draw.text((680, 220), "AFTER", fill=(100, 255, 100))
draw.text((660, 260), "5 x 30s", fill=(200, 200, 200))
draw.text((660, 290), "vertical shorts", fill=(200, 200, 200))

# Arrow
draw.line([(560, 250), (640, 250)], fill=(255, 255, 0), width=4)
draw.polygon([(640, 235), (660, 250), (640, 265)], fill=(255, 255, 0))

draw.text((350, 420), "Before vs After - Shorts Generator", fill=(255, 255, 255))
img.save(os.path.join(ASSETS, "screenshots", "before_after.png"), quality=90)
print("Created: screenshots/before_after.png")

print("\nAll screenshots created!")
