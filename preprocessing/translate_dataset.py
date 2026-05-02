import pandas as pd
from deep_translator import GoogleTranslator

# ✅ Load SMALL dataset (important)
df = pd.read_csv("dataset/reviews_small.csv")
df = df.sample(n=200)

# ✅ Show column names (for verification)
print("Columns:", df.columns)

# ✅ Set correct column name (based on your dataset)
text_column = "Review"

# ✅ Initialize translator
translator = GoogleTranslator(source='auto', target='en')

translated_reviews = []

print("Translating... please wait ⏳")

# 🔁 Loop through each review
for i, text in enumerate(df[text_column]):
    try:
        if isinstance(text, str) and text.strip() != "":
            translated = translator.translate(text)
        else:
            translated = ""
    except Exception as e:
        translated = ""

    translated_reviews.append(translated)

    # ✅ Progress update
    if i % 100 == 0:
        print(f"Processed {i} rows")

# ✅ Replace original column with translated text
df[text_column] = translated_reviews

# ✅ Save translated dataset
df.to_csv("dataset/reviews_english.csv", index=False)

print("✅ Translation completed successfully!")