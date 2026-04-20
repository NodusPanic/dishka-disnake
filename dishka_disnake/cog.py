from typing import Any

from disnake.ext.commands import (
    Cog,
    Command,
    InvokableSlashCommand,
    InvokableMessageCommand,
    InvokableUserCommand,
    SubCommand,
)

from dishka_disnake import patch
from dishka_disnake.injector.wrap._async import wrap_injector

_INVOKABLE_TYPES = (
    Command,
    SubCommand,
    InvokableSlashCommand,
    InvokableMessageCommand,
    InvokableUserCommand,
)


def _is_event(name: str, member) -> bool:
    return callable(member) and name.startswith("on_")


def _is_listener(member) -> bool:
    return callable(member) and hasattr(member, "__cog_listener__")


class DishkaCog(Cog):
    patch.check_disnake_patched()

    def __init_subclass__(cls, **kwargs: Any):
        super().__init_subclass__(**kwargs)
        for name, member in vars(cls).items():
            if isinstance(member, _INVOKABLE_TYPES):
                member._callback = wrap_injector(member._callback)
            elif _is_listener(member) or _is_event(name, member):
                setattr(cls, name, wrap_injector(member))
