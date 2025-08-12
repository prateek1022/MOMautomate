
# Whisper Transcription and Summarization Project

AI Meeting Summarizer for Teams — a command-line tool that transcribes meeting audio with OpenAI’s Whisper, generates concise summaries, and automatically emails them to your inbox.

## Features

-   Transcribe audio files (MP3, WAV, etc.) to text.
-   Summarize the transcribed text.
-   Send the summary via email.

## Prerequisites

-   Python 3.9+
-   FFmpeg: The project includes the necessary FFmpeg binary. For development, you might need to have it installed and available in your system's PATH.

## Installation

1.  **Clone the project repository:**
    ```bash
    git clone <your-repo-url>
    cd whisper-project
    ```

2.  **Clone the OpenAI Whisper repository:**
    This project requires the source code of OpenAI's Whisper for packaging. Clone it into the project directory.
    ```bash
    # This will create a 'whisper' folder in your project directory
    git clone https://github.com/openai/whisper.git whisper
    ```

3.  **Create and activate a virtual environment:**
    ```bash
    # For Windows
    python -m venv venv
    venv\Scripts\activate
    ```

4.  **Install the required Python packages:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To run the application, execute the `main.py` script from the command line, passing the path to the audio file you want to process.

```bash
python main.py "path/to/your/audiofile.mp3"
```

## Packaging

This project uses PyInstaller to package the application into a single executable file. This bundles Python, your scripts, and all necessary libraries and data files into one file for easy distribution.

### How to Package

1.  **Install PyInstaller:**
    ```bash
    pip install pyinstaller
    ```

2.  **Run the packaging command:**

    The following command will create a single, console-based executable named `transcribe_ap.exe` in the `dist` directory.

    ```bash
    pyinstaller --onefile --console --add-data "ffmpeg/bin/ffmpeg.exe;ffmpeg/bin" --collect-all whisper --collect-all torch --name transcribe_ap main.py
    ```

### Command Breakdown

-   `--onefile`: Creates a single executable file.
-   `--console`: Creates a console-based application (no GUI).
-   `--add-data "ffmpeg/bin/ffmpeg.exe;ffmpeg/bin"`: Bundles the `ffmpeg.exe` binary. The path after the semicolon tells PyInstaller to put it in the `ffmpeg/bin` directory inside the package.
-   `--collect-all whisper`: Finds and includes all necessary files from the `whisper` library.
-   `--collect-all torch`: Finds and includes all necessary files from the `torch` library.
-   `--name transcribe_ap`: Sets the name of the final executable.
-   `main.py`: The main entry point of the application.
# MOMautomate
