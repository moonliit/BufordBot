from __future__ import annotations
from classes.enum import Enum, enum_base, enum_variant
from classes.generic import Generic, T, U, E, F, _
from utility.debug import Debug
from typing import Callable, Type, TYPE_CHECKING

if TYPE_CHECKING:
    from classes.option import Option

class Result(Generic[T, E], Enum):
    """Rust-like Result Enum. Contains variants 'Ok' and 'Err'"""

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

        def map(self, return_type: Type[U]):
            """
            Transforms `Ok(T)` into `Ok(U)` using `fn: T -> U`, returning `Result[U, E]`. Keeps `Err` unchanged.

            ### Uses curried template args `[U]`
            """
            def inner(fn: Callable[[T], U]) -> Result[U, E]:
                return Result.Ok(return_type(fn(self.value))) if isinstance(self, Result.Ok) else self
            return inner

        def map_err(self, return_type: Type[F]):
            """
            Transforms `Err(E)` into `Err(F)` using `fn: E -> F`, returning `Result[T, F]`. Keeps `Ok` unchanged.

            ### Uses curried template args `[F]`
            """
            def inner(fn: Callable[[E], F]) -> Result[T, F]:
                return Result.Err(return_type(fn(self.error))) if isinstance(self, Result.Err) else self
            return inner

        def and_then(self, return_type: Type[U]):
            """
            Transforms `Ok(T)` into `Result[U, E]` using `fn: T -> Result[U, E]`, avoiding nested `Result[Result[U, E], E]`. 
            Keeps `Err` unchanged.

            ### Uses curried template args `[U]`
            """
            def inner(fn: Callable[[T], Result[U, E]]) -> Result[U, E]:
                return fn(self.value) if isinstance(self, Result.Ok) else self
            return inner

        def or_else(self, return_type: Type[F]):
            """
            Transforms `Err(E)` into `Result[T, F]` using `fn: E -> Result[T, F]`, avoiding nested `Result[T, Result[T, F]]`. 
            Keeps `Ok` unchanged.

            ### Uses curried template args `[F]`
            """
            def inner(fn: Callable[[E], Result[T, F]]) -> Result[T, F]:
                return fn(self.error) if isinstance(self, Result.Err) else self
            return inner

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
