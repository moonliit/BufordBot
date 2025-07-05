from bot.cogs.base_cog import BaseCog, commands

from transformers import DistilBertForSequenceClassification, DistilBertTokenizerFast
from pathlib import Path
import torch

PREFIX_PATH = Path("bot/cogs/bert_cog/")
MODEL_PATH = PREFIX_PATH / "saved_model"
LABEL_ENCODER_PATH = PREFIX_PATH / "label_encoder.pkl"
TORCH_DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class BertCog(BaseCog):
    """
    Discord cog to judge messages via the trained Bert model.
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

        label, confidence = self._predict(msg_str)
        
        if label == "not_cyberbullying":
            return
        
        warn_msg = ""
        warn_msg += f"\nTexto: {msg_str}\n"
        warn_msg += f"Predicción: {label}\n"
        warn_msg += f"Confianza: {confidence}\n"
        await message.reply(warn_msg)
    
    def _predict(self, text: str):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=200)

        with torch.no_grad():
            outputs = self.model(**inputs)
            predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
            predicted_class = torch.argmax(predictions, dim=-1).item()
            confidence = predictions[0][predicted_class].item()

        return self.label_mapping[predicted_class], confidence