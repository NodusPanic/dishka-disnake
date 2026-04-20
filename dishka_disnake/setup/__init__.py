from dishka import AsyncContainer, Container

from dishka_disnake import patch
from dishka_disnake.state_management import State


def setup_dishka(container: AsyncContainer | Container) -> None:
    """
    Setup dishka for disnake
    """
    State.container = container
    State.sync_container = container
    patch.patch_disnake()
