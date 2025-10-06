import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.utils import Bunch
import joblib
import os
import sys
from tqdm import tqdm
import nltk
from textblob import TextBlob
from scipy import sparse


def ensure_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")

ensure_directory('models')

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from scripts.utils import preprocess_text

def load_data(sample_size=10000):
    required_files = {
        "data/True.csv": "true news articles",
        "data/Fake.csv": "fake news articles"
    }
    for file_path, description in required_files.items():
        if not os.path.exists(file_path):
            print(f" Error: Could not find {description} at {file_path}")
            return None, None
    try:
        print(" Loading true news articles...")
        true_df = pd.read_csv("data/True.csv").sample(n=sample_size, random_state=42)
        print(f" Loaded {len(true_df)} true news articles")
        print(" Loading fake news articles...")
        fake_df = pd.read_csv("data/Fake.csv").sample(n=sample_size, random_state=42)
        print(f" Loaded {len(fake_df)} fake news articles")
        return true_df, fake_df
    except Exception as e:
        print(f" Error loading data: {str(e)}")
        return None, None

def extract_numeric_features(text, is_non_english):
    text = str(text)
    blob = TextBlob(text)
    length = len(text)
    word_count = len(text.split())
    avg_word_length = length / (word_count + 1)
    capitals_ratio = sum(1 for c in text if c.isupper()) / (length + 1)
    numbers_ratio = sum(c.isdigit() for c in text) / (length + 1)
    sentiment = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    exclamations = text.count('!')
    questions = text.count('?')
    quotes = text.count('"') + text.count("'")
    return {
        'length': length,
        'word_count': word_count,
        'avg_word_length': avg_word_length,
        'capitals_ratio': capitals_ratio,
        'numbers_ratio': numbers_ratio,
        'sentiment': sentiment,
        'subjectivity': subjectivity,
        'exclamations': exclamations,
        'questions': questions,
        'quotes': quotes,
        'is_non_english': 1 if is_non_english else 0
    }

def main():
    try:
        nltk.download('punkt')
    except:
        pass

    true_df, fake_df = load_data(sample_size=10000)
    if true_df is None or fake_df is None:
        print(" Failed to load required data files")
        sys.exit(1)

    true_df['label'] = 1
    fake_df['label'] = 0

    df = pd.concat([true_df, fake_df]).sample(frac=1, random_state=42).reset_index(drop=True)

    print(" Preprocessing text...")
    cleaned_texts = []
    for text in tqdm(df['text'], desc="Cleaning text"):
        cleaned_text, _ = preprocess_text(text)
        cleaned_texts.append(cleaned_text)
    df['clean_text'] = cleaned_texts
    print(" Text preprocessing complete")

    print(" Extracting features...")
    # Training data is English; set is_non_english=0 to mirror inference flag
    num_features_list = []
    for text in tqdm(df['text'], desc="Numeric features"):
        num_features_list.append(extract_numeric_features(text, is_non_english=False))
    df_num = pd.DataFrame(num_features_list)

    X_text = df['clean_text']
    num_feature_columns = ['length', 'word_count', 'avg_word_length', 'capitals_ratio',
                           'numbers_ratio', 'sentiment', 'subjectivity', 'exclamations',
                           'questions', 'quotes', 'is_non_english']
    X_num = df_num[num_feature_columns]
    y = df['label']

    print(" Creating vectorizers...")
    word_vectorizer = TfidfVectorizer(
        max_features=20000,
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.95,
        strip_accents='unicode'
    )
    char_vectorizer = TfidfVectorizer(
        analyzer='char',
        ngram_range=(3, 5),
        min_df=2,
        max_df=1.0
    )

    X_train_text, X_test_text, X_train_num, X_test_num, y_train, y_test = train_test_split(
        X_text, X_num, y, test_size=0.2, random_state=42, stratify=y
    )

    print(" Vectorizing text (word & char)...")
    X_train_word = word_vectorizer.fit_transform(X_train_text)
    X_test_word = word_vectorizer.transform(X_test_text)
    X_train_char = char_vectorizer.fit_transform(X_train_text)
    X_test_char = char_vectorizer.transform(X_test_text)

    print(" Scaling numeric features...")
    scaler = StandardScaler(with_mean=False)
    X_train_num_scaled = scaler.fit_transform(X_train_num.astype(float))
    X_test_num_scaled = scaler.transform(X_test_num.astype(float))

    print(" Combining features (sparse)...")
    X_train_combined = sparse.hstack([X_train_word, X_train_char, X_train_num_scaled]).tocsr()
    X_test_combined = sparse.hstack([X_test_word, X_test_char, X_test_num_scaled]).tocsr()

    print(" Training calibrated Linear SVM...")
    base_svm = LinearSVC(C=1.0, class_weight='balanced', max_iter=5000)
    model = CalibratedClassifierCV(estimator=base_svm, method='sigmoid', cv=3)
    model.fit(X_train_combined, y_train)

    print(" Evaluating model...")
    y_pred = model.predict(X_test_combined)
    conf_matrix = confusion_matrix(y_test, y_pred)
    class_report = classification_report(y_test, y_pred)
    print("\nConfusion Matrix:")
    print(conf_matrix)
    print("\nClassification Report:")
    print(class_report)

    feature_names_word = list(word_vectorizer.get_feature_names_out())
    feature_names_char = [f"<char:{f}>" for f in char_vectorizer.get_feature_names_out()]
    combined_feature_names = feature_names_word + feature_names_char + num_feature_columns

    print(" Saving artifacts...")
    joblib.dump(model, "models/news_svm_calibrated.pkl")
    joblib.dump(word_vectorizer, "models/tfidf_word.pkl")
    joblib.dump(char_vectorizer, "models/tfidf_char.pkl")
    joblib.dump(scaler, "models/num_scaler.pkl")
    joblib.dump(combined_feature_names, "models/feature_names.pkl")

    metadata = Bunch(
        model_type='CalibratedLinearSVC',
        num_feature_columns=num_feature_columns,
        word_vocab_size=len(feature_names_word),
        char_vocab_size=len(feature_names_char),
        confusion_matrix=conf_matrix,
        classification_report=class_report
    )
    joblib.dump(metadata, "models/model_metadata.pkl")
    print(" All files saved successfully!")

if __name__ == "__main__":
    main()
