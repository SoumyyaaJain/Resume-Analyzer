import re
from datetime import datetime
import spacy

# Load spaCy's English model
nlp = spacy.load("en_core_web_sm")

# Predefined lists for classification (can be extended or made ML-based)
HARD_SKILLS = ['python', 'java', 'excel', 'sql', 'machine learning', 'data analysis', 'c++', 'javascript', 'accounting', 'budgeting']
SOFT_SKILLS = ['communication', 'teamwork', 'leadership', 'adaptability', 'problem-solving', 'time management', 'creativity']

def classify_skills(text):
    text_lower = text.lower()
    hard = [skill for skill in HARD_SKILLS if skill in text_lower]
    soft = [skill for skill in SOFT_SKILLS if skill in text_lower]
    return list(set(hard)), list(set(soft))

def detect_employment_gaps(text):
    # Extract years
    years = re.findall(r'(20\d{2}|19\d{2})', text)
    years = sorted(set(map(int, years)))
    gaps = []
    for i in range(1, len(years)):
        gap = years[i] - years[i - 1]
        if gap > 1:
            gaps.append((years[i - 1], years[i]))
    return gaps

def is_chronological(text):
    years = re.findall(r'(20\d{2}|19\d{2})', text)
    years = list(map(int, years))
    return years == sorted(years, reverse=True)

def score_section(text):
    length_score = min(len(text.split()) / 100, 1.0)  # Up to 100 words = full score
    hard, soft = classify_skills(text)
    skill_score = min((len(hard) + len(soft)) / 10, 1.0)
    grammar_penalty = 0.1 if len(text.split()) > 0 and '.' not in text else 0.3
    return round((length_score + skill_score - grammar_penalty) * 50 + 50, 2)  # Scale to 100
