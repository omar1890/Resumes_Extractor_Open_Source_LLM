import re

def sanitize_raw_json(text: str) -> str:
    """
    Cleans LLM-generated raw JSON-like text:
    - Removes markdown fencing (``` or ```json)
    - Replaces all `null` values with empty strings
    - Trims leading/trailing whitespace
    """
    # Remove markdown fencing
    text = text.strip().strip("`")
    if text.startswith("json"):
        text = text[4:].strip()

    # Replace `null` values for any field (generic)
    text = re.sub(r':\s*null([,\n\r])', r': ""\1', text)

    return text.strip()
