from __future__ import annotations
from discord.ext import commands
from typing import Dict

class BaseCog(commands.Cog):
    _instances: Dict[BaseCog, BaseCog] = {}
    bot: commands.Bot

    def __init__(self):
        pass

    def assign_bot(self, bot: commands.Bot):
        self.bot = bot

    @classmethod
    def get_instance(cls):
        """Returns the singleton instance of the cog, creating it if necessary."""
        if cls not in cls._instances:
            cls._instances[cls] = cls()
        return cls._instances[cls]