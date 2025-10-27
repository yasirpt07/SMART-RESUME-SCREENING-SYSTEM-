# src/parser.py
import re
from io import BytesIO
from PyPDF2 import PdfReader

# ---------------- PDF TEXT EXTRACTION ----------------
def extract_text_from_pdf(uploaded_file):
    """
    Extract raw text content from an uploaded PDF file.
    Returns concatenated string of all text in the PDF.
    """
    try:
        pdf = PdfReader(uploaded_file)
        text = ""
        for page in pdf.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"
        return text.strip()
    except Exception as e:
        return f"Error reading PDF: {e}"

# ---------------- TEXT CLEANING ----------------
def clean_text(text):
    """
    Cleans the extracted resume text.
    Removes special characters, extra spaces, and non-ASCII symbols.
    """
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', text)              # Replace multiple spaces/newlines
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)   # Remove non-ASCII chars
    text = re.sub(r'[^\w\s@.,]', '', text)       # Keep only basic chars
    return text.strip().lower()

# ---------------- BASIC INFO PARSING ----------------
def parse_basic_info(text):
    """
    Extract basic candidate info (name, email, phone) from resume text.
    Uses regex patterns for detection.
    """
    info = {}

    # Email extraction
    email_pattern = re.compile(r'[\w\.-]+@[\w\.-]+\.\w+')
    emails = email_pattern.findall(text)
    info['email'] = emails[0] if emails else "Not found"

    # Phone number extraction
    phone_pattern = re.compile(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3,5}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}')
    phones = phone_pattern.findall(text)
    info['phone'] = phones[0] if phones else "Not found"

    # Name extraction (simple heuristic)
    # Often the first 2–4 words in resume text before keywords like "summary", "profile", etc.
    name_match = re.search(r'([A-Z][a-z]+(?:\s[A-Z][a-z]+){0,3})(?=\s+(?:summary|profile|objective|email|phone|contact))', text, re.IGNORECASE)
    if name_match:
        info['name'] = name_match.group(1).title()
    else:
        # fallback: take the first 2–3 words if no pattern matched
        tokens = text.split()
        info['name'] = " ".join(tokens[:2]).title() if len(tokens) >= 2 else "Not found"

    return info

# ---------------- SELF TEST ----------------
if __name__ == "__main__":
    # Quick test (optional)
    sample = """
    JOHN DOE
    Data Scientist | Python Developer
    Email: john.doe@example.com
    Phone: +1 987-654-3210
    Profile:
    Passionate about AI and data analytics...
    """
    print("🧠 Cleaned Text:", clean_text(sample))
    print("📬 Parsed Info:", parse_basic_info(clean_text(sample)))
