import os
import requests
import json
import re
from dotenv import load_dotenv

load_dotenv(override=True)
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL")


def sanitize_raw_output(text: str) -> str:
    """
    Clean LLM output for parsing:
    - Removes markdown wrappers (``` or ```json)
    - Replaces nulls with empty strings
    - Fixes common invalid JSON issues (single quotes, trailing commas)
    """
    text = text.strip().strip("`")
    if text.lower().startswith("json"):
        text = text[4:].strip()

    # Replace Python-style single quotes with double quotes
    text = re.sub(r"(?<!\\)'", '"', text)

    # Remove trailing commas
    text = re.sub(r",(\s*[}\]])", r"\1", text)

    # Replace : null with : ""
    text = re.sub(r':\s*null', ': ""', text)

    return text


def parse_model_response(raw_output: str):
    raw_output = sanitize_raw_output(raw_output)

    try:
        return json.loads(raw_output)
    except json.JSONDecodeError as e:
        print("[ERROR] JSON parsing failed after sanitation:", e)
        return None


def run_model(text, model_name):
    prompt = f"""
You are an information extraction engine. Extract the following structured fields from the CV text below.

Output only a JSON object in the following format:

{{
  "Full Name": "...",
  "Email": "...",
  "Phone Number": "...",
  "Education": "...",
  "Work Experience": "...",
  "Skills": "..."
}}

CV Text:
{text}

Respond ONLY with valid JSON. Do not include explanations, headers, or markdown.
"""

    try:
        response = requests.post(
            f"{OLLAMA_API_URL}/api/chat",
            json={
                "model": model_name,
                "stream": False,
                "messages": [{"role": "user", "content": prompt}]
            }
        )

        raw_output = response.json().get("message", {}).get("content", "").strip()
        print("=== RAW OUTPUT FROM MODEL ===")
        print(raw_output)

        parsed = parse_model_response(raw_output)

        if not parsed:
            return f"Error: Invalid JSON\n\n{raw_output}"

        return parsed

    except Exception as e:
        print("[ERROR] run_model Exception:", e)
        return f"Error: {e}"
