from __future__ import annotations
from classes.enum import Enum, enum_base, enum_variant
from classes.generic import Generic, T, E, _
from utility.debug import Debug
from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from classes.option import Option

# Rust-like Result<T, E>
class Result(Generic[T, E], Enum):
    @enum_base
    class ResultOpt(Enum.EnumOpt, Generic[T, E]):
        """Base class for Result variants, providing common methods."""

        def is_ok(self) -> bool:
            """Returns True if the result is Ok, otherwise False."""
            return isinstance(self, Result.Ok)

        def is_err(self) -> bool:
            """Returns True if the result is Err, otherwise False."""
            return isinstance(self, Result.Err)

        def unwrap(self) -> T:
            """Returns the Ok value or panics if the result is Err."""
            if isinstance(self, Result.Ok):
                return self.value
            Debug.panic(f"Called unwrap on Result.Err({self.error})!")

        def unwrap_or(self, default: T) -> T:
            """Returns the Ok value if present, otherwise returns the provided default."""
            return self.value if isinstance(self, Result.Ok) else default

        def unwrap_or_else(self, fn: Callable[[E], T]) -> T:
            """Returns the Ok value if present, otherwise computes a default value using fn(error)."""
            return self.value if isinstance(self, Result.Ok) else fn(self.error)

        def expect(self, msg: str) -> T:
            """Returns the Ok value if present, otherwise panics with a custom message."""
            if isinstance(self, Result.Ok):
                return self.value
            Debug.panic(f"{msg}: {self.error}")

        def expect_err(self, msg: str) -> E:
            """Returns the Err value if present, otherwise panics with a custom message."""
            if isinstance(self, Result.Err):
                return self.error
            Debug.panic(f"{msg}: {self.value}")

        def ok(self) -> "Option[T]":
            """Converts Result<T, E> into Option<T>, dropping the error if present."""
            from classes.option import Option
            return Option.Some(self.value) if isinstance(self, Result.Ok) else Option.Empty()

        def err(self) -> "Option[E]":
            """Converts Result<T, E> into Option<E>, dropping the success value if present."""
            from classes.option import Option
            return Option.Some(self.error) if isinstance(self, Result.Err) else Option.Empty()

        def map(self, fn: Callable[[T], U]) -> Result[U, E]:
            """Applies a function to the Ok value (if present), keeping Err unchanged."""
            return Result.Ok(fn(self.value)) if isinstance(self, Result.Ok) else self

        def map_err(self, fn: Callable[[E], F]) -> Result[T, F]:
            """Applies a function to the Err value (if present), keeping Ok unchanged."""
            return Result.Err(fn(self.error)) if isinstance(self, Result.Err) else self

        def and_then(self, fn: Callable[[T], Result[U, E]]) -> Result[U, E]:
            """Chains a function that returns a Result if this is Ok; propagates Err."""
            return fn(self.value) if isinstance(self, Result.Ok) else self

        def or_else(self, fn: Callable[[E], Result[T, F]]) -> Result[T, F]:
            """Chains a function that returns a Result if this is Err; propagates Ok."""
            return fn(self.error) if isinstance(self, Result.Err) else self

    @enum_variant
    class Ok(ResultOpt[T, _], Generic[T, _]):
        """Represents a successful result containing a value."""
        value: T

        def __repr__(self):
            return f"Result.Ok({self.value})"

    @enum_variant
    class Err(ResultOpt[_, E], Generic[_, E]):
        """Represents an error result containing an error value."""
        error: E

        def __repr__(self):
            return f"Result.Err({self.error})"
