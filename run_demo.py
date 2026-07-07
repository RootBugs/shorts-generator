import sys
sys.stdout.reconfigure(encoding='utf-8')
from transcript import get_transcript_with_timestamps, words_to_segments
from cutter import create_short
from config import OUTPUT_DIR
import os

video_path = r"C:\Users\Dc\shorts-generator\temp\source.mp4"
video_url = "https://www.youtube.com/watch?v=v9WSjE3tIkg"

print("="*50)
print("SHORTS GENERATOR - DEMO")
print("="*50)

# Step 1: Get transcript from YouTube URL
print("\n[1/3] Extracting transcript from YouTube...")
words = get_transcript_with_timestamps(video_url)
if not words:
    print("No transcript found!")
    sys.exit(1)

segments = words_to_segments(words)
print(f"  Words: {len(words)}, Segments: {len(segments)}")

# Step 2: Find best moments (local analysis)
print("\n[2/3] Finding funniest moments...")

funny_keywords = ["funny", "laugh", "haha", "lol", "joke", "stupid", "idiot",
    "oh no", "what", "why", "no way", "shut up", "really",
    "damn", "crazy", "insane", "epic", "fail", "win", "insane", "crazy"]

scored = []
for seg in segments:
    text_lower = seg["text"].lower()
    score = sum(2 for kw in funny_keywords if kw in text_lower)
    duration = seg["end"] - seg["start"]
    if 15 <= duration <= 55:
        score += 3
    elif 10 <= duration <= 60:
        score += 1
    score += seg["text"].count("!")
    score += seg["text"].count("?") * 0.5
    scored.append({**seg, "score": score})

scored.sort(key=lambda x: x["score"], reverse=True)

# Pick 2 clips spread across video
clips = []
used_ranges = []
for s in scored:
    if len(clips) >= 2:
        break
    overlap = any(not (s["end"] < u[0] or s["start"] > u[1]) for u in used_ranges)
    if not overlap:
        clips.append(s)
        used_ranges.append((s["start"], s["end"]))

print(f"  Found {len(clips)} clips:")
for i, c in enumerate(clips, 1):
    print(f"    {i}. [{c['start']:.1f}s - {c['end']:.1f}s] Score: {c['score']:.0f}")
    print(f"       {c['text'][:60]}...")

# Step 3: Cut shorts
print("\n[3/3] Cutting shorts...")
vid_name = "tiktoks"
results = []

for i, clip in enumerate(clips, 1):
    start = clip["start"]
    end = clip["end"]
    if end - start < 15:
        end = start + 20
    elif end - start > 58:
        end = start + 55

    output_path = os.path.join(OUTPUT_DIR, f"{vid_name}_short_{i:02d}.mp4")
    print(f"\n  Clip {i}: {start:.1f}s - {end:.1f}s ({end-start:.1f}s)")

    result = create_short(video_path, start, end, words, output_path)
    if result:
        print(f"  CREATED: {os.path.basename(result)}")
        results.append(result)
    else:
        print(f"  FAILED")

# Summary
print("\n" + "="*50)
print(f"DONE! Generated {len(results)} shorts")
for r in results:
    size_mb = os.path.getsize(r) / 1024 / 1024
    print(f"  {os.path.basename(r)} ({size_mb:.1f} MB)")
print(f"Output folder: {OUTPUT_DIR}")
print("="*50)
