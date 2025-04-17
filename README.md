Here’s a professional and complete `README.md` for your project:

---

### 📄 `README.md`

```markdown
# 🧠 CV Extractor with Open-Source LLMs

This project is a Streamlit-based web application that extracts structured information from CVs (PDF or scanned images) using open-source large language models (LLMs) running via [Ollama](https://ollama.com/). The extracted information is evaluated against predefined ground truth using precision, recall, and F1-score to compare the performance of different models.

---

## 🚀 Features

- Upload CVs as PDF or image (JPG/PNG)
- Use one of three LLMs for extraction:
  - `llama3`
  - `mistral`
  - `phi`
- Automatic text extraction (OCR or PDF parser)
- Extract structured fields:
  - Full Name
  - Email
  - Phone Number
  - Education
  - Work Experience
  - Skills
- Compare extraction accuracy against ground truth
- Save extracted output and metrics for each model per CV
- Visualize results using bar charts and Streamlit widgets

---

## 📦 Installation

1. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install and run Ollama**
   Follow instructions at [https://ollama.com](https://ollama.com) to install and run Ollama locally or on a remote machine (e.g., Colab + ngrok).

   Then run the following commands to install models:
   ```bash
   ollama run llama3
   ollama run mistral
   ollama run phi
   ```

3. **Create a `.env` file**

   ```env
   OLLAMA_API_URL=http://localhost:11434
   ```

   If using ngrok/Colab, replace with your public URL:
   ```env
   OLLAMA_API_URL=https://your-ngrok-url.ngrok.io
   ```

4. **Run the Streamlit app**
   ```bash
   streamlit run main.py
   ```

---

## 📂 Project Structure

```
cv_extractor_project/
├── app/                    # Streamlit UI logic
├── data/                   # Sample CVs and ground truth
├── evaluations/            # Saved outputs and metrics per model per CV
├── models/                 # Ollama integration and schema validation
├── utils/                  # Text extraction and evaluation logic
├── .env                    # Ollama server URL
├── main.py                 # Entry point
├── requirements.txt
└── README.md
```

---

## 📊 Evaluation Strategy

The extracted output is compared to a manually curated `ground_truth_<cv_name>.json`. The comparison uses:

- **Precision**: Correct fields extracted / All extracted fields
- **Recall**: Correct fields extracted / All expected fields
- **F1 Score**: Harmonic mean of precision and recall

Evaluation and extracted results are saved under:

```
evaluations/
├── extracted_<cv_name>_<model>.json
├── eval_<cv_name>.json
```

---

## ⚔️ Model Comparison

Example comparison for `OmarWaelAttia.pdf`:

| Model   | Precision | Recall | F1 Score |
|---------|-----------|--------|----------|
| LLaMA 3 | 1.00      | 0.50   | 0.67     |
| Mistral | 1.00      | 0.33   | 0.50     |
| Phi     | ⚠ Errors in formatting, JSON parsing failed |

> ⚠ `phi` currently produces less consistent JSON-like responses, requiring manual cleaning or custom prompt adjustments.

---

## 🔥 Known Challenges

- **Model Output Format**: Not all LLMs return well-formed JSON (e.g., `phi` often returns markdown or Python-style dicts).
- **Inconsistent Field Names**: Some models omit fields or rename keys.
- **Nested Structures**: Education and Work Experience are sometimes nested and must be flattened.
- **Null values and single quotes**: Cause parsing failures — handled with a robust sanitation pipeline.

---

## 📌 Next Improvements

- Add fuzzy matching for partial-field scoring
- Fine-tune prompts for `phi` or switch to stricter output constraints
- Add a dashboard for full model performance across many CVs

---

## 👨‍💻 Author

Omar Wael