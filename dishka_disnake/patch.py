from dishka_disnake.injector.util import extract_fromdishka
from dishka_disnake.state_management import State


def patch_disnake() -> None:
    from dishka_disnake.base.sign import rebuild_annotations, rebuild_signature
    from disnake.ext.commands import params as disnake_params, slash_core

    _original_expand_params = disnake_params.expand_params

    def _patched_expand_params(command):
        callback = command.callback
        callback.__dishka_annotations__ = callback.__annotations__.copy()
        callback.__annotations__ = rebuild_annotations(callback)
        callback.__signature__ = rebuild_signature(callback)
        result = _original_expand_params(command)
        dishka_params = {
            name for name, ann in callback.__dishka_annotations__.items()
            if extract_fromdishka(ann) is not None
        }
        return [o for o in result if o.name not in dishka_params]

    disnake_params.expand_params = _patched_expand_params  # type: ignore[assignment]
    slash_core.expand_params = _patched_expand_params  # type: ignore[assignment]

    State.disnake_patched = True


def check_disnake_patched() -> None:
    if getattr(State, "disnake_patched", False) is False:
        raise RuntimeError("Setup dishka first for using DishkaCog")
