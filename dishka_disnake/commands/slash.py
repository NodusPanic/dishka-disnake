from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Dict, List, Optional, Sequence, Any, Union

from disnake.ext.commands import InvokableSlashCommand as OriginalInvokableSlashCommand
from disnake import (
    Permissions,
    ApplicationInstallTypes,
    InteractionContextTypes,
    Option,
    utils,
)
from disnake.ext.commands.slash_core import (
    SubCommand,
    SubCommandGroup as OriginalSubCommandGroup,
)

if TYPE_CHECKING:
    from disnake.i18n import LocalizedOptional

    from disnake.ext.commands.base_core import CommandCallback

from dishka_disnake.injector.wrap._async import wrap_injector


class SubCommandGroup(OriginalSubCommandGroup):
    def sub_command(
        self,
        name: LocalizedOptional = None,
        description: LocalizedOptional = None,
        options: Optional[list] = None,
        connectors: Optional[dict] = None,
        extras: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Callable[[CommandCallback], SubCommand]:
        """A decorator that creates a subcommand in the subcommand group.
        Parameters are the same as in :class:`InvokableSlashCommand.sub_command`

        Returns
        -------
        Callable[..., :class:`SubCommand`]
            A decorator that converts the provided method into a SubCommand, adds it to the bot, then returns it.
        """

        def decorator(func: Callable) -> SubCommand:
            func = wrap_injector(func)
            new_func = SubCommand(
                func,
                self,
                name=name,
                description=description,
                options=options,
                connectors=connectors,
                extras=extras,
                **kwargs,
            )
            self.children[new_func.name] = new_func
            self.option.options.append(new_func.option)
            return new_func

        return decorator


class InvokableSlashCommand(OriginalInvokableSlashCommand):
    def sub_command(
        self,
        name: LocalizedOptional = None,
        description: LocalizedOptional = None,
        options: Optional[list] = None,
        connectors: Optional[dict] = None,
        extras: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Callable[[CommandCallback], SubCommand]:
        """A decorator that creates a subcommand under the base command.

        Parameters
        ----------
        name: Optional[Union[:class:`str`, :class:`.Localized`]]
            The name of the subcommand (defaults to function name).

            .. versionchanged:: 2.5
                Added support for localizations.

        description: Optional[Union[:class:`str`, :class:`.Localized`]]
            The description of the subcommand.

            .. versionchanged:: 2.5
                Added support for localizations.

        options: List[:class:`.Option`]
            the options of the subcommand for registration in API
        connectors: Dict[:class:`str`, :class:`str`]
            which function param states for each option. If the name
            of an option already matches the corresponding function param,
            you don't have to specify the connectors. Connectors template:
            ``{"option-name": "param_name", ...}``
        extras: Dict[:class:`str`, Any]
            A dict of user provided extras to attach to the subcommand.

            .. note::
                This object may be copied by the library.

            .. versionadded:: 2.5

        Returns
        -------
        Callable[..., :class:`SubCommand`]
            A decorator that converts the provided method into a :class:`SubCommand`, adds it to the bot, then returns it.
        """

        def decorator(func: Callable) -> SubCommand:
            func = wrap_injector(func)
            if len(self.children) == 0 and len(self.body.options) > 0:
                self.body.options = []
            new_func = SubCommand(
                func,
                self,
                name=name,
                description=description,
                options=options,
                connectors=connectors,
                extras=extras,
                **kwargs,
            )
            self.children[new_func.name] = new_func
            self.body.options.append(new_func.option)
            return new_func

        return decorator

    def sub_command_group(
        self,
        name: LocalizedOptional = None,
        extras: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Callable[[CommandCallback], SubCommandGroup]:
        """A decorator that creates a subcommand group under the base command.

        Parameters
        ----------
        name: Optional[Union[:class:`str`, :class:`.Localized`]]
            The name of the subcommand group (defaults to function name).

            .. versionchanged:: 2.5
                Added support for localizations.
        extras: Dict[:class:`str`, Any]
            A dict of user provided extras to attach to the subcommand group.

            .. note::
                This object may be copied by the library.

            .. versionadded:: 2.5

        Returns
        -------
        Callable[..., :class:`SubCommandGroup`]
            A decorator that converts the provided method into a :class:`SubCommandGroup`, adds it to the bot, then returns it.
        """

        def decorator(func: Callable) -> SubCommandGroup:
            func = wrap_injector(func)
            if len(self.children) == 0 and len(self.body.options) > 0:
                self.body.options = []
            new_func = SubCommandGroup(
                func,
                self,
                name=name,
                extras=extras,
                **kwargs,
            )
            self.children[new_func.name] = new_func
            self.body.options.append(new_func.option)
            return new_func

        return decorator


def slash_command(
    *,
    name: LocalizedOptional = None,
    description: LocalizedOptional = None,
    dm_permission: Optional[bool] = None,  # deprecated
    default_member_permissions: Optional[Union[Permissions, int]] = None,
    nsfw: Optional[bool] = None,
    install_types: Optional[ApplicationInstallTypes] = None,
    contexts: Optional[InteractionContextTypes] = None,
    options: Optional[List[Option]] = None,
    guild_ids: Optional[Sequence[int]] = None,
    connectors: Optional[Dict[str, str]] = None,
    auto_sync: Optional[bool] = None,
    extras: Optional[Dict[str, Any]] = None,
    **kwargs: Any,
) -> Callable[[CommandCallback], InvokableSlashCommand]:
    """A decorator that builds a slash command.

    Parameters
    ----------
    auto_sync: :class:`bool`
        Whether to automatically register the command. Defaults to ``True``.
    name: Optional[Union[:class:`str`, :class:`.Localized`]]
        The name of the slash command (defaults to function name).

        .. versionchanged:: 2.5
            Added support for localizations.

    description: Optional[Union[:class:`str`, :class:`.Localized`]]
        The description of the slash command. It will be visible in Discord.

        .. versionchanged:: 2.5
            Added support for localizations.

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

    options: List[:class:`.Option`]
        The list of slash command options. The options will be visible in Discord.
        This is the old way of specifying options. Consider using :ref:`param_syntax` instead.
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

    guild_ids: List[:class:`int`]
        If specified, the client will register the command in these guilds.
        Otherwise, this command will be registered globally.
    connectors: Dict[:class:`str`, :class:`str`]
        Binds function names to option names. If the name
        of an option already matches the corresponding function param,
        you don't have to specify the connectors. Connectors template:
        ``{"option-name": "param_name", ...}``.
        If you're using :ref:`param_syntax`, you don't need to specify this.
    extras: Dict[:class:`str`, Any]
        A dict of user provided extras to attach to the command.

        .. note::
            This object may be copied by the library.

        .. versionadded:: 2.5

    Returns
    -------
    Callable[..., :class:`InvokableSlashCommand`]
        A decorator that converts the provided method into an InvokableSlashCommand and returns it.
    """

    def decorator(func: CommandCallback) -> InvokableSlashCommand:
        func = wrap_injector(func)
        if not utils.iscoroutinefunction(func):
            raise TypeError(f"<{func.__qualname__}> must be a coroutine function")  # type: ignore[attr-defined]
        if hasattr(func, "__command_flag__"):
            raise TypeError("Callback is already a command.")
        if guild_ids and not all(isinstance(guild_id, int) for guild_id in guild_ids):
            raise ValueError("guild_ids must be a sequence of int.")
        return InvokableSlashCommand(
            func,
            name=name,
            description=description,
            options=options,
            dm_permission=dm_permission,
            default_member_permissions=default_member_permissions,
            nsfw=nsfw,
            install_types=install_types,
            contexts=contexts,
            guild_ids=guild_ids,
            connectors=connectors,
            auto_sync=auto_sync,
            extras=extras,
            **kwargs,
        )

    return decorator
