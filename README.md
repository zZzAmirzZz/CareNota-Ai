# 🏥 CareNota-Ai: Healthcare AI Audio Processing API

An AI-powered backend system that processes medical audio recordings and converts them into structured clinical reports using advanced speech recognition and large language models.

## 📌 Overview

CareNota-Ai streamlines clinical documentation by automatically converting audio recordings into structured SOAP-formatted medical reports. The system handles multiple languages including Arabic and Egyptian Arabic dialects, making it accessible for diverse healthcare environments.

### Key Capabilities

- 🎙️ **Speech-to-Text** - Uses OpenAI Whisper for accurate transcription
- 🧠 **AI Processing** - Leverages Google Gemini LLM for intelligent analysis
- 📄 **Structured Output** - Generates SOAP-formatted clinical reports
- 🌍 **Multilingual Support** - Arabic, English, and Egyptian Arabic dialects
- 📊 **Dual Summaries** - Separate doctor and patient-friendly report formats

## 🔄 Pipeline Flow

```
Audio Input
    ↓
Transcribe (Whisper)
    ↓
Clean Transcript (AI)
    ↓
Extract Structured Data (Gemini)
    ↓
Generate Medical Report (JSON)
```

## 📦 Tech Stack

- **Language:** Python
- **Framework:** FastAPI
- **Speech Recognition:** OpenAI Whisper
- **LLM:** Google Gemini API
- **Audio Processing:** FFmpeg

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- pip (Python package installer)
- FFmpeg installed on your system
- API Keys: Google Gemini API

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Nadeenyakout/CareNota-Ai.git
cd CareNota-Ai
```

2. Create a `.env` file with your API keys:
```
GEMINI_API_KEY=your_api_key_here
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## 📡 API Endpoints

### GET `/`
Health check endpoint to verify the API is running.

**Response:**
```json
{
  "status": "API is running"
}
```

### POST `/process-audio`
Process medical audio and generate clinical reports.

**Request:**
```json
{
  "audio_url": "https://example.com/audio.wav"
}
```

**Response:**
```json
{
  "doctor_summary": {
    "subjective": "Patient's complaints and history",
    "objective": "Clinical findings and observations",
    "assessment": "Medical diagnosis and interpretation",
    "plan": "Treatment plan and recommendations"
  },
  "patient_summary_ar": {
    "diagnosis": "التشخيص",
    "findings": "النتائج",
    "treatment_plan": "خطة العلاج"
  }
}
```

## ⚠️ Important Notes

- Audio URL must be a direct downloadable audio file
- Google Drive links require conversion to direct download URLs
- Large files may take longer to process
- Ensure FFmpeg is properly installed for audio processing

## 🔮 Future Improvements

- Direct audio file upload support
- Real-time streaming capability
- Database integration (Firebase)
- Enhanced error handling and validation
- Multi-user authentication

## 👩‍💻 Authors

- Nadeen Ahmed
- Malak Khaled
- Malak Badawy

**Field:** Health Informatics & Data Science

## 📄 License

This project is currently unlicensed. Consider adding a license to clarify usage terms.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

---

*Last updated: May 14, 2026*
