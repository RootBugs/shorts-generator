import os
import subprocess
import sys
sys.stdout.reconfigure(encoding='utf-8')


def check_ffmpeg():
    try:
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True, timeout=5)
        return result.returncode == 0
    except:
        return False


def check_ffprobe():
    try:
        result = subprocess.run(["ffprobe", "-version"], capture_output=True, text=True, timeout=5)
        return result.returncode == 0
    except:
        return False


def check_ytdlp():
    try:
        result = subprocess.run(["yt-dlp", "--version"], capture_output=True, text=True, timeout=5)
        return result.returncode == 0
    except:
        return False


def main():
    print("=" * 50)
    print("  Shorts Generator - Setup Check")
    print("=" * 50)

    ffmpeg_ok = check_ffmpeg()
    ffprobe_ok = check_ffprobe()
    ytdlp_ok = check_ytdlp()

    print(f"\n  [{'OK' if ffmpeg_ok else '!!'}] ffmpeg  {'installed' if ffmpeg_ok else 'MISSING'}")
    print(f"  [{'OK' if ffprobe_ok else '!!'}] ffprobe {'installed' if ffprobe_ok else 'MISSING'}")
    print(f"  [{'OK' if ytdlp_ok else '!!'}] yt-dlp  {'installed' if ytdlp_ok else 'MISSING'}")

    print("\n" + "=" * 50)
    if ffmpeg_ok and ffprobe_ok and ytdlp_ok:
        print("  All checks passed!")
        print("  Run: python main.py")
    else:
        print("  Missing tools:")
        if not ffmpeg_ok:
            print("  - ffmpeg: winget install ffmpeg")
        if not ffprobe_ok:
            print("  - ffprobe: comes with ffmpeg")
        if not ytdlp_ok:
            print("  - yt-dlp: pip install yt-dlp")
    print("=" * 50)


if __name__ == "__main__":
    main()
