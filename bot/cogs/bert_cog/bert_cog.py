from bot.cogs.base_cog import BaseCog, commands
from typing import List

from transformers import DistilBertForSequenceClassification, DistilBertTokenizerFast
from pathlib import Path
import numpy as np
import joblib
import torch

PREFIX_PATH = Path("bot/cogs/bert_cog/")
MODEL_PATH = PREFIX_PATH / "saved_model"
LABEL_ENCODER_PATH = PREFIX_PATH / "label_encoder.pkl"
TORCH_DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class BertCog(BaseCog):
    """
    A Discord cog that provides a help command.

    Attributes:
        msg (str): The message to reply with when the help command is used.
    """

    def __init__(self):
        """Initializes the BertCog."""

        # Cargar modelo y tokenizer
        self.model = DistilBertForSequenceClassification.from_pretrained(MODEL_PATH)
        self.tokenizer = DistilBertTokenizerFast.from_pretrained(MODEL_PATH)

        # Enviar el modelo a GPU si está disponible
        self.model.to(TORCH_DEVICE)
        self.model.eval()

        # Cargar el codificador de etiquetas
        self.label_encoder = joblib.load(LABEL_ENCODER_PATH)

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignore bot messages (including itself)
        if message.author.bot:
            return
        
        msg_str = message.content

        # Important: Let other commands run
        if msg_str.startswith("!"):
            await self.bot.process_commands(message)
            return

        text, label, prob = self._predict_one(msg_str)
        
        if label == "not_cyberbullying":
            return
        
        warn_msg = ""
        warn_msg += f"\nTexto: {text}\n"
        warn_msg += f"Predicción: {label}\n"
        warn_msg += f"Probabilidades: {dict(zip(self.label_encoder.classes_, prob.round(3)))}\n"
        await message.reply(warn_msg)

    def _predict_multiple(self, texts: List[str]):
        # Tokenización
        encodings = self.tokenizer(texts, truncation=True, padding=True, max_length=128, return_tensors="pt")
        input_ids = encodings["input_ids"].to(TORCH_DEVICE)
        attention_mask = encodings["attention_mask"].to(TORCH_DEVICE)

        # Inference
        with torch.no_grad():
            outputs = self.model(input_ids=input_ids, attention_mask=attention_mask)
            probs = torch.nn.functional.softmax(outputs.logits, dim=-1).cpu().numpy()

        # Predicción
        predictions = np.argmax(probs, axis=1)
        labels = self.label_encoder.inverse_transform(predictions)
        return list(zip(texts, labels, probs))

    def _predict_one(self, text: str):
        # Tokenización
        encodings = self.tokenizer([text], truncation=True, padding=True, max_length=128, return_tensors="pt")
        input_ids = encodings["input_ids"].to(TORCH_DEVICE)
        attention_mask = encodings["attention_mask"].to(TORCH_DEVICE)

        # Inference
        with torch.no_grad():
            outputs = self.model(input_ids=input_ids, attention_mask=attention_mask)
            probs = torch.nn.functional.softmax(outputs.logits, dim=-1).cpu().numpy()[0]

        # Predicción
        prediction = np.argmax(probs)
        label = self.label_encoder.inverse_transform([prediction])[0]
        return (text, label, probs)