import json
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY is missing in .env")

# ✅ Correct client
client = genai.Client(api_key=api_key)


# 🔹 PASS 1 — Clean transcript
def reconstruct_arabic(transcription_ar: str) -> str:
    prompt_clean = f"""
Clean this medical transcript. It may be in Egyptian Arabic or English.

RULES to follow:
- Fix spelling and Whisper recognition errors.
- Separate incorrectly connected words.
- Fix medical term misspellings.
- Keep all speaker labels (Doctor / Patient / Mother / etc).
- DO NOT summarize or remove any lines.
- DO NOT change the meaning.
- If already in English, just fix typos and formatting.

TEXT:
{transcription_ar}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt_clean
    )

    return response.text.strip()


# 🔹 PASS 2 — YOUR EXACT PROMPT (UNCHANGED)
def extract_json(speechmatics_transcript2: str) -> str:

    EXTRACTION_PROMPT = """
You are an ELITE MEDICAL SCRIBE. Transform the provided doctor-patient transcript into a structured clinical report.
### PREPROCESSING RULE:
- The input is an AUDIO TRANSCRIPT (Speech-to-Text output) and may contain recognition errors.
- FIRST step: mentally correct and normalize the transcript (fix medical words, grammar, and misheard terms).
- Then perform clinical interpretation based on the corrected version.
- DO NOT mention or output the corrected version separately — only use it internally.
### LANGUAGE RULES:
- The input may be Egyptian Arabic or English.
- doctor_summary fields: ALWAYS write in professional medical English.
- patient_summary fields: write in the SAME LANGUAGE as the input.
  - If Arabic: use clear, simple Arabic.
  - If English: use clear, patient-friendly English.
- If the input is Arabic, translate and elevate to medical English for doctor_summary.
- If the input is English, keep it as-is but upgrade to clinical terminology.

### TRANSFORMATION STRATEGY:
- Synthesize scattered conversation into professional clinical narratives.
- Upgrade informal language to proper medical terminology automatically based on context.
- If the doctor mentions a contraindication, include it in the plan.
- If the doctor mentions isolation or home rest, include it in the plan.
- If exposure history is mentioned, include it in subjective.
- Patient age is NOT symptom duration — never confuse the two.

### SOAP RULES:
- SUBJECTIVE: Full HPI — onset, duration, symptoms, severity, exposure history if mentioned.
- OBJECTIVE: Vitals (numerical values only) + Physical exam findings as described by doctor.
- ASSESSMENT: Provide the MOST SPECIFIC clinical diagnosis possible.
  If symptoms clearly match a known condition (e.g., vesicular rash + fever + exposure = Varicella),
  name it explicitly. Do NOT give a vague diagnosis if a specific one is implied.
- PLAN: Numbered list including medications, dosages (if mentioned), warnings, contraindications,
  hygiene advice, and isolation duration if mentioned.

### PATIENT SUMMARY RULES:
- Use simple, clear language for a non-medical patient
- No medical jargon unless explained
- Keep each field SHORT (1–2 lines max)
- Do NOT repeat the same information across fields
- Do NOT include doctor-only actions (e.g. auscultation, oxygen monitoring) unless rewritten as patient advice
- Focus on: what the patient has, what they feel, what to do, and when to worry
- Do NOT invent symptoms, medications, or advice not mentioned or clearly implied

### EMPTY FIELD RULE:
- Only leave a field empty if absolutely nothing related was mentioned.
- Do NOT invent information not present in the transcript.

### INPUT TRANSCRIPT:
{speechmatics_transcript2}

### OUTPUT (JSON ONLY, no explanation, no markdown):
{{
  "doctor_summary": {{
    "subjective": "Professional English narrative of patient complaints, symptom timeline, and any exposure history.",
    "objective": "Vitals: [any measurements mentioned]. Physical Exam: [doctor clinical findings].",
    "assessment": "Most specific clinical diagnosis as stated or clearly implied by doctor.",
    "plan": "Numbered list: medications, warnings, contraindications, hygiene advice, isolation if mentioned."
  }},
  "patient_summary": {{
    "diagnosis": "",
    "symptoms": "",
    "treatment_plan": "",
    "when_to_seek_help": "",
    "follow_up": ""
  }}
}}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=EXTRACTION_PROMPT.format(
            speechmatics_transcript2=speechmatics_transcript2
        )
    )

    return response.text.strip()


# 🔹 JSON parser (unchanged)
def safe_json_parse(text: str) -> dict:
    text = text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(text)
    except Exception as e:
        return {"error": f"JSON parse failed: {e}", "raw": text}