from bot.cogs.base_cog import BaseCog, commands

class HelpCog(BaseCog):
    """
    A Discord cog that provides a help command.

    Attributes:
        msg (str): The message to reply with when the help command is used.
    """

    def __init__(self):
        """Initializes the HelpCog."""
        self.msg = """**AYUDA - BUFORD BOT:**
- !prediction debug (on/off): Activa/Desactiva el modo debug. Para ver resultados clasificados como not_cyberbullying.
- !prediction model (bert/tf_idf): Cambia el modelo a 'bert' o a 'tf_idf' respectivamente.
"""

    @commands.command()
    async def help(self, ctx: commands.Context):
        """
        Replies with a help message when the command is used.

        Args:
            ctx (commands.Context): The command invocation context.
        """
        await ctx.reply(self.msg)
