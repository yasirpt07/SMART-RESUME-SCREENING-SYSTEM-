# 🤖 Smart Resume Screening System

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-App-success)
![BERT](https://img.shields.io/badge/BERT-NLP-yellow)
![License](https://img.shields.io/badge/License-MIT-green.svg)

### 🚀 An AI-powered Resume Screening System that semantically matches candidate resumes with job descriptions using **BERT embeddings** and **cosine similarity**.

---

## 📘 Overview
Recruiters often receive hundreds of resumes for a single job posting.  
Traditional keyword-based filtering misses out on strong candidates due to different wording.

This **Smart Resume Screening System** uses **Natural Language Processing (NLP)** and **BERT-based sentence embeddings** to measure how closely a resume aligns with a given job description — semantically, not just by keywords.

---

## 🧠 Features
✅ Resume text extraction from PDF  
✅ Job description semantic matching  
✅ BERT sentence embeddings for deep text understanding  
✅ Cosine similarity scoring  
✅ Streamlit Web App interface  
✅ Fit-level recommendation (Excellent / Moderate / Low)

---

## 🧩 Project Structure
```

smart_resume_screening/
│
├── data/
│   ├── resumes/              # Store sample resumes
│   ├── job_descriptions/     # Store job description text
│
├── src/
│   ├── parser.py             # Extract and clean resume text
│   ├── semantic_matcher.py   # Compute BERT-based similarity
│
├── app.py                    # Streamlit web app
├── requirements.txt
└── README.md

````

---

## ⚙️ Installation

### 1️⃣ Clone this Repository
```bash
git clone https://github.com/<your-username>/smart-resume-screening.git
cd smart-resume-screening
````

### 2️⃣ Create and Activate Virtual Environment (Optional)

```bash
python -m venv venv
source venv/bin/activate    # For Linux/Mac
venv\Scripts\activate       # For Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

---

## 🚀 How to Run

### Run the Streamlit App

```bash
streamlit run app.py
```

Then open your browser at 👉 `http://localhost:8501/`

---

## 🧠 Example Output

**Job Description:**

```
We are hiring a Data Scientist experienced in Python, Machine Learning, SQL, and Pandas.
```

**Resume Skills:**

```
Python, Pandas, SQL, Machine Learning, Django
```

**Output:**

```
Semantic Match Score: 92.45%
✅ Excellent Fit!
```

---

## 🧬 Tech Stack

| Component                       | Description                          |
| ------------------------------- | ------------------------------------ |
| **Python**                      | Core programming language            |
| **Streamlit**                   | Web app framework                    |
| **BERT (Sentence-Transformer)** | NLP model for semantic understanding |
| **Scikit-learn**                | Cosine similarity computation        |
| **Spacy / NLTK**                | Text preprocessing                   |

---

## 💡 Future Enhancements

🚀 Fine-tune BERT for ranking multiple resumes
🧾 Add NER (Named Entity Recognition) for education, experience, and skills
📊 Dashboard for multi-resume comparison
☁️ Deploy app on Streamlit Cloud or HuggingFace Spaces

---

## 📸 Preview

Here’s how it looks on your local Streamlit app 👇

```
+---------------------------------------------------------+
| Smart Resume Screening System                           |
|---------------------------------------------------------|
| [Upload Resume.pdf]                                     |
| [Paste Job Description Here]                            |
|                                                         |
| Semantic Match Score: 92.45%                            |
| ✅ Excellent Fit!                                        |
+---------------------------------------------------------+
```

---

## 👨‍💻 Author

**Mohammed Yasir Arafath PT**

🎓 BCA Graduate | Data Science & Machine Learning Enthusiast
📧 [info@example.com](yasirpt77@gmail.com)
🌐 [LinkedIn](https://www.linkedin.com/in/mohammed-yasir-arafath-pt/)

---

## 🪪 License

This project is licensed under the **MIT License** – feel free to use and modify it for learning or job projects.

---

### ⭐ If you like this project, don’t forget to **star** this repo!

Your support motivates me to build more real-world AI projects 💙

