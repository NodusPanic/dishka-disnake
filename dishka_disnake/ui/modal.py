from disnake import ModalInteraction, ui

from dishka_disnake.base.ui_component import WrappedDishkaComponent


class Modal(WrappedDishkaComponent[ModalInteraction], ui.Modal):
    """Represents a UI Modal.

    .. versionadded:: 2.4

    Parameters
    ----------
    title: :class:`str`
        The title of the modal.
    components: |modal_components_type|
        The components to display in the modal. A maximum of 5.

        Currently supports the following components:
            - :class:`.ui.TextDisplay`
            - :class:`.ui.TextInput`, in a :class:`.ui.Label`
            - select menus (e.g. :class:`.ui.StringSelect`), in a :class:`.ui.Label`

        .. versionchanged:: 2.11
            Using action rows in modals or passing :class:`.ui.TextInput` directly
            (which implicitly wraps it in an action row) is deprecated.
            Use :class:`.ui.TextInput` inside a :class:`.ui.Label` instead.

    custom_id: :class:`str`
        The custom ID of the modal. This is usually not required.
        If not given, then a unique one is generated for you.

        .. note::
            :class:`Modal`\\s are identified based on the user ID that triggered the
            modal, and this ``custom_id``.
            This can result in collisions when a user opens a modal with the same ``custom_id`` on
            two separate devices, for example.

            To avoid such issues, consider not specifying a ``custom_id`` to use an automatically generated one,
            or include a unique value in the custom ID (e.g. the original interaction ID).

    timeout: :class:`float`
        The time to wait until the modal is removed from cache, if no interaction is made.
        Modals without timeouts are not supported, since there's no event for when a modal is closed.
        Defaults to 600 seconds.
    """

