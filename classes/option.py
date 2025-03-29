from classes.enum import Enum, dataclass
from classes.generic import Generic, T

# Rust-like Option<T>
class Option(Enum):
    @dataclass
    class Some(Enum.EnumOpt, Generic[T]):
        value: T
        def __repr__(self):
            return f"Option.Some({self.value})"

    @dataclass
    class Empty(Enum.EnumOpt):
        def __repr__(self):
            return "Option.Empty()"