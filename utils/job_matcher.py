import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def clean_text(text):
    return re.sub(r'[^\w\s]', '', text.lower())

def match_resume_to_jd(resume_text, jd_text):
    resume_clean = clean_text(resume_text)
    jd_clean = clean_text(jd_text)

    vectorizer = CountVectorizer(stop_words='english').fit([resume_clean, jd_clean])
    vectors = vectorizer.transform([resume_clean, jd_clean])
    similarity = cosine_similarity(vectors[0], vectors[1])[0][0]

    keywords = set(jd_clean.split()) - set(resume_clean.split())
    missing_keywords = sorted(list(keywords))[:10]

    suggestions = [f"Include the keyword '{word}' if relevant." for word in missing_keywords]

    return round(similarity * 100, 2), missing_keywords, suggestions
