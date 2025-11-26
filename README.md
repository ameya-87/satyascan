# Multilingual Fake News Detection System

## Project Overview
This project implements a machine learning-based system for detecting fake news across 13+ Indian languages. The system combines natural language processing, machine learning, and a user-friendly graphical interface to help users identify potential fake news articles.

## Key Features
- **Multilingual Support**: Supports 13+ Indian languages (English, Hindi, Marathi, Tamil, Telugu, Bengali, Gujarati, Kannada, Malayalam, Punjabi, Odia, Urdu, Assamese) with automatic language detection and translation
- **Real-time Analysis**: Instant feedback on news article authenticity
- **Advanced Feature Analysis**: 
  - Combined word and character-level TF-IDF features
  - Text content analysis
  - Sentiment analysis
  - Writing style metrics
  - Statistical patterns
  - Language-specific features
- **Detailed Results**:
  - Verdict (Fake/Genuine)
  - Confidence score
  - Detected language
  - Key influencing features
  - Sentiment analysis
  - Translation (if applicable)

## Technical Architecture

### 1. Machine Learning Model
- **Algorithm**: Calibrated Linear SVM with balanced class weights
- **Performance Metrics**:
  - Accuracy: 99%
  - Precision: 0.99 (Fake), 0.99 (Genuine)
  - Recall: 0.99 (Fake), 0.99 (Genuine)
  - F1-Score: 0.99 (both classes)
- **Features**:
  - Word-level TF-IDF features (20,000 dimensions)
  - Character-level TF-IDF features (3-5 grams)
  - Document length and word count
  - Average word length
  - Capitalization ratio
  - Number density
  - Sentiment polarity
  - Subjectivity score
  - Punctuation patterns (!, ?, quotes)
  - Language flag (non-English indicator)

### 2. Text Processing Pipeline
1. Language detection (auto or manual selection)
2. Translation (All Indian languages → English)
3. Text preprocessing
4. Feature extraction (word + character + numeric)
5. Feature scaling
6. Prediction with calibrated probabilities

### 3. Graphical User Interface
- Built with PyQt6
- Language selection dropdown (Auto Detect + 13 Indian languages)
- Clean, intuitive design
- Real-time analysis
- Progress indication
- Color-coded results
- Detailed feature importance display
- Language detection feedback

## Project Structure
```
multilingual_fake_news/
├── app/
│   └── main_gui.py        # GUI implementation
├── scripts/
│   ├── model_training.py  # Model training script
│   └── utils.py          # Utility functions
├── models/               # Saved model files
│   ├── news_svm_calibrated.pkl
│   ├── tfidf_word.pkl
│   ├── tfidf_char.pkl
│   ├── num_scaler.pkl
│   ├── feature_names.pkl
│   └── model_metadata.pkl
└── data/                # Training data
    ├── True.csv
    └── Fake.csv
```

## Model Training Details

### Dataset
- **Size**: 20,000 articles (balanced)
  - 10,000 genuine news articles
  - 10,000 fake news articles
- **Source**: Combination of verified news sources and known fake news articles

### Training Process
1. **Data Preprocessing**:
   - Text cleaning
   - Language normalization
   - Feature extraction

2. **Model Selection**:
   - Calibrated Linear SVM
   - Optimized hyperparameters:
     - C: 1.0
     - class_weight: balanced
     - solver: lbfgs
     - max_iter: 5000

3. **Feature Engineering**:
   - Word-level TF-IDF (1-2 grams)
   - Character-level TF-IDF (3-5 grams)
   - 11 numeric features including language flag

### Performance Analysis
```
Confusion Matrix:
[[1988   12]
 [  12 1988]]

Classification Report:
              precision    recall  f1-score   support
           0       0.99      0.99      0.99      2000
           1       0.99      0.99      0.99      2000
    accuracy                           0.99      4000
```

## Usage Instructions

### Installation
1. Clone the repository
2. Install required packages:
```bash
pip install -r requirements.txt
```

### Running the Application
1. Start the GUI:
```bash
python app/main_gui.py
```
2. Select language (Auto Detect or choose from 13+ Indian languages)
3. Paste news article text into the input area
4. Click "Analyze Text"
5. Review the results:
   - Verdict and confidence score
   - Detected language
   - Sentiment analysis
   - Key features influencing the decision
   - Translation (if applicable)

### CLI Inference
Run predictions for a file containing one article per line:
```bash
python scripts/predict.py --input_file test_articles.txt
```

Interactive (single input):
```bash
python scripts/predict.py
```

### Train From Scratch
Place `data/True.csv` and `data/Fake.csv` locally (not committed). Then:
```bash
python scripts/model_training.py
```
This will generate artifacts under `models/`:
- `news_svm_calibrated.pkl`, `tfidf_word.pkl`, `tfidf_char.pkl`, `num_scaler.pkl`, `feature_names.pkl`, `model_metadata.pkl`

## Tools Used (What and Why)
- scikit-learn: LinearSVC with probability calibration (CalibratedClassifierCV) for robust, fast linear classification and calibrated probabilities.
- PyQt6: Desktop GUI for interactive analysis and portfolio-friendly demo.
- TfidfVectorizer (word + char): Captures topical and stylistic cues; char n-grams help with misspellings and obfuscation often present in fake news.
- StandardScaler: Normalizes numeric features to comparable scale before concatenation with sparse text features.
- deep-translator (GoogleTranslator): Lightweight translation for non-English inputs (hi/mr → en) to keep a single English-trained model.
- langdetect: Language identification to decide when to translate and to set a non-English flag feature.
- TextBlob: Quick sentiment and subjectivity features to capture emotional tone common in misinformation.
- nltk: Stopwords for preprocessing pipeline.
- joblib: Persist/restore models and vectorizers.
- scipy.sparse: Efficiently combine large sparse text matrices with small dense numeric features.

## Research and Approach (Detailed)
### Problem & Constraints
Goal: Detect fake news across 13+ Indian languages with a lightweight, reproducible pipeline that runs locally and provides calibrated probabilities for user-facing UX.

Constraints and choices:
- Data primarily in English; Indian language availability is limited → translate all languages to English and train a single model.
- Favor fast, interpretable, CPU-friendly methods for a desktop GUI → LinearSVC with calibration.
- Provide user trust signals → show confidence scores, language detection, sentiment, and (when available) top features.

### Data & Preprocessing
- Sources: `data/True.csv` and `data/Fake.csv` (English). Text is normalized with lowercasing, punctuation/number removal, English stopword removal, and stemming.
- Non-English input: Detect with `langdetect`; translate to English using `deep-translator` (Google). Record a binary `is_non_english` flag.

### Feature Engineering
1) Word-level TF-IDF (1–2 grams, max_features≈20k) → topical content.
2) Character-level TF-IDF (3–5 grams) → stylistic patterns and robustness to obfuscation.
3) Numeric features (11): length, word_count, avg_word_length, capitals_ratio, numbers_ratio, sentiment, subjectivity, exclamations, questions, quotes, is_non_english. These capture tone and writing style often correlated with misinformation.

All numeric features are scaled with `StandardScaler` and concatenated with sparse text features via `scipy.sparse.hstack`.

### Model Selection & Calibration
- Base classifier: `LinearSVC(C=1.0, class_weight='balanced', max_iter=5000)` → strong linear baseline on high-dimensional sparse text.
- Probability calibration: `CalibratedClassifierCV(..., method='sigmoid', cv=3)` → reliable `predict_proba` for GUI confidence.

### Evaluation
- Split: stratified train/test. Metrics reported via confusion matrix and classification report.
- Observed behavior: high accuracy on English test set; confidence well-calibrated post calibration.

### Limitations & Ethics
- Translation noise: Edge cases may degrade accuracy for long or idiomatic non-English text.
- Domain shift: Model trained on dataset news; may over/under-flag in other domains (blogs/social).
- Explainability: Linear weights offer some transparency, but translation changes tokens; feature attributions are best-effort.
- Responsible use: Predictions are advisory; human verification recommended for consequential decisions.

### Alternatives Considered
- Multilingual transformers (mBERT/XLM-R): higher accuracy but heavier, less instant startup for a desktop GUI. Chosen linear model for portability and simplicity.

## File-by-File Guide
- `app/main_gui.py`: PyQt6 app. Loads artifacts, detects/optionally translates language, preprocesses, extracts numeric features, builds combined sparse features, predicts, and renders verdict/metrics. Robust to cases where model coefficients are unavailable for feature importance.
- `scripts/model_training.py`: Loads `data/Fake.csv` and `data/True.csv`, cleans text, builds word/char TF-IDF and numeric features, scales numeric features, trains Calibrated LinearSVC, evaluates, and saves artifacts + metadata including combined feature names.
- `scripts/predict.py`: CLI inference mirroring GUI pipeline. Supports `--input_file` for batch prediction, otherwise interactive. Uses the same artifacts as the GUI to avoid feature mismatch.
- `scripts/utils.py`: Common preprocessing: language detect, translate non-English to English, lowercase, punctuation/number removal, stopword removal, stemming; plus basic numeric feature utilities.
- `quick_test.py`: Smoke test using the GUI detection thread in a headless core application to validate end-to-end behavior for a Hindi sample.
- `test_multilingual.py`: Simple harness to exercise the detection thread across en/hi/mr.
- `data/` (local): Training CSVs (not committed). Provide instructions in README for obtaining them.
- `models/`: Trained artifacts generated by the training script.
- `demo.py`: Optional helper/demo script.

### Key Functions & Classes (Highlights)
- `app/main_gui.py`
  - `DetectionThread.run()`: Loads artifacts (`news_svm_calibrated.pkl`, TF-IDF vectorizers, scaler, feature names, metadata), detects/possibly translates language, preprocesses text, extracts numeric features, builds combined sparse matrix, predicts `predict`/`predict_proba`, assembles result dictionary for the UI.
  - `MainWindow`: Wires UI, handles `Analyze` click, and renders verdict, confidence, language, sentiment, optional translation, and top features (when coefficients available).
- `scripts/model_training.py`
  - `extract_numeric_features()`: Computes 11 numeric features aligned with inference.
  - `main()`: Loads data, preprocesses, vectorizes (word/char), scales numeric features, combines them, trains calibrated LinearSVC, evaluates, and saves artifacts plus metadata including combined `feature_names` order.
- `scripts/predict.py`
  - `predict_news(text)`: Mirrors GUI pipeline; supports batch file via `--input_file` for reproducible CLI demos.
- `scripts/utils.py`
  - `preprocess_text(text)`: Detects language, translates (if needed), normalizes and stems English text, filters English stopwords; returns cleaned text and detected language.

## Multilingual Support

### Supported Languages
- **English**: Native support
- **Hindi (हिंदी)**: Automatic translation to English
- **Marathi (मराठी)**: Automatic translation to English
- **Tamil (தமிழ்)**: Automatic translation to English
- **Telugu (తెలుగు)**: Automatic translation to English
- **Bengali (বাংলা)**: Automatic translation to English
- **Gujarati (ગુજરાતી)**: Automatic translation to English
- **Kannada (ಕನ್ನಡ)**: Automatic translation to English
- **Malayalam (മലയാളം)**: Automatic translation to English
- **Punjabi (ਪੰਜਾਬੀ)**: Automatic translation to English
- **Odia (ଓଡ଼ିଆ)**: Automatic translation to English
- **Urdu (اردو)**: Automatic translation to English
- **Assamese (অসমীয়া)**: Automatic translation to English

### Language Detection
- Automatic language detection using `langdetect`
- Manual language selection via dropdown
- Translation using Google Translate API

### Translation Process
1. Detect input language
2. Translate non-English text to English
3. Add language flag feature
4. Process translated text through ML pipeline

## Future Improvements
1. Support for additional regional languages and dialects
2. Deep learning models for better accuracy
3. URL input support for direct article analysis
4. Browser extension integration
5. Batch processing capability
6. API endpoint for integration with other services
7. Real-time news monitoring

## Dependencies
- Python 3.8+
- PyQt6
- scikit-learn
- numpy
- pandas
- textblob
- deep-translator
- nltk
- joblib
- scipy
- langdetect

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- Dataset providers
- Open-source ML libraries
- PyQt community
- Google Translate service
- Language detection libraries

