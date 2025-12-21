from moviepy.video.io.VideoFileClip import VideoFileClip
import os

# CONFIGURATION
INPUT_FILE = "background.mp4"
OUTPUT_FILE = "background_small.mp4"
TARGET_DURATION = 60  # Seconds (Enough for any Short)

try:
    print(f"✂️ Cutting {INPUT_FILE} to first {TARGET_DURATION} seconds...")
    
    # Load and trim
    with VideoFileClip(INPUT_FILE) as video:
        # Cut from 0 to 90 seconds
        new_video = video.subclipped(0, TARGET_DURATION)
        # Resize to 1080p height if it's 4k (to save even more space)
        if video.h > 1080:
             new_video = new_video.resize(height=1080)
             
        # Write file with a reasonable bitrate (2Mbps is plenty for background)
        new_video.write_videofile(
            OUTPUT_FILE, 
            codec="libx264", 
            audio_codec="aac", 
            bitrate="2500k",
            preset="fast"
        )
    
    print("✅ Done! Check 'background_small.mp4'")
    
except OSError:
    print("❌ Error: Could not find 'background.mp4'. Is it in this folder?")