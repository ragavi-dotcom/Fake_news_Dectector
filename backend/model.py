from pathlib import Path
import joblib
from preprocess import clean_text

ARTIFACTS_DIR = Path(__file__).resolve().parent.parent / "notebook"
VECTORIZER_PATH = ARTIFACTS_DIR / "tfidf_vectorizer.joblib"
MODEL_PATH      = ARTIFACTS_DIR / "model_logreg.joblib"

_vectorizer = None
_model = None


def _load():
    global _vectorizer, _model
    if _vectorizer is None or _model is None:
        _vectorizer = joblib.load(VECTORIZER_PATH)
        _model = joblib.load(MODEL_PATH)


def predict(text: str) -> dict:

    _load()
    cleaned = clean_text(text)
    X = _vectorizer.transform([cleaned])
    proba = _model.predict_proba(X)[0]
    idx = int(proba.argmax())
    
    label = "real" if idx == 1 else "fake"
    return {"label": label, "confidence": float(proba[idx])}
