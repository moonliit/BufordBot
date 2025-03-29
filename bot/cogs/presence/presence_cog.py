from bot.cogs.base_cog import BaseCog, commands
from discord import Game

class PresenceCog(BaseCog):
    """
    A Discord cog that updates the bot's presence (status message) when it becomes ready.

    Attributes:
        status_message (str): The message displayed as the bot's activity.
    """

    def __init__(self):
        """Initializes the PresenceCog."""
        self.status_message: str = "sudo help"

    @commands.Cog.listener()
    async def on_ready(self):
        """Event listener that updates the bot's presence when it is ready."""
        await self.bot.change_presence(activity=Game(name=self.status_message))
