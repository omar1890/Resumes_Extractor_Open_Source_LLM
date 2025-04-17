import streamlit as st
from utils.pdf_image_extraction import extract_text
from models.inference import run_model
from utils.evaluation import evaluate_extraction
import os
import tempfile
import json
from utils.evaluation import evaluate_extraction, save_evaluation_to_file, save_extracted_output

def run_ui():
    st.title("📄 CV Extractor with Open-Source LLMs")
    st.write("Upload a CV PDF or image, then extract structured information using LLaMA 3, Mistral, or Phi-2.")

    uploaded_file = st.file_uploader("Upload CV", type=["pdf", "png", "jpg", "jpeg"])
    model_choice = st.selectbox("Choose Model", ["llama3", "mistral", "phi"])
    evaluate = st.checkbox("Evaluate against ground truth (if available)")

    if uploaded_file is not None:
        file_ext = os.path.splitext(uploaded_file.name)[1].lower()
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_file_path = tmp_file.name

        text = extract_text(tmp_file_path, file_ext)

        if text:
            st.subheader("Extracted CV Text (Preview)")
            st.text_area("", text[:2000], height=200)

            if st.button("Run Model"):
                with st.spinner("Extracting information..."):
                    result = run_model(text, model_choice)
                st.subheader("📋 Extracted Information")
                st.code(result)
                # Derive CV name from uploaded filename
                cv_name = os.path.splitext(uploaded_file.name)[0].replace(" ", "_")
                print(cv_name)


                if evaluate:
                    try:
                        
                        if isinstance(result, dict):
                            # Continue evaluation
                            with open(f"data/ground_truth_{cv_name}.json") as f:
                                ground_truth = json.load(f)

                            metrics = evaluate_extraction(result, ground_truth)
                            st.subheader("📊 Evaluation Metrics")
                            st.json(metrics)

                            save_evaluation_to_file(cv_name, model_choice, metrics)
                            save_extracted_output(cv_name, model_choice, result)
                        else:
                            st.warning("Model did not return valid structured output. Skipping evaluation.")


                    except Exception as e:
                        st.warning(f"Evaluation skipped: {e}")
        else:
            st.error("No text could be extracted.")
