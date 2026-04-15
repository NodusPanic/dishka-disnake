from collections.abc import Callable
from functools import wraps
from inspect import signature, _empty
from typing import (
    TypeVar,
    ParamSpec,
    Coroutine,
    Any,
)

from dishka import AsyncContainer

from dishka_disnake.base.sign import rebuild_signature
from dishka_disnake.injector.util import extract_fromdishka
from dishka_disnake.state_management import State

P = ParamSpec("P")
R = TypeVar("R")


def wrap_injector(
    func: Callable[P, Coroutine[Any, Any, R]],
) -> Callable[P, Coroutine[Any, Any, R]]:
    sig = signature(func)

    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        container: AsyncContainer | None = State.container

        if container is None:
            raise RuntimeError("Container is not initialized, setup dishka first")

        async with container() as c:
            params = sig.parameters.items()
            for name, param in params:
                annotation = param.annotation
                if name in kwargs or annotation is _empty:
                    continue

                dep_type = extract_fromdishka(annotation)
                if dep_type is not None:
                    kwargs[name] = await c.get(dep_type)

            return await func(*args, **kwargs)

    async_wrapper.__signature__ = rebuild_signature(func)  # type: ignore

    return async_wrapper
