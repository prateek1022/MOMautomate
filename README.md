# AI Meeting Summarizer for Teams

Stop drowning in meeting minutes. AI Meeting Summarizer for Teams is your personal assistant that listens to your meetings, provides a highly accurate transcript, and generates a smart summary delivered straight to your inbox. Focus on the conversation, not the note-taking.

## ✨ Core Features

-   **🎤 Crystal-Clear Transcription:** Powered by OpenAI's state-of-the-art Whisper model for industry-leading speech-to-text accuracy across multiple languages.

-   **🧠 AI-Powered Summaries:** Goes beyond simple transcription to provide intelligent, concise summaries of key points, decisions, and action items.

-   **📧 Automated Workflow:** Seamlessly integrates into your workflow by automatically preparing and sending summaries via email to all stakeholders.

## 🚀 Getting Started: Command Guide

Follow these steps in your terminal to get the AI Meeting Summarizer up and running.

```bash
# 1. Clone the AI Meeting Summarizer repository from GitHub
# Replace <your-repo-url> with the actual URL of your repository
git clone <your-repo-url>
cd whisper-project

# 2. Create a dedicated Python virtual environment
python -m venv venv

# 3. Activate the virtual environment (command for Windows)
venv\Scripts\activate

# 4. Install all the required Python libraries
pip install -r requirements.txt

# 5. Clone the OpenAI Whisper source code
# This is required for the packaging step to work correctly.
git clone https://github.com/openai/whisper.git whisper

# 6. Run the Summarizer!
# Replace "path/to/your/audio.mp3" with the actual file path.
python main.py "path/to/your/audio.mp3"
```

## 📦 Packaging for Distribution

Ready to share your AI assistant? You can package the entire application into a single executable file using PyInstaller. This allows it to run on other machines without requiring a Python installation.

1.  **Install PyInstaller:**
    ```bash
    pip install pyinstaller
    ```

2.  **Run the Build Command:**
    This command bundles your code, the AI models, and all dependencies into one file.
    ```bash
    pyinstaller --onefile --console --add-data "ffmpeg/bin/ffmpeg.exe;ffmpeg/bin" --collect-all whisper --collect-all torch --name transcribe_ap main.py
    ```