from typing import Generic, TypeVar
from types import NoneType
from classes.error import Error

# Generics
T = TypeVar("T")
U = TypeVar("U")

# Error generics
E = TypeVar("E", bound=Error)

# Empty generics
_ = TypeVar("_", bound=NoneType)