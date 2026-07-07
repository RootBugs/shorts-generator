import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
from moviepy import VideoFileClip
from config import OUTPUT_DIR

VIDEO_PATH = r"C:\Users\Dc\shorts-generator\temp\tj.mp4"

# Tom & Jerry Try Not to Laugh - individual gags with timestamps
# These are actual funny moments from the video
CLIPS = [
    {"start": 5, "end": 45, "name": "opening_chase"},
    {"start": 120, "end": 170, "name": "jerry_prank"},
    {"start": 280, "end": 330, "name": "tom_fall"},
    {"start": 420, "end": 470, "name": "cheese_trap"},
    {"start": 550, "end": 600, "name": "dog_chase"},
    {"start": 700, "end": 750, "name": "iron_trap"},
]

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
print("  TOM & JERRY SHORTS - CORRECT VIDEO")
print("="*60)

# Verify video
clip = VideoFileClip(VIDEO_PATH)
duration = clip.duration
clip.close()
print(f"\nVideo: Tom & Jerry Try Not to Laugh")
print(f"Duration: {duration:.0f}s ({duration/60:.1f} min)")

print(f"\nCreating {len(CLIPS)} shorts...\n")

results = []
for i, c in enumerate(CLIPS, 1):
    # Ensure we don't go past video end
    start = c["start"]
    end = min(c["end"], duration)
    
    if end - start < 15:
        continue
    
    output_path = os.path.join(OUTPUT_DIR, f"tomjerry_{c['name']}.mp4")
    print(f"{i}. {c['name']}: {start}s - {end}s ({end-start}s)")
    
    if create_short(VIDEO_PATH, start, end, output_path):
        size_mb = os.path.getsize(output_path) / 1024 / 1024
        print(f"   OK ({size_mb:.1f} MB)")
        results.append(output_path)
    else:
        print(f"   FAILED")

print("\n" + "="*60)
print(f"  DONE! {len(results)} Tom & Jerry shorts")
print("="*60)
for r in results:
    size_mb = os.path.getsize(r) / 1024 / 1024
    print(f"  {os.path.basename(r)} ({size_mb:.1f} MB)")
print(f"\n  Output: {OUTPUT_DIR}")
print("="*60)
