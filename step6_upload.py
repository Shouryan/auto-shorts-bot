import os
import sys
import googleapiclient.discovery
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

# NOTE: We removed 'InstalledAppFlow' so it is IMPOSSIBLE to open a browser.

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def authenticate():
    print("--- Authenticating (Server Mode) ---")

    # 1. FAIL FAST if token is missing
    if not os.path.exists("token.json"):
        print("❌ CRITICAL ERROR: 'token.json' file is missing on the server.")
        print("   Did you add the YOUTUBE_TOKEN_JSON secret to GitHub?")
        sys.exit(1)

    try:
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    except Exception as e:
        print(f"❌ JSON ERROR: 'token.json' is corrupted. {e}")
        sys.exit(1)

    # 2. Refresh if expired
    if not creds.valid:
        if creds.expired and creds.refresh_token:
            print("   ⏳ Token expired. Refreshing...")
            try:
                creds.refresh(Request())
                print("   ✅ Refreshed successfully.")
            except Exception as e:
                print(f"   ❌ REFRESH FAILED: {e}")
                print("   Your refresh_token is invalid. Generate a new one locally.")
                sys.exit(1)
        else:
            print("   ❌ TOKEN INVALID: No refresh_token found.")
            sys.exit(1)

    return googleapiclient.discovery.build("youtube", "v3", credentials=creds)

def upload_video(file_path):
    try:
        youtube = authenticate()
        print(f"--- Uploading: {file_path} ---")

        body = {
            "snippet": {
                "title": "Daily AI Short 🤖",
                "description": "Automated upload. #shorts #ai",
                "tags": ["shorts", "ai"],
                "categoryId": "22"
            },
            "status": {
                "privacyStatus": "public", 
                "selfDeclaredMadeForKids": False
            }
        }

        media = MediaFileUpload(file_path, chunksize=-1, resumable=True)
        request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"   Uploading... {int(status.progress() * 100)}%")

        print(f"✅ UPLOAD SUCCESS! Video ID: {response.get('id')}")

    except Exception as e:
        print(f"❌ UPLOAD CRASHED: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Make sure this matches your actual video file name
    if os.path.exists("final_short_automated.mp4"):
        upload_video("final_short_automated.mp4")
    else:
        print("❌ Video file not found.")
