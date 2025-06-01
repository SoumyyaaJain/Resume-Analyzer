# Resume-Analyzer
Resume Analyzer is an AI-powered web application that evaluates resumes for job readiness, role prediction, skill matching, ATS-friendliness, and job recommendation. It utilizes Natural Language Processing (NLP) and Machine Learning (ML) to analyze the quality, structure, and relevance of resumes across multiple domains. Built with Python and Streamlit for an interactive UI.

## Prerequisites
1. Python 3.8+
 - pip or pipenv

2. Required Python libraries:
 - streamlit
 - scikit-learn
 - pandas
 - numpy
 - joblib
 - nltk
 - pdfminer.six
 - python-docx

3. Install all dependencies:
 - pip install -r requirements.txt

## Project Structure Overview
<img width="628" alt="image" src="https://github.com/user-attachments/assets/65b5bf6b-6143-4b1d-b6c3-fda52b3d6ecc" />

## How to Run This Project

1. Clone the Repository:
 - git clone https://github.com/yourusername/resume-analyzer.git
 - cd resume-analyzer

2. Install Requirements:
 - pip install -r requirements.txt

3. Train the Model (Optional):
 - python train_model.py

4. Run the Web App:
 - streamlit run streamlit_app.py

## Feature Summary
 - Resume Parsing from PDF and DOCX
 - Job Role Prediction using trained ML model
 - Top 3 Role Suggestions with confidence scores
 - "Why this role?" Explanation feature using keyword mapping
 - Skill Gap Analysis between resume and job description
 - Job Matching Score using Cosine Similarity
 - ATS Compatibility Check (headers, format, tables, etc.)
 - Interactive Web UI using Streamlit

## Future Suggestions
 - Add Grammar & Readability Analysis using tools like TextStat or LanguageTool
 - Expand ML model using a larger, domain-diverse resume dataset
 - Integrate LinkedIn profile parser
 - Support real-time job scraping for direct matching
 - Add downloadable feedback reports (PDF) for users
 - Deploy the app using Docker or Streamlit Cloud









