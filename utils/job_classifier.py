import os
import re
import joblib
import numpy as np

# Load the model pipeline (which already includes the vectorizer)
model_path = os.path.join(os.path.dirname(__file__), "job_classifier.pkl")
model = joblib.load(model_path)

def clean_text(text):
    text = re.sub(r"http\S+", "", text)  # remove URLs
    text = re.sub(r"\s+", " ", text)     # remove extra whitespaces
    text = re.sub(r"[^\w\s]", "", text)  # remove punctuation
    text = text.lower().strip()
    return text

def predict_job_role(resume_text):
    clean_resume = clean_text(resume_text)
    prediction = model.predict([clean_resume])[0]
    return prediction

def predict_with_confidence(resume_text, top_n=3):
    clean_resume = clean_text(resume_text)
    proba = model.predict_proba([clean_resume])[0]
    classes = model.classes_

    top_n_indices = np.argsort(proba)[::-1][:top_n]
    top_roles = [(classes[i], round(proba[i] * 100, 2)) for i in top_n_indices]

    return top_roles[0]  # return top prediction with confidence

def get_top_n_roles(resume_text, n=3):
    clean_resume = clean_text(resume_text)
    proba = model.predict_proba([clean_resume])[0]
    classes = model.classes_

    top_indices = np.argsort(proba)[::-1][:n]
    return [(classes[i], round(proba[i] * 100, 2)) for i in top_indices]

def explain_prediction(resume_text):
    top_roles = get_top_n_roles(resume_text, n=3)
    top_role, confidence = top_roles[0]

    explanation = f"The resume is most likely for the role of **{top_role}** based on the following:\n\n"

    if 'data' in top_role.lower():
        explanation += "- Frequent use of terms like *data*, *analysis*, *statistics* suggests a data-centric role.\n"
    elif 'software' in top_role.lower() or 'developer' in top_role.lower():
        explanation += "- Presence of coding, development, and software-related terminology fits engineering roles.\n"
    elif 'project' in top_role.lower() or 'manager' in top_role.lower():
        explanation += "- Use of project management vocabulary like *stakeholders*, *timeline*, and *deliverables* indicates a managerial role.\n"
    elif 'designer' in top_role.lower():
        explanation += "- Resume emphasizes visual tools, design principles, and portfolio links—strong designer indicators.\n"
    elif 'analyst' in top_role.lower():
        explanation += "- Use of analytical terms and decision-making frameworks aligns with analyst positions.\n"

    explanation += f"\n🔍 Model confidence in this prediction: **{confidence:.2f}%**"
    return explanation
