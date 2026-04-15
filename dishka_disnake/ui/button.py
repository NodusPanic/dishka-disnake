from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Generic,
    Optional,
    TypeVar,
    Union,
    overload,
)

from disnake import MessageInteraction, ui

from disnake.enums import ButtonStyle
from disnake.partial_emoji import PartialEmoji
from disnake.ui.item import DecoratedItem

from dishka_disnake.ui.base import WrappedDishkaComponent

__all__ = (
    "Button",
    "button",
)

if TYPE_CHECKING:
    from typing_extensions import ParamSpec

    from disnake.emoji import Emoji
    from disnake.ui.item import ItemCallbackType
    from disnake.ui.view import View
    from disnake.client import Client

else:
    ParamSpec = TypeVar

from dishka_disnake.injector.wrap._async import wrap_injector

B = TypeVar("B", bound="Button")
B_co = TypeVar("B_co", bound="Button", covariant=True)
V_co = TypeVar("V_co", bound="Optional[View]", covariant=True)
ClientT = TypeVar("ClientT", bound="Client")
P = ParamSpec("P")


class Button(WrappedDishkaComponent[MessageInteraction], ui.Button[B_co], Generic[B_co]):
    """Represents a UI button with DI support.

    .. versionadded:: 2.0

    Parameters
    ----------
    style: :class:`disnake.ButtonStyle`
        The style of the button.
    custom_id: Optional[:class:`str`]
        The ID of the button that gets received during an interaction.
        If this button is for a URL or an SKU, it does not have a custom ID.
    url: Optional[:class:`str`]
        The URL this button sends you to.
    disabled: :class:`bool`
        Whether the button is disabled.
    label: Optional[:class:`str`]
        The label of the button, if any.
    emoji: Optional[Union[:class:`.PartialEmoji`, :class:`.Emoji`, :class:`str`]]
        The emoji of the button, if available.
    sku_id: Optional[:class:`int`]
        The ID of a purchasable SKU, for premium buttons.
        Premium buttons additionally cannot have a ``label``, ``url``, or ``emoji``.

        .. versionadded:: 2.11
    id: :class:`int`
        The numeric identifier for the component. Must be unique within the message.
        If set to ``0`` (the default) when sending a component, the API will assign
        sequential identifiers to the components in the message.

        .. versionadded:: 2.11
    row: Optional[:class:`int`]
        The relative row this button belongs to. A Discord component can only have 5
        rows. By default, items are arranged automatically into those 5 rows. If you'd
        like to control the relative positioning of the row then passing an index is advised.
        For example, row=1 will show up before row=2. Defaults to ``None``, which is automatic
        ordering. The row number must be between 0 and 4 (i.e. zero indexed).
    """


@overload
def button(
    *,
    label: Optional[str] = None,
    custom_id: Optional[str] = None,
    disabled: bool = False,
    style: ButtonStyle = ButtonStyle.secondary,
    emoji: Optional[Union[str, Emoji, PartialEmoji]] = None,
    id: int = 0,
    row: Optional[int] = None,
) -> Callable[..., DecoratedItem[Button[V_co]]]: ...


@overload
def button(
    cls: Callable[P, B_co], *_: P.args, **kwargs: P.kwargs
) -> Callable[..., DecoratedItem[B_co]]: ...


def button(
    cls: Callable[..., B_co] = Button[Any], **kwargs: Any
) -> Callable[..., DecoratedItem[B_co]]:
    """A decorator that attaches a button to a component with DI support.

    The function being decorated should have three parameters, ``self`` representing
    the :class:`disnake.ui.View`, the :class:`disnake.ui.Button` that was
    interacted with, and the :class:`disnake.MessageInteraction`.

    .. note::

        Link/Premium buttons cannot be created with this function,
        since these buttons do not have a callback associated with them.
        Consider creating a :class:`Button` manually instead, and adding it
        using :meth:`View.add_item`.

    Parameters
    ----------
    cls: Callable[..., :class:`Button`]
        A callable (may be a :class:`Button` subclass) to create a new instance of this component.
        If provided, the other parameters described below do not apply.
        Instead, this decorator will accept the same keywords as the passed callable/class does.

        .. versionadded:: 2.6
    label: Optional[:class:`str`]
        The label of the button, if any.
    custom_id: Optional[:class:`str`]
        The ID of the button that gets received during an interaction.
        It is recommended not to set this parameter to prevent conflicts.
    style: :class:`.ButtonStyle`
        The style of the button. Defaults to :attr:`.ButtonStyle.grey`.
    disabled: :class:`bool`
        Whether the button is disabled. Defaults to ``False``.
    emoji: Optional[Union[:class:`str`, :class:`.Emoji`, :class:`.PartialEmoji`]]
        The emoji of the button. This can be in string form or a :class:`.PartialEmoji`
        or a full :class:`.Emoji`.
    id: :class:`int`
        The numeric identifier for the component. Must be unique within the message.
        If set to ``0`` (the default) when sending a component, the API will assign
        sequential identifiers to the components in the message.

        .. versionadded:: 2.11
    row: Optional[:class:`int`]
        The relative row this button belongs to. A Discord component can only have 5
        rows. By default, items are arranged automatically into those 5 rows. If you'd
        like to control the relative positioning of the row then passing an index is advised.
        For example, row=1 will show up before row=2. Defaults to ``None``, which is automatic
        ordering. The row number must be between 0 and 4 (i.e. zero indexed).
    """
    def decorator(func: ItemCallbackType[V_co, B_co]) -> DecoratedItem[B_co]:
        func = wrap_injector(func)
        return ui.button(cls, **kwargs)(func)

    return decorator
