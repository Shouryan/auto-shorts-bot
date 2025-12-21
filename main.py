import subprocess
import time
import sys
import os

def run_step(script_name, step_description):
    print(f"\n{'='*60}")
    print(f"🎬 STARTING: {step_description} ({script_name})")
    print(f"{'='*60}")
    
    # 1. Verify file exists before trying to run it
    if not os.path.exists(script_name):
        print(f"❌ CRITICAL ERROR: File '{script_name}' not found in {os.getcwd()}")
        sys.exit(1)

    try:
        # 2. Use sys.executable to ensure we use the correct Python (venv)
        subprocess.run([sys.executable, script_name], check=True)
        print(f"✅ COMPLETED: {step_description}")
        time.sleep(2) 
        
    except subprocess.CalledProcessError:
        print(f"\n❌ CRITICAL ERROR in {script_name}. Stopping execution.")
        sys.exit(1)

def main():
    print("🚀 STARTING AUTOMATED YOUTUBE SHORTS BOT 🚀")
    
    # 1. Content Generation
    run_step("step1_scripting.py", "Generating Script & Image")
    
    # 2. Voiceover 
    run_step("step2_media.py", "Generating Voiceover")
    
    # 3. Assembly
    run_step("step3_assembly.py", "Assembling Base Video")
    
    # 4. Captions (Make sure this filename matches exactly!)
    # If you renamed it to step4_captions.py, update it here.
    # If it's still step5_captions.py, keep it as is.
    run_step("step5_captions.py", "Burning Captions")
    
    # 5. Upload
    run_step("step6_upload.py", "Uploading to YouTube")
    
    print("\n" + "="*60)
    print("🎉🎉 JOB DONE! VIDEO IS LIVE (Private) ON YOUTUBE! 🎉🎉")
    print("="*60)

if __name__ == "__main__":
    main()