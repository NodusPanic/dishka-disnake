from collections.abc import Callable
from typing import Any, Coroutine, Generic, TypeVar

from dishka_disnake.injector.wrap._async import wrap_injector


T = TypeVar("T")


class WrappedDishkaComponent(Generic[T]):
    async def callback(self, interaction: T, *args: Any, **kwargs: Any) -> None: ...

    def __init_subclass__(cls, **kwargs: Any):
        super().__init_subclass__(**kwargs)

        cb: Callable[..., Coroutine[Any, Any, None]] | None = cls.__dict__.get("callback")
        if cb is not None:
            cls.callback = wrap_injector(cb)  # type: ignore[assignment]
