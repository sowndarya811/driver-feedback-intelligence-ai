# backend/utils/predict.py

import os
import pickle
import numpy as np

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

from backend.utils.preprocess import clean_text

# ---------------- BASE DIRECTORY ---------------- #

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "model"
)

# ---------------- LOAD MODEL ---------------- #

model = load_model(
    os.path.join(
        MODEL_DIR,
        "sentiment_model.h5"
    )
)

# ---------------- LOAD TOKENIZER ---------------- #

with open(
    os.path.join(
        MODEL_DIR,
        "tokenizer.pkl"
    ),
    "rb"
) as f:

    tokenizer = pickle.load(f)

# ---------------- LOAD LABEL ENCODER ---------------- #

with open(
    os.path.join(
        MODEL_DIR,
        "label_encoder.pkl"
    ),
    "rb"
) as f:

    label_encoder = pickle.load(f)

# ---------------- CHECK LABEL ORDER ---------------- #

print("LABEL ORDER:")
print(label_encoder.classes_)

# ---------------- PREDICTION FUNCTION ---------------- #

def predict_sentiment(text):

    # CLEAN TEXT

    cleaned_text = clean_text(text)

    # TEXT TO SEQUENCE

    sequence = tokenizer.texts_to_sequences(
        [cleaned_text]
    )

    # PAD SEQUENCE

    padded = pad_sequences(
        sequence,
        maxlen=100
    )

    # MODEL PREDICTION

    prediction = model.predict(
        padded
    )[0]

    # CONFIDENCE

    confidence = float(
        max(prediction)
    )

    # GET PREDICTED INDEX

    predicted_index = np.argmax(
        prediction
    )

    # GET SENTIMENT FROM LABEL ENCODER

    sentiment = (
        label_encoder
        .inverse_transform(
            [predicted_index]
        )[0]
    )

    # LOWERCASE TEXT

    text_lower = text.lower()

    # ---------------- NEUTRAL BALANCING ---------------- #

    neutral_words = [

        "average",

        "okay",

        "normal",

        "fine",

        "not bad",

        "medium",

        "moderate",

        "ordinary"
    ]

    if any(
        word in text_lower
        for word in neutral_words
    ):

        sentiment = "Neutral"

    # ---------------- POSITIVE BALANCING ---------------- #

    positive_words = [

        "excellent",

        "good",

        "great",

        "amazing",

        "best",

        "awesome",

        "useful",

        "nice",

        "love",

        "fantastic",

        "happy"
    ]

    if any(
        word in text_lower
        for word in positive_words
    ):

        sentiment = "Positive"

    # ---------------- NEGATIVE BALANCING ---------------- #

    negative_words = [

        "worst",

        "bad",

        "poor",

        "terrible",

        "hate",

        "slow",

        "waste",

        "issue",

        "problem",

        "disappointed"
    ]

    if any(
        word in text_lower
        for word in negative_words
    ):

        sentiment = "Negative"

    # ---------------- RETURN RESULT ---------------- #

    return {

        "sentiment": sentiment,

        "confidence": confidence
    }