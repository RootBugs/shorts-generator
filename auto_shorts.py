import subprocess
import os
import json
import sys
import shutil
sys.stdout.reconfigure(encoding='utf-8')
from datetime import datetime
from config import YTDLP_PATH, INPUT_DIR, OUTPUT_DIR, TEMP_DIR, NUM_CLIPS
from transcript import download_video, get_transcript_with_timestamps, words_to_segments
from cutter import create_short, get_video_duration


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GENERATED_DIR = os.path.join(SCRIPT_DIR, "generated")
os.makedirs(GENERATED_DIR, exist_ok=True)


def analyze_with_chatgpt(video_title: str, segments: list[dict]) -> list[dict]:
    """Use ChatGPT to find funniest moments."""
    try:
        sys.path.insert(0, SCRIPT_DIR)
        from chatgpt import findFunnyMoments
        import asyncio
        result = asyncio.run(findFunnyMoments(video_title, segments))
        if result and "clips" in result:
            return result["clips"]
    except Exception as e:
        print(f"  ChatGPT error: {e}")
    return []


def analyze_locally(segments: list[dict], num_clips: int = 5) -> list[dict]:
    """Fallback: find interesting moments based on word patterns."""
    funny_keywords = [
        "funny", "laugh", "haha", "lol", "joke", "stupid", "idiot",
        "oh no", "what", "why", "no way", "shut up", "really",
        "damn", "crazy", "insane", "epic", "fail", "win",
    ]

    scored = []
    for i, seg in enumerate(segments):
        text_lower = seg["text"].lower()
        score = 0
        for kw in funny_keywords:
            if kw in text_lower:
                score += 2
        # Prefer medium length clips
        duration = seg["end"] - seg["start"]
        if 15 <= duration <= 55:
            score += 3
        elif 10 <= duration <= 60:
            score += 1
        # Boost segments with exclamation marks (excitement)
        score += seg["text"].count("!")
        # Boost question marks (setup for punchline)
        score += seg["text"].count("?") * 0.5

        scored.append({**seg, "score": score, "index": i})

    scored.sort(key=lambda x: x["score"], reverse=True)

    # Pick clips spread across the video
    clips = []
    used_ranges = []
    for s in scored:
        if len(clips) >= num_clips:
            break
        # Check overlap with existing clips
        overlap = False
        for used in used_ranges:
            if not (s["end"] < used[0] or s["start"] > used[1]):
                overlap = True
                break
        if not overlap:
            clips.append({
                "start": s["start"],
                "end": s["end"],
                "reason": f"Scored {s['score']:.0f} - engaging content",
                "title": s["text"][:50],
                "hashtags": ["funny", "viral", "shorts"],
            })
            used_ranges.append((s["start"], s["end"]))

    return clips


def merge_close_clips(clips: list[dict], min_gap: float = 5.0) -> list[dict]:
    """Merge clips that are close together."""
    if not clips:
        return []

    clips.sort(key=lambda x: x["start"])
    merged = [clips[0]]

    for c in clips[1:]:
        last = merged[-1]
        if c["start"] - last["end"] < min_gap:
            merged[-1] = {
                "start": last["start"],
                "end": c["end"],
                "reason": last["reason"] + " + " + c["reason"],
                "title": last["title"],
                "hashtags": list(set(last.get("hashtags", []) + c.get("hashtags", [])))[:8],
            }
        else:
            merged.append(c)

    return merged


def process_video(video_source: str, num_clips: int = None, use_chatgpt: bool = True) -> list[dict]:
    """Full pipeline: download → transcript → find moments → cut shorts."""
    num_clips = num_clips or NUM_CLIPS

    print(f"\n{'='*50}")
    print(f"SHORTS GENERATOR")
    print(f"{'='*50}")

    # Step 1: Download or use local file
    print("\n[1/4] Getting video...")
    if video_source.startswith("http"):
        video_path = download_video(video_source)
        if not video_path:
            print("Download failed!")
            return []
    else:
        video_path = video_source
        if not os.path.exists(video_path):
            print(f"File not found: {video_path}")
            return []

    print(f"  Video: {os.path.basename(video_path)}")

    # Step 2: Get transcript
    print("\n[2/4] Extracting transcript...")
    words = get_transcript_with_timestamps(video_source if video_source.startswith("http") else video_path)
    if not words:
        print("  No transcript found!")
        return []

    segments = words_to_segments(words)
    print(f"  Found {len(words)} words, {len(segments)} segments")

    # Step 3: Find funniest moments
    print("\n[3/4] Finding best moments...")
    video_title = os.path.splitext(os.path.basename(video_path))[0]

    if use_chatgpt:
        clips = analyze_with_chatgpt(video_title, segments)
        if clips:
            print(f"  ChatGPT found {len(clips)} clips")
        else:
            print("  ChatGPT failed, using local analysis")
            clips = analyze_locally(segments, num_clips)
    else:
        clips = analyze_locally(segments, num_clips)

    if not clips:
        print("  No clips found!")
        return []

    # Merge close clips
    clips = merge_close_clips(clips)
    print(f"  Final: {len(clips)} clips")

    # Step 4: Cut shorts
    print("\n[4/4] Cutting shorts...")
    results = []
    vid_name = os.path.splitext(os.path.basename(video_path))[0]
    vid_name = "".join(c if c.isalnum() or c in "._-" else "_" for c in vid_name)[:60]

    for i, clip in enumerate(clips[:num_clips], 1):
        start = clip["start"]
        end = clip["end"]
        duration = end - start

        # Enforce duration limits
        if duration < 15:
            end = start + 20
        elif duration > 58:
            end = start + 55

        output_path = os.path.join(OUTPUT_DIR, f"{vid_name}_short_{i:02d}.mp4")
        print(f"\n  Clip {i}/{min(len(clips), num_clips)}: {start:.1f}s - {end:.1f}s")
        print(f"    Reason: {clip.get('reason', 'N/A')[:60]}")

        result = create_short(video_path, start, end, words, output_path)
        if result:
            print(f"    Created: {os.path.basename(result)}")
            results.append({
                "clip_number": i,
                "start": start,
                "end": end,
                "duration": end - start,
                "reason": clip.get("reason", ""),
                "title": clip.get("title", ""),
                "hashtags": clip.get("hashtags", []),
                "output_path": result,
            })
        else:
            print(f"    FAILED")

    # Save metadata
    meta_path = os.path.join(GENERATED_DIR, f"{vid_name}_clips.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump({
            "source_video": video_path,
            "total_clips": len(results),
            "clips": results,
            "generated_at": datetime.now().isoformat(),
        }, f, indent=2, ensure_ascii=False)

    # Cleanup temp
    for f in os.listdir(TEMP_DIR):
        try:
            os.remove(os.path.join(TEMP_DIR, f))
        except:
            pass

    print(f"\n{'='*50}")
    print(f"DONE! Generated {len(results)} shorts")
    print(f"Output: {OUTPUT_DIR}")
    print(f"Metadata: {meta_path}")
    print(f"{'='*50}")

    return results


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python auto_shorts.py <youtube_url>")
        print("  python auto_shorts.py <local_video.mp4>")
        print("  python auto_shorts.py <url> --clips 8")
        print("  python auto_shorts.py <url> --no-chatgpt")
        sys.exit(1)

    source = sys.argv[1]
    num = 5
    chatgpt = True

    for i, arg in enumerate(sys.argv[2:], 2):
        if arg == "--clips" and i + 1 < len(sys.argv):
            num = int(sys.argv[i + 1])
        elif arg == "--no-chatgpt":
            chatgpt = False

    process_video(source, num_clips=num, use_chatgpt=chatgpt)
