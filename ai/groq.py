import json
import os
from groq import Groq

client = Groq(api_key="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")


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
    pass1 = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a medical transcript cleaner. Fix errors only, never change meaning."},
            {"role": "user", "content": prompt_clean}
        ],
        temperature=0.1,
        max_tokens=2000,
    )
    return pass1.choices[0].message.content.strip()


def extract_json(clean_text: str) -> str:
    prompt_extract = f"""
You are an ELITE MEDICAL SCRIBE. Transform the provided doctor-patient transcript into a structured clinical report.

### LANGUAGE RULES:
- The input may be Egyptian Arabic or English.
- doctor_summary fields: ALWAYS write in professional medical English.
- patient_summary_ar fields: ALWAYS write in clear simple Arabic.
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
If symptoms clearly match a known condition (e.g., vesicular rash + fever + exposure to infected child = Varicella),
name it explicitly. Do NOT give a vague generic diagnosis when a specific one is clearly implied by the transcript.
Use the doctor's own words as the primary source for diagnosis.
- PLAN: All medications, dosages if mentioned, warnings, contraindications, hygiene advice, isolation duration.

### EMPTY FIELD RULE:
- Only leave a field empty if absolutely nothing related was mentioned.
- Do NOT invent information not present in the transcript.

### INPUT TRANSCRIPT:
{clean_text}

### OUTPUT (JSON ONLY, no explanation, no markdown):
{{
  "doctor_summary": {{
    "subjective": "Professional English narrative of patient complaints, symptom timeline, and any exposure history.",
    "objective": "Vitals: [any measurements mentioned]. Physical Exam: [doctor clinical findings].",
    "assessment": "Most specific clinical diagnosis as stated or clearly implied by doctor.",
    "plan": "Numbered list: medications, warnings, contraindications, hygiene advice, isolation if mentioned."
  }},
  "patient_summary_ar": {{
    "diagnosis": "Vitals: [any measurements mentioned]. Physical Exam: [doctor clinical findings].",
    "findings": "Most specific clinical diagnosis as stated or clearly implied by doctor.",
    "treatment_plan": "Numbered list: medications, warnings, contraindications, hygiene advice, isolation if mentioned."
  }}
}}
"""
    pass2 = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "Return ONLY valid JSON. You are a senior medical scribe. Be accurate and detailed. Patient age is NOT symptom duration — never confuse the two."},
            {"role": "user", "content": prompt_extract}
        ],
        temperature=0,
        max_tokens=3000,
    )
    return pass2.choices[0].message.content.strip()


def safe_json_parse(text: str) -> dict:
    text = text.strip()
    if text.startswith("```") and text.endswith("```"):
        text = text[3:-3].strip()
    if text.startswith("```json"):
        text = text[7:].strip()
    try:
        return json.loads(text)
    except Exception as e:
        return {"error": f"JSON parse failed: {e}", "raw": text}