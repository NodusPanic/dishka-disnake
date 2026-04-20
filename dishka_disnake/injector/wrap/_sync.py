from collections.abc import Callable
from functools import wraps
from inspect import signature, _empty
from typing import (
    TypeVar,
    ParamSpec,
)

from dishka import Container

from dishka_disnake.base.sign import rebuild_annotations, rebuild_signature
from dishka_disnake.injector.util import extract_fromdishka
from dishka_disnake.state_management import State

P = ParamSpec("P")
R = TypeVar("R")


def wrap_injector(
    func: Callable[P, R],
) -> Callable[P, R]:
    original_annotations = getattr(func, "__dishka_annotations__", func.__annotations__)

    sig = signature(func)  # чистая (без DI) — для __signature__ wrapper'а

    full_params = {}
    for name, param in sig.parameters.items():
        if name in original_annotations:
            full_params[name] = param.replace(annotation=original_annotations[name])
        else:
            full_params[name] = param

    original_sig = getattr(func, "__signature__", None)
    if original_sig is not None:
        del func.__signature__  # type: ignore[assignment]
    func.__annotations__ = original_annotations
    full_sig = signature(func)
    func.__annotations__ = rebuild_annotations(func)
    if original_sig is not None:
        func.__signature__ = original_sig  # type: ignore[assignment]

    @wraps(func)
    def wrapper(*args, **kwargs):
        container: Container | None = State.sync_container

        if container is None:
            raise RuntimeError("Container is not initialized, setup dishka first")
        if not isinstance(container, Container):
            raise TypeError("Container is not a dishka sync container")

        with container() as c:
            params = full_sig.parameters.items()
            for name, param in params:
                annotation = param.annotation
                if name in kwargs or annotation is _empty:
                    continue

                dep_type = extract_fromdishka(annotation)
                if dep_type is not None:
                    kwargs[name] = c.get(dep_type)

            return func(*args, **kwargs)

    wrapper.__signature__ = rebuild_signature(func)  # type: ignore[assignment]
    wrapper.__annotations__ = rebuild_annotations(func)
    wrapper.__doc__ = func.__doc__
    try:
        del wrapper.__wrapped__
    except AttributeError:
        pass

    return wrapper
