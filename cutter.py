import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
from moviepy import VideoFileClip


def cut_clip(video_path: str, start: float, end: float, output_path: str) -> bool:
    """Cut a clip from video using moviepy."""
    try:
        clip = VideoFileClip(video_path).subclipped(start, end)
        clip.write_videofile(output_path, codec="libx264", audio_codec="aac", logger=None)
        clip.close()
        return os.path.exists(output_path)
    except Exception as e:
        print(f"Cut error: {e}")
        return False


def convert_to_shorts(input_path: str, output_path: str, width: int = 1080, height: int = 1920) -> bool:
    """Convert video to vertical shorts format (9:16)."""
    try:
        clip = VideoFileClip(input_path)
        
        # Calculate crop and resize
        w, h = clip.size
        target_ratio = width / height
        current_ratio = w / h
        
        if current_ratio > target_ratio:
            # Video is wider, crop sides
            new_w = int(h * target_ratio)
            x_center = w / 2
            clip = clip.cropped(x1=x_center - new_w/2, x2=x_center + new_w/2)
        else:
            # Video is taller, crop top/bottom
            new_h = int(w / target_ratio)
            y_center = h / 2
            clip = clip.cropped(y1=y_center - new_h/2, y2=y_center + new_h/2)
        
        clip = clip.resized(width=width, height=height)
        clip.write_videofile(output_path, codec="libx264", audio_codec="aac", logger=None)
        clip.close()
        return os.path.exists(output_path)
    except Exception as e:
        print(f"Resize error: {e}")
        return False


def create_short(video_path: str, start: float, end: float, 
                 words: list, output_path: str) -> str | None:
    """Full pipeline: cut → resize → output."""
    temp_cut = output_path.replace(".mp4", "_cut.mp4")
    
    # Step 1: Cut clip
    print(f"    Cutting {start:.1f}s - {end:.1f}s...")
    if not cut_clip(video_path, start, end, temp_cut):
        print("    Cut failed!")
        return None
    
    # Step 2: Convert to shorts format
    print(f"    Converting to shorts (1080x1920)...")
    if not convert_to_shorts(temp_cut, output_path):
        print("    Resize failed!")
        return None
    
    # Cleanup
    try:
        os.remove(temp_cut)
    except:
        pass
    
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python cutter.py <video> <start_sec> <end_sec> [output]")
        sys.exit(1)

    video = sys.argv[1]
    start = float(sys.argv[2])
    end = float(sys.argv[3])
    output = sys.argv[4] if len(sys.argv) > 4 else "output_short.mp4"

    result = create_short(video, start, end, [], output)
    if result:
        print(f"Created: {result}")
    else:
        print("Failed!")
