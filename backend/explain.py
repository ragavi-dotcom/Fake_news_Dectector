from lime.lime_text import LimeTextExplainer
import numpy as np

from model import _load
from preprocess import clean_text

CLASS_NAMES = ["fake", "real"]

_explainer = LimeTextExplainer(class_names=CLASS_NAMES)


def _predict_proba_for_lime(raw_texts):

    _load() 
    from model import _vectorizer as vec, _model as clf
    cleaned = [clean_text(t) for t in raw_texts]
    X = vec.transform(cleaned)
    return clf.predict_proba(X)


def explain_prediction(text: str, num_features: int = 8) -> list[dict]:
    
    exp = _explainer.explain_instance(
        text,
        _predict_proba_for_lime,
        num_features=num_features,
        labels=(1,), 
    )
    return [{"word": word, "weight": round(float(weight), 4)}
            for word, weight in exp.as_list(label=1)]
