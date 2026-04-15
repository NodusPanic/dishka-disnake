from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Generic,
    List,
    Optional,
    TypeVar,
    Union,
    overload,
)

from disnake import MessageInteraction, ui
from disnake.components import SelectOption
from disnake.ui.select.base import P, V_co

from dishka_disnake.base.ui_component import WrappedDishkaComponent
from dishka_disnake.injector.wrap._async import wrap_injector

if TYPE_CHECKING:
    from disnake.ui.item import DecoratedItem, ItemCallbackType


__all__ = (
    "StringSelect",
    "Select",
    "string_select",
    "select",
)


SelectOptionInput = Union[List[SelectOption], List[str], Dict[str, str]]


class StringSelect(WrappedDishkaComponent[MessageInteraction], ui.StringSelect[V_co], Generic[V_co]):
    """Represents a UI string select menu with DI support.

    This is usually represented as a drop down menu.

    In order to get the selected items that the user has chosen, use :attr:`.values`.

    .. versionadded:: 2.0

    .. versionchanged:: 2.7
        Renamed from ``Select`` to ``StringSelect``.

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
    options: Union[List[:class:`disnake.SelectOption`], List[:class:`str`], Dict[:class:`str`, :class:`str`]]
        A list of options that can be selected in this menu. Use explicit :class:`.SelectOption`\\s
        for fine-grained control over the options. Alternatively, a list of strings will be treated
        as a list of labels, and a dict will be treated as a mapping of labels to values.

        .. versionchanged:: 2.5
            Now also accepts a list of str or a dict of str to str, which are then appropriately parsed as
            :class:`.SelectOption` labels and values.

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
    values: List[:class:`str`]
        A list of values that have been selected by the user.
    """


S_co = TypeVar("S_co", bound="StringSelect", covariant=True)


@overload
def string_select(
    *,
    placeholder: Optional[str] = None,
    custom_id: str = ...,
    min_values: int = 1,
    max_values: int = 1,
    options: SelectOptionInput = ...,
    disabled: bool = False,
    id: int = 0,
    row: Optional[int] = None,
) -> Callable[..., DecoratedItem[StringSelect[V_co]]]: ...


@overload
def string_select(
    cls: Callable[P, S_co], *_: P.args, **kwargs: P.kwargs
) -> Callable[..., DecoratedItem[S_co]]: ...


def string_select(
    cls: Callable[..., S_co] = StringSelect[Any], **kwargs: Any
) -> Callable[..., DecoratedItem[S_co]]:
    """A decorator that attaches a string select menu to a component.

    The function being decorated should have three parameters, ``self`` representing
    the :class:`disnake.ui.View`, the :class:`disnake.ui.StringSelect` that was
    interacted with, and the :class:`disnake.MessageInteraction`.

    In order to get the selected items that the user has chosen within the callback
    use :attr:`StringSelect.values`.

    .. versionchanged:: 2.7
        Renamed from ``select`` to ``string_select``.

    Parameters
    ----------
    cls: Callable[..., :class:`StringSelect`]
        A callable (may be a :class:`StringSelect` subclass) to create a new instance of this component.
        If provided, the other parameters described below do not apply.
        Instead, this decorator will accept the same keywords as the passed callable/class does.

        .. versionadded:: 2.6
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
    options: Union[List[:class:`disnake.SelectOption`], List[:class:`str`], Dict[:class:`str`, :class:`str`]]
        A list of options that can be selected in this menu. Use explicit :class:`.SelectOption`\\s
        for fine-grained control over the options. Alternatively, a list of strings will be treated
        as a list of labels, and a dict will be treated as a mapping of labels to values.

        .. versionchanged:: 2.5
            Now also accepts a list of str or a dict of str to str, which are then appropriately parsed as
            :class:`.SelectOption` labels and values.

    disabled: :class:`bool`
        Whether the select is disabled. Defaults to ``False``.
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
        return ui.string_select(cls, **kwargs)(func)

    return decorator


Select = StringSelect  # backwards compatibility
select = string_select  # backwards compatibility
