from abc import ABC

# Define a base Error class to enforce error types
class Error(ABC):
    """Base class for all errors."""
    def __repr__(self):
        return f"{self.__class__.__name__}()"