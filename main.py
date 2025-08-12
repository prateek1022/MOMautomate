import os
import shutil
import time
import subprocess
import sys
import json
from email_prompt import get_email_address
from summarize_request import summarize_meeting
from email_sender import send_email
from config import (
    WATCH_FOLDER, DEST_FOLDER, LOG_FOLDER, TRANSCRIBE_FOLDER, METADATA_FILE, log_file, log_message
)
import datetime

# Try importing required modules
try:
    import whisper
    import torch
except ImportError:
    print("[✘] ERROR: Required Python modules are missing. Install them using:\n    pip install whisper torch")
    sys.exit(1)

def log_message(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_message = f"[{timestamp}] {message}\n"
    with open(log_file, "a", encoding="utf-8") as log:
        log.write(full_message)
    print(full_message.strip())

def load_metadata():
    """Load the metadata file containing transcribed recordings."""
    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, "r", encoding="utf-8") as file:
            return set(json.load(file))
    return set()

def save_metadata(metadata):
    """Save the metadata file with transcribed recordings."""
    with open(METADATA_FILE, "w", encoding="utf-8") as file:
        json.dump(list(metadata), file, indent=4)

def initialize_metadata():
    """Initialize metadata with all existing files in the watch folder."""
    log_message("[INFO] Initializing metadata with existing files...")
    metadata = set()
    for file in os.listdir(WATCH_FOLDER):
        if file.endswith(".mp4") or file.endswith(".m4a"):
            full_path = os.path.join(WATCH_FOLDER, file)
            metadata.add(full_path)
    save_metadata(metadata)
    log_message("[INFO] Metadata initialized with existing files.")

def check_dependency(command, name):
    """Check if a dependency is available."""
    try:
        subprocess.run([command, "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        log_message(f"[✔] {name} is installed and working.")
    except Exception as e:
        log_message(f"[✘] ERROR: {name} is missing or not found! {e}")
        sys.exit(1)

def setup_ffmpeg():
    """Ensure FFmpeg is installed and accessible inside the packaged EXE."""
    
    if getattr(sys, 'frozen', False):
        # Running inside PyInstaller bundle
        ffmpeg_path = os.path.join(sys._MEIPASS, "ffmpeg/bin/ffmpeg.exe")
    else:
        # Running normally in Python environment
        ffmpeg_path = os.path.abspath("ffmpeg/bin/ffmpeg.exe")

    if not os.path.exists(ffmpeg_path):
        log_message(f"[✘] ERROR: FFmpeg not found at {ffmpeg_path}! Ensure it is packaged correctly.")
        sys.exit(1)

    # Log success
    log_message(f"[✔] FFmpeg found at {ffmpeg_path}")

    # Set environment variable so Whisper uses this FFmpeg
    os.environ["FFMPEG_BINARY"] = ffmpeg_path
    os.environ["PATH"] = os.path.dirname(ffmpeg_path) + os.pathsep + os.environ["PATH"]

    return ffmpeg_path

def generate_timestamp_filename(original_file_path):
    """Generate a new filename with timestamp."""
    original_basename = os.path.basename(original_file_path)
    extension = os.path.splitext(original_basename)[1]
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{timestamp}{extension}"

def transcribe_audio(audio_path):
    """Main function to transcribe an audio file."""
    log_message(f"[INFO] Transcribing {audio_path}...")

    

    # Ensure FFmpeg is set up before running Whisper
    ffmpeg_path = setup_ffmpeg()
    log_message(f"[INFO] Using FFmpeg: {ffmpeg_path}")

    # Set FFmpeg for Whisper explicitly
    os.environ["PATH"] = os.path.dirname(ffmpeg_path) + os.pathsep + os.environ["PATH"]
    log_message("[✔] Updated system PATH for FFmpeg")

    # Load Whisper model
    try:
        model = whisper.load_model("small")
        log_message("[✔] Whisper model loaded successfully.")
    except Exception as e:
        log_message(f"[✘] ERROR: Failed to load Whisper model! {e}")
        return

    # Ensure the audio file exists
    if not os.path.exists(audio_path):
        log_message(f"[✘] ERROR: '{audio_path}' not found!")
        return

    # Transcribe the audio
    try:
        result = model.transcribe(audio_path)
        log_message(f"[SUCCESS] Transcribed {audio_path}: {result['text']}")

        # Save the transcription to a text file
        save_transcription(audio_path, result['text'])

    except Exception as e:
        log_message(f"[✘] ERROR: Failed to transcribe {audio_path}. {e}")

def save_transcription(audio_path, transcription):
    """Save the transcription to a text file."""
    file_name = os.path.splitext(os.path.basename(audio_path))[0] + ".txt"
    transcription_path = os.path.join(TRANSCRIBE_FOLDER, file_name)

    try:
        with open(transcription_path, "w", encoding="utf-8") as file:
            file.write(transcription)
        log_message(f"[SUCCESS] Transcription saved to {transcription_path}")
        summary = summarize_meeting(transcription)
        log_message(f"[SUCCESS] Meeting Summary:\n{summary}")
        send_email("Meeting Summary", summary)
    except Exception as e:
        log_message(f"[✘] ERROR: Failed to save transcription to {transcription_path}. {e}")

def process_file(file_path):
    """Processes a new file by renaming with timestamp, copying and transcribing it."""
    log_message(f"[INFO] New file detected: {file_path}")

    # Load metadata to check if the file has already been processed
    metadata = load_metadata()
    if file_path in metadata:
        log_message(f"[INFO] File already processed: {file_path}")
        return

    # Generate timestamp filename
    timestamp_filename = generate_timestamp_filename(file_path)
    dest_path = os.path.join(DEST_FOLDER, timestamp_filename)
    
    log_message(f"[INFO] Will save as: {timestamp_filename}")

    for attempt in range(5):  # Retry up to 5 times
        try:
            shutil.copy2(file_path, dest_path)
            log_message(f"[SUCCESS] Copied with timestamp: {file_path} -> {dest_path}")

            # Call the transcription function
            transcribe_audio(dest_path)

            # Update metadata after successful transcription
            metadata.add(file_path)
            save_metadata(metadata)

            break  # Exit loop if successful
        except Exception as e:
            log_message(f"[ERROR] Attempt {attempt + 1}: Failed to process {file_path}: {e}")
            time.sleep(2)  # Wait 2 seconds before retrying
    else:
        log_message(f"[ERROR] Giving up on processing {file_path}")

def poll_for_new_files():
    """Continuously checks for new files in the OneDrive folder."""
    processed_files = load_metadata()

    while True:
        try:
            files = os.listdir(WATCH_FOLDER)

            for file in files:
                if file.endswith(".mp4") or file.endswith(".m4a"):
                    full_path = os.path.join(WATCH_FOLDER, file)

                    # Ignore already processed files
                    if full_path in processed_files:
                        continue

                    # Ensure the file is fully written before processing
                    time.sleep(5)

                    process_file(full_path)
                    processed_files.add(full_path)

            time.sleep(10)  # Check every 10 seconds
        except Exception as e:
            log_message(f"[ERROR] Error during polling: {e}")
            time.sleep(30)  # Wait longer if there's an error

if __name__ == "__main__":
    # Prompt for email address if not already set
    get_email_address()

    log_message(f"[INFO] Starting file processor")
    log_message(f"[INFO] Monitoring folder: {WATCH_FOLDER}")
    log_message(f"[INFO] Destination folder: {DEST_FOLDER}")

    # Initialize metadata with existing files
    initialize_metadata()

    try:
        # Run polling in the main thread
        poll_for_new_files()
    except KeyboardInterrupt:
        log_message("[INFO] Stopping file monitoring...")
        log_message("[INFO] File monitoring stopped.")