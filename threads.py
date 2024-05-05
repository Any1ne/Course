import threading
import subprocess
import time
import json
import os

# Define functions for animation generation and configuration update (replace with your actual logic)
def generate_animation(config_file, animation_dir, file_path):
    subprocess.call(["ffmpeg", "-i", config_file, "-o", file_path])

def update_config(config_file):
    with open(config_file, "r") as f:
        config = json.load(f)
    config["iteration"] += 1
    with open(config_file, "w") as f:
        json.dump(config, f)

class AnimationThread(threading.Thread):
    def __init__(self, config_file, animation_dir, stop_event):
        super().__init__()
        self.config_file = config_file
        self.animation_dir = animation_dir
        self.stop_event = stop_event

    def run(self):
        while not self.stop_event.is_set():
            for i in range(10):  # Simulate 10 iterations
                file_path = os.path.join(self.animation_dir, f"animation_{i}.mp4")
                generate_animation(self.config_file, file_path)

                # Write file path to PMFL.txt
                with open("PMFL.txt", "a") as f:
                    f.write(f"{file_path}\n")

                # Update configuration for next iteration
                update_config(self.config_file)

                # Sleep for a short interval before next iteration
                time.sleep(1)

class FileMonitoringThread(threading.Thread):
    def __init__(self, animation_dir, stop_event):
        super().__init__()
        self.animation_dir = animation_dir
        self.stop_event = stop_event
        self.processed_files = set()  # To track processed files

    def run(self):
        while not self.stop_event.is_set():
            # Read new entries from PMFL.txt
            with open("PMFL.txt", "r") as f:
                lines = f.readlines()

            for line in lines:
                file_path = line.strip()

                # Check if file has already been processed
                if file_path in self.processed_files:
                    continue

                # Process newly found file path (e.g., play or analyze animation)
                print(f"Processing animation file: {file_path}")

                # Add file to processed_files to prevent duplicate processing
                self.processed_files.add(file_path)

            # Sleep for a short interval before checking PMFL.txt again
            time.sleep(2)
