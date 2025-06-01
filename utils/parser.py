from pdfminer.high_level import extract_text as extract_pdf
from docx import Document
import os
import re

def extract_text_from_file(file_path):
    ext = os.path.splitext(file_path)[-1].lower()
    if ext == '.pdf':
        return extract_pdf(file_path)
    elif ext == '.docx':
        doc = Document(file_path)
        return '\n'.join([para.text for para in doc.paragraphs])
    else:
        raise ValueError("Unsupported file type")

def extract_basic_info(text):
    lines = text.strip().split('\n')
    lines = [line.strip() for line in lines if line.strip()]
    
    # Assume name is the first non-empty line and does not contain email/phone
    probable_name = None
    for line in lines[:5]:  # check first few lines
        if not re.search(r'@|https?://|\d', line):
            probable_name = line
            break

    email = re.findall(r'\b[\w.-]+?@\w+?\.\w+?\b', text)
    phone = re.findall(r'\+?\d[\d\s()-]{8,}\d', text)
    linkedin = re.findall(r'https?://(www\.)?linkedin\.com/in/[A-Za-z0-9_-]+', text)
    github = re.findall(r'https?://(www\.)?github\.com/[A-Za-z0-9_-]+', text)
    portfolio = re.findall(r'https?://(?!www\.linkedin\.com|www\.github\.com)[^\s]+', text)

    return {
        "name": probable_name,
        "email": email[0] if email else None,
        "phone": phone[0] if phone else None,
        "linkedin": linkedin[0] if linkedin else None,
        "github": github[0] if github else None,
        "portfolio": portfolio[0] if portfolio else None
    }

