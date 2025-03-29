from classes.option import Option

from dotenv import load_dotenv
import os
load_dotenv()

class EnvLoader:
    @staticmethod
    def get(key: str) -> Option.EnumOpt:
        value = os.getenv(key)
        if value is not None:
            return Option.Some(value)
        else:
            return Option.Empty()