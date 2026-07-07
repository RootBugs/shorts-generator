import sys
import os
sys.stdout.reconfigure(encoding='utf-8')
from auto_shorts import process_video
from transcript import get_transcript_with_timestamps, words_to_segments


def print_menu():
    print("""
╔════════════════════════════════════════════════════╗
║       YouTube Shorts Generator                    ║
║       Transcript → Find Funniest → Cut Clips      ║
╠════════════════════════════════════════════════════╣
║  1. Generate shorts from YouTube URL              ║
║  2. Generate shorts from local video              ║
║  3. Preview transcript (find moments)             ║
║  4. Quick test                                    ║
║  0. Exit                                          ║
╚════════════════════════════════════════════════════╝
""")


def cmd_youtube():
    url = input("\nYouTube URL: ").strip()
    if not url:
        return
    num = input("How many shorts? (default 5): ").strip()
    num = int(num) if num.isdigit() else 5
    chatgpt = input("Use ChatGPT for better cuts? (y/n, default y): ").strip().lower()
    use_chatgpt = chatgpt != 'n'

    process_video(url, num_clips=num, use_chatgpt=use_chatgpt)


def cmd_local():
    path = input("\nVideo file path: ").strip().strip('"')
    if not path or not os.path.exists(path):
        print("File not found!")
        return
    num = input("How many shorts? (default 5): ").strip()
    num = int(num) if num.isdigit() else 5
    chatgpt = input("Use ChatGPT? (y/n, default y): ").strip().lower()
    use_chatgpt = chatgpt != 'n'

    process_video(path, num_clips=num, use_chatgpt=use_chatgpt)


def cmd_preview():
    url = input("\nYouTube URL: ").strip()
    if not url:
        return

    print("\nExtracting transcript...")
    words = get_transcript_with_timestamps(url)
    if not words:
        print("No transcript found!")
        return

    segments = words_to_segments(words)
    print(f"\nFound {len(segments)} segments:\n")

    for i, s in enumerate(segments[:30], 1):
        duration = s['end'] - s['start']
        print(f"{i:3d}. [{s['start']:6.1f}s - {s['end']:6.1f}s] ({duration:4.1f}s) {s['text'][:70]}")

    if len(segments) > 30:
        print(f"\n... and {len(segments) - 30} more segments")


def cmd_quick_test():
    print("\n=== Quick Test ===")
    print("Using a trending video to test the pipeline...\n")

    from searcher import search_youtube
    videos = search_youtube("funny cartoon compilation", max_results=1)
    if not videos:
        print("No videos found.")
        return

    best = videos[0]
    t = best['title'][:60].encode('ascii', 'replace').decode()
    print(f"Video: {t}")
    print(f"URL: {best['url']}")
    print("\nGenerating 2 shorts (no ChatGPT)...\n")

    process_video(best['url'], num_clips=2, use_chatgpt=False)


def main():
    print_menu()
    while True:
        try:
            choice = input("\nSelect (0-4): ").strip()
            if choice == "1": cmd_youtube()
            elif choice == "2": cmd_local()
            elif choice == "3": cmd_preview()
            elif choice == "4": cmd_quick_test()
            elif choice == "0": print("Bye!"); break
            else: print("Invalid choice")
        except KeyboardInterrupt:
            print("\nInterrupted"); break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
