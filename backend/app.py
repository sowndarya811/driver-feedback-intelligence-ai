from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.utils.predict import predict_sentiment

app = FastAPI(title="Driver Feedback Intelligence AI")

# ✅ CORS FIX
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Request Model
# -----------------------------
class ReviewRequest(BaseModel):
    text: str

# -----------------------------
# Root API
# -----------------------------
@app.get("/")
def home():
    return {
        "message": "Driver Feedback Intelligence AI API Running"
    }

# -----------------------------
# Predict API
# -----------------------------
@app.post("/predict")
def predict(data: ReviewRequest):

    result = predict_sentiment(data.text)

    return result