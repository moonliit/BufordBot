from bot.cogs.base_cog import BaseCog, commands

from transformers import AutoModelForSequenceClassification, AutoTokenizer
from pathlib import Path
import torch

PREFIX_PATH = Path("bot/cogs/bert")
MODEL_PATH = PREFIX_PATH / "saved_model"
TORCH_DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class BertCog(BaseCog):
    """
    Discord cog to judge messages via the trained Bert model.
    """

    def __init__(self):
        """Initializes the BertCog."""

        # Cargar modelo y tokenizer
        self.model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
        
        # Enviar el modelo a GPU si está disponible
        self.model.to(TORCH_DEVICE)
        self.model.eval()

        # Cargar el codificador de etiquetas
        self.label_mapping = {
            0: 'not_cyberbullying',
            1: 'gender/sexual',
            2: 'ethnicity/race',
            3: 'religion',
            4: 'other_cyberbullying'
        }

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignore bot messages (including itself)
        if message.author.bot:
            return
        
        msg_str: str = message.content

        # Important: Let other commands run
        if msg_str.startswith("!"):
            await self.bot.process_commands(message)
            return

        confidences = self._predict(msg_str)

        # if chance of it NOT being cyberbullying is higher than 50%, skip
        SOFT_MARGIN = 0.5
        if confidences["not_cyberbullying"] >= SOFT_MARGIN:
            return
        
        confidences.pop("not_cyberbullying", None)
        top_label = max(confidences, key=confidences.get)
        top_confidence = confidences[top_label]

        warn_msg = ""
        warn_msg += f"\nTexto: {msg_str}\n"
        warn_msg += f"Predicción: {top_label}\n"
        warn_msg += f"Confianza: {top_confidence}\n"
        await message.reply(warn_msg)
    
    def _predict(self, text: str):
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