import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import joblib
import os

def train_and_save_model(csv_path='/Users/mayankshukla/Downloads/Resume Analyzer/gpt_dataset.csv'):
    # 1. Load the dataset
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"{csv_path} not found!")

    df = pd.read_csv(csv_path)

    # 2. Keep only the required columns
    df = df[['Resume', 'Category']].dropna()

    # 3. Remove extra whitespace
    df['Resume'] = df['Resume'].apply(lambda x: x.strip())

    # 4. Split into train/test
    X_train, X_test, y_train, y_test = train_test_split(
        df['Resume'], df['Category'], test_size=0.2, random_state=42
    )

    # 5. Create pipeline (TF-IDF + Naive Bayes)
    model = make_pipeline(
        TfidfVectorizer(stop_words='english'),
        MultinomialNB()
    )

    # 6. Train the model
    model.fit(X_train, y_train)

    # 7. Save the trained model
    joblib.dump(model, 'utils/job_classifier.pkl')
    print("✅ Model trained and saved as utils/job_classifier.pkl")

# Run directly from terminal
if __name__ == '__main__':
    train_and_save_model()
