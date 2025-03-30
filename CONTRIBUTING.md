(escrito por gpt XD)

# Contributing to the Bot

Thank you for considering contributing to this project! This guide will walk you through the process of adding new features via cogs.

---

## 🛠 Prerequisites

Before contributing, ensure you have the following:

- Python 3.10 installed (may break in higher versions)
- The bot's repository cloned to your local machine
- Requirements installed (`pip install -r requirements.txt`)

---

## 🏗 How to Add a New Cog

Cogs are modular components that add functionality to the bot. To contribute a new cog, follow these steps:

### 1️⃣ Create a New Cog  

All cogs should extend `BaseCog` from `base_cog.py`. Here’s an example of a simple `PingCog`:

```python
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
```

### 2️⃣ Add Your Cog to main_bot.py

Once you've created your cog, you need to register it in main_bot.py. Open main_bot.py and locate the cog_array. Add your cog to the list:

```python
# Import your new cog
from bot.cogs.ping.ping_cog import PingCog

# Add it to the list of cogs
cog_array: List[Type[BaseCog]] = [
    PingCog,  # New cog added
    PresenceCog,
    HelpCog
]
```

### 3️⃣ Test Your Cog

Before submitting your contribution, make sure it works correctly:

1. Run the bot using `python3 main.py`. Alternatively run with the `Dockerfile`

2. Test your command in Discord (e.g., type `sudo ping`)

3. Fix any errors before proceeding

### 4️⃣ Submit a Pull Request

Once you've verified that your cog works as expected:

1. Commit your changes

2. Push to your forked repository

3. Open a pull request (PR) describing your changes

---

## ❗ Code Guidelines

- Follow [PEP 8](https://peps.python.org/pep-0008/) style conventions  

- Write clear docstrings for all functions and classes

- Ensure new cogs inherit from `BaseCog`

---

## 🤝 Need Help?

If you have any questions, feel free to ask in the project discussions or open an issue. Happy coding! 🚀