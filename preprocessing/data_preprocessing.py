import pandas as pd

# Load dataset
df = pd.read_csv("dataset/reviews.csv")

# Take only 15000 rows
df = df.sample(n=15000, random_state=42)

# Save new dataset
df.to_csv("dataset/filtered_reviews.csv", index=False)

print("Dataset filtered successfully!")