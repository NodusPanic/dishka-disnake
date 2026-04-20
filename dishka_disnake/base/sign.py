from collections.abc import Callable
from inspect import Signature, signature, Parameter, _empty

from dishka_disnake.injector.util import extract_fromdishka


def rebuild_signature(func: Callable) -> Signature:
    sig = signature(func)
    params: list[Parameter] = []
    for param in sig.parameters.values():
        if param.name == "self":
            params.append(param)
            continue
        if param.kind in (Parameter.VAR_POSITIONAL, Parameter.VAR_KEYWORD):
            params.append(param)
            continue
        if not extract_fromdishka(param.annotation):
            params.append(param)
    return sig.replace(parameters=params)


def rebuild_annotations(func: Callable) -> dict[str, object]:
    return {
        name: ann
        for name, ann in func.__annotations__.items()
        if ann is not _empty and extract_fromdishka(ann) is None
    }
