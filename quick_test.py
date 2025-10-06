import sys
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

def test_quick():
    
    
    print(" Quick Test - Multilingual Fake News Detection")
    print("=" * 50)
    
    
    hindi_text = "नई दिल्ली में आज एक नई मेट्रो लाइन का उद्घाटन किया गया। यह लाइन शहर के पूर्वी और पश्चिमी हिस्सों को जोड़ेगी। यात्रियों को इससे काफी राहत मिलेगी।"
    
    print(f"Testing Hindi text: {hindi_text[:50]}...")
    
    try:
        
        from app.main_gui import DetectionThread
        from PyQt6.QtCore import QCoreApplication
        
       
        app = QCoreApplication(sys.argv)
        
        
        thread = DetectionThread(hindi_text, 'hi')
        
        def handle_result(result):
            verdict = "FAKE" if result['is_fake'] else "GENUINE"
            confidence = result['confidence'] * 100
            print(f" Result: {verdict} (Confidence: {confidence:.1f}%)")
            print(f" Detected Language: {result['detected_language']}")
            if result['translation']:
                print(f" Translation: {result['translation'][:100]}...")
            print(" Test completed successfully!")
            app.quit()
        
        def handle_error(error):
            print(f" Error: {error}")
            app.quit()
        
        thread.finished.connect(handle_result)
        thread.error.connect(handle_error)
        
        
        thread.start()
        app.exec()
        
    except Exception as e:
        print(f" Test failed: {e}")

if __name__ == "__main__":
    test_quick()



