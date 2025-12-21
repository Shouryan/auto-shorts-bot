import os
import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# SCOPES tells Google what we want to do (Manage YouTube account)
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def authenticate_youtube():
    """Authenticates the user and returns the YouTube API service."""
    print("--- Authenticating with YouTube ---")
    
    # This will open a browser window for you to log in the first time
    flow = InstalledAppFlow.from_client_secrets_file(
        "client_secrets.json", SCOPES
    )
    credentials = flow.run_local_server(port=0)
    
    return build("youtube", "v3", credentials=credentials)

def upload_video(youtube, file_path, title, description, tags, category_id="17"):
    """Uploads a video to YouTube."""
    print(f"🚀 Uploading {file_path}...")

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": category_id  # 17 = Sports
        },
        "status": {
            "privacyStatus": "private", # Change to "public" when ready!
            "selfDeclaredMadeForKids": False,
        }
    }

    media = MediaFileUpload(file_path, chunksize=-1, resumable=True)

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploaded {int(status.progress() * 100)}%")

    print(f"✅ Upload Complete! Video ID: {response.get('id')}")
    return response.get('id')

if __name__ == "__main__":
    # --- CONFIGURATION ---
    VIDEO_FILE = "final_short_automated.mp4" # Ensure this matches your final output
    
    # We can read the script file to use as the description
    DESCRIPTION = "Automated Sports News #Shorts #Sports"
    if os.path.exists("daily_script.txt"):
        with open("daily_script.txt", "r") as f:
            DESCRIPTION = f.read() + "\n\n#Shorts #SportsNews"

    TITLE = "Breaking Sports News! 🚨 #Shorts" # You can make this dynamic later
    TAGS = ["Sports", "News", "Shorts", "Viral"]

    # 1. Authenticate
    try:
        youtube_service = authenticate_youtube()
        
        # 2. Upload
        if os.path.exists(VIDEO_FILE):
            upload_video(youtube_service, VIDEO_FILE, TITLE, DESCRIPTION, TAGS)
        else:
            print(f"❌ Error: Video file '{VIDEO_FILE}' not found.")
            
    except Exception as e:
        print(f"❌ Upload Failed: {e}")