from bot.cogs.base_cog import BaseCog, commands
from utility.text_cleaner import TextCleaner
from discord import Message

from bot.cogs.prediction.model.bert.model import BertModel
from bot.cogs.prediction.model.tf_idf.model import TfIdfModel

class PredictionCog(BaseCog):
    """
    Discord cog to predict cyberbulyying messages via the selected model.
    """

    def __init__(self):
        """Initializes the PredictionCog."""

        # Cargar el codificador de etiquetas
        self.label_mapping = {
            0: 'not_cyberbullying',
            1: 'gender',
            2: 'ethnicity', 
            3: 'religion',
            4: 'other_cyberbullying',
            5: 'age'
        }

        self.stored_models = {
            "bert": BertModel(self.label_mapping),
            "tf_idf": TfIdfModel()
        }
        self.current_model = self.stored_models["bert"]

    @commands.command()
    async def model(self, ctx, text):
        if text not in self.stored_models:
            await ctx.reply(f"'{text}' no se reconoce como un modelo!")
            return
        
        self.current_model = self.stored_models[text]
        await ctx.reply(f"Se cambio al modelo {text} correctamente!")

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        # Ignore bot messages (including itself)
        if message.author.bot:
            return
        
        msg_str: str = message.content

        # Important: Let other commands run
        if msg_str.startswith("!"):
            return
        
        cleaned_msg = TextCleaner.clean(msg_str)

        # if message after cleaning is empty
        if cleaned_msg.is_none():
            return
        
        msg_str = cleaned_msg.unwrap()
        await self._try_reply_with_prediction(message, msg_str)
    
    async def _try_reply_with_prediction(self, message: Message, text: str):
        # if chance of it NOT being cyberbullying is higher than 50%, skip
        SOFT_MARGIN = 0.5

        confidences = self.current_model.predict(text)
        if confidences["not_cyberbullying"] >= SOFT_MARGIN:
            return
        
        confidences.pop("not_cyberbullying", None)
        top_label = max(confidences, key=confidences.get)
        top_confidence = confidences[top_label]

        warn_msg = ""
        warn_msg += f"\nTexto: {text}\n"
        warn_msg += f"Predicción: {top_label}\n"
        warn_msg += f"Confianza: {top_confidence}\n"
        await message.reply(warn_msg)