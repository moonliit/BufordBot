from bot.main_bot import MainBot
from discord import Intents
from utility.env_loader import EnvLoader

def main() -> None:
    DISCORD_TOKEN = EnvLoader.get("DISCORD_TOKEN").unwrap_or_err("Failed to acquire Discord token")
    COMMAND_PREFIX = "!"
    BOT_DESCRIPTION = "this description of mine" #placeholder
    BOT_INTENTS = Intents.all()

    bot = MainBot (
        command_prefix = COMMAND_PREFIX,
        description = BOT_DESCRIPTION,
        intents = BOT_INTENTS,
        help_command = None # Left empty for custom help command
    )
    bot.init()
    bot.run(DISCORD_TOKEN)

if __name__ == "__main__":
    main()