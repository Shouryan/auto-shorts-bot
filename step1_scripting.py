import os
import random
import google.generativeai as genai
from datetime import datetime

def generate_content():
    print("--- Step 1: Generating High-CPM Niche Script ---")
    
    # 1. Setup API
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ Error: GEMINI_API_KEY is missing.")
        return

    genai.configure(api_key=api_key)
    
    # Use the smart, high-limit model
    MODEL_NAME = "gemini-1.5-flash" 
    
    # --- 2. DEFINE YOUR HIGH-CPM NICHES ---
    niches = [
        {
            "category": "Tech Nostalgia",
            "prompt": "Write a viral YouTube Short script about the history of a classic tech product (like Java, Windows XP, the first iPhone, or Nokia 3310). Focus on a surprising fact or its rise and fall."
        },
        {
            "category": "Failed Tech",
            "prompt": "Write a script about a famous failed tech product (like Google Glass, Segway, or Quibi). Explain ONE specific reason why it failed in a dramatic way."
        },
        {
            "category": "Grammar Tips",
            "prompt": "Explain a common grammar mistake people make (like 'Your vs You're', 'Could care less', or 'Literally'). Be snarky and educational."
        },
        {
            "category": "Explained in 60s",
            "prompt": "Explain a complex topic (like 5G, Blockchain, or HTTP) simply in under 60 seconds. Use an analogy."
        }
    ]
    
    # Pick one category at random for today
    selected_niche = random.choice(niches)
    print(f"🎯 Today's Niche: {selected_niche['category']}")

    try:
        model = genai.GenerativeModel(MODEL_NAME)
        
        # 3. Construct the Master Prompt
        full_prompt = f"""
        You are a YouTube Shorts scriptwriter for a high-tech educational channel.
        
        Task: {selected_niche['prompt']}
        
        Rules:
        1. Length: STRICTLY under 130 words.
        2. Hook: Start with a question or a bold statement.
        3. Style: Fast-paced, informative, no fluff.
        4. Format: Return ONLY the script text. Do not add "Title:" or "Scene 1".
        
        Crucial: At the very end, on a new line, write an image generation prompt for this specific topic starting with "IMAGE_PROMPT:".
        The image prompt should be: "A high quality, cinematic, 8k illustration of [Topic], cyberpunk or minimal style".
        """
        
        print(f"🤖 Asking {MODEL_NAME} to write script...")
        response = model.generate_content(full_prompt)
        text_output = response.text
        
        print("✅ Script Generated!")

    except Exception as e:
        print(f"\n⚠️ API ERROR: {e}")
        # Fallback script just in case
        text_output = (
            "Did you know the first computer bug was an actual moth? "
            "In 1947, Grace Hopper found a moth stuck in a relay of the Mark II computer. "
            "That is why we call coding errors 'bugs' today! "
            "\nIMAGE_PROMPT: A vintage computer schematic with a moth insect inside, retro tech style"
        )

    # 4. Save to File
    with open("daily_script.txt", "w", encoding="utf-8") as f:
        f.write(text_output)
    
    print("💾 Saved to daily_script.txt")

if __name__ == "__main__":
    generate_content()