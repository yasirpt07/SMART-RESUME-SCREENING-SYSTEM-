import pdfplumber
from docx import Document
import re

# Extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

# Extract text from DOCX
def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    return "\n".join([para.text for para in doc.paragraphs])

# Extract basic info like email and phone
def extract_info(text):
    email = re.findall(r'\S+@\S+', text)
    phone = re.findall(r'\b\d{10}\b', text)
    return {
        "email": email[0] if email else None,
        "phone": phone[0] if phone else None
    }

# Extract skills using keyword matching
skills_list = ['python', 'machine learning', 'sql', 'numpy', 'pandas', 'data analysis', 'excel',' Microsoft Power BI']

def extract_skills(text):
    text = text.lower()
    extracted = [skill for skill in skills_list if skill in text]
    return extracted

