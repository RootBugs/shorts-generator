import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
sys.stdout.reconfigure(encoding='utf-8')
from config import OUTPUT_DIR, TEMP_DIR, NUM_CLIPS
from transcript import get_transcript_with_timestamps, words_to_segments
from cutter import cut_single, get_duration

def download_video(url):
    """Download video using yt-dlp."""
    import subprocess
    output_template = os.path.join(TEMP_DIR, "source.%(ext)s")
    cmd = [
        "yt-dlp", "-f", "best[height<=720]",
        "--no-playlist", "-o", output_template, url
    ]
    subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    for f in os.listdir(TEMP_DIR):
        if f.startswith("source") and f.endswith(".mp4"):
            return os.path.join(TEMP_DIR, f)
    return None

def find_clips(words, num_clips, video_path):
    """Find clips from transcript or fallback to equal segments."""
    if words:
        segments = words_to_segments(words)
        keywords = ["funny", "laugh", "wow", "oh", "no", "what", "crazy", "epic"]
        scored = []
        for seg in segments:
            text = seg["text"].lower()
            duration = seg["end"] - seg["start"]
            score = sum(2 for kw in keywords if kw in text)
            if 15 <= duration <= 50:
                score += 5
            scored.append({**seg, "score": score})
        scored.sort(key=lambda x: x["score"], reverse=True)
        
        clips = []
        used = []
        for s in scored:
            if len(clips) >= num_clips:
                break
            overlap = any(not (s["end"] < u[0] or s["start"] > u[1]) for u in used)
            if not overlap:
                start = max(0, s["start"] - 2)
                end = min(s["end"] + 2, s["start"] + 55)
                if end - start < 15:
                    end = start + 20
                clips.append({"start": start, "end": end})
                used.append((start, end))
        if clips:
            return clips
    
    # Fallback: equal segments
    duration = get_duration(video_path)
    if duration <= 0:
        return []
    seg_len = min(duration / num_clips, 50)  # Max 50s per clip
    return [{"start": i * seg_len + 2, "end": min((i + 1) * seg_len, duration - 2)} 
            for i in range(num_clips) if seg_len > 15]

def process_video(url_or_path, num_clips=None):
    """Main pipeline - OPTIMIZED."""
    num_clips = num_clips or NUM_CLIPS
    t0 = time.time()
    
    print("="*50)
    print("  SHORTS GENERATOR (FAST)")
    print("="*50)
    
    # Get video
    print("\n[1/4] Video...")
    if url_or_path.startswith("http"):
        video_path = download_video(url_or_path)
    else:
        video_path = url_or_path
    
    if not video_path or not os.path.exists(video_path):
        print("  Not found!")
        return []
    print(f"  {os.path.basename(video_path)}")
    
    # Transcript
    print("\n[2/4] Transcript...")
    words = get_transcript_with_timestamps(url_or_path) if url_or_path.startswith("http") else []
    print(f"  {len(words)} words")
    
    # Find clips
    print("\n[3/4] Analyzing...")
    clips = find_clips(words, num_clips, video_path)
    print(f"  {len(clips)} clips")
    
    # Cut in parallel
    print(f"\n[4/4] Cutting (parallel)...")
    if not clips:
        print("  Nothing to cut!")
        return []
    
    vid_name = "".join(c if c.isalnum() or c in "._-" else "_" for c in os.path.splitext(os.path.basename(video_path))[0])[:50]
    
    results = []
    with ThreadPoolExecutor(max_workers=min(4, len(clips))) as pool:
        futures = {}
        for i, c in enumerate(clips, 1):
            out = os.path.join(OUTPUT_DIR, f"{vid_name}_{i:02d}.mp4")
            futures[pool.submit(cut_single, video_path, c["start"], c["end"], out)] = (i, out)
        
        for f in as_completed(futures):
            i, out = futures[f]
            if f.result():
                size = os.path.getsize(out) / 1024 / 1024
                print(f"  [{i}/{len(clips)}] {os.path.basename(out)} ({size:.1f} MB)")
                results.append(out)
    
    elapsed = time.time() - t0
    print(f"\n{'='*50}")
    print(f"  {len(results)} shorts in {elapsed:.1f}s")
    print(f"{'='*50}")
    return results

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python auto_shorts.py <url_or_path> [--clips N]")
        sys.exit(1)
    
    source = sys.argv[1]
    num = 5
    for i, arg in enumerate(sys.argv[2:], 2):
        if arg == "--clips" and i + 1 < len(sys.argv):
            num = int(sys.argv[i + 1])
    process_video(source, num_clips=num)
