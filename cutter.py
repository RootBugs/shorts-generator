import subprocess
import os
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

def get_ffmpeg():
    """Get imageio's bundled ffmpeg."""
    try:
        from imageio_ffmpeg import get_ffmpeg_exe
        return get_ffmpeg_exe()
    except:
        return "ffmpeg"

def get_duration(video_path):
    ffmpeg = get_ffmpeg()
    ffprobe = ffmpeg.replace("ffmpeg.exe", "ffprobe.exe").replace("ffmpeg", "ffprobe")
    if not os.path.exists(ffprobe):
        ffprobe = "ffprobe"
    cmd = [ffprobe, "-v", "quiet", "-print_format", "json", "-show_format", video_path]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
    if result.returncode == 0:
        try:
            return float(json.loads(result.stdout)["format"]["duration"])
        except:
            pass
    return 0

def cut_single(video_path, start, end, output_path):
    """Cut clip using imageio's ffmpeg binary directly."""
    ffmpeg = get_ffmpeg()
    duration = end - start
    
    cmd = [
        ffmpeg, "-y",
        "-ss", str(start),
        "-i", video_path,
        "-t", str(duration),
        "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "28",
        "-c:a", "aac", "-b:a", "64k",
        "-movflags", "+faststart", "-threads", "0",
        output_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    return result.returncode == 0 and os.path.exists(output_path)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python cutter.py <video> <start> <end> [output]")
        sys.exit(1)
    
    video = sys.argv[1]
    start = float(sys.argv[2])
    end = float(sys.argv[3])
    output = sys.argv[4] if len(sys.argv) > 4 else "output_short.mp4"
    
    print(f"FFmpeg: {get_ffmpeg()}")
    result = cut_single(video, start, end, output)
    if result:
        size = os.path.getsize(output) / 1024 / 1024
        print(f"Created: {output} ({size:.1f} MB)")
    else:
        print("Failed!")
