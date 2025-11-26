import sys
import os

# Add the project root to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QTextEdit, QPushButton, QLabel, QProgressBar, QComboBox)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
import joblib
import numpy as np
from deep_translator import GoogleTranslator
import langdetect
from textblob import TextBlob
from scipy import sparse
from scripts.utils import preprocess_text

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

class DetectionThread(QThread):
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, text, language='auto'):
        super().__init__()
        self.text = text
        self.language = language
        
    def run(self):
        try:
            # Load models
            print("Loading ML models...")
            model = joblib.load("models/news_svm_calibrated.pkl")
            word_vectorizer = joblib.load("models/tfidf_word.pkl")
            char_vectorizer = joblib.load("models/tfidf_char.pkl")
            scaler = joblib.load("models/num_scaler.pkl")
            feature_names = joblib.load("models/feature_names.pkl")
            metadata = joblib.load("models/model_metadata.pkl")
            print("Models loaded successfully!")
            
            # Detect language and translate if needed
            original_text = self.text
            translated_text = self.text
            detected_lang = 'en'
            is_non_english = False
            
            try:
                if self.language == 'auto':
                    detected_lang = langdetect.detect(self.text)
                else:
                    detected_lang = self.language
                
                if detected_lang not in ['en', 'english']:
                    is_non_english = True
                    translator = GoogleTranslator(source=detected_lang, target='en')
                    translated_text = translator.translate(self.text)
            except Exception as e:
                print(f"Translation error: {e}")
                translated_text = self.text
            
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
            
            # Try to derive feature importance from the underlying LinearSVC; if unavailable, fall back gracefully
            top_features = []
            try:
                calibrated = model.calibrated_classifiers_[0]
                base_estimator = getattr(calibrated, 'base_estimator', None) or getattr(calibrated, 'base_estimator_', None)
                if base_estimator is not None and hasattr(base_estimator, 'coef_'):
                    coef = base_estimator.coef_[0]
                    feature_importance = np.abs(coef)
                    top_indices = np.argsort(feature_importance)[-5:][::-1]
                    top_features = [(feature_names[i], coef[i]) for i in top_indices]
            except Exception:
                top_features = []
            # top_features already computed if coefficients were available; otherwise remains empty
            
            # Add sentiment analysis
            sentiment_info = {
                'sentiment': num_features['sentiment'],
                'subjectivity': num_features['subjectivity']
            }
            
            result = {
                'is_fake': prediction == 0,
                'confidence': float(confidence),
                'top_features': top_features,
                'translation': translated_text if translated_text != original_text else None,
                'sentiment': sentiment_info,
                'detected_language': detected_lang
            }
            
            self.finished.emit(result)
            
        except Exception as e:
            print(f"Error in detection thread: {str(e)}")
            self.error.emit(str(e))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        print("Initializing main window...")
        self.setWindowTitle("SatyaScan - Multilingual Fake News Detector (13+ Indian Languages)")
        self.setMinimumSize(800, 600)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Language selection
        lang_label = QLabel("Select Language:")
        self.language_combo = QComboBox()
        self.language_combo.addItems([
            'Auto Detect', 'English', 'Hindi', 'Marathi', 'Tamil', 'Telugu', 
            'Bengali', 'Gujarati', 'Kannada', 'Malayalam', 'Punjabi', 
            'Odia', 'Urdu', 'Assamese'
        ])
        
        # Create widgets
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("Paste news article text here...\nSupports 13+ Indian languages including Hindi, Tamil, Telugu, Bengali, Gujarati, Kannada, Malayalam, Punjabi, and more.")
        
        self.analyze_button = QPushButton("Analyze Text")
        self.analyze_button.clicked.connect(self.analyze_text)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        
        self.result_label = QLabel()
        self.result_label.setWordWrap(True)
        self.result_label.setStyleSheet("QLabel { padding: 10px; }")
        
        # Add widgets to layout
        layout.addWidget(lang_label)
        layout.addWidget(self.language_combo)
        layout.addWidget(self.text_input)
        layout.addWidget(self.analyze_button)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.result_label)
        
        print("Main window initialized successfully!")
    
    def analyze_text(self):
        text = self.text_input.toPlainText().strip()
        if not text:
            self.result_label.setText("Please enter some text to analyze.")
            return
        
        # Get selected language
        lang_map = {
            'Auto Detect': 'auto',
            'English': 'en',
            'Hindi': 'hi',
            'Marathi': 'mr',
            'Tamil': 'ta',
            'Telugu': 'te',
            'Bengali': 'bn',
            'Gujarati': 'gu',
            'Kannada': 'kn',
            'Malayalam': 'ml',
            'Punjabi': 'pa',
            'Odia': 'or',
            'Urdu': 'ur',
            'Assamese': 'as'
        }
        selected_lang = lang_map[self.language_combo.currentText()]
        
        self.analyze_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.result_label.setText("Analyzing...")
        
        self.thread = DetectionThread(text, selected_lang)
        self.thread.finished.connect(self.handle_result)
        self.thread.error.connect(self.handle_error)
        self.thread.start()
    
    def handle_result(self, result):
        verdict = "FAKE" if result['is_fake'] else "GENUINE"
        confidence = result['confidence'] * 100
        
        # Set color based on verdict
        color = "#ff4444" if result['is_fake'] else "#4CAF50"
        
        text = f"<h3 style='color: {color};'>Verdict: {verdict} (Confidence: {confidence:.1f}%)</h3>"
        
        # Add language info
        text += f"<p><b>Detected Language:</b> {result['detected_language']}</p>"
        
        # Add sentiment analysis
        sentiment = result['sentiment']
        sentiment_text = "Positive" if sentiment['sentiment'] > 0 else "Negative" if sentiment['sentiment'] < 0 else "Neutral"
        subjectivity_text = "Highly Subjective" if sentiment['subjectivity'] > 0.5 else "More Objective"
        
        text += f"<p><b>Sentiment Analysis:</b><br>"
        text += f"• Sentiment: {sentiment_text} ({sentiment['sentiment']:.2f})<br>"
        text += f"• Subjectivity: {subjectivity_text} ({sentiment['subjectivity']:.2f})</p>"
        
        if result['translation']:
            text += f"<p><b>Translated to English:</b><br>{result['translation']}</p>"
        
        text += "<p><b>Key features influencing this decision:</b></p><ul>"
        for feature, importance in result['top_features']:
            impact = "increases" if importance > 0 else "decreases"
            text += f"<li>'{feature}' {impact} likelihood of being genuine (weight: {abs(importance):.3f})</li>"
        text += "</ul>"
        
        self.result_label.setText(text)
        self.analyze_button.setEnabled(True)
        self.progress_bar.setVisible(False)
    
    def handle_error(self, error_message):
        self.result_label.setText(f"Error during analysis: {error_message}")
        self.analyze_button.setEnabled(True)
        self.progress_bar.setVisible(False)

def main():
    print("Starting application initialization...")
    print("Loading required libraries...")
    
    # Create application instance
    app = QApplication(sys.argv)
    print("Creating QApplication instance...")
    
    # Set application style
    app.setStyle('Fusion')
    print("Setting application style...")
    
    # Create and show main window
    print("Creating main window...")
    window = MainWindow()
    window.show()
    print("Application ready!")
    
    # Start event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 