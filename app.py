from dotenv import load_dotenv
load_dotenv()

import base64
import streamlit as st
import os
import io
from PIL import Image
import pdf2image
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Gemini Response Function
def get_gemini_response(input_prompt, pdf_content, job_description):

    model = genai.GenerativeModel("models/gemini-3.6-flash")

    response = model.generate_content(
        [
            input_prompt,
            pdf_content[0],
            job_description
        ]
    )

    return response.text
# Convert PDF to image
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:

        images = pdf2image.convert_from_bytes(uploaded_file.read())

        first_page = images[0]

        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format="JPEG")

        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]

        return pdf_parts

    else:
        raise FileNotFoundError("No file uploaded")


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
1. Overall evaluation
2. Strengths
3. Weaknesses
4. Suitability for the role
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