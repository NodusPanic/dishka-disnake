from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Generic,
    List,
    Optional,
    Sequence,
    TypeVar,
    overload,
)

from disnake import MessageInteraction, ui
from disnake.enums import ChannelType
from disnake.ui.select.base import P, SelectDefaultValueInputType, V_co

if TYPE_CHECKING:
    from disnake.abc import AnyChannel
    from disnake.ui.item import DecoratedItem, ItemCallbackType

from dishka_disnake.ui.base import WrappedDishkaComponent
from dishka_disnake.injector.wrap._async import wrap_injector

__all__ = (
    "ChannelSelect",
    "channel_select",
)


class ChannelSelect(WrappedDishkaComponent[MessageInteraction], ui.ChannelSelect[V_co], Generic[V_co]):
    """Represents a UI channel select menu.

    This is usually represented as a drop down menu.

    In order to get the selected items that the user has chosen, use :attr:`.values`.

    .. versionadded:: 2.7

    Parameters
    ----------
    custom_id: :class:`str`
        The ID of the select menu that gets received during an interaction.
        If not given then one is generated for you.
    placeholder: Optional[:class:`str`]
        The placeholder text that is shown if nothing is selected, if any.
    min_values: :class:`int`
        The minimum number of items that must be chosen for this select menu.
        Defaults to 1 and must be between 1 and 25.
    max_values: :class:`int`
        The maximum number of items that must be chosen for this select menu.
        Defaults to 1 and must be between 1 and 25.
    disabled: :class:`bool`
        Whether the select is disabled.
    channel_types: Optional[List[:class:`.ChannelType`]]
        The list of channel types that can be selected in this select menu.
        Defaults to all types (i.e. ``None``).
    default_values: Optional[Sequence[Union[:class:`.abc.GuildChannel`, :class:`.Thread`, :class:`.abc.PrivateChannel`, :class:`.PartialMessageable`, :class:`.SelectDefaultValue`, :class:`.Object`]]]
        The list of values (channels) that are selected by default.
        If set, the number of items must be within the bounds set by ``min_values`` and ``max_values``.

        .. versionadded:: 2.10
    required: :class:`bool`
        Whether the select menu is required. Only applies to components in modals.
        Defaults to ``True``.

        .. versionadded:: 2.11
    id: :class:`int`
        The numeric identifier for the component. Must be unique within the message.
        If set to ``0`` (the default) when sending a component, the API will assign
        sequential identifiers to the components in the message.

        .. versionadded:: 2.11
    row: Optional[:class:`int`]
        The relative row this select menu belongs to. A Discord component can only have 5
        rows. By default, items are arranged automatically into those 5 rows. If you'd
        like to control the relative positioning of the row then passing an index is advised.
        For example, row=1 will show up before row=2. Defaults to ``None``, which is automatic
        ordering. The row number must be between 0 and 4 (i.e. zero indexed).

    Attributes
    ----------
    values: List[Union[:class:`.abc.GuildChannel`, :class:`.Thread`, :class:`.abc.PrivateChannel`, :class:`.PartialMessageable`]]
        A list of channels that have been selected by the user.
    """


S_co = TypeVar("S_co", bound="ChannelSelect", covariant=True)


@overload
def channel_select(
    *,
    placeholder: Optional[str] = None,
    custom_id: str = ...,
    min_values: int = 1,
    max_values: int = 1,
    disabled: bool = False,
    channel_types: Optional[List[ChannelType]] = None,
    default_values: Optional[Sequence[SelectDefaultValueInputType[AnyChannel]]] = None,
    id: int = 0,
    row: Optional[int] = None,
) -> Callable[..., DecoratedItem[ChannelSelect[V_co]]]: ...


@overload
def channel_select(
    cls: Callable[P, S_co], *_: P.args, **kwargs: P.kwargs
) -> Callable[..., DecoratedItem[S_co]]: ...


def channel_select(
    cls: Callable[..., S_co] = ChannelSelect[Any], **kwargs: Any
) -> Callable[..., DecoratedItem[S_co]]:
    """A decorator that attaches a channel select menu to a component.

    The function being decorated should have three parameters, ``self`` representing
    the :class:`disnake.ui.View`, the :class:`disnake.ui.ChannelSelect` that was
    interacted with, and the :class:`disnake.MessageInteraction`.

    In order to get the selected items that the user has chosen within the callback
    use :attr:`ChannelSelect.values`.

    .. versionadded:: 2.7

    Parameters
    ----------
    cls: Callable[..., :class:`ChannelSelect`]
        A callable (may be a :class:`ChannelSelect` subclass) to create a new instance of this component.
        If provided, the other parameters described below do not apply.
        Instead, this decorator will accept the same keywords as the passed callable/class does.
    placeholder: Optional[:class:`str`]
        The placeholder text that is shown if nothing is selected, if any.
    custom_id: :class:`str`
        The ID of the select menu that gets received during an interaction.
        It is recommended not to set this parameter to prevent conflicts.
    min_values: :class:`int`
        The minimum number of items that must be chosen for this select menu.
        Defaults to 1 and must be between 1 and 25.
    max_values: :class:`int`
        The maximum number of items that must be chosen for this select menu.
        Defaults to 1 and must be between 1 and 25.
    disabled: :class:`bool`
        Whether the select is disabled. Defaults to ``False``.
    channel_types: Optional[List[:class:`.ChannelType`]]
        The list of channel types that can be selected in this select menu.
        Defaults to all types (i.e. ``None``).
    default_values: Optional[Sequence[Union[:class:`.abc.GuildChannel`, :class:`.Thread`, :class:`.abc.PrivateChannel`, :class:`.PartialMessageable`, :class:`.SelectDefaultValue`, :class:`.Object`]]]
        The list of values (channels) that are selected by default.
        If set, the number of items must be within the bounds set by ``min_values`` and ``max_values``.

        .. versionadded:: 2.10
    id: :class:`int`
        The numeric identifier for the component. Must be unique within the message.
        If set to ``0`` (the default) when sending a component, the API will assign
        sequential identifiers to the components in the message.

        .. versionadded:: 2.11
    row: Optional[:class:`int`]
        The relative row this select menu belongs to. A Discord component can only have 5
        rows. By default, items are arranged automatically into those 5 rows. If you'd
        like to control the relative positioning of the row then passing an index is advised.
        For example, row=1 will show up before row=2. Defaults to ``None``, which is automatic
        ordering. The row number must be between 0 and 4 (i.e. zero indexed).
    """

    def decorator(func: ItemCallbackType[V_co, S_co]) -> DecoratedItem[S_co]:
        func = wrap_injector(func)
        return ui.channel_select(cls, **kwargs)(func)

    return decorator
