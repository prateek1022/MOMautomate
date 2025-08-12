import os
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
from config import EMAIL_FILE, LOG_FOLDER, log_file, log_message, SENDER_EMAIL, SENDER_PASSWORD, SMTP_SERVER, SMTP_PORT

def get_email_address():
    """Retrieve the email address from the JSON file."""
    try:
        if os.path.exists(EMAIL_FILE):
            with open(EMAIL_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
                if data.get("email"):
                    return data["email"]
    except (json.JSONDecodeError, FileNotFoundError, KeyError) as e:
        log_message(f"Error reading email file: {e}")
    return None

def send_email(subject, body):
    """Send an email with the given subject and body to the email address in the JSON file."""
    recipient_email = get_email_address()

    if not recipient_email:
        log_message("No recipient email found. Email not sent.")
        return

    # Set up the MIME
    message = MIMEMultipart()
    message["From"] = SENDER_EMAIL
    message["To"] = recipient_email
    message["Subject"] = subject

    # Attach the greeting + summary in the email body
    email_body = f"""Hello,

Here is the summary of your meeting:

{body}

Regards,
MOMautomate Team"""

    message.attach(MIMEText(email_body, "plain"))

    try:
        # Connect with the server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        text = message.as_string()
        server.sendmail(SENDER_EMAIL, recipient_email, text)
        server.quit()
        log_message(f"Email sent successfully to {recipient_email}")
    except Exception as e:
        log_message(f"Failed to send email: {e}")

if __name__ == "__main__":
    # Example usage
    summary_text = "This is the summarized meeting text."  # Replace with actual summary
    send_email("Meeting Summary", summary_text)
