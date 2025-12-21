import os

# --- PILLOW PATCH ---
import PIL.Image
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS
# --------------------

from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip, CompositeVideoClip

def create_short(background_path, audio_path, image_path, output_path):
    print("--- Starting Assembly (Image on Top Half) ---")

    # 1. Load Audio and Background
    if not os.path.exists(audio_path): raise FileNotFoundError(f"Missing: {audio_path}")
    if not os.path.exists(background_path): raise FileNotFoundError(f"Missing: {background_path}")
    
    audio_clip = AudioFileClip(audio_path)
    short_duration = audio_clip.duration
    
    video_clip = VideoFileClip(background_path)
    video_clip = video_clip.subclip(0, short_duration)
    
    # Crop to 9:16 Vertical
    w, h = video_clip.size
    target_ratio = 9 / 16
    if w / h > target_ratio:
        new_width = int(h * target_ratio)
        video_clip = video_clip.crop(x1=w/2 - new_width/2, x2=w/2 + new_width/2, y1=0, y2=h)
    print(f"Video dimensions: {video_clip.w}x{video_clip.h}")

    # 2. Load and Position Image
    if not os.path.exists(image_path): raise FileNotFoundError(f"Missing: {image_path}")
    image_clip = ImageClip(image_path)
    
    # --- UPDATED SECTION ---
    # Resize image to FULL video width
    image_clip = image_clip.resize(width=video_clip.w)
    
    # Position at the TOP Center
    image_clip = image_clip.set_position(("center", "top"))
    # -----------------------
    
    image_clip = image_clip.set_duration(short_duration)

    # 3. Composite
    print("Combining layers...")
    # Image is second in list, so it sits ON TOP of video
    final = CompositeVideoClip([video_clip, image_clip])
    final = final.set_audio(audio_clip)

    # 4. Render
    print(f"Rendering to {output_path}...")
    final.write_videofile(output_path, codec="libx264", audio_codec="aac", fps=30, preset="ultrafast")
    print("Done!")

if __name__ == "__main__":
    BACKGROUND = "background_small.mp4"
    AUDIO = "voiceover.mp3"   
    IMAGE = "topic_image.png"  
    OUTPUT = "final_short_overlay.mp4" # This file will be used by Step 5
    
    create_short(BACKGROUND, AUDIO, IMAGE, OUTPUT)
