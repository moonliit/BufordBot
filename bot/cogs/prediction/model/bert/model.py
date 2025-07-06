from bot.cogs.prediction.model.i_model import IModel
from typing import Dict

from transformers import AutoModelForSequenceClassification, AutoTokenizer
from pathlib import Path
import torch

BERT_PREFIX_PATH = Path("bot/cogs/prediction/model/bert")
MODEL_PATH = BERT_PREFIX_PATH / "features"
TORCH_DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class BertModel(IModel):
    def __init__(self, label_mapping: Dict[int, str]):
        self.label_mapping = label_mapping

        # Cargar modelo y tokenizer
        self.model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
        
        # Enviar el modelo a GPU si está disponible
        self.model.to(TORCH_DEVICE)
        self.model.eval()

    def predict(self, text: str) -> Dict[str, float]:
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=200)

        with torch.no_grad():
            outputs = self.model(**inputs)
            predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)[0]  # Get first (and only) batch

        # Map each class index to label and confidence
        confidences = {
            self.label_mapping[i]: predictions[i].item()
            for i in range(len(predictions))
        }

        return confidences