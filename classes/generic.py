from typing import Generic, TypeVar
from classes.error import Error

# Generics
T = TypeVar("T")
K = TypeVar("K")

# Error generics
E = TypeVar("E", bound=Error)