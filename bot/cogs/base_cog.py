from __future__ import annotations
from discord.ext import commands
from typing import Dict

class BaseCog(commands.Cog):
    """
    A base class for Discord bot cogs, implementing a singleton pattern.
    
    Ensures that each cog has only one instance shared across the bot.
    """

    _instances: Dict[BaseCog, BaseCog] = {}  # Stores singleton instances of cogs
    bot: commands.Bot  # Reference to the bot instance

    def __init__(self):
        """Constructor for BaseCog. Kept empty as instances are managed via `get_instance`."""
        pass

    def assign_bot(self, bot: commands.Bot) -> None:
        """
        Assigns the bot instance to the cog.

        Args:
            bot (commands.Bot): The Discord bot instance.
        """
        self.bot = bot

    @classmethod
    def get_instance(cls) -> BaseCog:
        """
        Retrieves the singleton instance of the cog, creating it if necessary.

        Returns:
            BaseCog: The singleton instance of the cog.
        """
        if cls not in cls._instances:
            cls._instances[cls] = cls()  # Create and store instance if it doesn't exist
        return cls._instances[cls]  # Return the stored instance