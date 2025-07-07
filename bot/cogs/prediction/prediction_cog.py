from bot.cogs.base_cog import BaseCog, commands
from utility.text_cleaner import TextCleaner
from discord import Message

from bot.cogs.prediction.model.i_model import IModel
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

        # modo debug
        self.is_debug = False

        # modelos de prediccion almacenados
        self.stored_models = {
            "bert": BertModel(self.label_mapping),
            "tf_idf": TfIdfModel()
        }
        self.current_model: IModel = self.stored_models["bert"]

    @commands.group()
    async def prediction(self, ctx):
        pass

    @prediction.command()
    async def model(self, ctx, text):
        if text not in self.stored_models:
            await ctx.reply(f"'{text}' no se reconoce como un modelo!")
            return
        
        self.current_model = self.stored_models[text]
        await ctx.reply(f"Se cambio al modelo {text} correctamente!")

    @prediction.command()
    async def debug(self, ctx, text):
        EXPECTED = ["on", "off"]
        if text not in EXPECTED:
            await ctx.reply(f"'{text}' no se reconoce como un comando para debug!")
            return
        
        self.is_debug = bool(text == "on")
        await ctx.reply(f"Se cambio el modo debug a '{text}'!")

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
            if self.is_debug:
                await message.reply("El mensaje esta vacío!")
            return
        
        msg_str = cleaned_msg.unwrap()

        word_count = len(msg_str.strip().split(" "))
        MIN_WORD_AMOUNT = 3
        if word_count < MIN_WORD_AMOUNT:
            if self.is_debug:
                await message.reply(f"El mensaje: '{msg_str}'\nContiene solo {word_count} palabras. Mínimo para clasificación es {MIN_WORD_AMOUNT}")
            return

        await self._try_reply_with_prediction(message, msg_str)
    
    async def _try_reply_with_prediction(self, message: Message, text: str):
        # if chance of it NOT being cyberbullying is higher than 50%, skip
        SOFT_MARGIN = 0.5

        confidences = self.current_model.predict(text)
        if confidences["not_cyberbullying"] >= SOFT_MARGIN:
            if self.is_debug:
                info_msg  = f"Texto: {text}\n"
                info_msg += f"Detectado como 'not_cyberbullying'!\n"
                info_msg += f"Confianza: {confidences["not_cyberbullying"]}\n"
                await message.reply(info_msg)
            return
        
        confidences.pop("not_cyberbullying", None)
        top_label = max(confidences, key=confidences.get)
        top_confidence = confidences[top_label]

        warn_msg  = f"Texto: {text}\n"
        warn_msg += f"Predicción: {top_label}\n"
        warn_msg += f"Confianza: {top_confidence}\n"
        await message.reply(warn_msg)