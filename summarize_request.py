import os
import requests
import datetime
from config import GROQ_API_KEY, LOG_FOLDER, log_file, log_message

def summarize_meeting(transcript):
    """Summarize the meeting transcript using the Groq API and return the summary text."""
    url = "https://api.groq.com/openai/v1/chat/completions"  # Correct Groq API URL
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    # Define the system role prompt
    system_role_prompt = (
        "You are an advanced AI meeting summarizer. Your task is to read and analyze meeting transcriptions "
        "and generate a clear, structured summary in bullet points.\n\n"
        "- Extract only key points, important decisions, action items, and any critical discussions.\n"
        "- Do NOT include small talk, filler words, repeated statements, or off-topic discussions.\n"
        "- Only include information that is explicitly mentioned in the transcript.\n"
        "- If any section (e.g., meeting date, participants) is missing, do NOT mention it in the summary.\n"
        "- Use clear and concise language while preserving essential details.\n"
        "- Maintain a structured format with simple bullet points.\n"
    )

    # Define the user role prompt
    user_role_prompt = (
        "Here is a meeting transcript:\n\n"
        "{transcript}\n\n"
        "Please summarize this meeting transcript in bullet points using the following structure:\n"
        "- Meeting Date & Time (only if available)\n"
        "- Participants (only if mentioned)\n"
        "- Key Discussion Points\n"
        "- Decisions Made\n"
        "- Action Items & Responsibilities (who needs to do what?)\n"
        "- Next Steps or Follow-ups (future meetings, deadlines, etc.)\n\n"
        "Ensure that:\n"
        "- You only include available information from the transcript.\n"
        "- You do NOT mention missing details (e.g., do not write 'Meeting Date: Not Available').\n"
        "- The output is structured and formatted clearly with bullet points.\n"
        "- No unnecessary notes, explanations, or disclaimers are included—just the summary.\n"
    ).format(transcript=transcript)

    data = {
        "model": "llama-3.3-70b-versatile",  # Model from your cURL request
        "messages": [
            {"role": "system", "content": system_role_prompt},
            {"role": "user", "content": user_role_prompt}
        ]
    }

    log_message("Sending request to Groq API for summarization.")

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        result = response.json()["choices"][0]["message"]["content"]
        log_message(f"Successfully received summary from Groq API:\n{result}")
        return result  # Return the summary text
    else:
        error_message = f"Error {response.status_code}: {response.text}"
        log_message(error_message)
        raise Exception(error_message)  # Raise an exception on error

# Example usage (for testing purposes)
if __name__ == "__main__":
    meeting_transcript = input("💬 Enter the meeting transcript: ")  # Take transcript input
    try:
        summary = summarize_meeting(meeting_transcript)  # Call the summarizer function
        print("\n📝 Meeting Summary:\n", summary)  # Print the summary
    except Exception as e:
        log_message(f"Failed to summarize meeting: {e}")
