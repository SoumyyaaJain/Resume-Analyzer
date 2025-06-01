import os
import re
from docx import Document
from pdfminer.high_level import extract_text as extract_pdf

STANDARD_HEADERS = ["summary", "objective", "education", "experience", "work experience", "projects", "skills", "certifications", "languages", "awards", "publications"]

def check_file_format(file_path):
    ext = os.path.splitext(file_path)[-1].lower()
    return ext in ['.pdf', '.docx'], ext

def detect_columns(text):
    # Naive check: columns often have short lines followed by whitespace and another block
    lines = text.split("\n")
    col_like = sum(1 for line in lines if len(line) < 40 and line.strip())
    return col_like > 20

def check_headers(text):
    found_headers = []
    for header in STANDARD_HEADERS:
        if re.search(rf"\b{header}\b", text, re.IGNORECASE):
            found_headers.append(header)
    missing_headers = list(set(STANDARD_HEADERS) - set(found_headers))
    return found_headers, missing_headers

def detect_tables_docx(file_path):
    doc = Document(file_path)
    return any(table for table in doc.tables)

def detect_tables_pdf(text):
    # Basic heuristic for tabular structure
    return bool(re.search(r'\|\s?.+\s?\|', text)) or "Table" in text

def ats_friendly_check(file_path, text):
    file_ok, ext = check_file_format(file_path)
    is_column = detect_columns(text)
    headers_found, headers_missing = check_headers(text)

    has_tables = False
    if ext == ".docx":
        has_tables = detect_tables_docx(file_path)
    else:
        has_tables = detect_tables_pdf(text)

    return {
        "file_ok": file_ok,
        "extension": ext,
        "multi_column": is_column,
        "tables_present": has_tables,
        "headers_found": headers_found,
        "headers_missing": headers_missing
    }
