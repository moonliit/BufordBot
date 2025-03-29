class Debug:
    _is_debug: bool | None = None

    @staticmethod
    def is_debug() -> bool:
        if Debug._is_debug is None: 
            from utility.env_loader import EnvLoader # Lazy import
            from classes.option import Option # Lazy import

            match EnvLoader.get("IS_DEBUG"):
                case Option.Some(value_str):
                    Debug._is_debug = value_str.lower() == "true"
                case Option.Empty():
                    Debug._is_debug = False
        return Debug._is_debug

    @staticmethod
    def log(text: str) -> None:
        if Debug.is_debug():
            print(f"DEBUG: {text}")

    @staticmethod
    def panic(msg: str) -> None:
        panic_msg: str = f"PANIC: {msg}"
        if Debug.is_debug():
            raise RuntimeError(panic_msg)
        else:
            print(panic_msg)