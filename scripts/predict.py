import joblib
from utils import preprocess_text
import numpy as np
import argparse
import sys
from deep_translator import GoogleTranslator
import langdetect
from textblob import TextBlob
from scipy import sparse


model = joblib.load("models/news_svm_calibrated.pkl")
word_vectorizer = joblib.load("models/tfidf_word.pkl")
char_vectorizer = joblib.load("models/tfidf_char.pkl")
scaler = joblib.load("models/num_scaler.pkl")
feature_names = joblib.load("models/feature_names.pkl")
metadata = joblib.load("models/model_metadata.pkl")

def _extract_numeric_features(raw_text: str, is_non_english: bool) -> dict:
    text = str(raw_text)
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

def predict_news(text):
    detected_lang = 'en'
    translated_text = text
    is_non_english = False
    try:
        detected_lang = langdetect.detect(text)
        if detected_lang not in ['en', 'english']:
            is_non_english = True
            translator = GoogleTranslator(source=detected_lang, target='en')
            translated_text = translator.translate(text)
    except Exception:
        detected_lang = 'unknown'
        translated_text = text

    processed_text, _ = preprocess_text(translated_text)
    if not processed_text:
        return " Unsupported or invalid input.", detected_lang, 0.0

 
    num_features = _extract_numeric_features(translated_text, is_non_english)
    num_array = np.array([[num_features[col] for col in metadata.num_feature_columns]])

   
    word_features = word_vectorizer.transform([processed_text])
    char_features = char_vectorizer.transform([processed_text])

   
    num_scaled = scaler.transform(num_array)

    
    X_combined = sparse.hstack([word_features, char_features, num_scaled]).tocsr()

    prediction = model.predict(X_combined)[0]
    probabilities = model.predict_proba(X_combined)[0]
    confidence = probabilities[1] if prediction == 1 else probabilities[0]

    result = " Real News" if prediction == 1 else " Fake News"
    return result, detected_lang, round(float(confidence) * 100, 2)

def main():
    parser = argparse.ArgumentParser(description="Fake news classifier (CLI)")
    parser.add_argument("--input_file", type=str, default=None, help="Path to a text file with one article per line")
    args = parser.parse_args()

    if args.input_file:
        try:
            with open(args.input_file, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f" Failed to read input file: {e}")
            sys.exit(1)

        print(f" Classifying {len(lines)} articles from {args.input_file}...")
        for idx, line in enumerate(lines, 1):
            result, lang, confidence = predict_news(line)
            print(f"\n—— Article {idx} ——")
            print(" Prediction:", result)
            print(" Detected Language:", lang)
            print(" Confidence Score:", confidence, "%")
        return

   
    try:
        user_input = input("📰 Enter the news text: ")
    except KeyboardInterrupt:
        print("\nCancelled.")
        sys.exit(1)
    result, lang, confidence = predict_news(user_input)
    print("\n Prediction:", result)
    print(" Detected Language:", lang)
    print(" Confidence Score:", confidence, "%")

if __name__ == "__main__":
    main()
