from classes.option import Option
from dotenv import load_dotenv
import os

# Load environment variables from a .env file (if present).
load_dotenv()

class EnvLoader:
    """Utility class for retrieving environment variables safely."""

    @staticmethod
    def get(key: str) -> Option[str].OptionOpt:
        """
        Retrieves the value of an environment variable as an `Option`.

        Args:
            key (str): The name of the environment variable.

        Returns:
            Option[str].OptionOpt: `Option.Some(value)` if the variable exists, otherwise `Option.Empty()`.
        """
        value = os.getenv(key)
        if value is not None:
            return Option.Some(value)  # Return Some(value) if the variable is found
        else:
            return Option.Empty()  # Return Empty if the variable is not found
