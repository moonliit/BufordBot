from bot.cogs.base_cog import BaseCog, commands

class PingCog(BaseCog):
    """
    A Discord cog that provides a simple ping command.

    Attributes:
        msg (str): The message to reply with when the ping command is used.
    """

    def __init__(self):
        """Initializes the PingCog."""
        self.msg: str = "pong!"

    @commands.command()
    async def ping(self, ctx: commands.Context):
        """
        Replies with a pong message when the command is used.

        Args:
            ctx (commands.Context): The command invocation context.
        """
        await ctx.reply(self.msg)