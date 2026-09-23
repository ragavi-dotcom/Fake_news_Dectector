import sqlite3
from pathlib import Path
from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from model import predict
from explain import explain_prediction

DB_PATH = Path(__file__).resolve().parent.parent / "predictions.db"

app = FastAPI(title="Fake News Detector API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ArticleIn(BaseModel):
    text: str = Field(..., min_length=20, description="Full article text")


class WordWeight(BaseModel):
    word: str
    weight: float  


class PredictionOut(BaseModel):
    label: str
    confidence: float
    words: list[WordWeight] = []


def _db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionOut)
def predict_endpoint(article: ArticleIn):
    try:
        result = predict(article.text)
    except FileNotFoundError:
        raise HTTPException(500, "Model not trained yet. Run the notebook first.")

    try:
        result["words"] = explain_prediction(article.text)
    except Exception:
        result["words"] = []

    try:
        with _db() as conn:
            conn.execute(
                "INSERT INTO predictions (text, label, confidence, created_at) "
                "VALUES (?, ?, ?, ?)",
                (article.text[:1000], result["label"],
                 result["confidence"], datetime.utcnow().isoformat()),
            )
    except sqlite3.OperationalError:
        pass  

    return result


@app.get("/history")
def history():
    try:
        with _db() as conn:
            rows = conn.execute(
                "SELECT id, substr(text,1,120) AS preview, label, confidence, created_at "
                "FROM predictions ORDER BY id DESC LIMIT 50"
            ).fetchall()
        return [dict(r) for r in rows]
    except sqlite3.OperationalError:
        return []
