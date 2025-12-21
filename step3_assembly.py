import os
import sys
import traceback

# --- PILLOW PATCH (Crucial for newer Pillow versions) ---
import PIL.Image
if not hasattr(PIL.Image, 'ANTIALIAS'):
    print("DEBUG: Applying Pillow ANTIALIAS patch...")
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS
# --------------------

from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip, CompositeVideoClip

def create_short(background_path, audio_path, image_path, output_path):
    print(f"\n{'='*40}")
    print(f"🎬 STEP 3 START: Assembly ({output_path})")
    print(f"{'='*40}")

    # 1. VALIDATE FILES
    print("🔍 Checking input files...")
    files = {
        "Audio": audio_path,
        "Background": background_path,
        "Image": image_path
    }
    
    missing = []
    for name, path in files.items():
        if os.path.exists(path):
            size_mb = os.path.getsize(path) / (1024 * 1024)
            print(f"  ✅ Found {name}: {path} ({size_mb:.2f} MB)")
        else:
            print(f"  ❌ MISSING {name}: {path}")
            missing.append(path)
            
    if missing:
        raise FileNotFoundError(f"Missing required files: {missing}")

    try:
        # 2. LOAD AUDIO
        print(f"🔊 Loading Audio: {audio_path}")
        audio_clip = AudioFileClip(audio_path)
        short_duration = audio_clip.duration
        print(f"  - Audio Duration: {short_duration:.2f} seconds")

        # 3. LOAD BACKGROUND
        print(f"🎥 Loading Video: {background_path}")
        video_clip = VideoFileClip(background_path)
        print(f"  - Original Video Size: {video_clip.size}")
        
        # Trim video to match audio
        print(f"✂️ Trimming video to {short_duration:.2f}s...")
        video_clip = video_clip.subclip(0, short_duration)

        # 4. CROP TO 9:16
        w, h = video_clip.size
        target_ratio = 9 / 16
        current_ratio = w / h
        print(f"📐 Cropping Check: Current Ratio {current_ratio:.2f} vs Target {target_ratio:.2f}")
        
        if current_ratio > target_ratio:
            new_width = int(h * target_ratio)
            print(f"  - Cropping width from {w} to {new_width} (Height remains {h})")
            video_clip = video_clip.crop(x1=w/2 - new_width/2, x2=w/2 + new_width/2, y1=0, y2=h)
        else:
            print("  - Video is already vertical enough. No crop needed.")
            
        print(f"  - Final Video Dimensions: {video_clip.w}x{video_clip.h}")

        # 5. LOAD & RESIZE IMAGE
        print(f"🖼️ Processing Image: {image_path}")
        image_clip = ImageClip(image_path)
        print(f"  - Original Image Size: {image_clip.size}")
        
        # Resize to full width
        print(f"  - Resizing image to width: {video_clip.w}")
        image_clip = image_clip.resize(width=video_clip.w)
        
        # Position at Top
        print("  - Setting position: Center, Top")
        image_clip = image_clip.set_position(("center", "top"))
        image_clip = image_clip.set_duration(short_duration)

        # 6. COMPOSITE
        print("🏗️ Combining Video + Image Layer...")
        # Image is second, so it goes ON TOP of video
        final = CompositeVideoClip([video_clip, image_clip])
        final = final.set_audio(audio_clip)

        # 7. RENDER
        print(f"💾 Rendering to {output_path}...")
        print("  - Codec: libx264, Audio: aac, Preset: ultrafast")
        
        # Using 'logger=None' to prevent spamming generic moviepy logs if we want our own, 
        # but for debugging, standard logger is fine.
        final.write_videofile(
            output_path, 
            codec="libx264", 
            audio_codec="aac", 
            fps=30, 
            preset="ultrafast",
            threads=4
        )
        print(f"✅ SUCCESS! Created {output_path}")

    except Exception as e:
        print("\n❌ CRITICAL ERROR DURING PROCESSING:")
        print(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    # FILE NAMES (Must match exactly what is in your repo/folder)
    BACKGROUND = "background.mp4" 
    AUDIO = "voiceover.mp3"     
    IMAGE = "topic_image.png"   
    OUTPUT = "final_short_overlay.mp4" 
    
    create_short(BACKGROUND, AUDIO, IMAGE, OUTPUT)
