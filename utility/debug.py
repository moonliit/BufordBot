class Debug:
    """Utility class for handling debug logging and other functions."""

    _is_debug: bool | None = None

    @staticmethod
    def is_debug() -> bool:
        """Gets if debug mode is enabled for the program. Caches the result for future use."""
        if Debug._is_debug is not None:
            return Debug._is_debug # Return if value already cached
        
        # Lazy imports
        from utility.env_loader import EnvLoader

        Debug._is_debug = \
            EnvLoader.get("IS_DEBUG").\
            map(bool)(lambda s: s.lower() == "true").\
            unwrap_or_else(False)
        
        return Debug._is_debug

    @staticmethod
    def log(text: str) -> None:
        """
        Logs a debug message if debugging is enabled.

        Args:
            text (str): The message to log.
        """
        if Debug.is_debug():
            print(f"DEBUG: {text}")

    @staticmethod
    def panic(msg: str) -> None:
        """
        Raises a runtime error if debugging is enabled; otherwise, prints the panic message.

        Args:
            msg (str): The panic message to display or raise.
        """
        panic_msg: str = f"PANIC: {msg}"
        if Debug.is_debug():
            raise RuntimeError(panic_msg)
        else:
            print(panic_msg)