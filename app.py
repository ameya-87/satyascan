from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sys
import os

# Add the project root to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

import joblib
import numpy as np
from deep_translator import GoogleTranslator
import langdetect
from textblob import TextBlob
from scipy import sparse
from scripts.utils import preprocess_text

app = Flask(__name__)
CORS(app)

# Global variables for loaded models
model = None
word_vectorizer = None
char_vectorizer = None
scaler = None
feature_names = None
metadata = None

def load_models():
    """Load ML models into memory"""
    global model, word_vectorizer, char_vectorizer, scaler, feature_names, metadata
    try:
        model = joblib.load("models/news_svm_calibrated.pkl")
        word_vectorizer = joblib.load("models/tfidf_word.pkl")
        char_vectorizer = joblib.load("models/tfidf_char.pkl")
        scaler = joblib.load("models/num_scaler.pkl")
        feature_names = joblib.load("models/feature_names.pkl")
        metadata = joblib.load("models/model_metadata.pkl")
        print("Models loaded successfully!")
        return True
    except Exception as e:
        print(f"Error loading models: {str(e)}")
        return False

def extract_numeric_features(text, is_non_english):
    """Extract numeric features matching the trained model"""
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

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """API endpoint for fake news detection"""
    try:
        data = request.json
        text = data.get('text', '').strip()
        language = data.get('language', 'auto')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        if model is None:
            return jsonify({
                'error': 'Models not loaded. Please train the models first by running: python scripts/model_training.py'
            }), 503
        
        # Detect language and translate if needed
        original_text = text
        translated_text = text
        detected_lang = 'en'
        is_non_english = False
        
        try:
            if language == 'auto':
                detected_lang = langdetect.detect(text)
            else:
                detected_lang = language
            
            if detected_lang not in ['en', 'english']:
                is_non_english = True
                translator = GoogleTranslator(source=detected_lang, target='en')
                translated_text = translator.translate(text)
        except Exception as e:
            print(f"Translation error: {e}")
            translated_text = text
        
        # Preprocess text
        cleaned_text, _ = preprocess_text(translated_text)
        
        # Extract numeric features
        num_features = extract_numeric_features(translated_text, is_non_english)
        num_array = np.array([[num_features[col] for col in metadata.num_feature_columns]])
        
        # Transform text features
        word_features = word_vectorizer.transform([cleaned_text])
        char_features = char_vectorizer.transform([cleaned_text])
        
        # Scale numerical features
        num_scaled = scaler.transform(num_array)
        
        # Combine features (sparse)
        X_combined = sparse.hstack([word_features, char_features, num_scaled]).tocsr()
        
        # Make prediction
        prediction = model.predict(X_combined)[0]
        probabilities = model.predict_proba(X_combined)[0]
        confidence = probabilities[1] if prediction == 1 else probabilities[0]
        
        # Try to derive feature importance
        top_features = []
        try:
            calibrated = model.calibrated_classifiers_[0]
            base_estimator = getattr(calibrated, 'base_estimator', None) or getattr(calibrated, 'base_estimator_', None)
            if base_estimator is not None and hasattr(base_estimator, 'coef_'):
                coef = base_estimator.coef_[0]
                feature_importance = np.abs(coef)
                top_indices = np.argsort(feature_importance)[-5:][::-1]
                top_features = [(feature_names[i], float(coef[i])) for i in top_indices]
        except Exception:
            top_features = []
        
        # Add sentiment analysis
        sentiment_info = {
            'sentiment': float(num_features['sentiment']),
            'subjectivity': float(num_features['subjectivity'])
        }
        
        result = {
            'is_fake': bool(prediction == 0),
            'confidence': float(confidence),
            'top_features': top_features,
            'translation': translated_text if translated_text != original_text else None,
            'sentiment': sentiment_info,
            'detected_language': detected_lang
        }
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Error in analyze endpoint: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'models_loaded': model is not None
    })

if __name__ == '__main__':
    print("Loading ML models...")
    models_loaded = load_models()
    if not models_loaded:
        print("⚠️  Warning: Models not loaded. The website will start but analysis will not work.")
        print("   To train models, run: python scripts/model_training.py")
        print("   Make sure you have data/True.csv and data/Fake.csv files.")
        print()
    
    # Get port from environment variable (for cloud platforms) or use default
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    
    print("Starting Flask server...")
    if port != 5000:
        print(f"Server will be available at port {port}")
    else:
        print("Open your browser and navigate to: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    app.run(debug=debug_mode, host='0.0.0.0', port=port)

