import pandas as pd

df = pd.read_csv("dataset/cleaned_reviews.csv")

# Separate classes
positive = df[df['Sentiment'] == 'Positive']
negative = df[df['Sentiment'] == 'Negative']

# Balance
min_count = min(len(positive), len(negative))

df_balanced = pd.concat([
    positive.sample(min_count, random_state=42),
    negative.sample(min_count, random_state=42)
])

# Shuffle
df_balanced = df_balanced.sample(frac=1).reset_index(drop=True)

df_balanced.to_csv("dataset/balanced_reviews.csv", index=False)

print("Balanced dataset created ✅")