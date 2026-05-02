import pandas as pd
import numpy as np
import pickle

from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense

# Load dataset
df = pd.read_csv("dataset/reviews.csv")

# Use correct column names
texts = df["Review"].astype(str)

# Convert sentiment to numbers
label_map = {"Positive": 2, "Neutral": 1, "Negative": 0}
labels = df["Sentiment"].map(label_map)

# Tokenization
tokenizer = Tokenizer(num_words=5000)
tokenizer.fit_on_texts(texts)

sequences = tokenizer.texts_to_sequences(texts)
X = pad_sequences(sequences, maxlen=100)

y = np.array(labels)

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Build LSTM model
model = Sequential()
model.add(Embedding(5000, 128, input_length=100))
model.add(LSTM(64))
model.add(Dense(32, activation="relu"))
model.add(Dense(3, activation="softmax"))

model.compile(
    loss="sparse_categorical_crossentropy",
    optimizer="adam",
    metrics=["accuracy"]
)

# Train
model.fit(X_train, y_train, epochs=5, batch_size=32)

# Save model
model.save("backend/model/sentiment_model.h5")

# Save tokenizer
with open("backend/model/tokenizer.pkl", "wb") as f:
    pickle.dump(tokenizer, f)

print("✅ Model training completed and saved!")