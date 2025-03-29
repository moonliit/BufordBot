from abc import ABC
from dataclasses import dataclass

class Enum(ABC):  
    """Abstract base class representing a Rust-like enum."""

    class EnumOpt(ABC):  # Abstract ase class for enum variants
        pass

def enum_base(cls):
    return cls

def enum_variant(cls):
    dataclass(cls)
    return cls