from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Generic,
    Optional,
    Sequence,
    TypeVar,
    Union,
    overload,
)

from disnake import MessageInteraction, ui
from disnake.member import Member
from disnake.role import Role
from disnake.user import User
from disnake.ui.select.base import (
    P,
    SelectDefaultValueMultiInputType,
    V_co,
)

if TYPE_CHECKING:
    from disnake.ui.item import DecoratedItem, ItemCallbackType

from dishka_disnake.base.ui_component import WrappedDishkaComponent
from dishka_disnake.injector.wrap._async import wrap_injector

__all__ = ("MentionableSelect", "mentionable_select")


class MentionableSelect(WrappedDishkaComponent[MessageInteraction], ui.MentionableSelect[V_co], Generic[V_co]):
    """Represents a UI mentionable (user/member/role) select menu.

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
    default_values: Optional[Sequence[Union[:class:`~disnake.User`, :class:`.Member`, :class:`.Role`, :class:`.SelectDefaultValue`]]]
        The list of values (users/roles) that are selected by default.
        If set, the number of items must be within the bounds set by ``min_values`` and ``max_values``.

        Note that unlike other select menu types, this does not support :class:`.Object`\\s due to ambiguities.

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
    values: List[Union[:class:`~disnake.User`, :class:`.Member`, :class:`.Role`]]
        A list of users, members and/or roles that have been selected by the user.
    """


S_co = TypeVar("S_co", bound="MentionableSelect", covariant=True)


@overload
def mentionable_select(
    *,
    placeholder: Optional[str] = None,
    custom_id: str = ...,
    min_values: int = 1,
    max_values: int = 1,
    disabled: bool = False,
    default_values: Optional[
        Sequence[SelectDefaultValueMultiInputType[Union[User, Member, Role]]]
    ] = None,
    id: int = 0,
    row: Optional[int] = None,
) -> Callable[..., DecoratedItem[MentionableSelect[V_co]],
]: ...


@overload
def mentionable_select(
    cls: Callable[P, S_co], *_: P.args, **kwargs: P.kwargs
) -> Callable[..., DecoratedItem[S_co]]: ...


def mentionable_select(
    cls: Callable[..., S_co] = MentionableSelect[Any], **kwargs: Any
) -> Callable[..., DecoratedItem[S_co]]:
    """A decorator that attaches a mentionable (user/member/role) select menu to a component.

    The function being decorated should have three parameters, ``self`` representing
    the :class:`disnake.ui.View`, the :class:`disnake.ui.MentionableSelect` that was
    interacted with, and the :class:`disnake.MessageInteraction`.

    In order to get the selected items that the user has chosen within the callback
    use :attr:`MentionableSelect.values`.

    .. versionadded:: 2.7

    Parameters
    ----------
    cls: Callable[..., :class:`MentionableSelect`]
        A callable (may be a :class:`MentionableSelect` subclass) to create a new instance of this component.
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
    default_values: Optional[Sequence[Union[:class:`~disnake.User`, :class:`.Member`, :class:`.Role`, :class:`.SelectDefaultValue`]]]
        The list of values (users/roles) that are selected by default.
        If set, the number of items must be within the bounds set by ``min_values`` and ``max_values``.

        Note that unlike other select menu types, this does not support :class:`.Object`\\s due to ambiguities.

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
        return ui.mentionable_select(cls, **kwargs)(func)

    return decorator
