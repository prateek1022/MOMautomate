# config.py
import os
import datetime

# Base Directory
BASE_DIR = r"C:\MOMautomate"

# Directories
USER_HOME = os.path.expanduser("~")
WATCH_FOLDER = os.path.join(USER_HOME, "OneDrive - IBM", "Recordings")
DEST_FOLDER = os.path.join(BASE_DIR, "temp")
LOG_FOLDER = os.path.join(BASE_DIR, "log")
TRANSCRIBE_FOLDER = os.path.join(BASE_DIR, "transcribes")
DATA_FOLDER = os.path.join(BASE_DIR, "data")
METADATA_FILE = os.path.join(LOG_FOLDER, "transcribed_recordings.json")
EMAIL_FILE = os.path.join(DATA_FOLDER, "email.json")

# Ensure necessary folders exist
os.makedirs(DEST_FOLDER, exist_ok=True)
os.makedirs(LOG_FOLDER, exist_ok=True)
os.makedirs(TRANSCRIBE_FOLDER, exist_ok=True)
os.makedirs(DATA_FOLDER, exist_ok=True)

# Log file path
log_file = os.path.join(LOG_FOLDER, f"{datetime.date.today()}.txt")



# Email Configuration
SENDER_EMAIL = "yoursummarizer@gmail.com"
# Email Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def log_message(message):
    """Log a message to the log file with a timestamp."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_message = f"[{timestamp}] {message}\n"
    with open(log_file, "a", encoding="utf-8") as log:
        log.write(full_message)
    print(full_message.strip())
