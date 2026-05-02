import pandas as pd

# Load original dataset
df = pd.read_csv("dataset/reviews.csv")

# Take only 2000 rows
df_small = df.sample(n=2000, random_state=42)

# Save new dataset
df_small.to_csv("dataset/reviews_small.csv", index=False)

print("✅ Small dataset created!")
print("Rows:", len(df_small))