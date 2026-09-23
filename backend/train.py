from pathlib import Path
import json
import pandas as pd
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

from preprocess import clean_text

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
OUT_DIR  = Path(__file__).resolve().parent.parent / "notebook"
OUT_DIR.mkdir(exist_ok=True)


def load_kaggle():
    fake = pd.read_csv(DATA_DIR / "Fake.csv")
    real = pd.read_csv(DATA_DIR / "True.csv")
    fake["label"] = 0
    real["label"] = 1
    df = pd.concat([fake, real], ignore_index=True)
    df["content"] = (df["title"].fillna("") + " " + df["text"].fillna(""))
    return df[["content", "label"]]


def main():
    print("Loading data...")
    df = load_kaggle()
    print(f"  {len(df)} rows, class balance:\n{df['label'].value_counts()}")

    print("Cleaning text...")
    df["clean"] = df["content"].apply(clean_text)

    X_train, X_test, y_train, y_test = train_test_split(
        df["clean"], df["label"], test_size=0.2,
        stratify=df["label"], random_state=42,
    )

    print("Vectorizing (TF-IDF)...")
    vec = TfidfVectorizer(max_features=20000, ngram_range=(1, 2))
    Xtr = vec.fit_transform(X_train)
    Xte = vec.transform(X_test)

    print("Training Logistic Regression...")
    clf = LogisticRegression(max_iter=1000, n_jobs=-1)
    clf.fit(Xtr, y_train)

    print("\n=== Evaluation ===")
    preds = clf.predict(Xte)
    report_text = classification_report(y_test, preds, target_names=["fake", "real"])
    report_dict = classification_report(y_test, preds, target_names=["fake", "real"], output_dict=True)
    cm = confusion_matrix(y_test, preds)
    print(report_text)
    print("Confusion matrix:\n", cm)

    joblib.dump(vec, OUT_DIR / "tfidf_vectorizer.joblib")
    joblib.dump(clf, OUT_DIR / "model_logreg.joblib")

    metrics = {
        "accuracy": report_dict["accuracy"],
        "precision_fake": report_dict["fake"]["precision"],
        "recall_fake": report_dict["fake"]["recall"],
        "f1_fake": report_dict["fake"]["f1-score"],
        "precision_real": report_dict["real"]["precision"],
        "recall_real": report_dict["real"]["recall"],
        "f1_real": report_dict["real"]["f1-score"],
        "confusion_matrix": cm.tolist(),
        "train_size": len(X_train),
        "test_size": len(X_test),
    }
    with open(OUT_DIR / "metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    print(f"\nSaved artifacts + metrics.json to {OUT_DIR}")


if __name__ == "__main__":
    main()
