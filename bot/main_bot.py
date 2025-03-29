from discord.ext import commands
from typing import List, Type
import asyncio

# Import cogs here
from bot.cogs.base_cog import BaseCog
from bot.cogs.ping.ping_cog import PingCog
from bot.cogs.presence.presence_cog import PresenceCog
from bot.cogs.help.help_cog import HelpCog

# Add cogs here
cog_array: List[Type[BaseCog]] = [
    PingCog,
    PresenceCog,
    HelpCog
]

class MainBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def init(self) -> None:
        asyncio.run(self._async_setup())

    async def _async_setup(self) -> None:
        for cog_type in cog_array:
            cog = cog_type.get_instance()
            cog.assign_bot(self)
            await self.add_cog(cog)