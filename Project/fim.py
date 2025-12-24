import hashlib
import os
import time

# --- CONFIGURATION ---
# Folder to monitor
MONITORED_DIR = "monitored_files" 
# File to store the baseline hashes
BASELINE_FILE = "baseline.txt"

def calculate_sha256(filepath):
    """Calculates the SHA-256 hash of a given file."""
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception:
        return None

def create_baseline():
    """Initializes the baseline hash database for files in the target directory."""
    print("Initialization: Creating baseline hashes...")
    if not os.path.exists(MONITORED_DIR):
        os.makedirs(MONITORED_DIR)
        print(f"Created directory: {MONITORED_DIR}. Please add files and restart the script.")
        return

    files = os.listdir(MONITORED_DIR)
    with open(BASELINE_FILE, "w") as f:
        for filename in files:
            filepath = os.path.join(MONITORED_DIR, filename)
            if os.path.isfile(filepath):
                file_hash = calculate_sha256(filepath)
                f.write(f"{filepath}|{file_hash}\n")
    print("Baseline successfully saved.")

def monitor():
    """Monitors files and compares their current hashes against the baseline."""
    if not os.path.exists(BASELINE_FILE):
        create_baseline()

    # Load baseline into memory
    baseline = {}
    if os.path.exists(BASELINE_FILE):
        with open(BASELINE_FILE, "r") as f:
            for line in f:
                parts = line.strip().split("|")
                if len(parts) == 2:
                    path, file_hash = parts
                    baseline[path] = file_hash

    print("Monitoring started... (Press Ctrl+C to stop)")
    
    try:
        while True:
            time.sleep(1) # Check every second
            if not os.path.exists(MONITORED_DIR):
                continue

            current_files = os.listdir(MONITORED_DIR)
            
            for filename in current_files:
                filepath = os.path.join(MONITORED_DIR, filename)
                
                if os.path.isfile(filepath):
                    current_hash = calculate_sha256(filepath)

                    # Detection of a new file
                    if filepath not in baseline:
                        print(f"[ALERT] NEW FILE DETECTED: {filepath}")
                        baseline[filepath] = current_hash
                    
                    # Detection of a modified file
                    elif current_hash != baseline[filepath]:
                        print(f"[ALERT] FILE MODIFIED: {filepath}")
                        baseline[filepath] = current_hash
                        
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")

if __name__ == "__main__":
    monitor()