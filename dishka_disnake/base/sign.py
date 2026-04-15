from collections.abc import Callable
from inspect import Signature, signature, Parameter

from dishka_disnake.injector.util import extract_fromdishka


def rebuild_signature(func: Callable) -> Signature:
    sig = signature(func)
    params: list[Parameter] = []

    params_ = sig.parameters.values()
    for param in params_:
        if param.name == "self":
            params.append(param)
            continue

        if param.kind in (
            Parameter.VAR_POSITIONAL,
            Parameter.VAR_KEYWORD,
        ):
            params.append(param)
            continue

        if not extract_fromdishka(param.annotation):
            params.append(param)
            continue

    return sig.replace(parameters=params)
