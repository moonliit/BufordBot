from __future__ import annotations
from classes.enum import Enum, enum_base, enum_variant
from classes.generic import Generic, T, U, E
from utility.debug import Debug
from typing import Callable, Type, TYPE_CHECKING

if TYPE_CHECKING:
    from classes.result import Result

class Option(Generic[T], Enum):
    """Rust-like Option Enum. Contains variants 'Some' and 'Empty'"""

    @enum_base
    class OptionOpt(Enum.EnumOpt, Generic[T]):
        """Base class for Option variants, providing common methods."""
        
        def is_some(self) -> bool:
            """Returns `True` if the Option contains a value (`Some`), otherwise `False`."""
            return isinstance(self, Option.Some)

        def is_none(self) -> bool:
            """Returns `True` if the Option is empty (`Empty`), otherwise `False`."""
            return isinstance(self, Option.Empty)
        
        def unwrap(self) -> T:
            """Returns the value inside `Some`. Panics if called on `Empty`."""
            if isinstance(self, Option.Some):
                return self.value
            Debug.panic(f"Called unwrap on Option.Empty()!")

        def unwrap_or(self, default: T) -> T:
            """Returns the contained value if `Some`, otherwise returns the provided default value."""
            return self.value if isinstance(self, Option.Some) else default

        def unwrap_or_else(self, fn: Callable[[], T]) -> T:
            """Returns the contained value if `Some`, otherwise computes a default value using `fn`."""
            return self.value if isinstance(self, Option.Some) else fn()
        
        def unwrap_or_err(self, msg: str) -> T:
            """Returns the contained value if `Some`, otherwise panics thread with given `msg`"""
            from utility.debug import Debug  # Lazy import to avoid circular dependency
            if isinstance(self, Option.Some):
                return self.value
            Debug.panic(msg)

        def map(self, return_type: Type[U]):
            """
            Transforms `Some(T)` into `Some(U)` using `fn: T -> U`, returning `Option[U]`. Returns `Empty` otherwise.
            
            ### Uses curried template args `[U]` 
            """
            def inner(fn: Callable[[T], U]) -> Option[U].OptionOpt:
                return Option.Some(return_type(fn(self.value))) if isinstance(self, Option.Some) else Option.Empty()
            return inner
        
        def and_then(self, return_type: Type[U]):
            """
            Transforms `Some(T)` into `Option[U]` using `fn: T -> Option[U]`, avoiding nested `Option[Option[U]]`. Returns `Empty` otherwise.
            
            ### Uses curried template args `[U]` 
            """
            def inner(fn: Callable[[T], Option[U]]) -> Option[U].OptionOpt:
                return fn(self.value) if isinstance(self, Option.Some) else Option.Empty()
            return inner

        def filter(self, predicate: Callable[[T], bool]) -> Option[T].OptionOpt:
            """Returns `Some(value)` if the predicate returns `True`, otherwise `Empty`."""
            return self if isinstance(self, Option.Some) and predicate(self.value) else Option.Empty()

        def ok_or(self, err: E) -> "Result[T, E].ResultOpt":
            """Converts `Option<T>` into `Result<T, E>`, using `Err(err)` if `Empty`."""
            from classes.result import Result  # Lazy import to avoid circular dependency
            return Result.Ok(self.value) if isinstance(self, Option.Some) else Result.Err(err)

    @enum_variant
    class Some(OptionOpt[T], Generic[T]):
        """Represents an Option containing a value."""
        value: T

        def __repr__(self):
            return f"Option.Some({self.value})"

    @enum_variant
    class Empty(OptionOpt[None]):
        """Represents an empty Option."""
        def __repr__(self):
            return "Option.Empty()"
