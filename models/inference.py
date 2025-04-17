import os
import requests
from dotenv import load_dotenv
import json

load_dotenv(override=True)
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL")

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
        print("[DEBUG] Raw Model Output:\n", raw_output)

        if not raw_output:
            return "Error: Empty response from model."

        # Try to extract valid JSON even if wrapped in markdown
        if raw_output.startswith("```"):
            raw_output = raw_output.strip("`").strip()
            if raw_output.startswith("json"):
                raw_output = raw_output[4:].strip()

        return json.loads(raw_output)

    except json.JSONDecodeError as jde:
        print("[ERROR] Failed to parse JSON:", jde)
        return f"Error: Invalid JSON\n\n{raw_output}"
    except Exception as e:
        return f"Error: {e}"
