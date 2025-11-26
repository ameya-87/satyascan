import re
from langdetect import detect
from deep_translator import GoogleTranslator
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
from textblob import TextBlob

import nltk
nltk.download('stopwords')

def extract_features(text):
    """Extract additional features from text"""
   
    if not isinstance(text, str) or text.strip() == "":
        return {
            'length': 0,
            'sentiment': 0,
            'subjectivity': 0,
            'exclamations': 0,
            'questions': 0,
            'capitals_ratio': 0,
            'numbers': 0
        }
    
    
    length = len(text.split())
    
    
    try:
        blob = TextBlob(text)
        sentiment = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
    except:
        sentiment = 0
        subjectivity = 0
    
   
    exclamation_count = text.count('!')
    question_count = text.count('?')
    
    
    capitals = sum(1 for c in text if c.isupper())
    capitals_ratio = capitals / len(text) if len(text) > 0 else 0
    
    
    numbers = len(re.findall(r'\d+', text))
    
    return {
        'length': length,
        'sentiment': sentiment,
        'subjectivity': subjectivity,
        'exclamations': exclamation_count,
        'questions': question_count,
        'capitals_ratio': capitals_ratio,
        'numbers': numbers
    }

def preprocess_text(text):
    
    if not isinstance(text, str) or text.strip() == "":
        return "", "unknown"

    try:
        lang = detect(text)
    except:
        lang = "unknown"

    # Supported Indian languages
    supported_languages = ['en', 'hi', 'mr', 'ta', 'te', 'bn', 'gu', 'kn', 'ml', 'pa', 'or', 'ur', 'as']
    if lang not in supported_languages:
        return "", "unsupported"

    if lang != 'en':
        try:
            text = GoogleTranslator(source='auto', target='en').translate(text)
        except:
            return "", lang

    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)

    stop_words = set(stopwords.words('english'))
    text = " ".join([word for word in text.split() if word not in stop_words])

    stemmer = SnowballStemmer("english")
    text = " ".join([stemmer.stem(word) for word in text.split()])

    return text, lang
