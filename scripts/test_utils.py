from scripts.utils import preprocess_text

# Test input in Hindi, Marathi, and English
hindi_text = "यह एक फ़र्ज़ी खबर है जो इंटरनेट पर फैल रही है।"
marathi_text = "ही बनावट बातमी आहे जी सोशल मिडीयावर पसरत आहे."
english_text = "This is a fake news article spreading rapidly."

# Run preprocessing
print(" Testing Hindi:")
cleaned_hi, lang_hi = preprocess_text(hindi_text)
print("Language:", lang_hi)
print("Cleaned:", cleaned_hi)
print("\n")

print(" Testing Marathi:")
cleaned_mr, lang_mr = preprocess_text(marathi_text)
print("Language:", lang_mr)
print("Cleaned:", cleaned_mr)
print("\n")

print(" Testing English:")
cleaned_en, lang_en = preprocess_text(english_text)
print("Language:", lang_en)
print("Cleaned:", cleaned_en)
