from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Dict, Optional, Sequence, Union

from disnake.ext import commands
from disnake.flags import ApplicationInstallTypes, InteractionContextTypes
from disnake.permissions import Permissions
from disnake.ext.commands.ctx_menus_core import (
    InvokableMessageCommand,
    InvokableUserCommand,
)

from dishka_disnake.injector.wrap._async import wrap_injector

if TYPE_CHECKING:
    from typing_extensions import ParamSpec

    from disnake.i18n import LocalizedOptional
    from disnake.interactions import (
        MessageCommandInteraction,
        UserCommandInteraction,
    )

    from disnake.ext.commands.base_core import CogT, InteractionCommandCallback

    P = ParamSpec("P")


def user_command(
    *,
    name: LocalizedOptional = None,
    dm_permission: Optional[bool] = None,  # deprecated
    default_member_permissions: Optional[Union[Permissions, int]] = None,
    nsfw: Optional[bool] = None,
    install_types: Optional[ApplicationInstallTypes] = None,
    contexts: Optional[InteractionContextTypes] = None,
    guild_ids: Optional[Sequence[int]] = None,
    auto_sync: Optional[bool] = None,
    extras: Optional[Dict[str, Any]] = None,
    **kwargs: Any,
) -> Callable[
    [InteractionCommandCallback[CogT, UserCommandInteraction, P]], InvokableUserCommand
]:
    """A shortcut decorator that builds a user command.

    Parameters
    ----------
    name: Optional[Union[:class:`str`, :class:`.Localized`]]
        The name of the user command (defaults to the function name).

        .. versionchanged:: 2.5
            Added support for localizations.

    dm_permission: :class:`bool`
        Whether this command can be used in DMs.
        Defaults to ``True``.

        .. deprecated:: 2.10
            Use ``contexts`` instead.
            This is equivalent to the :attr:`.InteractionContextTypes.bot_dm` flag.

    default_member_permissions: Optional[Union[:class:`.Permissions`, :class:`int`]]
        The default required permissions for this command.
        See :attr:`.ApplicationCommand.default_member_permissions` for details.

        .. versionadded:: 2.5

    nsfw: :class:`bool`
        Whether this command is :ddocs:`age-restricted <interactions/application-commands#agerestricted-commands>`.
        Defaults to ``False``.

        .. versionadded:: 2.8

    install_types: Optional[:class:`.ApplicationInstallTypes`]
        The installation types where the command is available.
        Defaults to :attr:`.ApplicationInstallTypes.guild` only.
        Only available for global commands.

        See :ref:`app_command_contexts` for details.

        .. versionadded:: 2.10

    contexts: Optional[:class:`.InteractionContextTypes`]
        The interaction contexts where the command can be used.
        Only available for global commands.

        See :ref:`app_command_contexts` for details.

        .. versionadded:: 2.10

    auto_sync: :class:`bool`
        Whether to automatically register the command. Defaults to ``True``.
    guild_ids: Sequence[:class:`int`]
        If specified, the client will register the command in these guilds.
        Otherwise, this command will be registered globally.
    extras: Dict[:class:`str`, Any]
        A dict of user provided extras to attach to the command.

        .. note::
            This object may be copied by the library.

        .. versionadded:: 2.5

    Returns
    -------
    Callable[..., :class:`InvokableUserCommand`]
        A decorator that converts the provided method into an InvokableUserCommand and returns it.
    """

    def decorator(
        func: InteractionCommandCallback[CogT, UserCommandInteraction, P],
    ) -> InvokableUserCommand:
        func = wrap_injector(func)
        return commands.user_command(
            name=name,
            dm_permission=dm_permission,
            default_member_permissions=default_member_permissions,
            nsfw=nsfw,
            install_types=install_types,
            contexts=contexts,
            guild_ids=guild_ids,
            auto_sync=auto_sync,
            extras=extras,
            **kwargs,
        )(func)

    return decorator


def message_command(
    *,
    name: LocalizedOptional = None,
    dm_permission: Optional[bool] = None,  # deprecated
    default_member_permissions: Optional[Union[Permissions, int]] = None,
    nsfw: Optional[bool] = None,
    install_types: Optional[ApplicationInstallTypes] = None,
    contexts: Optional[InteractionContextTypes] = None,
    guild_ids: Optional[Sequence[int]] = None,
    auto_sync: Optional[bool] = None,
    extras: Optional[Dict[str, Any]] = None,
    **kwargs: Any,
) -> Callable[
    [InteractionCommandCallback[CogT, MessageCommandInteraction, P]],
    InvokableMessageCommand,
]:
    """A shortcut decorator that builds a message command.

    Parameters
    ----------
    name: Optional[Union[:class:`str`, :class:`.Localized`]]
        The name of the message command (defaults to the function name).

        .. versionchanged:: 2.5
            Added support for localizations.

    dm_permission: :class:`bool`
        Whether this command can be used in DMs.
        Defaults to ``True``.

        .. deprecated:: 2.10
            Use ``contexts`` instead.
            This is equivalent to the :attr:`.InteractionContextTypes.bot_dm` flag.

    default_member_permissions: Optional[Union[:class:`.Permissions`, :class:`int`]]
        The default required permissions for this command.
        See :attr:`.ApplicationCommand.default_member_permissions` for details.

        .. versionadded:: 2.5

    nsfw: :class:`bool`
        Whether this command is :ddocs:`age-restricted <interactions/application-commands#agerestricted-commands>`.
        Defaults to ``False``.

        .. versionadded:: 2.8

    install_types: Optional[:class:`.ApplicationInstallTypes`]
        The installation types where the command is available.
        Defaults to :attr:`.ApplicationInstallTypes.guild` only.
        Only available for global commands.

        See :ref:`app_command_contexts` for details.

        .. versionadded:: 2.10

    contexts: Optional[:class:`.InteractionContextTypes`]
        The interaction contexts where the command can be used.
        Only available for global commands.

        See :ref:`app_command_contexts` for details.

        .. versionadded:: 2.10

    auto_sync: :class:`bool`
        Whether to automatically register the command. Defaults to ``True``.
    guild_ids: Sequence[:class:`int`]
        If specified, the client will register the command in these guilds.
        Otherwise, this command will be registered globally.
    extras: Dict[:class:`str`, Any]
        A dict of user provided extras to attach to the command.

        .. note::
            This object may be copied by the library.

        .. versionadded:: 2.5

    Returns
    -------
    Callable[..., :class:`InvokableMessageCommand`]
        A decorator that converts the provided method into an InvokableMessageCommand and then returns it.
    """

    def decorator(
        func: InteractionCommandCallback[CogT, MessageCommandInteraction, P],
    ) -> InvokableMessageCommand:
        func = wrap_injector(func)
        return commands.message_command(
            name=name,
            dm_permission=dm_permission,
            default_member_permissions=default_member_permissions,
            nsfw=nsfw,
            install_types=install_types,
            contexts=contexts,
            guild_ids=guild_ids,
            auto_sync=auto_sync,
            extras=extras,
            **kwargs,
        )(func)

    return decorator
