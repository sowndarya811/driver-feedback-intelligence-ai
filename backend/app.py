from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

import numpy as np
import pandas as pd
import pickle
import io
import re
from collections import Counter

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences


# -------------------------------
# INIT APP
# -------------------------------
app = FastAPI()


# -------------------------------
# ENABLE CORS (VERY IMPORTANT)
# -------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------------
# LOAD MODEL + TOKENIZER
# -------------------------------
try:
    model = load_model("backend/model/sentiment_model.h5")

    with open("backend/model/tokenizer.pkl", "rb") as f:
        tokenizer = pickle.load(f)

    print("✅ Model & Tokenizer loaded successfully!")

except Exception as e:
    print("❌ Error loading model:", e)
    model = None
    tokenizer = None


# -------------------------------
# ROOT API
# -------------------------------
@app.get("/")
def home():
    return {"message": "🚀 Backend is running with AI model!"}


# -------------------------------
# SINGLE TEXT PREDICTION
# -------------------------------
@app.post("/predict")
async def predict(data: dict):
    try:
        if model is None or tokenizer is None:
            return {"error": "Model not loaded properly"}

        text = data.get("text", "")

        if text.strip() == "":
            return {"error": "Empty input text"}

        seq = tokenizer.texts_to_sequences([text])
        padded = pad_sequences(seq, maxlen=100)

        prediction = model.predict(padded, verbose=0)[0]

        sentiment_index = int(np.argmax(prediction))
        confidence = float(np.max(prediction)) * 100

        labels = ["Negative 😡", "Neutral 😐", "Positive 😊"]

        return {
            "sentiment": labels[sentiment_index],
            "confidence": round(confidence, 2)
        }

    except Exception as e:
        return {"error": str(e)}


# -------------------------------
# CSV UPLOAD + BULK ANALYSIS
# -------------------------------
@app.post("/upload_csv")
async def upload_csv(file: UploadFile = File(...)):
    try:
        if model is None or tokenizer is None:
            return {"error": "Model not loaded properly"}

        contents = await file.read()

        df = pd.read_csv(io.StringIO(contents.decode("utf-8")))

        # Detect column automatically
        if "Review" in df.columns:
            texts = df["Review"]
        elif "review" in df.columns:
            texts = df["review"]
        else:
            return {"error": "CSV must contain 'Review' column"}

        positive = 0
        negative = 0
        neutral = 0

        all_words = []

        for text in texts:
            text = str(text)

            # -------- Sentiment Prediction --------
            seq = tokenizer.texts_to_sequences([text])
            padded = pad_sequences(seq, maxlen=100)

            prediction = model.predict(padded, verbose=0)[0]
            sentiment_index = int(np.argmax(prediction))

            if sentiment_index == 2:
                positive += 1
            elif sentiment_index == 0:
                negative += 1
            else:
                neutral += 1

            # -------- Keyword Extraction --------
            words = re.findall(r'\b\w+\b', text.lower())
            all_words.extend(words)

        # -------- Top Keywords --------
        common_words = Counter(all_words).most_common(5)
        keywords = [word for word, _ in common_words]

        # -------- Insight Generation --------
        total = positive + negative + neutral

        if total == 0:
            insight = "No data available"
        elif positive > negative:
            insight = "😊 Overall sentiment is Positive"
        elif negative > positive:
            insight = "⚠️ Negative sentiment is high — users facing issues"
        else:
            insight = "😐 Mixed feedback from users"

        return {
            "positive": positive,
            "negative": negative,
            "neutral": neutral,
            "keywords": keywords,
            "insight": insight
        }

    except Exception as e:
        return {"error": str(e)}