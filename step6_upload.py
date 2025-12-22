import os
import sys
import googleapiclient.discovery
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

# SCOPES must match what you requested in Step 1
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def authenticate():
    print("--- Authenticating with YouTube (Server Mode) ---")
    
    # 1. Load the Token File
    if not os.path.exists("token.json"):
        print("❌ CRITICAL ERROR: 'token.json' not found.")
        print("   On GitHub, this means the 'Create Credentials' step failed.")
        sys.exit(1)

    try:
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    except Exception as e:
        print(f"❌ JSON ERROR: Could not read token.json. {e}")
        sys.exit(1)

    # 2. Check Validity & Refresh if needed
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("   ⏳ Token is expired. Refreshing now...")
            try:
                creds.refresh(Request())
                print("   ✅ Token refreshed successfully!")
            except Exception as e:
                print(f"   ❌ REFRESH FAILED: {e}")
                print("   The 'refresh_token' is invalid or revoked.")
                sys.exit(1)
        else:
            print("   ❌ AUTH ERROR: Token is invalid and has no refresh_token.")
            print("   You must generate a new 'token.json' locally with 'access_type=offline'.")
            sys.exit(1)

    print("   ✅ Authentication Valid. Building Service...")
    return googleapiclient.discovery.build("youtube", "v3", credentials=creds)

def upload_video(file_path, title="Daily AI Short", description="#shorts"):
    youtube = authenticate()
    
    print(f"--- Uploading: {file_path} ---")
    
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": ["shorts", "ai"],
            "categoryId": "22"
        },
        "status": {
            "privacyStatus": "private", 
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
            print(f"   Uploading... {int(status.progress() * 100)}%")
            
    print(f"✅ UPLOAD SUCCESS! Video ID: {response.get('id')}")

if __name__ == "__main__":
    # Ensure this filename matches your previous steps
    VIDEO_FILE = "final_short_automated.mp4" 
    
    if os.path.exists(VIDEO_FILE):
        upload_video(VIDEO_FILE)
    else:
        print(f"❌ Error: Video file '{VIDEO_FILE}' not found.")
        # Don't crash, just exit cleanly so logs are readable
        sys.exit(1)
