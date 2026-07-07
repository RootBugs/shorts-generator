import subprocess
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
from config import OUTPUT_DIR, TEMP_DIR
from moviepy import VideoFileClip

VIDEO_PATH = os.path.join(TEMP_DIR, "source.mp4")
NUM_CLIPS = 6
CLIP_DURATION = 30  # seconds each

def create_short(video_path, start, end, output_path):
    try:
        clip = VideoFileClip(video_path).subclipped(start, end)
        
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
        return os.path.exists(output_path)
    except Exception as e:
        print(f"    Error: {e}")
        return False

print("="*60)
print("  TOM & JERRY SHORTS GENERATOR")
print("="*60)

if not os.path.exists(VIDEO_PATH):
    print("\nDownloading...")
    cmd = [
        "yt-dlp", "-f", "best[ext=mp4]",
        "-o", os.path.join(TEMP_DIR, "source.%(ext)s"),
        "--no-playlist",
        "https://www.youtube.com/watch?v=Or-XHvRZFq0"
    ]
    subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    for f in os.listdir(TEMP_DIR):
        if f.startswith("source") and f.endswith(".mp4"):
            VIDEO_PATH = os.path.join(TEMP_DIR, f)
            break

if not os.path.exists(VIDEO_PATH):
    print("Download failed!")
    sys.exit(1)

clip = VideoFileClip(VIDEO_PATH)
duration = clip.duration
clip.close()
print(f"\nVideo: {os.path.basename(VIDEO_PATH)}")
print(f"Duration: {duration:.0f}s ({duration/60:.1f} min)")
print(f"Size: {os.path.getsize(VIDEO_PATH) / 1024 / 1024:.1f} MB")

# Create equal segments
print(f"\nCreating {NUM_CLIPS} shorts ({CLIP_DURATION}s each)...\n")

results = []
segment_size = duration / NUM_CLIPS

for i in range(NUM_CLIPS):
    start = i * segment_size
    end = min(start + CLIP_DURATION, duration)
    
    if end - start < 15:
        continue
    
    output_path = os.path.join(OUTPUT_DIR, f"tom_jerry_{i+1:02d}.mp4")
    print(f"Clip {i+1}: {start:.0f}s - {end:.0f}s ({end-start:.0f}s)")
    
    if create_short(VIDEO_PATH, start, end, output_path):
        size_mb = os.path.getsize(output_path) / 1024 / 1024
        print(f"  CREATED: tom_jerry_{i+1:02d}.mp4 ({size_mb:.1f} MB)")
        results.append(output_path)
    else:
        print(f"  FAILED")

print("\n" + "="*60)
print(f"  DONE! Generated {len(results)} Tom & Jerry shorts")
print("="*60)
for r in results:
    size_mb = os.path.getsize(r) / 1024 / 1024
    print(f"  {os.path.basename(r)} ({size_mb:.1f} MB)")
print(f"\n  Output: {OUTPUT_DIR}")
print("="*60)
