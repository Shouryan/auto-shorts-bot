import subprocess
import time
import sys
import os
# --- DEBUG PATHS ---
print(f"DEBUG: Script is running in: {os.getcwd()}")
if os.path.exists("token.json"):
    print(f"DEBUG: ✅ Found 'token.json' in this folder. Size: {os.path.getsize('token.json')} bytes")
else:
    print("DEBUG: ❌ 'token.json' NOT FOUND in this folder!")
    print("DEBUG: Listing all files here:", os.listdir())
# -------------------
def run_step(script_name, step_description):
    print(f"\n{'='*60}")
    print(f"🎬 STARTING: {step_description} ({script_name})")
    print(f"{'='*60}")
    
    # 1. Verify file exists
    if not os.path.exists(script_name):
        print(f"❌ CRITICAL ERROR: File '{script_name}' not found in {os.getcwd()}")
        sys.exit(1)

    try:
        # 2. Run the script and STREAM the output to the console live
        # We explicitly do NOT capture output so it flows directly to stdout
        process = subprocess.run(
            [sys.executable, "-u", script_name], # "-u" forces unbuffered binary stdout
            check=True,
            capture_output=False,  # This ensures logs print to the main console
            text=True
        )
        
        print(f"✅ COMPLETED: {step_description}")
        time.sleep(2) 
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ CRITICAL ERROR in {script_name}. Stopping execution.")
        sys.exit(1)

def main():
    print("🚀 STARTING AUTOMATED YOUTUBE SHORTS BOT 🚀")
    
    # 1. Content Generation
    run_step("step1_scripting.py", "Generating Script & Image")
    
    # 2. Voiceover 
    run_step("step2_media.py", "Generating Voiceover")
    
    # 3. Assembly (Now with live logging!)
    run_step("step3_assembly.py", "Assembling Base Video")
    
    # 4. Captions 
    run_step("step5_captions.py", "Burning Captions")
    
    # 5. Upload
    run_step("step6_upload.py", "Uploading to YouTube")
    
    print("\n" + "="*60)
    print("🎉🎉 JOB DONE! VIDEO IS LIVE (Private) ON YOUTUBE! 🎉🎉")
    print("="*60)

if __name__ == "__main__":
    main()
