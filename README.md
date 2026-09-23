# Fake News Detector

A full-stack web app that reads a news article and predicts whether it's **real or fake**, with a confidence score and word-level explanations (via LIME) — so the result isn't a black box.

## Why This Project

Misinformation spreads faster than people can fact-check it. This project applies NLP and machine learning to that problem, built as a complete system — not just a model in a notebook — with a trained classifier, an API, a frontend, a database, and an explainability layer.

## Tech Stack

- **Backend:** Python, FastAPI, scikit-learn (TF-IDF + Logistic Regression), LIME, NLTK
- **Frontend:** React, Vite
- **Database:** SQLite

## How to Run

```bash
git clone https://github.com/ragavi-dotcom/Fake_news_Dectector.git
cd Fake_news_Dectector

# Backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python train.py
uvicorn main:app --reload

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

Then open `http://localhost:5173`, paste in an article, and click "Check article."

## Limitations

- Trained on a 2016–2017 news dataset, so it's most reliable on similar political/news content — not guaranteed to generalize to current events
- Uses word-pattern matching (TF-IDF), not deep contextual understanding

## Future Work

- Retrain on more recent data
- Add a view for past predictions (API already supports it)
- Explore a transformer-based model for better context understanding

## Project Structure

```
Fake_news_Dectector/
├── backend/    # FastAPI app + ML model
├── frontend/   # React UI
├── database/   # SQLite schema
└── docs/
```
