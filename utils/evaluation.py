from sklearn.metrics import precision_score, recall_score, f1_score
from difflib import SequenceMatcher
import json
import re
import os
def string_similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

def evaluate_extraction(extracted_text, ground_truth, threshold=0.7):
    if isinstance(extracted_text, str):
        extracted = parse_result(extracted_text)
    elif isinstance(extracted_text, dict):
        extracted = extracted_text
    else:
        raise ValueError("Extracted output must be a dict or string")

    fields = ["Full Name", "Email", "Phone Number", "Education", "Work Experience", "Skills"]
    y_true = []
    y_pred = []

    for field in fields:
        gt = ground_truth.get(field, "")
        pred = extracted.get(field, "")

        if isinstance(gt, list):
            gt = " ".join(gt)
        if isinstance(pred, list):
            pred = " ".join(pred)

        gt = str(gt).strip().lower() if gt else ""
        pred = str(pred).strip().lower() if pred else ""

        sim = string_similarity(gt, pred)
        y_true.append(1)
        y_pred.append(1 if sim >= threshold else 0)

    return {
        "Precision": precision_score(y_true, y_pred, zero_division=0),
        "Recall": recall_score(y_true, y_pred, zero_division=0),
        "F1 Score": f1_score(y_true, y_pred, zero_division=0)
    }

def parse_result(text):
    result = {}
    current_key = None
    for line in text.strip().splitlines():
        line = line.strip().lstrip("- ").strip()

        if ":" in line:
            key, val = line.split(":", 1)
            current_key = key.strip()
            result[current_key] = val.strip()
        elif current_key:
            result[current_key] += " " + line.strip()
    return result


def save_evaluation_to_file(cv_name, model_name, metrics, folder="evaluations"):
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f"eval_{cv_name}.json")

    if os.path.exists(path):
        with open(path, "r") as f:
            data = json.load(f)
    else:
        data = {}

    data[model_name] = metrics

    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def save_extracted_output(cv_name, model_name, output_text, folder="evaluations"):
    os.makedirs(folder, exist_ok=True)
    output_path = os.path.join(folder, f"extracted_{cv_name}_{model_name}.json")

    with open(output_path, "w", encoding="utf-8") as f:
        if isinstance(output_text, dict):
            json.dump(output_text, f, indent=2)
        else:
            f.write(str(output_text))
