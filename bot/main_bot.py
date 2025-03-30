from discord.ext import commands
from typing import List, Type
import asyncio

# Import cogs here
from bot.cogs.base_cog import BaseCog
from bot.cogs.ping.ping_cog import PingCog
from bot.cogs.presence.presence_cog import PresenceCog
from bot.cogs.help.help_cog import HelpCog

# List of cogs to be loaded into the bot
cog_array: List[Type[BaseCog]] = [
    PingCog,
    PresenceCog,
    HelpCog
]

class MainBot(commands.Bot):
    """Custom Discord bot class that loads cogs using a singleton pattern."""

    def __init__(self, *args, **kwargs):
        """Initializes the bot, passing all arguments to `commands.Bot`."""
        super().__init__(*args, **kwargs)

    def init(self) -> None:
        """Synchronously initializes the bot by running the async setup."""
        asyncio.run(self._async_setup())

    async def _async_setup(self) -> None:
        """
        Asynchronously sets up the bot by loading all cogs.

        Each cog is retrieved as a singleton instance, assigned the bot reference,
        and added to the bot.
        """
        for cog_type in cog_array:
            cog = cog_type.get_instance()  # Retrieve singleton instance of the cog
            cog.assign_bot(self)  # Assign the bot instance to the cog
            await self.add_cog(cog)  # Register the cog with the bot