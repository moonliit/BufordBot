from bot.cogs.prediction.model.i_model import IModel
from typing import Dict
from joblib import load
from pathlib import Path

TF_IDF_PREFIX_PATH = Path("bot/cogs/prediction/model/tf_idf/features")
VECTORIZER_PATH = TF_IDF_PREFIX_PATH / "tfidf_vectorizer.joblib"
CLASSIFIER_PATH = TF_IDF_PREFIX_PATH / "logreg_classifier.joblib"

class TfIdfModel(IModel):
    def __init__(self):
        # Load vectorizer and classifier
        self.vectorizer = load(VECTORIZER_PATH)
        self.classifier = load(CLASSIFIER_PATH)

    def predict(self, text: str) -> Dict[str, float]:
        X = self.vectorizer.transform([text])  # Convert input to vector
        pred = self.classifier.predict(X)[0]          # Predict label
        prob = self.classifier.predict_proba(X)[0]    # Get probabilities
        label_prob = max(prob)            # Top confidence
        return dict(zip(self.classifier.classes_, prob))