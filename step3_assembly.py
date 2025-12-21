print("DEBUG: Step 3 script has started execution...")
import sys
import traceback

# Wrap imports in a try/except to catch "ImportError" crashes
try:
    print("DEBUG: Importing OS and System libraries...")
    import os
    
    # --- PILLOW PATCH ---
    print("DEBUG: Patching Pillow...")
    import PIL.Image
    if not hasattr(PIL.Image, 'ANTIALIAS'):
        PIL.Image.ANTIALIAS = PIL.Image.LANCZOS
    # --------------------

    print("DEBUG: Importing MoviePy (This is usually where it crashes)...")
    from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip, CompositeVideoClip
    print("DEBUG: MoviePy imported successfully!")

except Exception as e:
    print("\n❌ CRITICAL IMPORT ERROR:")
    print(traceback.format_exc())
    sys.exit(1)

def create_short(background_path, audio_path, image_path, output_path):
    print(f"\n{'='*40}")
    print(f"🎬 STEP 3 MAIN FUNCTION: Assembly")
    print(f"{'='*40}")

    # 1. Validate Files
    files = { "Audio": audio_path, "Background": background_path, "Image": image_path }
    for name, path in files.items():
        exists = os.path.exists(path)
        print(f"  [{'✅' if exists else '❌'}] {name}: {path}")
        if not exists:
            print(f"    -> ERROR: File not found!")
            sys.exit(1)

    try:
        # 2. Processing
        print("DEBUG: Loading Audio Clip...")
        audio_clip = AudioFileClip(audio_path)
        
        print("DEBUG: Loading Video Clip...")
        video_clip = VideoFileClip(background_path)
        
        # Trim
        video_clip = video_clip.subclip(0, audio_clip.duration)
        
        # Crop
        w, h = video_clip.size
        target_ratio = 9/16
        if w/h > target_ratio:
            new_width = int(h * target_ratio)
            video_clip = video_clip.crop(x1=w/2 - new_width/2, x2=w/2 + new_width/2, y1=0, y2=h)
            
        print("DEBUG: Loading Image...")
        image_clip = ImageClip(image_path).resize(width=video_clip.w).set_position(("center", "top")).set_duration(audio_clip.duration)

        print("DEBUG: Compositing...")
        final = CompositeVideoClip([video_clip, image_clip]).set_audio(audio_clip)

        print(f"DEBUG: Rendering to {output_path}...")
        final.write_videofile(output_path, codec="libx264", audio_codec="aac", fps=30, preset="ultrafast", logger=None)
        print("✅ SUCCESS!")

    except Exception as e:
        print("\n❌ PROCESSING ERROR:")
        print(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    # Ensure arguments match what Step 1 & 2 produce
    create_short("background.mp4", "voiceover.mp3", "topic_image.png", "final_short_overlay.mp4")
