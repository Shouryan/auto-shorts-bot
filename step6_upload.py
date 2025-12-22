import os
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

# PERMISSIONS
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def authenticate():
    print("--- Authenticating with YouTube ---")
    creds = None
    
    # 1. Load from file
    if os.path.exists("token.json"):
        print("   Found token.json. Verifying validity...")
        try:
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        except Exception as e:
            print(f"   ⚠️ Error reading token.json: {e}")
            creds = None

    # 2. Check Validity
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("   Token is expired. Attempting silent refresh...")
            try:
                creds.refresh(Request())
                print("   ✅ Refresh successful!")
            except Exception as e:
                print(f"   ❌ Refresh FAILED: {e}")
                print("   The 'refresh_token' might be revoked or invalid.")
                creds = None
        else:
            print("   Token is missing or invalid.")

    # 3. IF STILL NO CREDS -> FAIL (Don't open browser on Server)
    if not creds or not creds.valid:
        print("\n❌ CRITICAL AUTH ERROR:")
        print("   We do not have valid credentials, and we cannot open a browser on GitHub Actions.")
        print("   ACTION REQUIRED: Regenerate your 'token.json' locally and update GitHub Secrets.")
        # Raise error to stop the bot
        raise RuntimeError("Authentication Failed: No valid token available.")
    
    # 4. Build Service
    print("   ✅ Authentication Complete. Building YouTube Service...")
    return googleapiclient.discovery.build("youtube", "v3", credentials=creds)

def upload_video(file_path, title="Automated Short", description="Created by AI"):
    youtube = authenticate()
    
    print(f"--- Uploading: {file_path} ---")
    
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": ["shorts", "ai", "automation"],
            "categoryId": "22" # People & Blogs
        },
        "status": {
            "privacyStatus": "private", # Always start private!
            "selfDeclaredMadeForKids": False
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
            print(f"   Uploaded {int(status.progress() * 100)}%...")
            
    print(f"✅ UPLOAD SUCCESS! Video ID: {response.get('id')}")

if __name__ == "__main__":
    # Ensure this matches your actual video filename
    VIDEO_FILE = "final_short_automated.mp4" 
    
    if os.path.exists(VIDEO_FILE):
        upload_video(VIDEO_FILE, title="Daily AI Short", description="#shorts #ai")
    else:
        print(f"❌ Error: Video file '{VIDEO_FILE}' not found.")
