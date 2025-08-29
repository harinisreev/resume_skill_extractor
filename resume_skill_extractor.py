import streamlit as st
from PyPDF2 import PdfReader
import re
import pandas as pd

# -------------------------------
# 1. Sample Skill Dictionary
# -------------------------------
SKILL_LIST = [
    "python", "java", "c++", "sql", "excel", "tableau",
    "machine learning", "deep learning", "nlp",
    "data analysis", "data visualization", "cloud", "aws", "azure",
    "docker", "kubernetes", "html", "css", "javascript", "git",
    "tensorflow", "pytorch", "scikit-learn", "linux", "r"
]

# -------------------------------
# 2. Utility Functions
# -------------------------------
def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    return text

def extract_skills(text, skill_list):
    found_skills = []
    for skill in skill_list:
        if skill in text:
            found_skills.append(skill)
    return list(set(found_skills))

def match_skills(resume_skills, jd_skills):
    matched = set(resume_skills) & set(jd_skills)
    missing = set(jd_skills) - set(resume_skills)
    return matched, missing

# -------------------------------
# 3. Streamlit App
# -------------------------------
st.set_page_config(page_title="Resume Skill Extractor (Manual)", layout="wide")
st.title("Resume Skill Extractor (Manual Version)")

uploaded_resume = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
jd_text = st.text_area("Paste Job Description Here")

if uploaded_resume and jd_text.strip():
    # Extract resume text
    resume_text = extract_text_from_pdf(uploaded_resume)
    resume_text_clean = clean_text(resume_text)
    jd_text_clean = clean_text(jd_text)

    # Extract skills manually
    resume_skills = extract_skills(resume_text_clean, SKILL_LIST)
    jd_skills = extract_skills(jd_text_clean, SKILL_LIST)

    # Compare skills
    matched, missing = match_skills(resume_skills, jd_skills)

    # -------------------------------
    # Summary Score
    # -------------------------------
    if jd_skills:
        coverage = (len(matched) / len(jd_skills)) * 100
        st.metric("Resume Coverage", f"{coverage:.1f} %")
    else:
        coverage = 0
        st.metric("Resume Coverage", "N/A")

    # -------------------------------
    # Side-by-side display for Resume vs JD skills
    # -------------------------------
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📌 Skills Found in Resume")
        if resume_skills:
            st.write("\n".join([f"- {skill.upper()}" for skill in resume_skills]))
        else:
            st.write("No skills detected.")

    with col2:
        st.subheader("📌 Skills Found in Job Description")
        if jd_skills:
            st.write("\n".join([f"- {skill.upper()}" for skill in jd_skills]))
        else:
            st.write("No skills detected.")

    # -------------------------------
    # Side-by-side display for Matched vs Missing skills
    # -------------------------------
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("✅ Matched Skills")
        if matched:
            st.success("\n".join([f"- {skill.upper()}" for skill in matched]))
        else:
            st.success("No matches found.")

    with col4:
        st.subheader("❌ Missing Skills")
        if missing:
            st.error("\n".join([f"- {skill.upper()}" for skill in missing]))
        else:
            st.error("None! The resume covers all skills.")

    # -------------------------------
    # Candidate Suitability Analysis
    # -------------------------------
    st.subheader("Candidate Analysis")

    if not jd_skills:
        st.info("⚠️ No skills found in Job Description. Unable to analyze suitability.")
    else:
        if coverage >= 70:
            st.success("✅ The candidate is a **Good Fit** for the job. Most required skills are present.")
        elif 40 <= coverage < 70:
            st.warning("⚠️ The candidate is a **Moderate Fit**. Some important skills are missing.")
        else:
            st.error("❌ The candidate is **Not a Good Fit**. Too many required skills are missing.")
    
    # -------------------------------
    # Downloadable CSV (Neat Table)
    # -------------------------------
    df = pd.DataFrame({
        "Skill": sorted(set(resume_skills) | set(jd_skills)),  # union of both
        })
    df["In_Resume"] = df["Skill"].apply(lambda x: "YES" if x in resume_skills else "NO")
    df["In_Job_Description"] = df["Skill"].apply(lambda x: "YES" if x in jd_skills else "NO")
    df["Matched"] = df["Skill"].apply(lambda x: "YES" if x in matched else "NO")
    df["Missing"] = df["Skill"].apply(lambda x: "YES" if x in missing else "NO")

    # Show in Streamlit as interactive table
    st.subheader("📊 Detailed Skill Comparison Table")
    st.dataframe(df)

    # Download CSV in clean format
    st.download_button(
    "⬇ Download Results as CSV",
    df.to_csv(index=False).encode("utf-8"),
    "skill_match.csv",
    "text/csv"
)
