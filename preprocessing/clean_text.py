import pandas as pd
import re
import os

# ✅ Correct path handling
base_path = os.path.dirname(os.path.dirname(__file__))
file_path = os.path.join(base_path, "dataset", "reviews_small.csv")

# Load dataset
df = pd.read_csv(file_path)

print("Columns:", df.columns)

# ✅ Use correct column name
text_column = "Review"

# Convert to string and lowercase
df[text_column] = df[text_column].astype(str).str.lower()

# Remove special characters, numbers, emojis
df[text_column] = df[text_column].apply(lambda x: re.sub(r'[^a-zA-Z\s]', '', x))

# Remove extra spaces
df[text_column] = df[text_column].apply(lambda x: re.sub(r'\s+', ' ', x).strip())

print("\nSample cleaned data:")
print(df[text_column].head())

# ✅ Save cleaned dataset
output_path = os.path.join(base_path, "dataset", "cleaned_reviews.csv")
df.to_csv(output_path, index=False)

print("\n✅ Text cleaning completed!")
print("Saved at:", output_path)