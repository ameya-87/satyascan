#!/usr/bin/env python3
"""
Quick start script for SatyaScan Website
"""

import sys
import os

# Check if models exist
models_dir = "models"
required_models = [
    "news_svm_calibrated.pkl",
    "tfidf_word.pkl",
    "tfidf_char.pkl",
    "num_scaler.pkl",
    "feature_names.pkl",
    "model_metadata.pkl"
]

print("=" * 60)
print("SatyaScan - AI-Powered News Verification")
print("=" * 60)
print()

# Check for model files
missing_models = []
for model_file in required_models:
    model_path = os.path.join(models_dir, model_file)
    if not os.path.exists(model_path):
        missing_models.append(model_file)

if missing_models:
    print("⚠️  Warning: Missing model files:")
    for model in missing_models:
        print(f"   - {model}")
    print()
    print("Please train the models first by running:")
    print("   python scripts/model_training.py")
    print()
    response = input("Continue anyway? (y/n): ")
    if response.lower() != 'y':
        print("Exiting...")
        sys.exit(1)
else:
    print("✅ All model files found!")
    print()

print("Starting Flask server...")
print("Open your browser and navigate to: http://localhost:5000")
print("Press Ctrl+C to stop the server")
print("=" * 60)
print()

# Import and run the Flask app
try:
    from app import app, load_models
    
    if load_models():
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("❌ Failed to load models. Please check the models directory.")
        sys.exit(1)
except KeyboardInterrupt:
    print("\n\nServer stopped by user.")
except Exception as e:
    print(f"\n❌ Error starting server: {str(e)}")
    sys.exit(1)

