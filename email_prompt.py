import os
import json
import tkinter as tk
from tkinter import simpledialog
from config import EMAIL_FILE  # Import the correct file location

def get_email_address(silent=False):
    """Get the email address from config file or prompt the user via a dialog box."""
    
    # Check if email config file exists
    if os.path.exists(EMAIL_FILE):
        with open(EMAIL_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                email = data.get("email", "").strip()
                if email:
                    return email
            except json.JSONDecodeError:
                pass  # If file is corrupt, prompt again

    # If silent mode is enabled, return an empty string
    if silent:
        return ""

    # Create a Tkinter root window (hidden)
    root = tk.Tk()
    root.withdraw()  # Hide the main Tkinter window

    # Show input dialog
    email = simpledialog.askstring("Email Input", "Enter your email for transcription summaries:")

    if email:
        # Save email to JSON file
        with open(EMAIL_FILE, "w", encoding="utf-8") as f:
            json.dump({"email": email}, f, indent=4)

    return email
