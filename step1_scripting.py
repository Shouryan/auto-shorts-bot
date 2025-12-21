import feedparser
import google.generativeai as genai
import os
import requests
import urllib.parse
from dotenv import load_dotenv

# 1. Load API Key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ Error: API Key not found.")
    exit()

genai.configure(api_key=api_key)

# 2. Function to get Sports News
def get_latest_sports_news():
    rss_url = "https://news.google.com/rss/search?q=sports+when:1d&hl=en-US&gl=US&ceid=US:en"
    print(f"🔍 Fetching news from: {rss_url}...")
    feed = feedparser.parse(rss_url)
    
    if len(feed.entries) > 0:
        top_story = feed.entries[0]
        print(f"✅ Found Top Story: {top_story.title}")
        return top_story.title, top_story.link
    else:
        return None, None

# 3. Generate Script AND Image Prompt
def generate_content(news_headline):
    model = genai.GenerativeModel('gemini-2.5-flash') 
    
    # We ask for TWO things: The script, and a visual description
    prompt = f"""
    You are a sports content generator.
    Headline: "{news_headline}"
    
    OUTPUT FORMAT (Strictly separate with '|||'):
    [Viral Script]|||[Image Prompt]
    
    1. Viral Script:
       - 30-second high-energy script for Gen Z.
       - Detect the sport (NBA, Cricket, Football, WWE, Golf,Tennis etc).
       - Start with a loud hook.
       - End with a question.
       - Max 60 words. No intro/outro labels.
    
    2. Image Prompt:
       - A short, vivid description of an image to represent this news.
       - High quality, 8k, hyper-realistic, dramatic lighting.
       - Example: "Cristiano Ronaldo looking shocked on a soccer field, dramatic stadium lighting, hyper-realistic, 8k"
    """
    
    print("🧠 Generating script & image prompt with Gemini...")
    response = model.generate_content(prompt)
    
    if "|||" in response.text:
        script_text, image_prompt = response.text.split("|||")
        return script_text.strip(), image_prompt.strip()
    else:
        # Fallback if AI messes up formatting
        return response.text.strip(), f"Sports stadium scene related to {news_headline}, hyper-realistic"

# 4. Generate the actual Image (Free Method)
def download_image(prompt, filename="topic_image.png"):
    print(f"🎨 Generating image for: '{prompt}'...")
    
    # URL Encode the prompt
    encoded_prompt = urllib.parse.quote(prompt)
    
    # Use Pollinations.ai (Free, no key needed)
    # We request a vertical-ish or square aspect ratio
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1080&height=1080&model=flux"
    
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"🖼️ Image saved to '{filename}'")
        else:
            print("❌ Failed to download image.")
    except Exception as e:
        print(f"❌ Error downloading image: {e}")

# --- Main Execution ---
if __name__ == "__main__":
    headline, link = get_latest_sports_news()
    
    if headline:
        # 1. Generate Text Content
        script, image_description = generate_content(headline)
        
        print("\n" + "="*40)
        print("📜 SCRIPT:")
        print(script)
        print("-" * 20)
        print("🎨 IMAGE PROMPT:")
        print(image_description)
        print("="*40)
        
        # 2. Save Script
        with open("daily_script.txt", "w", encoding="utf-8") as f:
            f.write(script)
        print("💾 Script saved to 'daily_script.txt'")
        
        # 3. Generate Image
        download_image(image_description, "topic_image.png")
        
    else:
        print("❌ No news found today.")