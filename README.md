# CareNota-Ai

> AI-powered medical transcription and clinical report generation system

## Overview

CareNota-Ai is a Python-based application that converts medical audio recordings into structured clinical reports in JSON format. It uses OpenAI's Whisper for speech-to-text transcription and Google's Gemini API for intelligent medical text processing and SOAP-formatted report generation.

The system supports both **Egyptian Arabic** and **English** inputs, making it adaptable for diverse healthcare settings.

## Key Features

- 🎙️ **Audio Transcription** - Converts medical audio recordings to text using OpenAI Whisper
- 🧠 **AI-Powered Processing** - Uses Google Gemini to clean, correct, and structure medical transcripts
- 📋 **SOAP Format Reports** - Generates professional clinical reports with doctor and patient summaries
- 🌍 **Multilingual Support** - Handles Egyptian Arabic and English transcriptions
- ⚙️ **Audio Preprocessing** - Automatically normalizes and optimizes audio for accurate transcription
- 🔄 **Two-Pass Processing** - First pass cleans the transcript, second pass extracts structured JSON

## How It Works

```
Audio File
    ↓
Audio Preprocessing (Normalization & Format Conversion)
    ↓
Whisper Transcription (Speech-to-Text)
    ↓
Arabic Reconstruction (Cleaning & Correction with Gemini)
    ↓
JSON Extraction (Structured Report Generation with Gemini)
    ↓
JSON Output (Doctor Summary + Patient Summary)
```

## Tech Stack

- **Language:** Python
- **Web Framework:** FastAPI
- **Speech Recognition:** OpenAI Whisper
- **LLM:** Google Gemini API (gemini-2.5-flash)
- **Audio Processing:** pydub, PyTorch
- **HTTP Client:** Requests

## Installation

### Prerequisites

- Python 3.8+
- pip (Python package installer)

### Setup

1. **Clone the repository:**
```bash
git clone https://github.com/Nadeenyakout/CareNota-Ai.git
cd CareNota-Ai
```

2. **Create a virtual environment (recommended):**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Create a `.env` file** with your API key:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

5. **Run the application:**
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### GET `/`

Health check endpoint.

**Response:**
```json
{
  "message": "API is running 🚀"
}
```

### POST `/process-audio`

Process a medical audio file and generate a structured clinical report.

**Request:**
```json
{
  "audio_url": "https://example.com/medical-recording.wav"
}
```

**Response:**
```json
{
  "doctor_summary": {
    "subjective": "Patient presents with complaint of persistent cough for 3 days...",
    "objective": "Vitals: BP 120/80, HR 88, RR 18. Physical Exam: Bilateral wheezing on auscultation...",
    "assessment": "Acute bronchitis",
    "plan": "1. Amoxicillin 500mg TID for 7 days\n2. Rest at home for 3 days\n3. Return if symptoms worsen"
  },
  "patient_summary": {
    "diagnosis": "Chest infection (bronchitis)",
    "symptoms": "Cough, wheezing when breathing",
    "treatment_plan": "Antibiotics for 7 days, rest at home",
    "when_to_seek_help": "If breathing becomes difficult or cough worsens",
    "follow_up": "Return if not improved after 7 days"
  }
}
```

## File Structure

```
CareNota-Ai/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── .env                   # Environment variables (not in repo)
├── .gitignore             # Git ignore file
└── ai/
    ├── __init__.py
    ├── pipeline.py         # Main processing pipeline
    ├── preprocessing.py    # Audio preprocessing and normalization
    ├── whisper_model.py    # Whisper transcription
    └── gemini.py          # Gemini API integration
```

## Processing Pipeline Details

### 1. Audio Preprocessing (`ai/preprocessing.py`)
- Converts audio to 16kHz mono
- Normalizes audio levels
- Exports as WAV format for Whisper compatibility

### 2. Transcription (`ai/whisper_model.py`)
- Uses OpenAI Whisper Base model
- Converts audio to text (supports Arabic and English)

### 3. Arabic Reconstruction (`ai/gemini.py` - `reconstruct_arabic()`)
- First Gemini pass: Cleans and corrects the transcript
- Fixes Whisper recognition errors
- Separates incorrectly connected words
- Corrects medical terminology

### 4. JSON Extraction (`ai/gemini.py` - `extract_json()`)
- Second Gemini pass: Structures the cleaned transcript
- Generates SOAP-formatted doctor summary
- Creates patient-friendly summary
- Handles language-appropriate output (Arabic/English)

### 5. JSON Parsing (`ai/gemini.py` - `safe_json_parse()`)
- Parses and validates JSON response
- Handles markdown formatting in responses

## Environment Variables

Create a `.env` file in the root directory:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

Obtain your Gemini API key from [Google AI Studio](https://aistudio.google.com/)

## Error Handling

The API returns error responses in the following format:

```json
{
  "error": "Error description message"
}
```

Common errors:
- Invalid audio file type (must be audio content-type)
- Network timeout (15 second limit for file download)
- Missing or invalid GEMINI_API_KEY
- Invalid JSON parsing

## Notes

- Audio file URLs must be directly downloadable
- Google Drive links need to be converted to direct download URLs
- Temporary audio files are automatically cleaned up after processing
- Processing time depends on audio length and file size

## Authors

- Nadeen Ahmed
- Malak Khaled
- Malak Badawy

**Field:** Health Informatics & Data Science

## License

This project is currently unlicensed.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

---

*Last updated: May 14, 2026*
