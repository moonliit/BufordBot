from bot.main_bot import MainBot
from discord import Intents
from utility.env_loader import EnvLoader
from utility.debug import Debug
from classes.option import Option

def main() -> None:
    match EnvLoader.get("DISCORD_TOKEN"):
        case Option.Some(value):
            DISCORD_TOKEN = value
            Debug.log("Succesfully acquired Discord token")
        case Option.Empty():
            Debug.log("Failed to acquire Discord token")
            return

    COMMAND_PREFIX = "sudo "
    BOT_DESCRIPTION = "this description of mine"

    bot = MainBot (
        command_prefix = COMMAND_PREFIX,
        description = BOT_DESCRIPTION,
        intents = Intents.all(),
        help_command = None
    )

    bot.init()
    bot.run(DISCORD_TOKEN)

if __name__ == "__main__":
    main()