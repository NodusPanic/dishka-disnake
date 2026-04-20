from collections.abc import Callable
from inspect import iscoroutinefunction
from typing import TypeVar, ParamSpec, Coroutine, Any, overload

from dishka import FromDishka

from dishka_disnake import patch
from dishka_disnake.injector.wrap import _async, _sync

__all__ = ["inject", "inject_loose", "FromDishka"]

P = ParamSpec("P")
R = TypeVar("R")


@overload
def inject(
    func: Callable[P, Coroutine[Any, Any, R]],
) -> Callable[P, Coroutine[Any, Any, R]]: ...
@overload
def inject(func: Callable[P, R]) -> Callable[P, R]: ...
def inject(
    func: Callable[P, Coroutine[Any, Any, R]] | Callable[P, R],
) -> Callable:
    """
    Decorator that injects dependencies marked with FromDishka into the function.

    Resolves annotated parameters from the dishka container automatically,
    so they don't need to be passed manually by the caller.
    Supports both sync and async functions.
    """
    patch.check_disnake_patched()

    if not iscoroutinefunction(func):
        return _sync.wrap_injector(func)
    return _async.wrap_injector(func)


@overload
def inject_loose(
    func: Callable[..., Coroutine[Any, Any, R]],
) -> Callable[..., Coroutine[Any, Any, R]]: ...
@overload
def inject_loose(func: Callable[..., R]) -> Callable[..., R]: ...
def inject_loose(
    func: Callable[..., Coroutine[Any, Any, R]] | Callable[..., R],
) -> Callable:
    """
    Same as `inject`, but with loose typing (Callable[...] instead of Callable[P]).

    Use when the exact parameter signature doesn't matter to the caller,
    for example when decorating methods dynamically or in metaclasses.
    """
    patch.check_disnake_patched()

    return inject(func)
