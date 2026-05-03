🏥 Healthcare AI Audio Processing API
📌 Overview

This project is an AI-powered backend system that processes medical audio recordings and converts them into structured clinical reports.

The system uses:

🎙️ Speech-to-text (Whisper)
🧠 AI processing (Gemini LLM)
📄 Structured output (SOAP medical format)
⚙️ Features
Convert audio → text (Arabic & English)
Clean medical transcripts automatically
Generate structured clinical reports
Output in JSON format (doctor + patient summaries)
Handles Egyptian Arabic dialect 🇪🇬
🧠 Pipeline Flow
Upload or provide audio URL
Transcribe audio using Whisper
Clean transcript using AI
Extract structured JSON using Gemini
Return final medical report
📦 Tech Stack
Python
FastAPI
Whisper (OpenAI)
Google Gemini API (LLM)
FFmpeg
🚀 API Endpoints
🔹 GET /

Check if API is running

🔹 POST /process-audio

Process audio file from URL

Request:
{
  "audio_url": "https://example.com/audio.wav"
}
Response:
{
  "doctor_summary": {
    "subjective": "...",
    "objective": "...",
    "assessment": "...",
    "plan": "..."
  },
  "patient_summary_ar": {
    "diagnosis": "...",
    "findings": "...",
    "treatment_plan": "..."
  }
}
⚠️ Notes
Audio URL must be a direct downloadable audio file
Google Drive links need conversion to direct download
Large files may take longer to process
🔐 Environment Variables

Create a .env file:

GEMINI_API_KEY=your_api_key_here
▶️ How to Run
pip install -r requirements.txt
uvicorn main:app --reload
💡 Future Improvements
Upload audio directly (instead of URL)
Real-time streaming
Database integration (Firebase)
Error handling & validation improvements
👩‍💻 Author

Nadeen Ahmed
Malak Khaled
Malak Badawy
Health Informatics & Data Science