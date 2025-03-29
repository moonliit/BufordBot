from classes.enum import Enum, dataclass
from classes.generic import Generic, T, E

# Rust-like Result<T, E>
class Result(Enum):
    @dataclass
    class Ok(Enum.EnumOpt, Generic[T]):
        value: T
        def __repr__(self):
            return f"Result.Ok({self.value})"

    @dataclass
    class Err(Enum.EnumOpt, Generic[E]):
        error: E
        def __repr__(self):
            return f"Result.Err({self.error})"