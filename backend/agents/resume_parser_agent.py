import re
from pathlib import Path
from typing import Dict, List

try:
    import pdfplumber
except ImportError:
    pdfplumber = None

try:
    import spacy
    nlp = spacy.load("en_core_web_sm")
except Exception:
    nlp = None

SKILL_KEYWORDS = [
    "python", "fastapi", "flask", "sql", "postgresql", "mysql", "docker", "aws", "gcp", "azure",
    "langchain", "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", "sqlalchemy", "streamlit",
    "react", "node", "git", "nlp", "r", "spark", "mongodb", "redis", "linux"
]

EDUCATION_KEYWORDS = ["bachelor", "master", "phd", "degree", "diploma", "bs", "ms", "mba"]
CERTIFICATION_KEYWORDS = ["certified", "certification", "certificate", "aws", "gcp", "azure", "scrum"]


def extract_text_from_pdf(path: str) -> str:
    if pdfplumber:
        try:
            with pdfplumber.open(path) as pdf:
                return "\n".join(page.extract_text() or "" for page in pdf.pages)
        except Exception:
            pass

    from PyPDF2 import PdfReader
    reader = PdfReader(path)
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def extract_contact_info(text: str) -> Dict[str, str]:
    email_match = re.search(r"[\w\.-]+@[\w\.-]+", text)
    phone_match = re.search(r"(\+?\d[\d\s\-()]{7,}\d)", text)
    name = ""

    if nlp:
        doc = nlp(text)
        persons = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
        if persons:
            name = persons[0]

    if not name:
        first_line = next((line.strip() for line in text.splitlines() if line.strip()), "")
        name = first_line

    return {
        "name": name,
        "email": email_match.group(0) if email_match else "",
        "phone": phone_match.group(0) if phone_match else "",
    }


def extract_section_keywords(text: str, keywords: List[str]) -> List[str]:
    found = set()
    normalized = text.lower()
    for keyword in keywords:
        if keyword.lower() in normalized:
            found.add(keyword.title())
    return sorted(found)


def extract_summary(text: str) -> Dict[str, List[str]]:
    skills = extract_section_keywords(text, SKILL_KEYWORDS)
    education = extract_section_keywords(text, EDUCATION_KEYWORDS)
    certifications = extract_section_keywords(text, CERTIFICATION_KEYWORDS)
    return {
        "skills": skills,
        "education": education,
        "certifications": certifications,
    }


def parse_resume_pdf(path: str) -> Dict:
    raw_text = extract_text_from_pdf(path)
    contact = extract_contact_info(raw_text)
    summary = extract_summary(raw_text)

    sections = {"projects": [], "experience": [], "internships": []}
    lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
    for line in lines:
        low = line.lower()
        if any(x in low for x in ["project", "internship", "experience"]):
            sections["projects"].append(line)
        if "intern" in low and "experience" in low:
            sections["internships"].append(line)
        if any(x in low for x in ["company", "worked", "developed", "built"]):
            sections["experience"].append(line)

    return {
        "name": contact["name"],
        "email": contact["email"],
        "phone": contact["phone"],
        "skills": summary["skills"],
        "education": summary["education"],
        "certifications": summary["certifications"],
        "projects": sections["projects"],
        "experience": sections["experience"],
        "internships": sections["internships"],
        "tools": [skill for skill in summary["skills"] if skill.lower() in ["docker", "aws", "gcp", "azure", "git"]],
    }
