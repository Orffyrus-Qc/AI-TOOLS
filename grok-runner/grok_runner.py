import time
import subprocess
import os
from pathlib import Path
from datetime import datetime
import random

# ====================== CONFIGURATION ======================
QUEUE_DIR = r"W:\__grok_queue"
POLL_INTERVAL = 0.8  # seconds
# ===========================================================

def ensure_queue_folder():
    """Create the queue folder if it doesn't exist."""
    os.makedirs(QUEUE_DIR, exist_ok=True)

def get_next_command_file():
    """Return the oldest command file in the queue (or None)."""
    files = list(Path(QUEUE_DIR).glob("*.txt"))
    if not files:
        return None
    # Sort by filename (we use sortable timestamp names)
    files.sort(key=lambda p: p.name)
    return files[0]

def launch_batch(batch_path: str):
    if not Path(batch_path).exists():
        print(f"[Runner] ERROR: File not found -> {batch_path}")
        return

    print(f"[Runner] Launching in new window: {batch_path}")
    title = f"Grok - {Path(batch_path).name}"
    cmd = f'start "{title}" cmd /k "{batch_path}"'
    subprocess.Popen(cmd, shell=True)
    print(f"[Runner] Launched successfully.")

def process_command_file(file_path: Path):
    """Read and execute a command file, then delete it."""
    try:
        content = file_path.read_text(encoding="utf-8").strip()
        
        if content.startswith("RUN:"):
            batch_path = content[4:].strip()
            if batch_path:
                launch_batch(batch_path)
        
        # Delete the command file after processing
        file_path.unlink(missing_ok=True)
        
    except Exception as e:
        print(f"[Runner] Failed to process {file_path.name}: {e}")
        # Try to remove bad file so it doesn't block the queue
        try:
            file_path.unlink(missing_ok=True)
        except:
            pass

# ====================== MAIN ======================

os.system('title Grok Persistent Runner')

print("=== Grok Persistent Runner (Queue Mode) ===")
print("This window must stay open.")
print(f"Watching queue folder: {QUEUE_DIR}")
print("You can now send multiple commands. They will be processed in order.\n")

ensure_queue_folder()

while True:
    try:
        cmd_file = get_next_command_file()
        
        if cmd_file:
            print(f"[Runner] Found command: {cmd_file.name}")
            process_command_file(cmd_file)
        else:
            # No commands right now
            pass
        
        time.sleep(POLL_INTERVAL)
        
    except KeyboardInterrupt:
        print("\n[Runner] Shutting down...")
        break
    except Exception as e:
        print(f"[Runner] Unexpected error: {e}")
        time.sleep(2)
