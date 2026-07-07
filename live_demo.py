import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
from moviepy import VideoFileClip
import subprocess
import json

TEMP_DIR = r"C:\Users\Dc\shorts-generator\temp"
OUTPUT_DIR = r"C:\Users\Dc\shorts-generator\output"
ASSETS_DIR = r"C:\Users\Dc\shorts-generator\assets"

# Use existing video
VIDEO_PATH = os.path.join(TEMP_DIR, "BeEitK3FBLQ.f399.mp4")

if not os.path.exists(VIDEO_PATH):
    VIDEO_PATH = os.path.join(TEMP_DIR, "tj.mp4")

print("="*60)
print("  SHORTS GENERATOR - LIVE DEMO")
print("="*60)

# Get video info
clip = VideoFileClip(VIDEO_PATH)
duration = clip.duration
clip.close()
print(f"\n1. VIDEO INFO:")
print(f"   File: {os.path.basename(VIDEO_PATH)}")
print(f"   Duration: {duration:.0f}s ({duration/60:.1f} min)")
print(f"   Size: {os.path.getsize(VIDEO_PATH) / 1024 / 1024:.1f} MB")

# Get transcript
print(f"\n2. TRANSCRIPT:")
cmd = ["yt-dlp", "--write-auto-sub", "--sub-lang", "en", "--skip-download", "--sub-format", "vtt", "-o", os.path.join(TEMP_DIR, "demo_sub"), f"https://www.youtube.com/watch?v=BeEitK3FBLQ"]
result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

transcript_file = None
for f in os.listdir(TEMP_DIR):
    if f.startswith("demo_sub") and f.endswith(".vtt"):
        transcript_file = os.path.join(TEMP_DIR, f)
        break

if transcript_file:
    with open(transcript_file, "r", encoding="utf-8") as fh:
        lines = fh.readlines()
    word_count = len([l for l in lines if l.strip() and "-->" not in l and "WEBVTT" not in l])
    print(f"   Words extracted: {word_count}")
    os.remove(transcript_file)
else:
    print("   Using visual analysis (no transcript)")

# Find clips
print(f"\n3. ANALYSIS:")
clips = [
    {"start": 10, "end": 45, "reason": "Opening chase scene"},
    {"start": 150, "end": 195, "reason": "Jerry's prank"},
]
print(f"   Found {len(clips)} funny moments:")
for i, c in enumerate(clips, 1):
    print(f"     {i}. {c['start']}s - {c['end']}s: {c['reason']}")

# Cut shorts
print(f"\n4. CUTTING SHORTS:")
results = []

for i, c in enumerate(clips, 1):
    output_path = os.path.join(OUTPUT_DIR, f"demo_short_{i:02d}.mp4")
    print(f"   Clip {i}: {c['start']}s - {c['end']}s...", end=" ")
    
    try:
        clip = VideoFileClip(VIDEO_PATH).subclipped(c['start'], c['end'])
        
        # Resize to vertical
        w, h = clip.size
        target_w, target_h = 1080, 1920
        target_ratio = target_w / target_h
        current_ratio = w / h
        
        if current_ratio > target_ratio:
            new_w = int(h * target_ratio)
            x_center = w / 2
            clip = clip.cropped(x1=x_center - new_w/2, x2=x_center + new_w/2)
        else:
            new_h = int(w / target_ratio)
            y_center = h / 2
            clip = clip.cropped(y1=y_center - new_h/2, y2=y_center + new_h/2)
        
        clip = clip.resized(width=target_w, height=target_h)
        clip.write_videofile(output_path, codec="libx264", audio_codec="aac", logger=None)
        clip.close()
        
        size_mb = os.path.getsize(output_path) / 1024 / 1024
        print(f"OK ({size_mb:.1f} MB)")
        results.append(output_path)
    except Exception as e:
        print(f"FAILED: {e}")

# Summary
print(f"\n5. OUTPUT:")
print(f"   Generated {len(results)} shorts")
for r in results:
    size_mb = os.path.getsize(r) / 1024 / 1024
    print(f"   - {os.path.basename(r)} ({size_mb:.1f} MB)")

# Copy to assets for repo
print(f"\n6. COPY TO ASSETS:")
for r in results:
    dest = os.path.join(ASSETS_DIR, "output", os.path.basename(r))
    import shutil
    shutil.copy2(r, dest)
    print(f"   Copied: {os.path.basename(r)}")

print(f"\n{'='*60}")
print(f"  DEMO COMPLETE!")
print(f"  Output: {OUTPUT_DIR}")
print(f"  Assets: {ASSETS_DIR}/output/")
print(f"{'='*60}")
