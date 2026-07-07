import subprocess
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

def search(query, max_results=5):
    cmd = ["yt-dlp", f"ytsearch{max_results}:{query}", "--flat-playlist", "--dump-json", "--no-download"]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    videos = []
    for line in result.stdout.strip().splitlines():
        if not line: continue
        try:
            data = json.loads(line)
            videos.append({
                "id": data.get("id", ""),
                "title": data.get("title", ""),
                "duration": data.get("duration", 0),
                "views": data.get("view_count") or 0,
                "url": f"https://www.youtube.com/watch?v={data.get('id', '')}",
            })
        except: pass
    return videos

queries = [
    "tom and jerry funny moments compilation 10 minutes",
    "mr bean funniest scenes compilation",
    "funny cartoon moments compilation",
    "best comedy scenes compilation hindi",
]

print("SEARCHING FOR COMEDY/CARTOON VIDEOS...\n")
all_videos = []
for q in queries:
    results = search(q, max_results=3)
    print(f"\n--- {q[:40]} ---")
    for i, v in enumerate(results, 1):
        dur = v['duration'] / 60 if v['duration'] else 0
        print(f"  {i}. {v['title'][:55]}")
        print(f"     {dur:.1f} min | {v['views']:,} views | {v['url']}")
        all_videos.append(v)

print(f"\n\nTotal found: {len(all_videos)} videos")
