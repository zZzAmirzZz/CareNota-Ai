def run_pipeline(file_path, age=None, gender=None, chronic_conditions=None, allergies=None, last_summary=None):
    try:
        processed_path = preprocess_audio(file_path)
        text = transcribe_audio(processed_path)
        corrected = reconstruct_arabic(text)
        raw_json = extract_json(
            corrected,
            age=age,
            gender=gender,
            chronic_conditions=chronic_conditions,
            allergies=allergies,
            last_summary=last_summary
        )
        final_json = safe_json_parse(raw_json)
        return final_json
    except Exception as e:
        return {"error": str(e)}