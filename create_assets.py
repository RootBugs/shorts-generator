from moviepy import VideoFileClip
import os

OUTPUT_DIR = r"C:\Users\Dc\shorts-generator\output"
ASSETS_DIR = r"C:\Users\Dc\shorts-generator\assets"

# Create demo GIF from first short
short1 = os.path.join(OUTPUT_DIR, "tomjerry_jerry_prank.mp4")
gif_path = os.path.join(ASSETS_DIR, "demo.gif")

print("Creating demo GIF...")
clip = VideoFileClip(short1)
clip = clip.subclipped(0, 5)  # First 5 seconds
clip = clip.resized(width=320)
clip.write_gif(gif_path, fps=8)
clip.close()

size_kb = os.path.getsize(gif_path) / 1024
print(f"Created: demo.gif ({size_kb:.1f} KB)")

# Create a preview video (all shorts side by side as compilation)
print("\nCreating preview compilation...")
clips = []
for f in sorted(os.listdir(OUTPUT_DIR)):
    if f.startswith("tomjerry_") and f.endswith(".mp4"):
        path = os.path.join(OUTPUT_DIR, f)
        c = VideoFileClip(path).subclipped(0, 3)  # First 3 seconds of each
        clips.append(c)

if clips:
    from moviepy import concatenate_videoclips
    preview = concatenate_videoclips(clips)
    preview_path = os.path.join(ASSETS_DIR, "preview.mp4")
    preview.write_videofile(preview_path, codec="libx264", audio_codec="aac", logger=None)
    preview.close()
    for c in clips:
        c.close()
    print(f"Created: preview.mp4 ({os.path.getsize(preview_path) / 1024 / 1024:.1f} MB)")

print("\nDone!")
