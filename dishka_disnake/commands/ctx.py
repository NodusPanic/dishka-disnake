from __future__ import annotations

from collections.abc import Callable
from inspect import iscoroutinefunction
from typing import (
    TYPE_CHECKING,
    Any,
    Optional,
    TypeVar,
    overload,
)

import disnake
from disnake.ext.commands import Command
from disnake.ext.commands.cog import Cog
from disnake.ext.commands.context import Context

if TYPE_CHECKING:
    from typing import Concatenate, ParamSpec

    from disnake.ext.commands._types import Coro


MISSING: Any = disnake.utils.MISSING

T = TypeVar("T")
CogT = TypeVar("CogT", bound="Optional[Cog]")
CommandT = TypeVar("CommandT", bound="Command")
ContextT = TypeVar("ContextT", bound="Context")


if TYPE_CHECKING:
    P = ParamSpec("P")

    CommandCallback = (
        Callable[Concatenate[CogT, ContextT, P], Coro[T]]
        | Callable[Concatenate[ContextT, P], Coro[T]],
    )
else:
    P = TypeVar("P")
# from disnake.ext.commands.core import CommandDecorator, MISSING, CommandT, ContextT, CogT, P, T, CommandCallback

from dishka_disnake.injector.wrap._async import wrap_injector


@overload
def command(
    name: str,
    cls: type[CommandT],
    **attrs: Any,
) -> Callable[[CommandCallback[CogT, ContextT, P, T]], CommandT]: ...


@overload
def command(
    name: str = ...,
    *,
    cls: type[CommandT],
    **attrs: Any,
) -> Callable[[CommandCallback[CogT, ContextT, P, T]], CommandT]: ...


@overload
def command(
    name: str = ...,
    **attrs: Any,
) -> CommandDecorator: ...


def command(
    name: str = MISSING,
    cls: type[Command[Any, Any, Any]] = MISSING,
    **attrs: Any,
) -> Any:
    """A decorator that transforms a function into a :class:`.Command`
    or if called with :func:`.group`, :class:`.Group`.

    By default the ``help`` attribute is received automatically from the
    docstring of the function and is cleaned up with the use of
    ``inspect.cleandoc``. If the docstring is ``bytes``, then it is decoded
    into :class:`str` using utf-8 encoding.

    All checks added using the :func:`.check` & co. decorators are added into
    the function. There is no way to supply your own checks through this
    decorator.

    Parameters
    ----------
    name: :class:`str`
        The name to create the command with. By default this uses the
        function name unchanged.
    cls
        The class to construct with. By default this is :class:`.Command`.
        You usually do not change this.
    attrs
        Keyword arguments to pass into the construction of the class denoted
        by ``cls``.

    Raises
    ------
    TypeError
        If the function is not a coroutine or is already a command.
    """
    if cls is MISSING:
        cls = Command

    def decorator(func: CommandCallback[CogT, ContextT, P, T]) -> Command[Any, Any, Any]:
        func = wrap_injector(func)
        if not iscoroutinefunction(func):
            raise TypeError(f"<{func.__qualname__}> must be a coroutine function")  # type: ignore[attr-defined]
        if hasattr(func, "__command_flag__"):
            raise TypeError("Callback is already a command.")
        return cls(func, name=name, **attrs)

    return decorator
