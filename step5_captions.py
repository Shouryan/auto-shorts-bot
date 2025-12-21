import whisper
import os
import sys
import PIL.Image

# --- PILLOW PATCH ---
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS
# --------------------

from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

def get_file_path(filename):
    """
    Robustly finds a file relative to this script, regardless of where the script is run from.
    """
    # Get the directory where the script is actually located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Join it with the filename
    return os.path.join(script_dir, filename)

def split_text_into_chunks(text, max_words=4):
    words = text.split()
    chunks = []
    current_chunk = []
    for word in words:
        current_chunk.append(word)
        if len(current_chunk) >= max_words:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks

def burn_captions(video_filename, audio_filename, output_filename, font_filename):
    print("--- Starting Automated Captioning ---")
    
    # 1. RESOLVE ALL FILE PATHS AUTOMATICALLY
    video_path = get_file_path(video_filename)
    audio_path = get_file_path(audio_filename)
    output_path = get_file_path(output_filename)
    font_path = get_file_path(font_filename)

    # 2. VALIDATE ASSETS BEFORE STARTING
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"❌ CRITICAL ERROR: Video file missing at {video_path}")
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"❌ CRITICAL ERROR: Audio file missing at {audio_path}")
    
    # Check Font specifically
    font_arg = 'Arial-Bold' # Default fallback
    if os.path.exists(font_path):
        print(f"✅ Custom font found: {font_path}")
        font_arg = font_path 
    else:
        print(f"⚠️ WARNING: Custom font not found at {font_path}. Using system Arial.")

    # 3. Transcribe
    print("Transcribing audio...")
    model = whisper.load_model("base")
    result = model.transcribe(audio_path, word_timestamps=True) 
    segments = result['segments']

    # 4. Load Video
    video_clip = VideoFileClip(video_path)
    video_width, video_height = video_clip.size
    
    # 5. Generate Text Clips
    text_clips = []
    print("Generating text clips...")
    
    for segment in segments:
        full_text = segment['text'].strip().upper()
        start = segment['start']
        end = segment['end']
        duration = end - start
        
        chunks = split_text_into_chunks(full_text, max_words=4)
        if not chunks: continue
            
        total_len = len(full_text.replace(" ", ""))
        current_start = start
        
        for chunk in chunks:
            chunk_len = len(chunk.replace(" ", ""))
            chunk_duration = (chunk_len / total_len) * duration if total_len > 0 else 0
            
            txt_clip = TextClip(
                chunk, 
                fontsize=75, 
                color='#FFFFFF', 
                font=font_arg,  # Uses the robust path
                stroke_color='white', 
                stroke_width=5, 
                method='caption',
                size=(int(video_width * 0.9), None),
                align='center'
            )
            
            txt_clip = txt_clip.set_start(current_start).set_duration(chunk_duration)
            txt_clip = txt_clip.set_position(('center', 'center'))
            
            text_clips.append(txt_clip)
            current_start += chunk_duration

    # 6. Composite & Render
    print(f"Overlaying {len(text_clips)} text clips...")
    final_composite = CompositeVideoClip([video_clip] + text_clips)

    print(f"Rendering to {output_path}...")
    final_composite.write_videofile(output_path, codec="libx264", audio_codec="aac", fps=30, preset="ultrafast")
    print("--- DONE! ---")

if __name__ == "__main__":
    # Just define filenames. The script figures out the paths.
    INPUT_VIDEO = "final_short_overlay.mp4" 
    AUDIO_FILE = "voiceover.mp3"
    OUTPUT_FILE = "final_short_automated.mp4"
    FONT_NAME = "TikTokSans-VariableFont_opsz,slnt,wdth,wght.ttf" # Must be in the same folder
    
    try:
        burn_captions(INPUT_VIDEO, AUDIO_FILE, OUTPUT_FILE, FONT_NAME)
    except Exception as e:
        print(f"Script Failed: {e}")