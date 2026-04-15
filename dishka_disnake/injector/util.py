from typing import Annotated, Any, get_args, get_origin

from dishka import FromDishka
from dishka.entities.key import _FromComponent


def extract_fromdishka(annotation: object) -> Any | None:
    if get_origin(annotation) is not Annotated:
        return None

    base, *metadata = get_args(annotation)

    for meta in metadata:
        if isinstance(meta, _FromComponent):
            return base
        if isinstance(meta, FromDishka):  # deprecated: Annotated[int, FromDishka()];  # type: ignore[arg-type]
            return base

    return None
