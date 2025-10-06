import sys
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from app.main_gui import DetectionThread
from PyQt6.QtCore import QCoreApplication

def test_multilingual_detection():
    test_cases = [
        {
            "text": "Breaking: Scientists discover new planet in our solar system. The discovery was made using advanced telescopes and confirmed by multiple research teams.",
            "language": "en",
            "expected": "GENUINE"
        },
        {
            "text": "SHOCKING: This one weird trick will make you rich overnight! Click here now to learn the secret that banks don't want you to know!",
            "language": "en", 
            "expected": "FAKE"
        },
        {
            "text": "वैज्ञानिकों ने सौर मंडल में नया ग्रह खोजा। यह खोज उन्नत दूरबीनों का उपयोग करके की गई थी और कई शोध दलों द्वारा पुष्टि की गई थी।",
            "language": "hi",
            "expected": "GENUINE"
        },
        {
            "text": "वैज्ञानिकांनी आपल्या सौरमंडळात नवीन ग्रह शोधला. ही शोध प्रगत दुर्बिणींचा वापर करून केली गेली आणि अनेक संशोधन संघांनी पुष्टी केली.",
            "language": "mr",
            "expected": "GENUINE"
        }
    ]
    
    print(" Testing Multilingual Fake News Detection System")
    print("=" * 60)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest Case {i}:")
        print(f"Language: {test_case['language']}")
        print(f"Text: {test_case['text'][:100]}...")
        print(f"Expected: {test_case['expected']}")
        
        
        app = QCoreApplication(sys.argv)
        
        
        thread = DetectionThread(test_case['text'], test_case['language'])
        
       
        def handle_result(result):
            verdict = "FAKE" if result['is_fake'] else "GENUINE"
            confidence = result['confidence'] * 100
            print(f"Result: {verdict} (Confidence: {confidence:.1f}%)")
            print(f"Detected Language: {result['detected_language']}")
            if result['translation']:
                print(f"Translation: {result['translation'][:100]}...")
            print(" Test completed")
            app.quit()
        
        def handle_error(error):
            print(f"❌ Error: {error}")
            app.quit()
        
        thread.finished.connect(handle_result)
        thread.error.connect(handle_error)
        
       
        thread.start()
        app.exec()

if __name__ == "__main__":
    test_multilingual_detection()



