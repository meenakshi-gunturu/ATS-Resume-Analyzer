from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from PyPDF2 import PdfReader
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Gemini Response Function
def get_gemini_response(input_prompt, pdf_content, job_description):

    model = genai.GenerativeModel("models/gemini-3.6-flash")

    response = model.generate_content(
        f"""
        Resume:
        {pdf_content}

        Job Description:
        {job_description}

        Task:
        {input_prompt}
        """
    )

    return response.text


# Extract text from PDF
def input_pdf_setup(uploaded_file):

    pdf_reader = PdfReader(uploaded_file)

    text = ""

    for page in pdf_reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text

    return text


# Streamlit UI
st.set_page_config(page_title="ATS Resume Expert")

st.header("ATS Tracking System")

input_text = st.text_area("Job Description")

uploaded_file = st.file_uploader(
    "Upload your Resume (PDF)",
    type=["pdf"]
)

if uploaded_file is not None:
    st.success("PDF Uploaded Successfully")

submit1 = st.button("Tell Me About The Resume")
submit3 = st.button("Percentage Match")


# Prompt 1
input_prompt1 = """
You are an experienced Technical Human Resource Manager.

Review the provided resume against the job description.

Please provide:
1. Overall Evaluation
2. Strengths
3. Weaknesses
4. Suitability for the Role
"""


# Prompt 2
input_prompt3 = """
You are an ATS (Applicant Tracking System) scanner.

Evaluate the resume against the job description.

Provide:

1. ATS Match Percentage
2. Missing Keywords
3. Skills Match
4. Final Suggestions
"""


# Resume Review
if submit1:

    if uploaded_file is not None:

        try:

            pdf_content = input_pdf_setup(uploaded_file)

            response = get_gemini_response(
                input_prompt1,
                pdf_content,
                input_text
            )

            st.subheader("Resume Review")
            st.write(response)

        except Exception as e:
            st.error(f"Error: {e}")

    else:
        st.warning("Please upload a resume")


# ATS Match
if submit3:

    if uploaded_file is not None:

        try:

            pdf_content = input_pdf_setup(uploaded_file)

            response = get_gemini_response(
                input_prompt3,
                pdf_content,
                input_text
            )

            st.subheader("ATS Match Result")
            st.write(response)

        except Exception as e:
            st.error(f"Error: {e}")

    else:
        st.warning("Please upload a resume")
