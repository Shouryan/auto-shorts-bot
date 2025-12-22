import os
import sys
import traceback

# --- PILLOW PATCH ---
import PIL.Image
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS
# --------------------

from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip, CompositeVideoClip

def create_short(background_path, audio_path, image_path, output_path):
    print(f"\n{'='*40}")
    print(f"🎬 STEP 3: HD Assembly (1080x1920)")
    print(f"{'='*40}")

    try:
        # 1. Load Audio
        audio_clip = AudioFileClip(audio_path)
        duration = audio_clip.duration
        
        # 2. Load & Prepare Background (HD FORCE)
        print(f"🎥 Processing Video: {background_path}")
        video_clip = VideoFileClip(background_path)
        
        # Loop video if it's shorter than audio
        if video_clip.duration < duration:
            print("   - Video too short, looping it...")
            video_clip = video_clip.loop(duration=duration)
        
        video_clip = video_clip.subclip(0, duration)
        
        # --- HD RESIZING LOGIC ---
        # We want 1080x1920. We resize by HEIGHT first to ensure coverage.
        target_h = 1920
        target_w = 1080
        
        # Resize height to 1920 (width will scale automatically)
        video_clip = video_clip.resize(height=target_h)
        
        # Center Crop to 1080 width
        if video_clip.w > target_w:
            video_clip = video_clip.crop(x1=video_clip.w/2 - target_w/2, 
                                         x2=video_clip.w/2 + target_w/2, 
                                         width=target_w, height=target_h)
        # -------------------------

        # 3. Load & Position Image
        print(f"🖼️ Processing Image overlay...")
        image_clip = ImageClip(image_path)
        
        # Resize image to 90% of screen width for nice padding
        image_clip = image_clip.resize(width=target_w * 0.9)
        image_clip = image_clip.set_position(("center", "center")) # Put it right in the middle
        image_clip = image_clip.set_duration(duration)

        # 4. Composite
        print("🏗️ Compositing layers...")
        final = CompositeVideoClip([video_clip, image_clip])
        final = final.set_audio(audio_clip)

        # 5. Render in HD
        print(f"💾 Rendering HD to {output_path}...")
        final.write_videofile(
            output_path, 
            codec="libx264", 
            audio_codec="aac", 
            fps=30, 
            preset="medium",   # 'medium' gives better quality than 'ultrafast'
            bitrate="5000k",   # High bitrate for HD
            threads=4
        )
        print("✅ HD RENDER COMPLETE!")

    except Exception as e:
        print("\n❌ CRITICAL ERROR IN ASSEMBLY:")
        print(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    # Ensure these names match your files
    create_short("background.mp4", "voiceover.mp3", "topic_image.png", "final_short_automated.mp4")
