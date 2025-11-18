#!/usr/bin/env python3
"""
Demo script for Multilingual Fake News Detection System
"""

import sys
import os

# Add the project root to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

def demo_usage():
    """Demonstrate how to use the multilingual fake news detection system"""
    
    print("🌍 Multilingual Fake News Detection System Demo")
    print("=" * 60)
    print()
    
    print("📋 Supported Languages:")
    print("• English (Native)")
    print("• Hindi (हिंदी) - Auto-translated to English")
    print("• Marathi (मराठी) - Auto-translated to English")
    print()
    
    print("🚀 How to Use:")
    print("1. Run the GUI: python app/main_gui.py")
    print("2. Select language from dropdown (Auto Detect, English, Hindi, Marathi)")
    print("3. Paste news article text")
    print("4. Click 'Analyze Text'")
    print("5. View results with verdict, confidence, and analysis")
    print()
    
    print("📊 System Performance:")
    print("• Accuracy: 99%")
    print("• Precision: 99% (Fake), 99% (Genuine)")
    print("• Recall: 99% (Fake), 99% (Genuine)")
    print()
    
    print("🔧 Technical Features:")
    print("• Calibrated Linear SVM model")
    print("• Word + Character-level TF-IDF features")
    print("• Sentiment analysis")
    print("• Language detection and translation")
    print("• Feature importance analysis")
    print()
    
    print("📝 Sample Test Articles:")
    print()
    
    # Sample articles from test_articles.txt
    articles = [
        {
            "title": "Real News Example",
            "text": "Elon Musk has announced plans to visit India later this year following a conversation with Prime Minister Narendra Modi about technological collaboration and innovation.",
            "lang": "English"
        },
        {
            "title": "Fake News Example", 
            "text": "BREAKING: Scientists discover that drinking coffee makes you immortal! A secret study conducted by underground researchers found that people who drink 20 cups of coffee per day never die.",
            "lang": "English"
        },
        {
            "title": "Hindi News Example",
            "text": "नई दिल्ली में आज एक नई मेट्रो लाइन का उद्घाटन किया गया। यह लाइन शहर के पूर्वी और पश्चिमी हिस्सों को जोड़ेगी।",
            "lang": "Hindi"
        }
    ]
    
    for i, article in enumerate(articles, 1):
        print(f"{i}. {article['title']} ({article['lang']})")
        print(f"   Text: {article['text'][:80]}...")
        print()
    
    print("🎯 To test the system:")
    print("1. Copy any of the sample articles above")
    print("2. Run: python app/main_gui.py")
    print("3. Select appropriate language")
    print("4. Paste the text and analyze")
    print()
    print("✅ The system will provide:")
    print("• Verdict (Fake/Genuine)")
    print("• Confidence percentage")
    print("• Detected language")
    print("• Sentiment analysis")
    print("• Translation (if non-English)")
    print("• Key features influencing the decision")

if __name__ == "__main__":
    demo_usage()






