from utility.env_loader import EnvLoader
from classes.option import Option
    
match EnvLoader.get("IS_DEBUG"):
    case Option.Some(value_str):
        IS_DEBUG = value_str.lower() == "true"
    case Option.Empty():
        IS_DEBUG = False

class Debug:
    @staticmethod
    def log(text: str) -> None:
        if IS_DEBUG:
            print(f"Debug: {text}")