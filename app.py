# app.py
import streamlit as st
import time
import io
import re
import difflib
import pandas as pd
import requests
import matplotlib.pyplot as plt
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from streamlit_lottie import st_lottie
from src.parser import extract_text_from_pdf, clean_text, parse_basic_info

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Smart Resume Ranking (AI Dashboard)",
    page_icon="🤖",
    layout="wide"
)

# ---------------- LOAD MODEL ----------------
@st.cache_resource(show_spinner=False)
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

model = load_model()

# ---------------- LOTTIE ----------------
def load_lottie_url(url: str):
    """Load a Lottie animation from URL."""
    try:
        r = requests.get(url, timeout=6)
        if r.status_code == 200:
            return r.json()
    except Exception:
        return None
    return None

lottie_header = load_lottie_url("https://assets9.lottiefiles.com/packages/lf20_t9gkkhz4.json")
lottie_scan = load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_jbrw3hcz.json")

# ---------------- STYLING ----------------
st.markdown("""
<style>
body, [data-testid="stAppViewContainer"] {
  background: linear-gradient(135deg, #eef7ff, #e6f0ff, #f6fbff);
  font-family: 'Poppins', sans-serif;
  color: #0a1a33;
}
.card {
  background: rgba(255,255,255,0.9);
  border-radius: 16px;
  padding: 22px;
  box-shadow: 0 6px 20px rgba(0,0,0,0.08);
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}
.card:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 35px rgba(0,180,255,0.2);
}
.title {
  font-weight: 800;
  text-align: center;
  font-size: 42px;
  background: linear-gradient(90deg, #007bff, #00b4d8);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.stButton > button, .stDownloadButton>button {
  background: #1e293b;
  color: white;
  border-radius: 10px;
  padding: 0.6em 1.3em;
  border: none;
  font-weight: 600;
  box-shadow: 0 0 10px rgba(0,255,255,0.35);
  transition: all 0.25s ease;
}
.stButton > button:hover, .stDownloadButton>button:hover {
  background: #007bff;
  box-shadow: 0 0 20px rgba(0,255,255,0.55);
  transform: scale(0.97);
}
.stButton > button:active, .stDownloadButton>button:active {
  transform: scale(0.95);
  box-shadow: 0 0 12px rgba(0,255,255,0.3);
}
.stProgress > div > div > div > div {
  background: linear-gradient(90deg, #007bff, #00e0ff);
}
.footer {
  color:#334155;
  text-align:center;
  font-size:13px;
  margin-top:40px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<div class='title'>🤖 Smart Resume Ranking — AI Recruiter Dashboard</div>", unsafe_allow_html=True)
if lottie_header:
    st_lottie(lottie_header, height=160, key="header_anim")
st.markdown("<p style='text-align:center;color:#334155;'>AI-powered resume ranking with glowing animated insights</p>", unsafe_allow_html=True)
st.markdown("---")

# ---------------- FUNCTIONS ----------------
def semantic_similarity(resume_text, jd_text):
    """Compute semantic similarity using sentence embeddings."""
    emb1 = model.encode([resume_text])
    emb2 = model.encode([jd_text])
    return round(cosine_similarity(emb1, emb2)[0][0] * 100, 2)

def keyword_match(resume_text, jd_text, top_n=25, fuzzy_cutoff=0.75):
    """Extract and match top keywords between resume and job description."""
    resume_low = resume_text.lower()
    jd_low = jd_text.lower()

    tf = TfidfVectorizer(max_features=top_n, stop_words="english")
    tfidf_matrix = tf.fit_transform([jd_low, resume_low])
    feature_names = tf.get_feature_names_out()
    jd_vec = tfidf_matrix[0].toarray()[0]
    important_idx = jd_vec.argsort()[::-1][:top_n]
    jd_keywords = [feature_names[i] for i in important_idx if jd_vec[i] > 0]

    resume_tokens = re.findall(r"\w+", resume_low)
    resume_unique = list(dict.fromkeys(resume_tokens))

    matched = []
    for kw in jd_keywords:
        if (
            re.search(r"\b" + re.escape(kw) + r"\b", resume_low)
            or kw in resume_low
            or difflib.get_close_matches(kw, resume_unique, n=1, cutoff=fuzzy_cutoff)
        ):
            matched.append(kw)
    return jd_keywords, list(dict.fromkeys(matched))

def generate_excel_bytes(df):
    """Generate Excel file for download."""
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Ranking")
    return buf.getvalue()

# ---------------- INPUT SECTION ----------------
col_left, col_right = st.columns([2.3, 1])
with col_left:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📄 Upload Multiple Resumes & Paste Job Description")
    uploaded_files = st.file_uploader("Upload Resumes (PDFs)", type=["pdf"], accept_multiple_files=True)
    jd_text = st.text_area("Paste Job Description", height=220)
    st.markdown("</div>", unsafe_allow_html=True)

with col_right:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("⚙️ Settings")
    threshold = st.slider("Good Fit Threshold (%)", 40, 95, 70)
    enable_export = st.checkbox("Enable Excel Export", True)
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- MAIN LOGIC ----------------
if st.button("🚀 Analyze & Rank Resumes", use_container_width=True):
    if not uploaded_files or not jd_text.strip():
        st.warning("Please upload at least one resume and paste a job description.")
    else:
        all_data = []
        with st.spinner("🔍 Analyzing resumes..."):
            for file in uploaded_files:
                raw_text = clean_text(extract_text_from_pdf(file))
                candidate = parse_basic_info(raw_text)
                score = semantic_similarity(raw_text, jd_text)
                jd_keywords, matched = keyword_match(raw_text, jd_text)
                verdict = (
                    "Excellent Fit ✅" if score >= threshold
                    else "Good Fit 👍" if score >= 50
                    else "Needs Improvement ⚠️"
                )
                all_data.append({
                    "Name": candidate.get("name", "Not found"),
                    "Email": candidate.get("email", "Not found"),
                    "Phone": candidate.get("phone", "Not found"),
                    "Match Score (%)": score,
                    "Matched Keywords": matched,
                    "Verdict": verdict
                })
                time.sleep(0.1)

        df = pd.DataFrame(all_data).sort_values(by="Match Score (%)", ascending=False).reset_index(drop=True)
        top5 = df.head(5)

        st.success("✅ Top 5 Candidates Ranked Successfully!")
        if lottie_scan:
            st_lottie(lottie_scan, height=120, key="scan_anim")

        # ---------------- TABLE ----------------
        st.markdown("### 🏆 Top 5 Candidate Ranking Table")
        st.dataframe(
            top5[["Name", "Email", "Phone", "Match Score (%)", "Verdict"]]
            .style.format({"Match Score (%)": "{:.2f}"})
        )

        # ---------------- ANIMATED BAR CHART ----------------
        st.markdown("### 📊 Top 5 Candidates by Match Score (Animated)")
        colors = ['#00aaff', '#00b4d8', '#48cae4', '#90e0ef', '#0077b6']
        glow_steps = np.linspace(0.3, 1, 10)
        progress_placeholder = st.empty()

        for step, alpha in zip(range(1, 11), glow_steps):
            progress = top5.copy()
            progress["Animated Score"] = progress["Match Score (%)"] * (step / 10)
            fig, ax = plt.subplots(figsize=(8, 4))
            bars = ax.barh(progress["Name"], progress["Animated Score"], color=colors, alpha=alpha)
            ax.set_xlabel("Match Score (%)", fontsize=12)
            ax.set_title("Top 5 Resume Match Scores", fontsize=14, fontweight="bold", color="#001d3d")
            ax.invert_yaxis()
            ax.set_xlim(0, 100)
            for bar, val in zip(bars, progress["Animated Score"]):
                ax.text(val + 1, bar.get_y() + bar.get_height()/2, f"{val:.1f}%",
                        va='center', fontsize=10, color='#001d3d', fontweight='bold')
            fig.patch.set_alpha(0)
            plt.tight_layout()
            progress_placeholder.pyplot(fig)
            time.sleep(0.08)

        # ---------------- HIGHLIGHTS ----------------
        st.markdown("### 🧩 Top 5 Resume Highlights")
        for idx, row in top5.iterrows():
            with st.expander(f"📘 {row['Name']} — {row['Verdict']}"):
                if row["Matched Keywords"]:
                    st.markdown(f"**Matched Keywords in Resume:** {', '.join(row['Matched Keywords'][:20])}")
                else:
                    st.info("Semantic match is good — even if keywords differ slightly.")

        # ---------------- EXPORT ----------------
        if enable_export:
            export_df = df.drop(columns=["Matched Keywords"])
            st.download_button(
                "⬇️ Download Ranked Excel Report",
                data=generate_excel_bytes(export_df),
                file_name="resume_ranking_report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

# ---------------- FOOTER ----------------
st.markdown("<hr><p class='footer'>© 2025 Mohammed Yasir Arafath • Smart Resume Ranking Dashboard</p>", unsafe_allow_html=True)
