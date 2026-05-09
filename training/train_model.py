import os
import pandas as pd
import numpy as np
import pickle

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense

# -----------------------------
# 📁 PATH SETUP
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 👉 CHANGE FILE NAME HERE IF NEEDED
DATA_PATH = os.path.join(BASE_DIR, "datasets", "balanced_review.csv")

MODEL_DIR = os.path.join(BASE_DIR, "backend", "model")

# Create model folder if not exists
os.makedirs(MODEL_DIR, exist_ok=True)

# -----------------------------
# 🔍 DEBUG INFO
# -----------------------------
print("📂 DATA PATH:", DATA_PATH)
print("📁 DATASET FOLDER EXISTS:", os.path.exists(os.path.join(BASE_DIR, "datasets")))

if os.path.exists(os.path.join(BASE_DIR, "datasets")):
    print("📄 FILES INSIDE DATASETS:", os.listdir(os.path.join(BASE_DIR, "datasets")))

print("📄 FILE EXISTS:", os.path.exists(DATA_PATH))

# -----------------------------
# ❌ STOP IF FILE NOT FOUND
# -----------------------------
if not os.path.exists(DATA_PATH):
    raise FileNotFoundError("❌ Dataset file not found. Check file name and path!")

# -----------------------------
# 📊 LOAD DATASET
# -----------------------------
print("📊 Loading dataset...")
df = pd.read_csv(DATA_PATH)

# -----------------------------
# 🧹 CLEAN DATA
# -----------------------------
# Fix column names if needed
df = df.rename(columns={
    "review": "Review",
    "sentiment": "Sentiment"
})

# Remove empty rows
df = df.dropna()

# Ensure correct columns exist
if "Review" not in df.columns or "Sentiment" not in df.columns:
    raise ValueError("❌ Dataset must contain 'Review' and 'Sentiment' columns")

texts = df["Review"].astype(str)
labels = df["Sentiment"].astype(str)

print("✅ Dataset Loaded:", len(df))

# -----------------------------
# 🔠 ENCODE LABELS
# -----------------------------
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(labels)

# -----------------------------
# 🧠 TOKENIZATION
# -----------------------------
tokenizer = Tokenizer(num_words=5000)
tokenizer.fit_on_texts(texts)

X = tokenizer.texts_to_sequences(texts)
X = pad_sequences(X, maxlen=100)

# -----------------------------
# ✂️ TRAIN TEST SPLIT
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -----------------------------
# 🤖 MODEL BUILDING
# -----------------------------
model = Sequential([
    Embedding(input_dim=5000, output_dim=64, input_length=100),
    LSTM(64),
    Dense(32, activation='relu'),
    Dense(1, activation='sigmoid')
])

model.compile(
    loss='binary_crossentropy',
    optimizer='adam',
    metrics=['accuracy']
)

# -----------------------------
# 🏋️ TRAIN MODEL
# -----------------------------
print("🚀 Training started...")
model.fit(X_train, y_train, epochs=3, batch_size=32)

# -----------------------------
# 💾 SAVE FILES
# -----------------------------
model.save(os.path.join(MODEL_DIR, "sentiment_model.h5"))

with open(os.path.join(MODEL_DIR, "tokenizer.pkl"), "wb") as f:
    pickle.dump(tokenizer, f)

with open(os.path.join(MODEL_DIR, "label_encoder.pkl"), "wb") as f:
    pickle.dump(label_encoder, f)

print("✅ Model, Tokenizer, Label Encoder saved successfully!")