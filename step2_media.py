import edge_tts
import asyncio
import os

# VOICE OPTIONS
# "en-US-ChristopherNeural" -> Best for storytelling/facts (Male)
# "en-US-GuyNeural"         -> Casual/Energetic (Male)
VOICE = "en-US-ChristopherNeural"

async def generate_voiceover(text, output_filename="voiceover.mp3"):
    print(f"--- Generating Voiceover (Edge-TTS: {VOICE}) ---")
    
    # +10% speed for better engagement
    communicate = edge_tts.Communicate(text, VOICE, rate="+10%")
    
    await communicate.save(output_filename)
    print(f"✅ Saved to {output_filename}")

if __name__ == "__main__":
    # FILE PATHS
    SCRIPT_FILE = "daily_script.txt"
    OUTPUT_FILE = "voiceover.mp3"

    # 1. Read the text from Step 1
    if os.path.exists(SCRIPT_FILE):
        with open(SCRIPT_FILE, "r", encoding="utf-8") as f:
            TEXT = f.read().strip()
        
        if not TEXT:
            print(f"❌ Error: {SCRIPT_FILE} is empty!")
        else:
            print(f"📜 Loaded script from file: \"{TEXT[:50]}...\"")
            # 2. Generate Audio
            asyncio.run(generate_voiceover(TEXT, OUTPUT_FILE))
    else:
        print(f"❌ Error: Could not find '{SCRIPT_FILE}'")
        print("   Did you run 'step1_scripting.py' first?")