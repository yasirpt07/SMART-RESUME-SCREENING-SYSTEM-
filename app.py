import streamlit as st
from src.parser import extract_text_from_pdf, extract_text_from_docx
from src.semantic_matcher import semantic_match

st.title("Smart Resume Screening System")

# Upload Resume
resume_file = st.file_uploader("Upload resume file", type=["pdf"])
job_desc = st.text_area("Paste Job Description here:")

if resume_file and job_desc:
    # Extract resume Text
    resume_text = extract_text_from_pdf(resume_file)

    # Calculate semantic similarity
    score = semantic_match(resume_text,job_desc)

    st.subheader("Results")
    st.write(f"Semantic Matching Score: **{score}%**")

    if score > 80:
        st.success("Excellent Fit!")
    elif score > 50:
        st.info("Moderate Fit. Consider Applying.")
    else:
        st.warning("Low Match. Skills may not align well.")


