import re

SECTION_HEADERS = [
    "objective", "summary", "education", "experience", "work experience",
    "skills", "certifications", "projects", "awards", "publications",
    "languages", "interests"
]

def extract_sections(text):
    lines = text.split('\n')
    sections = {}
    current_section = None

    for line in lines:
        clean_line = line.strip().lower()
        if any(header in clean_line for header in SECTION_HEADERS):
            current_section = clean_line
            sections[current_section] = []
        elif current_section:
            sections[current_section].append(line.strip())
    
    return {k: '\n'.join(v).strip() for k, v in sections.items()}
