from abc import ABC
from dataclasses import dataclass

class Enum(ABC):  
    """Abstract base class representing a Rust-like enum."""

    class EnumOpt(ABC):
        """Abstract base class for enum variants"""
        pass

def enum_base(cls):
    """Decorator to add to the enum option type"""
    return cls

def enum_variant(cls):
    """Decorator to add to the enum variants. Ensures contents are dataclasses and else"""
    dataclass(cls)
    return cls